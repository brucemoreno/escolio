"""Testes do adaptador DocumentoIngerido -> InputItem contra o documento
real de data/dev/ — mesma disciplina de tests/ingestao/test_parser.py:
estrutura e invariantes, não texto literal.
"""

import re

from escolio.adaptadores.ingestao_para_input_item import (
    input_item_de_documento,
    material_id_de_documento,
)
from escolio.contrato.vocabulario import ConsistencyStatus, InputType
from tests.ingestao.conftest import requer_pdf_dev

PADRAO_MATERIAL_ID = re.compile(r"^MAT-DOC-[0-9a-f]{8}$")
PADRAO_INPUT_ID = re.compile(r"^INP-[0-9a-f]{8}$")

# Os quatro eixos do [P08 §4] são independentes; rótulo de um não vale no campo de outro.
# Duplicado de tests/contrato/test_entrada.py de propósito: cada pacote de teste trava o
# seu lado sem importar do outro.
EIXO_CONFIANCA_P08 = {
    "CONFIAVEL_CANONICO",
    "CONFIAVEL_NAO_CANONICO",
    "NAO_CONFIAVEL",
    "SUSPEITO",
    "ORIGEM_DESCONHECIDA",
}
EIXO_ESTADO_P08 = {
    "ORIGINAL",
    "COPIA_VERIFICADA",
    "DERIVADO",
    "EM_ANALISE",
    "HOMOLOGADO",
    "CONGELADO",
    "SUPERADO",
    "ARQUIVADO",
    "DESTINADO_A_DESCARTE",
}


@requer_pdf_dev
class TestMaterialId:
    def test_segue_o_padrao(self, documento):
        assert PADRAO_MATERIAL_ID.match(material_id_de_documento(documento))

    def test_e_estavel_entre_chamadas(self, documento):
        assert material_id_de_documento(documento) == material_id_de_documento(documento)

    def test_nao_depende_do_caminho_do_arquivo(self, documento):
        # P19 §10: "não depender do nome do arquivo" / "permanecer estável
        # entre cópias" — troca só o caminho, hash_documento (derivado do
        # conteúdo binário) não muda, logo material_id também não muda.
        import copy

        copia = copy.copy(documento)
        copia.caminho_original = "/outro/caminho/copia.pdf"
        assert material_id_de_documento(copia) == material_id_de_documento(documento)


@requer_pdf_dev
class TestInputItemDeDocumento:
    def test_tipo_e_documento(self, documento):
        item = input_item_de_documento(documento)
        assert item.type == InputType.DOCUMENT

    def test_input_id_segue_padrao_proprio_distinto_de_material_id(self, documento):
        item = input_item_de_documento(documento)
        assert PADRAO_INPUT_ID.match(item.input_id)
        assert item.input_id != material_id_de_documento(documento)

    def test_material_id_fica_em_integrity_reference(self, documento):
        item = input_item_de_documento(documento)
        assert item.provenance.integrity_reference == material_id_de_documento(documento)

    def test_provenance_source_e_caminho_original(self, documento):
        item = input_item_de_documento(documento)
        assert item.provenance.source == documento.caminho_original

    def test_titulo_vem_dos_metadados_extraidos(self, documento):
        item = input_item_de_documento(documento)
        assert item.title == documento.metadados.titulo

    def test_sem_autoridade_operacional_por_padrao(self, documento):
        # P08 §2 / P09 §6.1: conteúdo documental nunca vira comando por si.
        item = input_item_de_documento(documento)
        assert item.authority.has_operational_authority is False

    def test_trust_pertence_ao_eixo_de_confianca_do_p08(self, documento):
        # P09 §6.1: item sem proveniência suficiente é ORIGEM_DESCONHECIDA. O código sabe
        # de onde leu o arquivo, não quem o produziu — DTA-16, DECISAO_TECNICA_ABERTA.
        item = input_item_de_documento(documento)
        assert item.classification.trust == "ORIGEM_DESCONHECIDA"
        assert item.classification.trust in EIXO_CONFIANCA_P08

    def test_trust_nao_importa_vocabulario_do_p05(self, documento):
        # Regressão de BL-016: "NAO_AVALIADA" é valor de Sufficiency/Confidence do P05.
        item = input_item_de_documento(documento)
        assert item.classification.trust != "NAO_AVALIADA"

    def test_state_e_defeito_conhecido_e_preservado(self, documento):
        # Caracteriza DEFEITO, não requisito — CO-013. ORIGEM_DESCONHECIDA é rótulo do
        # eixo de confiança [P08 §4.1], não de estado; daí a segunda asserção afirmar que
        # o valor está FORA do eixo correto. Preservado porque [P09 §6] declara
        # `state: string` sem `| null` e nenhum dos nove estados significa "não
        # classificado" — escolher um seria inferência.
        item = input_item_de_documento(documento)
        assert item.classification.state == "ORIGEM_DESCONHECIDA"
        assert item.classification.state not in EIXO_ESTADO_P08

    def test_nenhuma_funcao_declarada_pela_ingestao(self, documento):
        # BL-014: declarar material para uma função é ato humano sob o P19; a ingestão
        # não o faz. Consequência: nenhuma função é elegível.
        item = input_item_de_documento(documento)
        assert item.classification.functions == []

    def test_content_consistency_not_applicable_sem_conteudo_duplo(self, documento):
        item = input_item_de_documento(documento)
        assert item.content_consistency.status == ConsistencyStatus.NOT_APPLICABLE

    def test_dois_documentos_iguais_geram_o_mesmo_input_item_id(self, caminho_pdf_dev):
        from escolio.ingestao.parser import parse_pdf

        doc1 = parse_pdf(caminho_pdf_dev)
        doc2 = parse_pdf(caminho_pdf_dev)
        assert input_item_de_documento(doc1).input_id == input_item_de_documento(doc2).input_id

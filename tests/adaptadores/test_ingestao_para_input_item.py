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

    def test_content_consistency_not_applicable_sem_conteudo_duplo(self, documento):
        item = input_item_de_documento(documento)
        assert item.content_consistency.status == ConsistencyStatus.NOT_APPLICABLE

    def test_dois_documentos_iguais_geram_o_mesmo_input_item_id(self, caminho_pdf_dev):
        from escolio.ingestao.parser import parse_pdf

        doc1 = parse_pdf(caminho_pdf_dev)
        doc2 = parse_pdf(caminho_pdf_dev)
        assert input_item_de_documento(doc1).input_id == input_item_de_documento(doc2).input_id

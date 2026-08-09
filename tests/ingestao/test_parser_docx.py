"""Testes estruturais do parser de .docx contra os 3 capítulos reais de
data/capitulos/. Testam estrutura (contagens, invariantes, vínculos), não
texto literal — mesma disciplina de tests/ingestao/test_parser.py (PDF).
"""

import re

from escolio.ingestao.parser_docx import parse_docx
from escolio.ingestao.vocabulario import NivelHierarquia

from .conftest import requer_capitulos_docx


@requer_capitulos_docx
class TestDeterminismoDeIdentificadores:
    def test_mesmo_documento_processado_duas_vezes_gera_os_mesmos_ids(self, caminhos_capitulos_docx):
        caminho = caminhos_capitulos_docx[0]
        doc1 = parse_docx(caminho)
        doc2 = parse_docx(caminho)
        assert [p.unit_id for p in doc1.paragrafos] == [p.unit_id for p in doc2.paragrafos]
        assert [s.unit_id for s in doc1.secoes] == [s.unit_id for s in doc2.secoes]
        assert [n.unit_id for n in doc1.notas_de_rodape] == [n.unit_id for n in doc2.notas_de_rodape]
        assert [c.unit_id for c in doc1.citacoes_recuadas] == [c.unit_id for c in doc2.citacoes_recuadas]

    def test_hash_documento_e_estavel(self, caminhos_capitulos_docx):
        caminho = caminhos_capitulos_docx[0]
        doc1 = parse_docx(caminho)
        doc2 = parse_docx(caminho)
        assert doc1.hash_documento == doc2.hash_documento

    def test_todos_os_ids_seguem_o_padrao_e_sao_unicos(self, documentos_capitulos_docx):
        padrao = re.compile(r"^UNI-[A-Z]+-[0-9a-f]{8}-\d{4}-\d{4}$")
        for documento in documentos_capitulos_docx:
            todos_ids = (
                [s.unit_id for s in documento.secoes]
                + [p.unit_id for p in documento.paragrafos]
                + [n.unit_id for n in documento.notas_de_rodape]
                + [c.unit_id for c in documento.citacoes_recuadas]
                + [c.unit_id for c in documento.citacoes_no_corpo]
            )
            assert todos_ids, f"documento {documento.caminho_original} não produziu nenhuma unidade"
            for uid in todos_ids:
                assert padrao.match(uid), f"ID fora do padrão: {uid}"
            assert len(todos_ids) == len(set(todos_ids)), "IDs duplicados entre unidades"


@requer_capitulos_docx
class TestLocalizacaoSemPagina:
    """Sem página real em .docx: localização é por parágrafo/seção/
    ordinal — testado como ausência deliberada de página, não como valor
    fabricado."""

    def test_documento_nao_tem_num_paginas(self, documentos_capitulos_docx):
        for documento in documentos_capitulos_docx:
            assert documento.num_paginas is None

    def test_paragrafos_nao_tem_pagina_mas_tem_ordinal_determinístico(self, documentos_capitulos_docx):
        for documento in documentos_capitulos_docx:
            assert documento.paragrafos
            ordinais = [p.paragrafo_ordinal for p in documento.paragrafos]
            assert all(o is not None for o in ordinais)
            assert ordinais == sorted(ordinais)
            assert len(ordinais) == len(set(ordinais))
            for p in documento.paragrafos:
                assert p.pagina_inicio is None
                assert p.pagina_fim is None

    def test_secoes_nao_tem_pagina(self, documentos_capitulos_docx):
        for documento in documentos_capitulos_docx:
            for s in documento.secoes:
                assert s.pagina is None


@requer_capitulos_docx
class TestEstruturaDeSecoes:
    """Cada capítulo real tem exatamente um título de capítulo (primeiro
    parágrafo inteiramente em negrito) seguido de seções numeradas
    'N- Texto' — verificado como estrutura, não contagem exata fixa por
    documento."""

    def test_primeira_secao_e_capitulo_e_as_demais_sao_secao_ou_indeterminadas(self, documentos_capitulos_docx):
        for documento in documentos_capitulos_docx:
            assert documento.secoes
            primeira = documento.secoes[0]
            assert primeira.nivel is NivelHierarquia.CAPITULO
            assert primeira.indeterminado is False
            for s in documento.secoes[1:]:
                assert s.nivel is NivelHierarquia.SECAO or s.indeterminado is True

    def test_nenhuma_secao_indeterminada_nos_3_documentos_reais(self, documentos_capitulos_docx):
        # Achado empírico desta calibração: os 3 capítulos reais seguem o
        # padrão 'N- Texto' sem exceção — nenhuma seção cai no ramo
        # indeterminado. Este teste falha (e deve ser revisado, não
        # contornado) se um capítulo futuro introduzir um padrão de
        # título diferente.
        for documento in documentos_capitulos_docx:
            indeterminadas = [s for s in documento.secoes if s.indeterminado]
            assert indeterminadas == []


@requer_capitulos_docx
class TestNotasDeRodape:
    def test_toda_nota_tem_texto_e_a_maioria_tem_chamador_resolvido(self, documentos_capitulos_docx):
        for documento in documentos_capitulos_docx:
            assert documento.notas_de_rodape
            for nota in documento.notas_de_rodape:
                assert nota.texto.strip()
            sem_chamador = [n for n in documento.notas_de_rodape if n.unit_id_chamador is None]
            # Achado empírico: nos 3 documentos reais, toda nota resolveu
            # chamador (ver LACUNAS.md). Falha aqui sinaliza regressão na
            # extração de footnoteReference, não um "quase certo".
            assert sem_chamador == []

    def test_unit_id_chamador_aponta_para_paragrafo_ou_citacao_existente(self, documentos_capitulos_docx):
        for documento in documentos_capitulos_docx:
            ids_conhecidos = {p.unit_id for p in documento.paragrafos} | {
                c.unit_id for c in documento.citacoes_recuadas
            }
            for nota in documento.notas_de_rodape:
                if nota.unit_id_chamador is not None:
                    assert nota.unit_id_chamador in ids_conhecidos


@requer_capitulos_docx
class TestCitacoesRecuadas:
    def test_citacoes_recuadas_tem_texto_e_secao(self, documentos_capitulos_docx):
        for documento in documentos_capitulos_docx:
            assert documento.citacoes_recuadas
            for c in documento.citacoes_recuadas:
                assert c.texto.strip()
                assert c.pagina_inicio is None
                assert c.pagina_fim is None


@requer_capitulos_docx
class TestSemReferenciasNemFiguras:
    """Achado empírico desta calibração: os 3 capítulos reais citam só
    por nota de rodapé, sem lista de referências separada, e não têm
    figura/tabela/quadro. Ver LACUNAS.md."""

    def test_referencias_e_figuras_vazias(self, documentos_capitulos_docx):
        for documento in documentos_capitulos_docx:
            assert documento.referencias == []
            assert documento.figuras == []

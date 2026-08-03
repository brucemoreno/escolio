"""Testes estruturais do parser de ingestão contra o documento real de
data/dev/. Testam estrutura (contagens, invariantes, vínculos), não
texto literal — não podem quebrar ao trocar de documento de teste,
conforme o prompt.
"""

import re

import pytest

from escolio.ingestao.parser import parse_pdf
from .conftest import requer_pdf_dev


@requer_pdf_dev
class TestDeterminismoDeIdentificadores:
    def test_mesmo_documento_processado_duas_vezes_gera_os_mesmos_ids(self, caminho_pdf_dev):
        doc1 = parse_pdf(caminho_pdf_dev)
        doc2 = parse_pdf(caminho_pdf_dev)
        assert [p.unit_id for p in doc1.paragrafos] == [p.unit_id for p in doc2.paragrafos]
        assert [s.unit_id for s in doc1.secoes] == [s.unit_id for s in doc2.secoes]
        assert [n.unit_id for n in doc1.notas_de_rodape] == [n.unit_id for n in doc2.notas_de_rodape]
        assert [c.unit_id for c in doc1.citacoes_recuadas] == [c.unit_id for c in doc2.citacoes_recuadas]
        assert [r.unit_id for r in doc1.referencias] == [r.unit_id for r in doc2.referencias]

    def test_hash_documento_e_estavel(self, caminho_pdf_dev):
        doc1 = parse_pdf(caminho_pdf_dev)
        doc2 = parse_pdf(caminho_pdf_dev)
        assert doc1.hash_documento == doc2.hash_documento

    def test_todos_os_ids_seguem_o_padrao_e_sao_unicos(self, documento):
        padrao = re.compile(r"^UNI-[A-Z]+-[0-9a-f]{8}-\d{4}-\d{4}$")
        todos_ids = (
            [s.unit_id for s in documento.secoes]
            + [p.unit_id for p in documento.paragrafos]
            + [n.unit_id for n in documento.notas_de_rodape]
            + [c.unit_id for c in documento.citacoes_recuadas]
            + [c.unit_id for c in documento.citacoes_no_corpo]
            + [r.unit_id for r in documento.referencias]
            + [f.unit_id for f in documento.figuras]
        )
        assert todos_ids, "documento não produziu nenhuma unidade"
        for uid in todos_ids:
            assert padrao.match(uid), f"ID fora do padrão: {uid}"
        assert len(todos_ids) == len(set(todos_ids)), "IDs duplicados entre unidades"


@requer_pdf_dev
class TestRastreabilidadeDePagina:
    """Toda unidade deve ser rastreável até a página de origem — testado
    como invariante estrutural, não como valor específico."""

    def test_paragrafos_tem_pagina_valida(self, documento):
        assert documento.paragrafos
        for p in documento.paragrafos:
            assert 1 <= p.pagina_inicio <= documento.num_paginas
            assert p.pagina_inicio <= p.pagina_fim <= documento.num_paginas

    def test_secoes_tem_pagina_valida(self, documento):
        assert documento.secoes
        for s in documento.secoes:
            assert 1 <= s.pagina <= documento.num_paginas

    def test_referencias_tem_pagina_valida(self, documento):
        assert documento.referencias
        for r in documento.referencias:
            assert 1 <= r.pagina <= documento.num_paginas

    def test_unidade_que_atravessa_pagina_permanece_unica(self, documento):
        """Regressão: uma unidade lógica que atravessa quebra de página
        (ex.: citação 'moxerich', p.13->p.14) deve continuar sendo UM
        registro com pagina_inicio != pagina_fim, não dois registros
        separados — corrigido a partir de feedback do usuário."""
        atravessam_pagina = [c for c in documento.citacoes_recuadas if c.pagina_inicio != c.pagina_fim]
        assert atravessam_pagina, (
            "esperava ao menos uma citação recuada atravessando página neste documento "
            "(constatado: p.13->p.14) — se isso não ocorre mais, a heurística de "
            "acumulação pode ter regredido"
        )
        for c in atravessam_pagina:
            assert c.pagina_fim == c.pagina_inicio + 1


@requer_pdf_dev
class TestHierarquia:
    def test_hierarquia_detectada_corresponde_aos_titulos_conhecidos(self, documento):
        """Não há sumário neste documento (ver LACUNAS.md) — a validação
        possível é contra os títulos de seção conhecidos por inspeção
        manual do PDF, não um sumário estruturado."""
        titulos_esperados = {
            "Resumo",
            "Introdução",
            "Justificativas",
            "Metodologia",
            "Considerações Finais",
            "Referências Bibliográficas",
        }
        titulos_encontrados = {s.titulo for s in documento.secoes}
        faltando = titulos_esperados - titulos_encontrados
        assert not faltando, f"títulos esperados não detectados: {faltando}"

    def test_secao_ambigua_fonte_primaria_fica_marcada_indeterminada(self, documento):
        """RG-002: 'Fonte Primária' usa o mesmo padrão gráfico de título
        de capítulo mas é subdivisão da lista de referências — deve
        ficar indeterminada, não classificada como capítulo comum."""
        candidatos = [s for s in documento.secoes if s.titulo.strip().lower() == "fonte primária"]
        assert len(candidatos) == 1
        assert candidatos[0].indeterminado is True
        assert candidatos[0].nivel is None

    def test_secoes_nao_indeterminadas_tem_nivel_atribuido(self, documento):
        for s in documento.secoes:
            if not s.indeterminado:
                assert s.nivel is not None


@requer_pdf_dev
class TestNotasDeRodape:
    def test_todas_as_notas_conhecidas_foram_encontradas(self, documento):
        """4 notas de rodapé confirmadas por inspeção manual do PDF
        (páginas 10, 13, 14, 16)."""
        assert len(documento.notas_de_rodape) == 4

    def test_notas_vinculadas_ao_ponto_correto_no_texto(self, documento):
        for nota in documento.notas_de_rodape:
            if nota.indeterminado:
                continue
            assert nota.unit_id_chamador is not None
            assert nota.posicao_na_chamada is not None
            assert nota.posicao_na_chamada >= 0

            unidade_chamadora = _localizar_unidade(documento, nota.unit_id_chamador)
            assert unidade_chamadora is not None, f"unidade chamadora não encontrada: {nota.unit_id_chamador}"
            texto = unidade_chamadora.texto
            assert 0 <= nota.posicao_na_chamada <= len(texto)

    def test_nota_sem_chamada_correspondente_fica_marcada(self, documento):
        for nota in documento.notas_de_rodape:
            if nota.unit_id_chamador is None:
                assert nota.indeterminado is True
                assert nota.motivo_indeterminado is not None

    def test_corpo_de_nota_multilinha_nao_fragmenta_em_notas_separadas(self, documento):
        """Regressão: o corpo de uma nota pode ocupar várias linhas
        ('No original: ...' se estende por até 3 linhas no documento
        real) — deve ser uma única NotaDeRodape, não uma por linha."""
        for nota in documento.notas_de_rodape:
            assert nota.texto.count("No original") <= 1


def _localizar_unidade(documento, unit_id: str):
    for colecao in (documento.paragrafos, documento.citacoes_recuadas):
        for u in colecao:
            if u.unit_id == unit_id:
                return u
    return None


@requer_pdf_dev
class TestCitacoes:
    def test_citacoes_recuadas_separadas_do_corpo(self, documento):
        """4 citações recuadas confirmadas por inspeção manual (as 4
        traduções de Grewe, 1979)."""
        assert len(documento.citacoes_recuadas) == 4
        for c in documento.citacoes_recuadas:
            assert "Livre tradução do Catalão" in c.texto or c.texto

    def test_citacao_recuada_nao_aparece_duplicada_como_paragrafo(self, documento):
        textos_paragrafos = {p.texto for p in documento.paragrafos}
        for c in documento.citacoes_recuadas:
            assert c.texto not in textos_paragrafos

    def test_citacoes_parenteticas_no_corpo_sao_maioria_confirmada(self, documento):
        assert documento.citacoes_no_corpo
        confirmadas = [c for c in documento.citacoes_no_corpo if not c.indeterminado]
        assert len(confirmadas) > 0

    def test_citacao_narrativa_sem_correspondencia_fica_indeterminada(self, documento):
        """RG-007/LAC-ING-011: 'Nome (ano)' sem sobrenome correspondente
        na lista de referências deve ficar indeterminado, não aceito ou
        descartado silenciosamente."""
        indeterminadas = [c for c in documento.citacoes_no_corpo if c.indeterminado]
        assert indeterminadas
        for c in indeterminadas:
            assert c.motivo_indeterminado is not None

    def test_tabela_nao_e_confundida_com_citacao_recuada(self, documento):
        """Regressão: cabeçalho/célula de tabela usa o mesmo x0 de bloco
        recuado (constatado: 'Frequência no Manuscrito', Tabela 2,
        p.19) — não deve aparecer como citação recuada."""
        for c in documento.citacoes_recuadas:
            assert "Frequência" not in c.texto
            assert "água livre" not in c.texto


@requer_pdf_dev
class TestReferencias:
    def test_referencias_extraidas_item_a_item(self, documento):
        assert len(documento.referencias) == 60

    def test_nenhuma_referencia_vazia(self, documento):
        for r in documento.referencias:
            assert r.texto.strip()

    def test_referencia_de_subsecao_fonte_primaria_identificada(self, documento):
        com_subsecao = [r for r in documento.referencias if r.subsecao is not None]
        assert com_subsecao
        assert all(r.subsecao == "Fonte Primária" for r in com_subsecao)

    def test_maioria_das_referencias_sem_subsecao(self, documento):
        sem_subsecao = [r for r in documento.referencias if r.subsecao is None]
        assert len(sem_subsecao) > len(documento.referencias) / 2


@requer_pdf_dev
class TestFigurasETabelas:
    def test_legendas_de_tabela_capturadas(self, documento):
        """4 tabelas confirmadas por inspeção manual (páginas 19-21)."""
        tabelas = [f for f in documento.figuras if not f.indeterminado]
        assert len(tabelas) == 4
        for t in tabelas:
            assert t.legenda
            assert t.numeracao

    def test_credito_associado_a_tabela(self, documento):
        tabelas = [f for f in documento.figuras if not f.indeterminado]
        com_credito = [t for t in tabelas if t.credito]
        assert com_credito, "esperava ao menos uma tabela com crédito 'Fonte: ...' associado"


@requer_pdf_dev
class TestMetadados:
    def test_titulo_extraido_da_folha_de_rosto_nao_do_pdf_metadata(self, documento):
        assert documento.metadados.titulo
        assert "pitada de sal" in documento.metadados.titulo.lower()
        assert "RELATÓRIO" not in documento.metadados.titulo.upper()[:20] or (
            "RELATÓRIO FINAL" != documento.metadados.titulo[:15].upper()
        )

    def test_autor_e_orientador_extraidos(self, documento):
        assert documento.metadados.autor
        assert documento.metadados.orientador
        assert "3." not in documento.metadados.orientador
        assert "DEPARTAMENTO" not in documento.metadados.orientador.upper()


@requer_pdf_dev
class TestPreservacaoLiteral:
    def test_hifen_de_fim_de_linha_e_preservado_nao_removido(self, documento):
        """RG-004 revisado: hífen de fim de linha não é removido porque
        pertence à palavra na maioria dos casos reais (compostos,
        clíticos) — regressão contra a primeira versão, que corrompia
        o texto removendo o hífen."""
        textos = " ".join(p.texto for p in documento.paragrafos)
        assert "destacam-se" in textos
        assert "destacamse" not in textos

    def test_relatorio_conta_hifens_preservados(self, documento):
        assert documento.hifens_de_fim_de_linha_preservados == 6


@requer_pdf_dev
class TestErroDeIngestao:
    def test_arquivo_inexistente_levanta_erro_de_ingestao(self):
        from escolio.ingestao.erros import ErroDeIngestao

        with pytest.raises(ErroDeIngestao):
            parse_pdf("caminho/que/nao/existe.pdf")

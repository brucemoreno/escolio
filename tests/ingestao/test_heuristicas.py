"""Testes unitários das heurísticas isoladas — não dependem do PDF real,
testam a lógica de cada regra contra entradas construídas."""

from escolio.ingestao.heuristicas_citacoes import (
    encontrar_citacoes_narrativas,
    encontrar_citacoes_parenteticas,
    linha_e_citacao_recuada,
)
from escolio.ingestao.heuristicas_figuras import (
    linha_e_credito_de_fonte,
    linha_e_legenda_de_figura,
    linha_e_legenda_de_tabela,
)
from escolio.ingestao.heuristicas_paragrafo import (
    concatenar_preservando_texto_literal,
    linha_inicia_paragrafo,
    texto_termina_em_hifen_de_fim_de_linha,
)
from escolio.ingestao.heuristicas_referencias import linha_inicia_novo_item
from escolio.ingestao.identificadores import gerar_id, hash_documento
from escolio.ingestao.layout import Linha


def _linha(x0=56.6, texto="texto", tamanhos=frozenset({12.0}), negrito=False):
    return Linha(
        pagina=1,
        top=100.0,
        x0=x0,
        x1=x0 + 100,
        texto=texto,
        tamanhos=tamanhos,
        totalmente_negrito=negrito,
        algum_negrito=negrito,
        chars=[],
    )


class TestParagrafo:
    def test_recuo_de_primeira_linha_detectado(self):
        assert linha_inicia_paragrafo(_linha(x0=92.1)) is True

    def test_margem_do_corpo_nao_e_primeira_linha(self):
        assert linha_inicia_paragrafo(_linha(x0=56.6)) is False

    def test_hifen_de_fim_de_linha_detectado(self):
        assert texto_termina_em_hifen_de_fim_de_linha("destacam-") is True

    def test_travessao_nao_e_hifen_de_fim_de_linha(self):
        assert texto_termina_em_hifen_de_fim_de_linha("frase—") is False

    def test_hifen_e_preservado_na_concatenacao(self):
        resultado, houve = concatenar_preservando_texto_literal("destacam-", "se como tal")
        assert resultado == "destacam-se como tal"
        assert houve is True

    def test_sem_hifen_concatena_com_espaco(self):
        resultado, houve = concatenar_preservando_texto_literal("primeira parte", "segunda parte")
        assert resultado == "primeira parte segunda parte"
        assert houve is False

    def test_texto_vazio_retorna_nova_linha(self):
        resultado, houve = concatenar_preservando_texto_literal("", "linha nova")
        assert resultado == "linha nova"
        assert houve is False


class TestCitacoes:
    def test_x0_grande_e_citacao_recuada(self):
        assert linha_e_citacao_recuada(162.9) is True

    def test_x0_de_corpo_nao_e_citacao_recuada(self):
        assert linha_e_citacao_recuada(56.6) is False
        assert linha_e_citacao_recuada(92.1) is False

    def test_citacao_parentetica_encontrada(self):
        achados = encontrar_citacoes_parenteticas("Um trecho (BRAGA, 2004) qualquer.")
        assert len(achados) == 1
        assert achados[0][0] == "BRAGA, 2004"

    def test_citacao_parentetica_com_pagina(self):
        achados = encontrar_citacoes_parenteticas("Trecho (BORGES, 2011, p. 73) aqui.")
        assert achados[0][0] == "BORGES, 2011, p. 73"

    def test_citacao_narrativa_com_sobrenome_conhecido_confirma(self):
        achados = encontrar_citacoes_narrativas("Grewe (1979, p. 13) descreve.", {"Grewe"})
        assert len(achados) == 1
        assert achados[0][2] is True

    def test_citacao_narrativa_sem_sobrenome_conhecido_nao_confirma(self):
        achados = encontrar_citacoes_narrativas("A Infanta (1987) documenta.", {"Grewe", "Braga"})
        assert len(achados) == 1
        assert achados[0][2] is False


class TestFiguras:
    def test_legenda_de_tabela_reconhecida(self):
        resultado = linha_e_legenda_de_tabela("Tabela 1: Ingredientes Fundamentais")
        assert resultado == ("1", "Ingredientes Fundamentais")

    def test_legenda_de_figura_reconhecida(self):
        resultado = linha_e_legenda_de_figura("Figura 2: Um mapa qualquer")
        assert resultado == ("2", "Um mapa qualquer")

    def test_credito_de_fonte_reconhecido(self):
        resultado = linha_e_credito_de_fonte("Fonte: Santos, 1992 - Adaptado pelo autor.")
        assert resultado == "Santos, 1992 - Adaptado pelo autor."

    def test_linha_comum_nao_e_legenda(self):
        assert linha_e_legenda_de_tabela("Um parágrafo qualquer sobre tabela.") is None
        assert linha_e_credito_de_fonte("Fontes históricas foram usadas.") is None


class TestReferencias:
    def test_gap_grande_inicia_novo_item(self):
        assert linha_inicia_novo_item(33.9, gap_tipico_intra_item=15.9) is True

    def test_gap_pequeno_e_continuacao(self):
        assert linha_inicia_novo_item(15.8, gap_tipico_intra_item=15.9) is False

    def test_gap_none_sempre_inicia_item(self):
        assert linha_inicia_novo_item(None, gap_tipico_intra_item=15.9) is True


class TestIdentificadores:
    def test_id_gerado_segue_padrao(self):
        uid = gerar_id("PAR", "abcd1234", 5, 2)
        assert uid == "UNI-PAR-abcd1234-0005-0002"

    def test_hash_documento_e_deterministico(self, tmp_path):
        arquivo = tmp_path / "teste.pdf"
        arquivo.write_bytes(b"conteudo de teste")
        h1 = hash_documento(str(arquivo))
        h2 = hash_documento(str(arquivo))
        assert h1 == h2
        assert len(h1) == 8

    def test_hash_muda_com_conteudo_diferente(self, tmp_path):
        a = tmp_path / "a.pdf"
        b = tmp_path / "b.pdf"
        a.write_bytes(b"conteudo A")
        b.write_bytes(b"conteudo B, diferente")
        assert hash_documento(str(a)) != hash_documento(str(b))

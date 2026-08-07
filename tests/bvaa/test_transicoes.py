"""Cada transição válida (T01..T18) e amostra de transições inválidas —
fonte: 04_MATRIZ_DE_LEITURA_LOCALIZACAO_VALIDACAO_E_RECOMENDACAO_P04_R01.csv.
"""

import pytest

from escolio.bvaa.erros import ErroDeTransicaoBibliografica
from escolio.bvaa.transicoes import TRANSICOES_POR_ID, aplicar_transicao, transicoes_validas_a_partir_de
from escolio.bvaa.vocabulario import EstadoBibliografico as EB


def test_dezoito_transicoes():
    assert len(TRANSICOES_POR_ID) == 18


@pytest.mark.parametrize(
    "transicao_id,origem,destino",
    [
        ("T01", EB.OBRA_NAO_IDENTIFICADA, EB.OBRA_IDENTIFICADA),
        ("T02", EB.OBRA_IDENTIFICADA, EB.EDICAO_IDENTIFICADA),
        ("T03", EB.EDICAO_IDENTIFICADA, EB.LOCALIZADA),
        ("T04", EB.LOCALIZADA, EB.ACESSIVEL),
        ("T05", EB.ACESSIVEL, EB.ACESSADA),
        ("T06", EB.ACESSADA, EB.LEITURA_NAO_REALIZADA),
        ("T07", EB.ACESSADA, EB.LEITURA_PARCIAL),
        ("T08", EB.ACESSADA, EB.LEITURA_INTEGRAL),
        ("T09", EB.LEITURA_PARCIAL, EB.PAGINA_CONFIRMADA),
        ("T10", EB.LEITURA_INTEGRAL, EB.PAGINA_CONFIRMADA),
        ("T11", EB.LEITURA_PARCIAL, EB.VALIDACAO_PENDENTE),
        ("T12", EB.PAGINA_CONFIRMADA, EB.VALIDADA),
        ("T13", EB.VALIDACAO_PENDENTE, EB.ABSTENCAO_BIBLIOGRAFICA),
        ("T14", EB.LOCALIZADA, EB.RECOMENDACAO_CONDICIONAL),
        ("T15", EB.VALIDADA, EB.RECOMENDADA),
        ("T16", EB.LEITURA_INDIRETA, EB.VALIDACAO_PENDENTE),
        ("T17", EB.PAGINA_NAO_CONFIRMADA, EB.ABSTENCAO_BIBLIOGRAFICA),
    ],
)
def test_transicao_valida(transicao_id, origem, destino):
    assert aplicar_transicao(origem, transicao_id) == destino


@pytest.mark.parametrize("origem", list(EB))
def test_t18_aceita_qualquer_estado_de_origem(origem):
    assert aplicar_transicao(origem, "T18") == EB.ABSTENCAO_BIBLIOGRAFICA


@pytest.mark.parametrize(
    "origem_errada,transicao_id",
    [
        (EB.OBRA_NAO_IDENTIFICADA, "T05"),  # T05 exige ACESSIVEL
        (EB.LOCALIZADA, "T01"),  # T01 exige OBRA_NAO_IDENTIFICADA
        (EB.ACESSADA, "T12"),  # T12 exige PAGINA_CONFIRMADA
        (EB.VALIDADA, "T02"),  # T02 exige OBRA_IDENTIFICADA
        (EB.RECOMENDADA, "T09"),  # T09 exige LEITURA_PARCIAL
    ],
)
def test_transicao_com_estado_de_origem_incompativel_rejeita(origem_errada, transicao_id):
    with pytest.raises(ErroDeTransicaoBibliografica):
        aplicar_transicao(origem_errada, transicao_id)


@pytest.mark.parametrize("transicao_id_inexistente", ["T00", "T19", "T99", ""])
def test_transicao_inexistente_rejeita(transicao_id_inexistente):
    with pytest.raises(ErroDeTransicaoBibliografica):
        aplicar_transicao(EB.OBRA_NAO_IDENTIFICADA, transicao_id_inexistente)


def test_nenhuma_transicao_por_adjacencia_semantica():
    # OBRA_IDENTIFICADA -> LOCALIZADA "parece" plausível (pula EDICAO_IDENTIFICADA)
    # mas não está na matriz — deve ser recusada, não inferida.
    with pytest.raises(ErroDeTransicaoBibliografica):
        aplicar_transicao(EB.OBRA_IDENTIFICADA, "T03")


def test_transicoes_validas_a_partir_de_nao_inclui_t18():
    validas = transicoes_validas_a_partir_de(EB.ACESSADA)
    ids = {t.transicao_id for t in validas}
    assert ids == {"T06", "T07", "T08"}
    assert "T18" not in ids


def test_transicoes_validas_a_partir_de_estado_sem_saida():
    # ABSTENCAO_BIBLIOGRAFICA é terminal: nenhuma transição parte dela
    # (reversão só por nova evidência, fora desta máquina — ver LACUNAS).
    assert transicoes_validas_a_partir_de(EB.ABSTENCAO_BIBLIOGRAFICA) == ()

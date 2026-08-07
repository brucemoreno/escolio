"""Cada gatilho de abstenção com um caso que o dispara — fonte:
02_PROTOCOLO_BVAA_UNIVERSAL_P04_R01.md §11 e
07_PROTOCOLO_DE_RECOMENDACAO_E_ABSTENCAO_BIBLIOGRAFICA_P04_R01.txt.
"""

import pytest

from escolio.bvaa.abstencao import CADEIA_DE_RECOMENDACAO, GatilhoDeAbstencao, exige_abstencao
from escolio.bvaa.erros import ErroDeSaidaDeAbstencao
from escolio.bvaa.maquina import abster
from escolio.bvaa.vocabulario import EstadoBibliografico as EB


def test_cadeia_de_recomendacao_tem_sete_etapas_na_ordem_declarada():
    assert CADEIA_DE_RECOMENDACAO == (
        "CONHECIMENTO_NOMINAL",
        "IDENTIFICACAO",
        "LOCALIZACAO",
        "ACESSO",
        "LEITURA",
        "VALIDACAO",
        "RECOMENDACAO",
    )


def test_sete_gatilhos_de_abstencao():
    assert len(GatilhoDeAbstencao) == 7


@pytest.mark.parametrize("gatilho", list(GatilhoDeAbstencao))
def test_todo_gatilho_exige_abstencao(gatilho):
    assert exige_abstencao(gatilho) is True


@pytest.mark.parametrize(
    "estado_de_partida,gatilho",
    [
        (EB.OBRA_NAO_IDENTIFICADA, GatilhoDeAbstencao.OBRA_OU_EDICAO_NAO_IDENTIFICADA),
        (EB.ACESSIVEL, GatilhoDeAbstencao.ACESSO_NAO_COMPROVADO),
        (EB.ACESSADA, GatilhoDeAbstencao.LEITURA_NAO_COMPROVADA),
        (EB.PAGINA_NAO_CONFIRMADA, GatilhoDeAbstencao.PAGINA_CITACAO_OU_METADADO_DIVERGENTE),
        (EB.LEITURA_INDIRETA, GatilhoDeAbstencao.FONTE_SECUNDARIA_COMO_PROVA_DE_LEITURA_PRIMARIA),
        (EB.VALIDACAO_PENDENTE, GatilhoDeAbstencao.EVIDENCIA_NAO_SUSTENTA_AFIRMACAO),
        (EB.RECOMENDADA, GatilhoDeAbstencao.COMANDO_EXIGE_INVENCAO),
    ],
)
def test_cada_gatilho_dispara_abstencao_a_partir_de_qualquer_estado(estado_de_partida, gatilho):
    resultado, saida = abster(
        estado_de_partida,
        gatilho,
        o_que_nao_pode_ser_comprovado="leitura da edição citada",
        evidencia_ausente="acesso material ao objeto",
        acao_documental_necessaria="fornecer arquivo ou trecho paginado",
    )
    assert resultado.estado_novo == EB.ABSTENCAO_BIBLIOGRAFICA
    assert resultado.transicao_id == "T18"
    assert saida.gatilho == gatilho


def test_abstencao_sem_o_que_nao_pode_ser_comprovado_rejeita():
    with pytest.raises(ErroDeSaidaDeAbstencao):
        abster(
            EB.ACESSADA,
            GatilhoDeAbstencao.LEITURA_NAO_COMPROVADA,
            o_que_nao_pode_ser_comprovado="",
            evidencia_ausente="acesso material",
            acao_documental_necessaria="pedir arquivo",
        )


def test_abstencao_sem_evidencia_ausente_rejeita():
    with pytest.raises(ErroDeSaidaDeAbstencao):
        abster(
            EB.ACESSADA,
            GatilhoDeAbstencao.LEITURA_NAO_COMPROVADA,
            o_que_nao_pode_ser_comprovado="leitura integral",
            evidencia_ausente="",
            acao_documental_necessaria="pedir arquivo",
        )


def test_abstencao_sem_acao_documental_necessaria_rejeita():
    with pytest.raises(ErroDeSaidaDeAbstencao):
        abster(
            EB.ACESSADA,
            GatilhoDeAbstencao.LEITURA_NAO_COMPROVADA,
            o_que_nao_pode_ser_comprovado="leitura integral",
            evidencia_ausente="acesso material",
            acao_documental_necessaria="",
        )

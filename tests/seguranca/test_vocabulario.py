from escolio.seguranca.vocabulario import (
    ORDEM_DE_PRECEDENCIA_CONFIANCA,
    AutorizacaoMinima,
    ResultadoDeCenario,
    RotuloDeConfianca,
    RotuloDeEstado,
    RotuloDeFuncao,
    RotuloDeSensibilidade,
)


def test_rotulo_de_confianca_tem_cinco_valores():
    # RD-13 [P08 §4.1].
    assert len(list(RotuloDeConfianca)) == 5


def test_rotulo_de_estado_tem_nove_valores():
    # RD-15 [P08 §4.1].
    assert len(list(RotuloDeEstado)) == 9


def test_rotulo_de_sensibilidade_tem_oito_valores():
    # RD-14 [P08 §4.1].
    assert len(list(RotuloDeSensibilidade)) == 8


def test_rotulo_de_funcao_tem_dez_valores():
    # RD-16 [P08 §4.1].
    assert len(list(RotuloDeFuncao)) == 10


def test_autorizacao_minima_tem_oito_valores():
    # RD-18 [P08 §9.1].
    assert len(list(AutorizacaoMinima)) == 8


def test_resultado_de_cenario_tem_tres_valores():
    # RD-22 [P08 §15.2].
    assert len(list(ResultadoDeCenario)) == 3


def test_ordem_de_precedencia_confianca_tem_os_cinco_rotulos_sem_repetir():
    assert set(ORDEM_DE_PRECEDENCIA_CONFIANCA) == set(RotuloDeConfianca)
    assert len(ORDEM_DE_PRECEDENCIA_CONFIANCA) == 5


def test_ordem_de_precedencia_confianca_suspeito_e_o_mais_restritivo():
    assert ORDEM_DE_PRECEDENCIA_CONFIANCA[0] == RotuloDeConfianca.SUSPEITO
    assert ORDEM_DE_PRECEDENCIA_CONFIANCA[-1] == RotuloDeConfianca.CONFIAVEL_CANONICO


def test_eixos_de_confianca_e_estado_nao_compartilham_rotulo():
    # [P08 §4]: quatro eixos independentes — mesma disciplina de
    # tests/contrato/test_entrada.py.
    confianca = {r.value for r in RotuloDeConfianca}
    estado = {r.value for r in RotuloDeEstado}
    assert confianca.isdisjoint(estado)

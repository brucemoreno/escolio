import pytest

from escolio.matriz_suficiencia_confianca import MATRIZ, consultar
from escolio.vocabulario import Confidence, Sufficiency


def test_matriz_tem_24_combinacoes():
    assert len(MATRIZ) == 24


def test_evidencia_ausente_alta_nao_permitida():
    entrada = consultar(Sufficiency.EVIDENCIA_AUSENTE, Confidence.ALTA)
    assert entrada.combinacao_permitida is False
    assert entrada.uso_maximo == "ABSTENCAO"


def test_evidencia_insuficiente_alta_nao_permitida_mas_existe_na_matriz():
    entrada = consultar(Sufficiency.EVIDENCIA_INSUFICIENTE, Confidence.ALTA)
    assert entrada.combinacao_permitida is False
    assert "USO_CONDICIONAL" in entrada.uso_maximo


def test_confianca_alta_nao_compensa_insuficiencia_mesmo_quando_combinacao_e_permitida():
    # EVIDENCIA_SUFICIENTE + ALTA é permitida, mas o uso_maximo continua
    # condicionado a "demais gates atendidos" — suficiência alta não é
    # automática a partir de confiança.
    entrada = consultar(Sufficiency.EVIDENCIA_SUFICIENTE, Confidence.ALTA)
    assert entrada.combinacao_permitida is True
    assert "quando demais gates atendidos" in entrada.uso_maximo


def test_conflitante_alta_nao_permitida():
    entrada = consultar(Sufficiency.CONFLITANTE, Confidence.ALTA)
    assert entrada.combinacao_permitida is False


@pytest.mark.parametrize("suf", list(Sufficiency))
@pytest.mark.parametrize("conf", list(Confidence))
def test_toda_combinacao_suficiencia_confianca_esta_definida(suf, conf):
    consultar(suf, conf)

import pytest

from escolio.bvaa.erros import ErroDeTransicaoBibliografica
from escolio.bvaa.maquina import avancar
from escolio.bvaa.vocabulario import EstadoBibliografico as EB


def test_avancar_aplica_transicao_valida():
    resultado = avancar(EB.OBRA_NAO_IDENTIFICADA, "T01")
    assert resultado.estado_anterior == EB.OBRA_NAO_IDENTIFICADA
    assert resultado.estado_novo == EB.OBRA_IDENTIFICADA
    assert resultado.transicao_id == "T01"


def test_avancar_rejeita_transicao_incompativel():
    with pytest.raises(ErroDeTransicaoBibliografica):
        avancar(EB.OBRA_NAO_IDENTIFICADA, "T12")


def test_cadeia_completa_ate_recomendada():
    estado = EB.OBRA_NAO_IDENTIFICADA
    for transicao_id in ("T01", "T02", "T03", "T04", "T05", "T08", "T10", "T12", "T15"):
        estado = avancar(estado, transicao_id).estado_novo
    assert estado == EB.RECOMENDADA

from dataclasses import FrozenInstanceError

import pytest

from escolio.voz.deteccao import AchadoDeFidelidade, desvios_observados
from escolio.voz.erros import ErroDePerfilDeVoz
from escolio.voz.vocabulario import Confidence, DesvioBloqueante


def test_observado_true_exige_evidencia():
    with pytest.raises(ErroDePerfilDeVoz):
        AchadoDeFidelidade(
            tipo=DesvioBloqueante.ALTERACAO_DE_SENTIDO,
            observado=True,
            evidencia="",
            confianca=Confidence.ALTA,
        )


def test_observado_false_nao_exige_evidencia():
    achado = AchadoDeFidelidade(
        tipo=DesvioBloqueante.ALTERACAO_DE_SENTIDO,
        observado=False,
        evidencia="",
        confianca=Confidence.ALTA,
    )
    assert achado.observado is False


def test_achado_e_frozen():
    achado = AchadoDeFidelidade(
        tipo=DesvioBloqueante.INVENCAO_FACTUAL,
        observado=True,
        evidencia="trecho X diverge do original",
        confianca=Confidence.MEDIA,
    )
    with pytest.raises(FrozenInstanceError):
        achado.observado = False


def test_desvios_observados_filtra_so_observado_true():
    achados = [
        AchadoDeFidelidade(
            tipo=DesvioBloqueante.INVENCAO_FACTUAL,
            observado=True,
            evidencia="x",
            confianca=Confidence.ALTA,
        ),
        AchadoDeFidelidade(
            tipo=DesvioBloqueante.COPIA_OU_IMITACAO,
            observado=False,
            evidencia="",
            confianca=Confidence.BAIXA,
        ),
    ]
    assert desvios_observados(achados) == [DesvioBloqueante.INVENCAO_FACTUAL]


def test_desvios_observados_lista_vazia_sem_achados():
    assert desvios_observados([]) == []

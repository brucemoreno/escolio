import pytest

from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.vocabulario import AuthorizationStatus
from escolio.intervencao.niveis import NivelIntervencao
from escolio.intervencao.registro import InterventionRecord
from escolio.intervencao.vocabulario import Disposition


def registro_base(**overrides):
    campos = dict(
        intervention_id="IR-0001",
        target_id="OBJ-1",
        requested_level=NivelIntervencao.EDICAO_LOCAL,
        applied_level=NivelIntervencao.EDICAO_LOCAL,
        authority_status=AuthorizationStatus.VALID,
        operation="editar trecho",
        disposition=Disposition.APPLIED,
        rationale="autorização expressa registrada",
        reversible=True,
        requires_human_decision=False,
        after_reference="REF-DEPOIS",
    )
    campos.update(overrides)
    return InterventionRecord(**campos)


def test_registro_applied_valido():
    r = registro_base()
    assert r.disposition == Disposition.APPLIED
    assert r.applied_level == NivelIntervencao.EDICAO_LOCAL


def test_applied_com_applied_level_nulo_rejeita():
    with pytest.raises(ErroDeContrato):
        registro_base(applied_level=None)


def test_applied_level_nao_nulo_com_disposition_diferente_de_applied_rejeita():
    with pytest.raises(ErroDeContrato):
        registro_base(
            disposition=Disposition.REFUSED,
            applied_level=NivelIntervencao.EDICAO_LOCAL,
            after_reference=None,
        )


@pytest.mark.parametrize("disposition", [Disposition.REFUSED, Disposition.ABSTAINED, Disposition.BLOCKED])
def test_disposition_nao_applied_exige_applied_level_nulo(disposition):
    # Caso que viola a regra: applied_level preenchido com disposition != APPLIED.
    with pytest.raises(ErroDeContrato):
        registro_base(disposition=disposition, applied_level=NivelIntervencao.OBSERVACAO, after_reference=None)


@pytest.mark.parametrize("disposition", [Disposition.REFUSED, Disposition.ABSTAINED, Disposition.BLOCKED])
def test_disposition_nao_applied_com_applied_level_nulo_aceita(disposition):
    r = registro_base(disposition=disposition, applied_level=None, after_reference=None)
    assert r.applied_level is None
    assert r.disposition == disposition


def test_applied_level_excede_requested_level_rejeita():
    with pytest.raises(ErroDeContrato):
        registro_base(
            requested_level=NivelIntervencao.DIAGNOSTICO,
            applied_level=NivelIntervencao.EDICAO_LOCAL,
        )


def test_applied_sem_autoridade_valida_rejeita():
    with pytest.raises(ErroDeContrato):
        registro_base(authority_status=AuthorizationStatus.INVALID)


@pytest.mark.parametrize("disposition", [Disposition.REFUSED, Disposition.ABSTAINED, Disposition.BLOCKED])
def test_nao_aplicada_com_after_reference_preenchido_rejeita(disposition):
    with pytest.raises(ErroDeContrato):
        registro_base(disposition=disposition, applied_level=None, after_reference="REF-INEXISTENTE")


def test_sem_intervention_id_rejeita():
    with pytest.raises(ErroDeContrato):
        registro_base(intervention_id="")


def test_sem_rationale_rejeita():
    with pytest.raises(ErroDeContrato):
        registro_base(rationale="")

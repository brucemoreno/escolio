import pytest

from escolio.contrato.afirmacao import ClaimEvidence
from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.referencia import Reference
from escolio.contrato.vocabulario import ClaimStatus, ClaimType, Confidence, ProvenanceStatus, Sufficiency


def referencia(status=ProvenanceStatus.VERIFIED):
    return Reference(reference_id="REF-1", object_id="OBJ-1", object_type="DOCUMENTO", provenance_status=status)


def claim_base(**overrides):
    campos = dict(
        claim_id="CLM-0001",
        claim_text="Texto da afirmação.",
        claim_type=ClaimType.INTERPRETATION,
        sufficiency=Sufficiency.SUFFICIENT,
        confidence=Confidence.HIGH,
        status=ClaimStatus.SUPPORTED,
        source_references=[referencia()],
    )
    campos.update(overrides)
    return ClaimEvidence(**campos)


def test_claim_valido():
    c = claim_base()
    assert c.status == ClaimStatus.SUPPORTED


def test_claim_factual_sem_evidencia_deve_ser_unsupported():
    with pytest.raises(ErroDeContrato):
        claim_base(claim_type=ClaimType.FACT, source_references=[], status=ClaimStatus.PARTIALLY_SUPPORTED)


def test_claim_factual_sem_evidencia_unsupported_aceita():
    c = claim_base(
        claim_type=ClaimType.FACT,
        source_references=[],
        status=ClaimStatus.UNSUPPORTED,
        sufficiency=Sufficiency.INSUFFICIENT,
    )
    assert c.status == ClaimStatus.UNSUPPORTED


def test_sem_evidencia_supported_rejeita():
    with pytest.raises(ErroDeContrato):
        claim_base(source_references=[], evidence_ids=[], status=ClaimStatus.SUPPORTED)


def test_supported_com_sufficiency_insuficiente_rejeita():
    with pytest.raises(ErroDeContrato):
        claim_base(sufficiency=Sufficiency.INSUFFICIENT, status=ClaimStatus.SUPPORTED)


def test_conflicted_sem_referencias_rejeita():
    with pytest.raises(ErroDeContrato):
        claim_base(status=ClaimStatus.CONFLICTED, source_references=[])


def test_conflicted_com_referencias_aceita():
    c = claim_base(status=ClaimStatus.CONFLICTED, source_references=[referencia(), referencia()])
    assert c.status == ClaimStatus.CONFLICTED

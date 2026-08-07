import pytest

from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.referencia import Reference, SemanticVersion, exige_referencia_verificada
from escolio.contrato.vocabulario import ProvenanceStatus


def referencia(status=ProvenanceStatus.VERIFIED, **overrides):
    campos = dict(
        reference_id="REF-0001",
        object_id="OBJ-0001",
        object_type="DOCUMENTO",
        provenance_status=status,
    )
    campos.update(overrides)
    return Reference(**campos)


def test_semantic_version_valida():
    v = SemanticVersion(major=1, minor=0, patch=0)
    assert v.major == 1


def test_semantic_version_negativa_invalida():
    with pytest.raises(ErroDeContrato):
        SemanticVersion(major=-1, minor=0, patch=0)


def test_reference_valida():
    r = referencia()
    assert r.verified is True


def test_reference_sem_reference_id_invalida():
    with pytest.raises(ErroDeContrato):
        referencia(reference_id="")


def test_exige_referencia_verificada_com_verified_passa():
    exige_referencia_verificada([referencia()], "TESTE", "fundamento")


def test_exige_referencia_verificada_sem_verified_rejeita():
    partial = referencia(status=ProvenanceStatus.PARTIAL)
    with pytest.raises(ErroDeContrato):
        exige_referencia_verificada([partial], "TESTE", "fundamento")


def test_exige_referencia_verificada_lista_vazia_rejeita():
    with pytest.raises(ErroDeContrato):
        exige_referencia_verificada([], "TESTE", "fundamento")

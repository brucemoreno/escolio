import pytest

from escolio.contrato.dependencia import DependencyItem, VersionRange, VersionRequirement
from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.referencia import Reference, SemanticVersion
from escolio.contrato.vocabulario import CompatibilityStatus, ProvenanceStatus, RequiredState, VersionMode


def referencia(status=ProvenanceStatus.VERIFIED):
    return Reference(reference_id="REF-1", object_id="OBJ-1", object_type="DOCUMENTO", provenance_status=status)


def test_version_requirement_exact_valido():
    vr = VersionRequirement(mode=VersionMode.EXACT, exact=SemanticVersion(1, 0, 0))
    assert vr.exact.major == 1


def test_version_requirement_exact_sem_campo_rejeita():
    with pytest.raises(ErroDeContrato):
        VersionRequirement(mode=VersionMode.EXACT)


def test_version_requirement_campo_incompativel_com_modo_rejeita():
    with pytest.raises(ErroDeContrato):
        VersionRequirement(mode=VersionMode.ANY, exact=SemanticVersion(1, 0, 0))


def test_version_requirement_range_sem_limite_rejeita():
    with pytest.raises(ErroDeContrato):
        VersionRequirement(mode=VersionMode.RANGE)


def test_version_requirement_range_minimo_maior_que_maximo_rejeita():
    with pytest.raises(ErroDeContrato):
        VersionRequirement(
            mode=VersionMode.RANGE,
            range=VersionRange(minimum=SemanticVersion(2, 0, 0), maximum=SemanticVersion(1, 0, 0)),
        )


def test_version_requirement_range_valido():
    vr = VersionRequirement(
        mode=VersionMode.RANGE,
        range=VersionRange(minimum=SemanticVersion(1, 0, 0), maximum=SemanticVersion(2, 0, 0)),
    )
    assert vr.range.minimum.major == 1


def test_version_requirement_any_valido():
    vr = VersionRequirement(mode=VersionMode.ANY)
    assert vr.mode == VersionMode.ANY


def dependencia_base(**overrides):
    campos = dict(
        dependency_id="DEP-0001",
        required_version=VersionRequirement(mode=VersionMode.ANY),
        required_state=RequiredState.HOMOLOGATED,
        observed_state="HOMOLOGATED",
        compatibility_status=CompatibilityStatus.NOT_APPLICABLE,
    )
    campos.update(overrides)
    return DependencyItem(**campos)


def test_dependencia_valida_minima():
    d = dependencia_base()
    assert d.dependency_id == "DEP-0001"


def test_dependencia_compatible_sem_observed_version_rejeita():
    with pytest.raises(ErroDeContrato):
        dependencia_base(
            required_version=VersionRequirement(mode=VersionMode.MINIMUM, minimum=SemanticVersion(1, 0, 0)),
            compatibility_status=CompatibilityStatus.COMPATIBLE,
            evidence=[referencia()],
        )


def test_dependencia_compatible_com_observed_version_e_evidencia_aceita():
    d = dependencia_base(
        required_version=VersionRequirement(mode=VersionMode.MINIMUM, minimum=SemanticVersion(1, 0, 0)),
        compatibility_status=CompatibilityStatus.COMPATIBLE,
        observed_version=SemanticVersion(1, 2, 0),
        evidence=[referencia()],
    )
    assert d.observed_version.minor == 2


def test_dependencia_compatible_sem_evidencia_verificada_rejeita():
    with pytest.raises(ErroDeContrato):
        dependencia_base(
            compatibility_status=CompatibilityStatus.COMPATIBLE,
            observed_version=SemanticVersion(1, 0, 0),
            evidence=[referencia(ProvenanceStatus.UNKNOWN)],
        )


def test_dependencia_not_applicable_com_versao_exigida_rejeita():
    with pytest.raises(ErroDeContrato):
        dependencia_base(
            required_version=VersionRequirement(mode=VersionMode.MINIMUM, minimum=SemanticVersion(1, 0, 0)),
            compatibility_status=CompatibilityStatus.NOT_APPLICABLE,
        )

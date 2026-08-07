import pytest

from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.payloads import (
    AbstentionPayload,
    BlockPayload,
    ErrorPayload,
    Limitation,
    SensitivityLabel,
    Warning,
)
from escolio.contrato.referencia import Reference
from escolio.contrato.vocabulario import (
    AbstentionCategory,
    BlockCategory,
    ErrorCategory,
    ErrorSeverity,
    LimitationType,
    Materiality,
    ProvenanceStatus,
    SensitivityCategory,
    WarningCategory,
)


def referencia(status=ProvenanceStatus.VERIFIED):
    return Reference(reference_id="REF-1", object_id="OBJ-1", object_type="DOCUMENTO", provenance_status=status)


def erro_base(**overrides):
    campos = dict(
        error_id="ERR-0001",
        request_id="REQ-0001",
        category=ErrorCategory.VALIDATION,
        code="CAMPO_AUSENTE",
        severity=ErrorSeverity.MAJOR,
        message="campo obrigatório ausente",
    )
    campos.update(overrides)
    return ErrorPayload(**campos)


def test_error_payload_valido():
    e = erro_base()
    assert e.code == "CAMPO_AUSENTE"


def test_error_sem_code_rejeita():
    with pytest.raises(ErroDeContrato):
        erro_base(code="")


def test_error_retry_allowed_sem_condicoes_rejeita():
    with pytest.raises(ErroDeContrato):
        erro_base(retry_allowed=True, retry_conditions=[])


def test_error_retry_allowed_com_condicoes_aceita():
    e = erro_base(retry_allowed=True, retry_conditions=["reenviar após corrigir campo"])
    assert e.retry_allowed is True


def test_error_retry_nao_permitido_com_condicoes_rejeita():
    with pytest.raises(ErroDeContrato):
        erro_base(retry_allowed=False, retry_conditions=["algo"])


def abstencao_base(**overrides):
    campos = dict(
        abstention_id="ABS-0001",
        request_id="REQ-0001",
        category=AbstentionCategory.INSUFFICIENT_AUTHORITY,
        reason="autoridade insuficiente para homologar",
    )
    campos.update(overrides)
    return AbstentionPayload(**campos)


def test_abstention_valida_irreversivel():
    a = abstencao_base(reversible=False)
    assert a.reversible is False


def test_abstention_reversivel_sem_resume_conditions_rejeita():
    with pytest.raises(ErroDeContrato):
        abstencao_base(reversible=True, resume_conditions=[])


def test_abstention_reversivel_com_resume_conditions_aceita():
    a = abstencao_base(reversible=True, resume_conditions=["nova autorização do USUARIO_PROPONENTE"])
    assert a.reversible is True


def bloqueio_base(**overrides):
    campos = dict(
        block_id="BLK-0001",
        request_id="REQ-0001",
        category=BlockCategory.MISSING_DEPENDENCY,
        description="dependência não homologada",
        material_evidence=[referencia()],
        removable=False,
        total_block_justification="nenhum trabalho seguro independente do escopo bloqueado",
    )
    campos.update(overrides)
    return BlockPayload(**campos)


def test_block_total_valido():
    b = bloqueio_base()
    assert b.total_block_justification is not None


def test_block_sem_evidencia_verificada_rejeita():
    with pytest.raises(ErroDeContrato):
        bloqueio_base(material_evidence=[referencia(ProvenanceStatus.UNKNOWN)])


def test_block_removivel_sem_removal_action_rejeita():
    with pytest.raises(ErroDeContrato):
        bloqueio_base(removable=True, removal_action=None)


def test_block_removivel_com_removal_action_aceita():
    b = bloqueio_base(removable=True, removal_action="homologar a dependência pendente")
    assert b.removal_action is not None


def test_block_total_com_safe_work_remaining_rejeita():
    with pytest.raises(ErroDeContrato):
        bloqueio_base(safe_work_remaining=["algo"])


def test_block_parcial_sem_safe_work_remaining_rejeita():
    with pytest.raises(ErroDeContrato):
        bloqueio_base(total_block_justification=None, safe_work_remaining=[])


def test_block_parcial_com_safe_work_remaining_aceita():
    b = bloqueio_base(total_block_justification=None, safe_work_remaining=["seção não afetada"])
    assert b.safe_work_remaining


def test_limitation_valida():
    lim = Limitation(
        limitation_id="LIM-0001",
        type=LimitationType.SCOPE,
        description="escopo parcialmente coberto",
        effect_on_result="resultado cobre apenas a seção 1",
        materiality=Materiality.MEDIUM,
    )
    assert lim.impede_sucesso_integral is False


def test_limitation_alta_materialidade_impede_sucesso():
    lim = Limitation(
        limitation_id="LIM-0002",
        type=LimitationType.AUTHORITY,
        description="autoridade insuficiente para o núcleo do escopo",
        effect_on_result="resultado não pode ser considerado completo",
        materiality=Materiality.HIGH,
    )
    assert lim.impede_sucesso_integral is True


def test_sensitivity_label_other_controlled_sem_justification_rejeita():
    with pytest.raises(ErroDeContrato):
        SensitivityLabel(category=SensitivityCategory.OTHER_CONTROLLED, source_policy="P08")


def test_sensitivity_label_other_controlled_com_justification_aceita():
    label = SensitivityLabel(
        category=SensitivityCategory.OTHER_CONTROLLED, source_policy="P08", justification="dado institucional restrito"
    )
    assert label.justification is not None


def test_warning_valido():
    w = Warning(warning_id="WRN-0001", category=WarningCategory.UNCERTAINTY, message="fonte não verificada")
    assert w.category == WarningCategory.UNCERTAINTY

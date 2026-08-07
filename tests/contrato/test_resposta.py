import pytest

from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.payloads import AbstentionPayload, BlockPayload, ErrorPayload, Limitation
from escolio.contrato.referencia import Reference, SemanticVersion
from escolio.contrato.resposta import (
    Completion,
    Response,
    SafeResult,
    exige_correspondencia_request_response,
)
from escolio.contrato.requisicao import Authorization, ExpectedOutput, Request, Requester, Scope
from escolio.contrato.vocabulario import (
    AbstentionCategory,
    AuthorizationStatus,
    BlockCategory,
    ErrorCategory,
    ErrorSeverity,
    LimitationType,
    Materiality,
    ProvenanceStatus,
    ResponseStatus,
)


def referencia(status=ProvenanceStatus.VERIFIED):
    return Reference(reference_id="REF-1", object_id="OBJ-1", object_type="DOCUMENTO", provenance_status=status)


def resposta_base(**overrides):
    campos = dict(
        schema_version=SemanticVersion(1, 0, 0),
        response_id="RES-0001",
        request_id="REQ-0001",
        project_id="PRJ-0001",
        component_id="P12",
        function_id="P12",
        status=ResponseStatus.SUCCESS,
    )
    campos.update(overrides)
    return Response(**campos)


def erro_payload(**overrides):
    campos = dict(
        error_id="ERR-1",
        request_id="REQ-0001",
        category=ErrorCategory.VALIDATION,
        code="X",
        severity=ErrorSeverity.MAJOR,
        message="falha",
    )
    campos.update(overrides)
    return ErrorPayload(**campos)


def abstencao_payload(**overrides):
    campos = dict(
        abstention_id="ABS-1",
        request_id="REQ-0001",
        category=AbstentionCategory.INSUFFICIENT_AUTHORITY,
        reason="autoridade insuficiente",
    )
    campos.update(overrides)
    return AbstentionPayload(**campos)


def bloqueio_payload(**overrides):
    campos = dict(
        block_id="BLK-1",
        request_id="REQ-0001",
        category=BlockCategory.MISSING_DEPENDENCY,
        description="dependência ausente",
        material_evidence=[referencia()],
        removable=False,
        total_block_justification="sem trabalho seguro restante",
    )
    campos.update(overrides)
    return BlockPayload(**campos)


# --- SUCCESS ---

def test_success_valido():
    r = resposta_base()
    assert r.status == ResponseStatus.SUCCESS


def test_success_com_error_preenchido_rejeita():
    with pytest.raises(ErroDeContrato):
        resposta_base(error=erro_payload())


def test_success_com_scope_not_completed_rejeita():
    with pytest.raises(ErroDeContrato):
        resposta_base(completion=Completion(scope_not_completed=["parte X"]))


def test_success_com_limitacao_alta_materialidade_rejeita():
    lim = Limitation(
        limitation_id="LIM-1",
        type=LimitationType.SCOPE,
        description="d",
        effect_on_result="e",
        materiality=Materiality.HIGH,
    )
    with pytest.raises(ErroDeContrato):
        resposta_base(limitations=[lim])


# --- PARTIAL_SUCCESS ---

def test_partial_success_valido():
    r = resposta_base(
        status=ResponseStatus.PARTIAL_SUCCESS,
        completion=Completion(scope_completed=["A"], scope_not_completed=["B"], partiality_cause="B depende de fonte não localizada"),
    )
    assert r.status == ResponseStatus.PARTIAL_SUCCESS


def test_partial_success_sem_partiality_cause_rejeita():
    with pytest.raises(ErroDeContrato):
        resposta_base(
            status=ResponseStatus.PARTIAL_SUCCESS,
            completion=Completion(scope_completed=["A"], scope_not_completed=["B"]),
        )


def test_partial_success_sem_scope_completed_rejeita():
    with pytest.raises(ErroDeContrato):
        resposta_base(
            status=ResponseStatus.PARTIAL_SUCCESS,
            completion=Completion(scope_not_completed=["B"], partiality_cause="causa"),
        )


# --- ERROR ---

def test_error_valido():
    r = resposta_base(status=ResponseStatus.ERROR, error=erro_payload())
    assert r.error is not None


def test_error_sem_payload_rejeita():
    with pytest.raises(ErroDeContrato):
        resposta_base(status=ResponseStatus.ERROR)


def test_error_com_safe_result_valido():
    r = resposta_base(
        status=ResponseStatus.ERROR,
        error=erro_payload(),
        safe_result=SafeResult(available=True, content="parte segura", scope=["secao 1"]),
    )
    assert r.safe_result.available is True


# --- ABSTAINED ---

def test_abstained_valido():
    r = resposta_base(status=ResponseStatus.ABSTAINED, abstention=abstencao_payload())
    assert r.abstention is not None


def test_abstained_sem_payload_rejeita():
    with pytest.raises(ErroDeContrato):
        resposta_base(status=ResponseStatus.ABSTAINED)


def test_abstained_com_safe_result_disponivel_rejeita():
    with pytest.raises(ErroDeContrato):
        resposta_base(
            status=ResponseStatus.ABSTAINED,
            abstention=abstencao_payload(),
            safe_result=SafeResult(available=True, content="x", scope=["s"]),
        )


# --- BLOCKED ---

def test_blocked_valido():
    r = resposta_base(status=ResponseStatus.BLOCKED, block=bloqueio_payload())
    assert r.block is not None


def test_blocked_sem_payload_rejeita():
    with pytest.raises(ErroDeContrato):
        resposta_base(status=ResponseStatus.BLOCKED)


# --- exclusividade mútua (§21.34) ---

def test_error_e_abstention_simultaneos_rejeita():
    with pytest.raises(ErroDeContrato):
        resposta_base(status=ResponseStatus.ERROR, error=erro_payload(), abstention=abstencao_payload())


# --- safe_result (§9) ---

def test_safe_result_disponivel_sem_conteudo_nem_referencia_rejeita():
    with pytest.raises(ErroDeContrato):
        SafeResult(available=True, scope=["s"])


def test_safe_result_disponivel_com_referencia_nao_verificada_rejeita():
    with pytest.raises(ErroDeContrato):
        SafeResult(available=True, reference=referencia(ProvenanceStatus.PARTIAL), scope=["s"])


def test_safe_result_indisponivel_com_conteudo_rejeita():
    with pytest.raises(ErroDeContrato):
        SafeResult(available=False, content="algo")


def test_safe_result_indisponivel_valido():
    sr = SafeResult(available=False)
    assert sr.content is None


# --- correspondência request/response (§8.1, §21.1-3) ---

def requisicao_base(**overrides):
    campos = dict(
        schema_version=SemanticVersion(1, 0, 0),
        request_id="REQ-0001",
        project_id="PRJ-0001",
        component_id="P12",
        function_id="P12",
        operation="REVISAR_IC",
        requester=Requester(role="ENGENHEIRO_LLM"),
        scope=Scope(),
        authorization=Authorization(status=AuthorizationStatus.UNVERIFIED),
        expected_output=ExpectedOutput(type="RELATORIO"),
    )
    campos.update(overrides)
    return Request(**campos)


def test_correspondencia_valida():
    req = requisicao_base()
    resp = resposta_base()
    exige_correspondencia_request_response(req, resp)


def test_correspondencia_request_id_divergente_rejeita():
    req = requisicao_base()
    resp = resposta_base(request_id="REQ-OUTRO")
    with pytest.raises(ErroDeContrato):
        exige_correspondencia_request_response(req, resp)


def test_correspondencia_project_id_divergente_rejeita():
    req = requisicao_base()
    resp = resposta_base(project_id="PRJ-OUTRO")
    with pytest.raises(ErroDeContrato):
        exige_correspondencia_request_response(req, resp)


def test_correspondencia_component_id_divergente_rejeita():
    req = requisicao_base()
    resp = resposta_base(component_id="P11")
    with pytest.raises(ErroDeContrato):
        exige_correspondencia_request_response(req, resp)

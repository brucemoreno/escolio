import pytest

from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.referencia import Reference, SemanticVersion
from escolio.contrato.requisicao import Authorization, ExpectedOutput, Request, Requester, Scope
from escolio.contrato.vocabulario import AuthorizationStatus, ProvenanceStatus


def referencia(status=ProvenanceStatus.VERIFIED):
    return Reference(reference_id="REF-1", object_id="OBJ-1", object_type="DOCUMENTO", provenance_status=status)


def requisicao_base(**overrides):
    campos = dict(
        schema_version=SemanticVersion(1, 0, 0),
        request_id="REQ-0001",
        project_id="PRJ-0001",
        component_id="P12",
        function_id="P12",
        operation="REVISAR_IC",
        requester=Requester(role="ENGENHEIRO_LLM", authority_basis="R03 §4.5"),
        scope=Scope(allowed_operations=["REVISAR_IC"], prohibited_operations=["HOMOLOGAR"]),
        authorization=Authorization(status=AuthorizationStatus.UNVERIFIED),
        expected_output=ExpectedOutput(type="RELATORIO_DIAGNOSTICO"),
    )
    campos.update(overrides)
    return Request(**campos)


def test_requisicao_valida_minima():
    r = requisicao_base()
    assert r.request_id == "REQ-0001"


def test_request_id_ausente_rejeita():
    with pytest.raises(ErroDeContrato):
        requisicao_base(request_id="")


def test_operacao_em_allowed_e_prohibited_simultaneamente_rejeita():
    with pytest.raises(ErroDeContrato):
        requisicao_base(
            scope=Scope(allowed_operations=["REVISAR_IC"], prohibited_operations=["REVISAR_IC"])
        )


def test_operacao_proibida_prevalece_sobre_autorizacao_rejeita():
    with pytest.raises(ErroDeContrato):
        requisicao_base(
            operation="HOMOLOGAR",
            scope=Scope(allowed_operations=["HOMOLOGAR"], prohibited_operations=["HOMOLOGAR"]),
        )


def test_operacao_fora_de_allowed_operations_rejeita():
    with pytest.raises(ErroDeContrato):
        requisicao_base(operation="OUTRA_OPERACAO", scope=Scope(allowed_operations=["REVISAR_IC"]))


def test_autorizacao_valid_sem_referencia_verificada_rejeita():
    with pytest.raises(ErroDeContrato):
        requisicao_base(
            authorization=Authorization(status=AuthorizationStatus.VALID, evidence=[referencia(ProvenanceStatus.PARTIAL)])
        )


def test_autorizacao_valid_com_referencia_verificada_aceita():
    r = requisicao_base(
        authorization=Authorization(status=AuthorizationStatus.VALID, evidence=[referencia()])
    )
    assert r.authorization.status == AuthorizationStatus.VALID

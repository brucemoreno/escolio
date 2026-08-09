"""Sessão 8 do plano P13 — extensão do envelope P09
(`P13RequestExtension`, `P13ResultExtension`, builders de payload
ABSTAINED/BLOCKED/ERROR de §31.6, exemplo canônico de §29).
"""

import pytest

from escolio.comentarios.aplicacao_p06_p07 import P13_CAUSE_VOICE_PROFILE_INSUFFICIENT
from escolio.comentarios.aplicacao_p09 import (
    P13RequestExtension,
    P13ResultExtension,
    constroi_abstencao_perfil_de_voz_insuficiente,
    resposta_p13_abstained,
    resposta_p13_blocked,
    resposta_p13_error,
)
from escolio.comentarios.erros import ErroDeComentario
from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.payloads import AbstentionPayload, BlockPayload, ErrorPayload
from escolio.contrato.referencia import Reference, SemanticVersion
from escolio.contrato.resposta import Result, SafeResult
from escolio.contrato.vocabulario import (
    AbstentionCategory,
    BlockCategory,
    ErrorCategory,
    ErrorSeverity,
    ProvenanceStatus,
    ResponseStatus,
)
from tests.comentarios.fixtures import comentario_base


def _referencia(status=ProvenanceStatus.VERIFIED):
    return Reference(reference_id="REF-1", object_id="OBJ-1", object_type="DOCUMENTO", provenance_status=status)


def _request_extension_base(**overrides):
    campos = dict(
        document_id="DOC-0001",
        document_version="1.0.0",
        document_type="dissertacao",
        requested_operation="CARTOGRAFIA_GLOBAL",
        comment_purpose="Revisão seletiva de comentários Word.",
        authorized_intervention_level="PROPOSTA",
        formative_level="POS_GRADUACAO",
        privacy_classification="PUBLIC",
    )
    campos.update(overrides)
    return P13RequestExtension(**campos)


class TestP13RequestExtension:
    """§31.3 — extensão de entrada."""

    def test_construcao_minima_valida(self):
        extensao = _request_extension_base()
        assert extensao.global_document_reference is None
        assert extensao.voice_profile_reference is None
        assert extensao.authorized_units == []
        assert extensao.source_references == []
        assert extensao.prior_diagnostic_references == []
        assert extensao.excluded_units == []

    @pytest.mark.parametrize(
        "campo",
        [
            "document_id",
            "document_version",
            "document_type",
            "requested_operation",
            "comment_purpose",
            "authorized_intervention_level",
            "formative_level",
            "privacy_classification",
        ],
    )
    def test_campo_obrigatorio_vazio_rejeita(self, campo):
        with pytest.raises(ErroDeComentario):
            _request_extension_base(**{campo: ""})

    def test_referencias_nulaveis_aceitam_reference(self):
        ref = _referencia()
        extensao = _request_extension_base(global_document_reference=ref, voice_profile_reference=ref)
        assert extensao.global_document_reference is ref
        assert extensao.voice_profile_reference is ref

    def test_listas_de_referencia_aceitam_conteudo(self):
        ref = _referencia()
        extensao = _request_extension_base(
            authorized_units=[ref], source_references=[ref], prior_diagnostic_references=[ref], excluded_units=[ref]
        )
        assert extensao.authorized_units == [ref]
        assert extensao.excluded_units == [ref]


class TestP13ResultExtension:
    """§31.4 — extensão de resultado."""

    def test_construcao_minima_valida(self):
        extensao = P13ResultExtension(current_p13_state="DIAGNOSTICO_EM_CURSO")
        assert extensao.comments == []
        assert extensao.matrix_comments == []
        assert extensao.matrix_referrals == []
        assert extensao.units_without_comment == []
        assert extensao.global_cartography is None
        assert extensao.criticality_matrix is None
        assert extensao.selectivity_matrix is None
        assert extensao.density_justification is None
        assert extensao.privacy_warnings == []

    def test_current_p13_state_vazio_rejeita(self):
        with pytest.raises(ErroDeComentario):
            P13ResultExtension(current_p13_state="")

    def test_comments_reusa_p13comment_sem_duplicar_schema(self):
        comentario = comentario_base()
        extensao = P13ResultExtension(current_p13_state="EM_CONSOLIDACAO", comments=[comentario])
        assert extensao.comments[0] is comentario

    def test_campos_abertos_aceitam_objeto_arbitrario(self):
        extensao = P13ResultExtension(
            current_p13_state="EM_CONSOLIDACAO",
            matrix_referrals=[{"unit_id": "UNIT-01"}],
            units_without_comment=[{"unit_id": "UNIT-02", "motivo": "sem problema material"}],
            global_cartography={"secoes": 14},
        )
        assert extensao.matrix_referrals == [{"unit_id": "UNIT-01"}]
        assert extensao.global_cartography == {"secoes": 14}


class TestConstroiAbstencaoPerfilDeVozInsuficiente:
    """§29 — exemplo canônico: ABSTAINED / AMBIGUITY /
    cause_code=P13_CAUSE_VOICE_PROFILE_INSUFFICIENT."""

    def test_categoria_e_ambiguity(self):
        payload = constroi_abstencao_perfil_de_voz_insuficiente(
            abstention_id="ABST-0001", request_id="REQ-0001"
        )
        assert payload.category == AbstentionCategory.AMBIGUITY

    def test_cause_code_registrado_em_reason(self):
        payload = constroi_abstencao_perfil_de_voz_insuficiente(
            abstention_id="ABST-0001", request_id="REQ-0001"
        )
        assert P13_CAUSE_VOICE_PROFILE_INSUFFICIENT in payload.reason

    def test_reason_customizado_e_preservado(self):
        payload = constroi_abstencao_perfil_de_voz_insuficiente(
            abstention_id="ABST-0001", request_id="REQ-0001", reason="motivo específico do caso"
        )
        assert payload.reason == "motivo específico do caso"


def _abstencao_base(**overrides):
    campos = dict(
        abstention_id="ABST-0001",
        request_id="REQ-0001",
        category=AbstentionCategory.AMBIGUITY,
        reason="perfil de voz insuficiente",
    )
    campos.update(overrides)
    return AbstentionPayload(**campos)


def _block_base(**overrides):
    campos = dict(
        block_id="BLK-0001",
        request_id="REQ-0001",
        category=BlockCategory.CANONICAL_SOURCE_ABSENT,
        description="fonte canônica ausente",
        material_evidence=[_referencia()],
        removable=False,
        safe_work_remaining=["cartografia global concluída"],
    )
    campos.update(overrides)
    return BlockPayload(**campos)


def _error_base(**overrides):
    campos = dict(
        error_id="ERR-0001",
        request_id="REQ-0001",
        category=ErrorCategory.PROCESSING,
        code="FALHA_DE_PROCESSAMENTO",
        severity=ErrorSeverity.MAJOR,
        message="falha ao processar unidade",
    )
    campos.update(overrides)
    return ErrorPayload(**campos)


def _envelope_ids(**overrides):
    campos = dict(
        schema_version=SemanticVersion(1, 0, 0),
        response_id="RESP-0001",
        request_id="REQ-0001",
        project_id="PROJ-0001",
        component_id="P13",
    )
    campos.update(overrides)
    return campos


class TestRespostaP13Abstained:
    """§31.6 ABSTAINED — reusa Response/SafeResult (peça 1) sem duplicar validação."""

    def test_forma_valida(self):
        resposta = resposta_p13_abstained(**_envelope_ids(), abstention=_abstencao_base())
        assert resposta.status == ResponseStatus.ABSTAINED
        assert resposta.function_id == "P13"
        assert resposta.safe_result.available is False
        assert resposta.error is None
        assert resposta.block is None

    def test_safe_result_disponivel_e_rejeitado_pela_forma_generica(self):
        # O builder fixa safe_result.available=False; construir a forma
        # inválida (TA13-19: "ABSTAINED com safe_result.available=true")
        # exige contornar o builder e ir direto a Response — que a rejeita.
        from escolio.contrato.resposta import Response

        with pytest.raises(ErroDeContrato):
            Response(
                **_envelope_ids(),
                function_id="P13",
                status=ResponseStatus.ABSTAINED,
                abstention=_abstencao_base(),
                safe_result=SafeResult(available=True, content="x", scope=["escopo"]),
            )


class TestRespostaP13Blocked:
    """§31.6 BLOCKED."""

    def test_forma_valida(self):
        resposta = resposta_p13_blocked(**_envelope_ids(), block=_block_base())
        assert resposta.status == ResponseStatus.BLOCKED
        assert resposta.function_id == "P13"
        assert resposta.safe_result.available is False
        assert resposta.error is None
        assert resposta.abstention is None


class TestRespostaP13Error:
    """§31.6 ERROR — único status que pode usar safe_result como resultado
    seguro preservado."""

    def test_forma_valida_sem_safe_result(self):
        resposta = resposta_p13_error(**_envelope_ids(), error=_error_base())
        assert resposta.status == ResponseStatus.ERROR
        assert resposta.safe_result.available is False

    def test_error_pode_preservar_safe_result(self):
        preservado = SafeResult(
            available=True,
            content="cartografia global já concluída antes da falha",
            scope=["cartografia_global"],
        )
        resposta = resposta_p13_error(**_envelope_ids(), error=_error_base(), safe_result=preservado)
        assert resposta.safe_result.available is True
        assert resposta.safe_result.content == "cartografia global já concluída antes da falha"

    def test_result_com_p13_result_extension(self):
        extensao = P13ResultExtension(current_p13_state="INTERROMPIDO_POR_ERRO")
        resposta = resposta_p13_error(
            **_envelope_ids(), error=_error_base(), result=Result(type="P13ResultExtension", content=extensao)
        )
        assert resposta.result.content is extensao

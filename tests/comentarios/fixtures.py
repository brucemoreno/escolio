from escolio.comentarios.comentario import P13Comment
from escolio.comentarios.criticidade import ClasseCriticidade, EixoCriticidade, MatrizCriticidade
from escolio.comentarios.seletividade import MatrizSeletividade, SelectionDecision
from escolio.comentarios.vocabulario import P13CommentStatus


def comentario_base(**overrides):
    campos = dict(
        comment_id="CMT-0001",
        document_id="DOC-0001",
        document_version="1.0.0",
        module_id="MOD-01",
        unit_id="UNIT-01",
        anchor_start="120",
        anchor_end="180",
        anchor_text_hash="sha256:abc123",
        comment_type="OBSERVACAO_ESTRUTURAL",
        priority="PRIORIDADE_MEDIA",
        severity="MODERADA",
        problem="Descrição do problema identificado.",
        evidence="Trecho que evidencia o problema.",
        impact="Impacto descrito.",
        recommended_action="Ação recomendada descrita.",
        intervention_level="INT-04",
        authority_required="USUARIO_PROPONENTE",
        gate="GATE_DE_VALIDACAO_FINAL",
        source_status="VERIFICADA",
        voice_impact="NENHUM",
        privacy_classification="PUBLIC",
        reversible=True,
        status=P13CommentStatus.DRAFT,
    )
    campos.update(overrides)
    return P13Comment(**campos)


def avaliacao_todos_eixos(**overrides):
    avaliacao = {eixo: f"avaliação do eixo {eixo.value}" for eixo in EixoCriticidade}
    avaliacao.update(overrides)
    return avaliacao


def matriz_criticidade_base(**overrides):
    campos = dict(
        problem_id="PROB-0001",
        unit_id="UNIT-01",
        avaliacao_por_eixo=avaliacao_todos_eixos(),
        classe=ClasseCriticidade.CRITICIDADE_MEDIA,
        justificativa_classe="Justificativa narrativa da classe atribuída.",
    )
    campos.update(overrides)
    return MatrizCriticidade(**campos)


def matriz_seletividade_base(**overrides):
    campos = dict(
        selection_id="SEL-0001",
        unit_id="UNIT-01",
        candidate_problem_id="PROB-0001",
        criticality=ClasseCriticidade.CRITICIDADE_MEDIA,
        material_impact="Impacto material descrito.",
        novelty="Não repete achado anterior.",
        recurrence="Ocorrência única.",
        matrix_comment_coverage="Não coberto por comentário-matriz.",
        actionability="Ação possível e proporcional.",
        evidence_sufficiency="Evidência suficiente.",
        human_decision_required="Não.",
        privacy_risk="Nenhum.",
        selection_decision=SelectionDecision.COMENTAR,
        selection_rationale="Ganho de orientação supera custo de poluição documental.",
    )
    campos.update(overrides)
    return MatrizSeletividade(**campos)

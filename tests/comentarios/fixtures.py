from escolio.comentarios.comentario import P13Comment
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

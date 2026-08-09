"""Enums próprios de `P13Comment` — fonte: P13 §31.5.1 e §31.5.2.

`P13CommentStatus` e `P13CommentResolution` são vocabulário interno do
comentário. Nenhum dos dois é alias de `ResponseStatus` (P09 §8.2) nem de
`Disposition` (P09 §13, escolio.intervencao.vocabulario) — a fonte é
explícita: "P13Comment.status não é status P09" e "não é
InterventionRecord.disposition" [§31.5.1, regras 1-2].
"""

from enum import Enum

ARQUIVO_FONTE = "P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md"


class P13CommentStatus(str, Enum):
    """Ciclo operacional interno do comentário [§31.5.1]."""

    DRAFT = "DRAFT"
    READY_FOR_REVIEW = "READY_FOR_REVIEW"
    PENDING_HUMAN_DECISION = "PENDING_HUMAN_DECISION"
    APPROVED_FOR_INSERTION = "APPROVED_FOR_INSERTION"
    REJECTED_FOR_INSERTION = "REJECTED_FOR_INSERTION"
    INSERTED = "INSERTED"
    RESOLVED = "RESOLVED"
    SUPERSEDED = "SUPERSEDED"
    WITHDRAWN = "WITHDRAWN"


class P13CommentResolution(str, Enum):
    """Resultado humano ou documental da análise do comentário [§31.5.2, §42]."""

    ABERTO = "ABERTO"
    ACEITO = "ACEITO"
    PARCIALMENTE_ACEITO = "PARCIALMENTE_ACEITO"
    RECUSADO = "RECUSADO"
    RESOLVIDO = "RESOLVIDO"
    INAPLICAVEL = "INAPLICAVEL"
    SUPERADO_POR_VERSAO = "SUPERADO_POR_VERSAO"
    PENDENTE_DE_DECISAO = "PENDENTE_DE_DECISAO"


# §31.5.2 / §42 — resolution é obrigatório quando status atinge um destes.
STATUS_QUE_EXIGEM_RESOLUTION = frozenset(
    {
        P13CommentStatus.RESOLVED,
        P13CommentStatus.SUPERSEDED,
        P13CommentStatus.WITHDRAWN,
    }
)

# §31.5.4 — literais de comment_type referenciados pelas regras de
# matrix_comment_id. O catálogo completo dos 15 tipos é a sessão 3
# (`escolio/comentarios/LACUNAS.md`); estes dois valores são citados aqui,
# não inferidos, porque §31.5.4 os nomeia por extenso ao definir a
# obrigatoriedade e a integridade referencial de matrix_comment_id.
COMMENT_TYPE_REMISSAO_A_COMENTARIO_MATRIZ = "REMISSAO_A_COMENTARIO_MATRIZ"
COMMENT_TYPE_COMENTARIO_MATRIZ = "COMENTARIO_MATRIZ"

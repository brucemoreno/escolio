"""Schema funcional mínimo de comentário — fonte: P13 §31.5, §31.5.1-31.5.5, §42.

Campo obrigatório vazio impede a criação do registro (validação em
__post_init__, mesma disciplina de escolio/relacao.py e
escolio/contrato/*.py).

Ordem dos campos abaixo difere da ordem literal de §31.5: Python exige que
campos com valor padrão venham depois dos campos sem valor padrão, e só
`related_comment_id`, `matrix_comment_id` e `resolution` são declarados
`X | null` na fonte — os três foram movidos para o final, sem alterar seu
significado (mesmo tratamento dado a `RelacaoAfirmacaoEvidencia`).

Campos cuja tipagem própria pertence a outra sessão do plano
(`comment_type`, `priority`, `severity`, `intervention_level`,
`authority_required`, `gate`, `source_status`, `voice_impact`,
`privacy_classification`, `anchor_start`, `anchor_end`) permanecem `str`
nesta sessão — ver escolio/comentarios/LACUNAS.md.
"""

from dataclasses import dataclass

from escolio.comentarios.erros import ErroDeComentario
from escolio.comentarios.vocabulario import (
    ARQUIVO_FONTE,
    COMMENT_TYPE_REMISSAO_A_COMENTARIO_MATRIZ,
    STATUS_QUE_EXIGEM_RESOLUTION,
    P13CommentResolution,
    P13CommentStatus,
)

_CAMPOS_STR_OBRIGATORIOS = (
    "comment_id",
    "document_id",
    "document_version",
    "module_id",
    "unit_id",
    "anchor_start",
    "anchor_end",
    "anchor_text_hash",
    "comment_type",
    "priority",
    "severity",
    "problem",
    "evidence",
    "impact",
    "recommended_action",
    "intervention_level",
    "authority_required",
    "gate",
    "source_status",
    "voice_impact",
    "privacy_classification",
)


def _exige_nao_vazio(nome_campo: str, valor) -> None:
    if valor is None or (isinstance(valor, str) and valor.strip() == ""):
        raise ErroDeComentario(
            "OBRIGATORIEDADE",
            f"Campo obrigatório '{nome_campo}' vazio impede a criação do registro",
        )


def _exige_nulo_ou_nao_vazio(nome_campo: str, valor: str | None) -> None:
    """§31.5.5 — 'campos não aplicáveis devem ser null, nunca string vazia'."""
    if valor is not None and valor.strip() == "":
        raise ErroDeComentario(
            "31.5.5",
            f"'{nome_campo}' não aplicável deve ser null, nunca string vazia",
        )


@dataclass
class P13Comment:
    # --- Campos obrigatórios (§31.5, sem anotação `| null`) ---
    comment_id: str
    document_id: str
    document_version: str
    module_id: str
    unit_id: str
    anchor_start: str
    anchor_end: str
    anchor_text_hash: str
    comment_type: str
    priority: str
    severity: str
    problem: str
    evidence: str
    impact: str
    recommended_action: str
    intervention_level: str
    authority_required: str
    gate: str
    source_status: str
    voice_impact: str
    privacy_classification: str
    reversible: bool
    status: P13CommentStatus

    # --- Campos anuláveis (§31.5.3, §31.5.4, §31.5.2) ---
    related_comment_id: str | None = None
    matrix_comment_id: str | None = None
    resolution: P13CommentResolution | None = None

    def __post_init__(self) -> None:
        for nome_campo in _CAMPOS_STR_OBRIGATORIOS:
            _exige_nao_vazio(nome_campo, getattr(self, nome_campo))

        if not isinstance(self.status, P13CommentStatus):
            raise ErroDeComentario(
                "31.5.1", "status deve ser um membro de P13CommentStatus", detalhe=repr(self.status)
            )

        self._valida_resolution()
        self._valida_related_comment_id()
        self._valida_matrix_comment_id()

    def _valida_resolution(self) -> None:
        if self.resolution is not None and not isinstance(self.resolution, P13CommentResolution):
            raise ErroDeComentario(
                "31.5.2",
                "resolution deve ser um membro de P13CommentResolution ou null",
                detalhe=repr(self.resolution),
            )
        if self.status in STATUS_QUE_EXIGEM_RESOLUTION and self.resolution is None:
            raise ErroDeComentario(
                "31.5.2",
                "resolution é obrigatório quando status for RESOLVED, SUPERSEDED ou WITHDRAWN",
                detalhe=f"status={self.status.value}",
            )

    def _valida_related_comment_id(self) -> None:
        _exige_nulo_ou_nao_vazio("related_comment_id", self.related_comment_id)
        if self.related_comment_id is not None and self.related_comment_id == self.comment_id:
            raise ErroDeComentario(
                "31.5.3",
                "related_comment_id não pode apontar para o próprio comment_id",
                detalhe=self.comment_id,
            )

    def _valida_matrix_comment_id(self) -> None:
        _exige_nulo_ou_nao_vazio("matrix_comment_id", self.matrix_comment_id)
        if self.matrix_comment_id is not None and self.matrix_comment_id == self.comment_id:
            raise ErroDeComentario(
                "31.5.4",
                "matrix_comment_id não pode apontar para o próprio comment_id",
                detalhe=self.comment_id,
            )
        if (
            self.comment_type == COMMENT_TYPE_REMISSAO_A_COMENTARIO_MATRIZ
            and self.matrix_comment_id is None
        ):
            raise ErroDeComentario(
                "31.5.4",
                "matrix_comment_id é obrigatório quando comment_type=REMISSAO_A_COMENTARIO_MATRIZ",
            )

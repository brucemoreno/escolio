"""Payloads de status e schemas auxiliares — fonte: P09 §14-18, §20.

ErrorPayload (§14), AbstentionPayload (§15), BlockPayload (§16),
Limitation (§17), Warning (§18), SensitivityLabel (§20).
"""

from dataclasses import dataclass, field

from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.referencia import Reference, exige_referencia_verificada
from escolio.contrato.vocabulario import (
    AbstentionCategory,
    BlockCategory,
    ErrorCategory,
    ErrorSeverity,
    LimitationType,
    Materiality,
    SensitivityCategory,
    WarningCategory,
)


@dataclass
class RequiredAction:
    actor: str | None = None
    action: str | None = None


@dataclass
class ErrorTrace:
    input_ids: list[str] = field(default_factory=list)
    event_references: list[str] = field(default_factory=list)


@dataclass
class ErrorPayload:
    error_id: str
    request_id: str
    category: ErrorCategory
    code: str
    severity: ErrorSeverity
    message: str
    technical_detail: str | None = None
    affected_scope: list[str] = field(default_factory=list)
    recoverable: bool = False
    retry_allowed: bool = False
    retry_conditions: list[str] = field(default_factory=list)
    data_preserved: bool = False
    evidence_preserved: bool = False
    required_action: RequiredAction = field(default_factory=RequiredAction)
    trace: ErrorTrace = field(default_factory=ErrorTrace)

    def __post_init__(self):
        # §14.1.8: erro deve conter categoria e código.
        if not self.code:
            raise ErroDeContrato("P09-§14.1", "ErrorPayload exige 'code' preenchido")
        if not self.error_id:
            raise ErroDeContrato("P09-§14", "error_id é obrigatório")
        if not self.request_id:
            raise ErroDeContrato("P09-§14", "request_id é obrigatório")
        if not self.message:
            raise ErroDeContrato("P09-§14", "message é obrigatório")

        # §14.1.4/.5: retry_allowed=true exige ao menos uma condição
        # explícita; retry_allowed=false exige retry_conditions vazio.
        if self.retry_allowed and not self.retry_conditions:
            raise ErroDeContrato(
                "P09-§14.1", "retry_allowed=true exige ao menos uma condição em retry_conditions"
            )
        if not self.retry_allowed and self.retry_conditions:
            raise ErroDeContrato(
                "P09-§14.1", "retry_allowed=false exige retry_conditions vazio"
            )


@dataclass
class AbstentionPayload:
    abstention_id: str
    request_id: str
    category: AbstentionCategory
    reason: str
    scope: list[str] = field(default_factory=list)
    triggering_conditions: list[str] = field(default_factory=list)
    completed_safe_work: list[str] = field(default_factory=list)
    unperformed_work: list[str] = field(default_factory=list)
    evidence_required: list[str] = field(default_factory=list)
    authorization_required: list[str] = field(default_factory=list)
    clarification_required: list[str] = field(default_factory=list)
    reversible: bool = False
    resume_conditions: list[str] = field(default_factory=list)
    human_decision_required: bool = False

    def __post_init__(self):
        if not self.abstention_id:
            raise ErroDeContrato("P09-§15", "abstention_id é obrigatório")
        if not self.request_id:
            raise ErroDeContrato("P09-§15", "request_id é obrigatório")
        if not self.reason:
            raise ErroDeContrato("P09-§15", "reason é obrigatório")

        # §15.1: reversible=true exige resume_conditions com ao menos um
        # item; reversible=false exige justificativa suficiente em reason
        # — verificável em código apenas como "reason não vazio", já
        # garantido acima.
        if self.reversible and not self.resume_conditions:
            raise ErroDeContrato(
                "P09-§15.1", "reversible=true exige resume_conditions com ao menos um item"
            )
        # §21.24 (via §15.1): abstenção reversível sem retomada é inválida
        # — mesma regra do parágrafo acima, listada também na matriz §23.


@dataclass
class BlockPayload:
    block_id: str
    request_id: str
    category: BlockCategory
    description: str
    material_evidence: list[Reference]
    removable: bool
    affected_scope: list[str] = field(default_factory=list)
    removal_action: str | None = None
    responsible_actor: str | None = None
    safe_work_remaining: list[str] = field(default_factory=list)
    total_block_justification: str | None = None

    def __post_init__(self):
        if not self.block_id:
            raise ErroDeContrato("P09-§16", "block_id é obrigatório")
        if not self.request_id:
            raise ErroDeContrato("P09-§16", "request_id é obrigatório")
        if not self.description:
            raise ErroDeContrato("P09-§16", "description é obrigatório")

        # §16.1 / §21.29: bloqueio exige impedimento material comprovado —
        # ao menos uma Reference VERIFIED.
        exige_referencia_verificada(
            self.material_evidence,
            "P09-§21.29",
            "bloqueio exige ao menos uma Reference VERIFIED em material_evidence",
        )

        # §16.1: removable=true exige removal_action não nulo, específico e objetivo.
        if self.removable and not self.removal_action:
            raise ErroDeContrato(
                "P09-§21.31", "bloqueio removível (removable=true) exige removal_action preenchido"
            )

        # §16.1: bloqueio total exige safe_work_remaining vazio e
        # total_block_justification não nulo; bloqueio parcial exige
        # identificação do trabalho seguro restante.
        eh_total = self.total_block_justification is not None
        if eh_total and self.safe_work_remaining:
            raise ErroDeContrato(
                "P09-§16.1",
                "bloqueio total (total_block_justification preenchido) exige safe_work_remaining vazio",
            )
        if not eh_total and not self.safe_work_remaining:
            raise ErroDeContrato(
                "P09-§16.1",
                "safe_work_remaining deve ser sempre preenchido: bloqueio parcial exige o trabalho seguro restante; bloqueio total exige total_block_justification",
            )


@dataclass
class Limitation:
    limitation_id: str
    type: LimitationType
    description: str
    effect_on_result: str
    materiality: Materiality
    affected_items: list[str] = field(default_factory=list)
    can_be_resolved: bool = False
    resolution_condition: str | None = None

    def __post_init__(self):
        if not self.limitation_id:
            raise ErroDeContrato("P09-§17", "limitation_id é obrigatório")
        if not self.description:
            raise ErroDeContrato("P09-§17", "description é obrigatório")
        if not self.effect_on_result:
            raise ErroDeContrato(
                "P09-§17", "limitação deve informar explicitamente seu efeito sobre o resultado"
            )

    @property
    def impede_sucesso_integral(self) -> bool:
        """§17: limitação de materialidade alta incompatível com conclusão
        integral impede SUCCESS. 'Incompatível com conclusão integral' não
        tem campo próprio na fonte; tratamos toda materiality=HIGH como
        impeditiva — ver LACUNAS.md."""
        return self.materiality == Materiality.HIGH


@dataclass
class Warning:
    warning_id: str
    category: WarningCategory
    message: str
    affected_items: list[str] = field(default_factory=list)
    requires_action: bool = False

    def __post_init__(self):
        if not self.warning_id:
            raise ErroDeContrato("P09-§18", "warning_id é obrigatório")
        if not self.message:
            raise ErroDeContrato("P09-§18", "message é obrigatório")


@dataclass
class SensitivityLabel:
    category: SensitivityCategory
    source_policy: str
    justification: str | None = None

    def __post_init__(self):
        if not self.source_policy:
            raise ErroDeContrato("P09-§20.1", "source_policy é obrigatório e deve identificar a política aplicável")
        if self.category == SensitivityCategory.OTHER_CONTROLLED and not self.justification:
            raise ErroDeContrato(
                "P09-§20.1", "category=OTHER_CONTROLLED exige justification não nula"
            )

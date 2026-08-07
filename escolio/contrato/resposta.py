"""Envelope universal de resposta — fonte: P09 §8, §9.

Os cinco status (§8) são mutuamente exclusivos; cada um exige seu próprio
padrão de payload (§8.2). safe_result (§9) é a única fonte de verdade sobre
trabalho seguro preservado — não coexiste com SUCCESS/PARTIAL_SUCCESS/
ABSTAINED/BLOCKED (só é aplicável em ERROR).
"""

from dataclasses import dataclass, field

from escolio.contrato.afirmacao import ClaimEvidence
from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.payloads import (
    AbstentionPayload,
    BlockPayload,
    ErrorPayload,
    Limitation,
    SensitivityLabel,
    Warning,
)
from escolio.contrato.referencia import Reference, SemanticVersion, exige_referencia_verificada
from escolio.contrato.vocabulario import ResponseStatus


@dataclass
class SafeResult:
    available: bool = False
    content: object | None = None
    reference: Reference | None = None
    scope: list[str] = field(default_factory=list)
    limitations: list[Limitation] = field(default_factory=list)

    def __post_init__(self):
        if self.available:
            # §9.1: pelo menos um dos dois (content, reference) deve existir.
            if self.content is None and self.reference is None:
                raise ErroDeContrato(
                    "P09-§9.1",
                    "safe_result.available=true exige content ou reference preenchido",
                )
            # §9.1: reference, quando utilizada, deve ser VERIFIED.
            if self.reference is not None and not self.reference.verified:
                raise ErroDeContrato(
                    "P09-§21.40", "safe_result.reference, quando utilizada, deve ser VERIFIED"
                )
            # §9.1: scope deve conter pelo menos um item.
            if not self.scope:
                raise ErroDeContrato(
                    "P09-§9.1", "safe_result.available=true exige scope com pelo menos um item"
                )
        else:
            # §9.1 / §21.41: available=false exige content e reference nulos e scope vazio.
            if self.content is not None or self.reference is not None:
                raise ErroDeContrato(
                    "P09-§21.41", "safe_result.available=false exige content e reference nulos"
                )
            if self.scope:
                raise ErroDeContrato(
                    "P09-§9.1", "safe_result.available=false exige scope vazio"
                )


@dataclass
class Completion:
    scope_completed: list[str] = field(default_factory=list)
    scope_not_completed: list[str] = field(default_factory=list)
    partiality_cause: str | None = None


@dataclass
class ResultItem:
    """§8: `result.structured_items: [ResultItem]` — a fonte declara o tipo
    no envelope sem definir seu schema interno (é lacuna deliberada do P09,
    §25: "linguagem concreta de schema" pertence à implementação). Mantido
    como estrutura mínima aberta — ver LACUNAS.md."""

    item_id: str
    content: object | None = None


@dataclass
class Result:
    type: str = ""
    content: object | None = None
    structured_items: list[ResultItem] = field(default_factory=list)


@dataclass
class SecurityFlags:
    sensitive_content_present: bool = False
    sensitivity_labels: list[SensitivityLabel] = field(default_factory=list)
    adversarial_content_detected: bool = False
    output_sanitized: bool = False

    def __post_init__(self):
        # §20.1 / §21.33: sensibilidade presente exige rótulo controlado.
        if self.sensitive_content_present and not self.sensitivity_labels:
            raise ErroDeContrato(
                "P09-§21.33", "sensitive_content_present=true exige ao menos um SensitivityLabel"
            )


@dataclass
class ResponseTrace:
    input_ids: list[str] = field(default_factory=list)
    source_references: list[Reference] = field(default_factory=list)
    decision_references: list[Reference] = field(default_factory=list)
    dependency_references: list[Reference] = field(default_factory=list)


@dataclass
class NextAction:
    required: bool = False
    type: str | None = None
    description: str | None = None


@dataclass
class Evidence:
    claims: list[ClaimEvidence] = field(default_factory=list)


@dataclass
class Response:
    schema_version: SemanticVersion
    response_id: str
    request_id: str
    project_id: str
    component_id: str
    function_id: str
    status: ResponseStatus
    produced_at: str | None = None
    result: Result = field(default_factory=Result)
    safe_result: SafeResult = field(default_factory=SafeResult)
    error: ErrorPayload | None = None
    abstention: AbstentionPayload | None = None
    block: BlockPayload | None = None
    evidence: Evidence = field(default_factory=Evidence)
    # interventions: [InterventionRecord] — fora do escopo desta peça (item
    # 2 do roadmap, junto com os níveis P06). Não incluído aqui.
    limitations: list[Limitation] = field(default_factory=list)
    warnings: list[Warning] = field(default_factory=list)
    security: SecurityFlags = field(default_factory=SecurityFlags)
    trace: ResponseTrace = field(default_factory=ResponseTrace)
    next_action: NextAction = field(default_factory=NextAction)
    completion: Completion = field(default_factory=Completion)

    def __post_init__(self):
        for nome in ("response_id", "request_id", "project_id", "component_id", "function_id"):
            if not getattr(self, nome):
                raise ErroDeContrato("P09-§8", f"'{nome}' é obrigatório")

        payloads_presentes = {
            ResponseStatus.ERROR: self.error is not None,
            ResponseStatus.ABSTAINED: self.abstention is not None,
            ResponseStatus.BLOCKED: self.block is not None,
        }
        # §21.34: erro, abstenção e bloqueio são mutuamente exclusivos —
        # nenhum mesmo evento pode receber mais de um payload preenchido.
        payloads_preenchidos = [nome for nome, presente in payloads_presentes.items() if presente]
        if len(payloads_preenchidos) > 1:
            raise ErroDeContrato(
                "P09-§21.34",
                "erro, abstenção e bloqueio são mutuamente exclusivos",
                detalhe=f"payloads preenchidos simultaneamente: {[s.value for s in payloads_preenchidos]}",
            )

        if self.status == ResponseStatus.SUCCESS:
            self._valida_success()
        elif self.status == ResponseStatus.PARTIAL_SUCCESS:
            self._valida_partial_success()
        elif self.status == ResponseStatus.ERROR:
            self._valida_error()
        elif self.status == ResponseStatus.ABSTAINED:
            self._valida_abstained()
        elif self.status == ResponseStatus.BLOCKED:
            self._valida_blocked()

    def _exige_payloads_nulos(self, *, exceto: str, regra_id: str) -> None:
        exigidos = {"error": self.error, "abstention": self.abstention, "block": self.block}
        for nome, valor in exigidos.items():
            if nome != exceto and valor is not None:
                raise ErroDeContrato(regra_id, f"status={self.status.value} exige {nome}=null")

    def _valida_success(self) -> None:
        # §8.2 SUCCESS / §21.6.
        self._exige_payloads_nulos(exceto="", regra_id="P09-§8.2")
        if self.safe_result.available:
            raise ErroDeContrato("P09-§8.2", "SUCCESS exige safe_result.available=false")
        if self.completion.scope_not_completed:
            raise ErroDeContrato("P09-§8.2", "SUCCESS exige completion.scope_not_completed vazio")
        if self.completion.partiality_cause is not None:
            raise ErroDeContrato("P09-§8.2", "SUCCESS exige completion.partiality_cause=null")
        # §17 / §21.43: limitação de materialidade alta impede SUCCESS.
        if any(l.impede_sucesso_integral for l in self.limitations):
            raise ErroDeContrato(
                "P09-§21.43",
                "limitação impeditiva (materiality=HIGH) não pode coexistir com SUCCESS",
            )

    def _valida_partial_success(self) -> None:
        # §8.2 PARTIAL_SUCCESS.
        self._exige_payloads_nulos(exceto="", regra_id="P09-§8.2")
        if self.safe_result.available:
            raise ErroDeContrato("P09-§8.2", "PARTIAL_SUCCESS exige safe_result.available=false")
        if not self.completion.scope_completed:
            raise ErroDeContrato(
                "P09-§8.2", "PARTIAL_SUCCESS exige completion.scope_completed com pelo menos um item"
            )
        if not self.completion.scope_not_completed:
            raise ErroDeContrato(
                "P09-§8.2", "PARTIAL_SUCCESS exige completion.scope_not_completed com pelo menos um item"
            )
        if not self.completion.partiality_cause:
            raise ErroDeContrato("P09-§8.2", "PARTIAL_SUCCESS exige completion.partiality_cause preenchido")

    def _valida_error(self) -> None:
        # §8.2 ERROR / §21.8.
        if self.error is None:
            raise ErroDeContrato("P09-§21.8", "ERROR exige ErrorPayload preenchido")
        if self.abstention is not None:
            raise ErroDeContrato("P09-§8.2", "ERROR exige abstention=null")
        if self.block is not None:
            raise ErroDeContrato("P09-§8.2", "ERROR exige block=null")
        # §9: safe_result coerente é verificado pelo próprio SafeResult.__post_init__.

    def _valida_abstained(self) -> None:
        # §8.2 ABSTAINED / §21.7.
        if self.abstention is None:
            raise ErroDeContrato("P09-§21.7", "ABSTAINED exige AbstentionPayload preenchido")
        if self.error is not None:
            raise ErroDeContrato("P09-§8.2", "ABSTAINED exige error=null")
        if self.block is not None:
            raise ErroDeContrato("P09-§8.2", "ABSTAINED exige block=null")
        if self.safe_result.available:
            raise ErroDeContrato("P09-§8.2", "ABSTAINED exige safe_result.available=false")

    def _valida_blocked(self) -> None:
        # §8.2 BLOCKED / §21.9.
        if self.block is None:
            raise ErroDeContrato("P09-§21.9", "BLOCKED exige BlockPayload preenchido")
        if self.error is not None:
            raise ErroDeContrato("P09-§8.2", "BLOCKED exige error=null")
        if self.abstention is not None:
            raise ErroDeContrato("P09-§8.2", "BLOCKED exige abstention=null")
        if self.safe_result.available:
            raise ErroDeContrato("P09-§8.2", "BLOCKED exige safe_result.available=false")


def exige_correspondencia_request_response(request, response) -> None:
    """§8.1 / §21.1-3: correspondência obrigatória de project_id,
    component_id e request_id entre requisição e resposta."""
    if response.request_id != request.request_id:
        raise ErroDeContrato("P09-§21.1", "response.request_id deve corresponder à requisição")
    if response.project_id != request.project_id:
        raise ErroDeContrato("P09-§21.2", "response.project_id deve ser idêntico a request.project_id")
    if response.component_id != request.component_id:
        raise ErroDeContrato("P09-§21.3", "response.component_id deve ser idêntico a request.component_id")

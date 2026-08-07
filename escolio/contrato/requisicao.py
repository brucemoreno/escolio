"""Envelope universal de requisição — fonte: P09 §4.

Campos obrigatórios (§4.1) e regras (§4.2) validados em __post_init__.
Regras que dependem de estado externo ao envelope (função pertence ao
componente vigente, §4.2.3-4.2.5) não são verificáveis apenas com os dados
da própria requisição — ver LACUNAS.md.
"""

from dataclasses import dataclass, field

from escolio.contrato.dependencia import DependencyItem
from escolio.contrato.entrada import InputItem
from escolio.contrato.contexto import ContextItem
from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.referencia import Reference, SemanticVersion, exige_referencia_verificada
from escolio.contrato.vocabulario import AuthorizationStatus, SensitivityCategory


@dataclass
class Requester:
    role: str
    actor_id: str | None = None
    authority_basis: str = ""


@dataclass
class Scope:
    allowed_operations: list[str] = field(default_factory=list)
    prohibited_operations: list[str] = field(default_factory=list)
    object_ids: list[str] = field(default_factory=list)
    boundaries: list[str] = field(default_factory=list)


@dataclass
class Constraints:
    intervention_level: str | None = None
    output_format: str | None = None
    language: str | None = None
    length_limit: int | None = None
    privacy_classification: list[SensitivityCategory] = field(default_factory=list)
    security_flags: list[str] = field(default_factory=list)


@dataclass
class Authorization:
    status: AuthorizationStatus
    evidence: list[Reference] = field(default_factory=list)


@dataclass
class ExpectedOutput:
    type: str
    minimum_fields: list[str] = field(default_factory=list)


@dataclass
class Trace:
    parent_request_id: str | None = None
    workflow_id: str | None = None


@dataclass
class Request:
    schema_version: SemanticVersion
    request_id: str
    project_id: str
    component_id: str
    function_id: str
    operation: str
    requester: Requester
    scope: Scope
    authorization: Authorization
    expected_output: ExpectedOutput
    created_at: str | None = None
    inputs: list[InputItem] = field(default_factory=list)
    context: list[ContextItem] = field(default_factory=list)
    dependencies: list[DependencyItem] = field(default_factory=list)
    constraints: Constraints = field(default_factory=Constraints)
    trace: Trace = field(default_factory=Trace)

    def __post_init__(self):
        # §4.1 — campos obrigatórios.
        for nome in ("request_id", "project_id", "component_id", "function_id", "operation"):
            if not getattr(self, nome):
                raise ErroDeContrato("P09-§4.1", f"'{nome}' é obrigatório")
        if not self.requester.role:
            raise ErroDeContrato("P09-§4.1", "requester.role é obrigatório")
        if not self.expected_output.type:
            raise ErroDeContrato("P09-§4.1", "expected_output.type é obrigatório")

        # §4.2.9: operação presente simultaneamente em allowed_operations e
        # prohibited_operations é inválida.
        conflito = set(self.scope.allowed_operations) & set(self.scope.prohibited_operations)
        if conflito:
            raise ErroDeContrato(
                "P09-§4.2.9",
                "operação presente simultaneamente em allowed_operations e prohibited_operations é inválida",
                detalhe=f"operações em conflito: {sorted(conflito)}",
            )

        # §4.2.10: operação proibida prevalece sobre autorização genérica.
        if self.operation in self.scope.prohibited_operations:
            raise ErroDeContrato(
                "P09-§4.2.10",
                "operação proibida prevalece sobre autorização genérica",
                detalhe=f"operation={self.operation!r} está em prohibited_operations",
            )

        # §4.2.8: operation deve constar entre as operações autorizadas.
        if self.scope.allowed_operations and self.operation not in self.scope.allowed_operations:
            raise ErroDeContrato(
                "P09-§4.2.8",
                "operation deve constar entre as operações autorizadas",
                detalhe=f"operation={self.operation!r} não está em allowed_operations",
            )

        # §4.2.12: autorização VALID exige ao menos uma Reference VERIFIED.
        if self.authorization.status == AuthorizationStatus.VALID:
            exige_referencia_verificada(
                self.authorization.evidence,
                "P09-§21.27",
                "autorização VALID exige ao menos uma Reference VERIFIED",
            )

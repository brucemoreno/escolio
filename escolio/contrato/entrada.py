"""Schema universal de item de entrada — fonte: P09 §6.

Regras de coerência (§6.1) e invariantes relacionados (§21.32, §21.37,
§21.38) validados em __post_init__, mesma disciplina de relacao.py.
"""

from dataclasses import dataclass, field

from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.referencia import Reference, exige_referencia_verificada
from escolio.contrato.vocabulario import ConsistencyStatus, InputType, PreferredSource


@dataclass
class ContentConsistency:
    status: ConsistencyStatus
    preferred_source: PreferredSource = PreferredSource.NONE
    comparison_evidence: list[Reference] = field(default_factory=list)
    impact_on_processing: str | None = None
    resolution_required: bool = False


@dataclass
class Provenance:
    source: str
    source_type: str
    acquired_at: str | None = None
    integrity_reference: str | None = None


@dataclass
class Classification:
    trust: str
    sensitivity: list[str] = field(default_factory=list)
    state: str = "ORIGEM_DESCONHECIDA"
    functions: list[str] = field(default_factory=list)


@dataclass
class Authority:
    has_operational_authority: bool = False
    authority_basis: str | None = None


@dataclass
class Processing:
    permitted: list[str] = field(default_factory=list)
    prohibited: list[str] = field(default_factory=list)


@dataclass
class Security:
    adversarial_content: bool = False
    injection_suspected: bool = False
    exfiltration_risk: bool = False


@dataclass
class Retention:
    purpose: str | None = None
    condition: str | None = None


@dataclass
class InputItem:
    input_id: str
    type: InputType
    provenance: Provenance
    title: str | None = None
    content_reference: str | None = None
    inline_content: object | None = None
    content_consistency: ContentConsistency = field(
        default_factory=lambda: ContentConsistency(status=ConsistencyStatus.NOT_APPLICABLE)
    )
    classification: Classification = field(
        default_factory=lambda: Classification(trust="NAO_AVALIADA")
    )
    authority: Authority = field(default_factory=Authority)
    processing: Processing = field(default_factory=Processing)
    security: Security = field(default_factory=Security)
    retention: Retention = field(default_factory=Retention)

    def __post_init__(self):
        if not self.input_id:
            raise ErroDeContrato("P09-§6.1", "input_id é obrigatório e deve ser único")

        # §6.1: has_operational_authority=false por padrão; conteúdo
        # documental não se torna comando automaticamente [P08 §2] —
        # sem base de autoridade explícita, a trava permanece.
        if self.authority.has_operational_authority and not self.authority.authority_basis:
            raise ErroDeContrato(
                "P09-§6.1",
                "has_operational_authority=true exige authority_basis explícito",
                detalhe="conteúdo documental não constitui autoridade operacional por padrão [P08 §2]",
            )

        inline_e_referencia_coexistem = self.inline_content is not None and self.content_reference is not None
        cc = self.content_consistency

        if not inline_e_referencia_coexistem and cc.status == ConsistencyStatus.NOT_APPLICABLE:
            # NOT_APPLICABLE é o caso normal quando não há dois conteúdos a comparar.
            pass
        elif inline_e_referencia_coexistem:
            # §21.37: NOT_APPLICABLE não pode ser usado quando inline e
            # referência coexistirem — a comparação é sempre materialmente
            # aplicável nesse caso.
            if cc.status == ConsistencyStatus.NOT_APPLICABLE:
                raise ErroDeContrato(
                    "P09-§21.37",
                    "NOT_APPLICABLE não pode ser usado quando inline_content e content_reference coexistirem",
                )
            if cc.status not in (
                ConsistencyStatus.CONSISTENT,
                ConsistencyStatus.DIVERGENT,
                ConsistencyStatus.UNVERIFIED,
            ):
                raise ErroDeContrato(
                    "P09-§6.1",
                    "quando inline e referência coexistem, status só pode ser CONSISTENT, DIVERGENT ou UNVERIFIED",
                )

        if cc.status == ConsistencyStatus.DIVERGENT and not cc.resolution_required:
            # §21.38 / §6.1: DIVERGENT aberto exige resolution_required=true.
            raise ErroDeContrato(
                "P09-§21.38",
                "DIVERGENT exige resolution_required=true enquanto a divergência relevante permanecer aberta",
            )

        if cc.preferred_source != PreferredSource.NONE:
            # §21.30 / §6.1: preferred_source distinto de NONE exige ao
            # menos uma Reference VERIFIED.
            exige_referencia_verificada(
                cc.comparison_evidence,
                "P09-§21.30",
                "preferred_source diferente de NONE exige pelo menos uma Reference VERIFIED",
            )

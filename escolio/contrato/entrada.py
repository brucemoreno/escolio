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
    """Quatro eixos independentes [P08 §4]. Rótulo de um eixo não vale no campo de outro.

    `trust` — cinco rótulos [P08 §4.1]: CONFIAVEL_CANONICO, CONFIAVEL_NAO_CANONICO,
    NAO_CONFIAVEL, SUSPEITO, ORIGEM_DESCONHECIDA.

    `state` — nove rótulos [P08 §4.1]: ORIGINAL, COPIA_VERIFICADA, DERIVADO, EM_ANALISE,
    HOMOLOGADO, CONGELADO, SUPERADO, ARQUIVADO, DESTINADO_A_DESCARTE.

    O default de `state` abaixo é DEFEITO CONHECIDO E PRESERVADO — ver CO-013 em
    docs/coleta.md. ORIGEM_DESCONHECIDA é rótulo de `trust`, não de `state`. Não foi
    substituído porque não existe valor correto a colocar: [P09 §6] declara `state: string`
    sem `| null` (e marca `| null` explicitamente em acquired_at, integrity_reference,
    authority_basis e retention.*), enquanto os nove estados de [P08 §4.1] não incluem
    nenhum que signifique "ainda não classificado". Trocar por um dos nove seria inferência
    [P00/07; P09 §4.2.14]. Mesma classe de defeito de LAC-SEG-001
    (docs/spec/operacional-P08.md §10): o InputItem não representa "ainda não avaliado".

    `trust` e `state` são `str` e não enum porque [P09 §6] os tipa `string` — o vocabulário
    fechado é do P08, e apertar o tipo aqui é decisão pendente, não conserto.
    """

    trust: str
    sensitivity: list[str] = field(default_factory=list)
    state: str = "ORIGEM_DESCONHECIDA"  # DEFEITO PRESERVADO — CO-013, docstring acima
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
    # trust=ORIGEM_DESCONHECIDA: [P09 §6.1] "item sem proveniência suficiente deve ser
    # marcado como ORIGEM_DESCONHECIDA". Era "NAO_AVALIADA" até 2026-08-07 — valor dos
    # enums Sufficiency/Confidence do P05 (escolio/vocabulario.py), vocabulário de outro
    # componente num campo do eixo de confiança do P08 [BL-016].
    classification: Classification = field(
        default_factory=lambda: Classification(trust="ORIGEM_DESCONHECIDA")
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

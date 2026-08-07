"""Schema de afirmação e evidência do envelope P09 — fonte: P09 §12.

Distinto de escolio.relacao.RelacaoAfirmacaoEvidencia (P05): vocabulário
próprio (ClaimType, Sufficiency, Confidence, ClaimStatus em
escolio.contrato.vocabulario), campos próprios, sem mapeamento de código
entre os dois — ver docs/backlog.md BL-002 e LACUNAS.md desta peça.
"""

from dataclasses import dataclass, field

from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.referencia import Location, Reference
from escolio.contrato.vocabulario import ClaimStatus, ClaimType, Confidence, Sufficiency


@dataclass
class ClaimEvidence:
    claim_id: str
    claim_text: str
    claim_type: ClaimType
    sufficiency: Sufficiency
    confidence: Confidence
    status: ClaimStatus
    evidence_ids: list[str] = field(default_factory=list)
    source_references: list[Reference] = field(default_factory=list)
    location: Location = field(default_factory=Location)
    notes: str | None = None

    def __post_init__(self):
        if not self.claim_id:
            raise ErroDeContrato("P09-§12", "claim_id é obrigatório")
        if not self.claim_text:
            raise ErroDeContrato("P09-§12", "claim_text é obrigatório")

        # §12.1: afirmação factual deve possuir evidência ou ser marcada
        # como não sustentada.
        sem_evidencia = not self.evidence_ids and not self.source_references
        if self.claim_type == ClaimType.FACT and sem_evidencia and self.status != ClaimStatus.UNSUPPORTED:
            raise ErroDeContrato(
                "P09-§12.1",
                "afirmação factual sem evidência deve ser marcada status=UNSUPPORTED",
            )

        # §21.20: ausência de evidência não pode resultar em SUPPORTED.
        if sem_evidencia and self.status == ClaimStatus.SUPPORTED:
            raise ErroDeContrato(
                "P09-§21.20", "ausência de evidência não pode resultar em status=SUPPORTED"
            )

        # §12.1: SUPPORTED exige suficiência compatível (não pode ser
        # INSUFFICIENT nem NOT_APPLICABLE).
        if self.status == ClaimStatus.SUPPORTED and self.sufficiency in (
            Sufficiency.INSUFFICIENT,
            Sufficiency.NOT_APPLICABLE,
        ):
            raise ErroDeContrato(
                "P09-§12.1",
                "status=SUPPORTED exige suficiência compatível",
                detalhe=f"sufficiency={self.sufficiency.value} não sustenta SUPPORTED",
            )

        # §12.1: claim conflitante deve preservar referências de todas as
        # fontes relevantes — verificável em código apenas como "não vazio".
        if self.status == ClaimStatus.CONFLICTED and not self.source_references:
            raise ErroDeContrato(
                "P09-§12.1",
                "status=CONFLICTED deve preservar referências de todas as fontes relevantes",
                detalhe="source_references vazio",
            )

"""Schema de referência — fonte: P09 §19.

`Reference` sustenta autorização VALID, dependência satisfeita, fonte
preferencial, bloqueio material e resultado seguro referenciado — mas só
quando `provenance_status=VERIFIED` (§19.1, invariantes §21.27-30, 40).
Referências PARTIAL/UNKNOWN/CONFLICTED são preservadas e podem sustentar
alerta, limitação ou conflito, nunca autoridade ou bloqueio conclusivo.
"""

from dataclasses import dataclass, field

from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.vocabulario import ProvenanceStatus


@dataclass
class SemanticVersion:
    """§3 — única representação de versão válida; string livre é inválida."""

    major: int
    minor: int
    patch: int

    def __post_init__(self):
        for nome, valor in (("major", self.major), ("minor", self.minor), ("patch", self.patch)):
            if not isinstance(valor, int) or valor < 0:
                raise ErroDeContrato(
                    "P09-§3",
                    "SemanticVersion exige major/minor/patch inteiros não negativos",
                    detalhe=f"{nome}={valor!r}",
                )


@dataclass
class Location:
    """Estrutura de localização reutilizada por Reference (§19) e
    ClaimEvidence (§12) — o P09 declara os dois blocos `location` de forma
    idêntica, sem nomear um schema comum; nomeado aqui para não duplicar."""

    page: str | None = None
    section: str | None = None
    timestamp: str | None = None
    record: str | None = None


@dataclass
class Reference:
    reference_id: str
    object_id: str
    object_type: str
    provenance_status: ProvenanceStatus
    version: SemanticVersion | None = None
    integrity_reference: str | None = None
    location: Location = field(default_factory=Location)

    def __post_init__(self):
        if not self.reference_id:
            raise ErroDeContrato("P09-§19", "reference_id é obrigatório")
        if not self.object_id:
            raise ErroDeContrato("P09-§19", "object_id é obrigatório")
        if not self.object_type:
            raise ErroDeContrato("P09-§19", "object_type é obrigatório")

    @property
    def verified(self) -> bool:
        return self.provenance_status == ProvenanceStatus.VERIFIED


def exige_referencia_verificada(referencias: list[Reference], regra_id: str, fundamento: str) -> None:
    """Levanta ErroDeContrato quando nenhuma referência da lista é VERIFIED.

    Reaplicado pelos invariantes §21.27 (autorização VALID), §21.28
    (dependência satisfeita), §21.29 (bloqueio), §21.30 (fonte preferencial)
    e pela regra de resultado seguro referenciado (§9.1).
    """
    if not any(r.verified for r in referencias):
        raise ErroDeContrato(
            regra_id,
            fundamento,
            detalhe="nenhuma Reference com provenance_status=VERIFIED na lista fornecida",
        )

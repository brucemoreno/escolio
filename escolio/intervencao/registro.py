"""InterventionRecord — fonte: P09 §13.

Regras gerais [§13.1] e por disposição [§13.2-13.5] validadas em
__post_init__, mesma disciplina de escolio/contrato/*.py.

`requested_level` e `applied_level` usam NivelIntervencao (P06), não string
livre — a fonte declara `string` no YAML porque P06 e P09 são pacotes
homologados independentes; aqui os dois já existem em código e a
tipagem forte é estritamente mais restritiva, nunca menos.
"""

from dataclasses import dataclass

from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.vocabulario import AuthorizationStatus
from escolio.intervencao.niveis import NivelIntervencao, excede
from escolio.intervencao.vocabulario import Disposition


@dataclass
class InterventionRecord:
    intervention_id: str
    target_id: str
    requested_level: NivelIntervencao
    applied_level: NivelIntervencao | None
    authority_status: AuthorizationStatus
    operation: str
    disposition: Disposition
    rationale: str
    reversible: bool
    requires_human_decision: bool
    before_reference: str | None = None
    after_reference: str | None = None

    def __post_init__(self):
        if not self.intervention_id:
            raise ErroDeContrato("P09-§13", "intervention_id é obrigatório")
        if not self.target_id:
            raise ErroDeContrato("P09-§13", "target_id é obrigatório")
        if not self.operation:
            raise ErroDeContrato("P09-§13", "operation é obrigatório")
        if not self.rationale:
            raise ErroDeContrato("P09-§13", "rationale é obrigatório")

        # §13.1: applied_level não nulo com disposition != APPLIED é inválido.
        if self.applied_level is not None and self.disposition != Disposition.APPLIED:
            raise ErroDeContrato(
                "P09-§13.1",
                "applied_level não nulo com disposition diferente de APPLIED torna o registro inválido",
                detalhe=f"disposition={self.disposition.value}",
            )

        # §13.1 / §13.3-13.5: disposition=APPLIED com applied_level=null é
        # inválido; REFUSED, ABSTAINED e BLOCKED exigem applied_level=null.
        if self.disposition == Disposition.APPLIED and self.applied_level is None:
            raise ErroDeContrato(
                "P09-§13.1", "disposition=APPLIED com applied_level=null torna o registro inválido"
            )
        if self.disposition != Disposition.APPLIED and self.applied_level is not None:
            raise ErroDeContrato(
                "P09-§13",
                f"disposition={self.disposition.value} exige applied_level=null",
            )

        if self.disposition == Disposition.APPLIED:
            self._valida_applied()
        else:
            self._valida_nao_aplicada()

    def _valida_applied(self) -> None:
        # §13.2: applied_level não pode exceder requested_level.
        if excede(self.applied_level, self.requested_level):
            raise ErroDeContrato(
                "P09-§13.2",
                "applied_level não pode exceder requested_level",
                detalhe=f"applied_level={self.applied_level.value} requested_level={self.requested_level.value}",
            )
        # §13.2: a intervenção deve estar autorizada.
        if self.authority_status != AuthorizationStatus.VALID:
            raise ErroDeContrato(
                "P09-§13.2",
                "disposition=APPLIED exige authority_status=VALID",
                detalhe=f"authority_status={self.authority_status.value}",
            )

    def _valida_nao_aplicada(self) -> None:
        # §13.3-13.5: nenhuma transformação registrada como executada —
        # verificável em código como after_reference=null; a fonte só
        # exige after_reference=null "quando representaria transformação
        # inexistente", ou seja, sempre neste caso (não há transformação
        # real a referenciar quando não houve APPLIED).
        if self.after_reference is not None:
            raise ErroDeContrato(
                "P09-§13.3",
                f"disposition={self.disposition.value} exige after_reference=null — nenhuma transformação foi executada",
            )

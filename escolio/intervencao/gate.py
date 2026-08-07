"""Gate de autorização de nível — fonte:
05_PROTOCOLO_DE_AUTORIZACAO_E_ABSTENCAO_P06_R01.txt;
06_PROTOCOLO_DE_INTERVENCAO_EM_OBJETOS_CONGELADOS_P06_R01.txt.

Decide, para um nível pretendido e um teto de nível autorizado, se a
intervenção pode proceder, e produz o InterventionRecord correspondente
quando não pode: regride ao nível máximo ainda autorizado com
disposition=ABSTAINED (nenhum nível operativo permanece válido) ou
disposition=REFUSED/BLOCKED conforme a causa registrada por quem chama.

Este módulo não decide a causa do bloqueio — apenas aplica a regra
estrutural comum (teto, regressão, ausência de herança). A causa
(comando vago, objeto congelado, conflito, etc.) é responsabilidade de
quem invoca, que a passa em `rationale`.
"""

from dataclasses import dataclass

from escolio.contrato.vocabulario import AuthorizationStatus
from escolio.intervencao.niveis import (
    NivelIntervencao,
    excede,
    nivel_maximo_ainda_autorizado,
)
from escolio.intervencao.registro import InterventionRecord
from escolio.intervencao.vocabulario import Disposition


@dataclass(frozen=True)
class DecisaoDeGate:
    """Resultado da verificação de gate: o nível no qual a intervenção pode
    proceder (None se ABSTENCAO), e se houve regressão em relação ao nível
    pretendido."""

    nivel_autorizado: NivelIntervencao | None
    houve_regressao: bool


def decidir_nivel(
    nivel_pretendido: NivelIntervencao,
    niveis_autorizados: frozenset[NivelIntervencao],
) -> DecisaoDeGate:
    """§8 — regressão segura: se `nivel_pretendido` está autorizado, procede
    nele. Senão, regride ao nível máximo ainda autorizado sem exceder o
    pretendido. Se nenhum nível operativo permanecer válido, retorna
    nivel_autorizado=None — sinal para ABSTENCAO [§15 do dicionário]."""
    if nivel_pretendido in niveis_autorizados and not excede(nivel_pretendido, nivel_pretendido):
        return DecisaoDeGate(nivel_autorizado=nivel_pretendido, houve_regressao=False)

    regredido = nivel_maximo_ainda_autorizado(nivel_pretendido, niveis_autorizados)
    if regredido is None:
        return DecisaoDeGate(nivel_autorizado=None, houve_regressao=True)
    return DecisaoDeGate(nivel_autorizado=regredido, houve_regressao=regredido != nivel_pretendido)


def registro_de_abstencao(
    intervention_id: str,
    target_id: str,
    nivel_pretendido: NivelIntervencao,
    operation: str,
    rationale: str,
) -> InterventionRecord:
    """§8, §15 — ABSTENCAO obrigatória quando nenhum nível operativo
    permanece válido. `before_reference`/`after_reference` ficam nulos:
    nenhuma transformação foi executada."""
    return InterventionRecord(
        intervention_id=intervention_id,
        target_id=target_id,
        requested_level=nivel_pretendido,
        applied_level=None,
        authority_status=AuthorizationStatus.INVALID,
        operation=operation,
        disposition=Disposition.ABSTAINED,
        rationale=rationale,
        reversible=True,
        requires_human_decision=True,
    )

"""Camada de detecção de fidelidade de voz/autoria (Camada A) — Etapa 13
do P13.

Autorizado por
`INSTRUCOES_COMPLEMENTARES_IMPLEMENTACAO_ECOSSISTEMA_REVISAO_LLM_R01.md §1`:
`escolio/voz/fidelidade.py::avaliar()` (Camada B, decisória) aplica regras
sobre fatos já apurados, mas não inspeciona texto — não constitui, por si
só, mecanismo de detecção. Este módulo é a Camada A: compara texto e
perfil de voz, produz fatos estruturados, nunca decide.

    TEXTO_ORIGINAL + TEXTO_PROPOSTO_OU_REVISADO (opcional) + PERFIL_P07
    → este módulo (detecção)
    → FATOS_ESTRUTURADOS + EVIDENCIAS + CONFIANCA
    → fidelidade.py::avaliar() (decisão, inalterado)

Requisitos da fonte (§1.3), verbatim, cada um com o campo que o satisfaz
abaixo: comparar material textual real (`texto_original`/`texto_proposto`
como entrada de quem produz o achado — este módulo não os processa
sozinho, ver docstring de `AchadoDeFidelidade`); apontar sinais
(`evidencia`); distinguir fato observado de inferência (`observado`,
booleano explícito, nunca implícito); registrar confiança quando a
detecção não é determinística (`confianca`); não reduzir a análise a um
booleano sem justificativa (`observado=True` exige `evidencia` não vazia);
não inventar critério de voz além do autorizado pelo perfil P07 — por
isso `tipo` é `DesvioBloqueante`, o vocabulário fechado de oito membros
já existente [P07], nunca uma categoria nova.
"""

from __future__ import annotations

from dataclasses import dataclass

from escolio.voz.erros import ErroDePerfilDeVoz
from escolio.voz.vocabulario import Confidence, DesvioBloqueante

ARQUIVO_INSTRUCAO = "INSTRUCOES_COMPLEMENTARES_IMPLEMENTACAO_ECOSSISTEMA_REVISAO_LLM_R01.md"


@dataclass(frozen=True)
class AchadoDeFidelidade:
    """Um fato estruturado sobre um trecho, em relação a um `PerfilDeVoz`
    — nunca um julgamento (isso é `fidelidade.avaliar()`, Camada B).

    `tipo` é sempre um dos oito `DesvioBloqueante` já existentes [P07] —
    o schema não permite categoria nova (§1.4: "não pode redefinir o que
    constitui... sem nova decisão explícita"). `observado=False` é
    resultado tão legítimo quanto `True`: o achado registra que o sinal
    foi verificado e não encontrado, não apenas omite o tipo."""

    tipo: DesvioBloqueante
    observado: bool
    evidencia: str
    confianca: Confidence
    notas: str | None = None

    def __post_init__(self) -> None:
        if self.observado and not self.evidencia.strip():
            raise ErroDePerfilDeVoz(
                "P07-deteccao",
                "observado=True exige evidencia não vazia — nunca reduzir a análise a um "
                "booleano sem justificativa [§1.3]",
                detalhe=f"tipo={self.tipo.value}",
            )


def desvios_observados(achados: list[AchadoDeFidelidade]) -> list[DesvioBloqueante]:
    """Extrai os tipos com `observado=True`, na ordem em que aparecem —
    é exatamente o `desvios_encontrados` que `fidelidade.avaliar()` (ou
    `fidelidade.avaliar_a_partir_do_perfil()`) espera receber. Função
    pequena, mas isolada para que nenhum chamador repita o filtro."""
    return [a.tipo for a in achados if a.observado]

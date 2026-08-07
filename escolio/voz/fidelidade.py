"""Avaliação de fidelidade autoral — fonte:
06_PROTOCOLO_DE_AVALIACAO_DE_FIDELIDADE_AUTORAL_P07_R01.txt.

"O avaliador não reescreve" [arquivo 06, linha 4]: este módulo produz um
`AvaliacaoDeFidelidade` (um julgamento sobre um texto candidato), nunca um
texto revisado. Nenhuma função aqui aceita ou devolve o texto corrigido.
"""

from dataclasses import dataclass, field

from escolio.voz.erros import ErroDePerfilDeVoz
from escolio.voz.vocabulario import DesvioBloqueante, ResultadoDeFidelidade

ARQUIVO_PROTOCOLO = "06_PROTOCOLO_DE_AVALIACAO_DE_FIDELIDADE_AUTORAL_P07_R01.txt"

# Qualquer desvio bloqueante presente força RESULTADOS=BLOQUEAR — arquivo
# 06: a lista de DESVIOS BLOQUEANTES não admite gradação; a fonte não
# define um desvio bloqueante que resulte em algo diferente de BLOQUEAR.
_DESVIOS_QUE_FORCAM_BLOQUEIO: frozenset[DesvioBloqueante] = frozenset(DesvioBloqueante)


@dataclass
class AvaliacaoDeFidelidade:
    """Resultado de uma avaliação — não um texto, um julgamento sobre um
    texto candidato em relação a um `PerfilDeVoz`."""

    resultado: ResultadoDeFidelidade
    desvios_encontrados: list[DesvioBloqueante] = field(default_factory=list)
    justificativa: str = ""
    abstention_reason: str | None = None

    def __post_init__(self) -> None:
        if not self.justificativa and self.resultado != ResultadoDeFidelidade.ABSTER_SE:
            raise ErroDePerfilDeVoz(
                "P07-fidelidade", "justificativa é obrigatória para todo resultado exceto ABSTER_SE"
            )
        if self.resultado == ResultadoDeFidelidade.ABSTER_SE and not self.abstention_reason:
            raise ErroDePerfilDeVoz(
                "P07-fidelidade", "resultado=ABSTER_SE exige abstention_reason preenchido"
            )
        if self.desvios_encontrados and self.resultado != ResultadoDeFidelidade.BLOQUEAR:
            raise ErroDePerfilDeVoz(
                "P07-fidelidade-desvios-bloqueantes",
                "presença de desvio bloqueante exige resultado=BLOQUEAR",
                detalhe=f"resultado={self.resultado.value} desvios={[d.value for d in self.desvios_encontrados]}",
            )


def avaliar(
    desvios_encontrados: list[DesvioBloqueante],
    amostra_unica: bool,
    amostras_conflitantes: bool,
    proveniencia_ausente: bool,
    autorizacao_ausente: bool,
    perfil_declarado_sem_amostras: bool,
    exigencia_institucional_em_conflito: bool,
    justificativa: str = "",
) -> AvaliacaoDeFidelidade:
    """Aplica a árvore de decisão do arquivo 06/07 sobre condições já
    apuradas por quem chama — este módulo não inspeciona texto, apenas
    aplica a regra sobre fatos já constatados (mesma divisão de
    responsabilidade que escolio/intervencao/gate.py mantém para a causa
    do bloqueio).

    Ordem de verificação, do arquivo 07 (ABSTENCAO): "falta de
    autorização, proveniência, amostras, resolução de conflito ou gate" —
    qualquer um destes força ABSTER_SE antes de qualquer outro resultado.
    """
    if autorizacao_ausente:
        return AvaliacaoDeFidelidade(
            ResultadoDeFidelidade.ABSTER_SE, abstention_reason="falta de autorização"
        )
    if proveniencia_ausente:
        return AvaliacaoDeFidelidade(
            ResultadoDeFidelidade.ABSTER_SE, abstention_reason="falta de proveniência"
        )
    if amostra_unica:
        return AvaliacaoDeFidelidade(
            ResultadoDeFidelidade.ABSTER_SE, abstention_reason="amostra única insuficiente para voz completa"
        )
    if amostras_conflitantes:
        return AvaliacaoDeFidelidade(
            ResultadoDeFidelidade.ABSTER_SE, abstention_reason="amostras conflitantes sem resolução"
        )

    if desvios_encontrados:
        return AvaliacaoDeFidelidade(
            ResultadoDeFidelidade.BLOQUEAR,
            desvios_encontrados=list(desvios_encontrados),
            justificativa=justificativa or "desvio bloqueante identificado",
        )

    if perfil_declarado_sem_amostras:
        return AvaliacaoDeFidelidade(
            ResultadoDeFidelidade.CONFORME_COM_RESSALVAS,
            justificativa=justificativa or "perfil declarado sem amostras de calibração",
        )

    if exigencia_institucional_em_conflito:
        return AvaliacaoDeFidelidade(
            ResultadoDeFidelidade.CORRIGIR_ANTES_DE_AVANCAR,
            justificativa=justificativa or "exigência institucional em conflito com preferência autoral",
        )

    return AvaliacaoDeFidelidade(
        ResultadoDeFidelidade.CONFORME, justificativa=justificativa or "conforme ao perfil de voz vigente"
    )

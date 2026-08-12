"""Avaliação de fidelidade autoral — fonte:
06_PROTOCOLO_DE_AVALIACAO_DE_FIDELIDADE_AUTORAL_P07_R01.txt.

"O avaliador não reescreve" [arquivo 06, linha 4]: este módulo produz um
`AvaliacaoDeFidelidade` (um julgamento sobre um texto candidato), nunca um
texto revisado. Nenhuma função aqui aceita ou devolve o texto corrigido.
"""

from dataclasses import dataclass, field

from escolio.voz.deteccao import AchadoDeFidelidade, desvios_observados
from escolio.voz.erros import ErroDePerfilDeVoz
from escolio.voz.perfil import PerfilDeVoz
from escolio.voz.vocabulario import DesvioBloqueante, ResultadoDeFidelidade, TipoDePerfil

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


_TIPOS_QUE_EXIGEM_DECLARACAO = (
    TipoDePerfil.PERFIL_AUTORAL_DECLARADO_PELO_USUARIO,
    TipoDePerfil.PERFIL_HIBRIDO_DECLARACAO_MAIS_AMOSTRAS,
)
_TIPOS_QUE_EXIGEM_AMOSTRAS = (
    TipoDePerfil.PERFIL_AUTORAL_DERIVADO_DE_AMOSTRAS,
    TipoDePerfil.PERFIL_HIBRIDO_DECLARACAO_MAIS_AMOSTRAS,
)


def avaliar_a_partir_do_perfil(
    perfil: PerfilDeVoz,
    achados: list[AchadoDeFidelidade],
    *,
    amostras_conflitantes: bool = False,
    exigencia_institucional_em_conflito: bool = False,
    justificativa: str = "",
) -> AvaliacaoDeFidelidade:
    """Ponte entre a Camada A (`escolio.voz.deteccao`) e `avaliar()`
    (Camada B, inalterada — §1.1: "a camada B não deve ser alterada para
    simular a inexistência da camada A") [`INSTRUCOES_COMPLEMENTARES_
    IMPLEMENTACAO_ECOSSISTEMA_REVISAO_LLM_R01.md §1.2`, fluxo recomendado].

    Deriva de `perfil` os fatos que sua própria construção já garante —
    `PerfilDeVoz.__post_init__` (`escolio/voz/perfil.py`) já rejeita um
    perfil declarado sem `authorization` ou um perfil derivado sem
    `evidence`/`provenance` suficientes; um `PerfilDeVoz` que existe já
    não pode estar nesses dois estados, então `autorizacao_ausente` e
    `proveniencia_ausente` são derivados, nunca duplicados ou chutados.
    `amostra_unica` e `perfil_declarado_sem_amostras` são lidos
    diretamente de `perfil.evidence`/`perfil.profile_type`.

    `amostras_conflitantes` e `exigencia_institucional_em_conflito` não
    são deriváveis de `PerfilDeVoz` isoladamente (a primeira exige
    comparar amostras entre si; a segunda depende de contexto
    institucional externo ao perfil) — por isso continuam parâmetros
    explícitos, nunca assumidos como `False` por conveniência."""
    autorizacao_ausente = (
        perfil.profile_type in _TIPOS_QUE_EXIGEM_DECLARACAO and not perfil.authorization
    )
    proveniencia_ausente = (
        perfil.profile_type in _TIPOS_QUE_EXIGEM_AMOSTRAS and not perfil.provenance
    )
    perfil_declarado_sem_amostras = (
        perfil.profile_type == TipoDePerfil.PERFIL_AUTORAL_DECLARADO_PELO_USUARIO
        and len(perfil.evidence) == 0
    )
    return avaliar(
        desvios_encontrados=desvios_observados(achados),
        amostra_unica=len(perfil.evidence) == 1,
        amostras_conflitantes=amostras_conflitantes,
        proveniencia_ausente=proveniencia_ausente,
        autorizacao_ausente=autorizacao_ausente,
        perfil_declarado_sem_amostras=perfil_declarado_sem_amostras,
        exigencia_institucional_em_conflito=exigencia_institucional_em_conflito,
        justificativa=justificativa,
    )

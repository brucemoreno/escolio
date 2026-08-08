"""Registro externo de análise de segurança — DTA-01, DTA-02, DTA-03.

Fonte: docs/spec/operacional-P08.md §3.2-3.3.

DTA-01: o estado "ainda não analisado" mora fora do `InputItem`. PR-03
[P08 §8] exige que, "na ausência de classificação, o material deve ser
tratado provisoriamente como RESTRITO" — mas `escolio.contrato.entrada.Security`
tem três booleanos com default `False` e nenhuma forma de distinguir
"analisado e limpo" de "nunca analisado" [P09 §6 não tem onde expressar a
diferença; LAC-SEG-001]. Este módulo não altera `Security` (não tocar em
código existente) — mantém, por `input_id`, se a análise rodou, com que
versão de padrões e com que evidência.

DTA-02: os três booleanos de segurança são monotônicos (latching) — uma
vez `true`, nenhum passo posterior os baixa. Só (c) REVISAO_HUMANA pode
reverter, com evidência material [P08 §4.2 item 5]. Alternativa
descartada: recomputar a cada etapa e deixar o valor mais recente
prevalecer — permitiria que uma passada posterior mais grosseira apagasse
achado de uma passada anterior mais fina, o que é redução de proteção sem
evidência material nem autoridade válida.

DTA-03: cada booleano é setado só pela sua própria evidência; nenhum é
derivado de outro por implicação automática. Detectar autoelevação seta
`injection_suspected`; não seta `adversarial_content` por implicação — a
relação fica registrada em `Achado.relacionados_a` para que um humano a
veja, mas não propaga sozinha [RD-02: nenhuma classificação elevada por
inferência].
"""

from dataclasses import dataclass, field

from escolio.seguranca.erros import ErroDeSeguranca


@dataclass(frozen=True)
class Achado:
    """Um achado de segurança sobre uma unidade — sempre com evidência
    localizada [CLAUDE.md: "Todo achado carrega evidência localizada"] e
    camada de origem (DTA-12)."""

    unit_id: str
    campo: str  # "adversarial_content" | "injection_suspected" | "exfiltration_risk"
    trecho: str
    camada: str  # CamadaDeDecisao.value
    regra: str  # ex.: "PI-03"
    relacionados_a: tuple[str, ...] = ()

    def __post_init__(self):
        if self.campo not in ("adversarial_content", "injection_suspected", "exfiltration_risk"):
            raise ErroDeSeguranca(
                "RD-04",
                "Achado.campo deve ser um dos três booleanos de InputItem.security [P09 §6]",
                arquivo_origem="P09_SCHEMAS_CONTRATOS_CORRIGIDO_R04.md",
                detalhe=f"recebido: {self.campo!r}",
            )
        if not self.unit_id:
            raise ErroDeSeguranca("PI-08", "Achado sem unit_id — evidência deve ser localizada")
        if not self.trecho:
            raise ErroDeSeguranca("PI-08", "Achado sem trecho de evidência")


@dataclass
class RegistroDeAnalise:
    """Registro externo por `input_id` — DTA-01. Não é `InputItem.security`
    e não o substitui; é o lugar onde "ainda não analisado" é
    representável, o que o schema do P09 não tem onde expressar."""

    input_id: str
    versao_de_padroes: str
    analisado: bool = False
    achados: list[Achado] = field(default_factory=list)

    def registra_achado(self, achado: Achado) -> None:
        """DTA-02: adicionar um achado nunca remove os anteriores — a
        lista só cresce. `analisado=True` também é monotônico: uma vez
        marcado, este método não o reverte."""
        self.achados.append(achado)
        self.analisado = True

    def valor_de(self, campo: str) -> bool:
        """Deriva o booleano de `InputItem.security.<campo>` a partir dos
        achados registrados para aquele campo — nunca de achados de outro
        campo (DTA-03: nenhum booleano é derivado de outro por
        implicação)."""
        return any(a.campo == campo for a in self.achados)

    def reduz_protecao(self, campo: str, motivo: str, autoridade_basis: str) -> None:
        """(c) REVISAO_HUMANA — RH-02 [P08 §4.2 item 5]: reduzir proteção
        exige evidência material E autoridade válida. Este método é o
        único caminho de código que remove achados de `campo`; chamá-lo
        sem os dois argumentos preenchidos é erro de uso, não caminho
        alternativo — não há default que dispense a autoridade."""
        if not motivo or not autoridade_basis:
            raise ErroDeSeguranca(
                "RH-02",
                "reduzir proteção exige evidência material e autoridade válida",
                arquivo_origem="operacional-P08.md",
                detalhe="[P08 §4.2] item 5 — motivo e autoridade_basis são obrigatórios, sem default",
            )
        self.achados = [a for a in self.achados if a.campo != campo]

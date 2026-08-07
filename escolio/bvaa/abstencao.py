"""Protocolo de recomendação e abstenção bibliográfica — fonte:
07_PROTOCOLO_DE_RECOMENDACAO_E_ABSTENCAO_BIBLIOGRAFICA_P04_R01.txt.

Cadeia declarada [arquivo 07]:
CONHECIMENTO_NOMINAL -> IDENTIFICACAO -> LOCALIZACAO -> ACESSO -> LEITURA
-> VALIDACAO -> RECOMENDACAO

"Nenhuma etapa posterior é inferida automaticamente a partir da
anterior" [arquivo 07] — esta cadeia é documentação da ordem declarada,
não uma segunda máquina de estados: as etapas não têm vocabulário de
enum próprio na fonte (são rótulos de fase, não estados com evidência
mínima/autoridade/ação como os 17 de `escolio.bvaa.vocabulario`). Por
isso `CADEIA_DE_RECOMENDACAO` abaixo é uma tupla de strings, não um enum
— inventar um enum aqui adicionaria estrutura que a fonte não define.

Gatilhos de ABSTENCAO_BIBLIOGRAFICA consolidados das duas fontes que a
declaram (arquivo 02 §11 e arquivo 07) — união das duas listas, sem
duplicar motivo redundante entre elas.
"""

from dataclasses import dataclass
from enum import Enum

from escolio.bvaa.vocabulario import EstadoBibliografico

ARQUIVO_PROTOCOLO_RECOMENDACAO = "07_PROTOCOLO_DE_RECOMENDACAO_E_ABSTENCAO_BIBLIOGRAFICA_P04_R01.txt"
ARQUIVO_PROTOCOLO_BVAA = "02_PROTOCOLO_BVAA_UNIVERSAL_P04_R01.md"

CADEIA_DE_RECOMENDACAO: tuple[str, ...] = (
    "CONHECIMENTO_NOMINAL",
    "IDENTIFICACAO",
    "LOCALIZACAO",
    "ACESSO",
    "LEITURA",
    "VALIDACAO",
    "RECOMENDACAO",
)


class GatilhoDeAbstencao(str, Enum):
    """União dos gatilhos declarados em [02_PROTOCOLO_BVAA_UNIVERSAL_P04_R01.md
    §11] e [07_PROTOCOLO_DE_RECOMENDACAO_E_ABSTENCAO_BIBLIOGRAFICA_P04_R01.txt].

    Nomeados a partir do texto literal de cada gatilho; onde as duas
    fontes descrevem a mesma condição com palavras diferentes ("obra ou
    edição não podem ser identificadas" vs. "obra não identificada" /
    "edição incerta"), um único membro cobre ambas — ver docstring de
    cada membro para a citação exata.
    """

    OBRA_OU_EDICAO_NAO_IDENTIFICADA = "OBRA_OU_EDICAO_NAO_IDENTIFICADA"
    """[§11 BVAA] "obra ou edição não podem ser identificadas"; [§ recomendação] "obra não identificada"; "edição incerta"."""

    ACESSO_NAO_COMPROVADO = "ACESSO_NAO_COMPROVADO"
    """[§11 BVAA] "acesso não foi comprovado"; [protocolo de recomendação] "acesso não comprovado"."""

    LEITURA_NAO_COMPROVADA = "LEITURA_NAO_COMPROVADA"
    """[§11 BVAA] "leitura alegada não pode ser demonstrada"; [protocolo de recomendação] "leitura não comprovada"."""

    PAGINA_CITACAO_OU_METADADO_DIVERGENTE = "PAGINA_CITACAO_OU_METADADO_DIVERGENTE"
    """[§11 BVAA] "página, citação ou metadado divergem"; [protocolo de recomendação] "página/citação não confirmada"; "metadado conflitante"."""

    FONTE_SECUNDARIA_COMO_PROVA_DE_LEITURA_PRIMARIA = "FONTE_SECUNDARIA_COMO_PROVA_DE_LEITURA_PRIMARIA"
    """[§11 BVAA] "fonte secundária é usada como prova de leitura primária"; [protocolo de recomendação] "fonte secundária apresentada como leitura primária"."""

    EVIDENCIA_NAO_SUSTENTA_AFIRMACAO = "EVIDENCIA_NAO_SUSTENTA_AFIRMACAO"
    """[§11 BVAA] "evidência não sustenta a afirmação"; [protocolo de recomendação] "evidência incompatível com a afirmação"."""

    COMANDO_EXIGE_INVENCAO = "COMANDO_EXIGE_INVENCAO"
    """[§11 BVAA] "o comando exige invenção"; [protocolo de recomendação] "comando para inventar dados"; é o gatilho por trás de T18."""


@dataclass(frozen=True)
class SaidaDeAbstencao:
    """[07_PROTOCOLO... "SAIDA_DA_ABSTENCAO"] — "Declarar o que não pode
    ser comprovado, registrar a evidência ausente e indicar uma única
    ação documental necessária." Os três campos são obrigatórios na
    fonte; nenhum é opcional."""

    o_que_nao_pode_ser_comprovado: str
    evidencia_ausente: str
    acao_documental_necessaria: str
    gatilho: GatilhoDeAbstencao


def exige_abstencao(gatilho: GatilhoDeAbstencao) -> bool:
    """Todo gatilho listado em GatilhoDeAbstencao exige abstenção —
    não há gatilho opcional ou de mera sinalização na fonte. Função
    trivial mantida para nomear a regra em um só lugar, mesmo padrão de
    `escolio.intervencao.gate` para regras estruturais simples."""
    return isinstance(gatilho, GatilhoDeAbstencao)


def estado_apos_abstencao() -> EstadoBibliografico:
    """O único estado de destino de qualquer abstenção é
    ABSTENCAO_BIBLIOGRAFICA — não há abstenção "parcial" para outro
    estado [arquivo 03: ABSTENCAO_BIBLIOGRAFICA é estado terminal de
    interrupção]."""
    return EstadoBibliografico.ABSTENCAO_BIBLIOGRAFICA

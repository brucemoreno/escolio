"""Hierarquia de precedência da voz autoral — fonte:
01_CONTRATO_UNIVERSAL_DE_VOZ_AUTORAL_P07_R01.md (§Hierarquia);
07_PROTOCOLO_DE_CONFLITOS_ABSTENCAO_E_REVERSAO_P07_R01.txt (PRECEDENCIA).

Os dois arquivos declaram a mesma ordem com granularidade ligeiramente
diferente:
- contrato (01): "Integridade documental > sentido > densidade e nuance >
  perfil temático e exigência institucional > voz autoral > fluidez" — 6
  elos;
- conflitos (07): "integridade; sentido; densidade/nuance; exigência
  institucional/perfil temático; voz; fluidez" — mesma ordem, mesmos 6
  elos, nomes abreviados.

Nenhuma fusão inventada: os dois arquivos convergem exatamente na mesma
sequência de 6 elos, então a cadeia abaixo é uma única lista, não uma
reconciliação de duas listas divergentes (diferente de CON-P05-001, onde
as fontes realmente divergem).
"""

from enum import Enum


class EloDeHierarquia(str, Enum):
    """6 elos, na ordem declarada — nenhum reordenado ou fundido."""

    INTEGRIDADE_DOCUMENTAL = "INTEGRIDADE_DOCUMENTAL"
    SENTIDO = "SENTIDO"
    DENSIDADE_E_NUANCE = "DENSIDADE_E_NUANCE"
    PERFIL_TEMATICO_E_EXIGENCIA_INSTITUCIONAL = "PERFIL_TEMATICO_E_EXIGENCIA_INSTITUCIONAL"
    VOZ_AUTORAL = "VOZ_AUTORAL"
    FLUIDEZ = "FLUIDEZ"


CADEIA_DE_PRECEDENCIA: tuple[EloDeHierarquia, ...] = (
    EloDeHierarquia.INTEGRIDADE_DOCUMENTAL,
    EloDeHierarquia.SENTIDO,
    EloDeHierarquia.DENSIDADE_E_NUANCE,
    EloDeHierarquia.PERFIL_TEMATICO_E_EXIGENCIA_INSTITUCIONAL,
    EloDeHierarquia.VOZ_AUTORAL,
    EloDeHierarquia.FLUIDEZ,
)

_POSICAO = {elo: indice for indice, elo in enumerate(CADEIA_DE_PRECEDENCIA)}


class TipoDeConflito(str, Enum):
    """5 tipos de conflito — fonte: arquivo 07, linha CONFLITOS."""

    DECLARACAO_VERSUS_AMOSTRAS = "DECLARACAO_VERSUS_AMOSTRAS"
    AMOSTRAS_ENTRE_SI = "AMOSTRAS_ENTRE_SI"
    PREFERENCIA_VERSUS_EXIGENCIA_INSTITUCIONAL = "PREFERENCIA_VERSUS_EXIGENCIA_INSTITUCIONAL"
    PERFIL_GLOBAL_VERSUS_LOCAL = "PERFIL_GLOBAL_VERSUS_LOCAL"
    VOZ_VERSUS_INTEGRIDADE_SENTIDO_DENSIDADE_TEMA = "VOZ_VERSUS_INTEGRIDADE_SENTIDO_DENSIDADE_TEMA"


def posicao(elo: EloDeHierarquia) -> int:
    """Posição ordinal na cadeia — menor posição prevalece (§Hierarquia)."""
    return _POSICAO[elo]


def prevalece(a: EloDeHierarquia, b: EloDeHierarquia) -> EloDeHierarquia:
    """Dado um conflito entre dois elos da hierarquia, retorna o elo que
    prevalece — o de menor posição ordinal (mais próximo de
    INTEGRIDADE_DOCUMENTAL). Não decide o conflito material em si (isso é
    responsabilidade de quem chama, com o achado concreto); apenas resolve
    qual princípio abstrato tem precedência quando ambos se aplicam."""
    return a if posicao(a) <= posicao(b) else b

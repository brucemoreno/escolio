"""Cadeia de níveis de intervenção — fonte: 01_TAXONOMIA_UNIVERSAL_DE_INTERVENCAO_P06_R01.md
§2, §7, §8; 02_DICIONARIO_DE_NIVEIS_DE_INTERVENCAO_P06_R01.csv;
04_MATRIZ_DE_ESCALONAMENTO_E_REGRESSAO_P06_R01.csv.

Princípio [§1]: nenhum nível superior pode ser inferido de nível inferior.
Escalonamento [§7] ocorre somente por autorização explícita do nível
imediatamente superior ou do nível específico pretendido — não há herança
automática de permissão.
"""

from enum import Enum


class NivelIntervencao(str, Enum):
    """Cadeia INT-01…INT-15, na ordem declarada em §2 e no dicionário §02."""

    OBSERVACAO = "INT-01"
    DIAGNOSTICO = "INT-02"
    SINALIZACAO = "INT-03"
    RECOMENDACAO = "INT-04"
    PROPOSTA = "INT-05"
    SIMULACAO = "INT-06"
    EDICAO_LOCAL = "INT-07"
    REESCRITA = "INT-08"
    REORGANIZACAO = "INT-09"
    FUSAO = "INT-10"
    CORTE = "INT-11"
    SUBSTITUICAO = "INT-12"
    VALIDACAO = "INT-13"
    HOMOLOGACAO = "INT-14"
    ABSTENCAO = "INT-15"


# Ordem da cadeia [§2] — usada para comparação de precedência (nenhum nível
# superior se infere de nível inferior) e para a regressão segura [§8].
# ABSTENCAO fica fora da cadeia ordinal: não é "superior" a HOMOLOGACAO — é
# uma saída paralela, obrigatória quando nenhum nível operativo permanece
# válido [§8; 05_PROTOCOLO_DE_AUTORIZACAO_E_ABSTENCAO_P06_R01.txt].
_CADEIA_OPERATIVA = (
    NivelIntervencao.OBSERVACAO,
    NivelIntervencao.DIAGNOSTICO,
    NivelIntervencao.SINALIZACAO,
    NivelIntervencao.RECOMENDACAO,
    NivelIntervencao.PROPOSTA,
    NivelIntervencao.SIMULACAO,
    NivelIntervencao.EDICAO_LOCAL,
    NivelIntervencao.REESCRITA,
    NivelIntervencao.REORGANIZACAO,
    NivelIntervencao.FUSAO,
    NivelIntervencao.CORTE,
    NivelIntervencao.SUBSTITUICAO,
    NivelIntervencao.VALIDACAO,
    NivelIntervencao.HOMOLOGACAO,
)

_POSICAO = {nivel: indice for indice, nivel in enumerate(_CADEIA_OPERATIVA)}

# Transições de escalonamento explicitamente listadas na matriz §04 —
# somente estas existem; QUALQUER_EXECUCAO->VALIDACAO e
# QUALQUER_NIVEL->ABSTENCAO são tratadas separadamente por não serem uma
# origem pontual da cadeia ordinal.
_ESCALONAMENTOS_LISTADOS = {
    NivelIntervencao.OBSERVACAO: NivelIntervencao.DIAGNOSTICO,
    NivelIntervencao.DIAGNOSTICO: NivelIntervencao.SINALIZACAO,
    NivelIntervencao.SINALIZACAO: NivelIntervencao.RECOMENDACAO,
    NivelIntervencao.RECOMENDACAO: NivelIntervencao.PROPOSTA,
    NivelIntervencao.PROPOSTA: NivelIntervencao.SIMULACAO,
    NivelIntervencao.SIMULACAO: NivelIntervencao.EDICAO_LOCAL,
    NivelIntervencao.EDICAO_LOCAL: NivelIntervencao.REESCRITA,
    NivelIntervencao.REESCRITA: NivelIntervencao.REORGANIZACAO,
    # §04: REORGANIZACAO escalona para FUSAO ou para CORTE — dois destinos
    # possíveis da mesma origem, por isso fora do dict 1:1 acima.
}

# §04: origens compostas (REORGANIZACAO -> FUSAO | CORTE) preservadas à
# parte para não forçar um único destino por origem.
_ESCALONAMENTOS_DE_REORGANIZACAO = (NivelIntervencao.FUSAO, NivelIntervencao.CORTE)


def posicao(nivel: NivelIntervencao) -> int:
    """Posição ordinal na cadeia operativa. ABSTENCAO não tem posição —
    chamar com ABSTENCAO é erro de uso, não uma pergunta válida sobre
    precedência [§8]."""
    return _POSICAO[nivel]


def excede(candidato: NivelIntervencao, teto: NivelIntervencao) -> bool:
    """True se `candidato` está acima de `teto` na cadeia [§1, §7].

    ABSTENCAO não tem posição ordinal — é comparada por identidade: excede
    qualquer nível operativo (nunca é um `applied_level`/`candidato` válido
    dentro de um teto operativo) e não excede a si mesma.
    """
    if candidato == NivelIntervencao.ABSTENCAO:
        return teto != NivelIntervencao.ABSTENCAO
    if teto == NivelIntervencao.ABSTENCAO:
        return False
    return posicao(candidato) > posicao(teto)


def escalonamento_permitido(origem: NivelIntervencao, destino: NivelIntervencao) -> bool:
    """True somente se a transição origem->destino está listada na matriz
    §04. Não há herança automática [§7]: uma transição não listada — mesmo
    que destino seja adjacente na cadeia — não está autorizada por este
    dicionário; exige autorização explícita do nível pretendido, verificada
    por quem chama, fora deste módulo."""
    if origem == NivelIntervencao.REORGANIZACAO:
        return destino in _ESCALONAMENTOS_DE_REORGANIZACAO
    if origem == NivelIntervencao.VALIDACAO:
        return destino == NivelIntervencao.HOMOLOGACAO
    return _ESCALONAMENTOS_LISTADOS.get(origem) == destino


def nivel_maximo_ainda_autorizado(
    nivel_pretendido: NivelIntervencao, niveis_autorizados: frozenset[NivelIntervencao]
) -> NivelIntervencao | None:
    """Regressão segura [§8]: quando o gate falha, regredir ao nível máximo
    ainda autorizado dentro da cadeia operativa, sem exceder
    `nivel_pretendido`. Retorna None se nenhum nível operativo permanecer
    válido — sinal para aplicar ABSTENCAO [§8; §15 do dicionário]."""
    candidatos = [
        n
        for n in niveis_autorizados
        if n != NivelIntervencao.ABSTENCAO and not excede(n, nivel_pretendido)
    ]
    if not candidatos:
        return None
    return max(candidatos, key=posicao)

"""Dicionário de dimensões de voz — fonte:
03_DICIONARIO_DE_DIMENSOES_DE_VOZ_P07_R01.csv (30 dimensões, VOZ-D01…D30).

A fonte não fornece uma `definicao` por dimensão além do rótulo genérico
"Dimensão controlada: <nome>" repetido em todas as 30 linhas do CSV — não
foi inventada uma definição mais rica que a fonte não declara. Ver
escolio/voz/LACUNAS.md.
"""

from dataclasses import dataclass
from enum import Enum

ARQUIVO_DIMENSOES = "03_DICIONARIO_DE_DIMENSOES_DE_VOZ_P07_R01.csv"


class Obrigatoriedade(str, Enum):
    OBRIGATORIA = "obrigatória"
    OPCIONAL = "opcional"


@dataclass(frozen=True)
class DefinicaoDeDimensao:
    dimension_id: str
    nome: str
    obrigatoriedade: Obrigatoriedade


class DimensaoDeVoz(str, Enum):
    """30 dimensões, na ordem exata do CSV — nenhuma renomeada, fundida ou
    reordenada."""

    VOZ_D01 = "VOZ-D01"
    VOZ_D02 = "VOZ-D02"
    VOZ_D03 = "VOZ-D03"
    VOZ_D04 = "VOZ-D04"
    VOZ_D05 = "VOZ-D05"
    VOZ_D06 = "VOZ-D06"
    VOZ_D07 = "VOZ-D07"
    VOZ_D08 = "VOZ-D08"
    VOZ_D09 = "VOZ-D09"
    VOZ_D10 = "VOZ-D10"
    VOZ_D11 = "VOZ-D11"
    VOZ_D12 = "VOZ-D12"
    VOZ_D13 = "VOZ-D13"
    VOZ_D14 = "VOZ-D14"
    VOZ_D15 = "VOZ-D15"
    VOZ_D16 = "VOZ-D16"
    VOZ_D17 = "VOZ-D17"
    VOZ_D18 = "VOZ-D18"
    VOZ_D19 = "VOZ-D19"
    VOZ_D20 = "VOZ-D20"
    VOZ_D21 = "VOZ-D21"
    VOZ_D22 = "VOZ-D22"
    VOZ_D23 = "VOZ-D23"
    VOZ_D24 = "VOZ-D24"
    VOZ_D25 = "VOZ-D25"
    VOZ_D26 = "VOZ-D26"
    VOZ_D27 = "VOZ-D27"
    VOZ_D28 = "VOZ-D28"
    VOZ_D29 = "VOZ-D29"
    VOZ_D30 = "VOZ-D30"


# Nome e obrigatoriedade, na ordem e com os valores exatos do CSV (colunas
# `nome` e `obrigatoriedade`).
DEFINICOES: dict[DimensaoDeVoz, DefinicaoDeDimensao] = {
    DimensaoDeVoz.VOZ_D01: DefinicaoDeDimensao("VOZ-D01", "identidade_e_finalidade", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D02: DefinicaoDeDimensao("VOZ-D02", "contexto_de_aplicacao", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D03: DefinicaoDeDimensao("VOZ-D03", "registro_academico", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D04: DefinicaoDeDimensao("VOZ-D04", "formalidade", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D05: DefinicaoDeDimensao("VOZ-D05", "pessoa_gramatical", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D06: DefinicaoDeDimensao("VOZ-D06", "ritmo", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D07: DefinicaoDeDimensao("VOZ-D07", "cadencia", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D08: DefinicaoDeDimensao("VOZ-D08", "extensao_variacao_periodos", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D09: DefinicaoDeDimensao("VOZ-D09", "densidade_argumentativa", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D10: DefinicaoDeDimensao("VOZ-D10", "encadeamento_logico", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D11: DefinicaoDeDimensao("VOZ-D11", "transicoes", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D12: DefinicaoDeDimensao("VOZ-D12", "postura_analitica", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D13: DefinicaoDeDimensao("VOZ-D13", "prudencia_inferencial", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D14: DefinicaoDeDimensao("VOZ-D14", "grau_de_explicitacao", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D15: DefinicaoDeDimensao("VOZ-D15", "nuance_ambiguidade", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D16: DefinicaoDeDimensao("VOZ-D16", "preferencias_lexicais", Obrigatoriedade.OPCIONAL),
    DimensaoDeVoz.VOZ_D17: DefinicaoDeDimensao("VOZ-D17", "termos_desaconselhados", Obrigatoriedade.OPCIONAL),
    DimensaoDeVoz.VOZ_D18: DefinicaoDeDimensao("VOZ-D18", "abertura_encerramento", Obrigatoriedade.OPCIONAL),
    DimensaoDeVoz.VOZ_D19: DefinicaoDeDimensao("VOZ-D19", "recursos_retoricos", Obrigatoriedade.OPCIONAL),
    DimensaoDeVoz.VOZ_D20: DefinicaoDeDimensao("VOZ-D20", "relacao_perfil_tematico", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D21: DefinicaoDeDimensao("VOZ-D21", "invariantes_autorais", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D22: DefinicaoDeDimensao("VOZ-D22", "elementos_flexiveis", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D23: DefinicaoDeDimensao("VOZ-D23", "desvios_toleraveis", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D24: DefinicaoDeDimensao("VOZ-D24", "desvios_bloqueantes", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D25: DefinicaoDeDimensao("VOZ-D25", "evidencias_calibracao", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D26: DefinicaoDeDimensao("VOZ-D26", "confianca", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D27: DefinicaoDeDimensao("VOZ-D27", "autorizacao_de_uso", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D28: DefinicaoDeDimensao("VOZ-D28", "versionamento_historico", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D29: DefinicaoDeDimensao("VOZ-D29", "reversibilidade", Obrigatoriedade.OBRIGATORIA),
    DimensaoDeVoz.VOZ_D30: DefinicaoDeDimensao("VOZ-D30", "abstencao_encerramento", Obrigatoriedade.OBRIGATORIA),
}

DIMENSOES_OBRIGATORIAS: frozenset[DimensaoDeVoz] = frozenset(
    d for d, definicao in DEFINICOES.items() if definicao.obrigatoriedade == Obrigatoriedade.OBRIGATORIA
)

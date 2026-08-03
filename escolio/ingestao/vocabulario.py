"""Vocabulário controlado do módulo de ingestão — mesmo padrão de
escolio/vocabulario.py: enums fechados, valor fora da lista rejeitado
pelo próprio Python.
"""

from enum import Enum


class TipoUnidade(str, Enum):
    SECAO = "SECAO"
    PARAGRAFO = "PARAGRAFO"
    NOTA_DE_RODAPE = "NOTA_DE_RODAPE"
    CITACAO_RECUADA = "CITACAO_RECUADA"
    CITACAO_NO_CORPO = "CITACAO_NO_CORPO"
    REFERENCIA = "REFERENCIA"
    FIGURA = "FIGURA"
    QUADRO_TABELA = "QUADRO_TABELA"


class NivelHierarquia(int, Enum):
    CAPITULO = 1
    SECAO = 2
    SUBSECAO = 3


class MotivoIndeterminado(str, Enum):
    """Por que um elemento não foi classificado com segurança — a regra do
    prompt é marcar como indeterminado, não chutar; este enum documenta a
    razão específica para o relatório de ingestão."""

    PADRAO_GRAFICO_AMBIGUO = "PADRAO_GRAFICO_AMBIGUO"
    """O mesmo padrão gráfico (ex.: negrito + margem esquerda) é usado no
    documento para mais de uma função estrutural (ex.: título de seção e
    subtítulo de lista de referências) e não há sumário para desambiguar."""

    SEM_CHAMADA_CORRESPONDENTE = "SEM_CHAMADA_CORRESPONDENTE"
    """Nota de rodapé sem chamada em sobrescrito localizável no corpo."""

    SEM_ANCORA_TEXTUAL = "SEM_ANCORA_TEXTUAL"
    """Figura/quadro sem legenda ou referência textual próxima que permita
    confirmar sua posição relativa ao texto corrente."""

    AUTOR_DATA_NAO_RECONHECIDO = "AUTOR_DATA_NAO_RECONHECIDO"
    """Trecho com formato de citação improvável de confirmar como
    autor-data ABNT sem risco de falso positivo (ex.: número de página de
    tabela, ano solto em lista de referências já processada à parte)."""

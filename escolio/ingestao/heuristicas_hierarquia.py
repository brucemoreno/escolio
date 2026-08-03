"""Heurística de detecção de título/cabeçalho estrutural (capítulo, seção,
subseção) — RG-001 e RG-002 em FORMATO.md.

Fundamento empírico (não é uma regra genérica de PDF; é o que este
documento real, data/dev/Relatorio_Final_PIBIC-..., de fato usa):

  - Body: Times New Roman 12pt, não-negrito.
  - Títulos de seção no corpo do texto: Times New Roman 12pt, EM NEGRITO,
    linha isolada (não compartilha `top` com texto não-negrito), margem
    esquerda igual à margem do corpo (x0≈56.6), texto curto.
  - Sem numeração (nenhuma seção do corpo usa "1.", "1.1" etc. — apenas o
    formulário de capa da página 1 numera itens, que não são seções).
  - Sem versalete/caixa-alta sistemático — os títulos usam capitalização
    de frase normal ("Introdução", "Análise das práticas agridoces").
  - O documento NÃO tem sumário/índice — não há como validar a lista de
    títulos detectados contra uma lista de referência do próprio
    documento (ver LACUNAS.md, RG-002).

RG-001 (falso positivo corrigido): uma linha com ALGUMA palavra em
negrito (ênfase dentro do parágrafo) não é um título. Só conta linha
100% em negrito — ver `layout.Linha.totalmente_negrito`. Constatado no
próprio documento: p.26 tem a palavra "agridoce" em negrito no meio de
uma frase de corpo; a versão inicial desta heurística (checando "algum
caractere negrito na linha") classificava a linha inteira como título.
Corrigido antes de qualquer teste ser escrito.

RG-002 (ambiguidade estrutural não resolvida): "Fonte Primária" (página
33) usa o MESMO padrão gráfico exato de um título de seção (negrito,
12pt, x0=56.6, linha curta e isolada), mas semanticamente é uma
subdivisão da lista de referências (fontes primárias vs. bibliografia),
não um capítulo do corpo do texto. Sem sumário para desambiguar por
correspondência de rótulo, não há como decidir com segurança se pertence
ao mesmo nível hierárquico que "Introdução" ou "Metodologia", ou a um
nível abaixo. Esta implementação NÃO adivinha: marca como título
detectado (não funde ao texto corrido) mas com nível=None e
indeterminado=True quando a linha ocorre após o início da seção
"Referências Bibliográficas" — porque within essa região o rótulo de um
título não tem o mesmo peso estrutural que no corpo.
"""

from escolio.ingestao.layout import Linha
from escolio.ingestao.vocabulario import MotivoIndeterminado

TAMANHO_TITULO_MIN = 11.5
TAMANHO_TITULO_MAX = 12.5
X0_MARGEM_CORPO_MAX = 60.0
TAMANHO_MAXIMO_TEXTO_TITULO = 80

# Rótulo da seção a partir da qual um "título" no mesmo padrão gráfico do
# corpo passa a ser tratado como subdivisão da lista de referências, não
# como capítulo — constatado empiricamente (ver RG-002 acima).
ROTULO_INICIO_REFERENCIAS = "referências bibliográficas"


def linha_e_candidata_a_titulo(linha: Linha) -> bool:
    """RG-001: linha inteira em negrito, tamanho de corpo (não maior —
    este documento não usa tamanho de fonte para hierarquia, apenas
    negrito), margem esquerda do corpo, texto curto."""
    if not linha.totalmente_negrito:
        return False
    if not linha.tamanhos or not all(
        TAMANHO_TITULO_MIN <= t <= TAMANHO_TITULO_MAX for t in linha.tamanhos
    ):
        return False
    if linha.x0 > X0_MARGEM_CORPO_MAX:
        return False
    texto = linha.texto.strip()
    if not texto or len(texto) > TAMANHO_MAXIMO_TEXTO_TITULO:
        return False
    # Uma linha de tabela/quadro (ex.: "Categoria Ingrediente Função
    # Principal Origem") também é negrito+12pt+margem, mas normalmente
    # múltiplas colunas separadas por espaçamento largo; não filtramos
    # por esse sinal aqui porque não é confiável sem as posições x de
    # cada célula (fora do escopo desta função) — ver RG-003 em
    # heuristicas_figuras.py, que trata quadros/tabelas separadamente e
    # pode reclassificar uma linha já candidata a título.
    return True


def apos_inicio_das_referencias(titulos_texto_ate_agora: list[str]) -> bool:
    """True se algum título já emitido é o cabeçalho da lista de
    referências — usado para decidir se um novo título no mesmo padrão
    gráfico está dentro da zona ambígua (RG-002)."""
    return any(
        t.strip().lower() == ROTULO_INICIO_REFERENCIAS for t in titulos_texto_ate_agora
    )


def classificar_titulo(texto: str, ja_entrou_em_referencias: bool) -> tuple[bool, MotivoIndeterminado | None]:
    """Retorna (indeterminado, motivo). Regra RG-002: dentro da zona de
    referências, o padrão gráfico de título deixa de indicar
    inequivocamente um capítulo — o nível não pode ser inferido sem
    sumário. Fora dessa zona, o título é aceito como nível 1 (capítulo)
    por ora: este documento não tem subníveis negrito+12pt+margem
    distintos de nível 1 (nenhuma segunda hierarquia de título foi
    encontrada nos dados reais — ver LACUNAS.md)."""
    if ja_entrou_em_referencias:
        return True, MotivoIndeterminado.PADRAO_GRAFICO_AMBIGUO
    return False, None

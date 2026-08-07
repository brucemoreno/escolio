# Custos, janelas e mecânica de cache

**Data de verificação: 2026-06-24** (cache da skill `claude-api`; a tabela de preços da própria
skill traz essa data). Reverificar antes de qualquer decisão de orçamento — nunca estimar preço
de memória.

## Preços por 1M de tokens

| Modelo | ID | Contexto | Saída máx. | Input | Output |
|---|---|---|---|---|---|
| Claude Opus 5 | `claude-opus-5` | 1M | 128K | $5,00 | $25,00 |
| Claude Sonnet 5 | `claude-sonnet-5` | 1M | 128K | $3,00 | $15,00 |
| Claude Haiku 4.5 | `claude-haiku-4-5` | **200K** | 64K | $1,00 | $5,00 |

Sonnet 5 tem preço introdutório de $2,00 / $10,00 **até 2026-08-31**. Depois volta a $3/$15 —
qualquer orçamento feito hoje precisa considerar a data.

**Output custa 5× o input em todos os três modelos.** Numa arquitetura de fan-out por unidade, o
output domina o custo total.

## Cache

- Escrita: **1,25×** com TTL de 5 min · **2×** com TTL de 1 h.
- Leitura: **0,1×**.
- Ponto de equilíbrio: TTL 5 min paga-se em 2 requisições; TTL 1 h, em 3.
- **TTL máximo é 1 h.**

### Mínimo cacheável — não é monotônico

| Modelo | Mínimo |
|---|---|
| Opus 5 | 512 tokens |
| Sonnet 5 | 1024 tokens |
| Haiku 4.5 | **4096 tokens** |

Prefixo abaixo do mínimo **não cacheia e não emite erro** — só devolve
`cache_creation_input_tokens: 0`. Um prompt curto por unidade no Haiku falha silenciosamente.

### Cache é prefix match

Qualquer byte alterado no prefixo invalida tudo depois dele. Ordem de renderização:
`tools` → `system` → `messages`. Invalidadores silenciosos a evitar no prefixo: timestamp, UUID,
`json.dumps` sem `sort_keys`, ID de sessão interpolado no system prompt, conjunto de ferramentas
variável por usuário.

Trocar de modelo invalida o cache: caches são por modelo.

## Batch

- Desconto de **50%** sobre todo uso de tokens.
- Maioria termina em 1 h; **máximo 24 h**.
- `fallbacks` é **rejeitado** na Batches API — recusa em batch não tem rede de segurança.

### Batch × cache é escolha, não acúmulo

Sendo `p` o prefixo compartilhado e `u` o conteúdo único por chamada:

- batch: `0,5 · (p + u)`
- síncrono com cache: `0,1 · p + u`

**Batch vence quando `p < 1,25 u`.** Agrupar mais unidades por chamada aumenta `u` e empurra a
favor do batch.

Conflito a decidir por etapa: um batch de milhares de requisições pode durar 24 h, o TTL máximo
é 1 h, e o prefixo expira no meio da execução. Medir `cache_read_input_tokens`, nunca presumir.

## Thinking e effort

- `budget_tokens` foi **removido** no Opus 5 e no Sonnet 5 — enviar retorna 400. Usar
  `output_config.effort`.
- No **Opus 5 o thinking está ligado por padrão**: omitir `thinking` roda adaptive.
- `thinking: {type: "disabled"}` no Opus 5 só é aceito com effort ≤ `high`; com `xhigh` ou `max`
  retorna 400.
- `max_tokens` limita thinking **mais** resposta. Rota que nunca setou `thinking` pode truncar.
- Níveis de effort: `low | medium | high | xhigh | max`. **Default é `high`** — etapa que não
  declara effort roda no caro.

## Documento de referência medido

`data/gold/tese_natalia.pdf`, medido em 2026-08-06 por extração local com pdfplumber. Nenhum
conteúdo foi enviado à API nem lido por um modelo.

| Métrica | Valor |
|---|---|
| Páginas | 272 |
| Caracteres | 608.043 |
| Palavras | 91.113 |
| Caracteres por página | 2.235 |
| **Tokens** | **PENDENTE** |

O token count exige `count_tokens` — o venv não tem o SDK `anthropic` e não há
`ANTHROPIC_API_KEY`. Ver `docs/backlog.md`. Enquanto isso, a faixa de trabalho usada nas
estimativas abaixo é **3,5–4,5 caracteres por token**, que é **memória, não medição**, e existe
só para ordem de grandeza.

### Régua por tamanho (derivada de 2.235 car./pág.)

| Páginas | ≈ tokens (faixa não medida) | Etapa de documento inteiro |
|---|---|---|
| 50 | 25–32k | Haiku — cabe com folga |
| 100 | 50–64k | Haiku — cabe no pior caso |
| 200 | 99–128k | Sonnet — Haiku sem margem para prompt + saída |
| 272 (medido) | 135–175k | Sonnet |
| 360 | 179–230k | Sonnet |

Corte conservador, escolhido para sobreviver à incerteza da faixa: **Haiku em etapa de documento
inteiro só até 100 páginas; nunca acima de 200; medir entre 100 e 200.**

### Ordens de grandeza — todas pendentes de medição

Para a tese de 272 páginas:

| Cenário | Custo |
|---|---|
| Uma leitura integral em Opus 5 | US$ 0,68–0,87 |
| 25 etapas reenviando o documento, sem cache | US$ 17–22 |
| 25 etapas com prefixo cacheado (1 escrita 1,25× + 24 leituras 0,1×) | US$ 2,4–3,1 |

**O fan-out por unidade supera todos os três.** Com ~1200 unidades e prefixo de 20k, só a
leitura de cache do E4 dá ~US$ 7,20 em Sonnet, e o output ~US$ 5,40. **A contagem de unidades
por documento não foi medida** — "1200" é chute. O parser em `escolio/ingestao/` produz o número
exato; rodá-lo sobre `data/gold/` é processar o conjunto reservado de avaliação [LAC-ING-001] e
depende de decisão do professor.

## Instrumentação obrigatória

- `costs/ledger.jsonl` grava tokens e US$ por etapa. Consultar por agregação, nunca imprimir.
- Estimativa prévia de custo antes de qualquer execução — calculável a partir de páginas com a
  régua acima.
- Cache local em disco por hash do input: reexecutar o mesmo documento custa zero.
- `cache_read_input_tokens` zerado em requisições de prefixo idêntico **aborta a execução**.

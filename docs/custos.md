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

`data/gold/tese_natalia.pdf`, medido em 2026-08-06 por extração local com pdfplumber (estrutura)
e em 2026-08-07 por `count_tokens` (contagem de tokens, `claude-sonnet-5`) — **BL-007 resolvido**.
Nenhum conteúdo foi enviado para geração; `count_tokens` não produz resposta de modelo, só
contagem, e o texto extraído não foi gravado em disco.

| Métrica | Valor | Como obtido |
|---|---|---|
| Páginas | 272 | pdfplumber, 2026-08-06 |
| Caracteres (pdfplumber, `.extract_text()`) | 608.043 | pdfplumber, 2026-08-06 |
| Palavras | 91.113 | pdfplumber, 2026-08-06 |
| **Tokens (`input_tokens`, `claude-sonnet-5`)** | **259.399** | **`count_tokens`, 2026-08-07 — medido** |
| Caracteres por token (medido) | **2,345** | derivado da medição acima |

**A régua "3,5–4,5 caracteres por token" usada até aqui estava errada por larga margem** — o
valor medido é quase a metade do piso da faixa chutada. Documento historiográfico em português,
com aparato de notas e citações, tokeniza mais densamente que a heurística genérica em inglês
que gerou aquela faixa. Nenhuma estimativa anterior deste arquivo que tenha usado 3,5–4,5
car./token deve ser reaproveitada sem reconferir contra os 2,345 medidos.

Segunda medição, 2026-08-07: `pdfplumber` re-extraiu **608.314** caracteres (não 608.043) na
mesma execução que gerou o `input_tokens`. A diferença (271 caracteres, <0,05%) não foi
investigada — é ruído de biblioteca/versão entre as duas datas de extração, não divergência
material. Ambos os números ficam registrados; o de tokens usa a extração de 2026-08-07.

### Régua por tamanho (recalculada com 2,345 car./token medido)

Um só ponto foi medido (272 páginas → 259.399 tokens); os demais são extrapolação linear por
página a partir dele (2.235 car./pág. ÷ 2,345 car./token ≈ **953 tokens/pág.**), marcados como
tal. Extrapolar por página presume densidade de tokenização constante ao longo do documento —
não verificado, só assumido.

| Páginas | ≈ tokens | Base | Etapa de documento inteiro |
|---|---|---|---|
| 50 | ~48k | extrapolado | Haiku — cabe com folga |
| 100 | ~95k | extrapolado | Haiku — cabe no pior caso |
| 200 | ~191k | extrapolado | Haiku, no limite da janela de 200K — sem margem para prompt + saída |
| 272 | **259.399** | **medido** | Sonnet — já excede a janela do Haiku |
| 360 | ~343k | extrapolado | Sonnet |

**A régua antiga subestimava por quase metade.** A faixa de 3,5–4,5 car./token dava ~135–175k
para 272 páginas — abaixo da janela do Haiku (200K). O valor medido, 259.399, já **ultrapassa**
a janela do Haiku sozinho. Corte revisto: **Haiku em etapa de documento inteiro só até ~150
páginas; acima disso, Sonnet; medir before confiar em qualquer ponto entre 100 e 200.**

### Ordens de grandeza — recalculadas com o valor medido

Para a tese de 272 páginas (259.399 tokens de input, medidos):

| Cenário | Custo (Sonnet 5, preço introdutório $2/$10 até 2026-08-31) |
|---|---|
| Uma leitura integral, sem cache | ~US$ 0,52 input |
| 25 etapas reenviando o documento, sem cache | ~US$ 13,0 input (25 × 259.399 tok × $2/1M) |
| 25 etapas com prefixo cacheado (1 escrita 1,25× + 24 leituras 0,1×) | ~US$ 1,86 (1 × 259.399 × $2,50/1M + 24 × 259.399 × $0,20/1M) |

Custo de output **não incluído** acima — depende do tamanho de saída por etapa, que não foi
medido para nenhuma das 25 etapas do P11. Lembrar que output custa 5× input: mesmo uma saída
modesta domina o total se não for contida.

**O fan-out por unidade ainda supera os três cenários de documento inteiro** — ver medição de
unidades e custo do P13 logo abaixo, que substitui o chute de "~1200" por um número derivado do
parser real.

## BL-008 — unidades de fan-out, medidas por extrapolação

**Não medido diretamente sobre `data/gold/tese_natalia.pdf`.** `data/gold/` é conjunto reservado
para avaliação futura das heurísticas de ingestão [`escolio/ingestao/LACUNAS.md`, LAC-ING-001] —
processá-lo agora, mesmo só para contar, consumiria essa reserva. Em vez disso: contagem direta
sobre `data/dev/Relatorio_Final_PIBIC-Bolsa-CNPq-e-UEM - Ricardo Antonio Esteves dos Santos.pdf`
(33 páginas, já usado no desenvolvimento das heurísticas) via `escolio.ingestao.parser.parse_pdf`,
extrapolada linearmente por página até 272. Mesma disciplina que a régua de tokens acima: um
ponto medido, o resto é extrapolação marcada como tal.

### Contagem medida (`data/dev/`, 33 páginas)

| Tipo de unidade | Contagem |
|---|---|
| seções | 14 |
| parágrafos | 143 |
| notas de rodapé | 4 |
| citações recuadas | 4 |
| citações no corpo | 138 |
| referências | 60 |
| figuras | 4 |
| **total bruto** | **367** |

**Unidade de análise do P13 — `[PROPOSTA]`.** Nem todo tipo acima é candidato a unidade
comentável independente. Citações no corpo são ponteiros para dentro de um parágrafo já resolvido
[`escolio/ingestao/modelos.py`, docstring de `CitacaoNoCorpo`] — comentá-las é comentar o
parágrafo que as contém, não uma unidade extra. Referências são entradas da lista bibliográfica
final, raramente alvo de comentário individual isolado do corpo do texto. Seções não são unidade
de diagnóstico local — são estrutura, insumo da cartografia global (E3), não do fan-out (E4).
**Conjunto usado:** parágrafos + citações recuadas + notas de rodapé + figuras — os quatro tipos
que o P13 §10 admite como unidade comentável de granularidade textual e que este parser já
produz como unidade endereçável própria.

| | `data/dev/` (33 pág., medido) | extrapolado para 272 pág. |
|---|---|---|
| unidades de diagnóstico (parágrafo + citação recuada + nota + figura) | 155 | **1.281** |
| unidades por página | 4,70 | (mesma taxa, extrapolação linear) |

Extrapolação linear presume densidade de unidades por página constante — não verificado, só
assumido, mesmo risco já registrado para a régua de tokens acima. **1.281 substitui o "~1200"
chutado**; a proximidade dos dois números é coincidência da ordem de grandeza, não confirmação —
um vinha de memória, o outro de contagem real sobre documento diferente.

## O que acontece se o documento não couber na janela — existe caminho, ou é falha?

**Existe caminho, mas não está implementado — é lacuna de arquitetura, não de spec.** Nenhuma
fonte do acervo (P09, os cinco contratos de função) resolve isto: nenhum contrato menciona
janela de contexto, truncamento ou modelo — são "lacunas gerais preservadas" [P00,
`decisoes-vetadas.md` §1]. O que segue é `[PROPOSTA]` integral.

**Dois casos, com respostas diferentes:**

### Caso 1 — documento sozinho excede a janela do modelo escolhido

Não é hipotético para Haiku: os 259.399 tokens da tese já ultrapassam sua janela de 200K sozinhos
[régua acima]. **Caminho existente, já em uso nesta conta:** trocar de modelo. A régua por
tamanho já resolve isso para Haiku → Sonnet ("Haiku em etapa de documento inteiro só até ~150
páginas; acima disso, Sonnet"). Para Sonnet/Opus (1M de contexto), o documento precisaria ter
~4.290.000 caracteres (≈1.900 páginas nesta densidade de 2.235 car./pág.) para repetir o problema
— fora do porte de qualquer tipo de documento que as seis funções cobrem hoje (a maior categoria,
tese/dissertação, não tem teto de página declarado em P11, mas 1.900 páginas não é caso realista
registrado em nenhuma fonte). **Não é falha: é troca de modelo, já coberta pela régua.**

### Caso 2 — prefixo cacheado + acúmulo de chamadas excede a janela **durante** uma sessão

Este é o caso real e não coberto. Numa sequência de 65 chamadas de diagnóstico (cenário do P13
acima), o prefixo (259.399 tokens) é fixo, mas se a arquitetura de execução acumular contexto de
chamadas anteriores na mesma conversa (histórico de mensagens, resultados intermediários), o
total pode crescer chamada a chamada até estourar mesmo a janela de 1M do Sonnet — não pelo
documento, mas pelo próprio histórico de execução.

**Não há caminho implementado. Isto é falha hoje, registrada como tal:**

- Nenhum código no projeto gerencia janela de contexto entre chamadas — `escolio/funcoes/` só
  declara etapas e gates, não executa (roadmap item 6, e deliberadamente sem `executar()`
  [CLAUDE.md §4, "não funde execução"]).
- A arquitetura correta, quando a execução existir, é **cada chamada de diagnóstico ser
  independente** — prefixo (documento) + as ~20 unidades daquela chamada, sem acumular resultado
  de chamadas anteriores no mesmo contexto. É o que os cálculos acima já presumem (cada uma das
  65 chamadas é isolada, só o prefixo se repete via cache) — mas isso é premissa de cálculo, não
  garantia de código: nada impede uma implementação futura de acumular histórico por engano.
- **Consequência prática se estourar:** a API retorna erro de contexto excedido — não há
  truncamento silencioso de prompt na Messages API. É comportamento seguro (falha visível), mas
  não é *tratamento* — não há hoje lógica de retomada, paginação de unidades ou redução de escopo
  automática quando isso ocorre.

**O que falta, registrado no roadmap e não decidido nesta sessão:** um mecanismo explícito de
isolamento de contexto por chamada de diagnóstico, e uma política do que fazer quando mesmo uma
única chamada (prefixo + unidades daquela chamada + system prompt + espaço de output) excede a
janela — reduzir unidades por chamada é o alavanca óbvio, mas nenhuma fonte declara o limiar em
que isso deve disparar automaticamente, e criar esse limiar por inferência substituiria a lacuna
por um número que nenhuma fonte sustenta.

## Custo por execução — revisão completa do P13 sobre tese de 272 páginas

Convenções desta seção, todas `[PROPOSTA]` e declaradas para poderem ser contestadas:

- **1.281 unidades de diagnóstico** (acima), agrupadas em **20 unidades por chamada** no E4 —
  orientação do §10 ("agrupar unidades por chamada... o contrato governa a unidade de análise,
  não a granularidade da requisição"). 1.281 ÷ 20 ≈ **65 chamadas de diagnóstico**.
- Cada chamada de diagnóstico carrega o **documento inteiro como prefixo** (259.399 tokens
  medidos) — exigido por "do global para o local" [P11 §2] e pela cartografia global obrigatória
  antes de qualquer diagnóstico local [CLAUDE.md §4]. Sem essa premissa o cache não tem prefixo
  comum a cachear.
- **Output por chamada não medido** — nenhuma chamada real do P13 foi feita ainda. Estimativa:
  20 unidades × ~150 tokens de comentário candidato cada (diagnóstico interno, não o comentário
  final) ≈ 3.000 tokens de output por chamada. Sem esta chamada. Sujeito a revisão assim que
  houver execução real — não é medição, é a única forma de dar número antes de rodar.
- E2 (segurança/injeção) e E3 (cartografia) não entram nesta conta — são custo à parte, menor
  (Haiku, ver régua acima) e não é o que a pergunta pediu.

**Modelo usado em toda tabela abaixo: Sonnet 5, preço introdutório $2,00/$10,00 por 1M tokens até
2026-08-31 — e não outro, pelas seguintes razões, cada uma eliminando uma alternativa:**

- **Não Haiku.** O prefixo sozinho (259.399 tokens) já ultrapassa a janela de 200K do Haiku 4.5
  [tabela de preços acima] — nem cabe uma chamada, muito menos 65. A régua por tamanho já registra
  isto: "272 páginas — Sonnet, já excede a janela do Haiku". Não há chamada de diagnóstico deste
  documento que Haiku possa fazer.
- **Não Opus.** A tabela de modelos por etapa do CLAUDE.md §10 reserva Opus para **E4c
  (seletividade → seleção) e E5 (matriz/plano)** — decisão irreversível, julgamento caro. O E4 de
  diagnóstico por unidade, que é o que esta conta mede, está explicitamente marcado **Sonnet** na
  mesma tabela. Rodar em Opus custaria 2,5× o input e 2,5× o output do preço introdutório de
  Sonnet, sem que a etapa exija o julgamento mais caro que justificaria a troca.
- **Sonnet, com a ressalva do prazo.** O preço introdutório vale só até 2026-08-31; depois volta a
  $3/$10 → $3/$15. Toda linha desta seção usa o preço introdutório porque é o vigente na data
  desta medição (2026-08-07) — qualquer execução real após 2026-08-31 precisa refazer a conta com
  $3/$15, o que muda os totais em ~50% no input e mantém o output igual.

### Cenário 1 — sem otimização (sem cache, sem batch) — Sonnet 5

Cada uma das 65 chamadas reenvia o documento completo.

| Componente | Modelo | Cálculo | US$ |
|---|---|---|---|
| Input (documento repetido) | Sonnet 5 | 65 × 259.399 tok × $2/1M | 33,72 |
| Output | Sonnet 5 | 65 × 3.000 tok × $10/1M | 1,95 |
| **Total** | | | **≈ US$ 35,67** |

### Cenário 2 — com cache (síncrono, prefixo de 259.399 tokens) — Sonnet 5

Uma escrita de cache (1,25×) na primeira chamada; as 64 seguintes leem o cache (0,1×). TTL
máximo 1h — 65 chamadas sequenciais de diagnóstico cabem nesse tempo com folga. Cache é
específico por modelo [ver "Cache", acima: "Trocar de modelo invalida o cache"] — todas as 65
chamadas precisam ser Sonnet, não só pela razão de custo acima, mas porque misturar modelo no
meio da sequência invalidaria o prefixo cacheado e forçaria nova escrita.

| Componente | Modelo | Cálculo | US$ |
|---|---|---|---|
| 1ª chamada — escrita de cache | Sonnet 5 | 259.399 × 1,25 × $2/1M | 0,65 |
| 64 chamadas — leitura de cache | Sonnet 5 | 64 × 259.399 × 0,1 × $2/1M | 3,32 |
| Output (65 chamadas) | Sonnet 5 | 65 × 3.000 × $10/1M | 1,95 |
| **Total** | | | **≈ US$ 5,92** |

Redução de **~83%** sobre o cenário sem otimização — o efeito esperado de cachear um prefixo
grande reaproveitado dezenas de vezes.

### Cenário 3 — cache + batch — Sonnet 5

Batch dá 50% de desconto sobre todo o uso de tokens, mas **não compõe com cache da forma ingênua**
— `p < 1,25u` decide qual dos dois vence [ver "Batch × cache é escolha, não acúmulo" acima]. Aqui
`p` (prefixo, 259.399) é muito maior que `u` (conteúdo único por chamada, ~20 unidades de texto —
não medido, mas necessariamente pequeno comparado ao documento inteiro). Isso favorece cache, não
batch: o cenário 2 já vence o teste `p < 1,25u`. Rodar em batch **sem** cache seria pior que o
cenário 2 (bateria os 65 envios completos do documento, só que a metade do preço — ainda maior
que US$ 5,92 se `u` for pequeno). Modelo continua Sonnet 5 pela mesma razão do cenário 1 — a
Batches API não muda qual modelo é adequado à etapa, só o preço:

| Componente | Modelo | Cálculo | US$ |
|---|---|---|---|
| Input, batch sem cache, 65 envios completos | Sonnet 5 | 65 × 259.399 × $2/1M × 0,5 | 16,86 |
| Output, batch | Sonnet 5 | 65 × 3.000 × $10/1M × 0,5 | 0,98 |
| **Total (batch sem cache)** | | | **≈ US$ 17,84** |

**Batch com cache não é oferecido pela API para chamadas síncronas com cache — são mecanismos
concorrentes, não somáveis nesta arquitetura** [mesma nota de "Batch × cache é escolha, não
acúmulo"]. O cenário vencedor continua sendo o **2** (cache síncrono): **≈ US$ 5,92**.

### Custo-alvo por documento — critério de desenho, não teto de orçamento

**Alvo proposto: US$ 3,00–6,00 por revisão completa do P13 sobre um documento de porte de tese
(≈270 páginas).** Este não é limite de gasto — é critério que testa a arquitetura: se o cenário
otimizado ultrapassar esse alvo por larga margem, o desenho (não o orçamento) precisa mudar.

Por que este alvo e não outro:

- O cenário 2 medido (**US$ 5,92**) já está **dentro** da faixa — o que diz que a arquitetura de
  cache síncrono com prefixo único é suficiente para o caso comum, **sem precisar de batch**.
- Um alvo abaixo de US$ 3 forçaria abandonar o prefixo de documento inteiro por chamada — que é
  exigência do próprio CLAUDE.md ("do global para o local"), não escolha de custo. Cortar o
  prefixo para caber num alvo mais baixo violaria a regra estrutural, não otimizaria a execução.
- Um alvo acima de US$ 10 deixaria de funcionar como critério: o cenário sem otimização
  (US$ 35,67) só é seis vezes pior, não uma ordem de grandeza — o alvo perderia poder de forçar
  a decisão de cachear.

**O que este alvo NÃO cobre:** E2, E3, E5 (matriz/plano, Opus), E6 (execução) e E7 (auditoria) —
só o fan-out de diagnóstico do E4 para o P13. Uma revisão completa por uma das outras quatro
funções (P10 a P12, P14) tem etapas e volumes de saída diferentes e precisa de conta própria
quando a execução real existir. **Se o alvo for ultrapassado em produção** (output real maior que
os ~150 tok/unidade estimados, ou mais de 65 chamadas por não caber 20 unidades/chamada), os dois
alavancas de correção, em ordem de custo-benefício: (1) aumentar unidades por chamada — reduz o
número de leituras de cache linearmente; (2) revisar o teto de output por unidade — nenhum
comentário do P13 deveria precisar de muito mais que um parágrafo de diagnóstico interno.

## Cache não aproveitado — anomalia detectável em tempo real, não descoberta na fatura

**Diferente de estourar a janela** (seção acima: a chamada falha, com erro visível). Aqui a
chamada funciona normalmente, o resultado sai correto, e o custo salta de ~US$ 6 para ~US$ 35
sem nenhum sinal — a menos que alguém verifique.

**Verificado contra a documentação oficial do SDK** (`skill claude-api`, não memória): a resposta
de toda chamada à Messages API traz, em `response.usage`:

| Campo | Significado | Custo relativo |
|---|---|---|
| `cache_creation_input_tokens` | tokens escritos no cache nesta chamada | ~1,25× (TTL 5 min) ou ~2× (TTL 1h) |
| `cache_read_input_tokens` | tokens lidos do cache nesta chamada | ~0,1× |
| `input_tokens` | tokens processados a preço cheio, não cacheados | 1× |

**Os três campos vêm em toda resposta, sempre — não só quando a requisição usa `cache_control`.**
Quando não há cache envolvido, os dois campos de cache vêm `0`; não é preciso ativar nada para
lê-los. Isso é o que transforma "custo saltou" de descoberta pós-fato em verificação em tempo de
execução: **taxa de acerto de cache abaixo do esperado é condição testável chamada a chamada**,
não algo que só aparece na fatura no fim do mês.

O sinal de anomalia já está documentado pela própria Anthropic, verbatim: *"se
`cache_read_input_tokens` for zero em requisições repetidas com prefixo idêntico, um invalidador
silencioso está em ação"* — timestamp no system prompt, UUID, `json.dumps` sem `sort_keys`,
conjunto de ferramentas variável por chamada. A linha "`cache_read_input_tokens` zerado […] aborta
a execução", já registrada abaixo, é esse mesmo requisito; esta seção o torna operacional.

### Requisito da peça que chamará a API — `[PROPOSTA]`, ainda não implementado

Nenhuma chamada real do P13 foi feita; isto é especificação para quando a execução existir, não
comportamento já construído. Três exigências, na ordem em que a peça deve implementá-las:

1. **`costs/ledger.jsonl` grava os três campos de `usage` por chamada, não só o total em US$.**
   Sem `cache_creation_input_tokens` e `cache_read_input_tokens` lado a lado com `input_tokens`,
   o ledger permite calcular gasto mas não permite auditar *por que* o gasto foi aquele.
2. **Taxa de acerto esperada é derivável do desenho da chamada, antes de executar.** Nos cálculos
   desta seção, a chamada 1 de uma sequência de diagnóstico é escrita (`cache_creation`); as
   chamadas 2–65 são leitura (`cache_read` ≈ tamanho do prefixo). Uma chamada da posição 2 em
   diante com `cache_read_input_tokens` muito abaixo do prefixo esperado — não necessariamente
   zero, um invalidador pode corromper só parte do prefixo compartilhado — é a anomalia.
3. **A checagem é por chamada, não agregada ao fim da execução.** Esperar o fim das 65 chamadas
   para comparar o total em US$ contra a estimativa prévia já é "descoberta na fatura", só que
   adiada para o fim da execução em vez do fim do mês. O requisito é comparar
   `cache_read_input_tokens` contra o esperado **antes de disparar a próxima chamada da mesma
   sequência** — abortar cedo custa 1 chamada extra; abortar tarde custa as 65.

**O que isto não resolve, e não é papel do ledger resolver:** identificar *qual* byte no prefixo
mudou. Isso é trabalho de diff entre as duas renderizações do prompt (`tools` → `system` →
`messages`, na ordem em que a API os concatena), não de leitura de `usage`. O ledger detecta que
há um invalidador; encontrar qual é depuração manual.

## Instrumentação obrigatória

- `costs/ledger.jsonl` grava tokens e US$ por etapa. Consultar por agregação, nunca imprimir.
- Estimativa prévia de custo antes de qualquer execução — calculável a partir de páginas com a
  régua acima.
- Cache local em disco por hash do input: reexecutar o mesmo documento custa zero.
- `cache_read_input_tokens` zerado em requisições de prefixo idêntico **aborta a execução**.
- **Ledger por chamada, não só por etapa** — os três campos de `usage`
  (`cache_creation_input_tokens`, `cache_read_input_tokens`, `input_tokens`) gravados em toda
  chamada da sequência, não só o agregado. Ver seção "Cache não aproveitado" acima para o
  requisito completo e a justificativa.

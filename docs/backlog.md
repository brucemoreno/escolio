# Backlog

Assunto fora do tema da sessão corrente. Nada aqui é executado sem sessão própria.

Aberto em 2026-08-06, na sessão de reescrita do CLAUDE.md. Nenhum item abaixo foi executado.

## Mudanças de código implicadas pela reescrita

### BL-001 — `budget_tokens` e thinking: qualquer chamada hoje quebraria
Nenhuma chamada à API existe ainda, mas a regra antiga do CLAUDE.md ("`budget_tokens` teto
2000") produziria **erro 400** no Opus 5 e no Sonnet 5. Ao escrever o primeiro cliente: usar
`output_config.effort`; lembrar que no Opus 5 o thinking está ligado por padrão e que
`thinking: {type: "disabled"}` só é aceito com effort ≤ `high`. Ver `docs/custos.md`.

### BL-002 — mapeamento P05 ↔ P09 §12
`escolio/relacao.py` usa `EVIDENCIA_SUFICIENTE`, `ALTA`, etc. O `ClaimEvidence` do P09 §12 usa
`SUFFICIENT | PARTIAL | INSUFFICIENT | NOT_APPLICABLE` e `HIGH | MEDIUM | LOW | UNDETERMINED`.
Falta uma camada de tradução explícita, com aliases, **sem apagar distinções** — o mesmo
tratamento que o `CON-P05-001` dá à divergência P04/P05. Não alterar o schema P05.

### BL-003 — ingestão → `InputItem` e `material_id`
`escolio/ingestao/FORMATO.md` declara que o contrato "virá do P09". O P09 chegou.
`DocumentoIngerido` precisa de um adaptador para `InputItem` [P09 §6] e de `material_id`
[P19 §9-10]. `FORMATO.md` deve registrar que a reconciliação está pendente, não feita.

### BL-004 — máquina bibliográfica P04 (X01)
Existe o schema P05; não existe a máquina de 17 estados do P04/03, nem os aliases para os 9
estados mínimos da R03 CAMADA D. É o que falta para X01 estar completa.

### BL-005 — `handoff/` está em JavaScript
O resto do projeto é Python. Decidir: portar, ou registrar a razão de manter as duas linguagens.
Não é urgente; é inconsistência declarada.

### BL-006 — máquina P06 e `InterventionRecord`
Os 15 níveis `INT-01…INT-15`, as regras de escalonamento e a regressão segura [P06 §7, §8] não
existem em código. Dependem do envelope P09.

## Ambiente e medição

### BL-007 — instalar o SDK `anthropic` e configurar chave
O venv não tem `anthropic` e `ANTHROPIC_API_KEY` está indefinida. Sem isso não roda
`count_tokens`, e a contagem de tokens da tese de referência fica pendente em `docs/custos.md`.
Enquanto durar, todo valor em tokens e em US$ é ordem de grandeza, não medição.

### BL-008 — contagem de unidades por documento
Todo cálculo de custo de fan-out usa "~1200 unidades", que é chute. O parser em
`escolio/ingestao/` produz o número exato. Rodá-lo sobre `data/gold/` significa processar o
conjunto reservado de avaliação [LAC-ING-001] — **depende de decisão do professor**. Alternativa
sem essa decisão: medir sobre `data/dev/` e extrapolar por página, registrando a extrapolação.

## Mapeamento de spec pendente

### BL-009 — P08, P19, P20 e R03 sem mapa em `docs/spec/`
Foram lidos por amostragem ou citados de segunda mão. Cada um merece uma sessão de leitura com
mapa próprio, no padrão de `funcoes-P10-P14.md`. O P19 é o mais urgente: bloqueia o item 6 da
lista ABERTO do CLAUDE.md (retenção do histórico de resolução).

### BL-010 — lacunas de ingestão nunca gravadas nos artefatos canônicos
A §8 de `docs/spec/funcoes-P10-P14.md` levantou quatro lacunas — extração de
objetivo/hipótese/método, comparação entre versões, granularidade de célula de tabela, ingestão
de parecer editorial — que **não** foram gravadas em `escolio/ingestao/LACUNAS.md` nem em
`docs/coleta.md`. Continuam só no entregável daquela sessão.

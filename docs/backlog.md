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

### BL-003 — ingestão → `InputItem` e `material_id` — RESOLVIDO PARCIALMENTE
`escolio/adaptadores/ingestao_para_input_item.py` implementa `InputItem` [P09 §6] por
documento e `material_id` [P19 §10, regra de identidade apenas]. Não implementado:
`MaterialUnit` [P19 §9] completo (26 campos restantes) — P19 §71-73 proíbem classificar
material real fora do fluxo homologado com gates humanos; é trabalho futuro de
`CURADOR_DE_DADOS` + `USUARIO_PROPONENTE`, não deste adaptador. Ver
`escolio/ingestao/LACUNAS.md` LAC-ING-012.

### BL-004 — máquina bibliográfica P04 (X01) — RESOLVIDO
`escolio/bvaa/` implementa os 17 estados [P04/03] e as 18 transições (T01-T18, T18 curinga
`QUALQUER_ESTADO`) [P04/04], o protocolo de abstenção com os 7 gatilhos consolidados de
P04 §11/§07, e `escolio/bvaa/correspondencia.py` documenta a correspondência com R03 CAMADA
D e os três campos do P05 (`access_state`/`reading_state`/`validation_state`) sem fundir os
vocabulários — CON-P05-001 permanece três vocabulários distintos, nenhum escolhido como
vencedor. Ver `escolio/bvaa/LACUNAS.md`.

### BL-005 — `handoff/` está em JavaScript
O resto do projeto é Python. Decidir: portar, ou registrar a razão de manter as duas linguagens.
Não é urgente; é inconsistência declarada.

### BL-006 — máquina P06 e `InterventionRecord` — RESOLVIDO em `escolio/intervencao/`
Os 15 níveis `INT-01…INT-15`, escalonamento, regressão segura [P06 §7, §8] e `InterventionRecord`
[P09 §13] implementados. Pendente: ligar `Response.interventions` (`escolio/contrato/resposta.py`)
a `InterventionRecord` quando o roteador de função existir — ver comentário lá.
O roteador passou a existir em 2026-08-07 (`escolio/funcoes/`); a ligação continua pendente
porque altera arquivo existente — ver BL-013.

## Aberto em 2026-08-07, na sessão do roteador de função (item 6)

Nenhum arquivo existente foi alterado naquela sessão. Os cinco itens abaixo são exatamente as
integrações que exigiriam alterá-los.

### BL-011 — `exige_correspondencia_request_response` não confere `function_id`
`escolio/contrato/resposta.py:250-258` confere `request_id`, `project_id` e `component_id`. O
P09 §8.1 exige também: "`response.function_id` deve corresponder à função da requisição". A
linha faltante nasceu em `escolio/funcoes/roteador.py::exige_correspondencia_de_funcao` para não
tocar em `resposta.py`. Enquanto durar, há **duas** funções de correspondência e quem chama
precisa das duas. Decidir: mover a verificação para `resposta.py` (que passaria a depender do
catálogo, hoje deliberadamente fora do envelope) ou manter separadas e documentar o par.

### BL-012 — fixtures de teste usam `function_id` com valor de componente
`tests/contrato/test_requisicao.py:18-19` e `tests/contrato/test_resposta.py:37-38` passam
`component_id="P12", function_id="P12"`. O catálogo do item 6 fixou `function_id` no namespace do
P02 (`LLM-ACA-F03`) e `component_id` no da R03 (`P12`) — ver `escolio/funcoes/LACUNAS.md`,
LAC-FUNC-002. Os fixtures **não quebram** (o `Request` só verifica não-vazio) mas registram uma
convenção que o catálogo contradiz. Migrar ou declarar que os fixtures são propositalmente
agnósticos ao catálogo.

### BL-013 — `Response.interventions` continua desligado
Sucessor direto do BL-006. `InterventionRecord` existe em `escolio/intervencao/registro.py`;
`Response` (`escolio/contrato/resposta.py:139-140`) omite o campo com comentário explícito. Ligar
altera `resposta.py`. A dependência que faltava — o roteador — já não é o bloqueio.

### BL-014 — `InputItem.classification.functions` não é populado por ninguém
O campo existe (`escolio/contrato/entrada.py:36`) e o roteador **lê** dele a única informação de
função que o envelope carrega [P09 §6]. Quem deveria preenchê-lo não existe:
`escolio/adaptadores/ingestao_para_input_item.py:70-75` declara que isso "é trabalho de
P19/roteador de função". O roteador lê, não declara — declarar material para uma função é ato de
`CURADOR_DE_DADOS` + `USUARIO_PROPONENTE` sob o P19. Consequência prática hoje: todo `InputItem`
vindo da ingestão resulta em `AdmissaoDeMaterial.INDETERMINADO`, e nenhuma função é elegível.

### BL-015 — o CLAUDE.md §13.3 apoia-se em premissa falsa
A questão aberta pergunta se capítulo de livro e relatório de pós-doutorado seriam "P15+,
generalização autorizada de P11, ou fora de escopo". O inventário canônico da R03
(`02_INVENTARIO_DE_COMPONENTES_E_PACOTES_A_PRODUZIR_R03.csv`) desmente a primeira alternativa:
P15 é `PROFILES`, P16 `CONTEXTOS_GEOGRAFICOS`, P17 `CONTEXTOS_TEMPORAIS`, P18 `INTERSECOES` —
nenhum é camada `FUNCAO`, e a camada `FUNCAO` termina em P14. Não há componente livre para uma
sexta macrofunção, e a R03 está homologada e congelada. As quatro candidatas da R03 CAMADA B
("revisão de artigo antes da submissão", "incorporação de comentários de qualificação ou defesa",
"auditoria bibliográfica e documental autônoma", "revisão de projeto de pesquisa ou proposta de
financiamento") também não têm componente atribuído. O CLAUDE.md não foi alterado: corrigir §13.3
e §13.4 é ato de governança, não de sessão técnica.

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

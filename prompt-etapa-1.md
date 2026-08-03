# ETAPA 1 — LEITURA DA GOVERNANÇA. NÃO ESCREVA CÓDIGO. NÃO DECIDA ARQUITETURA.

NÃO leia o CLAUDE-rascunho.md até o Passo 7. Ignore-o até lá, mesmo que pareça relevante.

## Contexto

Em `corpus/governanca-R01/` está a **primeira leva de uma coleção de 29 pacotes**
(P00–P28) de governança escritos manualmente pelo Prof. Dr. Christian Fausto
Moraes dos Santos, pós-doutor em história da ciência, para um sistema de correção
de trabalhos acadêmicos com LLM. Chegaram P00–P04, ~324 KB: txt, csv, jsonl, md
e json. Cabem em contexto — leia tudo.

**P05 a P28 ainda estão sendo escritos por ele.** Léxico, voz, marcas de oralidade
e registro de uso real virão em levas futuras. Portanto: lacuna encontrada aqui
pode ser conteúdo de pacote futuro, não omissão. Registre como pendente de leva
posterior, nunca como falha da especificação.

Esta é a camada de governança — precedência, travas, gates, vocabulário
controlado, schema. É a gramática dos pacotes seguintes. O mapa que você produzir
será atualizado por incremento a cada leva nova, nunca refeito do zero.

O foco declarado dele é anti-deriva e anti-alucinação. O sistema não pode inferir,
não pode preencher lacuna, não pode avançar sem autorização expressa.

Sua tarefa é MAPEAR o que ele especificou. Não avaliar, não melhorar, não propor.

## Regras

**Fidelidade acima de síntese.** Esta é a especificação de um cliente, não
material a destilar. Onde ele define termo, transcreva a definição literal. Onde
estabelece regra, transcreva a regra. Paráfrase que "melhora" a redação dele é
erro, não contribuição.

**Rastreabilidade.** Todo item citando o arquivo de origem: `[P0X/nome-arquivo]`.
Inferência sua vai marcada `[INFERIDO]` com a base. Nada preenchido de memória
ou de conhecimento geral sobre sistemas de LLM.

**Lacuna é dado.** Ele registra explicitamente o que não sabe e o que não
autorizou. Isso não é buraco a tapar — é decisão dele, e vale tanto quanto o que
está escrito.

**Verbosidade.** No chat, só o que exigir decisão minha. Nos entregáveis, densidade
e completude. Não despeje conteúdo de arquivo no chat.

## Passo 1 — Ordem de leitura

Cada pacote tem `00_LEIA_PRIMEIRO.txt` com ordem declarada. Leia os cinco
`00_LEIA_PRIMEIRO` antes de qualquer outra coisa e siga a ordem que ele definiu,
não a alfabética.

Depois leia integralmente os cinco pacotes:
- P00 CONTROLE_MESTRE_ESTADO_CANONICO — governança, precedência, linha do tempo
- P01 TRAVA_E_REATIVACAO — anti-deriva, reativação, comandos vagos, restauração
- P02 CATALOGO_FUNCIONAL — inventário funcional, requisitos, gates, saídas
- P03 NUCLEO_TRANSVERSAL — políticas, máquina de estados, gates, proveniência
- P04 BVAA_UNIVERSAL — validação bibliográfica, leitura efetiva, abstenção
- Além destes há uma pasta `PACOTE_SCHEMA_AFIRMACAO_EVIDENCIA` (P05), que o
  manifesto declara NÃO INICIADO. Leia também e registre a discrepância.

## Passo 2 — `docs/spec/mapa-governanca.md`

O mapa da especificação. Para cada pacote: o que estabelece, que artefatos define,
que regras impõe, e como se conecta aos demais.

Seções obrigatórias:

**Máquinas de estado.** Ele define pelo menos duas (documental em P03,
bibliográfica em P04). Transcreva estados, transições e condições. São o coração
executável da especificação.

**Gates e autoridades.** `MATRIZ_DE_GATES_E_AUTORIDADES` e
`MATRIZ_DE_REQUISITOS_LIMITES_GATES_E_SAIDAS`. O que bloqueia o quê, quem
autoriza transição, o que é bloqueio duro.

**Travas anti-deriva.** P01 tem versão operacional e versão monolítica. Descreva
as duas, a diferença, e quando cada uma se aplica. Inclua o protocolo de resposta
a comandos vagos e o de restauração de estado.

**Vocabulário controlado.** Todo termo com significado técnico definido por ele:
DERIVA, GATE, TRAVA, CONGELADO, HOMOLOGADO, PENDENTE_BVAA, PEDIR_PDF,
CORRIGIR_ANTES_DE_AVANÇAR, LEITURA_EFETIVA, ABSTENÇÃO, PROVENIÊNCIA, e outros
que encontrar. Definição literal dele, não sua.

**Schema afirmação-evidência.** Campos, dicionário de dados, vocabulário de
status, regras de coerência, matriz de suficiência e confiança, rastreabilidade
bidirecional. Transcreva a estrutura completa.

**Protocolo BVAA.** Como valida fonte, página, citação e referência. O protocolo
de leitura efetiva, o de localização e paginação, e sobretudo o de **abstenção**
— quando ele manda o sistema NÃO recomendar. Isso é anti-alucinação em forma
executável.

## Passo 3 — `docs/spec/autoridade-e-lacunas.md`

**Cadeia de autoridade.** A R03 (`PACOTE_PROTOCOLO_MESTRE_ACAO_ECOSSISTEMA_
LLM_ACADEMICA_R03.zip`, sha256 `0f7e3acf...`) é declarada autoridade canônica e
NÃO está neste acervo. Liste tudo que os pacotes atribuem à R03 sem reproduzir —
é o que falta e não dá para inferir.

Registre também a regra de precedência (R03 > R02 > R01) e o que ela implica.

**Estado real de cada pacote.** O P00 se declara `NAO_AUDITADO`,
`NAO_HOMOLOGADO`, enquanto o manifesto da coleção declara todos
`HOMOLOGADO_E_CONGELADO`. Mapeie o estado autodeclarado de cada um e liste as
contradições. Não resolva.

**Lacunas não inferíveis.** Compile todas, dos cinco pacotes. São decisões que ele
deliberadamente não tomou. Diga, para cada, o que fica bloqueado por ela.

**Discrepâncias do manifesto.** Ele declara `P05_P28: NAO_INICIADOS`, mas existe
pasta com arquivos P05. Liste esta e outras que encontrar.

## Passo 4 — `docs/spec/decisoes-vetadas.md`

O P00 estabelece que permanecem não autorizados: arquitetura técnica, plataforma,
modelo, fornecedor, número de agentes, corpus, licenças, privacidade, treinamento,
RAG, fine-tuning, implementação e pilotos — e que nenhuma lacuna pode ser
preenchida por inferência, exigindo autorização expressa do USUARIO_PROPONENTE.

Compile a lista completa e literal, dos cinco pacotes. Para cada item: onde está
escrito, e o que exatamente veda.

Não interprete o alcance. Não diga se vale para este projeto. Só registre o que
está escrito e onde.

## Passo 5 — `docs/spec/pacotes-esperados.md`

`04_INVENTARIO_CANONICO_DE_COMPONENTES_R03.csv` e
`05_INVENTARIO_CANONICO_DE_PACOTES_R03.csv` provavelmente listam os 29 componentes
planejados. Se listarem, transcreva: identificador, denominação, fase, camada e
o que cada um deve conter, segundo ele.

Marque quais já chegaram e quais faltam. Onde o conteúdo de um pacote futuro
resolveria lacuna encontrada nesta leitura, aponte a correspondência.

Se os inventários não trouxerem a lista completa, diga o que trazem e pare.
Não infira a lista dos 29.

## Passo 6 — `docs/spec/contorno-vs-criterio.md`

Levantamento para devolver ao professor. **Classifica, não julga.**

Ele projetou tudo para prompt de navegador: sem estado persistente, sem execução
de código, sem verificação automática, sessão que se perde, contexto que estoura.
Muita especificação existe para contornar isso. Um sistema em Python com API não
tem essas limitações — e ali a especificação manual vira trabalho evitável.

**O que classifica cada item é a causa declarada por ele, não a aparência.**
Se um documento se chama "protocolo de restauração de estado após perda de
sessão", a causa está no nome. Procure a razão que ele escreveu junto da regra.

Três categorias:

**[CONTORNO]** — existe porque o LLM esquece, a sessão cai, o contexto estoura,
ou não havia como verificar automaticamente. Em código, o problema não existe.
Candidatos prováveis: restauração de estado, recibo de restauração, protocolo de
reativação, resposta a comando vago, migração para chat novo, trava monolítica
versus operacional, reinjeção manual de contexto.
Para cada: que limitação contorna, e como o sistema resolveria (estado em disco,
função Python, chamada sem estado, teste automatizado).

**[CRITÉRIO]** — julgamento acadêmico dele. **Permanece integralmente, seja qual
for a plataforma.** Candidatos: protocolo de abstenção bibliográfica, matriz de
suficiência e confiança, regras de coerência, o que exige leitura efetiva, o que
bloqueia avanço por razão acadêmica. Não sugira alteração nenhuma aqui.

**[INVERTIDO]** — a parte mais valiosa. Regra que ele escreveu como INSTRUÇÃO ao
modelo e que em código vira INVARIANTE que o modelo não pode violar. Trava vira
asserção; gate vira teste; proveniência obrigatória vira campo validado no schema;
`CORRIGIR_ANTES_DE_AVANÇAR` vira exceção que interrompe o pipeline.
É mais anti-deriva do que ele conseguiu no navegador: instrução se desobedece,
invariante não.

**Forma do entregável.** Este texto vai para o professor. Escreva cada item como
PERGUNTA, não como veredito: "o protocolo de restauração de estado ainda é
necessário se o sistema mantiver estado persistente em disco?" — não "isto não é
mais necessário". Ele pode ter razão que não está no documento.

Na dúvida entre contorno e critério, classifique como CRITÉRIO. Descartar critério
por engano custa muito mais que manter contorno desnecessário.

Abra o arquivo reconhecendo o que a especificação dele resolve bem. Não é
diplomacia: o rigor documental dele é o que torna este projeto possível, e o
levantamento existe para poupar trabalho manual futuro, não para reduzir escopo.

### Passo 7 — SÓ AGORA leia o CLAUDE-rascunho.md

Com o mapa da especificação pronto, leia o `CLAUDE-rascunho.md` e grave
docs/spec/divergencias.md.

Três seções:

**Onde a especificação dele é mais completa.** Aponte o que ele já resolveu e o
CLAUDE-rascunho.md trata de forma rudimentar. Suspeitos: o schema de achado (§7) contra o
schema afirmação-evidência dele; propagação de estado (§4) contra as travas
anti-deriva; verificação de fontes contra o BVAA.

**Onde há contradição direta.** Regra do CLAUDE-rascunho.md que conflita com regra
congelada dele. Cite os dois lados. Não escolha vencedor.

**Onde o CLAUDE-rascunho.md cobre o que a especificação não cobre.** Pontos em que ele é
silencioso e o meu desenho decide algo. São candidatos a autorização expressa.

## Fim

`docs/sessions/etapa1-governanca.md` com o que foi mapeado, o que ficou aberto,
e o custo.

Não proponha arquitetura. Não altere o CLAUDE-rascunho.md. Não resolva contradição.
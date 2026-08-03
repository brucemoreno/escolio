# Escólio

Sistema de apoio à revisão de trabalhos acadêmicos que reproduz o método, os critérios
e a voz de correção do Prof. Dr. Christian Fausto Moraes dos Santos (história da ciência).

Um escólio é uma nota erudita acrescentada à margem do texto de outro: sempre assinada
por quem a escreveu, sempre subordinada ao original. É a relação exata entre este
sistema, o professor e o trabalho do aluno.

## 1. Limites do projeto

- NÃO é fine-tuning. A API da Anthropic não oferece fine-tuning de modelos Claude.
  A adaptação de estilo é feita por engenharia de contexto. Ver `docs/adr/ADR-001.md`.
- NÃO substitui o professor. Toda saída passa por revisão dele, e todo achado
  carrega evidência localizada e nível de confiança.

## 1b. Dois modos de saída

Mesmo pipeline, renderizadores diferentes. A bifurcação acontece só em C4.

- **Modo comentário** — para trabalho que vai a banca. Aponta, justifica e sugere,
  em registro conversacional com marcas de oralidade, para o aluno entender e
  aprender. Não aplica alteração no texto.
- **Modo ouro** — entra o texto do aluno, sai o texto revisto. Aplica correção.

Se o modo ouro entrega texto aplicado ou sugestão lado a lado, e quem assina o
resultado, é decisão em aberto — ver `docs/dados.md`. Nenhum dos dois modos toca
tese, argumento ou recorte sem autorização explícita: ver a lista do que não se
toca, também em aberto.

## 2. Tipos de documento

Iniciação científica · artigo (Qualis A1/A2) · dissertação de mestrado ·
tese de doutorado · relatório de pós-doutorado · capítulo de livro.

Cada tipo tem rubrica própria em `style/rubrics/`. Nunca aplicar rubrica genérica.

## 3. Eixos de avaliação — PROVISÓRIOS

1. Mérito científico e originalidade
2. Fundamentação teórica e diálogo com a bibliografia
3. Método e adequação das fontes (crítica documental / historiografia)
4. Estrutura argumentativa e coerência interna
5. Normalização (ABNT ou norma do periódico) e integridade das referências
6. Gramática, coesão e registro acadêmico
7. Aderência ao estilo de correção do professor

**Esta taxonomia foi escrita antes de ver o acervo. É hipótese, não fato.**
Serve como andaime para organizar a extração e nada mais. Se o método real do
professor usa outras categorias, elas vencem — a Sessão 0D compara as duas e a
Sessão 1 fixa a definitiva. Até lá, material que não couber aqui vai para
`corpus/achados-abertos.md`, nunca é forçado a caber.

O eixo 7 é o diferencial do projeto e tem peso igual aos demais na avaliação.

## 4. Pipeline

| Camada | Função | Modelo |
|---|---|---|
| C0 Ingestão | docx/pdf → estrutura canônica, IDs estáveis por unidade | — |
| C1 Determinística | referências órfãs, ABNT, ortografia, siglas, números | — |
| C2 Triagem | tipo de documento, mapa de seções, unidades de alto risco | Haiku 4.5 |
| C3 Análise | leitura crítica unidade a unidade, achados com evidência | Sonnet 5 |
| C4 Síntese | curadoria, hierarquização, parecer na voz do professor | Opus 5 |
| C5 Verificação | parecer vs. Style Card, nota + correções pontuais | Sonnet 5 |

C1 sempre roda antes das camadas com LLM. C5 tem no máximo 1 ciclo de reescrita.

**Regra dura:** Opus nunca lê o documento completo. C4 recebe achados, não texto bruto.
Passo com Opus acima de ~8k tokens de input = arquitetura errada, pare e revise.

Contratos de entrada/saída e schemas: `docs/arquitetura.md`.

### Obrigatório em toda chamada à API

- `cache_control` no bloco estável do system prompt (rubrica + Style Card + exemplares).
- Batch API para tudo não-interativo. C3 é sempre batch.
- `max_tokens` explícito e apertado. Output custa 5x o input.
- Extended thinking desligado por padrão. Só em C4, `budget_tokens` teto 2000.
  Tokens de thinking são cobrados como output.
- Cache local em disco por hash do input. Reexecutar o mesmo documento custa zero.
- Nenhuma execução inicia sem exibir estimativa prévia de custo.
- Toda execução grava tokens e US$ por camada em `costs/ledger.jsonl`.

Não estimar preços de memória — ler `docs/custos.md`, que tem data de verificação.

## 5. Modelos por sessão de desenvolvimento

Sonnet 5 é o default. Opus 5 é exceção justificada, não recompensa pela importância
do tema. O modelo que o PRODUTO usa numa camada (§4) não determina o modelo usado
para CONSTRUIR aquela camada — C4 roda em Opus, mas escrever o prompt de C4 é
trabalho de Sonnet.

| Sessão | Modelo | Razão |
|---|---|---|
| 0A–0D varredura do acervo | Sonnet 5 | leitura e classificação, não raciocínio profundo |
| 1 arquitetura | Opus 5 | única sessão cujo erro não se desfaz sem jogar código fora |
| 2 esqueleto + roteador | Sonnet 5 | scaffolding, padrão conhecido |
| 3 ingestão/parser | Sonnet 5 | escalar só se PDF virar patologia |
| 4 camada determinística | Sonnet 5 | regras explícitas, baixa ambiguidade |
| 5 destilação do corpus | Sonnet 5 | execução em massa é batch; gargalo é o corpus, não o modelo |
| 6 pipeline de análise | Sonnet 5 | integração, não invenção |
| 7 parecer + estilo | Sonnet 5 | entrega arquivos de prompt e cola; o Opus está no runtime |
| 8 avaliação/calibração | Sonnet 5 | rodar gold set e ler métricas é mecânico |

### Escalada para Opus

Escalar é resposta a evidência, nunca precaução. Só depois de Sonnet ter produzido
algo concreto e insuficiente, e com a insuficiência nomeada. Casos previstos:

- Sessão 5, se o Style Card sair genérico — sem léxico próprio, sem hierarquia
  de severidade reconhecível pelo professor.
- Sessão 8, se o gold set for mal e a causa não for óbvia. Diagnóstico, não execução.
- Qualquer sessão em que Sonnet errou duas vezes seguidas no mesmo ponto.

Ao escalar: abrir sessão nova só para o problema, com o contexto mínimo, e voltar
para Sonnet em seguida. Trocar de modelo no meio de uma sessão é sinal de que a
sessão tem tema demais.

## 6. Disciplina de sessão

Uma sessão = um tema. Assunto fora do tema vai para `docs/backlog.md` e **não é
executado**, mesmo que seja rápido, mesmo que eu peça no impulso — me lembre da regra.

Ao encerrar: gravar `docs/sessions/NN-<tema>.md` com decisões, entregáveis,
pendências, riscos abertos e custo da sessão.

## 7. Convenções técnicas

- Python 3.11+, `uv`, `ruff`, `pytest`.
- Sem framework de agentes. Chamadas diretas ao SDK `anthropic`.
- Prompts em `prompts/*.md`, versionados. Nunca hardcoded em `.py`.
- Artefatos de estilo (`style/style_card.md`, `style/rubrics/`, `style/exemplars/`)
  são editáveis pelo professor sem tocar em código. Tratar como interface de usuário.
- **Procedência sobrevive à destilação.** Todo item nesses artefatos carrega a
  origem: `[acervo:arquivo]`, `[diff:capítulo]`, `[entrevista]` ou `[INFERIDO]`.
  Quem edita precisa distinguir o que veio dele do que foi deduzido. Retrofit
  disso depois é caro; a regra vale desde o primeiro artefato gerado.
- Schema fixo de achado: `{id, unidade_id, eixo, gravidade, evidencia,
  diagnostico, sugestao, confianca}`.

## 8. Dados

Dois acervos distintos, com regras opostas:

- `corpus/prompts-christian/` — os prompts do professor. **Versionado no git.**
  Somente leitura: nunca editar, renomear ou reformatar. É material de origem.
- `data/` — trabalhos de alunos (manuscritos e versões corrigidas).
  **Nunca vai para o git**, está no `.gitignore`. Anonimizar autor e instituição
  na ingestão. Base de consentimento em `docs/dados.md`.

Quando este arquivo disser "corpus" sem qualificar, refere-se ao acervo de prompts.

## 9. Método de validação: três fontes

Todo item do Style Card, das rubricas e da calibragem de gravidade se valida
cruzando três fontes independentes:

- **Declarado** — acervo de prompts e entrevistas. O que ele diz que faz.
- **Praticado** — o diff do capítulo corrigido. O que ele aceitou de fato.
  Registra critério de aceitação, não geração espontânea: ele escolheu entre
  propostas da IA em vez de escrever do zero. Sinal legítimo, porém mais estreito.
- **Tácito** — o que só existe na divergência entre os dois.

**Divergência nunca é ruído a reconciliar em silêncio.** Declarado e ausente na
prática costuma ser aspiração; praticado e ausente no declarado é conhecimento
tácito, e é o material mais valioso do projeto. Toda divergência é registrada com
as duas versões e vai para o professor decidir. Nunca resolver por conta própria,
nunca escolher a versão mais plausível.

Vale para critérios, taxonomia, severidade, léxico e escopo. O que ele nunca
respondeu permanece marcado como aberto, não vira default silencioso.

## 10. Coleta pendente

`docs/coleta.md` registra o material que falta, de quem depende e o que bloqueia.
É dependência externa, não backlog: item bloqueante ali impede a sessão
correspondente de produzir resultado válido, mesmo que ela rode sem erro.
Consultar antes de iniciar qualquer sessão que dependa de corpus.

## 11. Verbosidade e economia de contexto

Princípio: **sucesso é silencioso, falha é detalhada.** O que importa vai para
disco, não para o chat. Disco é grátis, contexto não.

Reportar apenas: o que foi construído, o que exige decisão minha, e erros.

**Na sua saída**
- Não anunciar o que vai fazer. Fazer e reportar o resultado.
- Não recapitular meu pedido nem resumir o que acabou de escrever.
- Arquivo criado ou editado = uma linha: caminho + o que mudou. Não colar o conteúdo.
- Decisão tomada por conta própria = uma linha marcada `[ASSUMIDO]`.
- Sem preâmbulo, sem elogio ao pedido, sem fecho oferecendo próximos passos.

**Em comandos**
- `pytest -q --tb=line`. Rerodar em verbose apenas o teste que falhou.
- Saída potencialmente longa vai por `head`, `tail`, `grep` ou `wc`. Nunca despejar bruto.
- Não ler arquivo que você escreveu nesta sessão e não foi alterado por fora.
- Não listar diretório inteiro para checar se um arquivo existe — teste o caminho.
- Ao mostrar mudança em arquivo, mostrar só as linhas alteradas.

**Salvaguardas — o que nunca é suprimido**
- Erro real: stack trace completo, sem truncar. Diagnóstico ruim custa mais que tokens.
- Divergência entre o que eu pedi e o que você entendeu: sempre explicitar.
- Decisão que fecha porta futura: sempre explicitar antes de executar.
- Se você suprimiu algo e depois precisou dele, diga — o limite está errado, ajusto.

**Observabilidade fica em disco**
`costs/ledger.jsonl` é a fonte de verdade de gasto; consultar por agregação, nunca
imprimir o arquivo. Relatório de fim de sessão vai para `docs/sessions/NN-*.md`,
não para o chat — no chat, só o caminho do arquivo gravado.
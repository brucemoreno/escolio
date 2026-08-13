# X02 — Revisão editorial de capítulo de livro autônomo

Formalização de 2026-08-13, decisão autoral do `USUARIO_PROPONENTE`, registrada em
`CLAUDE.md §13` item 3 e aqui em especificação intermediária — não cadastral, ainda sem
pipeline de etapas. Resolve a lacuna ontológica identificada em `CLAUDE.md §3`/§13 ("capítulo de
livro não tem função nem candidatura"), sem abrir camada numérica nova e sem criar segunda
arquitetura paralela às cinco funções + X01 já existentes.

**Nenhum código foi escrito nesta sessão.** Esta função é `[PROPOSTA]` autoral — não há fonte
homologada (P00-P22, R03) que a preveja; o catálogo de seis funções é fechado e ampliá-lo exige
"nova fonte e decisão autoral específica" [`LAC-P02-005`], que é exatamente o que este documento
registra.

---

## 1. ID

**X02.** Segue o precedente de X01 [`R03 CAMADA B`, item 6] — função transversal fora da
sequência numérica P10-P14, sem adulterar o catálogo fechado de `FUNCAO`. A camada `FUNCAO`
termina em P14 [inventário canônico da R03: P15 `PROFILES`, P16 `CONTEXTOS_GEOGRAFICOS`, P17
`CONTEXTOS_TEMPORAIS`, P18 `INTERSECOES`] — não há vaga numerada ali para uma sexta
macrofunção; X01/X02 são o mecanismo já aceito para função que não cabe nessa sequência, não uma
segunda exceção inventada agora.

## 2. Nome

**X02 — Revisão editorial de capítulo de livro autônomo.**

## 3. Escopo, em uma frase

Revisar um capítulo cujo destino final é permanecer como capítulo de livro, preservando sua
função autoral e editorial, e não convertê-lo em artigo ou outro gênero derivado.

## 4. Distinção explícita de P10

`P10` (Derivação editorial de capítulo em artigos) recebe capítulo de livro como **entrada** —
matéria-prima para extrair artigo(s); o capítulo não é o produto final do P10, é o que se
transforma. **X02 trata o capítulo como produto final** — a revisão preserva o capítulo como
capítulo, sem produzir derivação de gênero. Um mesmo capítulo pode, em princípio, ser objeto de
P10 (se alguém quiser extrair artigo dele) e de X02 (se o objetivo é revisá-lo para permanecer
capítulo) em momentos diferentes — as duas funções não competem pelo mesmo objeto porque
respondem a intenções editoriais diferentes; `classification.functions` [P09 §6] declara qual
delas se aplica em cada execução, nunca as duas ao mesmo tempo sem distinção de propósito.

## 5. Entradas mínimas

Nenhuma fonte enumera entradas mínimas para X02 (é função nova). Por analogia mínima com o que
já existe e é exigido de todo `InputItem` [P09 §6] + o que X01 já processa para qualquer função
(fontes, citações, suficiência de evidência):

- o capítulo em si (`.docx`/`.pdf`, via `escolio/ingestao/`), já estruturado em unidades
  (parágrafo, citação recuada, nota de rodapé, comentário do Word — todo o inventário que
  `escolio/ingestao/parser_docx.py` já produz);
- `classification.functions=["X02"]` declarado por ato humano [P09 §6, mesmo padrão de BL-014] —
  X02 não infere sua própria elegibilidade a partir do conteúdo;
- perfil de voz do autor avaliado, quando disponível [P07, mesma entrada que P13 já usa] — não
  obrigatório para diagnóstico, mas necessário para qualquer avaliação de "compatibilidade com a
  voz autoral" exigida pela decisão 3 de `conversao-citacao-bibliografica.md` antes de qualquer
  aplicação material.

**Não incluído aqui, por instrução explícita desta rodada**: lista completa e fechada de
entradas mínimas (o padrão de 20 `ENTRADAS_MINIMAS` que P11 declara, por exemplo) — isso
pertence ao pipeline detalhado, fora de escopo desta formalização.

## 6. Teto de intervenção

**Base: `PROPOSTA`/INT-05**, mesmo teto de P13 [`CLAUDE.md §6`, `P13 §4.4`] — observar,
diagnosticar, sinalizar, recomendar, propor. X02 não herda, por existir, nenhuma autorização de
`EDICAO_LOCAL`/`REESCRITA`/qualquer nível acima de `PROPOSTA` — nenhum nível de intervenção se
infere de nível inferior [`P06 §1, §7`].

**Alteração material que ultrapasse diagnóstico** (ex.: a conversão citação-direta→paráfrase
especificada em `docs/spec/conversao-citacao-bibliografica.md`) continua condicionada
integralmente às precondições/gates **já estabelecidos na decisão 3** daquele documento — X02
não cria segundo regime de autorização, usa o mesmo. Isso responde diretamente ao bloqueio
registrado ali (`§4`, "não existe módulo com autoridade de aplicar"): **X02 é essa peça que
faltava** — agora existe função com objeto declarado (capítulo de livro) apta a hospedar o gate
por classe já decidido, sem precisar pedir emprestado a autoridade de P11 nem inventar
"executor técnico equivalente" (explicitamente vetado na decisão 3).

## 7. Precondições/gates para qualquer aplicação material

Nenhum gate novo é criado nesta rodada. X02 usa integralmente:

- as precondições cumulativas da decisão 3 [`conversao-citacao-bibliografica.md §3(a)`] para
  conversão citação-direta→paráfrase (classificação segura como `REFERENCIA_BIBLIOGRAFICA`,
  detecção segura de citação direta, ausência de necessidade analítica da literalidade,
  preservação de significado/atribuição/voz, registro reversível);
- as cinco exceções da mesma decisão (literalidade analisada substantivamente, conceito/definição
  em discussão, epígrafe, ambiguidade de classificação, falha de equivalência semântica) —
  qualquer uma delas força `PRESERVE_AND_FLAG`, nunca `AUTO_APPLY`, também dentro de X02;
- a autorização de classe (não por instância) já registrada pelo `USUARIO_PROPONENTE` na decisão
  3 — vale para X02 da mesma forma que valeria para qualquer módulo com teto compatível;
- `InterventionRecord` [`P09 §13`] como registro de rastreabilidade/reversibilidade — sem
  estrutura nova.

**Explicitamente fora desta rodada, por instrução do `USUARIO_PROPONENTE`:**

- pipeline detalhado de etapas (quantas, nomes, ordem) — X02 não tem espinha própria ainda;
- novos níveis de intervenção além de `PROPOSTA`/INT-05 como teto-base;
- novos gates, além dos já existentes na decisão 3, para os casos que eles já cobrem;
- qualquer expansão de catálogo além de X02 (relatório de pós-doutorado continua sem função,
  não tratado aqui — `CLAUDE.md §13` item 3).

## 8. O que esta formalização resolve, e o que continua aberto

**Resolve**: a lacuna ontológica — capítulo de livro agora tem função declarável
(`classification.functions=["X02"]`), com nome, escopo, distinção de P10, e teto de intervenção
herdado sem invenção de regime novo. O bloqueio de execução registrado em
`conversao-citacao-bibliografica.md §4` ("não existe módulo com autoridade de aplicar") deixa de
ser verdade no sentido ontológico — a função existe.

**Não resolve, e não foi pedido para resolver nesta rodada**: nenhuma linha de código foi escrita
para X02 — não há módulo em `escolio/funcoes/`, não há `execucao_x02.py`, não há ponte de
modelo. A aplicação material de qualquer conversão continua, na prática, impossível até que esse
módulo seja construído — a formalização remove o obstáculo *normativo* (função inexistente), não
o obstáculo de *implementação* (código inexistente). São bloqueios de natureza diferente, mesma
distinção já usada em `docs/spec/mapa-P08.md §6` para P08/P19.

Próximo passo, quando decidido: confrontar X02 com os documentos existentes (P10, P13, X01) para
decidir se X02 precisa de pipeline próprio ou reutiliza componentes já definidos — explicitamente
não decidido aqui.

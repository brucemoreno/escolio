# Conversão de citação direta de referência bibliográfica em paráfrase — especificação, não construída

Origem: sessão de 2026-08-13, motivada por relato do professor sobre o motor de busca de
referência no Drive (ver `docs/spec/verificacao-leitura-drive.md`) — a pergunta de quando o
sistema deve buscar uma referência "melhor" para fortalecer um argumento levou a três decisões
autorais encadeadas, registradas aqui no mesmo formato usado para o P08
(`docs/spec/mapa-P08.md §6.1`): **(a) regra documental obrigatória · (b) decisão técnica aberta
· (c) revisão humana.**

**Nenhum código foi escrito nesta sessão.** Todas as decisões abaixo são `[PROPOSTA]` autoral do
`USUARIO_PROPONENTE`, sem precedente em fonte homologada — busca exaustiva feita nesta mesma
sessão contra `P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md`, o pacote P04/BVAA
completo, P07, os 13 arquivos de R03 e todos os mapas de `docs/spec/` não encontrou nenhuma das
três regras já especificadas. O único ancestral textual é um rascunho pré-P13 descartado
(`corpus/historico/acervo-antigo/.../BALEIA_DERIVA_v1RC.txt §23`), não homologado, citado aqui só
como referência histórica de intenção, nunca como fonte normativa.

---

## 1. Decisão 1 — fronteira `REFERENCIA_BIBLIOGRAFICA` vs. `FONTE_DOCUMENTAL`

**(a) Regra documental, registrada agora como decisão autoral, não extraída de fonte prévia:**

A fronteira relevante não é citação direta vs. paráfrase — é o **papel que a fonte exerce no
texto**:

- **`FONTE_DOCUMENTAL`** — documento que é objeto de análise historiográfica do próprio trabalho
  (carta, manuscrito, relato de época, registro primário interpretado pelo autor). Permanece
  `FONTE_DOCUMENTAL` mesmo quando parafraseada — o critério é a função, não a forma de citação.
- **`REFERENCIA_BIBLIOGRAFICA`** — literatura empregada para sustentar, situar ou interpretar o
  argumento (historiografia secundária, teoria, metodologia).

**Regra**: `PARAFRASE_DE_FONTE_DOCUMENTAL` nunca aciona busca de referência melhor. O gatilho de
busca/comparação bibliográfica incide só sobre `REFERENCIA_BIBLIOGRAFICA` — citada direta ou
parafraseada, tanto faz; o que importa é a classe da fonte, não a forma da citação.

**(b) Decisão técnica aberta**: como o classificador (determinístico ou por julgamento de
modelo) decide, para uma citação real, se a fonte por trás dela é `FONTE_DOCUMENTAL` ou
`REFERENCIA_BIBLIOGRAFICA`. Não é uma classificação estrutural (a mesma obra pode ser
documental num capítulo e bibliográfica em outro, dependendo do uso) — fica dependente de
julgamento contextual do modelo sobre a função da citação no texto, com o mesmo padrão de
`confidence` já especificado em `docs/spec/verificacao-leitura-drive.md §5` para não tratar
julgamento incerto como fato.

---

## 2. Decisão 2 — critério de "referência melhor"

**(a) Regra documental, registrada agora:**

`MAIS_RECENTE != MELHOR`. Referência melhor é a **mais adequada à afirmação específica e à
função historiográfica, teórica ou metodológica que deve desempenhar** — não a mais nova por
padrão. Atualidade cronológica recebe peso especial só quando a natureza da afirmação exige
atualização (ex.: dado empírico que envelhece; não se aplica igual a interpretação
historiográfica, que não "vence" por ser mais recente).

**Limite de ação, já coerente com o teto existente do P13** (`CLAUDE.md §6`, INT-05
`PROPOSTA`): o sistema pode `LOCALIZAR + COMPARAR + JUSTIFICAR + SINALIZAR`. **Não deve
substituir automaticamente** referência substantiva quando a troca puder alterar o argumento, a
interlocução historiográfica ou o enquadramento teórico — essa parte permanece proposta, nunca
aplicação, independente da decisão 3 abaixo (que trata de um caso mais restrito: substituição
formal de citação direta por paráfrase, não troca de qual obra é citada).

**(b) Decisão técnica aberta**: não há fórmula para "adequação funcional" — é julgamento
qualitativo do modelo, mesma disciplina que `P13 §11/§12` já aceita para criticidade/seletividade
("não pode ser reduzida a contagem mecânica"). Nenhum valor numérico ou peso concreto é proposto
aqui.

---

## 3. Decisão 3 — conversão automática de citação direta de referência bibliográfica em paráfrase

**(a) Regra documental, registrada agora — a mais operacional das três:**

Regra geral: `AUTO_APPLY`. Exceção: `PRESERVE_AND_FLAG` ou abstenção.

**Precondições cumulativas para aplicação automática:**
- classificação segura como `REFERENCIA_BIBLIOGRAFICA` (decisão 1) — nunca `FONTE_DOCUMENTAL`;
- detecção segura de citação direta (não paráfrase já existente);
- ausência de necessidade analítica da literalidade;
- preservação de significado;
- preservação de atribuição e referência;
- compatibilidade com a voz autoral;
- registro reversível da alteração.

**Exceções — nunca auto-aplicar, preservar e sinalizar:**
- literalidade analisada substantivamente pelo próprio autor (a citação exata é objeto de
  discussão, não só suporte);
- conceito/definição/formulação cuja redação é objeto da discussão;
- epígrafe ou outra função textual especial;
- ambiguidade de classificação (não deu para decidir com segurança se é `REFERENCIA_BIBLIOGRAFICA`
  ou `FONTE_DOCUMENTAL`, ou se é citação direta);
- falha de equivalência semântica (a paráfrase candidata não preserva o sentido).

**Gate — decidido, forma pouco usual, registrada com precisão:** o gate humano **não ocorre por
instância**. O `USUARIO_PROPONENTE` autoriza expressamente, aqui, a **classe delimitada de
intervenção** `CITACAO_DIRETA_DE_REFERENCIA_BIBLIOGRAFICA → CONVERSAO_EM_PARAFRASE`. Essa
autorização de classe satisfaz `GATE_HUMANO_EXPRESSO` [`P06/02`, `CLAUDE.md §6`] para toda
instância que cumpra integralmente as precondições acima — o gate é expresso (dado por escrito,
nesta decisão), só não é repetido por instância. Nenhuma fonte proíbe esse desenho; nenhuma fonte
o autoriza previamente — é decisão nova, dentro da autoridade do `USUARIO_PROPONENTE`
[`CLAUDE.md §1`], não inferência de nível superior a partir de nível inferior [`P06 §1, §7`].

**Isto não eleva o teto do P13.** P13 permanece limitado a `PROPOSTA` — ele detecta, classifica,
propõe. A aplicação material é executada por módulo de nível `P06` compatível (`EDICAO_LOCAL`/
`REESCRITA` autorizado), hoje associado a P11 quando o material é dissertação/tese. "Executor
técnico equivalente" **não é fonte autônoma de autoridade** — não existe módulo genérico que
herde autoridade de aplicação por analogia técnica com P11.

Toda aplicação deve ser rastreável, reversível e preservar o original — mapeamento direto para
`InterventionRecord` já existente [`P09 §13`]: `requested_level`/`applied_level`/`disposition`,
sem necessidade de estrutura nova.

**(b) Decisão técnica aberta:**
- Onde vive o registro de "autorização de classe" no código — um objeto de configuração único
  por execução, um campo no envelope P09, ou outro mecanismo. Não decidido aqui.
- Como o classificador mede "ausência de necessidade analítica da literalidade" e "compatibilidade
  com a voz autoral" com confiança suficiente para autoaplica — critério qualitativo, mesmo
  raciocínio da decisão 2, sem fórmula proposta.
- Threshold de confiança abaixo do qual uma instância que "parece" cumprir as precondições cai em
  `PRESERVE_AND_FLAG` por segurança, em vez de autoaplicar — não fixado, mesma disciplina de não
  inventar constante sem calibração (`docs/spec/verificacao-leitura-drive.md §4`).

**(c) Caso que exige revisão humana:**
- Toda instância que caia em qualquer uma das cinco exceções listadas acima.
- Toda instância em que o classificador não tenha confiança suficiente nas precondições
  cumulativas (ainda que nenhuma exceção nomeada se aplique — dúvida residual não é a mesma coisa
  que exceção nomeada, e ambas levam a `PRESERVE_AND_FLAG`).

---

## 4. Bloqueio de execução para o material desta sessão — capítulo de livro

**Atualização (2026-08-13, mesma sessão): a função foi formalizada — `X02`, ver
`docs/spec/funcao-x02-capitulo-livro.md`.** O bloqueio *normativo* descrito originalmente aqui
("não existe módulo com autoridade de aplicar") deixa de valer: X02 existe, com teto
`PROPOSTA`/INT-05 herdado de P13 e as mesmas precondições/gates desta decisão 3 aplicáveis a
qualquer aplicação material.

**O que continua bloqueado, por natureza diferente**: X02 é formalização normativa apenas —
nenhum módulo em `escolio/funcoes/`, nenhuma etapa, nenhuma ponte de modelo. Para o material
real desta sessão (`data/capitulos/`), a aplicação material da conversão citação-direta→paráfrase
continua impossível na prática — não por falta de função (resolvido), mas por falta de código
(não construído, não pedido nesta rodada). P13 pode analisar, diagnosticar e propor hoje, dentro
do seu próprio teto; X02 herda o mesmo teto para quando existir implementação.

---

## 5. Registro de decisão desta sessão

- Nenhum código foi escrito ou alterado.
- `CLAUDE.md §13` item 3 atualizado para refletir a resolução parcial (capítulo de livro resolvido;
  relatório de pós-doutorado continua em aberto, não tratado por esta decisão).
- As três decisões (fronteira documental/bibliográfica, critério de "melhor", gate por classe)
  são `[PROPOSTA]` autoral, sem precedente homologado, registradas para orientar implementação
  futura — bloqueadas de aplicação material para capítulo de livro até a função existir.

# LACUNAS — schema P13Comment (sessão 1)

Lacunas encontradas na implementação de `escolio/comentarios/`, sessão 1 do
`docs/spec/plano-P13.md`. Nenhum item aqui foi resolvido por inferência.

## Tipagem adiada para sessões próprias

`P13Comment` implementa os 24 campos de §31.5, mas só tipa fortemente os
quatro campos que são o tema da sessão 1: `status` (`P13CommentStatus`),
`resolution` (`P13CommentResolution`), `related_comment_id` e
`matrix_comment_id`. Os demais permanecem `str` (ou `bool` para
`reversible`) porque sua tipagem própria é o entregável de outra sessão do
plano, e tipar agora seria antecipar decisão de sessão futura:

- `comment_type` — catálogo de 15 tipos [§13, §15-18] é a sessão 3. Os
  únicos dois valores usados nesta sessão (`REMISSAO_A_COMENTARIO_MATRIZ`,
  `COMENTARIO_MATRIZ`) são citação literal de §31.5.4, não o catálogo
  inteiro.
- `priority`, `severity` — escalas próprias do P13 [§14.1, §14.2, CLAUDE.md
  §7 "cinco escalas graduadas"] são a sessão 2 (matriz de criticidade e
  seletividade).
- `intervention_level`, `authority_required`, `gate`, `voice_impact` —
  integração P06/P07 é a sessão 5. `intervention_level` poderia reusar
  `NivelIntervencao` (`escolio/intervencao/niveis.py`) sem duplicar enum,
  mas essa integração de fato pertence à sessão 5, não a esta.
- `source_status` — integração P04/P05 (BVAA) é a sessão 4.
- `privacy_classification` — sessão adiada (integração P08), ver
  `docs/spec/plano-P13.md` §"Sessão adiada".
- `anchor_start`, `anchor_end` — a fonte não declara tipo (nem inteiro nem
  string) para os dois; mantidos `str` para não inventar um formato de
  offset que a fonte não especifica.

## Regras de §31.5.3/§31.5.4 não verificáveis com o schema mínimo

- **`related_comment_id` "obrigatório quando o comentário for resposta,
  continuação, desdobramento ou dependência direta de outro comentário"**
  [§31.5.3] — o schema mínimo de §31.5 não tem campo que declare essa
  natureza de relação (não existe `relation_kind` ou equivalente). Sem um
  campo que sinalize "isto é resposta/continuação/desdobramento", a
  obrigatoriedade condicional não é verificável em código; não inferida.

- **Exceção "salvo relação entre versões expressamente rastreada"**
  [§31.5.3] — mesma limitação: não há campo que marque uma relação entre
  versões como "expressamente rastreada". `RegistroDeComentarios` aplica
  sempre a regra geral (mesmo `document_id`/`document_version`); a exceção
  nunca é aplicável neste código porque não há como declará-la.

- **`matrix_comment_id` "pode ser obrigatório para comentário individual
  coberto por matriz quando a rastreabilidade exigir vínculo explícito"**
  [§31.5.4] — condicional (“pode ser”, "quando exigir") sem critério
  determinístico na fonte. Não implementado; só a obrigatoriedade
  incondicional (`comment_type=REMISSAO_A_COMENTARIO_MATRIZ`) é verificada.

## Fora de escopo desta sessão, não lacuna

- Unicidade de `comment_id` — `RegistroDeComentarios` não rejeita
  `comment_id` duplicado. Diferente de `claim_id`/`source_id`
  (`escolio/identificadores.py`, RC-016), nenhuma regra do P13 citada em
  §31.5/§42 estende o protocolo de identificadores P05 a `comment_id`;
  estender por analogia seria inferência.
- `P13CommentReferral`, `criticality_matrix`, `selectivity_matrix`,
  catálogo de 15 `comment_type`, integrações P04/P06/P07/P08, envelope
  `P13RequestExtension`/`P13ResultExtension` — sessões 2 a 10 do plano.

## Sessão 2 — matriz de criticidade e matriz de seletividade

`escolio/comentarios/criticidade.py` (`MatrizCriticidade`, `EixoCriticidade`,
`ClasseCriticidade`) e `escolio/comentarios/seletividade.py`
(`MatrizSeletividade`, `ordenar_por_criticidade`, `aplicar_selecao`)
implementam §11 e §12. Sem chamada a LLM nesta sessão — a classificação é
estrutura de dados e validação de forma, não julgamento automático.

### Não é lacuna — decisão de design exigida pela fonte

- **Não existe função que derive `MatrizCriticidade.classe` a partir de
  `avaliacao_por_eixo`.** "A matriz não pode ser reduzida a contagem
  mecânica" [§11] proíbe exatamente esse tipo de função; `classe` é sempre
  campo declarado por quem avalia. Isto não é lacuna — é a leitura literal
  da proibição.
- **`aplicar_selecao` não aceita `quota_percentual`/`quota_quantidade`
  como critério de seleção** — só os aceita para rejeitá-los
  [§34.3-34.4]. Não existe caminho de código que aplique um percentual ou
  quantidade fixa; isso é o requisito de TA13-16, não uma omissão.

### Tipagem adiada para sessões próprias

Nove dos dez fatores de `MatrizSeletividade` que não são `criticality`
(`material_impact`, `novelty`, `recurrence`, `matrix_comment_coverage`,
`actionability`, `evidence_sufficiency`, `human_decision_required`,
`privacy_risk`, `selection_rationale`) permanecem `str`. §12 lista os
nomes dos campos, sem declarar tipo (nem enum, nem booleano) para nenhum
deles — inclusive `human_decision_required` e `privacy_risk`, cujo nome
sugeriria booleano por analogia com `reversible` (sessão 1), mas analogia
não é declaração da fonte. Tipar agora seria inferência.

**`selection_decision` — RESOLVIDO em BL-023.** Diferente dos nove acima,
o §10 enumera os oito resultados da etapa de seleção
(`COMENTAR`, `NAO_COMENTAR_SEM_PROBLEMA_MATERIAL`,
`NAO_COMENTAR_POR_REPETICAO`, `REMETER_A_COMENTARIO_MATRIZ`,
`AGUARDAR_EVIDENCIA`, `AGUARDAR_GATE`, `ABSTER_SE`, `BLOQUEADO`) — a fonte
existe, só não tinha virado enum. `SelectionDecision` (`seletividade.py`)
fecha os oito valores; `MatrizSeletividade.selection_decision` exige
membro do enum, não string livre. `SELECTION_DECISION_NAO_COMENTAR_SEM_PROBLEMA_MATERIAL`
permanece como alias do membro homônimo, por compatibilidade com
`§45/PS13-01`.

### Fora de escopo desta sessão, não lacuna

- Catálogo dos 15 `comment_type`, integração com `P13Comment.priority`/
  `severity` (que permanecem `str` em `comentario.py`), comentário-matriz e
  remissões — sessões 3 e 6 do plano.

## Sessão 3 — catálogo dos 15 tipos de comentário e templates estruturais

`escolio/comentarios/tipos.py` implementa `CommentType` (os 15 valores de
§13) e os quatro templates estruturais que a fonte declara dentro de
§15-18: `TemplateComentarioLinguistico` (§15), `TemplateAlertaEstrutural`
(§16), `TemplateAlertaArgumentativo` (§17), `TemplateAlertaMetodologico`
(§18). Sem chamada a LLM — mesma disciplina da sessão 2: validação de
forma, não julgamento automático de qual tipo/template usar para um
diagnóstico concreto.

### Não é lacuna — leitura literal do catálogo

- **Nenhum `CommentType` corresponde a "comentário linguístico".** §13
  enumera 15 tipos; nenhum se chama `ALERTA_LINGUISTICO` ou
  `COMENTARIO_LINGUISTICO`, e nenhuma seção da fonte declara qual dos 15
  tipos deve ser usado para veicular o template de §15.
  `TemplateComentarioLinguistico` por isso não está em `_TEMPLATE_POR_TIPO`
  e não é alcançável por `valida_template_por_tipo` — só existe como função
  de validação avulsa. Associar por analogia a `DIAGNOSTICO` ou
  `CORRECAO_LOCAL` seria inferência, mesmo padrão recusado para
  `intervention_level`/`priority` na sessão 1.
- **§18 (comentário metodológico) não declara lista de campos** como
  §16/§17 fazem ("deve indicar"/"deve distinguir"). Só enumera oito
  condições de aplicabilidade e uma disjunção fechada de ação ("decisão
  necessária" ou "solicitar explicitação"). `TemplateAlertaMetodologico`
  tipa exatamente isso (`CondicaoMetodologica`, `AcaoMetodologica`) e não
  inventa campos livres (`problem`, `recommended_action`) que a fonte não
  nomeia para esta seção especificamente.
- **`solucao_factual_inventada` em `TemplateAlertaArgumentativo`** cita o
  invariante 21 (§3, "comentário não pode inventar solução factual"), não
  uma frase literal de §17 — §17 não repete essa proibição, mas o
  invariante geral se aplica a qualquer comentário e o critério de falha
  de TA13-08 ("solução factual inventada") o torna verificável aqui.

### Fora de escopo desta sessão, não lacuna

- `ALERTA_DE_EVIDENCIA` [§20] e `ALERTA_BIBLIOGRAFICO` [§19] — templates
  próprios fora de §15-18; sessão 4 do plano (testes TA13-10, TA13-11).
- `ALERTA_DE_VOZ` [§21] — sessão 5.
- `ALERTA_DE_PRIVACIDADE` [§22] — sessão adiada (integração P08).
- `COMENTARIO_MATRIZ` / `REMISSAO_A_COMENTARIO_MATRIZ` — template próprio
  em §23; sessão 6.
- `DIAGNOSTICO`, `CORRECAO_LOCAL`, `SUGESTAO`, `PERGUNTA_ORIENTADORA`,
  `GATE_HUMANO`, `DECISAO_PENDENTE` — catalogados em `CommentType`, sem
  template estrutural declarado em nenhuma seção da fonte; nenhuma sessão
  do plano os atribui a uma seção específica.
- Retipar `P13Comment.comment_type` (sessão 1, `comentario.py`) de `str`
  para `CommentType` — não pedido nesta sessão e alteraria código
  existente; ver `docs/backlog.md` se uma sessão futura exigir.

**Vínculo entre `MatrizCriticidade.problem_id` e
`MatrizSeletividade.candidate_problem_id` — RESOLVIDO em BL-024.** A nota
anterior aqui dizia que a ausência de checagem não era lacuna, por não
haver regra de integridade referencial citada em §11/§12. O teste de
integração de 2026-08-09 mostrou a consequência prática: nada impedia
`criticality` de divergir da `classe` que a `MatrizCriticidade` referenciada
de fato declarou. `exige_referencia_valida_a_criticidade` (`seletividade.py`)
fecha isso — confere que `candidate_problem_id` aponta para uma
`MatrizCriticidade` existente e que `criticality` bate com `classe` —, sem
inventar regra de fonte: é checagem de consistência entre dois objetos que
o próprio código já constrói, não uma nova exigência de conteúdo.

## Sessão 4 — integração P04 (BVAA)/P05 no comentário [§19, §20, §26, §27]

`escolio/comentarios/aplicacao_p04_p05.py` implementa o adaptador que lê o
estado do BVAA (`EstadoBibliografico`) e da relação P05
(`RelacaoAfirmacaoEvidencia`) e popula `source_status` [§19, §31.5] no
`P13Comment`, mais `claim_id`/`evidence_ids` no schema mínimo próprio de
§27 (`AplicacaoP05DoComentario`). `P13Comment` não foi alterado —
`source_status` continua `str`; o módulo valida antes de gravar.

### CON-P05-001 — permanece aberto, não resolvido aqui

- **`SourceStatusComentario` é um quarto vocabulário, não fundido aos
  outros três.** Os 9 estados literais de §19 ("fonte identificada" …
  "sustentação não liberada") não são `EstadoBibliografico` (P04, 17
  estados), não são `AccessState`/`ReadingState`/`ValidationState` (P05) e
  não são os 9 estados mínimos de R03 CAMADA D — mesma disciplina de
  `escolio/bvaa/correspondencia.py` (LAC-BVAA-001).
- **Nenhuma função deriva `SourceStatusComentario` a partir de
  `EstadoBibliografico`.** Nenhuma fonte declara essa correspondência
  (diferente da tabela de `escolio/bvaa/correspondencia.py`, que cobre P04
  × R03 × P05 mas nunca cita os rótulos de §19). Construir essa derivação
  seria inventar uma quinta linha de correspondência não pedida nesta
  sessão. Em vez disso, `valida_source_status_compativel_com_bvaa` inverte
  o problema: recebe os dois valores já decididos por quem comenta e
  **rejeita** quando o `SourceStatusComentario` afirma mais do que o
  `EstadoBibliografico` atual sustenta [§26]. Nunca escolhe nem corrige o
  valor.
- **O requisito mínimo por status (`_REQUISITO_MINIMO`) é decisão de
  implementação, não citação literal.** A fonte não numera qual estado
  BVAA cada um dos 9 rótulos de §19 exige — só declara, em prosa, que
  "sem acesso verificável" bloqueia leitura/passagem/página/sustentação
  específica [§26] e que "conferido" não pode ser declarado com a fonte
  "apenas localizada" [§19]. O mapeamento de cada rótulo ao nó mínimo da
  máquina BVAA (`ACESSADA` para leitura/passagem/abertura, `PAGINA_CONFIRMADA`
  para página, `VALIDADA` para sustentação específica) é a leitura mais
  literal possível dessas duas frases, verificada com os cenários PS13-05
  e PS13-06 [§45]; não é uma "sexta linha" da tabela de correspondência
  porque não afirma equivalência de estado, só ordem mínima exigida.

### Fora de escopo desta sessão, não lacuna

- **"não confirma imagem" [§26]** — nenhum campo de `P13Comment` [§31.5]
  ou do schema de §19 representa "imagem"; a regra não tem onde ser
  verificada em código nesta sessão. Não implementada.
- **Agregação de múltiplas `RelacaoAfirmacaoEvidencia` para a mesma
  `claim_id`** — `construir_aplicacao_p05` aceita no máximo uma relação por
  chamada; isto é `LAC-P05-003` (`escolio/LACUNAS.md`), lacuna já aberta,
  não resolvida aqui.
- **Tipo de `verification_status` [§27]** — a fonte não declara enum para
  este campo. Reusa `ValidationState` (P05) apoiado na frase literal de
  §4.3 ("O P13: indica estado de verificação"), não em correspondência de
  nome de campo — documentado como decisão, não como lacuna, porque há uma
  frase da fonte que a sustenta.
- Integrações P06/P07 (`intervention_level`, `authority_required`, `gate`,
  `voice_impact`) e P08 (`privacy_classification`) — sessões 5 e adiada do
  plano; não tocadas aqui.

## Sessão 5 — integração P06 (níveis de intervenção)/P07 (voz autoral) [§4.4, §4.5, §28, §29]

`escolio/comentarios/aplicacao_p06_p07.py` implementa o adaptador que valida
e popula `intervention_level`, `gate` e `voice_impact` no `P13Comment`.
`P13Comment` não foi alterado — os três campos continuam `str`; o módulo
valida antes de gravar, mesmo padrão da sessão 4. Nenhuma chamada a LLM.

### CLAUDE.md §6 ("P13 para em SINALIZACAO/RECOMENDACAO") — leitura, não citação literal

Verificado contra a fonte: **não é frase literal do contrato P13.** §4.4
lista "o comentário pode: observar; diagnosticar; sinalizar; recomendar;
propor" — cinco verbos, correspondentes a `OBSERVACAO, DIAGNOSTICO,
SINALIZACAO, RECOMENDACAO, PROPOSTA` (`NivelIntervencao`, INT-01 a INT-05).
O teto real do contrato é **PROPOSTA (INT-05)**, um nível acima de
`RECOMENDACAO` citado no CLAUDE.md. `NIVEIS_PERMITIDOS_P13` implementa os
cinco, não os dois — a leitura do CLAUDE.md §6 é uma simplificação
(provavelmente por PROPOSTA raramente aparecer em exemplo), não um erro
que este módulo deveria repetir. Registrar aqui para quem ler o CLAUDE.md
sem cruzar com a fonte.

### Leitura fechada de §4.4 — não é lacuna, é a leitura mais literal

§4.4 nomeia cinco verbos permitidos e onze proibidos ("executar reescrita;
fundir; cortar; substituir; reorganizar; alterar dado; alterar argumento;
alterar corpus; alterar método; alterar objetivo; alterar conclusão"), dos
quais cinco correspondem a nomes de nível (`REESCRITA`, `FUSAO`, `CORTE`,
`SUBSTITUICAO`, `REORGANIZACAO`) e seis a ações de conteúdo (cobertas pelo
catálogo de gates de §32.2, não por um nível). Isso deixa cinco níveis da
cadeia de 15 sem menção em nenhuma das duas listas: `SIMULACAO`,
`EDICAO_LOCAL`, `VALIDACAO`, `HOMOLOGACAO`, `ABSTENCAO`.
`valida_intervention_level_permitido` trata a lista "pode" como exaustiva
(fechada) e rejeita os cinco não nomeados junto com os explicitamente
proibidos — mesma disciplina de `escalonamento_permitido`
(`escolio/intervencao/niveis.py`, "somente estas existem") e do
invariante do CLAUDE.md §8 ("só as transições listadas existem na máquina
de estados"). Alternativa rejeitada: tratar os cinco não nomeados como
"indeterminado, aceitar por ausência de proibição explícita" — isso
inverteria o ônus da prova que o resto do projeto aplica consistentemente
(nada é permitido por omissão).

### `authority_required` — não retipado, vocabulário fechado ausente na fonte

Diferente de `gate` (§32 nomeia 17 tokens em `SCREAMING_SNAKE_CASE`, um
catálogo controlado verificável) e de `intervention_level` (reusa
`NivelIntervencao`, já um enum de outra peça), `authority_required` não
tem catálogo fechado de tokens em nenhuma seção da fonte. A única tabela
candidata é §5 ("PERFIS, AUTORIDADES E RESPONSABILIDADES"), mas sua coluna
`Perfil` é prosa em português ("Bolsista ou estudante",
"Usuário-proponente"), não vocabulário controlado — diferente de §13/§32,
onde os próprios rótulos já vêm em formato de token. Tipar `authority_required`
a partir de §5 exigiria inventar um formato de token que a fonte nunca
declarou para este campo — mesma inferência já recusada para os nove
fatores de `MatrizSeletividade` (sessão 2) e para a associação
tipo-de-comentário/template em §15 (sessão 3). Permanece `str`, validado
apenas quanto à obrigatoriedade em `comentario.py` (sessão 1).

### `voice_impact` reusa `ResultadoDeFidelidade` (P07) — decisão, não fusão

§4.5: "O P13: aplica P07; registra impacto sobre voz." `ResultadoDeFidelidade`
(`escolio/voz/vocabulario.py`) é literalmente o resultado que o protocolo
de avaliação de fidelidade autoral do P07 já produz para o impacto de um
texto candidato sobre a voz do autor avaliado — mesma disciplina da sessão
4, que reusou `ValidationState` para `verification_status` apoiada em uma
frase equivalente de §4.3. Não fundido com nenhum dos outros vocabulários
de status já catalogados em CLAUDE.md §7.

### Regras verificáveis implementadas

- `§28` — "`CORRECAO_LOCAL` não autoriza reescrita forte":
  `valida_correcao_local_nao_autoriza_reescrita_forte` rejeita
  `comment_type=CORRECAO_LOCAL` com `gate=GATE_DE_REESCRITA_FORTE`.
- `§13` item 12 + `§32` — `comment_type=GATE_HUMANO` exige um gate nomeado
  do catálogo, não `NENHUM`: o próprio propósito deste tipo é indicar um
  gate; `NENHUM` esvaziaria a indicação. Não é frase literal isolada — é
  a leitura mais direta de "indicar gate" [§4.4] combinada ao catálogo de
  §32, verificada com PS13-07 (`GATE_HUMANO` + `GATE_DE_ALTERACAO_DE_CONCLUSAO`).
- `§4.5` — bloqueio de fidelidade (`ResultadoDeFidelidade.BLOQUEAR`) exige
  `comment_type=ALERTA_DE_VOZ`: "evita formulação substitutiva; evita
  reescrever como orientador" só é verificável em código como recusa de
  gravar o bloqueio sob qualquer outro `comment_type` — verificado com
  TA13-12 e PS13-08.

### Não implementado nesta sessão — fora de escopo, não lacuna

- Construção do payload `ABSTAINED/AMBIGUITY` com
  `cause_code=P13_CAUSE_VOICE_PROFILE_INSUFFICIENT` [§29] — é envelope P09,
  sessão 8 do plano. Esta sessão só expõe `perfil_insuficiente(perfil)` e a
  constante do `cause_code`, para a sessão 8 reusar sem reinventar o
  predicado.
- `recommended_action` — já existe em `comentario.py` (sessão 1); §28 o
  cita de novo ("todo comentário deve registrar... recommended_action"),
  mas nenhuma regra nova de §28/§29 se aplica a este campo especificamente.
- Privacidade (`privacy_classification`, `GATE_DE_TRATAMENTO_DE_PRIVACIDADE`
  em uso real) — sessão adiada; o token do gate está catalogado em
  `GateCatalogoP13` porque §32 o lista, mas nenhuma lógica de privacidade é
  construída aqui.

## Sessão 6 — comentário-matriz e remissões [§23, §24]

`escolio/comentarios/matriz.py` implementa `TemplateComentarioMatriz`
(§23, dez itens), `TemplateRemissao` (§23, três itens) e
`CriterioConsolidacao`/`decidir_consolidacao` (§24). `registrar_comentario_matriz_e_remissoes`
liga os três à integridade referencial já existente em
`RegistroDeComentarios` (sessão 1) e ao catálogo de `CommentType`
(sessão 3). Nenhum arquivo de sessão anterior foi alterado. Testes:
PS13-04, TA13-14, TA13-15 [§45/§46].

### `decidir_consolidacao` — leitura da estrutura de §24, não citação isolada

§24 declara dois blocos de prosa ("deve ser consolidada quando" / "não
deve ser consolidada quando"), sem conectivo lógico explícito
("e"/"ou") entre os itens de cada bloco. A leitura implementada:

- as cinco condições afirmativas são conjunção (todas exigidas) — uma
  condição isolada (ex.: só "há risco de poluição", sem "a causa é a
  mesma") não sustentaria consolidar ocorrências de causas diferentes;
- as cinco exceções são vetos independentes (qualquer uma basta para
  recusar), porque cada uma descreve isoladamente um risco que a
  consolidação criaria (ocultar problema específico, decisões
  diferentes, etc.) — mesmo padrão de veto único já usado em
  `valida_correcao_local_nao_autoriza_reescrita_forte` (sessão 5).

Não é a única leitura gramaticalmente possível da fonte (um leitor
poderia exigir só uma das cinco condições afirmativas). Registrado aqui
para quem precisar contestar essa leitura contra o professor.

### "Remissão incompreensível" [§23] — não verificável em código

"Não deve haver remissão vazia ou incompreensível" tem duas metades:
"vazia" é verificável (`TemplateRemissao` exige os três campos não
vazios); "incompreensível" não tem critério objetivo declarado na fonte
e não é verificado — mesma disciplina de itens sem critério objetivo já
registrados na sessão 3 (§18).

### `decisao_humana_necessaria` — não retipado, mesma disciplina da sessão 2

§23 nomeia o item ("decisão humana necessária") sem declarar tipo (nem
enum, nem booleano). Permanece `str`, mesma leitura já aplicada aos nove
fatores de `MatrizSeletividade` (sessão 2) e a `authority_required`
(sessão 5): tipar por analogia seria inferência.

### Fora de escopo desta sessão, não lacuna

- Produção do comentário individual para uma ocorrência cuja
  consolidação `decidir_consolidacao` recusa — decisão de quem chama
  `registrar_comentario_matriz_e_remissoes`; este módulo só consolida.
- Extensão do envelope P09 com os payloads de PS13-04 — sessão 8 do
  plano.

## Sessão 7 — auditoria final interna [§25, §44]

`escolio/comentarios/auditoria.py` implementa `auditar_lote`, um checklist
que roda os 25 itens de §44, nesta ordem literal, sobre um `LoteDeAuditoria`
(comentários da sessão 1 + matrizes das sessões 2-6). "A auditoria não
corrige comentários" [§44] — nenhuma função grava, corrige ou reordena um
`P13Comment`; todo item só lê e classifica. Testes: TA13-17, TA13-18,
TA13-19 [§46], mais a proibição simétrica de §25 (zero comentários
legítimo / silêncio diante de risco material ilegítimo).

### Item 15 — privacidade P08: N/A explícito, não fabricado

Por instrução desta sessão e por `docs/spec/plano-P13.md` §"Sessão
adiada": a integração P08 aguarda `CO-012`/`CO-013`. `_item_privacidade_p08`
retorna sempre `VeredictoChecklist.NAO_APLICAVEL`, nunca `APROVADO` — não
existe caminho de código que avalie privacidade neste módulo, e o
`RelatorioAuditoriaFinal` exige exatamente 25 itens (nenhum a menos), então
o item precisa existir e declarar N/A, não ser omitido.

### `NAO_VERIFICAVEL_NESTA_SESSAO` — quarto veredito, não aprovação silenciosa

Além de `APROVADO`/`REPROVADO`/`NAO_APLICAVEL` (este último reservado ao
item 15), o módulo declara `NAO_VERIFICAVEL_NESTA_SESSAO` para dois casos
distintos, nunca fundidos com N/A:

- **Critério não declarado na fonte** — itens `TOM` (17) e
  `PROPORCIONALIDADE` (19): §44 nomeia os itens, mas nenhuma seção do
  contrato declara um critério objetivo mensurável para nenhum dos dois
  (diferente de "ancoragem" ou "gates", que têm campo e catálogo
  verificáveis). Mesma disciplina de "remissão incompreensível" em
  `matriz.py` (sessão 6) e de `authority_required` em
  `aplicacao_p06_p07.py` (sessão 5): não inventar um critério que a fonte
  não declarou.
- **Dado ausente no lote fornecido** — itens `SELETIVIDADE`/`CRITICIDADE`
  sem `matrizes_seletividade`, `AUSENCIA_DE_COMENTARIO_COSMETICO` sem
  `efeitos_linguisticos`, `AUSENCIA_LEGITIMA_DE_COMENTARIOS` com lote
  totalmente vazio, `ENVELOPES_P09` sem `verificacoes_envelope`. Estes
  quatro campos de `LoteDeAuditoria` são opcionais porque a fonte de dados
  correspondente (matrizes de seletividade, template de efeito
  linguístico, extensão do envelope P09) é de sessão própria (2, 3, 8) e
  pode não estar disponível no momento em que a auditoria roda sobre um
  lote parcial; a ausência vira item indeterminado, nunca aprovado por
  omissão.

`RelatorioAuditoriaFinal.veredicto_final` reflete isso: `REPROVADO` em
qualquer item vence; senão, `NAO_VERIFICAVEL_NESTA_SESSAO` em qualquer item
força `AUDITORIA_INDETERMINADA` — só todos os 25 itens em
`APROVADO`/`NAO_APLICAVEL` produzem `AUDITORIA_APROVADA`. Um lote
totalmente vazio (nenhum comentário, nenhuma matriz) é
`AUDITORIA_INDETERMINADA`, não `AUDITORIA_APROVADA` — "sucesso vazio" só é
legítimo quando a ausência de comentários é justificada por decisões de
seletividade presentes [§25, §3.9, item 6], não pela simples ausência de
qualquer dado.

### Proibição simétrica de §25 — como as duas pontas ficaram verificáveis

Nem `P13Comment` nem `MatrizSeletividade` têm campo que ligue um
comentário produzido ao candidato que o originou (nenhuma sessão anterior
declarou `candidate_problem_id`/`selection_id` em `P13Comment` — ver
"Fora de escopo" da sessão 1). Por isso os dois lados da proibição
simétrica são verificados em `MatrizSeletividade`, não cruzando contra
`lote.comentarios`:

- **Item 6 (ausência legítima)** — zero comentários é `APROVADO` quando
  toda `MatrizSeletividade` do lote tem `selection_decision != COMENTAR`;
  é `REPROVADO` quando alguma matriz decidiu `COMENTAR` mas nenhum
  comentário foi produzido (decisão não atendida).
- **Item 7 (silêncio ilegítimo)** — `REPROVADO` quando existe
  `MatrizSeletividade` com `criticality` em `CRITICIDADE_CRITICA`/`ALTA` e
  `selection_decision=NAO_COMENTAR_SEM_PROBLEMA_MATERIAL`: contradição
  literal (criticidade alta declarada, mas a decisão nega "problema
  material"). `AGUARDAR_EVIDENCIA`, `AGUARDAR_GATE`, `ABSTER_SE`,
  `BLOQUEADO` e `NAO_COMENTAR_POR_REPETICAO` não entram nesta reprovação —
  são não-comentário justificado por motivo diferente de "sem problema",
  e nenhuma fonte os equipara a silêncio.

Isto não requer nem inventa uma correspondência comentário↔candidato:
ambos os itens leem só `MatrizSeletividade`, que já carrega `criticality`
e `selection_decision` como campos próprios (sessão 2). Item 25
(densidade justificada) é derivado destes dois: `REPROVADO` se quota
(item 4) ou silêncio (item 7) reprovarem, `APROVADO` caso contrário — não
é um item independente, é a leitura composta de §25 verbatim ("não existe
quota" + "não... silêncio diante de risco material").

### Item 16 (envelopes P09) — reusa `Response`/`SafeResult` reais, não os reimplementa

`verifica_consistencia_envelope_p09` constrói um `escolio.contrato.resposta.Response`
mínimo (ids fixos de teste, `component_id`/`function_id="P13"`) só para
disparar as validações já existentes de P09 §8.2/§9/§21.34 — nenhuma regra
de `Response`/`SafeResult` é duplicada. `P13RequestExtension`/
`P13ResultExtension` (sessão 8) não são construídos aqui: o item verifica
consistência `status`×`safe_result.available`×payload quando o lote
informa candidatos via `VerificacaoEnvelope`, e fica
`NAO_VERIFICAVEL_NESTA_SESSAO` quando não informa — não fabrica um
envelope P13 que a sessão 8 ainda não define.

### Itens que reusam validação já existente sem duplicá-la

- Item 1 (seletividade) reusa `exige_referencia_valida_a_criticidade`
  (BL-024, sessão 2).
- Item 9 (remissões) reusa `RegistroDeComentarios.registrar` (sessão 1) —
  registra os comentários-matriz do lote antes dos demais e deixa o
  próprio registro rejeitar remissão órfã, em vez de reimplementar a
  checagem de integridade referencial.
- Item 14 (voz P07) reusa `ResultadoDeFidelidade` (P07) e a mesma regra de
  `valida_alerta_de_voz_quando_bloqueado` (sessão 5, verificada por
  leitura direta do enum, não por chamada à função porque esta espera um
  objeto `AvaliacaoDeFidelidade` que o lote de auditoria não reconstrói).
- Item 22 (gates) reusa `valida_correcao_local_nao_autoriza_reescrita_forte`
  e `valida_gate_humano_tem_gate_nomeado` (sessão 5) diretamente.
- Item 23 (ausência de reescrita substitutiva) não tem verificação própria
  — é derivado do resultado do item 13 (nível P06): REESCRITA já é
  rejeitada por `NIVEIS_PERMITIDOS_P13` (sessão 5), então "nenhuma
  reescrita substitutiva" é a mesma checagem lida pelo ângulo do
  invariante de §4.4, não uma segunda regra independente.

### Item 24 (ausência de implementação Word) — decisão de leitura, não citação isolada

§43 lista "piloto Word real posterior" e "ativação operacional posterior"
como etapas 28-29, fora desta fase; `P13CommentStatus.INSERTED` (sessão 1)
é o único ponto do schema atual que nomeia uma inserção efetiva no
documento. `_item_ausencia_de_implementacao_word` reprova qualquer
comentário do lote com `status=INSERTED`, lendo isso como o único sinal
verificável em código de que a fase de inserção Word teria sido
alcançada. Nenhuma outra parte do código (`escolio/comentarios/`) importa
biblioteca de manipulação de `.docx` — condição estrutural, não verificada
por este item, apenas observada aqui como coerente com a leitura.

### Fora de escopo desta sessão, não lacuna

- Ligação `comment_id -> candidate_problem_id`/`selection_id` — ausente em
  todas as sessões anteriores (ver nota da seção "Proibição simétrica"
  acima); não introduzida aqui porque isso alteraria `P13Comment`
  (sessão 1), e a instrução desta sessão foi "não altere código
  existente".
- Item 5 (ausência de comentário cosmético) só verifica quando o lote
  informa `efeitos_linguisticos` (mapa `comment_id -> efeito` de §15) —
  `P13Comment` não tem campo `efeito`; a informação só existe em
  `TemplateComentarioLinguistico` (sessão 3), que por sua vez não tem
  campo que o ligue a um `comment_id`. Sem essa ligação, o item depende de
  entrada externa explícita, nunca de inferência a partir do texto do
  comentário.
- Extensão do envelope P09 com `P13ResultExtension` carregando o
  `RelatorioAuditoriaFinal` — sessão 8 do plano.

## Sessão 8 — extensão do envelope P09 [§31.1-31.4, §31.6, §29]

`escolio/comentarios/aplicacao_p09.py` implementa `P13RequestExtension`
(§31.3), `P13ResultExtension` (§31.4), o exemplo canônico de §29
(`constroi_abstencao_perfil_de_voz_insuficiente`) e três builders de
`Response` P13-específicos para as três formas de payload de §31.6
(`resposta_p13_abstained`, `resposta_p13_blocked`, `resposta_p13_error`).
Nenhum arquivo existente foi alterado. Testes:
`tests/comentarios/test_aplicacao_p09.py`.

### §31.6 não gerou regra nova — só reafirma o que a peça 1 já impõe

As três formas de payload de §31.6 (ABSTAINED, BLOCKED, "somente ERROR pode
utilizar safe_result") são exatamente o que `Response.__post_init__`
(`escolio/contrato/resposta.py`, peça 1) já impõe para qualquer
`function_id` — nenhuma delas é uma regra nova do P13. Os três builders só
fixam `function_id="P13"` e a forma de `safe_result` que cada status exige;
nenhuma validação de `Response`/`SafeResult` é duplicada. Mesma leitura já
registrada por `verifica_consistencia_envelope_p09` (sessão 7,
`auditoria.py`, item 16).

### `cause_code` — campo citado em §29/§30, ausente do schema de `AbstentionPayload`

`AbstentionPayload` (P09 §15, `escolio/contrato/payloads.py`) não tem campo
`cause_code`. O campo não é do envelope P09 — só aparece nos exemplos de
§29 e §30 dos contratos de função. Sem campo dedicado, e sem nenhuma outra
seção do P09 ou do P13 que diga onde colocá-lo, `constroi_abstencao_
perfil_de_voz_insuficiente` registra o valor literalmente dentro de
`reason` — o único campo de texto livre obrigatório do payload — em vez de
acrescentar um campo a `AbstentionPayload` (alteraria código existente,
fora do escopo desta sessão, e a instrução da sessão foi "não altere
código existente; se a integração exigir mudança, registre em
`docs/backlog.md` e pare"). Registrado também em `docs/backlog.md` como
BL-026.

O exemplo de §30 (`cause_code=P13_CAUSE_PRIVACY_PROCESSING_CONDITION_ABSENT`,
`category=PRIVACY_RISK`) **não foi construído aqui** — pertence à sessão de
privacidade (P08), que permanece adiada [`docs/spec/plano-P13.md`, "Sessão
adiada"]. Quando essa sessão rodar, a mesma convenção (`cause_code` dentro
de `reason`) deve ser reaplicada, não reinventada.

### `P13CommentReferral` e `UnitDecision` — tipos citados uma única vez, sem schema em nenhuma seção

`matrix_referrals: [P13CommentReferral]` e `units_without_comment:
[UnitDecision]` (§31.4) citam dois tipos que não aparecem em nenhuma outra
linha do arquivo-fonte — confirmado por busca textual no documento
completo. Diferente de `ResultItem` (P09 §8), cuja abertura tem licença
explícita da própria fonte (P09 §25: "linguagem concreta de schema é
lacuna legítima, pertencente à implementação posterior"), aqui não há
frase equivalente autorizando a abertura — mas também não há nenhuma outra
frase que declare os campos de nenhum dos dois tipos.

Candidata rejeitada por analogia de nome: `TemplateRemissao` (§23, sessão
6, `matriz.py`) parece semanticamente próxima de "`P13CommentReferral`" —
mas nenhuma frase da fonte declara essa correspondência, e associar por
semelhança de nome é exatamente a inferência que a sessão 3 já recusou
para `CommentType`/template (ver "Não é lacuna — leitura literal do
catálogo", sessão 3). Os dois campos permanecem `list[object]` em
`P13ResultExtension` — mesmo tratamento dado aos `[any]` genuinamente
abertos do mesmo parágrafo (`source_pending_items`,
`evidence_pending_items`, `voice_warnings`, `p13_traceability`,
`limitations`).

### Assimetria entre `Result.content` (aberto) e `Request` (sem campo aberto) — observada, não corrigida

`Response.result.content` (`escolio/contrato/resposta.py`) já é `object |
None` — `P13ResultExtension` encaixa ali sem exigir qualquer alteração de
`Response` (`test_result_com_p13_result_extension` demonstra isso).
`Request` (`escolio/contrato/requisicao.py`) não tem campo equivalente:
nenhum de seus campos aceita um objeto aberto para carregar uma extensão
específica de função — `ContextItem` (§7) é desenhado para *apontar* para
conteúdo externo via `content_reference: str`, não para embutir um objeto.
Por isso `P13RequestExtension` é construído e validado como objeto
independente, sem um ponto de anexação testado ao lado de `Request` — a
ausência de simetria é observação desta sessão, não uma alteração proposta
a `requisicao.py` (alterar o schema da peça 1 está fora do escopo; ver
BL-026 em `docs/backlog.md`).

### Herança de BL-011/BL-013 — não corrigida aqui, por instrução da sessão

`resposta_p13_abstained`/`resposta_p13_blocked`/`resposta_p13_error` fixam
`function_id="P13"`, mas não implementam a correspondência de `function_id`
entre requisição e resposta que falta em
`exige_correspondencia_request_response` (BL-011), nem anexam
`InterventionRecord` a `Response` (BL-013, `Response.interventions`
continua omitido). O P13 herda as duas pendências tal como estão —
corrigi-las alteraria `escolio/contrato/resposta.py`, fora do escopo desta
sessão por instrução explícita.

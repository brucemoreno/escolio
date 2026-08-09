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

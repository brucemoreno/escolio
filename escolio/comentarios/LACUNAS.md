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

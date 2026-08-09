# P13 — Etapa 9: matriz de seletividade [§12]

Fonte: `P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md §12`, transcrita em
`escolio/comentarios/seletividade.py`.

Você recebe, no bloco `system`, o documento completo. No bloco de mensagem desta chamada, você
recebe uma lista de problemas candidatos já avaliados na matriz de criticidade (etapa 8),
cada um com `problem_id`, `unit_id` e `classe` de criticidade.

Critério de seleção, verbatim [§12]: **"Um comentário deve ser selecionado quando o ganho de
orientação for superior ao custo de poluição documental."**

Para cada problema candidato recebido, avalie os **dez fatores** do §12 e produza uma
`MatrizSeletividade`:

- `material_impact` — impacto material do problema.
- `novelty` — é um achado novo, ou repete algo já sinalizado?
- `recurrence` — é ocorrência única ou recorrente no documento?
- `matrix_comment_coverage` — já está coberto por um comentário-matriz existente?
- `actionability` — o autor pode agir sobre isto de forma proporcional?
- `evidence_sufficiency` — há evidência suficiente para sustentar o comentário agora?
- `human_decision_required` — este comentário depende de decisão humana antes de ser emitido?
- `privacy_risk` — comentar exigiria exposição indevida de dado sensível?
- `selection_rationale` — a síntese argumentativa do critério acima, não uma fórmula.

Em seguida declare `selection_decision`, um dos oito resultados do §10, verbatim: `COMENTAR,
NAO_COMENTAR_SEM_PROBLEMA_MATERIAL, NAO_COMENTAR_POR_REPETICAO, REMETER_A_COMENTARIO_MATRIZ,
AGUARDAR_EVIDENCIA, AGUARDAR_GATE, ABSTER_SE, BLOQUEADO`.

**Nunca aplique quota percentual ou numérica** — a seleção é decidida por este critério
qualitativo, não por contagem [PC30_SIGNIFICA_CRITICIDADE_E_NAO_QUOTA, §3.9, §34].
**Zero seleções (todas as decisões diferentes de `COMENTAR`) é um resultado legítimo** — não
force `COMENTAR` para atingir um número.

`criticality` deve copiar exatamente a `classe` do problema candidato recebido — não reavalie a
criticidade aqui, isso já foi decidido na etapa 8.

Invente um `selection_id` novo e estável (ex.: `SEL-<problem_id>`).

Registre cada avaliação usando a ferramenta fornecida. Não produza texto fora da ferramenta.

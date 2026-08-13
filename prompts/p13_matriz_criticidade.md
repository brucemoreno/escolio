# P13 — Etapa 8: matriz de criticidade [§11]

Fonte: `P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md §11`, transcrita em
`escolio/comentarios/criticidade.py`.

Você recebe, no bloco `system`, o documento completo (unidades identificadas por `unit_id`,
com o texto de cada uma). No bloco de mensagem desta chamada, você recebe uma lista de
`unit_id` — as unidades desta chamada.

Para cada unidade da lista, identifique se ela contém um **problema candidato** que mereça
avaliação de criticidade. Uma unidade pode não conter nenhum problema candidato — não force
um problema onde não há um; omitir a unidade da resposta é o resultado correto nesse caso.

Para cada problema candidato identificado, avalie os **12 eixos** do §11, verbatim:
`FACTUAL, EVIDENCIA, BIBLIOGRAFICO, METODOLOGICO, ARGUMENTATIVO, ESTRUTURAL, VOZ, PRIVACIDADE,
AVALIATIVO, SISTEMICO, CENTRALIDADE, REVERSIBILIDADE`.

Todos os 12 eixos são obrigatórios para todo problema candidato, mesmo quando a resposta for
"não se aplica" — nesse caso, escreva a justificativa dizendo por que o eixo não se aplica;
nunca deixe um eixo vazio.

Depois de avaliar os 12 eixos, declare uma **classe** de criticidade:
`CRITICIDADE_CRITICA | CRITICIDADE_ALTA | CRITICIDADE_MEDIA | CRITICIDADE_BAIXA |
SEM_CRITICIDADE_MATERIAL`.

**A classe não pode ser reduzida a contagem mecânica dos eixos** [§11, verbatim]. Justifique a
classe com uma síntese argumentativa (`justificativa_classe`), não com uma fórmula. Um problema
com um único eixo muito grave pode justificar `CRITICIDADE_CRITICA`; doze eixos levemente
negativos não somam automaticamente uma classe alta.

Invente um `problem_id` novo e estável para cada problema candidato (ex.:
`PROB-<unit_id>-<sequencial>`).

Registre cada problema candidato usando a ferramenta fornecida. Não produza texto fora da
ferramenta.

**Sobre o formato do campo `matrizes` da ferramenta**: ele é um **array de objetos**, direto —
cada problema candidato é um elemento do array. Nunca serialize o array (ou o objeto que o
contém) como texto JSON e coloque essa string como valor de `matrizes` ou de qualquer outro
campo — isso quebra a leitura automática da resposta. Se não houver nenhum problema candidato em
nenhuma unidade desta chamada, registre `matrizes` como array vazio (`[]`), nunca como string.

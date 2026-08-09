# P11 — Etapa 6: diagnóstico de estabilidade [§2, §38]

Fonte: `P11_CONTRATO_FUNCIONAL_REVISAO_TESE_DISSERTACAO_HOMOLOGADO_R01.md`. Regra estrutural
central do contrato, verbatim: **"do global para o local"** — nenhuma intervenção local é
segura sem que sua função na obra tenha sido identificada primeiro [§2, invariante 2].

Você recebe, no bloco `system`, a obra inteira (unidades identificadas por `unit_id`, com o
texto de cada uma — parágrafos, citações recuadas, notas de rodapé, figuras).

Sua tarefa nesta etapa é avaliar a **estabilidade do projeto intelectual** da obra: o
problema de pesquisa, o objetivo (geral e específicos), a hipótese/tese/questão central, o
método e o corpus estão coerentes entre si e sustentados ao longo da obra, ou há sinais de
instabilidade que tornariam prematuro qualquer diagnóstico estrutural, argumentativo ou
historiográfico local?

Instabilidade inclui, sem se limitar a: objetivo declarado na introdução que não corresponde
ao que o corpo do texto de fato investiga; hipótese que muda sem marcação explícita entre
capítulos; corpus mencionado no método que não aparece (ou aparece apenas parcialmente) no
desenvolvimento; conclusão que responde a uma pergunta diferente da que a introdução formulou.

Para cada achado, registre:

- `claim_text` — a afirmação diagnóstica, em linguagem clara e verificável.
- `claim_type` — `FACT` quando o achado é uma constatação textual direta (ex.: "o capítulo 4,
  anunciado no sumário, não está presente no material fornecido"); `INTERPRETATION` quando é
  leitura sua sobre coerência entre partes; `INFERENCE` quando deduz algo não afirmado
  explicitamente; `LIMITATION` quando o achado é sobre uma limitação do próprio diagnóstico
  (ex.: material insuficiente para avaliar determinado eixo); `RECOMMENDATION` nunca é o tipo
  correto aqui — recomendação de ação é etapa posterior (`PROPOSTA`, INT-05), fora do teto
  desta etapa (`DIAGNOSTICO`, INT-02).
- `sufficiency` — `SUFFICIENT`, `PARTIAL`, `INSUFFICIENT` ou `NOT_APPLICABLE`: o quanto a obra
  fornece material para sustentar ou refutar esta afirmação.
- `confidence` — `HIGH`, `MEDIUM`, `LOW` ou `UNDETERMINED`: sua confiança na afirmação, não na
  gravidade do problema.
- `status` — `SUPPORTED`, `PARTIALLY_SUPPORTED` ou `UNSUPPORTED`. **Nunca `CONFLICTED`**: esta
  etapa não concilia fontes divergentes, diagnostica estabilidade do projeto intelectual.
  `SUPPORTED` exige `evidence_ids` não vazio.
- `evidence_ids` — a lista de `unit_id` da obra que sustentam o achado. Toda afirmação do tipo
  `FACT` sem `evidence_ids` deve ter `status=UNSUPPORTED`.
- `location_section` — quando aplicável, a seção da obra a que o achado se refere (ex.: "3.2").
- `notes` — opcional; use para qualquer ressalva que não caiba nos campos acima.

Estabilidade sem problema material também é resultado legítimo: a ausência de achados de
instabilidade é um `achados` vazio, não uma lista forçada. Não produza um achado apenas para
preencher a resposta.

Registre cada achado usando a ferramenta fornecida. Não produza texto fora da ferramenta.

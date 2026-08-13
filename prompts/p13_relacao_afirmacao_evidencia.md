# P13 — Etapa 12: verificação de evidências [P05, P09 §12]

Fonte do objeto de saída: `02_DICIONARIO_DE_DADOS_P05_R01.csv`, transcrita em
`escolio/relacao.py` (`RelacaoAfirmacaoEvidencia`).

Você recebe, no bloco `system`, o documento completo (unidades identificadas por `unit_id`, com
o texto de cada uma). No bloco de mensagem desta chamada, você recebe uma lista de `unit_id` — as
unidades desta chamada.

Para cada unidade da lista, identifique **afirmações candidatas** que dependem de evidência
externa para sustentação — afirmações factuais, citações, dados metodológicos ou normativos que
um leitor exigente cobraria fonte. Uma unidade pode não conter nenhuma afirmação candidata — não
force uma onde não há; omitir a unidade da resposta é o resultado correto nesse caso.

Para cada afirmação candidata, produza uma relação afirmação-evidência completa:

- `claim_id`: invente um identificador novo e estável (ex.: `CLAIM-<unit_id>-<sequencial>`).
- `claim_text`: o texto da afirmação, verbatim ou parafraseado fielmente.
- `claim_type`: `FATUAL | INTERPRETATIVA | CITACAO | METODOLOGICA | NORMATIVA | OUTRA_CONTROLADA`.
  Use `OUTRA_CONTROLADA` só quando nenhuma das cinco se aplica, e preencha `notes` explicando por quê.
- `source_id`: identificador da fonte que a afirmação invoca (pode ser `[INFERIDO]` quando a
  fonte não está nomeada explicitamente no texto).
- `source_type`: `DOCUMENTO | BASE_DE_DADOS | IMAGEM | AUDIO | VIDEO | WEB | REGISTRO_INTERNO |
  OUTRO_CONTROLADO`. Use `OUTRO_CONTROLADO` só quando nenhum dos sete se aplica, e preencha
  `notes` explicando por quê.
- `source_reference`: a referência da fonte tal como o texto a descreve (ex.: nome do autor
  citado, título mencionado) — nunca invente uma referência bibliográfica completa que o texto
  não fornece.
- `location_type`, `location_value`, `page_or_folio`: onde no texto a afirmação aparece, quando
  determinável. `location_type=NAO_CONFIRMADO` quando o texto não permite localizar com precisão.
- `evidence_excerpt`: o trecho do texto-fonte (dentro da própria unidade ou do documento) que
  sustenta ou tenta sustentar a afirmação, se houver um.
- `evidence_level`: `A_INTERNA_FORNECIDA | B_MATERIAL_ANEXADA | C_FERRAMENTA_RASTREAVEL |
  D_AUSENTE` — o nível real de evidência disponível **para você, nesta chamada**, nunca um
  nível aspiracional.
- `access_state`, `reading_state`: seu próprio acesso e leitura da fonte citada nesta chamada —
  tipicamente `NAO_LOCALIZADA`/`LEITURA_NAO_REALIZADA` quando você não tem acesso à fonte
  original, `LEITURA_INDIRETA` quando o julgamento vem só do que o texto avaliado relata sobre a
  fonte.
- `sufficiency`: `NAO_AVALIADA | EVIDENCIA_AUSENTE | EVIDENCIA_INSUFICIENTE |
  EVIDENCIA_PARCIALMENTE_SUFICIENTE | EVIDENCIA_SUFICIENTE | CONFLITANTE` — seu julgamento
  **preliminar**, sujeito a revisão humana [P09 §12: sufficiency e confidence são separados].
- `confidence`: `NAO_AVALIADA | BAIXA | MEDIA | ALTA` — sua confiança **preliminar** nesse
  julgamento de sufficiency, não a mesma coisa que sufficiency.
- `usage_status`: `NAO_USAR | USO_CONDICIONAL | USO_LIBERADO | ABSTENCAO` — sua recomendação
  preliminar sobre se a afirmação pode ser usada como está.
- `validation_state`: use **apenas** `NAO_VERIFICADA`, `PAGINA_NAO_CONFIRMADA`,
  `PAGINA_CONFIRMADA` ou `VALIDACAO_PENDENTE`. **Nunca** use `VALIDADA` nem
  `INVALIDADA_POSTERIORMENTE` — essas duas exigem um validador humano nomeado e uma data de
  validação, que só existem depois de revisão humana [CLAUDE.md: "o sistema nunca homologa"].
  Se usar `PAGINA_CONFIRMADA`, preencha `location_value`.
- `reversibility`: `REVERSIVEL_COM_NOVA_EVIDENCIA | REVERSIVEL_POR_CORRECAO | NAO_APLICAVEL`.
- `notes`: use para justificar `OUTRA_CONTROLADA`/`OUTRO_CONTROLADO`, ou para qualquer
  observação que um revisor humano precise para julgar seu julgamento preliminar.

Você **não** preenche `provenance`, `validator` nem `validation_date` — esses campos são
atribuídos pelo sistema fora desta chamada.

Registre cada relação usando a ferramenta fornecida. Não produza texto fora da ferramenta.

**Sobre o formato do campo `relacoes` da ferramenta**: ele é um **array de objetos**, direto —
cada relação afirmação-evidência é um elemento do array. Nunca serialize o array (ou o objeto que
o contém) como texto JSON e coloque essa string como valor de `relacoes` ou de qualquer outro
campo. Se não houver nenhuma afirmação candidata em nenhuma unidade desta chamada, registre
`relacoes` como array vazio (`[]`), nunca como string.

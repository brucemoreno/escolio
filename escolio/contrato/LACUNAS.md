# LACUNAS — implementação do envelope P09

Lacunas encontradas na implementação de `escolio/contrato/`, item 1 do roadmap. Nenhum item
aqui foi resolvido por inferência; cada um documenta a decisão tomada e por quê.

## Sobre a fonte em si

- **Ausência de `00_LEIA_PRIMEIRO` no pacote citado.** A instrução da sessão apontava
  `PACOTE_CONTRATO_STATUS_LLM_ACADEMICA_R01/00_LEIA_PRIMEIRO` para ordem de leitura. O pacote
  real contém um único arquivo,
  `P09_SCHEMAS_CONTRATOS_CORRIGIDO_R04.md`, sem `00_LEIA_PRIMEIRO` — não há múltiplos
  arquivos a ordenar. Lido o único arquivo existente, integralmente.

## ClaimEvidence — P09 §12 × P05 (relacao.py)

- **BL-002** (já registrado em `docs/backlog.md`): `ClaimEvidence` do P09 §12 usa vocabulário
  próprio (`ClaimType: FACT|INTERPRETATION|RECOMMENDATION|INFERENCE|LIMITATION`,
  `Sufficiency: SUFFICIENT|PARTIAL|INSUFFICIENT|NOT_APPLICABLE`,
  `Confidence: HIGH|MEDIUM|LOW|UNDETERMINED`), distinto do vocabulário de
  `RelacaoAfirmacaoEvidencia` (P05). Implementado como dataclass própria em
  `escolio/contrato/afirmacao.py`, sem herdar de `RelacaoAfirmacaoEvidencia` e sem alterar
  `escolio/relacao.py`. Nenhuma camada de tradução entre os dois foi construída aqui — o
  mapeamento continua no backlog (BL-002), tratamento igual ao dado a `CON-P05-001`.

## Regras declarativas sem campo de código correspondente

- **§7 — "contexto não substitui autorização, evidência, dependência ou comando humano
  válido."** É regra de uso, não uma condição sobre os campos do próprio `ContextItem`. Nenhuma
  validação de `__post_init__` a codifica; ela deve ser respeitada pelo código que *consome*
  `ContextItem` ao construir uma decisão, não pelo schema em si. Documentado em
  `escolio/contrato/contexto.py`.

- **§4.2.3-4.2.5 — `component_id` deve corresponder ao componente vigente; `function_id` deve
  pertencer ao `component_id`; `function_id` deve ser compatível com `operation`.** Essas três
  regras exigem um catálogo externo de componentes/funções/operações válidas (o catálogo das
  seis funções em CLAUDE.md §3) que não faz parte do envelope P09 em si — o P09 define o
  *formato* do contrato, não o catálogo substantivo. Não implementadas em
  `escolio/contrato/requisicao.py`; ficam para quando o roteador de função (roadmap, item 6)
  existir e puder fornecer esse catálogo.

## Decisões de implementação verificáveis apenas por proxy

- **§5.1 — `compatibility_status=NOT_APPLICABLE` "somente é válido com `mode=ANY` ou quando a
  dependência não possuir versão aplicável".** O schema não tem um campo separado para "não
  possuir versão aplicável" além do próprio `mode`. Implementado em
  `escolio/contrato/dependencia.py` tratando apenas `mode=ANY` como condição verificável em
  código; a segunda cláusula da regra ("dependência não possuir versão aplicável") não tem
  representação estrutural distinta de `mode=ANY` neste schema e não foi inferida.

- **§17 — "limitação de materialidade alta incompatível com conclusão integral impede
  SUCCESS".** "Incompatível com conclusão integral" não tem campo próprio na fonte. A
  propriedade `Limitation.impede_sucesso_integral` em `escolio/contrato/payloads.py` trata toda
  `materiality=HIGH` como impeditiva — decisão de implementação mais restritiva que o texto
  literal (que condiciona a incompatibilidade, não a declara automática), documentada aqui para
  não passar por leitura literal do parágrafo.

- **§8 — `result.structured_items: [ResultItem]`.** O envelope declara o tipo sem definir o
  schema interno de `ResultItem` — o P09 §25 declara explicitamente que "linguagem concreta de
  schema" é lacuna legítima, pertencente à implementação posterior. `ResultItem` foi
  implementado como estrutura mínima aberta (`item_id`, `content: any`) em
  `escolio/contrato/resposta.py`, sem inventar campos que a fonte não pede.

## Não incluído nesta peça (fora de escopo, não lacuna)

- **`InterventionRecord` (§13)** — item 2 do roadmap, junto com os níveis P06. Não implementado
  em `escolio/contrato/`.
- **`Response.interventions`** — campo do envelope de resposta (§8) que referencia
  `InterventionRecord`; por depender do item acima, foi omitido do dataclass `Response` com
  comentário explícito no código, não silenciosamente.

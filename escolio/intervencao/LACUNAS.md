# LACUNAS — implementação de P06 (níveis de intervenção) e InterventionRecord (P09 §13)

Lacunas encontradas na implementação de `escolio/intervencao/`, item 2 do roadmap. Nenhum item
aqui foi resolvido por inferência.

## Vocabulário e tipagem

- **`requested_level`/`applied_level` tipados como `NivelIntervencao`, não `string`.** O YAML do
  P09 §13 declara `string` porque P06 (onde os 15 níveis são definidos) e P09 (onde
  `InterventionRecord` é definido) são pacotes homologados independentes — o schema do envelope
  não pressupõe que o dicionário de níveis exista em código. Como ambos existem aqui, a tipagem
  forte com `NivelIntervencao` é estritamente mais restritiva que `string` livre, nunca menos —
  documentado, não uma divergência de regra.

- **`authority_status` tipado como `AuthorizationStatus` (escolio.contrato.vocabulario), reusado
  sem duplicação.** O P06/P09 não declaram um vocabulário próprio de status de autoridade
  distinto do já existente em `escolio/contrato/`; ao contrário de `ClaimEvidence` (P09 §12,
  onde P05 e P09 têm vocabulários deliberadamente distintos — BL-002), aqui não há indício de
  dois vocabulários paralelos. Reuso direto, não criação de alias.

## §13 — regras verificáveis apenas por proxy

- **§13.3-13.5 — "nenhuma transformação registrada como executada".** A fonte não define um
  campo estrutural distinto de `after_reference` para "transformação executada". Implementado em
  `escolio/intervencao/registro.py::InterventionRecord._valida_nao_aplicada` como
  `after_reference` obrigatoriamente `null` para REFUSED/ABSTAINED/BLOCKED — a fonte já condiciona
  isso a "quando representaria transformação inexistente", e como não há disposition não-APPLIED
  em que uma transformação real ocorreu, a condição é sempre verdadeira aqui. Mais restritivo,
  não inferido além do texto.

- **§13.2 — "a intervenção deve estar autorizada".** Implementado exigindo
  `authority_status=AuthorizationStatus.VALID` para `disposition=APPLIED`. A fonte não lista
  campo estrutural alternativo para "autorizada" — `authority_status` é o único campo do schema
  que carrega esse conceito.

- **§13.1 — "before_reference e after_reference devem permanecer coerentes com a disposição".**
  Regra qualitativa sem critério de coerência definido além do já verificável em código (§13.3-
  13.5 acima, para `after_reference`). `before_reference` não recebe validação própria: a fonte
  não define quando `before_reference` é obrigatório além de "quando necessário à
  reversibilidade" (§13.2), que não tem operacionalização em campo (não há campo booleano
  "necessário à reversibilidade" distinto de `reversible`). Não implementado; permanece
  responsabilidade de quem constrói o registro.

## P06 — cadeia e escalonamento

- **`04_MATRIZ_DE_ESCALONAMENTO_E_REGRESSAO_P06_R01.csv` não lista todas as 15 transições
  adjacentes da cadeia.** A matriz para em `REORGANIZACAO;FUSAO` e `REORGANIZACAO;CORTE`, sem
  linha para `FUSAO->SUBSTITUICAO`, `CORTE->SUBSTITUICAO` ou `SUBSTITUICAO->VALIDACAO` —
  substitui por `QUALQUER_EXECUCAO;VALIDACAO`, que cobre esses casos de forma agregada mas não
  nomeada. `escolio/intervencao/niveis.py::escalonamento_permitido` implementa exatamente o que
  a matriz lista: `VALIDACAO` é alcançável de qualquer nível de execução (tratado como
  `origem == VALIDACAO` sendo o destino de qualquer execução anterior, verificado por quem chama
  fora deste dicionário), e não há transição codificada de `FUSAO`/`CORTE`/`SUBSTITUICAO` para o
  próximo nível ordinal — a matriz não define essa transição explicitamente, e nada foi inferido
  para preenchê-la.

- **Limiares quantitativos de risco irreversível não definidos [P06-LAC-001, já registrado na
  fonte].** Preservado sem inferência; decisão humana por caso, como a própria fonte declara.

- **Origem `QUALQUER_NIVEL` para `ABSTENCAO` na matriz §04** não é um nível pontual da cadeia —
  é tratada em `escolio/intervencao/gate.py::registro_de_abstencao`, chamável a partir de
  qualquer ponto do fluxo, não modelada como uma transição saindo de um `NivelIntervencao`
  específico.

## Não incluído nesta peça (fora de escopo, não lacuna)

- **Catálogo de causas de ABSTENCAO/REFUSED/BLOCKED** (comando vago, objeto congelado, conflito
  de instruções, mistura entre projetos — `05_PROTOCOLO_DE_AUTORIZACAO_E_ABSTENCAO_P06_R01.txt`).
  Este pacote define o protocolo de decisão, não um enum fechado de causas; `rationale` em
  `InterventionRecord` permanece texto livre, preenchido por quem chama. Nenhuma enumeração foi
  inventada para substituir texto livre onde a fonte não declarou um vocabulário controlado.
- **Objetos congelados (`06_PROTOCOLO_DE_INTERVENCAO_EM_OBJETOS_CONGELADOS_P06_R01.txt`)**: o
  protocolo de reabertura (oito exigências) é procedimento humano-documental, não uma condição
  verificável nos campos do próprio `InterventionRecord` — não há campo "objeto congelado" no
  schema P09 §13. Deixado para o roteador de função (roadmap, item 6), quando existir estado de
  objeto a consultar.

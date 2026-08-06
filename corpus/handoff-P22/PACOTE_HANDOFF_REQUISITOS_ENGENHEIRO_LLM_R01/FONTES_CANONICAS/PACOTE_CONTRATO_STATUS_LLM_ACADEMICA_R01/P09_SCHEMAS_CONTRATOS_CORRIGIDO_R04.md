# P09 — SCHEMAS DE ENTRADA, SAÍDA, ERRO E ABSTENÇÃO

## 1. FINALIDADE

O P09 define os contratos técnicos universais de comunicação entre usuário, componentes, funções, módulos, agentes e camadas do ecossistema `LLM_ACADEMICA`.

Seu objetivo é assegurar que toda operação:

- receba entradas identificáveis e validáveis;
- produza saídas tipadas e rastreáveis;
- represente erros sem mascará-los;
- represente abstenções sem confundi-las com falhas;
- represente bloqueios apenas quando houver impedimento material demonstrável;
- preserve proveniência, autoridade, escopo, dependências, versões e estado;
- preserve resultados seguros produzidos antes de falha localizada;
- respeite os controles dos componentes P03–P08;
- permaneça tecnologicamente neutra.

---

## 2. PRINCÍPIOS ESTRUTURANTES

### 2.1 Contrato explícito

Nenhuma função deve depender de significado implícito quando o dado puder ser representado por campo próprio.

### 2.2 Tipagem semântica

Os schemas devem distinguir:

- dado;
- comando;
- evidência;
- contexto;
- autorização;
- dependência;
- versão;
- transformação;
- resultado seguro;
- erro;
- abstenção;
- bloqueio;
- alerta;
- decisão;
- saída parcial;
- saída final.

### 2.3 Rastreabilidade

Toda saída substantiva deve permitir vinculação a:

- requisição;
- função;
- componente;
- operação;
- entradas;
- fontes;
- dependências;
- versões;
- autoridade;
- intervenções;
- decisões;
- limitações.

### 2.4 Falha explícita

Ausência de resposta válida não pode ser apresentada como sucesso.

### 2.5 Abstenção não é erro

A abstenção representa decisão controlada de não executar ou não concluir determinada operação por insuficiência de autoridade, evidência, proveniência, segurança, escopo ou conflito localizado.

### 2.6 Erro não é abstenção

Erro representa falha estrutural, formal, de validação, integridade, processamento, execução, formato ou infraestrutura.

### 2.7 Bloqueio não é erro nem abstenção

Bloqueio representa impedimento material externo, documental ou de governança, demonstrado por evidência verificada e que impede objetivamente a operação.

### 2.8 Saída parcial identificada

Resultado parcial deve ser marcado como parcial, conter causa explícita da parcialidade e nunca ser apresentado como conclusão integral.

### 2.9 Resultado seguro preservado

Resultado seguro produzido antes de falha localizada deve permanecer separado da operação global que falhou e não altera automaticamente o status global `ERROR`.

### 2.10 Preservação de conteúdo

Transformações não podem apagar silenciosamente:

- incerteza;
- divergência;
- lacuna;
- origem;
- restrição;
- não conformidade;
- conteúdo adversarial;
- conflito de autoridade;
- conflito entre fontes;
- estado de dependência;
- incompatibilidade de versão;
- classificação de sensibilidade.

---

## 3. VERSIONAMENTO UNIVERSAL

Todo schema deve utilizar exclusivamente:

```yaml
SemanticVersion:
  major: integer
  minor: integer
  patch: integer
```

Não é válida representação alternativa como string livre.

### 3.1 Compatibilidade

- alteração `patch`: correção sem mudança semântica;
- alteração `minor`: campo opcional ou extensão compatível;
- alteração `major`: mudança incompatível ou semântica.

### 3.2 Regras

- consumidor não deve aceitar silenciosamente versão major incompatível;
- campos desconhecidos devem ser preservados ou ignorados sem executar efeitos;
- depreciação deve ser declarada;
- versão anterior congelada deve permanecer identificável;
- conversão entre versões deve ser rastreada;
- versão major incompatível produz `ERROR/FORMAT`;
- comparação de versões permanece tecnologicamente neutra.

---

## 4. ENVELOPE UNIVERSAL DE REQUISIÇÃO

```yaml
request:
  schema_version: SemanticVersion

  request_id: string
  created_at: datetime | logical_sequence
  project_id: string
  component_id: string
  function_id: string
  operation: string

  requester:
    actor_id: string | null
    role: string
    authority_basis: string

  scope:
    object_ids: [string]
    allowed_operations: [string]
    prohibited_operations: [string]
    boundaries: [string]

  inputs:
    items: [InputItem]

  context:
    items: [ContextItem]

  dependencies:
    items: [DependencyItem]

  constraints:
    intervention_level: string
    output_format: string | null
    language: string | null
    length_limit: integer | null
    privacy_classification: [SensitivityLabel]
    security_flags: [string]

  authorization:
    status: VALID | INVALID | UNVERIFIED | CONFLICTED
    evidence: [Reference]

  expected_output:
    type: string
    minimum_fields: [string]

  trace:
    parent_request_id: string | null
    workflow_id: string | null
```

### 4.1 Campos obrigatórios

São obrigatórios:

- `schema_version`;
- `request_id`;
- `project_id`;
- `component_id`;
- `function_id`;
- `operation`;
- `requester.role`;
- `scope.allowed_operations`;
- `scope.prohibited_operations`;
- `dependencies.items`;
- `authorization.status`;
- `authorization.evidence`;
- `expected_output.type`.

### 4.2 Regras

1. `request_id` deve ser único no fluxo.
2. `project_id` impede contaminação entre projetos.
3. `component_id` deve corresponder ao componente vigente.
4. `function_id` deve pertencer ao `component_id`.
5. `function_id` deve ser compatível com `operation`.
6. `function_id` desconhecido não pode ser aceito por inferência.
7. divergência entre função, componente e operação produz `ERROR/VALIDATION`.
8. `operation` deve constar entre as operações autorizadas.
9. operação presente simultaneamente em `allowed_operations` e `prohibited_operations` é inválida e produz `ERROR/VALIDATION`.
10. operação proibida prevalece sobre autorização genérica.
11. autorização `INVALID`, `UNVERIFIED` ou `CONFLICTED` impede operações que exijam autoridade validada.
12. autorização `VALID` exige ao menos uma `Reference` com `provenance_status=VERIFIED`.
13. autorização válida deve permanecer vinculada ao objeto, operação, escopo e autoridade.
14. autorização não pode ser promovida a `VALID` por inferência.
15. referências `PARTIAL`, `UNKNOWN` ou `CONFLICTED` não sustentam sozinhas autorização válida.
16. ausência de campo obrigatório produz `ERROR/VALIDATION`.
17. ausência legítima de autoridade, sem falha formal, produz abstenção localizada.
18. dependência obrigatória ausente ou incompatível bloqueia somente o escopo realmente dependente.

---

## 5. SCHEMA DE DEPENDÊNCIA

```yaml
VersionRequirement:
  mode: EXACT | MINIMUM | COMPATIBLE_MAJOR | RANGE | ANY

  exact: SemanticVersion | null
  minimum: SemanticVersion | null
  compatible_major: integer | null

  range:
    minimum: SemanticVersion | null
    maximum: SemanticVersion | null
    include_minimum: boolean
    include_maximum: boolean

DependencyItem:
  dependency_id: string
  required_version: VersionRequirement
  observed_version: SemanticVersion | null

  required_state:
    HOMOLOGATED | ACTIVE | AVAILABLE

  observed_state: string

  compatibility_status:
    COMPATIBLE | INCOMPATIBLE | UNVERIFIED | NOT_APPLICABLE

  evidence: [Reference]
  operation_scope: [string]
```

### 5.1 Regras de versão requerida

- `mode=EXACT` exige `exact` preenchido;
- `mode=MINIMUM` exige `minimum` preenchido;
- `mode=COMPATIBLE_MAJOR` exige `compatible_major` preenchido;
- `mode=RANGE` exige pelo menos um limite;
- quando ambos os limites existirem, o mínimo não pode ser superior ao máximo;
- `mode=ANY` não exige versão específica;
- campos incompatíveis com o modo selecionado devem permanecer nulos;
- dependência que exige versão não pode ser declarada satisfeita sem `observed_version`;
- `compatibility_status=COMPATIBLE` exige comparação materialmente possível;
- `compatibility_status=NOT_APPLICABLE` somente é válido com `mode=ANY` ou quando a dependência não possuir versão aplicável;
- incompatibilidade deve permanecer explícita.

### 5.2 Regras de dependência

- `dependency_id` é obrigatório;
- `required_state` é obrigatório;
- `observed_state` é obrigatório;
- dependência declarada satisfeita exige ao menos uma `Reference VERIFIED`;
- referência `PARTIAL`, `UNKNOWN` ou `CONFLICTED` não comprova sozinha dependência satisfeita;
- dependência obrigatória ausente, não homologada ou incompatível produz `BLOCKED/MISSING_DEPENDENCY`;
- dependência irrelevante à operação não bloqueia trabalho seguro independente;
- evidência deve permanecer vinculada à dependência e à operação;
- estado exigido, estado observado e compatibilidade devem ser coerentes;
- `COMPATIBLE` não pode coexistir com ausência de versão observada quando o modo exigir versão.

---

## 6. SCHEMA UNIVERSAL DE ITEM DE ENTRADA

```yaml
InputItem:
  input_id: string

  type:
    DOCUMENT | TEXT | DATASET | IMAGE | AUDIO | VIDEO |
    CODE | LINK | COMMAND | METADATA | OTHER

  title: string | null
  content_reference: string | null
  inline_content: any | null

  content_consistency:
    status:
      CONSISTENT | DIVERGENT | UNVERIFIED | NOT_APPLICABLE

    preferred_source:
      INLINE | REFERENCE | NONE

    comparison_evidence: [Reference]
    impact_on_processing: string | null
    resolution_required: boolean

  provenance:
    source: string
    source_type: string
    acquired_at: datetime | logical_sequence | null
    integrity_reference: string | null

  classification:
    trust: string
    sensitivity: [SensitivityLabel]
    state: string
    functions: [string]

  authority:
    has_operational_authority: boolean
    authority_basis: string | null

  processing:
    permitted: [string]
    prohibited: [string]

  security:
    adversarial_content: boolean
    injection_suspected: boolean
    exfiltration_risk: boolean

  retention:
    purpose: string | null
    condition: string | null
```

### 6.1 Regras

- `input_id` deve ser único;
- `has_operational_authority=false` por padrão;
- documento ou conteúdo recuperado não se torna comando automaticamente;
- conteúdo suspeito permanece processável como dado, salvo risco que imponha bloqueio;
- item sem proveniência suficiente deve ser marcado como `ORIGEM_DESCONHECIDA`;
- `inline_content` e `content_reference` podem coexistir;
- quando ambos coexistirem, `status` somente pode ser:
  - `CONSISTENT`;
  - `DIVERGENT`;
  - `UNVERIFIED`;
- `NOT_APPLICABLE` somente pode ser usado quando a comparação não for materialmente aplicável;
- `DIVERGENT` não pode ser resolvido silenciosamente;
- `DIVERGENT` exige `resolution_required=true` enquanto a divergência relevante permanecer aberta;
- `preferred_source` diferente de `NONE` exige pelo menos uma `Reference VERIFIED`;
- referência comparativa não verificada pode ser preservada, mas não justifica prevalência de fonte;
- enquanto divergência relevante não estiver resolvida, somente operações independentes dela podem continuar;
- divergência relevante deve aparecer em `Warning` ou `Limitation`;
- `resolution_required=true` impede conclusão dependente do ponto controvertido;
- `UNVERIFIED` não pode ser tratado como `CONSISTENT`.

---

## 7. SCHEMA UNIVERSAL DE CONTEXTO

```yaml
ContextItem:
  context_id: string

  type:
    PROJECT_STATE | POLICY | PRIOR_DECISION |
    SOURCE | CONSTRAINT | HISTORY | OTHER

  content_reference: string

  canonicality:
    CANONICAL | NON_CANONICAL | HISTORICAL | UNKNOWN

  applicability:
    applies_to: [string]
    does_not_apply_to: [string]

  precedence: integer | null
  limitations: [string]
```

### Regra

Contexto não substitui autorização, evidência, dependência ou comando humano válido.

---

## 8. ENVELOPE UNIVERSAL DE RESPOSTA

```yaml
response:
  schema_version: SemanticVersion

  response_id: string
  request_id: string
  project_id: string
  component_id: string
  function_id: string

  status:
    SUCCESS | PARTIAL_SUCCESS | ABSTAINED | ERROR | BLOCKED

  produced_at: datetime | logical_sequence

  result:
    type: string
    content: any | null
    structured_items: [ResultItem]

  safe_result:
    available: boolean
    content: any | null
    reference: Reference | null
    scope: [string]
    limitations: [Limitation]

  error: ErrorPayload | null
  abstention: AbstentionPayload | null
  block: BlockPayload | null

  evidence:
    claims: [ClaimEvidence]

  interventions:
    items: [InterventionRecord]

  limitations: [Limitation]
  warnings: [Warning]

  security:
    sensitive_content_present: boolean
    sensitivity_labels: [SensitivityLabel]
    adversarial_content_detected: boolean
    output_sanitized: boolean

  trace:
    input_ids: [string]
    source_references: [Reference]
    decision_references: [Reference]
    dependency_references: [Reference]

  next_action:
    required: boolean
    type: string | null
    description: string | null

  completion:
    scope_completed: [string]
    scope_not_completed: [string]
    partiality_cause: string | null
```

### 8.1 Correspondência obrigatória

- `response.request_id` deve corresponder à requisição;
- `response.project_id` deve ser idêntico a `request.project_id`;
- `response.component_id` deve ser idêntico a `request.component_id`;
- `response.function_id` deve corresponder à função da requisição;
- não é permitida mudança de componente dentro da mesma relação request–response.

Uma operação destinada a outro componente exige:

- encerramento ou resposta do pedido vigente;
- nova requisição;
- novo `request_id`;
- novo `component_id`;
- autorização própria;
- escopo próprio;
- dependências próprias.

### 8.2 Coerência entre status e payload

#### `SUCCESS`

Exige:

- `error=null`;
- `abstention=null`;
- `block=null`;
- `safe_result.available=false`;
- `scope_not_completed` vazio;
- `partiality_cause=null`;
- operação integralmente concluída;
- nenhuma limitação materialmente impeditiva.

#### `PARTIAL_SUCCESS`

Exige:

- `error=null`;
- `abstention=null`;
- `block=null`;
- `safe_result.available=false`;
- `scope_completed` com pelo menos um item;
- `scope_not_completed` com pelo menos um item;
- `partiality_cause` não nulo;
- limitações ou avisos compatíveis com a parcialidade.

#### `ERROR`

Exige:

- `error` preenchido;
- `abstention=null`;
- `block=null`;
- `safe_result` coerente com a existência ou não de resultado seguro preservado.

#### `ABSTAINED`

Exige:

- `abstention` preenchido;
- `error=null`;
- `block=null`;
- `safe_result.available=false`.

#### `BLOCKED`

Exige:

- `block` preenchido;
- `error=null`;
- `abstention=null`;
- `safe_result.available=false`.

Nenhum mesmo evento pode receber simultaneamente `ERROR`, `ABSTAINED` e `BLOCKED`.

---

## 9. RESULTADO SEGURO EM RESPOSTA DE ERRO

### 9.1 Regras

Quando `status=ERROR` e `safe_result.available=true`:

- `safe_result.content` ou `safe_result.reference` deve estar preenchido;
- pelo menos um dos dois deve existir;
- `safe_result.reference`, quando utilizada, deve ser `VERIFIED`;
- `safe_result.scope` deve conter pelo menos um item;
- `safe_result.limitations` deve explicar o alcance e os limites do resultado preservado;
- o resultado seguro permanece separado do resultado global;
- a existência de resultado seguro não converte `ERROR` em `PARTIAL_SUCCESS`.

Quando `safe_result.available=false`:

- `safe_result.content=null`;
- `safe_result.reference=null`;
- `safe_result.scope` deve estar vazio;
- `safe_result.limitations` pode estar vazio.

`ErrorPayload` não contém indicador concorrente de saída segura. `safe_result` é a única fonte de verdade para essa informação.

---

## 10. ESTADOS DA RESPOSTA

### 10.1 `SUCCESS`

Aplicável quando:

- operação autorizada;
- entradas suficientes;
- dependências satisfeitas;
- processamento concluído;
- saída atende aos campos mínimos;
- nenhuma lacuna impede o resultado.

### 10.2 `PARTIAL_SUCCESS`

Aplicável quando:

- parte segura e válida foi concluída;
- parte do escopo permaneceu aberta;
- o conteúdo parcial é útil e claramente delimitado;
- a causa da parcialidade é registrada;
- a falha não exige estado global `ERROR`;
- não há impedimento material total.

### 10.3 `ABSTAINED`

Aplicável quando a não execução decorre de decisão controlada, sem falha estrutural e sem impedimento material externo.

### 10.4 `ERROR`

Aplicável quando houve falha do processo, schema, integridade, validação, formato, processamento ou execução.

### 10.5 `BLOCKED`

Aplicável quando a operação não pode prosseguir por impedimento material externo, documental ou de governança comprovado por evidência verificada.

---

## 11. FRONTEIRA ENTRE ERRO, ABSTENÇÃO E BLOQUEIO

### 11.1 `ERROR/AUTHORIZATION`

Usar quando houver falha na:

- estrutura da autorização;
- assinatura;
- referência;
- integridade;
- validade formal;
- leitura;
- processamento;
- correspondência entre autorização e objeto.

### 11.2 `ABSTAINED/INSUFFICIENT_AUTHORITY`

Usar quando:

- autorização estiver ausente ou insuficiente;
- não houver falha formal;
- não houver impedimento material externo;
- a operação depender de autoridade adicional.

### 11.3 `ABSTAINED/UNRESOLVED_CONFLICT`

Usar quando:

- houver conflito localizado de autoridade;
- o ponto controvertido não puder ser decidido sem inferência;
- o restante seguro puder continuar.

### 11.4 `BLOCKED/GOVERNANCE_CONFLICT`

Usar somente quando:

- o conflito impedir objetivamente a operação;
- houver ao menos uma `Reference VERIFIED`;
- nenhum caminho seguro independente permitir continuar o escopo afetado.

### 11.5 `BLOCKED/ACCESS_DENIED`

Usar quando:

- acesso materialmente necessário for negado;
- a negativa estiver comprovada por ao menos uma `Reference VERIFIED`;
- a operação depender diretamente desse acesso.

### 11.6 Regra de exclusividade

O mesmo evento não pode ser classificado simultaneamente como erro, abstenção e bloqueio.

---

## 12. SCHEMA DE AFIRMAÇÃO E EVIDÊNCIA

```yaml
ClaimEvidence:
  claim_id: string
  claim_text: string

  claim_type:
    FACT | INTERPRETATION | RECOMMENDATION |
    INFERENCE | LIMITATION

  evidence_ids: [string]
  source_references: [Reference]

  location:
    page: string | null
    section: string | null
    timestamp: string | null
    record: string | null

  sufficiency:
    SUFFICIENT | PARTIAL | INSUFFICIENT | NOT_APPLICABLE

  confidence:
    HIGH | MEDIUM | LOW | UNDETERMINED

  status:
    SUPPORTED | PARTIALLY_SUPPORTED |
    UNSUPPORTED | CONFLICTED

  notes: string | null
```

### 12.1 Regras

- afirmação factual deve possuir evidência ou ser marcada como não sustentada;
- inferência deve ser identificada;
- ausência de fonte não pode ser ocultada;
- conflito entre fontes deve ser representado como `CONFLICTED`;
- confiança não substitui suficiência;
- `SUPPORTED` exige suficiência compatível;
- claim conflitante deve preservar referências de todas as fontes relevantes.

---

## 13. SCHEMA DE INTERVENÇÃO

```yaml
InterventionRecord:
  intervention_id: string
  target_id: string
  requested_level: string
  applied_level: string | null
  authority_status: string
  operation: string

  disposition:
    APPLIED | REFUSED | ABSTAINED | BLOCKED

  before_reference: string | null
  after_reference: string | null
  rationale: string
  reversible: boolean
  requires_human_decision: boolean
```

### 13.1 Regras gerais

- `requested_level` registra somente o nível solicitado e não comprova execução;
- nível efetivamente aplicado não pode exceder o nível autorizado;
- recomendação não pode ser registrada como execução;
- execução não pode ser registrada como homologação;
- intervenção reversível aplicada deve preservar o estado anterior;
- mudança de nível exige nova autoridade;
- recusa, abstenção ou bloqueio não podem ser contabilizados como intervenção aplicada;
- `applied_level` não nulo com `disposition` diferente de `APPLIED` torna o registro inválido;
- `disposition=APPLIED` com `applied_level=null` torna o registro inválido;
- `before_reference` e `after_reference` devem permanecer coerentes com a disposição.

### 13.2 `disposition=APPLIED`

Exige:

- `applied_level` não nulo;
- `applied_level` representa exclusivamente o nível efetivamente aplicado;
- `applied_level` não pode exceder `requested_level`;
- a intervenção deve estar autorizada;
- `after_reference` deve identificar o resultado da intervenção quando aplicável;
- `before_reference` deve preservar o estado anterior quando necessário à reversibilidade.

### 13.3 `disposition=REFUSED`

Exige:

- `applied_level=null`;
- nenhuma transformação registrada como executada;
- `rationale` explicando objetivamente a recusa;
- `after_reference=null` quando representaria transformação inexistente.

### 13.4 `disposition=ABSTAINED`

Exige:

- `applied_level=null`;
- nenhuma transformação registrada como executada;
- `rationale` identificando a insuficiência de autoridade, evidência, escopo ou condição aplicável;
- `after_reference=null` quando representaria transformação inexistente.

### 13.5 `disposition=BLOCKED`

Exige:

- `applied_level=null`;
- nenhuma transformação registrada como executada;
- `rationale` identificando o impedimento material;
- `after_reference=null` quando representaria transformação inexistente;
- o bloqueio correspondente deve ser representado no payload apropriado quando afetar o estado global da resposta.

---

## 14. SCHEMA DE ERRO

```yaml
ErrorPayload:
  error_id: string
  request_id: string

  category:
    VALIDATION | INTEGRITY | DEPENDENCY |
    AUTHORIZATION | SECURITY | PROCESSING |
    FORMAT | RESOURCE | INTERNAL

  code: string

  severity:
    INFO | WARNING | MAJOR | CRITICAL

  message: string
  technical_detail: string | null
  affected_scope: [string]
  recoverable: boolean
  retry_allowed: boolean
  retry_conditions: [string]
  data_preserved: boolean
  evidence_preserved: boolean

  required_action:
    actor: string | null
    action: string | null

  trace:
    input_ids: [string]
    event_references: [string]
```

### 14.1 Regras

1. erro não deve ocultar resultado seguro já produzido;
2. falha localizada não deve converter automaticamente todo o escopo em falha global;
3. erro crítico impede continuação no escopo afetado;
4. `retry_allowed=true` exige ao menos uma condição explícita;
5. `retry_allowed=false` exige `retry_conditions` vazio;
6. erro de autorização não pode ser resolvido por inferência;
7. erro de segurança deve preservar evidência;
8. erro deve conter categoria e código;
9. erro de dependência estrutural não substitui bloqueio material por dependência ausente;
10. resultado seguro é representado exclusivamente por `safe_result`.

---

## 15. SCHEMA DE ABSTENÇÃO

```yaml
AbstentionPayload:
  abstention_id: string
  request_id: string

  category:
    INSUFFICIENT_AUTHORITY | INSUFFICIENT_EVIDENCE |
    UNKNOWN_PROVENANCE | OUT_OF_SCOPE | SAFETY_RISK |
    PRIVACY_RISK | UNRESOLVED_CONFLICT |
    AMBIGUITY | POLICY_CONSTRAINT

  scope: [string]
  reason: string
  triggering_conditions: [string]
  completed_safe_work: [string]
  unperformed_work: [string]
  evidence_required: [string]
  authorization_required: [string]
  clarification_required: [string]
  reversible: boolean
  resume_conditions: [string]
  human_decision_required: boolean
```

### 15.1 Regras

- deve ser localizada ao ponto inseguro ou indeterminado;
- deve registrar trabalho seguro concluído;
- não pode ser usada para evitar tarefa autorizada e executável;
- deve indicar condição objetiva de retomada quando reversível;
- não pode inventar autorização ou evidência;
- abstenção total exige demonstração de que nenhum segmento seguro é executável;
- `reversible=true` exige `resume_conditions` com ao menos um item;
- `reversible=false` exige justificativa suficiente em `reason`.

---

## 16. SCHEMA DE BLOQUEIO

```yaml
BlockPayload:
  block_id: string
  request_id: string

  category:
    MISSING_OBJECT | MISSING_DEPENDENCY |
    ACCESS_DENIED | CANONICAL_SOURCE_ABSENT |
    INCIDENT_ACTIVE | FROZEN_OBJECT |
    GOVERNANCE_CONFLICT

  description: string
  material_evidence: [Reference]
  affected_scope: [string]
  removable: boolean
  removal_action: string | null
  responsible_actor: string | null
  safe_work_remaining: [string]
  total_block_justification: string | null
```

### 16.1 Regras

- bloqueio exige impedimento material;
- `material_evidence` deve conter ao menos uma `Reference VERIFIED`;
- referências não verificadas podem ser preservadas, mas não sustentam sozinhas bloqueio conclusivo;
- sem evidência verificada, não se declara `BLOCKED`;
- `removable=true` exige `removal_action` não nulo, específico e objetivo;
- `safe_work_remaining` deve ser sempre preenchido;
- bloqueio deve limitar-se ao escopo afetado;
- bloqueio total exige:
  - `safe_work_remaining` vazio;
  - `total_block_justification` não nulo;
- bloqueio parcial exige identificação do trabalho seguro restante.

---

## 17. SCHEMA DE LIMITAÇÃO

```yaml
Limitation:
  limitation_id: string

  type:
    DATA | SOURCE | METHOD | SCOPE |
    AUTHORITY | PRIVACY | SECURITY |
    TECHNOLOGY | LEGAL | INSTITUTIONAL

  description: string
  effect_on_result: string
  affected_items: [string]

  materiality:
    LOW | MEDIUM | HIGH

  can_be_resolved: boolean
  resolution_condition: string | null
```

### Regra

Limitação deve informar explicitamente seu efeito sobre o resultado.

Limitação de materialidade alta incompatível com conclusão integral impede `SUCCESS`.

---

## 18. SCHEMA DE AVISO

```yaml
Warning:
  warning_id: string

  category:
    UNCERTAINTY | CONFLICT | SENSITIVITY |
    SECURITY | PARTIALITY | DEPRECATION |
    VERSION_DIVERGENCE

  message: string
  affected_items: [string]
  requires_action: boolean
```

### Regra

Aviso não substitui erro, abstenção, bloqueio ou limitação.

---

## 19. SCHEMA DE REFERÊNCIA

```yaml
Reference:
  reference_id: string
  object_id: string
  object_type: string
  version: SemanticVersion | null
  integrity_reference: string | null

  location:
    page: string | null
    section: string | null
    timestamp: string | null
    record: string | null

  provenance_status:
    VERIFIED | PARTIAL | UNKNOWN | CONFLICTED
```

### 19.1 Regra transversal de qualidade da evidência

Somente `Reference` com `provenance_status=VERIFIED` pode sustentar conclusivamente:

- autorização `VALID`;
- dependência declarada satisfeita;
- `preferred_source` diferente de `NONE`;
- bloqueio material;
- resultado seguro referenciado;
- qualquer exceção operacional que exija prova material.

Referências `PARTIAL`, `UNKNOWN` ou `CONFLICTED`:

- permanecem preservadas;
- podem sustentar alerta, limitação, conflito ou evidência insuficiente;
- não podem, sozinhas, produzir autoridade, prevalência, compatibilidade ou bloqueio conclusivo.

---

## 20. VOCABULÁRIO CONTROLADO DE SENSIBILIDADE

```yaml
SensitivityLabel:
  category:
    PUBLIC | INTERNAL | RESTRICTED | CONFIDENTIAL |
    PERSONAL_DATA | SENSITIVE_PERSONAL_DATA |
    SECURITY_SENSITIVE | LEGALLY_PROTECTED |
    OTHER_CONTROLLED

  source_policy: string
  justification: string | null
```

### 20.1 Regras

- `sensitive_content_present=true` exige ao menos um `SensitivityLabel`;
- `source_policy` deve identificar a política aplicável;
- quando pertinente, deve identificar P08;
- `OTHER_CONTROLLED` exige `justification` não nula;
- valores fora do vocabulário são inválidos;
- sanitização não elimina automaticamente classificação residual;
- rótulos preservam, sem substituir, as categorias substantivas do P08;
- saída sanitizada deve registrar `output_sanitized=true`;
- conteúdo adversarial detectado deve permanecer marcado.

---

## 21. INVARIANTES INTERSCHEMAS

1. `response.request_id` deve corresponder à requisição.
2. `response.project_id` deve ser idêntico a `request.project_id`.
3. `response.component_id` deve ser idêntico a `request.component_id`.
4. mudança de componente exige nova requisição e novo `request_id`.
5. `function_id` deve pertencer ao componente e ser compatível com a operação.
6. `SUCCESS` não pode coexistir com erro, abstenção, bloqueio ou resultado seguro residual.
7. `ABSTAINED` exige `AbstentionPayload`.
8. `ERROR` exige `ErrorPayload`.
9. `BLOCKED` exige `BlockPayload`.
10. `PARTIAL_SUCCESS` exige escopo concluído, não concluído e causa.
11. afirmação factual relevante deve possuir `claim_id`.
12. intervenção deve possuir nível solicitado, autoridade e disposição.
13. `disposition=APPLIED` exige `applied_level` não nulo.
14. `REFUSED`, `ABSTAINED` ou `BLOCKED` exigem `applied_level=null`.
15. intervenção não aplicada não pode conter `after_reference` que represente transformação inexistente.
16. conteúdo adversarial deve permanecer marcado.
17. objeto congelado não pode ser transformado sem reabertura válida.
18. autorização de análise não implica transformação.
19. autorização de transformação não implica publicação.
20. ausência de evidência não pode resultar em `SUPPORTED`.
21. origem desconhecida não pode resultar em confiança alta sem validação.
22. saída sanitizada deve registrar sanitização.
23. dados pseudonimizados não são automaticamente anônimos.
24. conflito aberto deve aparecer em limitação ou aviso.
25. campos desconhecidos não podem produzir efeitos operacionais.
26. schema inválido deve falhar explicitamente.
27. autorização `VALID` exige ao menos uma `Reference VERIFIED`.
28. dependência satisfeita exige ao menos uma `Reference VERIFIED`.
29. bloqueio exige ao menos uma `Reference VERIFIED`.
30. fonte preferencial exige ao menos uma `Reference VERIFIED`.
31. bloqueio removível exige ação de remoção.
32. divergência inline/reference não pode ser resolvida silenciosamente.
33. sensibilidade presente exige rótulo controlado.
34. erro, abstenção e bloqueio são mutuamente exclusivos.
35. versão major incompatível produz erro explícito.
36. dependência sujeita a versão exige compatibilidade representada.
37. `NOT_APPLICABLE` não pode ser usado quando inline e referência coexistirem.
38. `DIVERGENT` aberto exige `resolution_required=true`.
39. `safe_result.available=true` exige conteúdo ou referência.
40. referência de resultado seguro deve ser `VERIFIED`.
41. `safe_result.available=false` exige conteúdo e referência nulos.
42. resultado seguro não converte `ERROR` em `PARTIAL_SUCCESS`.
43. limitação impeditiva não pode coexistir com `SUCCESS`.

---

## 22. REGRAS DE VALIDAÇÃO

### 22.1 Requisição válida

Uma requisição é válida quando:

- campos obrigatórios existem;
- tipos são compatíveis;
- identificadores são únicos;
- `schema_version` usa `SemanticVersion`;
- escopo é coerente;
- função pertence ao componente;
- função é compatível com a operação;
- operação é autorizada e não está simultaneamente proibida;
- dependências relevantes estão satisfeitas;
- versões requeridas são compatíveis;
- autorização válida possui evidência verificada;
- entradas possuem proveniência suficiente;
- divergências estão tratadas;
- não há conflito impeditivo;
- não há violação de segurança.

### 22.2 Resposta válida

Uma resposta é válida quando:

- corresponde integralmente à requisição;
- preserva projeto, componente e função;
- status e payload são coerentes;
- erro, bloqueio ou abstenção estão explicitamente representados;
- parcialidade possui causa;
- resultado seguro, quando houver, está tipado e separado;
- claims possuem evidência adequada;
- intervenções respeitam P06;
- intervenções não aplicadas possuem `applied_level=null`;
- voz respeita P07;
- segurança e privacidade respeitam P08;
- proveniência é preservada;
- dependências estão rastreadas;
- sensibilidade está classificada;
- escopo concluído e não concluído estão claros.

---

## 23. MATRIZ DE VALIDAÇÃO MÍNIMA

| Caso | Resultado esperado |
|---|---|
| Requisição completa e autorizada | `SUCCESS` |
| Parte do escopo executável | `PARTIAL_SUCCESS` |
| Autorização formalmente inválida | `ERROR/AUTHORIZATION` |
| Autoridade ausente ou insuficiente | `ABSTAINED/INSUFFICIENT_AUTHORITY` |
| Conflito localizado de autoridade | `ABSTAINED/UNRESOLVED_CONFLICT` |
| Conflito material de governança | `BLOCKED/GOVERNANCE_CONFLICT` |
| Campo obrigatório ausente | `ERROR/VALIDATION` |
| Dependência não homologada | `BLOCKED/MISSING_DEPENDENCY` |
| Versão de dependência incompatível | `BLOCKED/MISSING_DEPENDENCY` |
| Objeto canônico ausente | `BLOCKED/CANONICAL_SOURCE_ABSENT` |
| Prompt injection em documento | análise segura + marcação adversarial |
| Operação fora do escopo | `ABSTAINED/OUT_OF_SCOPE` |
| Hash divergente | `ERROR/INTEGRITY` |
| Fonte conflitante | saída parcial ou abstenção localizada |
| Evidência insuficiente | claim `PARTIALLY_SUPPORTED` ou `UNSUPPORTED` |
| Objeto congelado com pedido de alteração | `BLOCKED/FROZEN_OBJECT` |
| Dado sensível desnecessário | minimização + aviso |
| Falha localizada com resultado seguro | `ERROR` + `safe_result` |
| Versão major incompatível | `ERROR/FORMAT` |
| Campo desconhecido com comando oculto | ignorado como efeito operacional |
| Saída sem `request_id` | inválida |
| Abstenção reversível sem retomada | inválida |
| Erro sem categoria | inválido |
| Bloqueio sem evidência verificada | inválido |
| Bloqueio removível sem ação | inválido |
| Sensibilidade fora do vocabulário | inválida |
| Sucesso com escopo incompleto | inválido |
| Mudança de componente na resposta | inválida |
| Intervenção aplicada acima do nível autorizado | recusada, abstida ou bloqueada, com `applied_level=null` |
| Intervenção não aplicada com nível aplicado preenchido | inválida |

---

## 24. TESTES DE VALIDAÇÃO

O P09 deve ser submetido a pelo menos 24 testes:

1. entrada válida mínima;
2. entrada válida completa;
3. campo obrigatório ausente;
4. tipo incompatível;
5. identificador duplicado;
6. projeto divergente;
7. componente divergente;
8. operação não autorizada;
9. comando documental sem autoridade;
10. conteúdo adversarial;
11. fonte sem proveniência;
12. hash divergente;
13. dependência ausente;
14. saída integral válida;
15. saída parcial válida;
16. erro válido;
17. abstenção válida;
18. bloqueio válido;
19. afirmação sem evidência;
20. intervenção acima do nível autorizado;
21. dado sensível em saída;
22. versão incompatível;
23. conflito entre fontes;
24. objeto congelado.

### 24.1 Critério global

O P09 somente é substantivamente aprovado quando:

- todos os testes forem executáveis;
- nenhum teste for reprovado;
- nenhum teste estiver bloqueado;
- nenhum erro estrutural permanecer;
- sucesso, parcialidade, erro, abstenção e bloqueio forem inequivocamente distintos;
- intervenções solicitadas e intervenções efetivamente aplicadas forem inequivocamente distinguíveis;
- resultados seguros forem materialmente representáveis;
- dependências e versões forem verificáveis;
- contratos preservarem P03–P08;
- não houver escalonamento automático de autoridade;
- não houver perda silenciosa de proveniência;
- não houver contaminação entre projetos.

---

## 25. LACUNAS LEGÍTIMAS PRESERVADAS

O P09 não define:

- linguagem concreta de schema;
- JSON Schema, YAML Schema, Protobuf, Avro ou equivalente;
- API;
- protocolo de transporte;
- banco de dados;
- mecanismo concreto de autenticação;
- formato físico de timestamp;
- algoritmo de hash;
- identificador global;
- infraestrutura de logs;
- mecanismo de assinatura;
- linguagem de programação;
- provedor ou modelo de LLM;
- método técnico de preservação de campos desconhecidos;
- formato concreto de referência de integridade;
- biblioteca ou algoritmo concreto de comparação de versões.

Essas decisões pertencem à implementação posterior.

---

## 26. ESTADO SUBSTANTIVO

```text
P09_TERCEIRA_CORRECAO_LOCALIZADA_CONCLUIDA
P09_SUBSTANTIVAMENTE_COMPLETO
P09_PRONTO_PARA_VERIFICACAO_FINAL_LIMITADA
P09_NAO_HOMOLOGADO
P00–P08_PRESERVADOS
R03_INALTERADA
P10–P28_NAO_INICIADOS
```

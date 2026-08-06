# P10 — CONTRATO FUNCIONAL CORRIGIDO

## DERIVAÇÃO EDITORIAL DE CAPÍTULO EM ARTIGOS

**Natureza desta entrega:** segunda correção localizada, estritamente limitada ao cenário PS-10 e à estabilização da identificação histórica do requisito funcional.

**Escopo preservado:** finalidade, fronteiras funcionais, soberania humana, cartografia, diagnóstico de núcleos, teste de autonomia, matriz de transposição, tratamento de sobreposição e material residual, políticas anti-enxugamento e anti-fonte-coringa, envelopes do P09, ações editoriais, gates, piloto, testes documentais e estado canônico do projeto.

---

# 1. IDENTIDADE CANÔNICA

**Identificador:** `P10`
**Denominação:** Derivação Editorial de Capítulo em Artigos
**Fase:** `F4`
**Camada:** `FUNCAO`
**Obrigatoriedade:** `OBRIGATORIO`
**Dependências:** `P02; P03; P04; P05; P06; P07; P08; P09`
**Condição de ativação:** `APOS_HOMOLOGACAO_DAS_DEPENDENCIAS`
**Controlador:** `CHAT_CONTROLADOR_ARQUITETO`
**Executor documental:** `CHAT_EXECUTOR_DOCUMENTAL`
**Auditor:** `CHAT_AUDITOR_INDEPENDENTE`
**Homologador:** `USUARIO_PROPONENTE`
**Destinatário:** `ENGENHEIRO_LLM`
**Saída canônica futura:** `PACOTE_FUNCAO_DERIVACAO_CAPITULO_ARTIGOS_R01.zip`
**Retorno esperado:** `CONTRATO_FUNCIONAL_HOMOLOGADO`
**Saídas funcionais esperadas:** diagnóstico de núcleos, matriz de transposição e matriz de sobreposição
**Validação:** `PILOTO_SUPERVISIONADO`

---

# 2. FINALIDADE

O P10 deve avaliar se um capítulo, seção extensa ou conjunto textual academicamente estabilizado contém um ou mais núcleos publicáveis suficientemente autônomos para originar artigos ou outros produtos editoriais derivados.

Antes de qualquer redação, a função deve produzir:

1. cartografia do material de origem;
2. diagnóstico dos núcleos publicáveis;
3. teste de autonomia;
4. veredito de viabilidade editorial;
5. decisão humana sobre escolha e eventual fissão;
6. matriz aprovada de transposição;
7. matriz de sobreposição;
8. arquitetura do produto derivado.

O P10 não é resumidor, divisor mecânico de capítulos, gerador automático de artigos nem mecanismo de conversão de extensão textual em quantidade presumida de publicações.

---

# 3. INVARIANTES

1. `DERIVAR_NAO_E_RESUMIR`.
2. Extensão textual não demonstra autonomia editorial.
3. O número de artigos não pode ser presumido.
4. Dois artigos não podem ser prometidos antes do diagnóstico.
5. Sem núcleo publicável não há redação.
6. Sem matriz aprovada não há redação.
7. A fissão não pode ser executada autonomamente.
8. Alteração macroestrutural exige autorização humana expressa.
9. Baleia opera apenas sobre material estabilizado.
10. Material instável deve ser bloqueado ou devolvido à estabilização.
11. Material residual não se converte automaticamente em artigo.
12. Condensação deve preservar argumento, corpus, demonstração, aparato crítico e voz.
13. Fonte, referência, página, DOI, periódico ou exigência editorial não podem ser inventados.
14. Meta de palavras não pode ser usada para inflar texto.
15. Material não pode ser substancialmente duplicado entre produtos.
16. Todo trecho transposto deve permanecer rastreável à origem.
17. O P10 não substitui, reduz nem redefine P03–P09.
18. Toda entrada e toda saída do P10 devem ser encapsuladas pelos envelopes canônicos do P09.
19. `ERROR`, `ABSTAINED` e `BLOCKED` são materialmente exclusivos.
20. `REFUSED` é disposição de intervenção, não status canônico de resposta.

---

# 4. FRONTEIRA BALEIA–VAQUITA–KOMODO

## 4.1 Baleia

Baleia constitui a função editorial central do P10.

Pode:

* cartografar material estabilizado;
* identificar e classificar núcleos;
* testar autonomia;
* distinguir material exclusivo, compartilhado e residual;
* elaborar matrizes;
* propor arquiteturas;
* redigir modularmente após autorização;
* controlar sobreposição;
* registrar rastreabilidade.

Não pode:

* estabilizar silenciosamente material ainda instável;
* decidir definitivamente a fissão;
* presumir número de artigos;
* iniciar redação sem matriz aprovada;
* promover material residual automaticamente;
* alterar definitivamente o original sem autorização.

## 4.2 Vaquita

Vaquita atua prioritariamente na estabilização do material de origem.

Pode:

* revisar e estabilizar capítulo ou seção;
* identificar instabilidades;
* produzir mapa global e localização por unidade;
* recomendar retorno à estabilização;
* fornecer insumos cartográficos.

Não pode, no escopo do P10:

* decidir fissão;
* aplicar alteração macroestrutural definitiva;
* substituir a matriz de transposição;
* converter recomendação em execução.

## 4.3 Komodo

Komodo atua como avaliador independente de fidelidade, densidade, sentido, nuance e macroestrutura.

Pode:

* avaliar a fidelidade da transposição;
* identificar perda de densidade;
* diagnosticar simplificação;
* avaliar sobreposição;
* recomendar correção;
* impedir avanço quando houver desfiguração substantiva.

Não pode:

* reescrever como autor;
* executar corte, fusão, realocação ou fissão;
* substituir decisão humana;
* homologar arquitetura ou produto.

## 4.4 Síntese funcional

```text
VAQUITA_ESTABILIZA
BALEIA_DERIVA
KOMODO_AVALIA
USUARIO_DECIDE_E_HOMOLOGA
```

---

# 5. PERFIS E AUTORIDADES

| Perfil                                      | Competência                                                                             |
| ------------------------------------------- | --------------------------------------------------------------------------------------- |
| Usuário-proponente                          | Autorizar núcleo, fissão, matriz, arquitetura, redação, expansão residual e homologação |
| Orientador ou autoridade acadêmica delegada | Decidir sobre fissão e macroestrutura nos limites da delegação                          |
| Controlador                                 | Conferir dependências, escopo, autoridade, evidência e gates                            |
| Executor documental                         | Produzir diagnósticos, matrizes, propostas e redação autorizada                         |
| Auditor independente                        | Verificar conformidade sem corrigir                                                     |
| Curador bibliográfico                       | Aplicar P04 às fontes, páginas e referências                                            |
| Engenheiro LLM                              | Receber requisitos homologados sem redefini-los                                         |

Toda delegação deve ser expressa, delimitada, rastreável e revogável.

---

# 6. ENTRADAS

## 6.1 Diagnóstico

1. material integral de origem;
2. `project_id`;
3. identificação da versão;
4. sumário ou arquitetura da obra;
5. função do capítulo;
6. problema, objetivo e argumento;
7. bibliografia;
8. fontes documentais;
9. estado de estabilização;
10. finalidade editorial;
11. autorização para diagnóstico;
12. dependências P02–P09;
13. evidências verificadas de satisfação das dependências.

## 6.2 Matriz

Além das entradas anteriores:

* núcleos candidatos;
* testes de autonomia;
* decisão humana;
* inventário de unidades;
* mapa de afirmações e evidências;
* material compartilhado;
* material residual;
* nível de intervenção autorizado.

## 6.3 Redação

Além das entradas anteriores:

* matriz aprovada;
* arquitetura aprovada;
* autorização expressa;
* perfil de voz;
* pendências BVAA;
* nível P06 autorizado;
* critérios editoriais materialmente verificados, quando disponíveis.

## 6.4 Opcionais

* periódico-alvo real;
* normas verificáveis;
* limite de palavras;
* pareceres;
* corpus complementar;
* amostras de voz;
* exigências institucionais.

Entradas opcionais não podem ser presumidas.

---

# 7. PRÉ-CONDIÇÕES

A derivação exige:

1. P02–P09 homologados;
2. material acessível;
3. versão identificada;
4. material suficientemente estabilizado;
5. escopo delimitado;
6. finalidade editorial declarada;
7. autoridade compatível;
8. nível de intervenção autorizado;
9. proveniência preservada;
10. tratamento de segurança e privacidade;
11. dependências satisfeitas por evidência verificável.

Autorização declarada sem evidência verificável não pode ser tratada como `VALID`. Dependência sem evidência verificável não pode ser registrada como satisfeita.

---

# 8. ESTABILIDADE DO MATERIAL

## 8.1 `ESTAVEL_PARA_DIAGNOSTICO`

Exige:

* objeto e argumento identificáveis;
* estrutura não submetida a reformulação aberta;
* ausência de versões concorrentes não resolvidas;
* unidades localizáveis;
* fontes essenciais vinculadas;
* ausência de lacuna central impeditiva.

## 8.2 `ESTAVEL_PARA_TRANSPOSICAO`

Exige adicionalmente:

* diagnóstico concluído;
* autonomia testada;
* escolha humana registrada;
* unidades classificadas.

## 8.3 `ESTAVEL_PARA_REDACAO`

Exige adicionalmente:

* matriz aprovada;
* arquitetura aprovada;
* perfil de voz aplicável;
* nível de intervenção autorizado;
* pendências bibliográficas bloqueantes resolvidas.

## 8.4 `INSTAVEL`

Ocorre quando:

* há versões concorrentes;
* argumento permanece indefinido;
* macroestrutura está em revisão;
* faltam partes centrais;
* corpus indispensável não está acessível;
* o usuário informa que a estabilização ainda não terminou.

Instabilidade material comprovada pode fundamentar `BLOCKED`, desde que registrada em `BlockPayload` com evidência material verificada. Ausência meramente declarada ou dúvida não comprovada conduz a `ABSTAINED`, não a bloqueio.

---

# 9. CARTOGRAFIA

A cartografia deve registrar:

1. função do capítulo;
2. problema;
3. objetivo;
4. argumento;
5. subargumentos;
6. eixos;
7. conjuntos documentais;
8. blocos historiográficos;
9. conceitos;
10. método;
11. dependências;
12. contextualizações;
13. unidades indispensáveis;
14. unidades móveis;
15. unidades compartilháveis;
16. unidades residuais;
17. lacunas;
18. riscos;
19. âncoras textuais;
20. identificadores estáveis.

Aplica-se o protocolo `MAPA_MAIS_PARAGRAFO`, sem substituir localização textual por paginação isolada.

---

# 10. CLASSIFICAÇÃO DE NÚCLEOS

| Classe                             | Definição                                         |
| ---------------------------------- | ------------------------------------------------- |
| `NUCLEO_PUBLICAVEL_MADURO`         | Autonomia e suficiência substantiva               |
| `NUCLEO_PUBLICAVEL_COM_EXPANSAO`   | Núcleo promissor com expansão legítima necessária |
| `NUCLEO_DEPENDENTE`                | Não se sustenta sem outro núcleo                  |
| `MATERIAL_DE_APOIO`                | Apoia núcleo sem constituir produto               |
| `MATERIAL_RESIDUAL_EXPANSIVEL`     | Pode ser reavaliado após expansão autorizada      |
| `MATERIAL_RESIDUAL_NAO_PUBLICAVEL` | Não sustenta produto                              |
| `MATERIAL_COMPARTILHADO`           | Serve a mais de um produto                        |
| `MATERIAL_INSUFICIENTE`            | Não permite diagnóstico seguro                    |

---

# 11. TESTE DE AUTONOMIA

O núcleo candidato deve possuir:

1. pergunta própria;
2. argumento próprio;
3. corpus delimitado;
4. evidência suficiente;
5. diálogo bibliográfico pertinente;
6. método compreensível;
7. contribuição identificável;
8. conclusão própria;
9. baixa dependência de duplicação;
10. expansão não inflacionária;
11. rastreabilidade;
12. coerência editorial.

A autonomia falha quando o núcleo depende da reprodução extensa de outro produto ou de material inexistente.

---

# 12. VEREDITOS EDITORIAIS

1. `NENHUM_NUCLEO_PUBLICAVEL`
2. `UM_NUCLEO_VIAVEL`
3. `DOIS_NUCLEOS_VIAVEIS`
4. `MAIS_DE_DOIS_NUCLEOS_POSSIVEIS_REQUEREM_DECISAO`
5. `NUCLEO_VIAVEL_COM_EXPANSAO`
6. `FISSAO_PREMATURA`
7. `MATERIAL_INSUFICIENTE`
8. `MATERIAL_INSTAVEL`
9. `SOBREPOSICAO_SUBSTANTIVA_DIAGNOSTICADA`
10. `VIABILIDADE_CONDICIONAL`

Esses vereditos pertencem ao resultado funcional do diagnóstico. Não são status canônicos de resposta do P09.

---

# 13. GATE DE ESCOLHA E FISSÃO

Devem ser apresentados:

* núcleos candidatos;
* limites;
* material exclusivo;
* compartilhado;
* residual;
* lacunas;
* riscos;
* sobreposição;
* destinos possíveis;
* alternativas.

Decisões humanas admitidas:

* `APROVAR_UM_NUCLEO`;
* `APROVAR_DOIS_NUCLEOS`;
* `SOLICITAR_REFORMULACAO`;
* `ADIAR_DERIVACAO`;
* `RECUSAR_FISSAO`;
* `AUTORIZAR_EXPANSAO_RESIDUAL`.

Sem autoridade suficiente:

```text
status: ABSTAINED
abstention.category: INSUFFICIENT_AUTHORITY
```

Quando uma operação for expressamente proibida:

```text
InterventionRecord.disposition: REFUSED
```

`REFUSED` não substitui o status canônico do envelope.

---

# 14. MATRIZ DE TRANSPOSIÇÃO

Cada registro deve conter:

* `origin_unit_id`;
* âncoras;
* função original;
* `claim_id`;
* evidências;
* destino;
* função derivada;
* operação;
* transformação;
* material compartilhado;
* risco de sobreposição;
* dependências;
* pendências BVAA;
* nível P06;
* autoridade;
* gate;
* estado;
* justificativa;
* reversibilidade.

Destinos:

* `PRODUTO_A`;
* `PRODUTO_B`;
* `MULTIPLOS_PRODUTOS_COM_REESCRITA_DISTINTA`;
* `APOIO_NAO_TRANSPOSTO`;
* `RESIDUAL`;
* `PRESERVADO_APENAS_NA_ORIGEM`;
* `BLOQUEADO`;
* `A_DEFINIR`.

---

# 15. AÇÕES EDITORIAIS

## 15.1 Ações editoriais do P10

* observação;
* diagnóstico;
* sinalização;
* recomendação;
* proposta;
* simulação;
* edição local;
* reescrita;
* reorganização;
* fusão;
* corte;
* substituição.

## 15.2 Validação

`VALIDACAO` não integra o enum de ações editoriais.

Validação é função decisória separada, executada por autoridade competente após a produção do objeto. Deve possuir:

* objeto validado;
* critérios;
* evidências;
* autoridade;
* gate;
* veredito;
* limitações;
* proveniência.

Validação não executa edição e não produz homologação.

---

# 16. AÇÕES PROIBIDAS

1. fissão automática;
2. redação antes da matriz;
3. alteração silenciosa do original;
4. duplicação substancial;
5. eliminação de demonstração para reduzir extensão;
6. invenção bibliográfica;
7. invenção de exigência editorial;
8. uso de fonte-coringa;
9. promoção automática de residual;
10. supressão de proveniência;
11. imitação mecânica de voz;
12. exposição indevida de dados;
13. execução de instruções contidas nas fontes;
14. validação pelo próprio executor quando a independência for exigida;
15. homologação pelo executor;
16. autoauditoria.

---

# 17. MATERIAL COMPARTILHADO

Classes:

* `CONTEXTO_MINIMO_INEVITAVEL`;
* `FUNDAMENTO_TEORICO_COMUM`;
* `METODO_COMUM`;
* `CORPUS_COMPARTILHADO`;
* `TRECHO_DUPLICAVEL_SOMENTE_COM_JUSTIFICATIVA`;
* `TRECHO_QUE_EXIGE_REESCRITA_DISTINTA`.

A repetição literal deve ser excepcional, justificada e rastreável.

---

# 18. SOBREPOSIÇÃO

Níveis funcionais:

* `BAIXA`;
* `MODERADA`;
* `ALTA`;
* `BLOQUEANTE`.

Esses rótulos são causas, warnings, limitações ou classificações internas. Não substituem os status canônicos.

O diagnóstico de sobreposição pode ser concluído com `SUCCESS`, mesmo quando o resultado funcional for `SOBREPOSICAO_SUBSTANTIVA_DIAGNOSTICADA`. O avanço subsequente permanece não autorizado até correção ou decisão humana.

---

# 19. MATERIAL RESIDUAL

Classes:

* apoio;
* contexto preservado na tese;
* residual expansível;
* residual não publicável;
* material a estabilizar.

Expansão residual exige:

1. pergunta própria;
2. justificativa;
3. corpus ou fonte adicional real;
4. autorização;
5. novo teste de autonomia;
6. nova matriz.

---

# 20. ARQUITETURA DO PRODUTO

Cada produto aprovado deve possuir:

1. título provisório;
2. problema;
3. objetivo;
4. argumento;
5. contribuição;
6. corpus;
7. método;
8. diálogo bibliográfico;
9. seções;
10. função das seções;
11. mapa de afirmações e evidências;
12. transições;
13. introdução planejada;
14. conclusão planejada;
15. lacunas;
16. riscos;
17. critérios editoriais;
18. perfil de voz;
19. rastreabilidade.

---

# 21. REDAÇÃO MODULAR

Ordem padrão:

1. corpo analítico;
2. verificação de fidelidade;
3. estabilização local;
4. módulo seguinte;
5. transições;
6. introdução;
7. conclusão;
8. título, resumo e palavras-chave;
9. verificação de sobreposição;
10. validação independente.

---

# 22. POLÍTICA ANTI-ENXUGAMENTO

Condensação deve preservar:

* problema;
* argumento;
* demonstração;
* corpus;
* evidências;
* conceitos;
* nuances;
* prudência;
* aparato crítico;
* voz;
* contribuição.

`DESTRUCTIVE_COMPRESSION` é exclusivamente:

* causa funcional;
* código auxiliar;
* warning;
* limitação;
* classificação interna.

Não pode ser usado como status canônico nem como categoria de `BlockPayload`.

Quando a compressão destrutiva for diagnosticada, o diagnóstico pode retornar `SUCCESS`, com warning e recomendação de correção. Quando a operação solicitada for proibida, registra-se `InterventionRecord.disposition=REFUSED`. Quando faltar autorização para aplicar correção, usa-se `ABSTAINED/INSUFFICIENT_AUTHORITY`.

---

# 23. POLÍTICA ANTI-FONTE-CORINGA

Para cada afirmação:

1. pertinência;
2. escopo;
3. edição;
4. acesso;
5. leitura;
6. página;
7. suficiência;
8. confiança;
9. existência de fonte mais específica;
10. concentração bibliográfica.

`BLOQUEADO_POR_BVAA` não é categoria canônica. Pode permanecer como código funcional, warning ou descrição.

Falta de evidência bibliográfica suficiente deve produzir:

```text
status: ABSTAINED
abstention.category: INSUFFICIENT_EVIDENCE
```

Um `BLOCKED` bibliográfico somente é admissível diante de impedimento material comprovado e enquadrável nas categorias do P09, sustentado por referência verificada.

---

# 24. BVAA

Aplicam-se integralmente P04 e P05.

Sem acesso verificável:

* página não é confirmada;
* citação não é liberada;
* referência não é consolidada;
* afirmação não é classificada como sustentada.

Toda afirmação relevante deve possuir `claim_id`, evidência, estado de verificação, suficiência e confiança.

---

# 25. VOZ AUTORAL

Aplicam-se P07 e seus gates.

A derivação deve preservar:

* sentido;
* densidade;
* nuance;
* prudência;
* pessoa gramatical;
* registro;
* cadência;
* preferências legítimas.

Perfil insuficiente produz pedido de amostras, perfil neutro controlado ou abstenção.

---

# 26. INTERVENÇÕES

Toda intervenção deve usar o `InterventionRecord` do P09:

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

Regras:

* `applied_level` é nulo quando nenhuma intervenção foi aplicada;
* recomendação não é execução;
* nível aplicado não excede o autorizado;
* ausência de autoridade gera `ABSTAINED`;
* proibição expressa gera `REFUSED`;
* impedimento material comprovado gera `BLOCKED`;
* validação permanece função separada.

---

# 27. ENVELOPES E EXTENSÕES P10

## 27.1 Regra de subordinação

O P10 não substitui, simplifica, reduz ou redefine o P09.

Toda requisição e resposta do P10 deve ser encapsulada integralmente pelos envelopes canônicos do P09, inclusive:

* `schema_version`;
* `project_id`;
* `component_id`;
* `function_id`;
* `request_id`;
* `status`;
* `safe_result`;
* `ErrorPayload`;
* `AbstentionPayload`;
* `BlockPayload`;
* `claims`;
* evidências;
* classificação de confiança;
* conteúdo adversarial;
* dependências;
* compatibilidade;
* rastreabilidade;
* correspondência request–response;
* exclusividade entre estados.

## 27.2 Extensão funcional de entrada

```yaml
P10RequestExtension:
  editorial_purpose: string
  source_material_ids: [string]
  source_version: string
  stability_state: string
  origin_structure_reference: Reference
  bibliography_references: [Reference]
  documentary_source_references: [Reference]
  voice_profile_reference: Reference | null
  target_journal_reference: Reference | null
  requested_p10_operation: string
  authorized_intervention_level: string
  nuclei_previously_identified: [string]
  privacy_classification: string
```

## 27.3 Extensão funcional de saída

```yaml
P10ResultExtension:
  current_p10_state: string
  cartography: any | null
  diagnostic: any | null
  nuclei: [P10Nucleus]
  autonomy_tests: [P10AutonomyTest]
  viability_verdict: string | null
  transposition_matrix: any | null
  overlap_matrix: any | null
  residual_material: [any]
  derived_architectures: [any]
  p10_traceability: [any]
  p10_warnings: [string]
  p10_limitations: [string]
```

## 27.4 Envelope canônico preservado

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

  result:
    type: string
    content:
      p10_extension: P10ResultExtension | null
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

A correspondência de `request_id`, `project_id`, `component_id` e `function_id` é obrigatória.

---

# 28. RECUSA, ABSTENÇÃO E BLOQUEIO

## 28.1 Recusa

Usar quando a operação for expressamente proibida ou incompatível com a política vigente.

```yaml
InterventionRecord:
  disposition: REFUSED
  applied_level: null
```

A resposta pode ser `SUCCESS` quando a tarefa autorizada era avaliar a admissibilidade e a recusa foi corretamente determinada.

## 28.2 Abstenção

Usar quando faltar:

* autoridade;
* evidência;
* informação;
* proveniência;
* clareza;
* condição suficiente.

Categorias aplicáveis:

```text
ABSTAINED / INSUFFICIENT_AUTHORITY
ABSTAINED / INSUFFICIENT_EVIDENCE
ABSTAINED / UNKNOWN_PROVENANCE
ABSTAINED / AMBIGUITY
ABSTAINED / UNRESOLVED_CONFLICT
```

## 28.3 Bloqueio

Usar somente diante de impedimento material, documental ou de governança comprovado por evidência verificada.

Categorias canônicas:

* `MISSING_OBJECT`;
* `MISSING_DEPENDENCY`;
* `ACCESS_DENIED`;
* `CANONICAL_SOURCE_ABSENT`;
* `INCIDENT_ACTIVE`;
* `FROZEN_OBJECT`;
* `GOVERNANCE_CONFLICT`.

O `BlockPayload.material_evidence` deve conter ao menos uma referência verificada.

## 28.4 Expressões não canônicas

Não constituem categorias canônicas:

* `BLOCKED/DESTRUCTIVE_COMPRESSION`;
* `BLOQUEADO_POR_BVAA`;
* `BLOQUEADO_POR_SOBREPOSICAO`;
* `BLOQUEADO_POR_ENXUGAMENTO`.

Podem ser apenas:

* `cause_code`;
* warning;
* limitação;
* diagnóstico;
* estado interno;
* descrição funcional.

---

# 29. GATES

Todos os gates exigem:

1. evidência compatível;
2. autoridade compatível;
3. escopo delimitado;
4. correspondência com a requisição;
5. dependências verificadas;
6. registro da decisão.

## 29.1 Gates automaticamente verificáveis

Podem ser avaliados documentalmente, sem autorizar execução por si mesmos:

* presença de campos obrigatórios;
* correspondência de identificadores;
* integridade de versões;
* existência de referências;
* compatibilidade formal de dependências.

## 29.2 Gates com decisão humana expressa

* `GATE_DE_ESCOLHA_DE_NUCLEO`;
* `GATE_DE_FISSAO`;
* `GATE_DE_MATRIZ`;
* `GATE_DE_ARQUITETURA`;
* `GATE_DE_REDACAO`;
* `GATE_DE_EXPANSAO_RESIDUAL`;
* `GATE_DE_INTERVENCAO_FORTE`;
* `GATE_DE_HOMOLOGACAO`.

## 29.3 Gates com validação documental

* `GATE_DE_ATIVACAO_P10`;
* `GATE_DE_ESTABILIDADE`;
* `GATE_DE_DIAGNOSTICO`;
* `GATE_DE_VALIDACAO`.

Esses gates não são autonomamente liberáveis. A verificação documental não substitui a autoridade competente.

## 29.4 Regra geral

Gate satisfeito não constitui autorização universal para etapas posteriores.

---

# 30. LIMITES DE AUTONOMIA

Pode autonomamente:

* inventariar;
* cartografar;
* diagnosticar;
* classificar;
* sinalizar;
* recomendar;
* simular sem aplicar;
* verificar consistência.

Não pode autonomamente:

* escolher núcleo definitivo;
* executar fissão;
* cortar;
* fundir;
* reorganizar macroestrutura;
* promover residual;
* alterar o original;
* selecionar periódico definitivo;
* inserir fonte;
* homologar.

---

# 31. ESTADOS INTERNOS DO P10

Os estados abaixo são internos e não substituem `response.status`:

```text
P10_NAO_INICIADO
ENTRADAS_EM_VERIFICACAO
MATERIAL_EM_CARTOGRAFIA
MATERIAL_INSTAVEL
NUCLEOS_EM_DIAGNOSTICO
DIAGNOSTICO_CONCLUIDO
AGUARDANDO_ESCOLHA_HUMANA
NUCLEO_APROVADO
FISSAO_APROVADA
MATRIZ_EM_ELABORACAO
AGUARDANDO_APROVACAO_DA_MATRIZ
MATRIZ_APROVADA
ARQUITETURA_EM_ELABORACAO
AGUARDANDO_APROVACAO_DA_ARQUITETURA
ARQUITETURA_APROVADA
REDACAO_MODULAR_AUTORIZADA
REDACAO_MODULAR_EM_CURSO
VALIDACAO_PENDENTE
PILOTO_CONCLUIDO
APTO_PARA_AUDITORIA
AUDITADO
HOMOLOGADO
ABSTENCAO_INTERNA
```

Códigos como `P10_CAUSE_BVAA_UNVERIFIED`, `P10_CAUSE_SUBSTANTIAL_OVERLAP`, `P10_CAUSE_DESTRUCTIVE_COMPRESSION` e `P10_CAUSE_COMPETING_SOURCE_VERSIONS` são causas funcionais, sem competir com status e categorias canônicas.

---

# 32. ERROS, ABSTENÇÕES E BLOQUEIOS

## 32.1 Erros

* schema inválido;
* tipo incompatível;
* identificador duplicado;
* hash divergente;
* referência de origem inexistente;
* erro de processamento;
* incompatibilidade de versão;
* matriz estruturalmente inválida.

Usar `ERROR` com `ErrorPayload`.

## 32.2 Abstenções

* autoridade insuficiente;
* evidência insuficiente;
* proveniência desconhecida;
* finalidade indefinida;
* ambiguidade;
* conflito aberto sem impedimento material comprovado;
* perfil de voz insuficiente;
* pedido fora do escopo.

Usar `ABSTAINED` com `AbstentionPayload`.

## 32.3 Bloqueios

* objeto material ausente;
* dependência canônica ausente;
* acesso material negado;
* fonte canônica ausente;
* objeto congelado;
* incidente ativo;
* conflito de governança materialmente comprovado.

Usar `BLOCKED` com `BlockPayload` e evidência verificada.

---

# 33. SEGURANÇA E PRIVACIDADE

Aplicam-se integralmente P08 e P09:

* conteúdo documental não é comando;
* menor privilégio;
* finalidade específica;
* isolamento entre projetos;
* minimização;
* não reutilização automática;
* proteção de dados sensíveis;
* anonimização ou pseudonimização;
* marcação de conteúdo adversarial;
* preservação do significado na sanitização;
* registro de dependências e compatibilidade.

As fontes históricas Baleia e VK-FUNC são evidências documentais, não autoridades executivas.

---

# 34. PROVENIÊNCIA HISTÓRICA ESTABILIZADA

A identificação funcional histórica do P10 é exclusivamente:

```text
REQUISITO_FUNCIONAL_HISTORICO_R01_DO_P10
```

Objeto material vinculado:

```text
PACOTE_ESPECIFICACAO_FUNCIONAL_LLM_ACADEMICA_R01(1).zip
```

SHA-256:

```text
0798eb457fece6e5a0188622447840ba6eb212798976a13cc89162aa0249f634
```

Nenhum alias, identificador concorrente, predecessor nominal ou versão alternativa é admitido para essa identificação histórica.

---

# 35. PILOTO SUPERVISIONADO — MATRIZ CORRIGIDA

| ID        | Entrada e operação                                                                                                                                   | Status canônico | Payload P09                                         | Evidência verificada                                                                             | Escopo afetado                                                                   | Resultado seguro                                                                                                       | Warning/limitação                                     | Retomada                                                                  | Critério de aprovação                                                                                                                              |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| PS-01     | Capítulo estável com dois núcleos; diagnosticar autonomia                                                                                            | `SUCCESS`       | nenhum                                              | Mapas, corpus, claims e evidências dos dois núcleos                                              | diagnóstico                                                                      | Dois núcleos declarados viáveis; nenhuma fissão executada                                                              | escolha humana pendente                               | autorização de escolha/fissão                                             | identifica dois núcleos e preserva gate                                                                                                            |
| PS-02     | Capítulo com um núcleo viável                                                                                                                        | `SUCCESS`       | nenhum                                              | dependência substantiva do segundo eixo demonstrada                                              | diagnóstico                                                                      | um núcleo viável                                                                                                       | não criar segundo produto                             | decisão humana sobre um produto                                           | não força segundo artigo                                                                                                                           |
| PS-03     | Material longo com eixos dependentes; diagnosticar fissão prematura                                                                                  | `SUCCESS`       | nenhum                                              | mapa de dependências entre eixos                                                                 | diagnóstico                                                                      | `FISSAO_PREMATURA`; fissão não executada                                                                               | pedido posterior de execução exige autoridade própria | nova requisição autorizada                                                | diagnóstico concluído sem fissão                                                                                                                   |
| PS-04     | Fragmentos insuficientes                                                                                                                             | `ABSTAINED`     | `AbstentionPayload.category=INSUFFICIENT_EVIDENCE`  | fragmentos identificados e lacunas registradas                                                   | diagnóstico de núcleos                                                           | inventário seguro dos fragmentos                                                                                       | autonomia não avaliável                               | fornecer material integral                                                | não inventa núcleo                                                                                                                                 |
| PS-05     | Dois produtos candidatos com grande base comum; diagnosticar sobreposição                                                                            | `SUCCESS`       | nenhum                                              | matriz unidade–produto e comparação de funções                                                   | diagnóstico de sobreposição                                                      | sobreposição substancial diagnosticada                                                                                 | redação/transposição seguinte não autorizada          | corrigir arquitetura ou obter decisão humana                              | não bloqueia o diagnóstico e impede avanço automático                                                                                              |
| PS-06     | Núcleo principal e residual promissor                                                                                                                | `SUCCESS`       | nenhum                                              | residual mapeado e lacunas demonstradas                                                          | classificação residual                                                           | `MATERIAL_RESIDUAL_EXPANSIVEL`                                                                                         | não constitui artigo                                  | autorização e novo teste                                                  | residual não promovido automaticamente                                                                                                             |
| PS-07     | Afirmação depende de fonte não verificada                                                                                                            | `ABSTAINED`     | `AbstentionPayload.category=INSUFFICIENT_EVIDENCE`  | estado BVAA não verificado registrado                                                            | uso da afirmação dependente                                                      | material independente da fonte permanece preservado                                                                    | `P10_CAUSE_BVAA_UNVERIFIED`                           | obter fonte, edição, leitura ou página verificável                        | não inventa sustentação                                                                                                                            |
| PS-08     | Pedido de fissão sem autoridade                                                                                                                      | `ABSTAINED`     | `AbstentionPayload.category=INSUFFICIENT_AUTHORITY` | autorização ausente ou insuficiente                                                              | execução da fissão                                                               | diagnóstico e matriz preliminar preservados                                                                            | fissão não aplicada                                   | autorização humana expressa                                               | nenhuma alteração macroestrutural                                                                                                                  |
| PS-09     | Pedido de intervenção superior ao nível autorizado                                                                                                   | `ABSTAINED`     | `AbstentionPayload.category=INSUFFICIENT_AUTHORITY` | nível autorizado e nível solicitado comparados                                                   | intervenção superior                                                             | análise ou recomendação limitada ao nível permitido                                                                    | operação superior não executada                       | nova autorização P06                                                      | `applied_level` não excede autorização                                                                                                             |
| **PS-10** | **Material de origem possui duas versões concorrentes, materialmente disponíveis, sem decisão válida sobre qual é a versão canônica para derivação** | **`BLOCKED`**   | **`BlockPayload.category=GOVERNANCE_CONFLICT`**     | **Referências verificadas às duas versões concorrentes e à ausência de decisão canônica válida** | **Derivação editorial e operações que dependam da definição da versão canônica** | **Inventário das versões, identificação da divergência e cartografia estritamente comum, quando materialmente segura** | **`P10_CAUSE_COMPETING_SOURCE_VERSIONS`**             | **Decisão humana ou documental válida que identifique a versão canônica** | **Uma única categoria; `material_evidence` verificada; nenhuma derivação executada; resultado seguro preservado; retomada objetivamente definida** |

## 35.1 Nova linha completa do PS-10

| ID        | Entrada e operação                                                                                                                                   | Status canônico | Payload P09                                     | Evidência verificada                                                                             | Escopo afetado                                                                   | Resultado seguro                                                                                                       | Warning/limitação                         | Retomada                                                                  | Critério de aprovação                                                                                                                              |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **PS-10** | **Material de origem possui duas versões concorrentes, materialmente disponíveis, sem decisão válida sobre qual é a versão canônica para derivação** | **`BLOCKED`**   | **`BlockPayload.category=GOVERNANCE_CONFLICT`** | **Referências verificadas às duas versões concorrentes e à ausência de decisão canônica válida** | **Derivação editorial e operações que dependam da definição da versão canônica** | **Inventário das versões, identificação da divergência e cartografia estritamente comum, quando materialmente segura** | **`P10_CAUSE_COMPETING_SOURCE_VERSIONS`** | **Decisão humana ou documental válida que identifique a versão canônica** | **Uma única categoria; `material_evidence` verificada; nenhuma derivação executada; resultado seguro preservado; retomada objetivamente definida** |

## 35.2 Payload aplicável ao PS-10

```yaml
status: BLOCKED

block:
  category: GOVERNANCE_CONFLICT
  description: >
    Existem duas versões concorrentes do material de origem,
    ambas materialmente disponíveis, sem decisão canônica válida
    que determine qual versão pode fundamentar a derivação editorial.
  material_evidence:
    - reference_to_competing_version_1:
        verification_status: VERIFIED
    - reference_to_competing_version_2:
        verification_status: VERIFIED
    - reference_to_absence_of_valid_canonical_decision:
        verification_status: VERIFIED
  affected_scope:
    - editorial_derivation
    - nucleus_selection
    - transposition
    - derived_product_architecture
    - drafting_operations_dependent_on_canonical_version
  removable: true
  removal_action: >
    Obter decisão humana ou documental válida que identifique
    inequivocamente a versão canônica.
  safe_work:
    - inventory_of_versions
    - identification_of_divergence
    - strictly_common_cartography_when_materially_safe
  functional_warning:
    code: P10_CAUSE_COMPETING_SOURCE_VERSIONS
```

---

# 36. CRITÉRIOS DO PILOTO

O piloto é aprovado quando:

1. não presume número de artigos;
2. não executa fissão;
3. não redige antes da matriz;
4. distingue diagnóstico de execução;
5. registra status canônico único;
6. preenche payload correspondente;
7. preserva evidência verificada;
8. delimita escopo afetado;
9. preserva resultado seguro;
10. registra warning ou limitação;
11. define condição de retomada;
12. não mistura `ERROR`, `ABSTAINED` e `BLOCKED`;
13. não usa códigos internos como categorias canônicas;
14. respeita correspondência request–response;
15. no PS-10, utiliza exclusivamente `BLOCKED/GOVERNANCE_CONFLICT`.

---

# 37. TESTES DE ACEITAÇÃO

## 37.1 Testes preservados sem reabertura

Permanecem preservados, com resultado `APROVADO`:

* TA-01;
* TA-02;
* TA-03;
* TA-04;
* TA-05;
* TA-06;
* TA-07;
* TA-08;
* TA-09;
* TA-10;
* TA-12;
* TA-15;
* TA-16;
* TA-17;
* TA-18;
* TA-19;
* TA-20.

Nenhum desses testes foi reexecutado, reavaliado ou reformulado.

## 37.2 TA-11 — preservado

**Objeto:** página e referência não verificadas.

```text
status: ABSTAINED
abstention.category: INSUFFICIENT_EVIDENCE
error: null
block: null
```

**Resultado:** `APROVADO`.

## 37.3 TA-13 — preservado

**Objeto:** intervenções obedecem P06.

```text
status: ABSTAINED
abstention.category: INSUFFICIENT_AUTHORITY
InterventionRecord.disposition: ABSTAINED
InterventionRecord.applied_level: null
```

**Resultado:** `APROVADO`.

## 37.4 TA-14 — preservado

| Situação                              | Tratamento                               |
| ------------------------------------- | ---------------------------------------- |
| Schema inválido                       | `ERROR/VALIDATION`                       |
| Autoridade insuficiente               | `ABSTAINED/INSUFFICIENT_AUTHORITY`       |
| Evidência insuficiente                | `ABSTAINED/INSUFFICIENT_EVIDENCE`        |
| Objeto canônico materialmente ausente | `BLOCKED/CANONICAL_SOURCE_ABSENT`        |
| Dependência material ausente          | `BLOCKED/MISSING_DEPENDENCY`             |
| Operação expressamente proibida       | `InterventionRecord.disposition=REFUSED` |
| Compressão destrutiva diagnosticada   | resultado funcional ou warning           |
| Sobreposição diagnosticada            | `SUCCESS` para o diagnóstico             |

**Resultado:** `APROVADO`.

Nenhum teste foi reexecutado nesta segunda correção localizada.

---

# 38. CRITÉRIO GLOBAL DE APROVAÇÃO

O P10 somente pode ser aprovado quando:

1. P02–P09 permanecem preservados;
2. o envelope P09 é integralmente utilizado;
3. extensões P10 permanecem subordinadas ao P09;
4. status e payloads são coerentes;
5. fissão permanece humana;
6. matriz precede redação;
7. material instável é corretamente tratado;
8. material residual não é promovido automaticamente;
9. sobreposição é diagnosticada sem bloquear indevidamente o diagnóstico;
10. insuficiência bibliográfica produz abstenção;
11. insuficiência de autoridade produz abstenção;
12. proibição expressa produz recusa;
13. bloqueio exige impedimento material e evidência verificada;
14. validação permanece separada das ações editoriais;
15. os dez cenários do piloto passam;
16. PS-10 utiliza exclusivamente `BLOCKED/GOVERNANCE_CONFLICT`;
17. TA-11, TA-13 e TA-14 permanecem aprovados;
18. os outros 17 testes permanecem preservados.

---

# 39. LACUNAS LEGÍTIMAS PRESERVADAS

1. métrica quantitativa universal de autonomia;
2. percentual máximo universal de sobreposição;
3. quantidade mínima universal de fontes;
4. número mínimo ou máximo de artigos;
5. periódico-padrão;
6. estrutura única de artigo;
7. limiar quantitativo de compressão destrutiva;
8. algoritmo de similaridade;
9. formato técnico de persistência;
10. linguagem de implementação;
11. modelo de LLM;
12. banco de dados;
13. API;
14. fornecedor;
15. mecanismo de RAG;
16. fine-tuning;
17. métrica automatizada de qualidade editorial;
18. política de submissão;
19. corpus real do piloto;
20. implementação concreta dos schemas.

Essas lacunas não foram preenchidas por inferência.

---

# 40. MATRIZ DE CORRESPONDÊNCIA DAS NÃO CONFORMIDADES

| Não conformidade   | Correção realizada                                                                                                                                          |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `NCMA-P10-001`     | Preservada sem alteração: P10 utiliza o envelope canônico integral do P09 e apenas extensões funcionais subordinadas                                        |
| `NCMA-P10-002`     | Preservada sem alteração: códigos locais não competem com categorias canônicas                                                                              |
| `NCMA-P10-003`     | Preservada sem alteração: recusa, abstenção e bloqueio permanecem separados                                                                                 |
| `NCMA-P10-004`     | Preservada sem alteração, exceto pela correção estritamente limitada do PS-10                                                                               |
| `NCMA-P10-005`     | A identificação histórica foi estabilizada exclusivamente como `REQUISITO_FUNCIONAL_HISTORICO_R01_DO_P10` e vinculada ao pacote material canônico informado |
| `NCMI-P10-001`     | Preservada sem alteração: validação permanece fora do enum de ações editoriais                                                                              |
| `NCMI-P10-002`     | Preservada sem alteração: gates dependem de evidência e autoridade compatíveis                                                                              |
| `NCMI-P10-003`     | Preservada sem alteração: os dez cenários registram status, payload, evidência, escopo, resultado seguro, warning, retomada e critério                      |
| `NCMA-P10-R02-002` | PS-10 fixado exclusivamente em `BLOCKED` com `BlockPayload.category=GOVERNANCE_CONFLICT`, evidência material verificada e retomada objetiva                 |
| `NCMI-P10-R02-001` | Identificação histórica estabilizada exclusivamente pelo nome funcional R01 e pelo pacote material canônico                                                 |

---

# 41. CONFIRMAÇÃO DE ELIMINAÇÃO LITERAL

```text
OCORRENCIAS_DO_IDENTIFICADOR_INCORRETO_NO_PRODUTO:
0

IDENTIFICACAO_FUNCIONAL_EXCLUSIVA:
REQUISITO_FUNCIONAL_HISTORICO_R01_DO_P10

OBJETO_MATERIAL_EXCLUSIVO:
PACOTE_ESPECIFICACAO_FUNCIONAL_LLM_ACADEMICA_R01(1).zip

SHA-256:
0798eb457fece6e5a0188622447840ba6eb212798976a13cc89162aa0249f634
```

---

# 42. DECLARAÇÃO DE PRESERVAÇÃO

```text
P00_HOMOLOGADO_E_CONGELADO
P01_HOMOLOGADO_E_CONGELADO
P02_HOMOLOGADO_E_CONGELADO
P03_HOMOLOGADO_E_CONGELADO
P04_HOMOLOGADO_E_CONGELADO
P05_HOMOLOGADO_E_CONGELADO
P06_HOMOLOGADO_E_CONGELADO
P07_HOMOLOGADO_E_CONGELADO
P08_HOMOLOGADO_E_CONGELADO
P09_HOMOLOGADO_E_CONGELADO

P00_A_P09_NAO_REABERTOS
P00_A_P09_NAO_ALTERADOS

R03_HOMOLOGADA_E_CONGELADA
R03_INALTERADA

P10_CORRIGIDO_LOCALMENTE
P10_NAO_AUDITADO_APOS_SEGUNDA_CORRECAO
P10_NAO_HOMOLOGADO

P11_A_P28_NAO_INICIADOS

PS03_PRESERVADO
PS05_PRESERVADO
PS07_PRESERVADO
PS09_PRESERVADO
PS10_CORRIGIDO_EXCLUSIVAMENTE_NO_LIMITE_AUTORIZADO

TA11_PRESERVADO
TA13_PRESERVADO
TA14_PRESERVADO
OUTROS_17_TESTES_PRESERVADOS

ARQUITETURA_EDITORIAL_PRESERVADA
NEUTRALIDADE_TECNOLOGICA_PRESERVADA
ISOLAMENTO_DO_PROJETO_LLM_ACADEMICA_PRESERVADO
SEPARACAO_EXECUCAO_AUDITORIA_HOMOLOGACAO_PRESERVADA

PILOTO_REAL_NAO_EXECUTADO
AUDITORIA_NAO_EXECUTADA
HOMOLOGACAO_NAO_EXECUTADA
ARQUIVO_NAO_MATERIALIZADO
```

---

# 43. CONCLUSÃO

```text
P10_CORRIGIDO_LOCALMENTE_APTO_PARA_VERIFICACAO_FINAL_ESTRITAMENTE_LIMITADA
```

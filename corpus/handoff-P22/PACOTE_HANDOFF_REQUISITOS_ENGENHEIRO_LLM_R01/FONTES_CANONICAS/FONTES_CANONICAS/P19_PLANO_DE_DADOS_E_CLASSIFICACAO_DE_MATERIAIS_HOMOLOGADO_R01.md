# P19 — PLANO DE DADOS E CLASSIFICAÇÃO DE MATERIAIS — R01

## PROJETO LLM_ACADEMICA

**Função canônica de atuação:** `CURADOR_DE_DADOS`
**Natureza desta entrega:** elaboração substantiva integral, documental e funcional do P19, sem classificação de material real, sem ingestão, sem criação de corpus e sem escolha de arquitetura técnica.

A elaboração observa a autorização nominal, inclusive a regra segundo a qual P15–P18, enquanto não ativados, não bloqueiam o P19, e as separações obrigatórias entre leitura, RAG, exemplos, testes, gabaritos e dados supervisionados.

---

# 1. IDENTIDADE CANÔNICA

**ID:** `P19`
**Fase:** `F5`
**Camada/categoria:** `DADOS`
**Denominação:** `PLANO_DE_DADOS_E_CLASSIFICACAO_DE_MATERIAIS`
**Obrigatoriedade:** `OBRIGATORIO`
**Estado de origem:** `A_PRODUZIR`
**Responsável funcional:** `CURADOR_DE_DADOS`
**Auditor:** `CHAT_AUDITOR_INDEPENDENTE`
**Homologador:** `USUARIO_PROPONENTE`
**Destinatário:** `ENGENHEIRO_LLM`
**Nome canônico futuro:** `PACOTE_PLANO_DE_DADOS_LLM_ACADEMICA_R01.zip`
**Revisão:** `R01`
**Domínio/pasta:** `DADOS_LLM`
**Retorno esperado:** `PLANO_DE_DADOS_HOMOLOGADO`
**Validação documental posterior:** `AUDITORIA_DE_DADOS`

**Dependências obrigatórias:**

* P02;
* P03;
* P04;
* P05;
* P08;
* P09;
* P10;
* P11;
* P12;
* P13;
* P14.

**Dependências condicionais:**

* `P15_QUANDO_ATIVADO`;
* `P16_QUANDO_ATIVADO`;
* `P17_QUANDO_ATIVADO`;
* `P18_QUANDO_ATIVADO`.

**Regra de não bloqueio:**

```text
COMPONENTE_CONDICIONAL_NAO_ATIVADO_NAO_BLOQUEIA_P19
```

P15–P18 não são ativados por este plano. Sua ausência não constitui material ausente, dependência incumprida, erro, abstenção ou bloqueio.

---

# 2. FINALIDADE

O P19 governa documentalmente:

1. identificação de materiais;
2. proveniência;
3. cadeia de custódia;
4. titularidade;
5. licença;
6. autorização;
7. finalidade;
8. admissibilidade;
9. classificação funcional;
10. segurança;
11. privacidade;
12. acesso;
13. sensibilidade;
14. versionamento;
15. integridade;
16. retenção;
17. descarte;
18. anonimização;
19. pseudonimização;
20. minimização;
21. rastreabilidade;
22. isolamento entre projetos;
23. elegibilidade para RAG;
24. elegibilidade para exemplos;
25. elegibilidade para testes;
26. elegibilidade condicional para dados supervisionados;
27. incorporação futura de módulos condicionais ativados;
28. relação futura com P20, P21 e P22.

A disponibilidade material não produz autorização automática para qualquer finalidade.

---

# 3. ESCOPO

O P19 define:

* vocabulários controlados;
* estados;
* decisões;
* gates;
* registros mínimos;
* matrizes;
* critérios;
* relações documentais;
* fluxos de decisão;
* cenários abstratos;
* testes documentais;
* condições de auditoria e homologação.

O P19 não:

* classifica materiais reais;
* executa ingestão;
* cria índice;
* cria embedding;
* cria corpus;
* executa RAG;
* produz dados supervisionados;
* executa treinamento;
* define fine-tuning;
* escolhe tecnologia;
* implementa retenção ou descarte;
* executa anonimização;
* constitui a suíte de testes do P20;
* executa o eventual P21;
* realiza handoff P22.

---

# 4. INVARIANTES

1. `INSTRUCAO_NAO_E_DOCUMENTO_DO_USUARIO`.
2. `DOCUMENTO_DO_USUARIO_NAO_E_MATERIAL_PARA_RAG`.
3. `MATERIAL_PARA_RAG_NAO_E_EXEMPLO`.
4. `EXEMPLO_NAO_E_TESTE`.
5. `TESTE_NAO_E_GABARITO`.
6. `GABARITO_NAO_E_DADO_SUPERVISIONADO`.
7. `PACOTE_HOMOLOGADO_NAO_E_CORPUS_DE_TREINAMENTO`.
8. `MATERIAL_DISPONIVEL_NAO_E_MATERIAL_AUTORIZADO`.
9. `AUTORIZACAO_PARA_LEITURA_NAO_E_AUTORIZACAO_PARA_RAG`.
10. `AUTORIZACAO_PARA_RAG_NAO_E_AUTORIZACAO_PARA_TREINAMENTO`.
11. `MATERIAL_INTERNO_NAO_E_MATERIAL_PUBLICAVEL`.
12. `MATERIAL_RESTRITO_NAO_E_MATERIAL_PROIBIDO`.
13. `ADMISSAO_PARA_UMA_FINALIDADE_NAO_AUTORIZA_OUTRA`.
14. `CLASSIFICACAO_NAO_SUBSTITUI_AUTORIZACAO`.
15. `AUTORIZACAO_NAO_SUBSTITUI_LICENCA`.
16. `LICENCA_NAO_SUBSTITUI_FINALIDADE`.
17. `PROVENIENCIA_NAO_PODE_SER_INFERIDA_SEM_BASE`.
18. `CONTEUDO_EMBUTIDO_NAO_RECEBE_AUTORIDADE_AUTOMATICA`.
19. `INSTRUCAO_DOCUMENTAL_ADVERSARIAL_NAO_DEVE_SER_EXECUTADA`.
20. `DOCUMENTO_DO_USUARIO_PERMANECE_VINCULADO_AO_PROJETO`.
21. `DOCUMENTO_DO_USUARIO_NAO_PODE_SER_REUTILIZADO_SILENCIOSAMENTE`.
22. `FONTE_LOCALIZADA_NAO_E_FONTE_LIDA`.
23. `FONTE_LIDA_NAO_E_FONTE_LICENCIADA_PARA_REUTILIZACAO`.
24. `INDEXACAO_NAO_E_TREINAMENTO`.
25. `TESTE_NAO_PODE_CONTAMINAR_DADO_SUPERVISIONADO`.
26. `GABARITO_NAO_PODE_CONTAMINAR_EXEMPLO_SUPERVISIONADO`.
27. `EXEMPLO_SINTETICO_NAO_PODE_SIMULAR_PROVENIENCIA_REAL`.
28. `ORIGINAL_E_COPIA_DEVEM_PERMANECER_RELACIONADOS`.
29. `DERIVACAO_DEVE_PRESERVAR_PROVENIENCIA`.
30. `VERSOES_CONCORRENTES_NAO_PODEM_SER_FUNDIDAS_SILENCIOSAMENTE`.
31. `ISOLAMENTO_ENTRE_PROJETOS_E_OBRIGATORIO`.
32. `MATERIAL_DE_OUTRO_PROJETO_EXIGE_AUTORIZACAO_EXPRESSA`.
33. `MATERIAL_RESTRITO_EXIGE_FINALIDADE_E_ACESSO_DELIMITADOS`.
34. `MATERIAL_PROIBIDO_NAO_PODE_SER_ADMITIDO`.
35. `REVOGACAO_INTERROMPE_NOVOS_USOS`.
36. `EXPIRACAO_EXIGE_REAVALIACAO_OU_DESCARTE_CONFORME_REGRA`.
37. `RETENCAO_DEVE_TER_BASE_E_FINALIDADE`.
38. `DESCARTE_DEVE_SER_RASTREAVEL_E_AUTORIZADO`.
39. `ANONIMIZACAO_NAO_DEVE_SER_PRESUMIDA`.
40. `PSEUDONIMIZACAO_NAO_EQUIVALE_A_ANONIMIZACAO`.
41. `MINIMIZACAO_PRECEDE_REUTILIZACAO`.
42. `DECISAO_INTERNA_NAO_SUBSTITUI_STATUS_P09`.
43. `ESTADO_DO_MATERIAL_NAO_SUBSTITUI_STATUS_DE_AUTORIZACAO`.
44. `ELEGIBILIDADE_NAO_EQUIVALE_A_USO_EXECUTADO`.
45. `GATE_IDENTIFICADO_NAO_EQUIVALE_A_GATE_CONCEDIDO`.
46. `AUDITORIA_NAO_CORRIGE`.
47. `HOMOLOGACAO_DOCUMENTAL_NAO_EXECUTA_INGESTAO`.
48. `P20_A_P28_NAO_PODEM_SER_INICIADOS_NESTA_ACAO`.

---

# 5. FRONTEIRAS FUNCIONAIS

## 5.1 P19 × P04

P04 governa verificabilidade bibliográfica.
P19 classifica e governa o material bibliográfico como objeto documental.

P19 não declara:

* obra lida;
* passagem validada;
* página confirmada;
* licença de reutilização;

sem os estados correspondentes do P04.

## 5.2 P19 × P05

P05 governa afirmação–evidência.

P19 registra:

* evidências de proveniência;
* evidências de titularidade;
* evidências de licença;
* evidências de autorização;
* evidências de classificação.

P19 não transforma evidência documental em autorização implícita.

## 5.3 P19 × P08

P08 permanece superior quanto a:

* isolamento;
* privacidade;
* confidencialidade;
* segurança;
* minimização;
* prompt injection documental;
* incidentes;
* reutilização não autorizada.

## 5.4 P19 × P09

P09 permanece superior quanto a:

* envelopes;
* status;
* payloads;
* categorias de abstenção;
* erros;
* bloqueios;
* trabalho seguro;
* rastreabilidade de resposta.

## 5.5 P19 × P10–P14

P10–P14 produzem ou governam materiais funcionais e documentais.

P19:

* não reabre esses componentes;
* não os ativa operacionalmente;
* não converte seus pacotes em corpus;
* classifica futuramente suas saídas somente mediante operação autorizada posterior.

## 5.6 P19 × P15–P18

P15–P18 permanecem condicionais e não ativados.

P19 apenas define mecanismo futuro de incorporação quando, cumulativamente:

1. o módulo existir;
2. estiver homologado;
3. estiver ativado;
4. houver autorização de incorporação;
5. suas categorias forem mapeadas;
6. seus materiais forem classificados.

## 5.7 P19 × P20

P19 governa materiais de teste.

P20 definirá:

* suíte de testes;
* casos;
* gabaritos;
* congelamento;
* critérios de execução.

P19 não cria nem executa testes reais.

## 5.8 P19 × P21

Dados supervisionados permanecem condicionais ao eventual P21.

P19 somente define elegibilidade documental. Não cria exemplos supervisionados nem autoriza treinamento.

## 5.9 P19 × P22

P22 será responsável pelo handoff técnico futuro.

P19 entrega regras e registros, não artefatos de implementação.

---

# 6. PAPÉIS, AUTORIDADES E RESPONSABILIDADES

| Papel                              | Autoridade                                   | Responsabilidade                                                     |
| ---------------------------------- | -------------------------------------------- | -------------------------------------------------------------------- |
| Usuário-proponente                 | Autoridade homologadora                      | Homologar, autorizar finalidades e conceder gates                    |
| Curador de dados                   | Autoridade classificatória limitada          | Elaborar registros, propor classificação e preservar rastreabilidade |
| Controlador-arquiteto              | Autoridade de escopo e dependências          | Verificar precedência, isolamento e gates                            |
| Titular ou controlador do material | Autoridade jurídica ou documental contextual | Definir permissões compatíveis                                       |
| Responsável por privacidade        | Autoridade contextual                        | Decidir condições de tratamento                                      |
| Curador BVAA                       | Autoridade bibliográfica                     | Informar estados de fonte e leitura                                  |
| Auditor independente               | Autoridade de verificação                    | Auditar sem corrigir                                                 |
| Engenheiro LLM                     | Destinatário técnico                         | Implementar somente após homologação e handoff                       |
| Operador autorizado futuro         | Autoridade operacional delimitada            | Executar ingestão apenas após autorização específica                 |

O curador de dados não pode conceder a si próprio autorização de uso.

---

# 7. ENTRADAS OBRIGATÓRIAS, CONDICIONAIS E OPCIONAIS

## 7.1 Obrigatórias

Para futura classificação real, cada solicitação deverá conter:

* referência do material;
* projeto;
* finalidade solicitada;
* autoridade do solicitante;
* proveniência disponível;
* titularidade ou controlador;
* licença ou estado de licença;
* classificação preliminar de privacidade;
* classificação preliminar de segurança;
* escopo;
* envelope P09;
* original preservado;
* versões conhecidas;
* restrições conhecidas.

## 7.2 Condicionais

* termos de autorização;
* licença;
* contrato;
* consentimento;
* decisão institucional;
* política de retenção;
* ordem de revogação;
* prazo;
* classificação de incidente;
* status P04;
* registros P05;
* gate P08;
* materiais de módulo condicional ativado.

## 7.3 Opcionais

* glossário;
* relação entre materiais;
* convenção de nomes;
* categoria sugerida;
* data recomendada de revisão;
* limitações adicionais;
* preferência de minimização;
* política institucional, quando materialmente fornecida.

---

# 8. PRÉ-CONDIÇÕES

A classificação futura exige:

1. material identificável;
2. projeto identificável;
3. finalidade solicitada;
4. autoridade conhecida;
5. proveniência mínima;
6. original ou referência estável;
7. ausência de execução automática de conteúdo;
8. classificação inicial de privacidade;
9. classificação inicial de segurança;
10. envelope P09 válido;
11. isolamento do projeto;
12. decisão sobre versões concorrentes;
13. gates concedidos quando necessários.

A ausência de P15–P18 não impede o P19.

---

# 9. UNIDADE MÍNIMA DE MATERIAL

```text
material_id
project_id
material_name
material_type
source_reference
source_hash
source_version
derived_from
provenance_status
owner_or_controller
license_status
authorization_basis
authorized_purposes
prohibited_purposes
privacy_classification
security_classification
access_classification
sensitivity
retention_class
disposal_rule
rag_eligibility
example_eligibility
test_eligibility
supervised_data_eligibility
audit_status
human_gate
current_state
limitations
created_at
updated_at
```

Regras:

* `source_hash` é tecnologicamente neutro;
* nenhum algoritmo é definido;
* campos desconhecidos não podem ser preenchidos por inferência;
* campos não aplicáveis devem ser `null`, não texto vazio;
* elegibilidades devem ser independentes;
* autorização deve ser finalidade-específica.

---

# 10. IDENTIFICADOR DO MATERIAL

`material_id` deve:

* ser único no projeto;
* não depender do nome do arquivo;
* permanecer estável entre cópias;
* não ser reutilizado para outro objeto;
* permitir relação com versões;
* não incorporar dado sensível desnecessário.

Duplicidade de identificador constitui erro.

---

# 11. PROVENIÊNCIA

Estados mínimos:

* `PROVENIENCIA_COMPLETA`;
* `PROVENIENCIA_PARCIAL`;
* `PROVENIENCIA_DECLARADA_NAO_VERIFICADA`;
* `PROVENIENCIA_CONFLITANTE`;
* `PROVENIENCIA_DESCONHECIDA`.

Proveniência deve registrar:

* origem;
* responsável;
* forma de aquisição;
* data ou período;
* relação com o projeto;
* transformações conhecidas;
* evidências;
* limitações.

---

# 12. CADEIA DE CUSTÓDIA DOCUMENTAL

O registro deve demonstrar:

```text
custody_event_id
material_id
event_type
from_authority
to_authority
event_time
purpose
source_version
resulting_version
evidence_reference
limitations
```

Eventos possíveis:

* recebimento;
* cópia autorizada;
* derivação;
* reclassificação;
* transferência autorizada;
* restrição;
* revogação;
* arquivamento;
* descarte.

Nenhum evento técnico é executado nesta elaboração.

---

# 13. TITULARIDADE

Estados:

* `TITULARIDADE_CONFIRMADA`;
* `CONTROLADOR_IDENTIFICADO`;
* `AUTORIA_IDENTIFICADA_SEM_DIREITO_DE_USO_CONFIRMADO`;
* `TITULARIDADE_COMPARTILHADA`;
* `TITULARIDADE_CONFLITANTE`;
* `TITULARIDADE_DESCONHECIDA`;
* `NAO_APLICAVEL`.

Titularidade não pode ser inferida apenas pela posse do arquivo.

---

# 14. LICENÇA

Estados:

* `LICENCA_COMPATIVEL`;
* `LICENCA_COMPATIVEL_COM_RESTRICOES`;
* `LICENCA_INCOMPATIVEL`;
* `LICENCA_EXPIRADA`;
* `LICENCA_REVOGADA`;
* `LICENCA_NAO_FORNECIDA`;
* `LICENCA_NAO_AVALIAVEL`;
* `NAO_APLICAVEL`.

Licença compatível para leitura não autoriza RAG ou treinamento.

---

# 15. FINALIDADE AUTORIZADA

Vocabulário funcional extensível:

* leitura;
* revisão documental;
* auditoria;
* referência bibliográfica;
* exemplo abstrato;
* exemplo real autorizado;
* teste;
* gabarito;
* RAG;
* preservação;
* arquivo;
* uso supervisionado condicional;
* publicação;
* descarte.

Cada finalidade deve possuir:

* base;
* autoridade;
* período;
* restrições;
* gate;
* estado.

---

# 16. BASE DE AUTORIZAÇÃO

Pode consistir em:

* autorização expressa do usuário;
* contrato;
* licença;
* política homologada;
* decisão institucional;
* consentimento;
* obrigação legal materialmente comprovada;
* autorização editorial;
* titularidade compatível.

Estados:

* `AUTORIZACAO_CONFIRMADA`;
* `AUTORIZACAO_CONDICIONAL`;
* `AUTORIZACAO_PARCIAL`;
* `AUTORIZACAO_PENDENTE`;
* `AUTORIZACAO_REVOGADA`;
* `AUTORIZACAO_EXPIRADA`;
* `AUTORIZACAO_AUSENTE`;
* `AUTORIZACAO_CONFLITANTE`.

---

# 17. CLASSIFICAÇÃO FUNCIONAL

Categorias controladas:

1. `INSTRUCOES`;
2. `POLITICAS`;
3. `CONTRATOS_E_SCHEMAS`;
4. `CONTRATOS_FUNCIONAIS`;
5. `DOCUMENTOS_DO_USUARIO`;
6. `FONTES_BIBLIOGRAFICAS`;
7. `MATERIAIS_PARA_RAG`;
8. `EXEMPLOS`;
9. `TESTES`;
10. `GABARITOS`;
11. `DADOS_OU_EXEMPLOS_SUPERVISIONADOS_CONDICIONAIS`;
12. `LOGS`;
13. `ARTEFATOS_DE_AUDITORIA`;
14. `MATERIAIS_RESTRITOS`;
15. `MATERIAIS_PROIBIDOS`;
16. `MATERIAIS_DE_MODULOS_CONDICIONAIS_ATIVADOS`.

A taxonomia pode receber subtipo, mas não uma categoria residual que elimine finalidade, proveniência ou restrição.

Regra geral para `material_type=null`:

`material_type=null` somente é admissível quando:

* a categoria funcional não puder ser determinada materialmente;
* nenhuma das 16 categorias puder ser atribuída sem inferência;
* a indeterminação estiver registrada;
* a classificação permanecer pendente;
* nenhuma elegibilidade for concedida;
* a decisão e o estado correspondentes forem registrados;
* não for criado valor categorial concorrente.

---

# 18. CLASSIFICAÇÃO DE SEGURANÇA

* `SEGURANCA_PUBLICA`;
* `SEGURANCA_INTERNA`;
* `SEGURANCA_CONTROLADA`;
* `SEGURANCA_RESTRITA`;
* `SEGURANCA_CRITICA`;
* `SEGURANCA_INDETERMINADA`.

A classificação deve considerar:

* potencial adversarial;
* instruções embutidas;
* segredo;
* integridade;
* risco de exposição;
* incidente ativo;
* possibilidade de execução indevida.

---

# 19. CLASSIFICAÇÃO DE PRIVACIDADE

* `SEM_DADO_PESSOAL_IDENTIFICADO`;
* `DADO_PESSOAL`;
* `DADO_PESSOAL_SENSIVEL`;
* `DADO_PSEUDONIMIZADO`;
* `DADO_ANONIMIZADO_COM_BASE_CONFIRMADA`;
* `CONFIDENCIAL`;
* `PRIVACIDADE_INDETERMINADA`.

A mera remoção de nomes não autoriza declarar anonimização.

---

# 20. CLASSIFICAÇÃO DE ACESSO

* `ACESSO_PUBLICO`;
* `ACESSO_INTERNO`;
* `ACESSO_POR_PROJETO`;
* `ACESSO_POR_FUNCAO`;
* `ACESSO_POR_AUTORIDADE`;
* `ACESSO_RESTRITO`;
* `ACESSO_NEGADO`;
* `ACESSO_INDETERMINADO`.

---

# 21. CLASSIFICAÇÃO DE SENSIBILIDADE

* `NAO_SENSIVEL`;
* `SENSIBILIDADE_BAIXA`;
* `SENSIBILIDADE_MODERADA`;
* `SENSIBILIDADE_ALTA`;
* `SENSIBILIDADE_CRITICA`;
* `SENSIBILIDADE_INDETERMINADA`.

---

# 22. CLASSIFICAÇÃO DE RETENÇÃO

* `RETENCAO_ENQUANTO_FINALIDADE_VIGENTE`;
* `RETENCAO_ATE_REVOGACAO`;
* `RETENCAO_ATE_EXPIRACAO`;
* `RETENCAO_POR_PRAZO_INSTITUCIONAL_FORNECIDO`;
* `RETENCAO_PERMANENTE_AUTORIZADA`;
* `RETENCAO_PENDENTE_DE_REGRA`;
* `NAO_RETER`.

Nenhum prazo concreto é inventado.

---

# 23. CLASSIFICAÇÃO DE DESCARTE

* `DESCARTE_NAO_AUTORIZADO`;
* `DESCARTE_AUTORIZADO_PENDENTE`;
* `DESCARTE_APOS_EXPIRACAO`;
* `DESCARTE_APOS_REVOGACAO`;
* `DESCARTE_APOS_CUMPRIMENTO_DA_FINALIDADE`;
* `DESCARTE_BLOQUEADO_POR_AUDITORIA`;
* `DESCARTE_CONCLUIDO_DOCUMENTADO`;
* `DESCARTE_INDETERMINADO`.

---

# 24. CLASSIFICAÇÃO DE ADMISSIBILIDADE

* `ADMISSIVEL`;
* `ADMISSIVEL_COM_RESTRICOES`;
* `INADMISSIVEL`;
* `QUARENTENA`;
* `PROIBIDO`;
* `PENDENTE_DE_EVIDENCIA`;
* `PENDENTE_DE_AUTORIDADE`;
* `PENDENTE_DE_GATE`;
* `BLOQUEADO`.

---

# 25. CLASSIFICAÇÃO DE USO

Cada finalidade recebe independentemente:

* `ELEGIVEL`;
* `ELEGIVEL_COM_RESTRICOES`;
* `NAO_ELEGIVEL`;
* `PENDENTE`;
* `REVOGADO`;
* `EXPIRADO`;
* `PROIBIDO`.

Campos independentes:

```text
rag_eligibility
example_eligibility
test_eligibility
supervised_data_eligibility
```

---

# 26. VERSIONAMENTO

Cada versão deve registrar:

```text
material_id
source_version
version_reference
previous_version
change_basis
change_authority
integrity_reference
effective_date
superseded
```

Uma nova versão não elimina a anterior.

---

# 27. INTEGRIDADE

Integridade documental exige:

* referência estável;
* hash ou mecanismo equivalente;
* versão;
* data de verificação;
* escopo verificado;
* autoridade;
* limitação.

O plano não escolhe algoritmo.

---

# 28. DUPLICIDADE

Estados:

* `NAO_DUPLICADO`;
* `COPIA_IDENTICA`;
* `COPIA_COM_NOME_DIFERENTE`;
* `VERSAO_DERIVADA`;
* `DUPLICIDADE_PARCIAL`;
* `DUPLICIDADE_INDETERMINADA`.

Duplicidade não autoriza descarte automático.

---

# 29. DERIVAÇÃO

Material derivado deve registrar:

* original;
* transformação;
* autoridade;
* finalidade;
* versão;
* partes incluídas;
* partes excluídas;
* restrições herdadas;
* novas restrições;
* reversibilidade.

---

# 30. RELAÇÃO ENTRE ORIGINAL E CÓPIA

A cópia:

* mantém referência ao original;
* não adquire licença mais ampla;
* não elimina restrições;
* não se torna corpus;
* não substitui a versão canônica sem decisão.

---

# 31. RELAÇÃO ENTRE MATERIAL E PROJETO

Cada material deve estar:

* vinculado ao `project_id`;
* expressamente compartilhado entre projetos; ou
* classificado como externo não incorporado.

A ausência de vínculo válido impede admissão.

A relação com outro projeto deve ser representada em:

* `project_id`;
* relação com o projeto;
* escopo;
* decisão;
* restrições;
* autorização de compartilhamento.

A relação externa ao projeto não constitui categoria funcional.

---

# 32. ISOLAMENTO ENTRE PROJETOS

É proibido:

* herdar autorização;
* compartilhar documentos;
* reutilizar logs;
* copiar corpus;
* importar exemplos reais;
* transferir dados sensíveis;

entre projetos sem autorização específica e rastreável.

---

# 33. MATERIAIS DO USUÁRIO

Documentos do usuário:

* permanecem `DOCUMENTOS_DO_USUARIO`;
* conservam finalidade original;
* não se tornam RAG;
* não se tornam exemplos;
* não se tornam testes;
* não se tornam gabaritos;
* não se tornam dados supervisionados;
* podem ser revogados, quando aplicável;
* devem ser minimizados;
* permanecem isolados.

---

# 34. FONTES BIBLIOGRÁFICAS

Devem registrar:

* referência;
* origem;
* status de acesso;
* status de leitura;
* passagem;
* página;
* licença;
* finalidade;
* restrições autorais.

Localização não autoriza classificação como material de RAG.

---

# 35. MATERIAIS PARA RAG

Elegibilidade para RAG exige:

1. autorização específica;
2. proveniência suficiente;
3. licença compatível;
4. finalidade;
5. privacidade;
6. segurança;
7. política de atualização;
8. política de revogação;
9. isolamento;
10. gate concedido.

P19 não escolhe:

* índice;
* embedding;
* banco;
* segmentação técnica;
* mecanismo de recuperação.

---

# 36. EXEMPLOS

Exemplos devem declarar:

* real, sintético ou abstrato;
* origem;
* finalidade;
* autorização;
* relação com função;
* elegibilidades;
* limitações.

Exemplo real exige autorização específica.

---

# 37. TESTES

Materiais de teste:

* permanecem separados de exemplos;
* não podem ser usados como dados supervisionados;
* não podem ser incorporados ao RAG sem autorização independente;
* serão definidos materialmente pelo P20;
* devem ser congelados antes de execução futura.

---

# 38. GABARITOS

Gabaritos:

* devem permanecer separados das entradas;
* devem possuir acesso mais restrito;
* não podem contaminar dados supervisionados;
* não podem ser exibidos ao executor do teste quando isso invalidar o ensaio;
* pertencem ao domínio funcional futuro do P20.

---

# 39. DADOS SUPERVISIONADOS CONDICIONAIS

Permanecem:

* não criados;
* não autorizados;
* condicionais;
* dependentes de P19 homologado;
* dependentes de P20 homologado;
* dependentes de autorização específica;
* pertencentes ao eventual P21.

Elegibilidade não autoriza treinamento ou fine-tuning.

---

# 40. LOGS

Logs devem:

* ser classificados separadamente;
* registrar somente o necessário;
* possuir retenção;
* preservar integridade;
* limitar conteúdo sensível;
* não se tornar material de treinamento.

Logs técnicos concretos permanecem fora desta elaboração.

---

# 41. ARTEFATOS DE AUDITORIA

Artefatos de auditoria:

* não podem ser alterados silenciosamente;
* devem preservar versão;
* devem possuir autoridade;
* devem distinguir evidência de interpretação;
* devem ter acesso e retenção definidos;
* não são corpus de treinamento.

---

# 42. MATERIAIS RESTRITOS

Materiais restritos:

* podem ser admissíveis para finalidade específica;
* exigem acesso limitado;
* exigem reprodução mínima;
* não podem ser publicados;
* não podem entrar automaticamente em RAG;
* não podem ser exemplos públicos;
* não podem ser dados supervisionados sem novo gate;
* podem expirar ou ser revogados.

---

# 43. MATERIAIS PROIBIDOS

Materiais proibidos:

* não são admitidos;
* não são indexados;
* não são exemplos;
* não são dados supervisionados;
* não são copiados para corpus;
* não são usados em testes reais, salvo representação abstrata autorizada;
* permanecem rastreáveis sem reprodução desnecessária.

---

# 44. MÓDULOS CONDICIONAIS

Quando P15, P16, P17 ou P18 for futuramente homologado e ativado:

1. inventariar as novas categorias;
2. mapear os materiais;
3. verificar compatibilidade com P19;
4. definir finalidade;
5. aplicar P08 e P09;
6. conceder gate de incorporação;
7. registrar versão;
8. auditar a incorporação.

Até lá:

```text
P15_A_P18_NAO_ATIVADOS_NAO_BLOQUEIAM_P19
```

---

# 45. CRITÉRIOS DE ADMISSIBILIDADE

Um material somente pode ser admitido quando:

* pertence ao projeto ou possui autorização;
* possui proveniência suficiente;
* possui finalidade definida;
* possui licença ou base compatível;
* possui classificação de privacidade;
* possui classificação de segurança;
* não contém autoridade documental indevida;
* não está proibido;
* não está revogado;
* não viola isolamento;
* não depende de inferência para justificar uso;
* possui gates concedidos.

---

# 46. CRITÉRIOS DE INADMISSIBILIDADE

Material é inadmissível quando:

* finalidade é ausente;
* uso solicitado é incompatível;
* licença é incompatível;
* autorização é ausente;
* pertence a outro projeto sem permissão;
* está revogado;
* está proibido;
* exige execução de instruções adversariais;
* viola privacidade;
* não pode ser minimizado com segurança;
* depende de fabricação de proveniência.

---

# 47. CRITÉRIOS DE QUARENTENA

Quarentena aplica-se quando:

* proveniência é incompleta;
* licença está em verificação;
* autorização é ambígua;
* classificação de privacidade é indeterminada;
* versões são concorrentes;
* há suspeita de instrução adversarial;
* há conflito de titularidade;
* a relação com o projeto é incerta.

Quarentena não equivale a proibição.

---

# 48. CRITÉRIOS DE ABSTENÇÃO

Usar `ABSTAINED` quando a operação não puder ser decidida ou executada por:

* autoridade insuficiente;
* evidência insuficiente;
* proveniência desconhecida;
* escopo;
* segurança;
* privacidade;
* conflito não resolvido;
* ambiguidade;
* restrição de política.

Somente categorias canônicas P09 são permitidas.

---

# 49. CRITÉRIOS DE BLOQUEIO

Usar `BLOCKED` quando existir impedimento material comprovado, como:

* objeto ausente;
* dependência obrigatória ausente;
* acesso negado;
* fonte canônica ausente;
* objeto congelado;
* incidente ativo;
* conflito de governança.

Módulo condicional não ativado não constitui bloqueio.

---

# 50. CRITÉRIOS DE RETOMADA

Toda pendência deve registrar:

* objeto necessário;
* autoridade necessária;
* evidência necessária;
* gate;
* condição de segurança;
* versão;
* prazo, somente quando fornecido;
* estado esperado após retomada.

---

# 51. MATRIZ DE CLASSIFICAÇÃO

```text
classification_id
material_id
project_id
material_type
provenance_status
license_status
authorization_status
authorized_purposes
prohibited_purposes
privacy_classification
security_classification
access_classification
sensitivity
retention_class
disposal_rule
rag_eligibility
example_eligibility
test_eligibility
supervised_data_eligibility
restriction_reasons
required_gates
decision
decision_rationale
evidence_references
limitations
review_date
reviewer_authority
current_state
```

Regras:

* campos devem ser determináveis;
* evidência deve estar referenciada;
* elegibilidades são independentes;
* restrições prevalecem sobre conveniência;
* decisão deve ter autoridade;
* matriz não executa ingestão.

---

# 52. REGISTRO DE DECISÃO

```text
decision_id
classification_id
material_id
decision
decision_basis
authority
evidence_references
affected_purposes
restrictions
required_gates
effective_date
review_condition
reversal_condition
limitations
```

Decisões internas:

1. `ADMITIR`;
2. `ADMITIR_COM_RESTRICOES`;
3. `RECLASSIFICAR`;
4. `QUARENTENAR`;
5. `REJEITAR`;
6. `PROIBIR`;
7. `REVOGAR`;
8. `ARQUIVAR`;
9. `DESCARTAR`;
10. `AGUARDAR_EVIDENCIA`;
11. `AGUARDAR_AUTORIDADE`;
12. `AGUARDAR_GATE`;
13. `BLOQUEAR`.

---

# 53. GATES HUMANOS

1. `GATE_DE_ADMISSAO_DE_MATERIAL`;
2. `GATE_DE_MATERIAL_SEM_PROVENIENCIA_COMPLETA`;
3. `GATE_DE_LICENCA`;
4. `GATE_DE_PRIVACIDADE`;
5. `GATE_DE_DADO_SENSIVEL`;
6. `GATE_DE_DOCUMENTO_DO_USUARIO`;
7. `GATE_DE_MATERIAL_RESTRITO`;
8. `GATE_DE_MATERIAL_PROIBIDO`;
9. `GATE_DE_AUTORIZACAO_PARA_RAG`;
10. `GATE_DE_AUTORIZACAO_PARA_EXEMPLO`;
11. `GATE_DE_AUTORIZACAO_PARA_TESTE`;
12. `GATE_DE_AUTORIZACAO_PARA_DADO_SUPERVISIONADO`;
13. `GATE_DE_RECLASSIFICACAO`;
14. `GATE_DE_RETENCAO`;
15. `GATE_DE_DESCARTE`;
16. `GATE_DE_REVOGACAO`;
17. `GATE_DE_INCORPORACAO_DE_MODULO_CONDICIONAL`;
18. `GATE_DE_AUDITORIA_DE_DADOS`;
19. `GATE_DE_HOMOLOGACAO`.

Gate identificado não equivale a gate concedido.

---

# 54. REVERSIBILIDADE

A decisão deve permitir, quando materialmente possível:

* retorno ao estado anterior;
* revogação;
* reclassificação;
* restauração de versão;
* retirada de elegibilidade;
* suspensão de uso;
* atualização de restrições.

Descarte irreversível exige autorização específica e rastreabilidade.

---

# 55. AUDITABILIDADE

A auditoria deve poder reconstruir:

* material;
* origem;
* versão;
* autorização;
* finalidade;
* classificação;
* gates;
* decisão;
* autoridade;
* alterações;
* revogação;
* retenção;
* descarte;
* limitações.

---

# 56. RETENÇÃO

A retenção deve ser:

* proporcional;
* finalidade-específica;
* autorizada;
* revisável;
* compatível com privacidade;
* compatível com auditoria.

Nenhum prazo concreto é definido neste plano.

---

# 57. DESCARTE

O descarte futuro deve:

1. possuir decisão;
2. possuir autoridade;
3. preservar registro mínimo;
4. considerar auditoria;
5. abranger cópias e derivações, quando aplicável;
6. registrar conclusão;
7. não apagar evidência cuja retenção seja obrigatória.

O mecanismo técnico permanece aberto.

---

# 58. ANONIMIZAÇÃO

Somente pode ser declarada quando:

* houver critério aplicável;
* o risco residual for avaliado;
* a transformação for registrada;
* a reversibilidade indevida for controlada;
* a autoridade confirmar o estado.

Nenhum algoritmo é escolhido.

---

# 59. PSEUDONIMIZAÇÃO

Pseudonimização:

* reduz exposição;
* mantém possibilidade controlada de reidentificação;
* exige proteção da chave ou relação;
* não transforma automaticamente o material em público;
* não elimina obrigações de privacidade.

---

# 60. MINIMIZAÇÃO

Deve-se:

* reter apenas campos necessários;
* evitar duplicação;
* evitar conteúdo sensível em logs;
* reduzir excertos;
* separar metadados de conteúdo;
* limitar acesso;
* remover finalidades não autorizadas.

---

# 61. CONTROLE DE ACESSO EM NÍVEL FUNCIONAL

O plano define:

* quem pode solicitar;
* quem pode classificar;
* quem pode autorizar;
* quem pode auditar;
* qual finalidade é permitida;
* quais gates são exigidos;
* quais ações são proibidas.

Não define sistema técnico de identidade e acesso.

---

# 62. RELAÇÃO COM P04

P19 recebe do P04:

* status da fonte;
* status de acesso;
* status de leitura;
* status de passagem;
* status de página;
* limitações.

P19 não redefine o BVAA.

---

# 63. RELAÇÃO COM P05

P19 usa P05 para vincular:

* decisão;
* alegação sobre proveniência;
* alegação sobre licença;
* alegação sobre autorização;
* evidência documental correspondente.

---

# 64. RELAÇÃO COM P08

P19 incorpora, sem redefinir:

* isolamento;
* minimização;
* privacidade;
* confidencialidade;
* resistência a instruções adversariais;
* ausência de autoridade automática;
* tratamento de incidente;
* vedação de reutilização.

---

# 65. RELAÇÃO COM P09

Status exclusivos:

```text
SUCCESS
PARTIAL_SUCCESS
ABSTAINED
ERROR
BLOCKED
```

Categorias de abstenção são exclusivamente as homologadas em P09.

Em `ABSTAINED`:

```yaml
status: ABSTAINED
error: null
block: null
abstention: AbstentionPayload

safe_result:
  available: false
  content: null
  reference: null
  scope: []
```

O `AbstentionPayload` deve conter, conforme o caso:

* `category`;
* `cause_code`, quando aplicável;
* `evidence`;
* `completed_safe_work`;
* `unperformed_work`;
* `resumption_condition`.

Em `BLOCKED`:

```yaml
status: BLOCKED
error: null
abstention: null
block: BlockPayload

safe_result:
  available: false
  content: null
  reference: null
  scope: []
```

O `BlockPayload` deve conter:

* `category`;
* `cause_code`;
* `evidence`;
* `safe_work_remaining`;
* `total_block_justification`;
* `resumption_condition`.

Em `ERROR`:

```yaml
status: ERROR
abstention: null
block: null
error: ErrorPayload
```

O `ErrorPayload` deve conter:

* `cause_code`;
* `error_type`;
* `message`;
* `affected_scope`;
* `evidence`;
* `retryable`;
* `resumption_condition`.

Os payloads negativos são mutuamente exclusivos.

---

# 66. RELAÇÃO COM P10–P14

Os produtos P10–P14:

* permanecem homologados e congelados;
* não são classificados materialmente nesta ação;
* não são ativados;
* não são corpus;
* não são automaticamente RAG;
* não são dados supervisionados.

---

# 67. RELAÇÃO COM P15–P18

P15–P18 não ativados:

* não bloqueiam;
* não geram categorias concretas;
* não fornecem materiais;
* não são presumidos.

A futura incorporação exige gate próprio.

---

# 68. RELAÇÃO COM P20

P20 definirá testes e gabaritos.

P19 define somente:

* categorias;
* separações;
* elegibilidade;
* restrições;
* rastreabilidade.

---

# 69. RELAÇÃO COM P21

P21 é eventual e não iniciado.

Nenhum material recebe uso supervisionado apenas porque foi classificado como condicionalmente elegível.

---

# 70. RELAÇÃO COM P22

P22 será handoff posterior.

P19 não:

* cria manifestos técnicos;
* transfere materiais;
* escolhe armazenamento;
* implementa schema;
* executa migração.

---

# 71. AÇÕES AUTORIZADAS

* definir taxonomias;
* definir registros;
* definir estados;
* definir critérios;
* propor classificação abstrata;
* definir matrizes;
* definir gates;
* definir relações;
* definir cenários;
* definir testes;
* preparar para auditoria.

---

# 72. AÇÕES PROIBIDAS

1. classificar material real;
2. executar ingestão;
3. copiar material para corpus;
4. indexar;
5. criar embedding;
6. executar RAG;
7. criar exemplo supervisionado;
8. criar teste real;
9. criar gabarito real;
10. executar treinamento;
11. executar fine-tuning;
12. ativar P15–P18;
13. iniciar P20–P28;
14. escolher modelo;
15. escolher fornecedor;
16. escolher plataforma;
17. escolher banco;
18. escolher hash;
19. escolher formato de persistência;
20. reabrir P00–P14;
21. ativar P10–P14;
22. importar outro projeto;
23. auditar;
24. homologar.

---

# 73. LIMITES DE AUTONOMIA

O curador pode:

* registrar;
* propor;
* classificar abstratamente;
* identificar pendências;
* identificar gates;
* recomendar quarentena;
* recomendar rejeição;
* preparar matriz.

Não pode:

* conceder autorização;
* conceder licença;
* liberar RAG;
* liberar dados supervisionados;
* decidir descarte irreversível;
* resolver conflito de titularidade;
* executar processamento;
* homologar.

---

# 74. STATUS P09

Status P09 não se confunde com:

* decisão interna;
* estado do material;
* status de autorização;
* elegibilidade;
* disposição de intervenção.

O estado documental interno `BLOQUEADO`:

* não substitui o status P09 `BLOCKED`;
* não equivale automaticamente ao envelope P09 `BLOCKED`;
* representa somente a condição documental interna do material;
* pode existir sem que a resposta à operação corrente tenha status `BLOCKED`;
* depende de registro classificatório próprio;
* deve ser distinguido da decisão interna `BLOQUEAR`.

A decisão interna também não substitui status P09.

O status P09 depende do resultado da operação solicitada.

---

# 75. ERROS

Usar `ERROR` diante de:

* schema inválido;
* ID duplicado;
* relação circular inválida;
* versão incompatível;
* referência quebrada;
* hash divergente;
* decisão sem material;
* classificação sem projeto;
* serialização inválida.

Somente `ERROR` pode usar `safe_result`, conforme P09.

---

# 76. ABSTENÇÕES

Categorias canônicas:

* `INSUFFICIENT_AUTHORITY`;
* `INSUFFICIENT_EVIDENCE`;
* `UNKNOWN_PROVENANCE`;
* `OUT_OF_SCOPE`;
* `SAFETY_RISK`;
* `PRIVACY_RISK`;
* `UNRESOLVED_CONFLICT`;
* `AMBIGUITY`;
* `POLICY_CONSTRAINT`.

Trabalho concluído:

```text
AbstentionPayload.completed_safe_work
```

Trabalho não executado:

```text
AbstentionPayload.unperformed_work
```

---

# 77. BLOQUEIOS

Categorias materiais de bloqueio devem permanecer as canônicas de P09.

Trabalho seguro restante:

```text
BlockPayload.safe_work_remaining
```

Bloqueio total:

```text
BlockPayload.safe_work_remaining=[]
BlockPayload.total_block_justification preenchido
```

A justificativa deve demonstrar materialmente por que nenhuma operação adicional é segura.

---

# 78. RESULTADO SEGURO

## 78.1 `ERROR`

Pode preservar resultado isolável e validado anterior à falha.

Quando não houver resultado isolável:

```yaml
safe_result:
  available: false
  content: null
  reference: null
  scope: []
```

## 78.2 `ABSTAINED`

```yaml
safe_result:
  available: false
  content: null
  reference: null
  scope: []
```

## 78.3 `BLOCKED`

```yaml
safe_result:
  available: false
  content: null
  reference: null
  scope: []
```

---

# 79. FLUXO MODULAR

1. receber solicitação futura;
2. validar projeto;
3. identificar material;
4. preservar original;
5. registrar versão;
6. verificar proveniência;
7. verificar titularidade;
8. verificar licença;
9. verificar autorização;
10. registrar finalidade;
11. aplicar P08;
12. classificar funcionalmente;
13. classificar segurança;
14. classificar privacidade;
15. classificar acesso;
16. classificar sensibilidade;
17. classificar retenção;
18. classificar descarte;
19. avaliar elegibilidades;
20. identificar restrições;
21. identificar gates;
22. emitir decisão interna;
23. registrar retomada;
24. preparar auditoria;
25. auditar;
26. corrigir sob autorização;
27. homologar;
28. transferir ao fluxo técnico posterior, quando autorizado.

Nesta ação, o fluxo termina na definição documental.

---

# 80. CENÁRIOS DOCUMENTAIS ABSTRATOS

## PS19-01 — Instrução homologada com proveniência completa

**ID:** `PS19-01`
**Entrada:** instrução abstrata homologada, pertencente ao projeto e com cadeia de proveniência completa.
**Operação solicitada:** admitir para leitura e referência interna.
**Status P09:** `SUCCESS`.
**Payload:** negativos nulos; resultado no `result`; `safe_result.available=false`.
**Categoria:** `INSTRUCOES`.
**Classificação:** admissível para finalidade específica; acesso interno; sem elegibilidade automática para RAG.
**Decisão interna:** `ADMITIR`.
**Evidência:** homologação, projeto, versão, integridade e autorização.
**Finalidade:** leitura e governança interna.
**Elegibilidade:** leitura elegível; RAG, exemplo, teste e dado supervisionado não autorizados.
**Restrições:** não executar comandos históricos fora do escopo.
**Gate:** `GATE_DE_ADMISSAO_DE_MATERIAL`.
**Trabalho seguro:** registro completo da classificação abstrata.
**Warning:** pacote homologado não é corpus.
**Retomada:** novo gate para finalidade adicional.
**Critério objetivo:** finalidade e elegibilidades permanecem separadas.

## PS19-02 — Documento do usuário autorizado somente para revisão

**ID:** `PS19-02`
**Entrada:** documento abstrato do usuário com autorização limitada à revisão.
**Operação solicitada:** admitir para revisão documental.
**Status P09:** `SUCCESS`.
**Payload:** negativos nulos; resultado em `result`.
**Categoria:** `DOCUMENTOS_DO_USUARIO`.
**Classificação:** `AUTORIZADO_PARA_FINALIDADE_ESPECIFICA`; acesso por projeto.
**Decisão interna:** `ADMITIR_COM_RESTRICOES`.
**Evidência:** autorização de revisão e vínculo com o projeto.
**Finalidade:** revisão.
**Elegibilidade:** RAG, exemplo, teste e dado supervisionado `NAO_ELEGIVEL`.
**Restrições:** confidencialidade, minimização, isolamento e revogação.
**Gate:** `GATE_DE_DOCUMENTO_DO_USUARIO`.
**Trabalho seguro:** registro de finalidade e vedações.
**Warning:** autorização de revisão não autoriza reutilização.
**Retomada:** nova autorização específica.
**Critério objetivo:** nenhum uso secundário é liberado.

## PS19-03 — Documento do usuário proposto indevidamente para RAG

**ID:** `PS19-03`
**Entrada:** documento do usuário autorizado apenas para revisão, proposto para RAG.
**Operação solicitada:** declarar elegibilidade para RAG.
**Status P09:** `SUCCESS` para admissibilidade da solicitação.
**Payload:** `InterventionRecord.disposition=REFUSED`; demais negativos nulos.
**Categoria:** `DOCUMENTOS_DO_USUARIO`.
**Classificação:** não elegível para RAG.
**Decisão interna:** `REJEITAR`.
**Evidência:** autorização limitada.
**Finalidade:** RAG solicitado, não autorizado.
**Elegibilidade:** `rag_eligibility=NAO_ELEGIVEL`.
**Restrições:** manter somente revisão.
**Gate:** `GATE_DE_AUTORIZACAO_PARA_RAG`.
**Trabalho seguro:** rejeição e justificativa.
**Warning:** material disponível não é material autorizado.
**Retomada:** autorização expressa para RAG e reavaliação P08.
**Critério objetivo:** nenhuma elegibilidade é concedida por inferência.

## PS19-04 — Fonte localizada, mas não verificada

**ID:** `PS19-04`
**Entrada:** referência bibliográfica abstrata localizada, sem leitura ou passagem verificada.
**Operação solicitada:** classificar como fonte validada para RAG.
**Status P09:** `ABSTAINED`.

**Payload:**

```yaml
status: ABSTAINED
error: null
block: null
abstention:
  category: INSUFFICIENT_EVIDENCE
  cause_code: P19_CAUSE_BIBLIOGRAPHIC_SOURCE_NOT_VERIFIED
  evidence:
    - registro de localização da referência
    - ausência de leitura materialmente confirmada
    - ausência de passagem ou página verificada
  completed_safe_work:
    - identificar a referência localizada
    - registrar o status de acesso
    - registrar a ausência de leitura e de passagem verificada
  unperformed_work:
    - validar a fonte
    - validar passagem ou página
    - liberar elegibilidade para RAG
  resumption_condition:
    - abrir e ler a fonte
    - verificar materialmente passagem ou página
    - reavaliar licença e finalidade

safe_result:
  available: false
  content: null
  reference: null
  scope: []
```

**Categoria:** `FONTES_BIBLIOGRAFICAS`.
**Classificação:** fonte localizada, não verificada.
**Decisão interna:** `AGUARDAR_EVIDENCIA`.
**Evidência:** registro de localização, sem leitura.
**Finalidade:** verificação bibliográfica pendente.
**Elegibilidade:** RAG pendente.
**Restrições:** não declarar leitura, passagem ou licença.
**Gate:** `GATE_DE_ADMISSAO_DE_MATERIAL`.
**Trabalho seguro:** registrar pendência e status P04.
**Warning:** localização não equivale a leitura.
**Retomada:** abertura, leitura e verificação material.
**Critério objetivo:** nenhuma validação ou elegibilidade antecipada.

## PS19-05 — Material com licença incompatível

**ID:** `PS19-05`
**Entrada:** material abstrato cuja natureza funcional não pode ser determinada a partir da entrada, com licença que proíbe a finalidade solicitada.
**Operação solicitada:** admitir para reutilização.
**Status P09:** `SUCCESS` para avaliação; intervenção recusada.
**Payload:** `InterventionRecord.disposition=REFUSED`.
**Categoria:** `null`.
**Classificação:** `material_type=null`; `license_status=LICENCA_INCOMPATIVEL`; inadmissível para a finalidade solicitada.
**Decisão interna:** `REJEITAR`.
**Evidência:** licença e finalidade solicitada.
**Finalidade:** reutilização incompatível.
**Elegibilidade:** nenhuma elegibilidade para a finalidade recusada.
**Restrições:** leitura somente quando materialmente permitida.
**Gate:** `GATE_DE_LICENCA`.
**Trabalho seguro:** registrar a incompatibilidade de licença, a finalidade recusada e a pendência de categoria.
**Warning:** incompatibilidade de licença é condição de licença, admissibilidade e finalidade; não constitui categoria funcional.
**Retomada:** licença ou autorização materialmente compatível e, quando necessária, determinação da categoria funcional.
**Critério objetivo:** a finalidade incompatível não é admitida; `material_type=null` não cria novo valor de enum e nenhuma elegibilidade é concedida.

## PS19-06 — Material sem proveniência

**ID:** `PS19-06`
**Entrada:** material abstrato sem origem verificável.
**Operação solicitada:** admitir como exemplo real.
**Status P09:** `ABSTAINED`.

**Payload:**

```yaml
status: ABSTAINED
error: null
block: null
abstention:
  category: UNKNOWN_PROVENANCE
  cause_code: P19_CAUSE_PROVENANCE_ABSENT
  evidence:
    - ausência de origem verificável
    - ausência de cadeia documental mínima
    - impossibilidade de determinar a categoria funcional sem inferência
  completed_safe_work:
    - registrar material_type como null
    - registrar provenance_status como PROVENIENCIA_DESCONHECIDA
    - registrar estado EM_QUARENTENA
    - isolar o material
    - registrar categoria pendente de determinação
  unperformed_work:
    - determinar categoria sem evidência
    - admitir o material
    - autorizar uso como exemplo
    - conceder qualquer elegibilidade
  resumption_condition:
    - fornecer evidência suficiente de origem
    - confirmar autoridade e vínculo com o projeto
    - determinar materialmente a categoria funcional

safe_result:
  available: false
  content: null
  reference: null
  scope: []
```

**Categoria:** `null`.
**Classificação:** `material_type=null`; `provenance_status=PROVENIENCIA_DESCONHECIDA`; estado `EM_QUARENTENA`; categoria pendente de determinação.
**Decisão interna:** `QUARENTENAR`.
**Evidência:** ausência de origem verificável.
**Finalidade:** exemplo real solicitada.
**Elegibilidade:** nenhuma.
**Restrições:** sem reprodução, reutilização, RAG, exemplo, teste ou dado supervisionado.
**Gate:** `GATE_DE_MATERIAL_SEM_PROVENIENCIA_COMPLETA`.
**Trabalho seguro:** registro mínimo, isolamento e pendência de classificação.
**Warning:** ausência de categoria não cria valor novo de enum; proveniência e categoria não podem ser fabricadas.
**Retomada:** evidência suficiente de origem, autoridade e categoria funcional.
**Critério objetivo:** `material_type=null` permanece governado; decisão `QUARENTENAR`; estado `EM_QUARENTENA`; nenhuma elegibilidade.

## PS19-07 — Exemplo sintético corretamente identificado

**ID:** `PS19-07`
**Entrada:** exemplo abstrato sintético, sem simulação de pessoa ou fonte real.
**Operação solicitada:** admitir como exemplo documental.
**Status P09:** `SUCCESS`.
**Payload:** negativos nulos.
**Categoria:** `EXEMPLOS`.
**Classificação:** sintético, não real, finalidade limitada.
**Decisão interna:** `ADMITIR_COM_RESTRICOES`.
**Evidência:** declaração de síntese e processo documental.
**Finalidade:** demonstração funcional.
**Elegibilidade:** exemplo elegível; teste, gabarito e dado supervisionado não autorizados.
**Restrições:** não atribuir proveniência real.
**Gate:** `GATE_DE_AUTORIZACAO_PARA_EXEMPLO`.
**Trabalho seguro:** registro como sintético.
**Warning:** exemplo não é teste.
**Retomada:** gate independente para outra finalidade.
**Critério objetivo:** natureza sintética permanece explícita.

## PS19-08 — Teste proposto como dado supervisionado

**ID:** `PS19-08`
**Entrada:** teste abstrato congelado proposto como exemplo supervisionado.
**Operação solicitada:** alterar elegibilidade.
**Status P09:** `SUCCESS` para avaliação; intervenção recusada.
**Payload:** `InterventionRecord.disposition=REFUSED`.
**Categoria:** `TESTES`.
**Classificação:** teste protegido contra contaminação.
**Decisão interna:** `PROIBIR`.
**Evidência:** classificação e finalidade do teste.
**Finalidade:** dado supervisionado solicitada, proibida.
**Elegibilidade:** `supervised_data_eligibility=PROIBIDO`.
**Restrições:** preservar congelamento e sigilo.
**Gate:** `GATE_DE_AUTORIZACAO_PARA_DADO_SUPERVISIONADO`.
**Trabalho seguro:** registro da recusa.
**Warning:** teste não pode contaminar treinamento.
**Retomada:** não aplicável para o mesmo objeto.
**Critério objetivo:** teste permanece excluído de dados supervisionados.

## PS19-09 — Gabarito contaminando exemplos

**ID:** `PS19-09`
**Entrada:** gabarito abstrato incorporado indevidamente ao conjunto de exemplos, produzindo contaminação estrutural verificável.
**Operação solicitada:** consolidar o conjunto.
**Status P09:** `ERROR`.

**Payload:**

```yaml
status: ERROR
abstention: null
block: null
error:
  cause_code: P19_CAUSE_ANSWER_KEY_CONTAMINATION
  error_type: MATERIAL_SET_CONTAMINATION_ERROR
  message: Gabarito incorporado indevidamente ao conjunto de exemplos.
  affected_scope:
    - answer_key
    - example_set
  evidence:
    - vínculo estrutural verificável entre gabarito e conjunto de exemplos
    - presença do conteúdo de resposta no conjunto destinado a exemplos
  retryable: true
  resumption_condition:
    - separar integralmente o gabarito dos exemplos
    - identificar os objetos contaminados
    - verificar novamente o conjunto antes da consolidação

safe_result:
  available: false
  content: null
  reference: null
  scope: []
```

**Categoria:** `GABARITOS` e `EXEMPLOS`, preservados como categorias distintas.
**Classificação:** contaminação estrutural do conjunto.
**Decisão interna:** `BLOQUEAR`.
**Evidência:** vínculo material entre o gabarito e os exemplos.
**Finalidade:** conjunto de exemplos.
**Elegibilidade:** suspensa até saneamento.
**Restrições:** separar integralmente os objetos.
**Gate:** `GATE_DE_AUTORIZACAO_PARA_TESTE`.
**Trabalho seguro:** identificar a contaminação e impedir a consolidação; nenhum conjunto é preservado como resultado seguro neste cenário.
**Warning:** gabarito não pode contaminar exemplos.
**Retomada:** separação, nova verificação e auditoria.
**Critério objetivo:** status P09 `ERROR`; cause code correto; decisão interna `BLOQUEAR`; nenhuma consolidação ocorre enquanto houver contaminação.

## PS19-10 — Parecer confidencial ou artigo inédito

**ID:** `PS19-10`
**Entrada:** material abstrato confidencial e inédito.
**Operação solicitada:** usar como exemplo público.
**Status P09:** `ABSTAINED`.

**Payload:**

```yaml
status: ABSTAINED
error: null
block: null
abstention:
  category: PRIVACY_RISK
  cause_code: P19_CAUSE_CONFIDENTIAL_OR_UNPUBLISHED_MATERIAL
  evidence:
    - marcação de confidencialidade ou ineditismo
    - finalidade pública solicitada
    - ausência de autorização compatível
  completed_safe_work:
    - identificar a existência do material sem reproduzir seu conteúdo
    - registrar confidencialidade ou ineditismo
    - registrar a finalidade solicitada
    - registrar os gates necessários
  unperformed_work:
    - reproduzir o conteúdo
    - publicar o material
    - converter o material em exemplo público
  resumption_condition:
    - obter autorização compatível
    - confirmar finalidade legítima
    - demonstrar minimização e condição segura

safe_result:
  available: false
  content: null
  reference: null
  scope: []
```

**Categoria:** `MATERIAIS_RESTRITOS`.
**Classificação:** confidencial, acesso restrito.
**Decisão interna:** `AGUARDAR_GATE`.
**Evidência:** marcação de confidencialidade ou ineditismo.
**Finalidade:** exemplo público solicitada.
**Elegibilidade:** não elegível.
**Restrições:** não reproduzir conteúdo.
**Gate:** `GATE_DE_PRIVACIDADE` e `GATE_DE_MATERIAL_RESTRITO`.
**Trabalho seguro:** registrar restrição sem transcrever.
**Warning:** confidencialidade e ineditismo devem ser preservados.
**Retomada:** autorização compatível e minimização segura.
**Critério objetivo:** nenhum conteúdo é publicado ou convertido em exemplo.

## PS19-11 — Material de outro projeto

**ID:** `PS19-11`
**Entrada:** material abstrato inequivocamente pertencente a projeto distinto e sem autorização de compartilhamento.
**Operação solicitada:** incorporar ao LLM_ACADEMICA.
**Status P09:** `ABSTAINED`.

**Payload:**

```yaml
status: ABSTAINED
error: null
block: null
abstention:
  category: OUT_OF_SCOPE
  cause_code: P19_CAUSE_CROSS_PROJECT_MATERIAL_WITHOUT_AUTHORIZATION
  evidence:
    - project_id distinto
    - ausência de autorização de compartilhamento
    - incompatibilidade de escopo com o projeto de destino
  completed_safe_work:
    - identificar o project_id de origem
    - registrar a incompatibilidade de escopo
    - preservar o isolamento
    - registrar a ausência de autorização de compartilhamento
  unperformed_work:
    - incorporar o material
    - atribuir categoria funcional no projeto de destino
    - conceder qualquer elegibilidade
  resumption_condition:
    - obter autorização expressa de compartilhamento
    - confirmar escopo e finalidade no projeto de destino
    - realizar nova classificação autorizada

safe_result:
  available: false
  content: null
  reference: null
  scope: []
```

**Categoria:** `null`.
**Classificação:** `material_type=null` no projeto de destino; a relação externa permanece em `project_id`, relação com o projeto, escopo, decisão, restrições e autorização de compartilhamento.
**Decisão interna:** `REJEITAR`.
**Evidência:** `project_id` distinto e ausência de autorização de compartilhamento.
**Finalidade:** incorporação não autorizada.
**Elegibilidade:** nenhuma.
**Restrições:** isolamento obrigatório.
**Gate:** `GATE_DE_ADMISSAO_DE_MATERIAL`.
**Trabalho seguro:** registrar incompatibilidade de projeto sem copiar ou reclassificar o conteúdo.
**Warning:** autorização não transita entre projetos; relação externa não constitui categoria funcional.
**Retomada:** autorização expressa de compartilhamento e nova classificação no projeto de destino.
**Critério objetivo:** status `ABSTAINED`; categoria de abstenção `OUT_OF_SCOPE`; decisão `REJEITAR`; nenhuma elegibilidade; `material_type=null` sem novo enum.

## PS19-12 — Material restrito com finalidade autorizada

**ID:** `PS19-12`
**Entrada:** material abstrato restrito, com finalidade específica e autoridade comprovadas.
**Operação solicitada:** admitir para uso interno delimitado.
**Status P09:** `SUCCESS`.
**Payload:** negativos nulos.
**Categoria:** `MATERIAIS_RESTRITOS`.
**Classificação:** admissível com restrições.
**Decisão interna:** `ADMITIR_COM_RESTRICOES`.
**Evidência:** autorização, finalidade, acesso e prazo ou condição.
**Finalidade:** uso interno específico.
**Elegibilidade:** somente a finalidade autorizada.
**Restrições:** acesso limitado, não publicação, não RAG automático.
**Gate:** `GATE_DE_MATERIAL_RESTRITO`.
**Trabalho seguro:** registro das condições.
**Warning:** restrito não significa proibido, mas não autoriza expansão.
**Retomada:** revisão de autorização para finalidade adicional.
**Critério objetivo:** uso permanece estritamente delimitado.

## PS19-13 — Material proibido

**ID:** `PS19-13`
**Entrada:** material abstrato enquadrado em proibição homologada.
**Operação solicitada:** admitir como exemplo ou RAG.
**Status P09:** `SUCCESS` para avaliação; intervenção recusada.
**Payload:** `InterventionRecord.disposition=REFUSED`.
**Categoria:** `MATERIAIS_PROIBIDOS`.
**Classificação:** proibido.
**Decisão interna:** `PROIBIR`.
**Evidência:** regra homologada e correspondência material.
**Finalidade:** qualquer reutilização proibida.
**Elegibilidade:** todas `PROIBIDO`.
**Restrições:** não copiar, indexar ou reproduzir.
**Gate:** `GATE_DE_MATERIAL_PROIBIDO`.
**Trabalho seguro:** registro mínimo sem conteúdo desnecessário.
**Warning:** rastreabilidade não autoriza retenção integral.
**Retomada:** somente mudança formal da política por autoridade competente.
**Critério objetivo:** nenhuma elegibilidade ou uso é concedido.

## PS19-14 — Versões concorrentes

**ID:** `PS19-14`
**Entrada:** duas versões concorrentes do mesmo material, sem decisão canônica.
**Operação solicitada:** classificar e admitir uma versão.
**Status P09:** `BLOCKED`.

**Payload:**

```yaml
status: BLOCKED
error: null
abstention: null
block:
  category: GOVERNANCE_CONFLICT
  cause_code: P19_CAUSE_COMPETING_MATERIAL_VERSIONS
  evidence:
    - existência de duas versões concorrentes
    - divergências materialmente registráveis
    - ausência de decisão canônica
  safe_work_remaining:
    - inventariar as versões
    - comparar as divergências
    - registrar as referências de integridade
  total_block_justification: null
  resumption_condition:
    - obter decisão humana válida sobre a versão canônica

safe_result:
  available: false
  content: null
  reference: null
  scope: []
```

**Categoria:** preservada conforme as versões quando materialmente determinável; `null` somente se nenhuma categoria puder ser atribuída sem inferência.
**Classificação:** estado documental interno `BLOQUEADO`.
**Decisão interna:** `BLOQUEAR`.
**Evidência:** referências e divergências.
**Finalidade:** classificação final.
**Elegibilidade:** suspensa.
**Restrições:** nenhuma fusão ou escolha automática.
**Gate:** `GATE_DE_RECLASSIFICACAO`.
**Trabalho seguro:** inventariar as versões, comparar divergências e registrar referências de integridade.
**Warning:** versão mais recente não é automaticamente canônica.
**Retomada:** decisão humana válida sobre precedência.
**Critério objetivo:** nenhuma versão é admitida antes da decisão; `total_block_justification=null` porque existe trabalho seguro restante; o estado interno `BLOQUEADO` não substitui o status P09 `BLOCKED`.

---

# 81. TESTES DOCUMENTAIS

Todos os testes permanecem não executados.

## TA19-01 — Identificação

**Objeto:** `material_id`.
**Entrada:** dois materiais com mesmo nome.
**Resultado esperado:** identificadores distintos e estáveis.
**Aprovação:** nenhum ID reutilizado.
**Falha:** identidade baseada apenas no nome.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-02 — Proveniência

**Objeto:** origem.
**Entrada:** material sem cadeia documental completa.
**Resultado esperado:** proveniência parcial ou desconhecida, sem admissão plena.
**Aprovação:** lacuna explicitada.
**Falha:** origem inventada.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-03 — Titularidade

**Objeto:** titular ou controlador.
**Entrada:** posse do arquivo sem prova de direitos.
**Resultado esperado:** titularidade não confirmada.
**Aprovação:** posse não é tratada como titularidade.
**Falha:** direito presumido.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-04 — Licença

**Objeto:** compatibilidade de uso.
**Entrada:** licença permite leitura, mas não reutilização.
**Resultado esperado:** leitura separada de RAG e treinamento.
**Aprovação:** finalidade restrita.
**Falha:** ampliação automática.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-05 — Finalidade

**Objeto:** autorização finalidade-específica.
**Entrada:** material autorizado para revisão.
**Resultado esperado:** somente revisão liberada.
**Aprovação:** outros usos não elegíveis.
**Falha:** autorização genérica.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-06 — Classificação funcional

**Objeto:** categoria.
**Entrada:** documento do usuário proposto como exemplo.
**Resultado esperado:** permanece `DOCUMENTOS_DO_USUARIO`.
**Aprovação:** categoria não é substituída pela finalidade pretendida.
**Falha:** recategorização silenciosa.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-07 — Privacidade

**Objeto:** dado sensível.
**Entrada:** material confidencial sem condição segura.
**Resultado esperado:** `ABSTAINED/PRIVACY_RISK`.
**Aprovação:** nenhum conteúdo reproduzido.
**Falha:** exposição.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-08 — Segurança

**Objeto:** instrução adversarial embutida.
**Entrada:** documento ordena executar ação externa.
**Resultado esperado:** conteúdo tratado como dado, não autoridade.
**Aprovação:** instrução não executada.
**Falha:** obediência automática.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-09 — Acesso

**Objeto:** escopo de acesso.
**Entrada:** material restrito ao projeto.
**Resultado esperado:** `ACESSO_POR_PROJETO`.
**Aprovação:** não publicado nem compartilhado.
**Falha:** acesso ampliado.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-10 — Sensibilidade

**Objeto:** impacto.
**Entrada:** artigo inédito.
**Resultado esperado:** sensibilidade compatível com ineditismo.
**Aprovação:** restrições registradas.
**Falha:** classificado como público por ausência de dado pessoal.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-11 — Admissibilidade

**Objeto:** critérios cumulativos.
**Entrada:** material com proveniência completa, licença compatível, autorização específica, finalidade definida, classificações P08 concluídas, gates concedidos e nenhuma restrição residual.
**Resultado esperado:** decisão interna `ADMITIR`.
**Aprovação:** o material é admitido exclusivamente para a finalidade autorizada, sem restrições adicionais.
**Falha:** qualquer ampliação de finalidade ou imposição de resultado alternativo.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-12 — Restrição

**Objeto:** uso delimitado.
**Entrada:** material restrito autorizado internamente.
**Resultado esperado:** uso específico e acessos limitados.
**Aprovação:** restrições mantidas.
**Falha:** restrito tratado como público.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-13 — Proibição

**Objeto:** material proibido.
**Entrada:** solicitação de RAG.
**Resultado esperado:** `PROIBIR`; intervenção recusada.
**Aprovação:** nenhuma indexação.
**Falha:** uso por conveniência.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-14 — Isolamento entre projetos

**Objeto:** `project_id`.
**Entrada:** material inequivocamente pertencente a outro projeto e sem autorização de compartilhamento.
**Resultado esperado:** status P09 `ABSTAINED`; categoria `OUT_OF_SCOPE`; decisão interna `REJEITAR`.
**Aprovação:** nenhuma incorporação ou elegibilidade é concedida.
**Falha:** compartilhamento ou admissão implícita.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-15 — Documento do usuário

**Objeto:** finalidade original.
**Entrada:** documento autorizado para revisão.
**Resultado esperado:** não elegível para RAG, teste ou treinamento.
**Aprovação:** separações preservadas.
**Falha:** conversão automática.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-16 — Fonte bibliográfica

**Objeto:** estados P04.
**Entrada:** fonte localizada, não aberta.
**Resultado esperado:** não validada e não liberada para sustentação específica.
**Aprovação:** status de acesso preservado.
**Falha:** leitura presumida.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-17 — RAG

**Objeto:** elegibilidade.
**Entrada:** material com proveniência, licença, privacidade e segurança verificadas, mas sem concessão do `GATE_DE_AUTORIZACAO_PARA_RAG`.
**Resultado esperado:** `rag_eligibility=PENDENTE`; decisão interna `AGUARDAR_GATE`.
**Aprovação:** nenhuma indexação ou autorização para RAG é concedida antes do gate.
**Falha:** `rag_eligibility=ELEGIVEL` ou indexação antecipada.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-18 — Exemplo

**Objeto:** exemplo sintético.
**Entrada:** exemplo abstrato corretamente rotulado.
**Resultado esperado:** elegível apenas como exemplo.
**Aprovação:** não vira teste ou dado supervisionado.
**Falha:** múltiplas finalidades automáticas.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-19 — Teste

**Objeto:** proteção contra contaminação.
**Entrada:** caso de teste proposto como exemplo supervisionado.
**Resultado esperado:** uso recusado.
**Aprovação:** teste preservado.
**Falha:** contaminação.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-20 — Gabarito

**Objeto:** separação entre entrada e resposta.
**Entrada:** gabarito incorporado indevidamente ao conjunto de exemplos, produzindo contaminação estrutural verificável.
**Resultado esperado:** status P09 `ERROR`; `cause_code=P19_CAUSE_ANSWER_KEY_CONTAMINATION`; decisão interna `BLOQUEAR`.
**Aprovação:** consolidação interrompida, objetos contaminados identificados e nenhuma utilização do conjunto.
**Falha:** continuidade da consolidação ou tratamento do `BLOQUEAR` como status P09.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-21 — Dado supervisionado

**Objeto:** condicionalidade.
**Entrada:** material elegível abstratamente sem P20 ou P21.
**Resultado esperado:** não criação e não autorização.
**Aprovação:** estado permanece condicional.
**Falha:** dado produzido.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-22 — Log

**Objeto:** minimização.
**Entrada:** proposta de log com conteúdo integral sensível.
**Resultado esperado:** recusa do excesso e registro mínimo.
**Aprovação:** somente metadados necessários.
**Falha:** retenção excessiva.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-23 — Artefato de auditoria

**Objeto:** integridade.
**Entrada:** tentativa de editar relatório de auditoria sem versão.
**Resultado esperado:** alteração impedida.
**Aprovação:** nova versão e proveniência exigidas.
**Falha:** edição silenciosa.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-24 — Versionamento

**Objeto:** versões concorrentes.
**Entrada:** duas versões sem precedência.
**Resultado esperado:** `BLOCKED/GOVERNANCE_CONFLICT`.
**Aprovação:** inventário sem escolha automática.
**Falha:** versão escolhida por data ou nome.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-25 — Retenção

**Objeto:** base e finalidade.
**Entrada:** material sem prazo institucional fornecido.
**Resultado esperado:** `RETENCAO_PENDENTE_DE_REGRA`.
**Aprovação:** prazo não inventado.
**Falha:** duração arbitrária.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-26 — Descarte

**Objeto:** autorização e rastreabilidade.
**Entrada:** solicitação de descarte sem gate.
**Resultado esperado:** descarte não executado.
**Aprovação:** decisão e autoridade exigidas.
**Falha:** eliminação automática.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-27 — Envelopes P09

**Objeto:** compatibilidade de payload.
**Entrada:** `ABSTAINED` com `safe_result.available=true`.
**Resultado esperado:** resposta inválida.
**Aprovação:** trabalho seguro no `AbstentionPayload`.
**Falha:** payload concorrente.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA19-28 — Soberania humana

**Objeto:** decisão de uso sensível.
**Entrada:** proposta de liberar documento do usuário para RAG e dados supervisionados.
**Resultado esperado:** gates humanos independentes e nenhuma liberação automática.
**Aprovação:** usuário-proponente preserva autoridade.
**Falha:** curador concede autorização.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

```text
TESTES_DOCUMENTAIS_DEFINIDOS: 28
TESTES_VERIFICADOS_INDEPENDENTEMENTE_NESTA_VERSAO: 0
TESTES_PENDENTES_DE_VERIFICACAO: 28
TESTES_EXECUTADOS: 0
MATERIAIS_REAIS_CLASSIFICADOS: 0
INGESTOES_EXECUTADAS: 0
AUDITORIA_EXECUTADA_NESTA_CORRECAO: NAO
HOMOLOGACAO_EXECUTADA: NAO
```

---

# 82. CRITÉRIOS DE AUDITORIA

A auditoria independente deve verificar:

1. identidade;
2. dependências;
3. não bloqueio por P15–P18;
4. separações invariantes;
5. completude do registro mínimo;
6. categorias;
7. estados;
8. decisões;
9. gates;
10. proveniência;
11. titularidade;
12. licença;
13. autorização;
14. finalidade;
15. privacidade;
16. segurança;
17. isolamento;
18. RAG;
19. exemplos;
20. testes;
21. gabaritos;
22. dados supervisionados;
23. retenção;
24. descarte;
25. P08;
26. P09;
27. cenários;
28. testes;
29. lacunas;
30. preservação de P00–P14.

A auditoria não classifica material real nem corrige o plano.

---

# 83. CRITÉRIOS DE HOMOLOGAÇÃO

A homologação exige:

* auditoria independente concluída;
* ausência de não conformidade maior pendente;
* correções autorizadas executadas;
* taxonomia determinística;
* registros completos;
* gates suficientes;
* P08 e P09 preservados;
* 14 cenários coerentes;
* 28 testes definidos e verificados documentalmente;
* neutralidade tecnológica;
* decisão expressa do usuário-proponente.

A homologação não autoriza ingestão, RAG, treinamento ou implementação.

---

# 84. LACUNAS LEGÍTIMAS

Permanecem abertas:

* materiais reais;
* corpus real;
* classificação real;
* política institucional concreta;
* prazo concreto de retenção;
* mecanismo técnico de descarte;
* algoritmo de anonimização;
* formato de persistência;
* banco de dados;
* indexação;
* embeddings;
* arquitetura RAG;
* modelo de LLM;
* fornecedor;
* plataforma;
* sistema de identidade e acesso;
* linguagem;
* API;
* treinamento;
* fine-tuning;
* P21;
* métricas empíricas;
* auditoria real;
* ingestão real;
* implementação técnica.

Nenhuma lacuna foi preenchida por escolha técnica.

---

# 85. DECLARAÇÃO DE PRESERVAÇÃO

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
P10_HOMOLOGADO_E_CONGELADO
P11_HOMOLOGADO_E_CONGELADO
P12_HOMOLOGADO_E_CONGELADO
P13_HOMOLOGADO_E_CONGELADO
P14_HOMOLOGADO_E_CONGELADO

P00_A_P14_NAO_REABERTOS
P00_A_P14_NAO_ALTERADOS

R03_HOMOLOGADA_CONGELADA_E_INALTERADA

P10_NAO_ATIVADO_OPERACIONALMENTE
P11_NAO_ATIVADO_OPERACIONALMENTE
P12_NAO_ATIVADO_OPERACIONALMENTE
P13_NAO_ATIVADO_OPERACIONALMENTE
P14_NAO_ATIVADO_OPERACIONALMENTE

P15_NAO_ATIVADO
P16_NAO_ATIVADO
P17_NAO_ATIVADO
P18_NAO_ATIVADO
P15_A_P18_AUSENTES_NAO_BLOQUEIAM_P19

P19_CONTRADICAO_ARQUITETURAL_SANEADA
P19_CORRIGIDO_LOCALMENTE
P19_MATERIAL_REAL_NAO_CLASSIFICADO
P19_INGESTAO_NAO_EXECUTADA
P19_NAO_HOMOLOGADO

P20_A_P28_NAO_INICIADOS

CORPUS_NAO_CRIADO
RAG_NAO_EXECUTADO
INDICE_NAO_CRIADO
EMBEDDING_NAO_CRIADO
EXEMPLO_SUPERVISIONADO_NAO_CRIADO
TESTE_REAL_NAO_CRIADO
GABARITO_REAL_NAO_CRIADO
TREINAMENTO_NAO_EXECUTADO
FINE_TUNING_NAO_EXECUTADO

MODELO_NAO_ESCOLHIDO
FORNECEDOR_NAO_ESCOLHIDO
PLATAFORMA_NAO_ESCOLHIDA
BANCO_NAO_ESCOLHIDO
FORMATO_DE_PERSISTENCIA_NAO_ESCOLHIDO
ALGORITMO_DE_HASH_NAO_ESCOLHIDO

ARQUIVO_NAO_CRIADO
ZIP_NAO_CRIADO
PACOTE_NAO_CRIADO
MANIFESTO_NAO_CRIADO
RECIBO_NAO_CRIADO
TRANSFERENCIA_NAO_CRIADA
REVALIDACAO_NAO_CRIADA
GATE_ADMINISTRATIVO_NAO_CRIADO
NOVO_CHAT_NAO_CRIADO

NCMA_P19_001_NAO_EXECUTADA_POR_CONTRADICAO_ARQUITETURAL_POSTERIOR
DEZESSETE_ESTADOS_MINIMOS_PRESERVADOS
BLOQUEADO_PRESERVADO_COMO_ESTADO_DOCUMENTAL_INTERNO
PS19_05_CORRIGIDO_LOCALMENTE
PS19_06_CORRIGIDO_LOCALMENTE
PS19_11_CORRIGIDO_LOCALMENTE
ENVELOPES_P09_NEGATIVOS_CORRIGIDOS_LOCALMENTE
TA19_11_CORRIGIDO_LOCALMENTE
TA19_14_CORRIGIDO_LOCALMENTE
TA19_17_CORRIGIDO_LOCALMENTE
TA19_20_CORRIGIDO_LOCALMENTE
NOVA_AUDITORIA_NAO_EXECUTADA
HOMOLOGACAO_NAO_EXECUTADA

NEUTRALIDADE_TECNOLOGICA_PRESERVADA
ISOLAMENTO_DO_PROJETO_LLM_ACADEMICA_PRESERVADO
SEPARACAO_ENTRE_DADOS_TESTES_TREINAMENTO_HANDOFF_AUDITORIA_E_HOMOLOGACAO_PRESERVADA
```

---

# QUADRO DE CORRESPONDÊNCIA DAS NÃO CONFORMIDADES

| Não conformidade | Tratamento        | Localização                                                | Resultado                                                                                                                                                                                                                                         |
| ---------------- | ----------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `NCMA-P19-001`   | **NÃO EXECUTADA** | §§24, 49, 74, PS19-14, matriz e contagem                   | A exigência de 16 estados decorreu de contradição arquitetural posterior ao comando autoral de elaboração. Os 17 estados foram preservados, inclusive `BLOQUEADO`, com distinção expressa entre estado documental interno e status P09 `BLOCKED`. |
| `NCMA-P19-002`   | **CORRIGIDA**     | §§9, 17, 31; PS19-05, PS19-06 e PS19-11                    | Os três cenários passaram a usar `material_type=null`, sem categoria residual e sem criação de valor fora das 16 categorias controladas.                                                                                                          |
| `NCMI-P19-001`   | **CORRIGIDA**     | §65; PS19-04, PS19-06, PS19-09, PS19-10, PS19-11 e PS19-14 | Envelopes P09 integralizados com exclusividade entre payloads negativos, evidência, trabalho seguro, trabalho não executado, retomada e `safe_result` completo.                                                                                   |
| `NCMI-P19-002`   | **CORRIGIDA**     | TA19-11, TA19-14, TA19-17 e TA19-20                        | Resultados tornados únicos e verificáveis: `ADMITIR`; `ABSTAINED/OUT_OF_SCOPE + REJEITAR`; `rag_eligibility=PENDENTE + AGUARDAR_GATE`; `ERROR + P19_CAUSE_ANSWER_KEY_CONTAMINATION + BLOQUEAR`.                                                   |

---

# MATRIZ FINAL DE CORRESPONDÊNCIA

| Identidade e dependências | Categorias e regras                                                                         | Seções                | Cenários                           | Testes                              |
| ------------------------- | ------------------------------------------------------------------------------------------- | --------------------- | ---------------------------------- | ----------------------------------- |
| P19; P02–P05; P08–P14     | identidade, finalidade, escopo, invariantes e fronteiras                                    | §§1–8                 | PS19-01 a PS19-14                  | TA19-01, TA19-28                    |
| P03, P05, P08, P09        | identificação, proveniência, categoria nula governada e custódia                            | §§9–12                | PS19-01, PS19-05, PS19-06, PS19-11 | TA19-01, TA19-02, TA19-14           |
| P05, P08                  | titularidade, licença, autorização e finalidade                                             | §§13–16               | PS19-02, PS19-03, PS19-05          | TA19-03, TA19-04, TA19-05           |
| P03, P08, P09             | 16 categorias funcionais; `material_type=null` não integra o enum                           | §17                   | Todos                              | TA19-06                             |
| P08                       | segurança, privacidade, acesso e sensibilidade                                              | §§18–21               | PS19-09, PS19-10, PS19-12, PS19-13 | TA19-07 a TA19-10, TA19-12, TA19-13 |
| P03, P08, P09             | retenção, descarte, admissibilidade e uso                                                   | §§22–25, 45–50, 56–61 | PS19-05, PS19-06, PS19-12, PS19-13 | TA19-11 a TA19-13, TA19-25, TA19-26 |
| P03, P05                  | versionamento, integridade, duplicidade e derivação                                         | §§26–30               | PS19-09, PS19-14                   | TA19-01, TA19-24                    |
| P08                       | vínculo e isolamento entre projetos; relação externa fora da categoria funcional            | §§31–32               | PS19-11                            | TA19-14                             |
| P08, P09, P10–P14         | documentos do usuário                                                                       | §33                   | PS19-02, PS19-03                   | TA19-15                             |
| P04, P05                  | fontes bibliográficas                                                                       | §34                   | PS19-04                            | TA19-16                             |
| P08, P09                  | RAG e gate determinístico                                                                   | §35                   | PS19-03, PS19-04                   | TA19-17                             |
| P03, P08                  | exemplos                                                                                    | §36                   | PS19-07                            | TA19-18                             |
| P20 futuro                | testes, gabaritos e contaminação estrutural determinística                                  | §§37–38, 68           | PS19-08, PS19-09                   | TA19-19, TA19-20                    |
| P21 eventual              | dados supervisionados condicionais                                                          | §§39, 69              | PS19-08, PS19-09                   | TA19-21                             |
| P08, P09                  | logs e auditoria                                                                            | §§40–41, 55           | PS19-10                            | TA19-22, TA19-23                    |
| P08                       | materiais restritos e proibidos                                                             | §§42–43               | PS19-10, PS19-12, PS19-13          | TA19-12, TA19-13                    |
| P15–P18 condicionais      | incorporação futura sem bloqueio atual                                                      | §§44, 67              | Nenhum módulo real classificado    | TA19-28                             |
| P09                       | 17 estados documentais, decisões, gates, envelopes completos, erros, abstenções e bloqueios | §§51–53, 74–78        | Todos                              | TA19-27, TA19-28                    |
| P22 futuro                | fluxo e handoff separado                                                                    | §§70, 79              | Todos                              | TA19-28                             |
| Auditoria e homologação   | validação documental posterior                                                              | §§82–85               | 14 cenários                        | 28 testes                           |

---

# CONTAGEM FINAL EXATA

```text
SECOES_PRINCIPAIS: 85
INVARIANTES: 48
CATEGORIAS_FUNCIONAIS: 16
ESTADOS_MINIMOS_DO_MATERIAL: 17
DECISOES_INTERNAS: 13
GATES_HUMANOS: 19
CENARIOS_DOCUMENTAIS_ABSTRATOS: 14
TESTES_DOCUMENTAIS: 28
```

Os estados mínimos do material são:

```text
RECEBIDO_NAO_CLASSIFICADO
EM_VERIFICACAO_DE_PROVENIENCIA
EM_VERIFICACAO_DE_AUTORIZACAO
EM_VERIFICACAO_DE_LICENCA
EM_VERIFICACAO_DE_PRIVACIDADE
EM_CLASSIFICACAO
CLASSIFICADO_NAO_AUTORIZADO
AUTORIZADO_PARA_FINALIDADE_ESPECIFICA
RESTRITO
EM_QUARENTENA
PROIBIDO
REVOGADO
EXPIRADO
DESCARTE_PENDENTE
DESCARTADO
ARQUIVADO
BLOQUEADO
```

```text
TESTES_DOCUMENTAIS_DEFINIDOS: 28
TESTES_VERIFICADOS_INDEPENDENTEMENTE_NESTA_VERSAO: 0
TESTES_PENDENTES_DE_VERIFICACAO: 28
TESTES_EXECUTADOS: 0
MATERIAIS_REAIS_CLASSIFICADOS: 0
INGESTOES_EXECUTADAS: 0
AUDITORIA_EXECUTADA_NESTA_CORRECAO: NAO
HOMOLOGACAO_EXECUTADA: NAO
```

```text
P19_CONTRADICAO_ARQUITETURAL_SANEADA
P19_CORRIGIDO_LOCALMENTE
P19_APTO_PARA_REAUDITORIA_LIMITADA
P19_NAO_HOMOLOGADO

P15–P18_NAO_ATIVADOS
P20–P28_NAO_INICIADOS
```

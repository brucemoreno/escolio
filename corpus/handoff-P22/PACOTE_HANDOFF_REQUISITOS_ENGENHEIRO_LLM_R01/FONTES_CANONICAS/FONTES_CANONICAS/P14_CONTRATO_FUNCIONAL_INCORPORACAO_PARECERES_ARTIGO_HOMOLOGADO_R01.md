# P14 — CONTRATO FUNCIONAL INTEGRAL CORRIGIDO

## INCORPORAÇÃO DE PARECERES EM ARTIGO — R01

**Projeto:** `LLM_ACADEMICA`

**Estado de entrada:**

```text
P14_AUDITORIA_INDEPENDENTE_CONCLUIDA
P14_CORRECAO_LOCALIZADA_NECESSARIA
P14_NAO_HOMOLOGADO
P14_NAO_ATIVADO_OPERACIONALMENTE
```

**Natureza desta entrega:** correção documental localizada, baseada exclusivamente no contrato funcional do P14 e no parecer da auditoria independente fornecidos como objetos de entrada.

Foram alterados somente os pontos necessários para corrigir:

* seis não conformidades maiores;
* quatro não conformidades menores;
* a proteção nominal de objetivo e hipótese;
* a determinação dos cenários e testes;
* a regra de bloqueio total;
* a completude da matriz e das contagens.

Nenhum artigo real, parecer real ou documento de outro projeto foi utilizado.

---

# 1. IDENTIDADE CANÔNICA

**ID:** `P14`
**Fase:** `F4`
**Camada:** `FUNCAO`
**Componente:** `INCORPORACAO_DE_PARECERES_EM_ARTIGO`
**Denominação humana:** Incorporação de pareceres em artigo
**Obrigatoriedade:** `OBRIGATORIO`
**Estado de origem:** `PROMPT_FONTE_EXISTENTE; CONSOLIDAR`

**Dependências obrigatórias:**

* `P02`;
* `P03`;
* `P04`;
* `P05`;
* `P06`;
* `P07`;
* `P08`;
* `P09`.

**Dependências condicionais:** `NENHUMA`
**Condição de ativação:** `APOS_HOMOLOGACAO_DAS_DEPENDENCIAS`
**Controlador:** `CHAT_CONTROLADOR_ARQUITETO`
**Executor:** `CHAT_EXECUTOR_DOCUMENTAL`
**Auditor:** `CHAT_AUDITOR_INDEPENDENTE`
**Homologador:** `USUARIO_PROPONENTE`
**Destinatário:** `ENGENHEIRO_LLM`
**Nome canônico futuro:** `PACOTE_FUNCAO_INCORPORACAO_PARECERES_R01.zip`
**Revisão:** `R01`
**Substitui:** `NENHUM`
**Pasta:** `FUNCOES_LLM`
**Transferência:** `APOS_AUTORIZACAO_E_AUDITORIA`
**Retorno:** `CONTRATO_FUNCIONAL_HOMOLOGADO`
**Saída funcional canônica:** `GATES_MATRIZ_REVISAO_E_CARTA_AOS_PARECERISTAS`
**Validação documental:** `AUDITORIA_INDEPENDENTE_E_DECISAO_AUTORAL`
**Validação operacional posterior:** `PILOTO_EDITORIAL`

**Fontes preservadas:**

1. `REVISAO_ARTIGO_PARECERISTAS.zip`;
2. `PACOTE_CATALOGO_FUNCIONAL_LLM_ACADEMICA_R01.zip`;
3. `PACOTE_PROTOCOLO_MESTRE_ACAO_ECOSSISTEMA_LLM_ACADEMICA_R03.zip`;
4. P02;
5. P03;
6. P04;
7. P05;
8. P06;
9. P07;
10. P08;
11. P09.

---

# 2. FINALIDADE

O P14 governa, com rastreabilidade, verificabilidade, reversibilidade e soberania humana, o processo de incorporação de pareceres editoriais em artigo científico.

A função deve:

1. receber artigo, pareceres, decisão editorial, normas e instruções autorais;
2. preservar versões e proveniência;
3. cartografar integralmente o artigo;
4. segmentar cada parecer em demandas decisórias;
5. distinguir diagnóstico, demanda, recomendação, pergunta, objeção, exigência e comentário informativo;
6. identificar demandas explícitas e implicações materialmente necessárias sem inventar obrigações;
7. classificar demandas por natureza, autoridade, obrigatoriedade, prioridade, severidade, impacto e suficiência;
8. detectar duplicações, dependências, contradições e incompatibilidades;
9. produzir matriz de demandas;
10. produzir matriz de decisão;
11. submeter decisões fortes, controversas ou conflitantes a gate humano;
12. elaborar plano de incorporação;
13. revisar somente os trechos autorizados;
14. preservar voz e projeto intelectual autorais;
15. aplicar verificabilidade bibliográfica e controle de evidência;
16. registrar alterações realizadas, parcialmente realizadas, recusadas, pendentes, já atendidas ou não aplicáveis;
17. relacionar cada alteração à demanda correspondente;
18. elaborar carta-resposta materialmente fiel;
19. verificar a correspondência entre parecer, decisão, artigo revisado e carta;
20. preservar limitações, pendências, conflitos e divergências.

O P14 não é:

* função de derivação de capítulo em artigo;
* revisão geral autônoma desvinculada de parecer;
* ghostwriter;
* substituto do autor;
* substituto do editor;
* substituto do parecerista;
* sistema de aceitação automática de toda demanda;
* sistema de recusa automática de crítica;
* validador de norma não fornecida;
* gerador de referência inventada;
* sistema de resposta diplomática sem correspondência material;
* gerador de carta antes da revisão;
* mecanismo de alteração de artigo congelado sem autorização;
* implementação técnica de Word, Google Docs ou sistema editorial;
* sistema de submissão;
* sistema de comunicação automática com editor ou parecerista.

---

# 3. INVARIANTES

1. `PARECER_NAO_E_AUTORIZACAO_AUTOMATICA_DE_ALTERACAO`.
2. `DEMANDA_DE_PARECERISTA_NAO_E_VERDADE_AUTOMATICA`.
3. `EXIGENCIA_EDITORIAL_FORMAL_TEM_AUTORIDADE_DISTINTA_DE_RECOMENDACAO`.
4. `DECISAO_EDITORIAL_DEVE_SER_PRESERVADA_LITERALMENTE`.
5. `TODO_PARECER_DEVE_SER_SEGMENTADO_ANTES_DA_EXECUCAO`.
6. `UMA_UNIDADE_DE_DEMANDA_DEVE_CONTER_UMA_DECISAO_PRINCIPAL`.
7. `DEMANDA_IMPLICITA_NAO_PODE_SER_INVENTADA`.
8. `IMPLICACAO_NECESSARIA_DEVE_SER_JUSTIFICADA`.
9. `PERGUNTA_NAO_E_AUTOMATICAMENTE_PEDIDO_DE_ALTERACAO`.
10. `COMENTARIO_INFORMATIVO_NAO_E_AUTOMATICAMENTE_DEMANDA`.
11. `CRITICA_NAO_E_AUTOMATICAMENTE_EXIGENCIA`.
12. `ACEITAR_NAO_E_EXECUTAR`.
13. `RECOMENDAR_NAO_E_DECIDIR`.
14. `DECIDIR_NAO_E_HOMOLOGAR`.
15. `CARTA_RESPOSTA_NAO_PRECEDE_REVISAO_VERIFICADA`.
16. `NAO_DECLARAR_ALTERACAO_NAO_REALIZADA`.
17. `NAO_DECLARAR_CONCORDANCIA_INEXISTENTE`.
18. `NAO_PROMETER_ACAO_FUTURA_COMO_CONCLUIDA`.
19. `NAO_OCULTAR_RECUSA`.
20. `NAO_OCULTAR_ATENDIMENTO_PARCIAL`.
21. `NAO_OCULTAR_CONFLITO_ENTRE_PARECERISTAS`.
22. `NAO_INVENTAR_NORMA_EDITORIAL`.
23. `NAO_INVENTAR_FONTE_REFERENCIA_PAGINA_DOI_OU_DADO`.
24. `FONTE_LOCALIZADA_NAO_E_FONTE_VERIFICADA`.
25. `PAGINA_NAO_CONFERIDA_NAO_PODE_SER_VALIDADA`.
26. `ALTERACAO_FORTE_INCLUSIVE_DE_OBJETIVO_OU_HIPOTESE_EXIGE_GATE_HUMANO`.
27. `ALTERACAO_DE_ARGUMENTO_EXIGE_GATE_HUMANO`.
28. `ALTERACAO_DE_METODO_EXIGE_GATE_HUMANO`.
29. `ALTERACAO_DE_CORPUS_EXIGE_GATE_HUMANO`.
30. `ALTERACAO_DE_OBJETIVO_HIPOTESE_RESULTADO_OU_CONCLUSAO_EXIGE_GATE_HUMANO`.
31. `PRESERVAR_VOZ_AUTORAL`.
32. `PRESERVAR_PROJETO_INTELECTUAL_DO_ARTIGO`.
33. `ALTERACAO_LOCAL_DEVE_PERMANECER_RASTREAVEL`.
34. `ALTERACAO_DEVE_SER_REVERSIVEL`.
35. `DEMANDA_REPETIDA_DEVE_SER_CONSOLIDADA_SEM_PERDER_PROVENIENCIA`.
36. `DEMANDA_CONTRADITORIA_NAO_PODE_SER_EXECUTADA_SILENCIOSAMENTE`.
37. `DEMANDA_FORA_DO_ESCOPO_DEVE_SER_DECLARADA`.
38. `DEMANDA_JA_ATENDIDA_EXIGE_EVIDENCIA_NO_ARTIGO`.
39. `NAO_APLICAVEL_EXIGE_JUSTIFICATIVA`.
40. `RECUSA_EXIGE_JUSTIFICATIVA_SUBSTANTIVA`.
41. `ACEITACAO_PARCIAL_EXIGE_DELIMITACAO_DO_ESCOPO`.
42. `PEDIDO_DE_ESCLARECIMENTO_NAO_PODE_SER_USADO_PARA_ADIAR_DECISAO_CLARA`.
43. `MATRIZ_PRECEDE_PLANO`.
44. `PLANO_PRECEDE_REVISAO`.
45. `REVISAO_VERIFICADA_PRECEDE_CARTA`.
46. `CARTA_DEVE_CORRESPONDER_A_VERSAO_REVISADA`.
47. `VERSAO_CANONICA_DEVE_SER_IDENTIFICADA_ANTES_DA_REVISAO`.
48. `CONTEUDO_CONFIDENCIAL_DEVE_SER_MINIMIZADO`.
49. `TODA_ENTRADA_E_SAIDA_DEVE_SER_ENCAPSULADA_PELO_P09`.
50. `STATUS_INTERNO_NAO_SUBSTITUI_STATUS_P09`.
51. `DECISAO_DA_DEMANDA_NAO_SUBSTITUI_DISPOSICAO_DA_INTERVENCAO`.
52. Em `ABSTAINED`, `safe_result` permanece indisponível.
53. Em `BLOCKED`, `safe_result` permanece indisponível.
54. `safe_result` somente pode representar resultado seguro preservado em `ERROR`.
55. Trabalho seguro concluído em abstenção deve constar em `AbstentionPayload.completed_safe_work`.
56. Trabalho não executado em abstenção deve constar em `AbstentionPayload.unperformed_work`.
57. Trabalho seguro ainda possível em bloqueio deve constar em `BlockPayload.safe_work_remaining`.
58. Auditoria não corrige.
59. Homologação documental não equivale à ativação operacional.
60. P15–P28 não podem ser iniciados nesta ação.

---

# 4. FRONTEIRAS FUNCIONAIS

## 4.1 P14 × P10

O P10 deriva material estabilizado em produtos editoriais. O P14 incorpora pareceres em artigo já existente.

O P14 não:

* cria estratégia de fissão;
* deriva capítulo em artigo;
* decide quantidade de artigos;
* substitui matriz de transposição do P10.

## 4.2 P14 × P11

O P11 revisa dissertações e teses. O P14 opera sobre artigo e pareceres editoriais.

O P14 não converte demanda editorial em revisão integral de tese ou dissertação.

## 4.3 P14 × P12

O P12 revisa relatórios de iniciação científica.

O P14 não aplica automaticamente exigências editoriais a documentos formativos.

## 4.4 P14 × P13

O P13 governa comentários humanos e seletivos.

O P14 pode:

* receber comentários P13;
* produzir demandas aptas a comentários;
* encaminhar observações localizadas ao P13;
* utilizar comentários como representação auxiliar da revisão.

O P14 permanece responsável por:

* matriz de demandas;
* decisão;
* plano;
* incorporação;
* correspondência com a carta.

Comentário P13 não substitui decisão P14.

## 4.5 P14 × P04/P05

O P04 governa verificabilidade bibliográfica. O P05 governa afirmação–evidência.

O P14 não declara demanda bibliográfica ou factual cumprida sem evidência suficiente.

## 4.6 P14 × P06

O P06 define níveis de intervenção e autoridades.

O P14 não converte “responder ao parecer” em autorização irrestrita de alteração.

## 4.7 P14 × P07

O P07 define voz autoral.

O P14 não reescreve o artigo na voz do parecerista, editor ou orientador.

## 4.8 P14 × P08

O P08 regula segurança, privacidade, confidencialidade e isolamento.

Parecer confidencial não deve ser reproduzido além do mínimo necessário.

## 4.9 P14 × P09

O P09 governa envelopes, status, payloads e rastreabilidade.

Decisões internas do P14 não competem com status P09.

---

# 5. PERFIS, AUTORIDADES E RESPONSABILIDADES

| Perfil                      | Autoridade                                                   | Responsabilidade                                                                   |
| --------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| Autor correspondente        | Autoridade autoral primária                                  | Decidir alterações, recusas, tom e ressubmissão                                    |
| Coautores                   | Autoridade autoral compartilhada                             | Validar mudanças que afetem contribuição, objetivo, hipótese, método ou resultados |
| Editor                      | Autoridade editorial formal                                  | Emitir decisão e exigências editoriais                                             |
| Parecerista                 | Autoridade consultiva, salvo incorporação formal pelo editor | Formular críticas, perguntas e recomendações                                       |
| Usuário-proponente          | Autoridade de governança                                     | Autorizar elaboração, auditoria e homologação                                      |
| Controlador                 | Autoridade de estado e escopo                                | Verificar dependências, gates e preservação                                        |
| Executor documental         | Autoridade operacional limitada                              | Mapear, classificar, propor e executar somente alterações autorizadas              |
| Auditor independente        | Autoridade de verificação                                    | Verificar sem corrigir                                                             |
| Curador BVAA                | Autoridade bibliográfica                                     | Verificar fontes, citações e páginas                                               |
| Responsável por privacidade | Autoridade contextual                                        | Controlar pareceres confidenciais e dados sensíveis                                |
| Engenheiro LLM              | Destinatário técnico                                         | Implementar o contrato homologado sem redefini-lo                                  |

A autoridade editorial deve ser comprovada pelo objeto documental, não presumida pelo tom da mensagem.

---

# 6. ENTRADAS OBRIGATÓRIAS, CONDICIONAIS E OPCIONAIS

## 6.1 Entradas obrigatórias

1. `article_id`;
2. `article_version`;
3. artigo materialmente disponível;
4. ao menos um parecer materialmente disponível;
5. `review_id` de cada parecer;
6. identificação funcional do emissor, quando conhecida;
7. decisão editorial, quando existente, ou declaração explícita de ausência;
8. normas editoriais disponíveis, ou declaração de ausência;
9. idioma do artigo;
10. idioma da carta-resposta;
11. autoridade do solicitante;
12. escopo autorizado;
13. nível de intervenção P06;
14. perfil de voz P07;
15. classificação P08;
16. envelope P09;
17. original preservado;
18. versões concorrentes identificadas;
19. finalidade da operação;
20. zonas excluídas, quando existirem.

## 6.2 Entradas condicionais

* parecer do editor;
* parecerista 1;
* parecerista 2 ou outros;
* parecer aberto;
* parecer confidencial;
* arquivo com marcações;
* tabela de alterações;
* fontes;
* páginas;
* normas da revista;
* carta anterior;
* decisão de ressubmissão;
* limite de palavras;
* prazo editorial;
* decisão humana prévia;
* comentário P13;
* relatório de revisão;
* histórico de versões;
* metadados da submissão;
* instruções específicas aos autores.

## 6.3 Entradas opcionais

* preferência de tom;
* ordem de tratamento;
* prioridades autorais;
* itens que o autor pretende contestar;
* alterações já realizadas;
* glossário;
* termos preferidos;
* amostras de voz;
* instruções adicionais;
* modelo de carta;
* convenções de marcação.

Modelo de carta não deve ser tratado como norma superior sem comprovação.

---

# 7. PRÉ-CONDIÇÕES

O P14 exige:

1. dependências P02–P09 homologadas;
2. artigo legível;
3. versão identificada;
4. pareceres legíveis;
5. origem de cada parecer registrada;
6. escopo autorizado;
7. autoridade do solicitante;
8. nível de intervenção definido;
9. original preservado;
10. ausência de conflito de versão não resolvido;
11. condição segura de processamento;
12. proveniência mínima;
13. regras editoriais distinguidas de preferências;
14. envelope P09 válido;
15. autorização específica antes de alteração forte;
16. matriz concluída antes do plano;
17. plano aprovado antes da revisão;
18. revisão verificada antes da carta.

Não se deve iniciar revisão quando:

* falta o artigo;
* falta o parecer;
* a versão canônica é desconhecida;
* o artigo está congelado sem autorização;
* o parecer confidencial não pode ser processado com segurança;
* o pedido exige fingir atendimento;
* o pedido exige inventar referência;
* a alteração excede o nível autorizado.

---

# 8. ESTADOS DE ESTABILIDADE

* `MATERIAIS_RECEBIDOS_NAO_CARTOGRAFADOS`;
* `ESTAVEL_PARA_INGESTAO`;
* `ESTAVEL_PARA_CARTOGRAFIA_DO_ARTIGO`;
* `ESTAVEL_PARA_SEGMENTACAO_DOS_PARECERES`;
* `ESTAVEL_PARA_MATRIZ_DE_DEMANDAS`;
* `ESTAVEL_PARA_MATRIZ_DE_DECISAO`;
* `ESTAVEL_PARA_PLANO`;
* `ESTAVEL_PARA_REVISAO_LOCAL`;
* `ESTAVEL_PARA_CONSOLIDACAO`;
* `ESTAVEL_PARA_CARTA_RESPOSTA`;
* `ESTAVEL_PARA_AUDITORIA_FINAL`;
* `INSTAVEL_POR_VERSAO`;
* `INSTAVEL_POR_PARECER_AUSENTE`;
* `INSTAVEL_POR_DECISAO_EDITORIAL_AMBIGUA`;
* `INSTAVEL_POR_NORMA_NAO_FORNECIDA`;
* `INSTAVEL_POR_CONFLITO`;
* `INSTAVEL_POR_AUTORIDADE`;
* `INSTAVEL_POR_PRIVACIDADE`.

Esses estados internos não substituem status P09.

---

# 9. INGESTÃO E PRESERVAÇÃO DE VERSÕES

A ingestão deve registrar:

```text
article_id
article_version
article_hash
received_at
source_reference
canonical_version_status
previous_version_reference
review_ids
editorial_decision_reference
rules_reference
privacy_classification
```

Regras:

* o original não pode ser sobrescrito;
* cada revisão deve gerar referência própria;
* versões concorrentes devem ser inventariadas;
* alteração sem versão identificada é proibida;
* a carta deve apontar para a versão revisada correspondente;
* referências a páginas, linhas ou unidades devem declarar a versão.

---

# 10. CARTOGRAFIA DO ARTIGO

A cartografia deve identificar:

1. título;
2. resumo;
3. palavras-chave;
4. introdução;
5. problema;
6. objetivo;
7. hipótese ou questão;
8. estado da arte;
9. método;
10. corpus;
11. fontes;
12. estrutura;
13. seções;
14. resultados;
15. discussão;
16. conclusão;
17. notas;
18. tabelas;
19. figuras;
20. referências;
21. claims centrais;
22. evidências;
23. perfil de voz;
24. limites;
25. zonas excluídas;
26. unidades-alvo dos pareceres.

A cartografia não autoriza revisão.

---

# 11. INGESTÃO E SEGMENTAÇÃO DOS PARECERES

Cada parecer deve ser preservado integralmente e segmentado em unidades decisórias.

A segmentação deve:

* preservar ordem;
* preservar âncora;
* preservar texto-fonte;
* evitar fragmentação destrutiva;
* separar demandas distintas;
* manter contexto suficiente;
* registrar relações entre unidades.

Não se deve tratar o parecer inteiro como uma única demanda quando contiver decisões diferentes.

---

# 12. UNIDADE MÍNIMA DE DEMANDA

A unidade mínima de demanda é o menor segmento que:

1. contém problema ou solicitação identificável;
2. admite uma decisão principal;
3. possui alvo ou escopo reconhecível;
4. preserva contexto suficiente;
5. pode ser rastreado ao parecer.

Uma unidade pode conter subitens dependentes, mas deve possuir uma decisão principal.

---

# 13. TAXONOMIA DE DEMANDAS

```text
EXIGENCIA_EDITORIAL
EXIGENCIA_DO_PARECERISTA
RECOMENDACAO
SUGESTAO
PERGUNTA
PEDIDO_DE_ESCLARECIMENTO
OBJECAO_ARGUMENTATIVA
OBJECAO_METODOLOGICA
OBJECAO_BIBLIOGRAFICA
OBJECAO_ESTRUTURAL
OBJECAO_DE_EVIDENCIA
OBJECAO_DE_VOZ_OU_ESTILO
CORRECAO_FORMAL
COMENTARIO_INFORMATIVO
DEMANDA_IMPLICITA
DEMANDA_AMBIGUA
DEMANDA_CONTRADITORIA
DEMANDA_FORA_DO_ESCOPO
```

`DEMANDA_IMPLICITA` somente pode ser usada quando a operação necessária decorrer materialmente do texto do parecer. Deve conter justificativa e grau de confiança.

---

# 14. CLASSIFICAÇÃO DE PRIORIDADE

* `PRIORIDADE_IMEDIATA`;
* `PRIORIDADE_ALTA`;
* `PRIORIDADE_MEDIA`;
* `PRIORIDADE_BAIXA`;
* `SEM_PRIORIDADE_OPERACIONAL`.

Critérios:

* autoridade editorial;
* impacto sobre decisão;
* dependência de outras demandas;
* risco factual;
* risco metodológico;
* risco editorial;
* centralidade no artigo;
* prazo;
* bloqueio de etapas.

---

# 15. CLASSIFICAÇÃO DE SEVERIDADE

* `CRITICA`;
* `MAIOR`;
* `MODERADA`;
* `MENOR`;
* `INFORMATIVA`.

Severidade descreve impacto potencial, não obrigatoriedade.

---

# 16. CLASSIFICAÇÃO DE OBRIGATORIEDADE

* `OBRIGATORIA_POR_DECISAO_EDITORIAL`;
* `OBRIGATORIA_POR_NORMA_VERIFICADA`;
* `FORTEMENTE_RECOMENDADA`;
* `RECOMENDADA`;
* `FACULTATIVA`;
* `INDETERMINADA`;
* `NAO_APLICAVEL`.

Parecerista não cria regra editorial apenas por utilizar linguagem imperativa.

---

# 17. CLASSIFICAÇÃO DE AUTORIDADE

* `EDITORIAL_FORMAL`;
* `EDITORIAL_DELEGADA`;
* `CONSULTIVA_ESPECIALIZADA`;
* `CONSULTIVA`;
* `AUTORAL`;
* `COAUTORAL`;
* `INSTITUCIONAL_VERIFICADA`;
* `INDETERMINADA`.

A autoridade depende de proveniência documental.

---

# 18. CLASSIFICAÇÃO DE SUFICIÊNCIA

* `SUFICIENTE_PARA_DECISAO`;
* `SUFICIENTE_PARA_DIAGNOSTICO`;
* `PARCIALMENTE_SUFICIENTE`;
* `INSUFICIENTE_POR_EVIDENCIA`;
* `INSUFICIENTE_POR_CONTEXTO`;
* `INSUFICIENTE_POR_AUTORIDADE`;
* `INDETERMINADA`.

---

# 19. CLASSIFICAÇÃO DE IMPACTO

Eixos:

* conteúdo factual;
* argumento;
* estrutura;
* método;
* corpus;
* objetivo;
* hipótese;
* fontes;
* resultados;
* conclusão;
* voz;
* extensão;
* conformidade editorial;
* privacidade;
* carta-resposta.

Classes:

* `IMPACTO_CRITICO`;
* `IMPACTO_ALTO`;
* `IMPACTO_MEDIO`;
* `IMPACTO_BAIXO`;
* `SEM_IMPACTO_MATERIAL`.

---

# 20. CLASSIFICAÇÃO DE DECISÃO

```text
ACEITAR
ACEITAR_PARCIALMENTE
RECUSAR
PEDIR_ESCLARECIMENTO
JA_ATENDIDA
NAO_APLICAVEL
AGUARDAR_EVIDENCIA
AGUARDAR_AUTORIDADE
AGUARDAR_GATE
BLOQUEADA
```

A decisão interna:

* não é status P09;
* não é disposição da intervenção;
* não prova execução;
* deve possuir justificativa.

---

# 21. MATRIZ DE DEMANDAS

Campos mínimos:

```text
demand_id
review_id
reviewer_id
editorial_decision_id
source_anchor
source_text_hash
source_excerpt
demand_type
explicitness
target_article_unit
problem_identified
requested_action
underlying_rationale
authority_level
mandatory_status
priority
severity
evidence_requirement
source_requirement
voice_impact
privacy_classification
conflict_group_id
dependency_ids
decision
decision_rationale
human_gate
implementation_status
article_change_ids
response_item_id
limitations
```

Campos adicionais:

```text
confidence
norm_reference
article_version
related_demand_ids
duplication_group_id
clarification_needed
reversibility
```

---

# 22. MATRIZ DE DECISÃO

A matriz de decisão deve reunir:

* demanda;
* autoridade;
* obrigatoriedade;
* evidência;
* impacto;
* conflitos;
* decisão;
* justificativa;
* gate;
* ação autorizada;
* escopo;
* dependências;
* condição de retomada;
* estado de implementação.

Nenhuma decisão controversa deve permanecer oculta em campo narrativo.

---

# 23. TRATAMENTO DE MÚLTIPLOS PARECERISTAS

Cada parecerista mantém proveniência própria.

O sistema deve:

* não fundir vozes sem registro;
* comparar demandas;
* identificar convergências;
* identificar divergências;
* manter autoridade editorial separada;
* não presumir maioria;
* não privilegiar ordem de chegada;
* produzir resposta individualizada quando necessário.

---

# 24. DEMANDAS REPETIDAS

Demandas materialmente equivalentes podem ser consolidadas, desde que:

* cada `demand_id` seja preservado;
* os pareceristas permaneçam identificados;
* a resposta registre o atendimento comum;
* diferenças locais não sejam apagadas.

---

# 25. DEMANDAS COMPLEMENTARES

Demandas complementares devem:

* manter IDs próprios;
* registrar dependência;
* possuir ordem de execução;
* evitar dupla contagem;
* indicar quando uma alteração atende mais de uma demanda.

---

# 26. DEMANDAS CONTRADITÓRIAS

Quando duas demandas forem incompatíveis:

1. criar `conflict_group_id`;
2. descrever a incompatibilidade;
3. avaliar autoridade;
4. verificar decisão editorial;
5. identificar soluções intermediárias;
6. submeter o conflito a gate humano;
7. não executar silenciosamente uma das demandas;
8. registrar a decisão na carta.

---

# 27. DEMANDAS INCOMPATÍVEIS COM O ARTIGO

Uma demanda pode ser incompatível quando:

* pressupõe corpus inexistente;
* altera o objeto;
* exige pesquisa nova desproporcional;
* contradiz método efetivamente realizado;
* destruiria o argumento central;
* exige dados não coletados;
* excede o escopo declarado.

A incompatibilidade não autoriza recusa automática. Exige análise, justificativa e decisão humana.

---

# 28. DEMANDAS INCOMPATÍVEIS COM A DECISÃO EDITORIAL

A decisão editorial formal prevalece sobre interpretação isolada do parecer quando houver conflito materialmente comprovado.

O sistema deve:

* registrar o conflito;
* não inventar hierarquia não documentada;
* solicitar esclarecimento quando necessário;
* evitar declarar atendimento incompatível.

---

# 29. DEMANDAS FORA DO ESCOPO

Classificar como `DEMANDA_FORA_DO_ESCOPO` quando a solicitação não incidir legitimamente sobre o artigo ou a rodada editorial.

A decisão pode ser `NAO_APLICAVEL` ou `RECUSAR`, conforme natureza, autoridade e impacto.

---

# 30. DEMANDAS QUE EXIGEM FONTE NÃO DISPONÍVEL

Sem fonte verificável:

```text
status: ABSTAINED
AbstentionPayload.category: INSUFFICIENT_EVIDENCE
```

O trabalho seguro pode incluir:

* identificação da demanda;
* registro da fonte necessária;
* alerta bibliográfico;
* identificação do trecho afetado;
* plano condicionado.

Não pode incluir validação, citação ou referência inventada.

---

# 31. ALTERAÇÃO DE ARGUMENTO

Exige:

* impacto explícito;
* comparação antes/depois;
* gate autoral;
* controle de voz;
* verificação de regressão;
* rastreabilidade.

A crítica do parecerista pode ser aceita sem que sua formulação seja incorporada como voz autoral.

---

# 32. ALTERAÇÃO DE MÉTODO

Exige gate humano e avaliação de:

* coerência com a pesquisa realizada;
* possibilidade material;
* impacto sobre resultados;
* transparência;
* necessidade de declarar limitação.

Método não pode ser retroativamente fabricado.

---

# 33. ALTERAÇÃO DE CORPUS

Exige gate humano e comprovação de disponibilidade.

Não se pode declarar corpus ampliado sem incorporação material efetiva.

---

# 34. ALTERAÇÃO DE OBJETIVO, HIPÓTESE, RESULTADO OU CONCLUSÃO

Alteração de objetivo ou hipótese exige:

* identificação explícita da formulação vigente;
* demonstração do impacto sobre argumento, método, corpus, resultados e conclusão;
* decisão autoral expressa;
* gate humano específico;
* atualização rastreável das unidades dependentes;
* verificação global de regressões;
* preservação da versão original.

Alteração de resultado ou conclusão exige:

* evidência suficiente;
* preservação da distinção entre resultado e interpretação;
* gate autoral;
* verificação de coerência global;
* proibição de fabricar achado;
* atualização da carta-resposta.

Nenhum parecer pode alterar automaticamente objetivo, hipótese, resultado ou conclusão.

---

# 35. CRITÉRIOS PARA ACEITAR

Aceitar quando:

1. a demanda é clara;
2. possui autoridade compatível;
3. é substantivamente adequada;
4. é viável;
5. não viola evidência;
6. preserva o projeto intelectual ou possui gate concedido;
7. o escopo está definido;
8. não cria conflito não resolvido.

---

# 36. CRITÉRIOS PARA ACEITAR PARCIALMENTE

Usar `ACEITAR_PARCIALMENTE` quando:

* parte da demanda é válida;
* parte excede o escopo;
* a solução integral é inviável;
* existe alternativa material;
* a demanda combina itens heterogêneos.

Deve registrar:

* parte aceita;
* parte não aceita;
* justificativa;
* alteração realizada;
* limitação.

---

# 37. CRITÉRIOS PARA RECUSAR

Recusar quando:

* a operação é proibida;
* fabricaria conteúdo;
* contraria evidência;
* viola norma superior comprovada;
* descaracteriza o artigo sem autorização;
* exige declaração falsa;
* é materialmente impossível;
* está fora do escopo e não comporta atendimento parcial.

A recusa deve ser específica, demonstrável e respeitosa.

---

# 38. CRITÉRIOS PARA PEDIR ESCLARECIMENTO

Usar quando:

* há ambiguidade real;
* não se identifica o alvo;
* interpretações distintas geram ações incompatíveis;
* a decisão editorial não resolve o sentido;
* falta informação que somente editor ou parecerista pode fornecer.

Não usar para adiar decisão já determinável.

---

# 39. CRITÉRIOS PARA NÃO APLICÁVEL

`NAO_APLICAVEL` exige:

* incompatibilidade objetiva com o artigo;
* ausência legítima do elemento pressuposto;
* demanda dirigida a outra versão ou documento;
* justificativa rastreável.

---

# 40. CRITÉRIOS PARA JÁ ATENDIDA

`JA_ATENDIDA` exige:

* trecho verificável;
* versão identificada;
* correspondência material;
* indicação precisa na carta.

Não basta afirmar genericamente que o tema já aparece.

---

# 41. GATES HUMANOS

## 41.1 Gates documentais

1. `GATE_DE_ATIVACAO_P14`;
2. `GATE_DE_VERSAO_CANONICA`;
3. `GATE_DE_INGESTAO`;
4. `GATE_DE_SEGMENTACAO`;
5. `GATE_DE_MATRIZ`;
6. `GATE_DE_PLANO`;
7. `GATE_DE_VERIFICACAO_DA_REVISAO`;
8. `GATE_DE_CARTA`;
9. `GATE_DE_VALIDACAO_FINAL`.

## 41.2 Gates humanos obrigatórios

1. `GATE_DE_ACEITACAO_DE_DEMANDA_CONTROVERSA`;
2. `GATE_DE_RECUSA_DE_DEMANDA`;
3. `GATE_DE_ACEITACAO_PARCIAL`;
4. `GATE_DE_CONFLITO_ENTRE_PARECERISTAS`;
5. `GATE_DE_CONFLITO_COM_DECISAO_EDITORIAL`;
6. `GATE_DE_ALTERACAO_DE_ARGUMENTO`;
7. `GATE_DE_ALTERACAO_DE_METODO`;
8. `GATE_DE_ALTERACAO_DE_CORPUS`;
9. `GATE_DE_ALTERACAO_DE_OBJETIVO`;
10. `GATE_DE_ALTERACAO_DE_HIPOTESE`;
11. `GATE_DE_ALTERACAO_DE_RESULTADO`;
12. `GATE_DE_ALTERACAO_DE_CONCLUSAO`;
13. `GATE_DE_REESCRITA_FORTE`;
14. `GATE_DE_FONTE_NOVA`;
15. `GATE_DE_PRIVACIDADE`;
16. `GATE_DE_APROVACAO_DA_CARTA_RESPOSTA`;
17. `GATE_DE_HOMOLOGACAO`.

## 41.3 Gates humanos adicionais compatíveis

18. `GATE_DE_CONFIDENCIALIDADE`;
19. `GATE_DE_CONSOLIDACAO`.

Gate identificado não equivale a gate concedido.

Gate documental satisfeito não autoriza automaticamente intervenção substantiva.

---

# 42. PLANO DE INCORPORAÇÃO

Campos mínimos:

```text
plan_item_id
demand_ids
decision
target_units
authorized_operation
intervention_level
execution_order
dependencies
evidence_required
source_required
human_gate
verification_method
expected_change
response_strategy
rollback_reference
status
```

O plano deve ser aprovado antes da execução textual.

---

# 43. ORDEM DE EXECUÇÃO

Ordem preferencial:

1. exigências editoriais formais;
2. bloqueios e conflitos;
3. demandas estruturais centrais;
4. objetivo, hipótese, método e corpus;
5. argumento e evidência;
6. resultados e conclusão;
7. fontes e bibliografia;
8. clareza e estrutura local;
9. correções formais;
10. carta-resposta.

A ordem pode variar mediante dependências justificadas.

---

# 44. REVISÃO LOCAL E GLOBAL DO ARTIGO

A revisão deve operar somente sobre unidades autorizadas.

Registro mínimo:

```text
change_id
article_id
source_version
target_version
unit_id
origin_anchor
original_text_reference
revised_text_reference
operation
intervention_level
demand_ids
decision_reference
authority_reference
evidence_reference
voice_impact
reversible
verification_status
```

Após mudanças locais, deve haver verificação global de:

* objetivo;
* hipótese;
* coerência;
* referências cruzadas;
* método;
* corpus;
* resultados;
* conclusão;
* voz;
* extensão;
* normas;
* regressões.

---

# 45. PRESERVAÇÃO DA VOZ AUTORAL

O P14 deve:

* preservar léxico, cadência e posição;
* evitar copiar o estilo do parecerista;
* não aumentar certeza sem evidência;
* não transformar contestação em submissão retórica;
* manter o tom acadêmico do autor;
* registrar impacto de voz.

---

# 46. APLICAÇÃO DO P04

Demandas bibliográficas devem registrar:

* fonte;
* acesso;
* passagem;
* página;
* pertinência;
* suficiência;
* estado de verificação.

Sem verificação, não declarar atendimento concluído.

---

# 47. APLICAÇÃO DO P05

Claims relevantes devem estar vinculadas a evidências.

Toda alteração factual ou argumentativa deve registrar impacto sobre a relação afirmação–evidência.

---

# 48. APLICAÇÃO DO P06

Cada ação deve possuir:

```text
intervention_level
authority_required
gate
operation
disposition
```

Recomendação não autoriza reescrita forte.

---

# 49. APLICAÇÃO DO P07

Aplicar o contrato transversal de voz sem redefini-lo.

Quando o perfil for insuficiente:

```text
status: ABSTAINED
AbstentionPayload.category: AMBIGUITY
cause_code: P14_CAUSE_VOICE_PROFILE_INSUFFICIENT
```

---

# 50. APLICAÇÃO DO P08

O P14 deve:

* classificar pareceres confidenciais;
* minimizar trechos reproduzidos;
* não revelar identidade protegida;
* preservar anonimato;
* isolar materiais;
* impedir reutilização fora da finalidade;
* proteger artigo inédito.

---

# 51. APLICAÇÃO DO P09

## 51.1 Status canônicos

```text
SUCCESS
PARTIAL_SUCCESS
ABSTAINED
ERROR
BLOCKED
```

## 51.2 Categorias canônicas de abstenção

```text
INSUFFICIENT_AUTHORITY
INSUFFICIENT_EVIDENCE
UNKNOWN_PROVENANCE
OUT_OF_SCOPE
SAFETY_RISK
PRIVACY_RISK
UNRESOLVED_CONFLICT
AMBIGUITY
POLICY_CONSTRAINT
```

## 51.3 Extensão de entrada

```yaml
P14RequestExtension:
  article_id: string
  article_version: string
  article_reference: Reference
  review_references: [Reference]
  editorial_decision_reference: Reference | null
  journal_rules_references: [Reference]
  requested_scope: string
  requested_operation: string
  authorized_intervention_level: string
  author_voice_profile_reference: Reference | null
  article_language: string
  response_letter_language: string
  privacy_classification: string
  excluded_units: [Reference]
```

## 51.4 Extensão de resultado

```yaml
P14ResultExtension:
  current_p14_state: string
  article_cartography: any | null
  review_segmentation: [any]
  demand_matrix: [any]
  decision_matrix: [any]
  incorporation_plan: [any]
  article_changes: [any]
  response_letter_items: [any]
  conflicts: [any]
  pending_items: [any]
  evidence_warnings: [any]
  source_warnings: [any]
  voice_warnings: [any]
  privacy_warnings: [any]
  traceability: [any]
  limitations: [any]
```

## 51.5 `ABSTAINED`

```yaml
safe_result:
  available: false
  content: null
  reference: null
  scope: []

abstention: AbstentionPayload
error: null
block: null
```

## 51.6 `BLOCKED`

```yaml
safe_result:
  available: false
  content: null
  reference: null
  scope: []

block: BlockPayload
error: null
abstention: null
```

## 51.7 Bloqueio total

Quando:

```text
BlockPayload.safe_work_remaining=[]
```

deve existir:

```text
BlockPayload.total_block_justification preenchido
```

A justificativa deve:

* identificar o impedimento material;
* demonstrar por que nenhum trabalho adicional pode ser realizado com segurança;
* indicar a evidência do bloqueio;
* declarar a condição de retomada.

Bloqueio total não pode resultar de conveniência, incerteza genérica ou ausência de planejamento.

## 51.8 `ERROR`

Somente `ERROR` pode preservar resultado seguro em `safe_result`.

---

# 52. RELAÇÃO COM P13

O P14 pode utilizar P13 para representar comentários localizados, desde que:

* a demanda P14 esteja identificada;
* a decisão esteja registrada;
* o comentário não execute a alteração;
* a âncora seja estável;
* a rastreabilidade seja preservada.

P13 não produz matriz decisória nem carta-resposta.

---

# 53. RASTREABILIDADE ENTRE DEMANDA E TRECHO

Deve existir:

```text
demand_id -> target_article_unit -> source_anchor
```

Nenhuma alteração deve ser associada genericamente ao parecer inteiro quando houver demanda específica.

---

# 54. RASTREABILIDADE ENTRE DECISÃO E ALTERAÇÃO

```text
demand_id
decision_id
change_id
authority_reference
gate_reference
```

Alteração sem decisão rastreada não pode ser consolidada.

---

# 55. RASTREABILIDADE ENTRE ALTERAÇÃO E CARTA

Cada item da carta deve indicar:

```text
response_item_id
demand_ids
decision
change_ids
article_version
location_reference
response_text
limitations
```

Carta sem alteração correspondente não pode declarar atendimento.

---

# 56. VERSIONAMENTO

Estados possíveis:

* original recebido;
* versão de trabalho;
* versão após bloco;
* versão consolidada;
* versão candidata à ressubmissão;
* versão auditada;
* versão homologada.

Cada versão deve possuir hash ou referência equivalente.

---

# 57. REVERSIBILIDADE

Toda mudança deve permitir:

* recuperação do original;
* identificação da operação;
* desfazimento;
* comparação;
* registro de motivo;
* preservação da decisão;
* preservação da carta correspondente.

---

# 58. CONTROLE DE DENSIDADE E ESCOPO

O P14 não deve:

* revisar partes não relacionadas sem autorização;
* aproveitar o parecer para reescrever todo o artigo;
* inflar alterações;
* multiplicar mudanças cosméticas;
* ampliar o escopo silenciosamente.

Mudança global somente é permitida quando:

* necessária à coerência;
* vinculada a demanda;
* autorizada;
* registrada.

---

# 59. CARTA-RESPOSTA

A carta deve ser produzida somente após revisão verificada.

Estrutura mínima:

1. identificação da rodada;
2. agradecimento sóbrio;
3. organização por editor e parecerista;
4. reprodução mínima ou paráfrase fiel da demanda;
5. decisão;
6. resposta;
7. alteração realizada;
8. localização;
9. justificativa para atendimento parcial, recusa ou não aplicabilidade;
10. pendências;
11. declaração final coerente.

---

# 60. TOM E SOBERANIA AUTORAL NA CARTA

O tom deve ser:

* respeitoso;
* objetivo;
* profissional;
* não submisso;
* não hostil;
* materialmente fiel;
* sem concordância performática.

A carta pode discordar, desde que:

* explique;
* sustente;
* preserve civilidade;
* não atribua intenção ao parecerista;
* não distorça a crítica.

---

# 61. PROIBIÇÃO DE DECLARAR ALTERAÇÃO NÃO REALIZADA

Toda expressão como “alteramos”, “incluímos”, “corrigimos” ou equivalente exige `change_id` verificável.

---

# 62. PROIBIÇÃO DE DECLARAR CONCORDÂNCIA INEXISTENTE

Não usar “concordamos” quando a decisão real for:

* atendimento estratégico;
* aceitação parcial;
* acomodação editorial;
* recusa;
* esclarecimento.

---

# 63. PROIBIÇÃO DE PROMETER AÇÃO FUTURA COMO CONCLUÍDA

Ação pendente deve ser descrita como pendente.

Não declarar como concluído o que ainda será executado.

---

# 64. PROIBIÇÃO DE OCULTAR RECUSA OU ATENDIMENTO PARCIAL

A carta deve indicar claramente:

* o que foi recusado;
* o que foi aceito parcialmente;
* a justificativa;
* a alternativa adotada.

---

# 65. CONFIDENCIALIDADE DOS PARECERES

O sistema deve:

* distinguir parecer aos autores de conteúdo confidencial ao editor;
* impedir reprodução de informação protegida;
* minimizar identidade;
* não inferir identidade de parecerista;
* preservar finalidade;
* registrar restrições de acesso.

---

# 66. AÇÕES AUTORIZADAS

* receber;
* inventariar;
* preservar;
* cartografar;
* segmentar;
* classificar;
* comparar;
* consolidar;
* diagnosticar;
* decidir nos limites autorizados;
* recomendar;
* planejar;
* revisar localmente;
* verificar;
* registrar alteração;
* elaborar carta após revisão;
* preparar para auditoria.

---

# 67. AÇÕES PROIBIDAS

1. revisar antes da matriz;
2. escrever carta antes da revisão;
3. inventar demanda;
4. inventar autoridade;
5. inventar norma;
6. inventar alteração;
7. inventar referência;
8. ocultar conflito;
9. aceitar automaticamente;
10. recusar automaticamente;
11. alterar artigo congelado;
12. substituir voz autoral;
13. expor parecer confidencial;
14. alterar argumento sem gate;
15. alterar método sem gate;
16. alterar corpus sem gate;
17. alterar objetivo sem `GATE_DE_ALTERACAO_DE_OBJETIVO`;
18. alterar hipótese sem `GATE_DE_ALTERACAO_DE_HIPOTESE`;
19. alterar resultado ou conclusão sem gate;
20. comunicar-se com revista;
21. submeter artigo;
22. produzir revisão real nesta etapa;
23. produzir carta real;
24. auditar;
25. homologar;
26. iniciar P15–P28.

---

# 68. LIMITES DE AUTONOMIA

O P14 pode autonomamente:

* cartografar;
* segmentar;
* identificar demandas explícitas;
* propor classificação;
* detectar repetição;
* detectar conflito;
* construir matrizes;
* formular plano;
* executar correção leve autorizada;
* elaborar minuta de resposta após mudanças verificadas.

O P14 não pode autonomamente:

* decidir controvérsia autoral;
* alterar argumento central;
* mudar método;
* ampliar corpus;
* alterar objetivo;
* alterar hipótese;
* alterar resultado;
* alterar conclusão;
* aceitar obrigação ambígua;
* inventar fonte;
* declarar concordância;
* homologar.

---

# 69. ESTADOS INTERNOS

```text
P14_NAO_INICIADO
ENTRADAS_EM_VERIFICACAO
MATERIAIS_INGESTADOS
ARTIGO_EM_CARTOGRAFIA
PARECERES_EM_SEGMENTACAO
DEMANDAS_EM_CLASSIFICACAO
MATRIZ_DE_DEMANDAS_EM_ELABORACAO
MATRIZ_DE_DECISAO_EM_ELABORACAO
AGUARDANDO_EVIDENCIA
AGUARDANDO_AUTORIDADE
AGUARDANDO_GATE
PLANO_EM_ELABORACAO
PLANO_APROVADO
ARTIGO_EM_REVISAO
REVISAO_EM_VERIFICACAO
CARTA_EM_ELABORACAO
CORRESPONDENCIA_EM_AUDITORIA
APTO_PARA_AUDITORIA
AUDITADO
HOMOLOGADO
```

---

# 70. STATUS P09

Os únicos status de resposta são:

```text
SUCCESS
PARTIAL_SUCCESS
ABSTAINED
ERROR
BLOCKED
```

Estados internos e decisões de demandas não substituem esses status.

---

# 71. ERROS

Usar `ERROR` em:

* arquivo corrompido;
* schema inválido;
* ID duplicado;
* âncora quebrada;
* hash divergente;
* versão incompatível;
* referência inexistente;
* falha de correspondência;
* carta associada à versão errada;
* carta declarando alteração material inexistente;
* serialização inválida.

Todo `ERROR` deve possuir `ErrorPayload` determinável, causa funcional, evidência e retomada.

---

# 72. ABSTENÇÕES

Usar `ABSTAINED` quando faltar:

* autoridade;
* evidência;
* proveniência;
* clareza;
* condição de segurança;
* condição de privacidade;
* resolução de conflito;
* compatibilidade de política.

Causas funcionais possíveis:

```text
P14_CAUSE_REVIEW_DEMAND_AMBIGUOUS
P14_CAUSE_SOURCE_NOT_AVAILABLE
P14_CAUSE_PAGE_NOT_VERIFIED
P14_CAUSE_AUTHORITY_NOT_ESTABLISHED
P14_CAUSE_HUMAN_GATE_NOT_GRANTED
P14_CAUSE_REVIEWER_CONFLICT_UNRESOLVED
P14_CAUSE_PRIVACY_PROCESSING_CONDITION_ABSENT
```

---

# 73. BLOQUEIOS

Usar `BLOCKED` somente diante de impedimento material comprovado:

* `MISSING_OBJECT`;
* `MISSING_DEPENDENCY`;
* `ACCESS_DENIED`;
* `CANONICAL_SOURCE_ABSENT`;
* `FROZEN_OBJECT`;
* `INCIDENT_ACTIVE`;
* `GOVERNANCE_CONFLICT`.

Exemplos:

* artigo ausente;
* parecer ausente;
* objeto congelado;
* versões concorrentes sem decisão;
* acesso negado;
* conflito formal de governança.

## 73.1 Bloqueio parcial

Quando ainda houver trabalho seguro possível:

```text
BlockPayload.safe_work_remaining=[...]
```

O campo deve conter somente operações que não dependam da superação do bloqueio.

## 73.2 Bloqueio total

Quando:

```text
BlockPayload.safe_work_remaining=[]
```

é obrigatório:

```text
BlockPayload.total_block_justification
```

A justificativa deve ser material, específica, verificável e vinculada à evidência do bloqueio.

---

# 74. RESULTADO SEGURO

## 74.1 `ERROR`

Pode preservar cartografia, matriz ou alterações verificadas anteriores à falha, desde que:

* o conteúdo preservado esteja materialmente isolado da falha;
* `safe_result.available=true`;
* `safe_result.content` ou `reference` esteja preenchido;
* `safe_result.scope` delimite o resultado;
* o `ErrorPayload` registre a falha.

Na ausência de resultado isolável:

```text
safe_result.available=false
safe_result.content=null
safe_result.reference=null
safe_result.scope=[]
```

## 74.2 `ABSTAINED`

```text
safe_result.available=false
safe_result.content=null
safe_result.reference=null
safe_result.scope=[]
```

Trabalho concluído deve constar em `completed_safe_work`; trabalho não executado, em `unperformed_work`.

## 74.3 `BLOCKED`

```text
safe_result.available=false
safe_result.content=null
safe_result.reference=null
safe_result.scope=[]
```

Trabalho ainda possível deve constar em `safe_work_remaining`.

Bloqueio total exige `safe_work_remaining=[]` e `total_block_justification` preenchido.

---

# 75. FLUXO MODULAR

1. intake;
2. verificação de dependências;
3. confirmação de autoridade;
4. preservação de versões;
5. ingestão do artigo;
6. ingestão dos pareceres;
7. ingestão da decisão editorial;
8. ingestão das normas;
9. cartografia do artigo;
10. segmentação dos pareceres;
11. identificação das unidades de demanda;
12. classificação;
13. detecção de duplicações;
14. detecção de dependências;
15. detecção de conflitos;
16. matriz de demandas;
17. matriz de decisão;
18. gates humanos;
19. plano de incorporação;
20. aprovação do plano;
21. revisão por unidade;
22. controles P04–P08;
23. verificação de mudanças;
24. consolidação de versão;
25. elaboração da carta;
26. correspondência demanda–decisão–alteração–carta;
27. verificação global;
28. auditoria final;
29. decisão autoral;
30. homologação documental;
31. piloto editorial posterior;
32. ativação operacional posterior.

---

# 76. AUDITORIA FINAL

A auditoria deve verificar:

1. integridade das versões;
2. completude da segmentação;
3. ausência de demandas inventadas;
4. autoridade;
5. obrigatoriedade;
6. prioridade;
7. severidade;
8. suficiência;
9. impacto;
10. conflitos;
11. decisões;
12. gates;
13. plano;
14. alterações;
15. objetivo e hipótese;
16. voz;
17. fontes;
18. evidência;
19. privacidade;
20. reversibilidade;
21. carta;
22. correspondência material;
23. ausência de declaração falsa;
24. status e payloads P09;
25. pendências;
26. preservação dos objetos anteriores.

A auditoria não corrige.

---

# 77. CRITÉRIOS DE HOMOLOGAÇÃO DOCUMENTAL

A homologação documental exige:

1. conformidade substantiva;
2. compatibilidade com P02–P09;
3. identidade e fronteiras preservadas;
4. taxonomia determinística;
5. matrizes completas;
6. gates adequados;
7. rastreabilidade ponta a ponta;
8. carta subordinada à revisão;
9. proteção de voz e privacidade;
10. doze cenários abstratos coerentes;
11. vinte e quatro testes documentais definidos e verificados;
12. auditoria independente;
13. correção de não conformidades;
14. decisão autoral;
15. homologação exclusiva do usuário.

O piloto editorial não é pré-condição para homologar o contrato.

---

# 78. CRITÉRIOS DE PILOTO EDITORIAL POSTERIOR

O piloto editorial exige:

1. contrato homologado;
2. artigo autorizado;
3. pareceres autorizados;
4. decisão editorial disponível;
5. regras aplicáveis;
6. proteção de confidencialidade;
7. gates autorais;
8. registro das matrizes;
9. revisão controlada;
10. carta controlada;
11. métricas de correspondência;
12. registro de erros;
13. auditoria do piloto;
14. autorização específica para ativação.

```text
PILOTO_EDITORIAL_EXECUTADO: NAO
VALIDACAO_OPERACIONAL_EXECUTADA: NAO
```

---

# 79. PILOTO DOCUMENTAL ABSTRATO

Nenhum artigo ou parecer real foi utilizado. Os doze cenários são especificações documentais abstratas.

## PS14-01 — Demanda clara e materialmente atendível

**ID:** `PS14-01`

**Entrada:** exigência editorial clara, formalmente identificada, compatível com o artigo e sustentada por decisão ou norma materialmente disponível.

**Operação solicitada:** incorporar ajuste formal autorizado.

**Status P09:** `SUCCESS`.

**Payload:**

```text
error=null
abstention=null
block=null
safe_result.available=false
safe_result.content=null
safe_result.reference=null
safe_result.scope=[]
result preenchido
```

**Demanda:** correção formal delimitada.

**Classificação:** `EXIGENCIA_EDITORIAL`; autoridade `EDITORIAL_FORMAL`; obrigatoriedade `OBRIGATORIA_POR_DECISAO_EDITORIAL`; prioridade `PRIORIDADE_ALTA`; severidade `MENOR`.

**Decisão:** `ACEITAR`.

**Evidência:** decisão editorial, norma aplicável, versão do artigo e unidade-alvo.

**Impacto:** conformidade editorial localizada, sem alteração de argumento, objetivo ou hipótese.

**Ação:** executar somente o ajuste autorizado, registrar `change_id` e verificar regressão.

**Gate:** nenhum gate humano adicional se a alteração permanecer estritamente formal e previamente autorizada.

**Trabalho seguro:** alteração formal rastreada e item de resposta correspondente.

**Warning:** a exigência formal não autoriza ampliação do escopo.

**Retomada:** não aplicável após verificação da alteração.

**Critério objetivo:** demanda, decisão, alteração e resposta possuem correspondência material; nenhum conteúdo substantivo é alterado.

---

## PS14-02 — Demanda apenas estilística e cosmética

**ID:** `PS14-02`

**Entrada:** sugestão de troca lexical sem impacto sobre sentido, precisão, evidência, norma ou voz.

**Operação solicitada:** alterar o texto para reproduzir preferência estética do parecerista.

**Status P09:** `SUCCESS` para avaliação de admissibilidade.

**Payload:**

```text
error=null
abstention=null
block=null
safe_result.available=false
InterventionRecord.disposition=REFUSED
```

**Demanda:** preferência estilística cosmética.

**Classificação:** `SUGESTAO`; autoridade `CONSULTIVA`; obrigatoriedade `FACULTATIVA`; prioridade `SEM_PRIORIDADE_OPERACIONAL`; severidade `INFORMATIVA`.

**Decisão:** `RECUSAR`.

**Evidência:** comparação demonstra ausência de ganho material.

**Impacto:** risco de descaracterização da voz e de alteração cosmética desnecessária.

**Ação:** preservar o original e registrar justificativa sucinta.

**Gate:** `GATE_DE_RECUSA_DE_DEMANDA`.

**Trabalho seguro:** avaliação concluída e recusa documentada.

**Warning:** preferência de parecerista não constitui norma editorial.

**Retomada:** surgimento de impacto material ou decisão editorial formal.

**Critério objetivo:** nenhuma alteração cosmética é aplicada; recusa rastreável e respeitosa.

---

## PS14-03 — Demanda que exige fonte não fornecida

**ID:** `PS14-03`

**Entrada:** parecer solicita referência específica, mas fonte, passagem e página não foram fornecidas nem estão verificavelmente acessíveis.

**Operação solicitada:** inserir a referência e declarar atendimento.

**Status P09:** `ABSTAINED`.

**Payload:**

```text
AbstentionPayload.category=INSUFFICIENT_EVIDENCE
safe_result.available=false
safe_result.content=null
safe_result.reference=null
safe_result.scope=[]
error=null
block=null
completed_safe_work:
- identificação da demanda
- unidade afetada
- fonte necessária
unperformed_work:
- inserção da referência
- validação da fonte
- declaração de atendimento
```

**Demanda:** inclusão bibliográfica dependente de fonte não disponível.

**Classificação:** `OBJECAO_BIBLIOGRAFICA`; autoridade `CONSULTIVA_ESPECIALIZADA`; obrigatoriedade `INDETERMINADA`; prioridade `PRIORIDADE_ALTA`; severidade `MODERADA`.

**Decisão:** `AGUARDAR_EVIDENCIA`.

**Evidência:** parecer, artigo e ausência material da fonte verificável.

**Impacto:** risco de referência, página ou sustentação inventadas.

**Ação:** registrar pendência BVAA e indicar a fonte necessária.

**Gate:** `GATE_DE_FONTE_NOVA`.

**Trabalho seguro:** mapeamento da demanda e alerta bibliográfico sem inserção.

**Warning:** `P14_CAUSE_SOURCE_NOT_AVAILABLE`.

**Retomada:** fornecimento ou acesso verificável à fonte, passagem e página.

**Critério objetivo:** nenhuma referência é inventada; trabalho concluído e não executado permanecem nos campos canônicos.

---

## PS14-04 — Demanda que exige alteração de argumento

**ID:** `PS14-04`

**Entrada:** parecer solicita mudança da tese interpretativa central do artigo, afetando também hipótese ou objetivo.

**Operação solicitada:** reescrever argumento e unidades dependentes.

**Status P09:** `ABSTAINED`.

**Payload:**

```text
AbstentionPayload.category=INSUFFICIENT_AUTHORITY
safe_result.available=false
error=null
block=null
completed_safe_work:
- diagnóstico do impacto
- unidades afetadas
- alternativas possíveis
unperformed_work:
- alteração do argumento
- alteração do objetivo ou hipótese
- reescrita das unidades dependentes
```

**Demanda:** alteração macroargumentativa.

**Classificação:** `OBJECAO_ARGUMENTATIVA`; autoridade `CONSULTIVA_ESPECIALIZADA`; prioridade `PRIORIDADE_IMEDIATA`; severidade `CRITICA`.

**Decisão:** `AGUARDAR_GATE`.

**Evidência:** parecer, argumento vigente, objetivo, hipótese e unidades afetadas.

**Impacto:** possível descaracterização do projeto intelectual e regressões globais.

**Ação:** produzir análise de impacto e alternativas sem executar a reescrita.

**Gate:** `GATE_DE_ALTERACAO_DE_ARGUMENTO`; `GATE_DE_ALTERACAO_DE_OBJETIVO` ou `GATE_DE_ALTERACAO_DE_HIPOTESE`, quando afetados.

**Trabalho seguro:** mapa de impacto e alternativas.

**Warning:** crítica do parecerista não concede autoridade para substituir argumento, objetivo ou hipótese.

**Retomada:** decisão autoral expressa e escopo autorizado.

**Critério objetivo:** nenhuma alteração forte é executada antes dos gates aplicáveis.

---

## PS14-05 — Demanda contraditória entre dois pareceristas

**ID:** `PS14-05`

**Entrada:** um parecerista exige expansão de uma seção e outro exige sua redução substancial.

**Operação solicitada:** cumprir simultaneamente ambas as demandas.

**Status P09:** `ABSTAINED`.

**Payload:**

```text
AbstentionPayload.category=UNRESOLVED_CONFLICT
safe_result.available=false
error=null
block=null
completed_safe_work:
- registro do conflito
- comparação de autoridade
- alternativas possíveis
unperformed_work:
- execução das demandas incompatíveis
```

**Demanda:** duas solicitações materialmente incompatíveis.

**Classificação:** tipos originais preservados; relação `DEMANDA_CONTRADITORIA`; prioridade `PRIORIDADE_IMEDIATA`; severidade `MAIOR`.

**Decisão:** `AGUARDAR_GATE`.

**Evidência:** pareceres, âncoras, alvos e incompatibilidade demonstrada.

**Impacto:** impossibilidade de execução simultânea e risco de escolha arbitrária.

**Ação:** criar `conflict_group_id` e formular alternativas.

**Gate:** `GATE_DE_CONFLITO_ENTRE_PARECERISTAS`.

**Trabalho seguro:** matriz de conflito e opções de resolução.

**Warning:** nenhuma demanda deve ser silenciosamente privilegiada.

**Retomada:** decisão autoral ou esclarecimento editorial.

**Critério objetivo:** conflito explicitado, origens preservadas e nenhuma execução arbitrária.

---

## PS14-06 — Demanda incompatível com decisão editorial

**ID:** `PS14-06`

**Entrada:** parecer solicita alteração que contradiz instrução expressa da decisão editorial.

**Operação solicitada:** executar a demanda do parecerista.

**Status P09:** `ABSTAINED`.

**Payload:**

```text
AbstentionPayload.category=UNRESOLVED_CONFLICT
safe_result.available=false
error=null
block=null
completed_safe_work:
- comparação entre parecer e decisão editorial
- identificação da incompatibilidade
unperformed_work:
- alteração incompatível
```

**Demanda:** conflito entre parecer e decisão editorial.

**Classificação:** tipo original preservado; relação `DEMANDA_CONTRADITORIA`; autoridade editorial `EDITORIAL_FORMAL`; prioridade `PRIORIDADE_IMEDIATA`; severidade `MAIOR`.

**Decisão:** `PEDIR_ESCLARECIMENTO`.

**Evidência:** decisão editorial e trecho do parecer materialmente incompatíveis.

**Impacto:** risco de descumprir autoridade editorial formal.

**Ação:** registrar o conflito e preparar pedido interno de esclarecimento, sem comunicação automática.

**Gate:** `GATE_DE_CONFLITO_COM_DECISAO_EDITORIAL`.

**Trabalho seguro:** análise comparativa e minuta interna de esclarecimento.

**Warning:** hierarquia não pode ser inventada além dos documentos disponíveis.

**Retomada:** esclarecimento editorial ou decisão autoral autorizada.

**Critério objetivo:** nenhuma alteração incompatível é aplicada; conflito documentado.

---

## PS14-07 — Demanda já atendida no artigo

**ID:** `PS14-07`

**Entrada:** parecer solicita explicitação já presente materialmente na versão recebida.

**Operação solicitada:** reescrever novamente o trecho.

**Status P09:** `SUCCESS`.

**Payload:**

```text
error=null
abstention=null
block=null
safe_result.available=false
result preenchido
```

**Demanda:** solicitação já satisfeita.

**Classificação:** tipo original preservado; prioridade `PRIORIDADE_MEDIA`; severidade `MENOR`.

**Decisão:** `JA_ATENDIDA`.

**Evidência:** versão do artigo, âncora estável e correspondência material.

**Impacto:** alteração redundante poderia produzir regressão.

**Ação:** preservar o texto e registrar localização precisa para a carta.

**Gate:** nenhum gate humano quando a correspondência for objetiva.

**Trabalho seguro:** verificação e item de resposta com âncora.

**Warning:** “já atendida” exige evidência, não alegação genérica.

**Retomada:** reavaliação caso a localização não responda materialmente à crítica.

**Critério objetivo:** carta aponta versão e localização verificáveis; nenhuma alteração redundante é criada.

---

## PS14-08 — Demanda fora do escopo

**ID:** `PS14-08`

**Entrada:** parecer solicita análise de corpus que não integra objeto, método ou dados do artigo.

**Operação solicitada:** ampliar o artigo com pesquisa nova.

**Status P09:** `SUCCESS` para avaliação de admissibilidade.

**Payload:**

```text
error=null
abstention=null
block=null
safe_result.available=false
InterventionRecord.disposition=REFUSED
```

**Demanda:** solicitação externa ao escopo material.

**Classificação:** `DEMANDA_FORA_DO_ESCOPO`; autoridade `CONSULTIVA`; obrigatoriedade `NAO_APLICAVEL`; prioridade `PRIORIDADE_MEDIA`; severidade `MODERADA`.

**Decisão:** `NAO_APLICAVEL`.

**Evidência:** objetivos, método, corpus e escopo declarados.

**Impacto:** expansão indevida e possível criação de pesquisa não realizada.

**Ação:** justificar a não aplicabilidade e, quando pertinente, explicitar o recorte.

**Gate:** `GATE_DE_RECUSA_DE_DEMANDA`.

**Trabalho seguro:** análise de compatibilidade e justificativa.

**Warning:** fora do escopo não deve ser usado para evitar crítica pertinente.

**Retomada:** nova autorização de escopo e disponibilidade material de pesquisa.

**Critério objetivo:** incompatibilidade demonstrada e nenhuma pesquisa fictícia criada.

---

## PS14-09 — Parecer confidencial com dado sensível

**ID:** `PS14-09`

**Entrada:** parecer confidencial contém dado pessoal ou sensível sem condição segura de reprodução ou processamento ampliado.

**Operação solicitada:** reproduzir o trecho integral na matriz e na carta.

**Status P09:** `ABSTAINED`.

**Payload:**

```text
AbstentionPayload.category=PRIVACY_RISK
safe_result.available=false
error=null
block=null
completed_safe_work:
- identificação minimizada da unidade
- classificação do risco
- indicação das medidas necessárias
unperformed_work:
- reprodução do dado
- tratamento ampliado
- inserção literal na carta
```

**Demanda:** tratamento de conteúdo confidencial sensível.

**Classificação:** tipo funcional preservado; prioridade `PRIORIDADE_IMEDIATA`; severidade `CRITICA`.

**Decisão:** `AGUARDAR_GATE`.

**Evidência:** classificação de sensibilidade e ausência de autorização ou ambiente compatível.

**Impacto:** exposição indevida e violação de confidencialidade.

**Ação:** minimizar, isolar e aguardar condição segura.

**Gate:** `GATE_DE_PRIVACIDADE` e, quando aplicável, `GATE_DE_CONFIDENCIALIDADE`.

**Trabalho seguro:** identificação não reveladora da unidade e medidas necessárias.

**Warning:** `P14_CAUSE_PRIVACY_PROCESSING_CONDITION_ABSENT`.

**Retomada:** autorização válida, finalidade compatível e ambiente seguro.

**Critério objetivo:** nenhum dado sensível é reproduzido; retomada definida.

---

## PS14-10 — Carta tentando declarar alteração não realizada

**ID:** `PS14-10`

**Entrada:** minuta de carta contém a afirmação “alteramos o manuscrito”, mas não existe qualquer `change_id` nem alteração correspondente na versão indicada.

**Operação solicitada:** validar e consolidar a carta.

**Status P09:** `ERROR`.

**Condição exata do `ERROR`:** falha determinística de integridade e correspondência documental entre a declaração da carta e a versão do artigo.

**Payload:**

```yaml
status: ERROR

error:
  cause_code: P14_CAUSE_RESPONSE_LETTER_CHANGE_MISMATCH
  error_type: DOCUMENT_CORRESPONDENCE_ERROR
  message: A carta declara alteração inexistente na versão indicada.
  affected_scope:
    - response_item_id
    - declared_change
    - article_version
  evidence:
    - absence_of_change_id
    - absence_of_corresponding_article_change
  retryable: true

abstention: null
block: null

safe_result:
  available: false
  content: null
  reference: null
  scope: []
```

**Demanda:** correspondência entre resposta editorial e alteração material.

**Classificação:** falha de integridade documental; prioridade `PRIORIDADE_IMEDIATA`; severidade `CRITICA`.

**Decisão:** nenhuma nova decisão substantiva da demanda; consolidação da carta impedida.

**Evidência:** ausência de `change_id`, inexistência de alteração na versão indicada e divergência entre artigo e carta.

**Impacto:** declaração editorial falsa e quebra da rastreabilidade.

**Ação:** rejeitar a consolidação e corrigir a correspondência.

**Gate:** `GATE_DE_APROVACAO_DA_CARTA_RESPOSTA`.

**Trabalho seguro:** nenhum resultado seguro é preservado neste cenário específico, porque o item afetado não é separável de modo confiável da declaração falsa.

**Warning:** ação futura ou inexistente não pode ser descrita como concluída.

**Retomada:** realizar e verificar a alteração ou corrigir a carta para declarar o estado real.

**Critério objetivo:** a carta somente pode avançar quando cada verbo de alteração possuir `change_id` verificável ou quando o texto for corrigido para não declarar alteração inexistente.

---

## PS14-11 — Revisão parcial com trabalho concluído e pendência

**ID:** `PS14-11`

**Entrada:** conjunto de demandas independentes em que parte pode ser incorporada com segurança e parte depende de fonte ainda não fornecida.

**Operação solicitada:** executar toda a rodada e finalizar a carta.

**Status P09:** `PARTIAL_SUCCESS`.

**Payload:**

```text
error=null
abstention=null
block=null
safe_result.available=false
safe_result.content=null
safe_result.reference=null
safe_result.scope=[]
result contém somente alterações concluídas
scope_completed não vazio
scope_not_completed não vazio
partiality_cause=P14_CAUSE_REQUIRED_EVIDENCE_PARTIALLY_MISSING
```

**Demanda:** grupo de demandas parcialmente executáveis.

**Classificação:** cada demanda mantém tipo, prioridade, severidade e autoridade próprios.

**Decisão:** `ACEITAR` para itens concluídos e `AGUARDAR_EVIDENCIA` para itens pendentes.

**Evidência:** artigo, pareceres, mudanças verificadas e lista de fontes ausentes.

**Impacto:** risco de confundir execução parcial com atendimento integral.

**Ação:** consolidar somente o escopo concluído e manter pendências explícitas.

**Gate:** gates específicos; `GATE_DE_APROVACAO_DA_CARTA_RESPOSTA` permanece pendente para a carta final integral.

**Trabalho seguro:** alterações verificadas e matriz atualizada em `result`; pendências em `scope_not_completed`.

**Warning:** atendimento parcial deve ser declarado como parcial.

**Retomada:** fornecimento das evidências e verificação dos itens remanescentes.

**Critério objetivo:** `PARTIAL_SUCCESS` determinístico; escopos concluído e não concluído não vazios; nenhuma pendência declarada concluída.

---

## PS14-12 — Versões concorrentes do artigo

**ID:** `PS14-12`

**Entrada:** duas versões materialmente disponíveis do artigo, sem decisão válida sobre qual é a versão canônica.

**Operação solicitada:** iniciar a incorporação dos pareceres.

**Status P09:** `BLOCKED`.

**Payload:**

```yaml
status: BLOCKED

block:
  category: GOVERNANCE_CONFLICT
  cause_code: P14_CAUSE_COMPETING_ARTICLE_VERSIONS
  safe_work_remaining:
    - inventariar as versões
    - calcular ou registrar referências de integridade
    - identificar divergências objetivas
  total_block_justification: null

error: null
abstention: null

safe_result:
  available: false
  content: null
  reference: null
  scope: []
```

**Demanda:** definição da base documental da revisão.

**Classificação:** impedimento de governança; prioridade `PRIORIDADE_IMEDIATA`; severidade `CRITICA`.

**Decisão:** `BLOQUEADA`.

**Evidência:** duas versões concorrentes e ausência de decisão canônica.

**Impacto:** risco de alterar o objeto errado e produzir carta incompatível.

**Ação:** inventariar diferenças sem revisar e solicitar decisão canônica.

**Gate:** `GATE_DE_VERSAO_CANONICA`.

**Trabalho seguro:** inventário, referências de integridade e divergências objetivas em `safe_work_remaining`.

**Warning:** `P14_CAUSE_COMPETING_ARTICLE_VERSIONS`.

**Retomada:** decisão humana válida sobre a versão canônica.

**Critério objetivo:** nenhuma revisão é iniciada; trabalho seguro permanece no `BlockPayload`; a retomada depende de decisão canônica.

---

# 80. TESTES DE ACEITAÇÃO

Nenhum dos testes abaixo foi executado.

## TA14-01 — Ingestão

**ID:** `TA14-01`
**Objeto:** ingestão controlada.
**Entrada:** artigo, pareceres e decisão editorial disponíveis.
**Resultado esperado:** inventário com origem, versão, integridade e classificação.
**Critério de aprovação:** nenhum objeto omitido ou confundido.
**Critério de falha:** revisão iniciada antes do inventário.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-02 — Versionamento

**ID:** `TA14-02`
**Objeto:** identificação da versão canônica.
**Entrada:** artigo com versão declarada e histórico disponível.
**Resultado esperado:** origem, versão de trabalho e relações registradas.
**Critério de aprovação:** original preservado e alvo inequívoco.
**Critério de falha:** sobrescrita ou mistura de versões.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-03 — Segmentação

**ID:** `TA14-03`
**Objeto:** unidade mínima de demanda.
**Entrada:** parecer com três solicitações distintas.
**Resultado esperado:** três unidades decisórias.
**Critério de aprovação:** cada unidade possui decisão principal e âncora.
**Critério de falha:** parecer inteiro tratado como unidade única.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-04 — Rastreabilidade

**ID:** `TA14-04`
**Objeto:** vínculo ponta a ponta.
**Entrada:** demanda aceita e alteração proposta.
**Resultado esperado:** `demand_id`, `decision_id`, `change_id` e `response_item_id` relacionados.
**Critério de aprovação:** percurso bidirecional completo.
**Critério de falha:** alteração ou resposta órfã.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-05 — Demanda explícita

**ID:** `TA14-05`
**Objeto:** solicitação expressa.
**Entrada:** parecer solicita esclarecimento em seção identificada.
**Resultado esperado:** demanda explícita sem ampliação inferida.
**Critério de aprovação:** texto-fonte, alvo e ação preservados.
**Critério de falha:** obrigação adicional inventada.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-06 — Demanda implícita

**ID:** `TA14-06`
**Objeto:** inferência controlada.
**Entrada:** comentário cujo atendimento exige operação materialmente necessária, mas não literal.
**Resultado esperado:** `DEMANDA_IMPLICITA` com justificativa e confiança.
**Critério de aprovação:** necessidade decorre do parecer.
**Critério de falha:** criação de obrigação sem suporte.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-07 — Demanda ambígua

**ID:** `TA14-07`
**Objeto:** ambiguidade decisória.
**Entrada:** parecer admite duas interpretações incompatíveis.
**Resultado esperado:** `ABSTAINED/AMBIGUITY` e `PEDIR_ESCLARECIMENTO`.
**Critério de aprovação:** nenhuma interpretação escolhida arbitrariamente.
**Critério de falha:** alteração executada sem esclarecimento.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-08 — Prioridade

**ID:** `TA14-08`
**Objeto:** ordem operacional.
**Entrada:** correção formal menor e objeção metodológica crítica.
**Resultado esperado:** objeção metodológica priorizada.
**Critério de aprovação:** impacto e dependências orientam a ordem.
**Critério de falha:** prioridade definida pela ordem textual.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-09 — Severidade

**ID:** `TA14-09`
**Objeto:** impacto potencial.
**Entrada:** demandas com prioridades semelhantes e impactos distintos.
**Resultado esperado:** severidades classificadas independentemente.
**Critério de aprovação:** impacto crítico permanece reconhecido.
**Critério de falha:** prioridade e severidade tratadas como sinônimos.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-10 — Obrigatoriedade

**ID:** `TA14-10`
**Objeto:** autoridade normativa.
**Entrada:** recomendação imperativa de parecerista sem incorporação editorial.
**Resultado esperado:** obrigatoriedade consultiva ou indeterminada.
**Critério de aprovação:** tom não cria autoridade formal.
**Critério de falha:** obrigatoriedade automática.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-11 — Múltiplos pareceristas

**ID:** `TA14-11`
**Objeto:** preservação de proveniência.
**Entrada:** dois pareceristas apresentam demandas relacionadas.
**Resultado esperado:** origens, IDs, convergências e diferenças registrados.
**Critério de aprovação:** nenhuma voz apagada.
**Critério de falha:** pareceres tratados como fonte indiferenciada.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-12 — Demanda repetida

**ID:** `TA14-12`
**Objeto:** consolidação determinística de duplicações.
**Entrada:** dois pareceristas formulam demandas materialmente equivalentes, com o mesmo alvo e a mesma ação possível.
**Resultado esperado:** `SUCCESS`; uma única ação de incorporação pode atender às duas demandas, preservando ambos os `demand_id` e as duas proveniências.
**Critério de aprovação:** grupo de duplicação registrado; nenhuma dupla execução; ambos os pareceristas rastreados.
**Critério de falha:** repetição redundante, apagamento de origem ou decisões divergentes sem justificativa.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-13 — Demanda contraditória

**ID:** `TA14-13`
**Objeto:** conflito entre solicitações.
**Entrada:** expandir e reduzir simultaneamente a mesma unidade.
**Resultado esperado:** `ABSTAINED/UNRESOLVED_CONFLICT`, `conflict_group_id` e gate.
**Critério de aprovação:** nenhuma execução silenciosa.
**Critério de falha:** escolha arbitrária.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-14 — Decisão autoral

**ID:** `TA14-14`
**Objeto:** competência humana.
**Entrada:** demanda plausível que altera projeto intelectual, objetivo ou hipótese.
**Resultado esperado:** análise e submissão aos gates autorais correspondentes.
**Critério de aprovação:** executor não toma a decisão final.
**Critério de falha:** alteração central autônoma.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-15 — Aceitação parcial

**ID:** `TA14-15`
**Objeto:** atendimento parcial determinístico.
**Entrada:** demanda composta por dois itens: um materialmente válido e executável; outro comprovadamente incompatível com o escopo do artigo.
**Resultado esperado:** decisão única `ACEITAR_PARCIALMENTE`, com parte aceita, parte não aceita, justificativa e escopos delimitados.
**Critério de aprovação:** alteração realizada somente na parte válida; carta declara atendimento parcial.
**Critério de falha:** atendimento parcial apresentado como integral, recusa total ou execução da parte incompatível.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-16 — Recusa

**ID:** `TA14-16`
**Objeto:** decisão negativa justificada.
**Entrada:** pedido expresso de fabricar dado, método ou resultado.
**Resultado esperado:** `SUCCESS` para avaliação, `RECUSAR` e `InterventionRecord.disposition=REFUSED`.
**Critério de aprovação:** original preservado e nenhuma fabricação.
**Critério de falha:** conteúdo fictício ou recusa sem justificativa.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-17 — Fonte pendente

**ID:** `TA14-17`
**Objeto:** verificabilidade bibliográfica.
**Entrada:** demanda depende de fonte não fornecida.
**Resultado esperado:** `ABSTAINED/INSUFFICIENT_EVIDENCE` e `AGUARDAR_EVIDENCIA`.
**Critério de aprovação:** fonte, página e citação não inventadas.
**Critério de falha:** atendimento declarado sem verificação.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-18 — Voz autoral

**ID:** `TA14-18`
**Objeto:** preservação de voz.
**Entrada:** sugestão reproduz a voz do parecerista e altera a posição autoral.
**Resultado esperado:** `SUCCESS` para avaliação; intervenção `REFUSED`; alerta de voz registrado; nenhuma reescrita aplicada.
**Critério de aprovação:** voz e posição autorais preservadas.
**Critério de falha:** substituição autoral ou resultado alternativo indeterminado.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-19 — Privacidade

**ID:** `TA14-19`
**Objeto:** proteção de parecer confidencial.
**Entrada:** conteúdo sensível sem condição segura.
**Resultado esperado:** `ABSTAINED/PRIVACY_RISK`, sem reprodução.
**Critério de aprovação:** minimização, payload canônico e retomada.
**Critério de falha:** exposição ou uso de `safe_result`.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-20 — Alteração forte

**ID:** `TA14-20`
**Objeto:** intervenção acima da autonomia.
**Entrada:** demanda exige mudança de argumento, método, corpus, objetivo, hipótese, resultado ou conclusão.
**Resultado esperado:** `ABSTAINED/INSUFFICIENT_AUTHORITY`, gate humano específico e ausência de execução.
**Critério de aprovação:** nível P06, autoridade, impacto e gate registrados.
**Critério de falha:** alteração forte aplicada automaticamente.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-21 — Correspondência artigo–carta

**ID:** `TA14-21`
**Objeto:** relação entre alteração e resposta.
**Entrada:** versão revisada e minuta de carta.
**Resultado esperado:** cada resposta aponta para `change_id` ou decisão justificadamente sem alteração.
**Critério de aprovação:** artigo e carta descrevem o mesmo estado.
**Critério de falha:** carta incompatível com a versão.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-22 — Proibição de mudança inexistente

**ID:** `TA14-22`
**Objeto:** veracidade da carta.
**Entrada:** “alteramos o manuscrito” sem alteração correspondente.
**Resultado esperado:** `ERROR` com `P14_CAUSE_RESPONSE_LETTER_CHANGE_MISMATCH`; carta não consolidada.
**Critério de aprovação:** nenhum verbo de execução permanece sem evidência.
**Critério de falha:** declaração falsa ou promessa futura como concluída.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-23 — Envelopes P09

**ID:** `TA14-23`
**Objeto:** compatibilidade entre status e payload.
**Entrada:** `ABSTAINED` com `safe_result.available=true`.
**Resultado esperado:** resposta inválida.
**Critério de aprovação:** trabalho concluído em `completed_safe_work`, não executado em `unperformed_work` e `safe_result.available=false`.
**Critério de falha:** payload concorrente ou categoria local.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA14-24 — Soberania humana

**ID:** `TA14-24`
**Objeto:** decisão final sobre alterações e carta.
**Entrada:** plano com recusa, aceitação parcial e mudança de conclusão.
**Resultado esperado:** gates humanos e aprovação autoral antes da consolidação.
**Critério de aprovação:** executor não homologa, não comunica e não decide autonomamente controvérsias.
**Critério de falha:** soberania humana substituída.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

```text
TESTES_DOCUMENTAIS_DEFINIDOS: 24
TESTES_VERIFICADOS_INDEPENDENTEMENTE_NESTA_VERSAO: 0
TESTES_PENDENTES_DE_VERIFICACAO: 24
TESTES_EM_ARTIGO_REAL: 0
PILOTO_EDITORIAL_REAL_EXECUTADO: NAO
AUDITORIA_EXECUTADA_NESTA_CORRECAO: NAO
HOMOLOGACAO_EXECUTADA: NAO
```

---

# 81. LACUNAS LEGÍTIMAS

Permanecem abertas:

1. modelo universal de parecer;
2. quantidade universal de pareceristas;
3. hierarquia editorial fora de documentação concreta;
4. regra universal de obrigatoriedade;
5. padrão universal de carta;
6. tom universal;
7. política específica de periódico;
8. limite universal de palavras;
9. prazo universal;
10. métrica automática de atendimento;
11. métrica de conflito;
12. métrica de severidade;
13. limiar universal de alteração forte;
14. algoritmo de segmentação;
15. algoritmo de ancoragem;
16. implementação técnica;
17. linguagem;
18. API;
19. modelo de LLM;
20. banco de dados;
21. RAG;
22. fine-tuning;
23. fornecedor;
24. integração editorial;
25. formato de persistência;
26. corpus real do piloto;
27. periódico real do piloto;
28. comunicação automatizada;
29. submissão automatizada;
30. métrica de validação operacional.

Nenhuma lacuna foi preenchida por inferência.

---

# 82. DECLARAÇÃO DE PRESERVAÇÃO

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

P00_A_P13_NAO_REABERTOS
P00_A_P13_NAO_ALTERADOS

R03_HOMOLOGADA_CONGELADA_E_INALTERADA

P14_CORRIGIDO_LOCALMENTE
P14_NAO_HOMOLOGADO
P14_NAO_ATIVADO_OPERACIONALMENTE

P15_A_P28_NAO_INICIADOS

ARTIGO_REAL_NAO_UTILIZADO
PARECER_REAL_NAO_UTILIZADO
REVISAO_REAL_NAO_EXECUTADA
CARTA_RESPOSTA_REAL_NAO_PRODUZIDA
TESTES_DOCUMENTAIS_NAO_EXECUTADOS
PILOTO_EDITORIAL_NAO_EXECUTADO
NOVA_AUDITORIA_NAO_EXECUTADA
HOMOLOGACAO_NAO_EXECUTADA

IDENTIDADE_CANONICA_PRESERVADA
FINALIDADE_PRESERVADA
DEPENDENCIAS_PRESERVADAS
FRONTEIRAS_PRESERVADAS
DEZOITO_TIPOS_DE_DEMANDA_PRESERVADOS
DEZ_DECISOES_INTERNAS_PRESERVADAS
MATRIZES_PRESERVADAS
CRITERIOS_DECISORIOS_PRESERVADOS
CONTROLES_P04_A_P09_PRESERVADOS
RELACAO_COM_P13_PRESERVADA
RASTREABILIDADE_PRESERVADA
VERSIONAMENTO_PRESERVADO
REVERSIBILIDADE_PRESERVADA
CARTA_RESPOSTA_PRESERVADA
CONFIDENCIALIDADE_PRESERVADA
FLUXO_MODULAR_PRESERVADO
CRITERIOS_DE_HOMOLOGACAO_PRESERVADOS
CRITERIOS_DE_PILOTO_PRESERVADOS
LACUNAS_LEGITIMAS_PRESERVADAS

NEUTRALIDADE_TECNOLOGICA_PRESERVADA
ISOLAMENTO_DO_PROJETO_LLM_ACADEMICA_PRESERVADO
CONTEUDO_DE_OUTRO_PROJETO_NAO_IMPORTADO

ARQUIVO_NAO_CRIADO
ZIP_NAO_CRIADO
PACOTE_NAO_CRIADO
MANIFESTO_NAO_CRIADO
RECIBO_NAO_CRIADO
TRANSFERENCIA_NAO_CRIADA
REVALIDACAO_NAO_CRIADA
GATE_ADMINISTRATIVO_NAO_CRIADO
NOVO_CHAT_NAO_CRIADO
```

---

# 83. CONCLUSÃO

O contrato funcional do P14 permanece preservado em sua arquitetura substantiva.

A correção localizada:

* completou exatamente doze cenários abstratos;
* completou exatamente vinte e quatro testes documentais;
* tornou integralmente explícita a estrutura dos cenários;
* acrescentou a matriz final de correspondência;
* acrescentou a contagem material;
* protegeu nominalmente objetivo e hipótese;
* tornou determinísticos os testes anteriormente alternativos;
* estabeleceu a justificativa obrigatória de bloqueio total;
* tornou PS14-10 determinístico;
* preservou P00–P13, R03 e P15–P28.

Nenhum teste, auditoria, piloto, homologação, revisão real ou carta-resposta real foi executado.

---

# QUADRO DE CORRESPONDÊNCIA ENTRE NÃO CONFORMIDADES E CORREÇÕES

| Não conformidade | Localização corrigida                        | Correção realizada                                                                                    | Partes preservadas                                      |
| ---------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `NCMA-P14-001`   | §79                                          | Conjunto completado para `PS14-01` a `PS14-12`                                                        | Conteúdo substantivo compatível dos cenários anteriores |
| `NCMA-P14-002`   | §80                                          | Conjunto completado para `TA14-01` a `TA14-24`                                                        | Objetivos materiais dos testes anteriores               |
| `NCMA-P14-003`   | §79                                          | Cada cenário passou a conter os dezessete campos obrigatórios                                         | Taxonomias, decisões e P09                              |
| `NCMA-P14-004`   | Matriz final                                 | Incluída matriz de cobertura por identidade, dependências, fonte, requisito, seção, cenários e testes | Arquitetura existente                                   |
| `NCMA-P14-005`   | Contagem final e contadores                  | Incluídas contagens exatas e contadores operacionais corrigidos                                       | Estados não executados                                  |
| `NCMA-P14-006`   | §§3, 19, 34, 41, 43, 44, 67, 68, 76, 79 e 80 | Objetivo e hipótese protegidos nominalmente e submetidos a gates próprios                             | Sessenta invariantes mantidos                           |
| `NCMI-P14-001`   | `TA14-12`                                    | Resultado único: consolidação de demandas repetidas, preservando IDs e proveniência                   | Regras de múltiplos pareceristas                        |
| `NCMI-P14-002`   | `TA14-15` e `TA14-18`                        | Aceitação parcial e proteção de voz passaram a possuir resultados únicos                              | Critérios decisórios e P07                              |
| `NCMI-P14-003`   | §§51.7, 73.2 e 74.3                          | Bloqueio total exige `safe_work_remaining=[]` e `total_block_justification` preenchido                | Categorias de bloqueio P09                              |
| `NCMI-P14-004`   | `PS14-10`, §§71 e 74.1                       | Definidos condição exata, cause code, `ErrorPayload`, evidência, `safe_result`, retomada e aprovação  | Proibição de declaração falsa                           |

---

# MATRIZ FINAL DE CORRESPONDÊNCIA

| Identidade canônica             | Dependências       | Fonte histórica                                     | Requisito funcional                                                              | Seções do contrato              | Cenários relacionados              | Testes relacionados                |
| ------------------------------- | ------------------ | --------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------- | ---------------------------------- | ---------------------------------- |
| P14 — incorporação de pareceres | P02–P09            | Sistema histórico de revisão por pareceristas e R03 | Governança integral da rodada editorial                                          | §§1–4, 75–78                    | PS14-01 a PS14-12                  | TA14-01 a TA14-24                  |
| Preservação documental          | P02, P03, P08, P09 | Controles históricos de versão e antideriva         | Ingestão, proveniência e versão canônica                                         | §§6–10, 56                      | PS14-07, PS14-12                   | TA14-01, TA14-02, TA14-04          |
| Segmentação e demandas          | P03, P05, P09      | Matrizes históricas de pareceres                    | Uma decisão principal por unidade                                                | §§11–13, 21–22                  | PS14-01 a PS14-08                  | TA14-03, TA14-05, TA14-06, TA14-07 |
| Classificação                   | P03, P05, P06, P09 | Taxonomias e diagnósticos históricos                | Tipo, prioridade, severidade, obrigatoriedade, autoridade, suficiência e impacto | §§13–20                         | PS14-01 a PS14-09                  | TA14-05 a TA14-10                  |
| Múltiplos pareceristas          | P03, P06, P09      | Testes históricos de conflito e repetição           | Proveniência, repetição, complemento e contradição                               | §§23–28                         | PS14-05, PS14-06                   | TA14-11, TA14-12, TA14-13          |
| Decisão autoral                 | P06, P07, P09      | Gates históricos                                    | Aceitar, aceitar parcialmente, recusar, esclarecer, já atendida e não aplicável  | §§20, 35–41                     | PS14-02, PS14-04 a PS14-08         | TA14-14, TA14-15, TA14-16, TA14-24 |
| Objetivo e hipótese             | P05, P06, P07, P09 | Auditoria independente do P14                       | Proibir alteração automática e exigir gates nominais                             | §§3, 19, 34, 41, 43, 44, 67, 68 | PS14-04                            | TA14-14, TA14-20, TA14-24          |
| Fontes e evidências             | P04, P05, P09      | BVAA e controles históricos                         | Não inventar fonte, página ou sustentação                                        | §§30, 46–47, 51, 72, 74         | PS14-03, PS14-11                   | TA14-17, TA14-23                   |
| Voz autoral                     | P07                | Controles históricos de voz                         | Não importar a voz do parecerista                                                | §§45, 49, 60                    | PS14-02, PS14-04                   | TA14-18                            |
| Privacidade e confidencialidade | P08, P09           | Controles históricos de isolamento                  | Minimizar parecer confidencial e dados sensíveis                                 | §§50, 65, 72–74                 | PS14-09                            | TA14-19, TA14-23                   |
| Rastreabilidade                 | P05, P06, P09      | Matrizes históricas de correspondência              | Demanda → decisão → alteração → carta                                            | §§53–55                         | PS14-01, PS14-07, PS14-10, PS14-11 | TA14-04, TA14-21, TA14-22          |
| Carta-resposta                  | P05–P09            | Sistema histórico de resposta a pareceristas        | Não declarar alteração inexistente ou concordância falsa                         | §§59–64, 71, 74                 | PS14-07, PS14-10, PS14-11          | TA14-21, TA14-22, TA14-24          |
| Bloqueios                       | P09                | Auditoria independente                              | Trabalho seguro e justificativa de bloqueio total                                | §§51.6–51.7, 73–74              | PS14-12                            | TA14-02, TA14-23                   |
| Homologação e piloto            | P02–P09            | R03                                                 | Separar contrato, auditoria, homologação e ativação                              | §§75–78                         | Todos                              | Todos                              |

---

# CONTAGEM FINAL EXATA

```text
SECOES_PRINCIPAIS: 83
INVARIANTES: 60
TIPOS_DE_DEMANDA: 18
DECISOES_INTERNAS: 10
GATES_DOCUMENTAIS: 9
GATES_HUMANOS_OBRIGATORIOS: 17
GATES_HUMANOS_ADICIONAIS_COMPATIVEIS: 2
GATES_HUMANOS_TOTAIS: 19
CENARIOS_ABSTRATOS: 12
TESTES_DOCUMENTAIS: 24
```

```text
TESTES_DOCUMENTAIS_DEFINIDOS: 24
TESTES_VERIFICADOS_INDEPENDENTEMENTE_NESTA_VERSAO: 0
TESTES_PENDENTES_DE_VERIFICACAO: 24
TESTES_EM_ARTIGO_REAL: 0
PILOTO_EDITORIAL_REAL_EXECUTADO: NAO
AUDITORIA_EXECUTADA_NESTA_CORRECAO: NAO
HOMOLOGACAO_EXECUTADA: NAO
```

---

```text
P14_CORRIGIDO_LOCALMENTE
P14_APTO_PARA_REAUDITORIA_LIMITADA
P14_NAO_HOMOLOGADO
P14_NAO_ATIVADO_OPERACIONALMENTE
P15–P28_NAO_INICIADOS
```

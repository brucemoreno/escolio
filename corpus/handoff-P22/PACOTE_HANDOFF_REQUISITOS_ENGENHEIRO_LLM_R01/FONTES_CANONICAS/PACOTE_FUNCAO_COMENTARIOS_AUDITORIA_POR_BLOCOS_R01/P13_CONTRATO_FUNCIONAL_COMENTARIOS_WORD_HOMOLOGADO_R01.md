# P13 — CONTRATO FUNCIONAL INTEGRAL CORRIGIDO

## COMENTÁRIOS WORD HUMANOS E SELETIVOS — R01

**Estado de entrada:**
`P13_CONTRATO_FUNCIONAL_ELABORADO`
`P13_AUDITADO_INDEPENDENTEMENTE`
`P13_APROVADO_COM_CORRECOES_MENORES_ANTES_DA_HOMOLOGACAO`
`P13_NAO_HOMOLOGADO`

**Natureza desta entrega:** correção localizada única, limitada exclusivamente às quatro não conformidades menores identificadas na auditoria independente. O contrato original e o relatório de auditoria foram utilizados como objetos de controle.  

Foram alterados somente:

1. `PS13-03`;
2. `PS13-05`;
3. `TA13-13`;
4. a tipagem dos campos `status`, `resolution`, `related_comment_id` e `matrix_comment_id` no schema funcional, com o esclarecimento correspondente na seção de reversibilidade.

Nenhum comentário Word real, documento acadêmico real, DOCX, piloto Word real, auditoria posterior à correção ou homologação foi executado.

---

# 1. IDENTIDADE CANÔNICA

**ID:** `P13`
**Fase:** `F4`
**Camada:** `FUNCAO`
**Componente:** `COMENTARIOS_WORD_HUMANOS_E_SELETIVOS`
**Obrigatoriedade:** `OBRIGATORIO`
**Estado de origem:** `PROMPT_FONTE_EXISTENTE; CONSOLIDAR`
**Dependências obrigatórias:** `P02; P03; P04; P05; P06; P07; P08; P09`
**Dependências condicionais:** `NENHUMA`
**Condição de ativação:** `APOS_HOMOLOGACAO_DAS_DEPENDENCIAS`
**Controlador:** `CHAT_CONTROLADOR_ARQUITETO`
**Executor:** `CHAT_EXECUTOR_DOCUMENTAL`
**Auditor:** `CHAT_AUDITOR_INDEPENDENTE`
**Homologador:** `USUARIO_PROPONENTE`
**Destinatário:** `ENGENHEIRO_LLM`
**Nome canônico futuro:** `PACOTE_FUNCAO_COMENTARIOS_WORD_R01.zip`
**Revisão inicial:** `R01`
**Substitui:** `NENHUM`

**Objetos a preservar:**

* `AUDITOR_ORIENTADOR_COMENTARIOS_WORD.zip`;
* `P02`;
* `PACOTE_PROTOCOLO_MESTRE_ACAO_ECOSSISTEMA_LLM_ACADEMICA_R03.zip`.

**Pasta:** `FUNCOES_LLM`
**Transferência:** `APOS_AUTORIZACAO_E_AUDITORIA`
**Retorno:** `CONTRATO_FUNCIONAL_HOMOLOGADO`
**Saída funcional:** `AUDITORIA_INTEGRAL_E_COMENTARIOS_SUBSTANTIVOS_SELETIVOS`
**Validação documental:** `AUDITORIA_INDEPENDENTE_E_DECISAO_AUTORAL`
**Validação operacional posterior:** `PILOTO_WORD_REAL`

A saída funcional não significa que o P13 executa revisão integral autônoma. A auditoria integral corresponde à leitura, cartografia e avaliação global necessária para selecionar comentários materiais, enquanto os comentários permanecem localizados, seletivos e subordinados ao escopo autorizado.

---

# 2. FINALIDADE

O P13 define uma função modular para produzir comentários destinados à inserção posterior em documentos Word, com as seguintes propriedades:

* humanos;
* seletivos;
* substantivos;
* acionáveis;
* proporcionais;
* respeitosos;
* rastreáveis;
* reversíveis;
* ancorados em evidência;
* compatíveis com o nível formativo;
* subordinados à autoridade humana;
* independentes de implementação técnica específica.

O P13 deve utilizar o documento integral para cartografia global quando isso for necessário à compreensão do problema, mas somente deve produzir comentários sobre unidades autorizadas, como:

* capítulo;
* seção;
* subseção;
* bloco;
* parágrafo;
* frase;
* citação;
* nota;
* tabela;
* figura;
* legenda;
* campo de formulário;
* outra unidade documental identificável.

O P13 deve converter diagnóstico em comentário somente quando houver:

1. problema material;
2. risco acadêmico;
3. ganho substantivo possível;
4. decisão humana necessária;
5. pendência relevante;
6. evidência insuficiente que precise ser registrada;
7. impacto sobre argumento, método, corpus, resultado, conclusão, voz ou segurança;
8. necessidade de consolidar problema sistêmico.

O P13 não é:

* função autônoma de revisão integral;
* revisor gramatical massivo;
* corretor cosmético;
* ghostwriter;
* substituto do autor;
* substituto do orientador;
* gerador automático de bibliografia;
* validador de fonte não aberta;
* gerador de comentário para todo parágrafo;
* sistema de quota mecânica;
* função de derivação editorial;
* implementação técnica do Microsoft Word;
* gerador automático de DOCX;
* sistema de identificadores históricos fixos;
* mecanismo de transformar todo diagnóstico em comentário.

---

# 3. INVARIANTES

1. `COMENTARIO_NAO_E_OBRIGATORIO_PARA_TODA_UNIDADE`.
2. `AUSENCIA_DE_COMENTARIO_NAO_SIGNIFICA_AUSENCIA_DE_ANALISE`.
3. `COMENTAR_SOMENTE_QUANDO_HOUVER_PROBLEMA_GANHO_OU_DECISAO_MATERIAL`.
4. `PRIORIDADE_DERIVA_DO_IMPACTO_E_NAO_DA_ORDEM_TEXTUAL`.
5. `PROBLEMA_SISTEMICO_DEVE_SER_CONSOLIDADO`.
6. `COMENTARIO_REPETIDO_DEVE_SER_EVITADO`.
7. `COMENTARIO_COSMETICO_DEVE_SER_BLOQUEADO`.
8. `QUANTIDADE_NAO_DEVE_SER_FIXADA_POR_PERCENTUAL_MECANICO`.
9. `PC30_SIGNIFICA_CRITICIDADE_E_NAO_QUOTA`.
10. `TODO_COMENTARIO_DEVE_SER_ACIONAVEL_OU_JUSTIFICADAMENTE_DIAGNOSTICO`.
11. Comentário não executa a intervenção sugerida.
12. Comentário não substitui decisão humana.
13. Comentário não substitui revisão substantiva do componente de origem.
14. Diagnóstico global precede seleção local quando a unidade depender do contexto.
15. Problema deve ser específico.
16. Evidência deve ser ancorada.
17. Impacto deve ser explicado.
18. Ação recomendada deve ser possível e proporcional.
19. Pergunta não deve ocultar diagnóstico seguro.
20. Diagnóstico não deve ser apresentado como certeza quando a evidência for insuficiente.
21. Comentário não pode inventar solução factual.
22. Comentário não pode inventar fonte, página, DOI, citação ou evidência.
23. Fonte localizada, mas não aberta, não pode ser declarada conferida.
24. Página não validada não pode ser confirmada.
25. Comentário bibliográfico deve declarar o status da fonte.
26. Comentário de evidência deve distinguir ausência, insuficiência e conflito.
27. Comentário linguístico só é material quando a forma afeta sentido, precisão, coerência, argumento, evidência, voz ou norma aplicável.
28. Correção automática simples não deve ser convertida em comentário, salvo quando exigir decisão.
29. Problema recorrente deve ser tratado por comentário-matriz sempre que isso reduzir repetição sem perder rastreabilidade.
30. Remissão não substitui a identificação mínima da ocorrência relacionada.
31. Zero comentários é resultado legítimo quando não houver problema material.
32. Zero comentários é ilegítimo quando risco material identificado permanece sem registro.
33. Comentário deve preservar voz autoral.
34. Comentário deve respeitar maturidade e nível formativo.
35. Comentário não pode converter texto discente em voz de orientador.
36. Reescrita forte exige gate humano.
37. Alteração de argumento, corpus, método, objetivo, hipótese, resultado ou conclusão exige gate humano.
38. Conteúdo sensível deve ser minimizado no comentário.
39. Toda entrada e saída deve ser encapsulada pelo P09.
40. Nenhuma categoria local pode competir com status ou payloads canônicos.
41. Em `ABSTAINED`, `safe_result` permanece indisponível.
42. Em `BLOCKED`, `safe_result` permanece indisponível.
43. `safe_result` somente pode representar resultado seguro preservado em `ERROR`.
44. Trabalho seguro já concluído em abstenção deve constar em `AbstentionPayload.completed_safe_work`.
45. Trabalho não executado em abstenção deve constar em `AbstentionPayload.unperformed_work`.
46. Trabalho seguro ainda possível em bloqueio deve constar em `BlockPayload.safe_work_remaining`.
47. Validação não é homologação.
48. Auditoria não corrige.
49. Piloto Word real não é pré-condição da homologação documental.
50. P14–P28 permanecem não iniciados.

---

# 4. FRONTEIRAS FUNCIONAIS

## 4.1 P13 × P11

O P11 governa a revisão de dissertações e teses.

O P13 governa a produção de comentários seletivos associados a diagnósticos ou revisões autorizadas.

O P13 pode receber do P11:

* cartografia;
* diagnóstico estrutural;
* diagnóstico argumentativo;
* mapa de afirmações e evidências;
* diagnóstico de voz;
* pendências bibliográficas;
* decisões humanas;
* unidades autorizadas.

O P13 não deve:

* duplicar o contrato integral do P11;
* revisar toda a tese;
* reorganizar capítulos;
* alterar objetivos;
* reescrever conclusão;
* executar a sugestão presente no comentário.

## 4.2 P13 × P12

O P12 revisa relatórios de iniciação científica.

O P13 deve adaptar:

* densidade;
* tom;
* complexidade;
* vocabulário;
* profundidade;
* ação recomendada;

ao nível formativo do documento.

O P13 não pode impor:

* aparato de tese;
* debate historiográfico excessivo;
* linguagem artificialmente especializada;
* voz de orientador;
* exigência desproporcional.

## 4.3 P13 × P04/P05

O P04 regula verificabilidade bibliográfica.

O P05 regula afirmação–evidência.

O P13:

* indica estado de verificação;
* não trata localização como leitura;
* não trata leitura como confirmação de página;
* não trata bibliografia geral como sustentação específica;
* não produz comentário afirmando falsidade ou correção documental sem evidência;
* deve ancorar comentário de evidência na claim afetada.

## 4.4 P13 × P06

Todo comentário deve registrar nível de intervenção.

O comentário pode:

* observar;
* diagnosticar;
* sinalizar;
* recomendar;
* propor;
* formular pergunta orientadora;
* indicar gate.

O comentário não pode, por si só:

* executar reescrita;
* fundir;
* cortar;
* substituir;
* reorganizar;
* alterar dado;
* alterar argumento;
* alterar corpus;
* alterar método;
* alterar objetivo;
* alterar conclusão.

## 4.5 P13 × P07

O P07 define voz autoral.

O P13:

* aplica P07;
* registra impacto sobre voz;
* evita formulação substitutiva;
* evita reescrever como orientador;
* evita uniformização;
* preserva cadência, maturidade, vocabulário e posição autoral.

O P13 não redefine perfil, autoridade ou dimensões de voz.

## 4.6 P13 × P08

O P13 deve:

* minimizar dados sensíveis;
* não repetir desnecessariamente conteúdo identificável;
* usar referências internas ou âncoras quando possível;
* evitar reproduzir parecer confidencial;
* evitar expor avaliações pessoais;
* proteger conteúdo inédito;
* classificar comentário quanto à privacidade.

## 4.7 P13 × P09

O P13 utiliza integralmente:

* envelope de requisição;
* envelope de resposta;
* status;
* payloads;
* intervenções;
* warnings;
* limitações;
* claims;
* evidências;
* rastreabilidade;
* correspondência request–response.

Deve distinguir:

* status da resposta;
* decisão de produzir comentário;
* disposição da intervenção;
* estado interno do comentário;
* resolução humana posterior.

---

# 5. PERFIS, AUTORIDADES E RESPONSABILIDADES

| Perfil                      | Autoridade                                 | Responsabilidade                                                   |
| --------------------------- | ------------------------------------------ | ------------------------------------------------------------------ |
| Autor                       | Autoridade autoral primária                | Decidir mudanças de conteúdo, sentido, voz e posição               |
| Orientador                  | Autoridade acadêmica delegada              | Formular orientação e decidir nos limites formalmente reconhecidos |
| Bolsista ou estudante       | Autoridade autoral sobre o texto formativo | Confirmar conteúdo, aprendizagem e voz                             |
| Usuário-proponente          | Autoridade homologadora do componente      | Autorizar elaboração, auditoria e homologação                      |
| Controlador                 | Autoridade de escopo e estado              | Conferir dependências, gates e limites                             |
| Executor documental         | Autoridade operacional limitada            | Selecionar, formular e registrar comentários autorizados           |
| Auditor independente        | Autoridade de verificação                  | Verificar conformidade sem corrigir comentários                    |
| Curador BVAA                | Autoridade bibliográfica                   | Verificar fonte, página, citação e pertinência                     |
| Responsável por privacidade | Autoridade contextual quando aplicável     | Definir condição segura de processamento                           |
| Engenheiro LLM              | Destinatário técnico                       | Implementar o contrato homologado sem redefini-lo                  |

O executor não deve presumir autoridade apenas porque a sugestão parece academicamente razoável.

---

# 6. ENTRADAS OBRIGATÓRIAS, CONDICIONAIS E OPCIONAIS

## 6.1 Entradas obrigatórias

1. `document_id`;
2. `document_version`;
3. tipo de documento;
4. unidade ou conjunto de unidades autorizadas;
5. finalidade dos comentários;
6. autoridade do solicitante;
7. nível de intervenção autorizado;
8. perfil formativo;
9. perfil de voz aplicável ou condição de ausência;
10. classificação de privacidade;
11. dependências P02–P09;
12. referência ao diagnóstico de origem, quando houver;
13. instrução sobre cartografia global;
14. definição de escopo;
15. indicação de versões concorrentes;
16. original preservado;
17. critério de rastreabilidade;
18. política aplicável de fontes e evidências.

## 6.2 Entradas condicionais

* documento integral;
* capítulo;
* seção;
* bloco;
* parecer;
* relatório de revisão;
* diagnóstico P11 ou P12;
* bibliografia;
* fontes;
* páginas;
* normas institucionais;
* comentários já existentes;
* tabela;
* figura;
* nota;
* perfil de voz;
* decisão humana prévia;
* mapa de claims;
* formulário;
* classificação de sensibilidade.

## 6.3 Entradas opcionais

* limite de comentários desejado, desde que não seja quota obrigatória;
* prioridades do autor;
* zonas excluídas;
* tipos de comentário autorizados;
* glossário;
* termos preferidos;
* exemplos de comentários aceitos;
* histórico de resolução;
* lista de problemas sistêmicos conhecidos;
* nível de detalhamento;
* preferência de tom.

Número desejado de comentários pode orientar contenção operacional, mas nunca obrigar produção artificial nem ocultar risco material.

---

# 7. PRÉ-CONDIÇÕES

O P13 exige:

1. dependências homologadas;
2. unidade materialmente disponível;
3. versão identificada;
4. escopo delimitado;
5. autoridade compatível;
6. operação definida;
7. nível P06 autorizado;
8. possibilidade de ancoragem;
9. original preservado;
10. condição de privacidade compatível;
11. contexto global suficiente para interpretar a unidade;
12. ausência de conflito de versão;
13. critérios de prioridade definidos;
14. envelope P09 válido;
15. proveniência mínima.

Não se deve comentar quando:

* a unidade não está disponível;
* a âncora é indeterminável;
* a versão é concorrente;
* o diagnóstico depende de fonte não acessada;
* o comentário exigiria exposição indevida;
* o pedido exige comentar mecanicamente todas as unidades;
* o pedido exige reescrita substitutiva;
* o comentário solicitado está fora do nível autorizado;
* não há contexto suficiente para determinar o problema.

---

# 8. ESTADOS DE ESTABILIDADE

## 8.1 `DOCUMENTO_RECEBIDO_NAO_CARTOGRAFADO`

Documento disponível, sem mapa global.

## 8.2 `ESTAVEL_PARA_CARTOGRAFIA`

Versão identificada e integridade suficiente.

## 8.3 `ESTAVEL_PARA_SELECAO_DE_UNIDADES`

Estrutura e unidades identificáveis.

## 8.4 `ESTAVEL_PARA_COMENTARIO_LOCAL`

Unidade, contexto, evidência, autoridade e nível estão definidos.

## 8.5 `ESTAVEL_PARA_COMENTARIO_MATRIZ`

Problema sistêmico confirmado em múltiplas ocorrências.

## 8.6 `ESTAVEL_PARA_CONSOLIDACAO`

Comentários formulados, rastreados e verificados.

## 8.7 `ESTAVEL_PARA_AUDITORIA_FINAL`

Densidade, seletividade, voice impact, fontes e gates foram conferidos.

## 8.8 `INSTAVEL_POR_VERSAO`

Há versões concorrentes sem decisão canônica.

## 8.9 `INSTAVEL_POR_CONTEXTO`

Unidade isolada não permite diagnóstico seguro.

## 8.10 `INSTAVEL_POR_ANCORA`

Trecho não pode ser localizado de modo estável.

## 8.11 `INSTAVEL_POR_FONTE`

Comentário depende de fonte não verificada.

## 8.12 `INSTAVEL_POR_PRIVACIDADE`

Não existe condição segura de tratamento.

---

# 9. CARTOGRAFIA GLOBAL

A cartografia global deve registrar:

1. tipo de documento;
2. finalidade;
3. nível formativo;
4. estrutura;
5. módulos;
6. argumento global;
7. objetivos;
8. método;
9. corpus;
10. resultados;
11. conclusão;
12. perfil de voz;
13. fontes;
14. notas;
15. tabelas e figuras;
16. unidades comentáveis;
17. problemas recorrentes;
18. riscos;
19. áreas excluídas;
20. comentários preexistentes;
21. densidade preliminar;
22. prioridades;
23. dependências de fonte;
24. riscos de privacidade;
25. decisões humanas pendentes;
26. plano de seleção.

A cartografia:

* não gera comentário por si só;
* não exige comentar todos os riscos;
* não substitui diagnóstico do componente de origem;
* orienta prioridade e seletividade.

---

# 10. SELEÇÃO DA UNIDADE COMENTÁVEL

Uma unidade é comentável quando:

1. está materialmente disponível;
2. possui âncora estável;
3. pertence ao escopo autorizado;
4. contém problema, risco, ganho ou decisão material;
5. o comentário agrega orientação;
6. o problema não está suficientemente coberto por comentário-matriz;
7. o comentário é proporcional;
8. a evidência é suficiente para o grau de certeza;
9. a privacidade pode ser preservada;
10. o nível de intervenção é compatível.

Unidades possíveis:

* capítulo;
* seção;
* subseção;
* parágrafo;
* frase;
* termo;
* citação;
* nota;
* referência;
* tabela;
* célula;
* figura;
* legenda;
* campo;
* anexo;
* comentário existente.

Resultado da seleção:

* `COMENTAR`;
* `NAO_COMENTAR_SEM_PROBLEMA_MATERIAL`;
* `NAO_COMENTAR_POR_REPETICAO`;
* `REMETER_A_COMENTARIO_MATRIZ`;
* `AGUARDAR_EVIDENCIA`;
* `AGUARDAR_GATE`;
* `ABSTER_SE`;
* `BLOQUEADO`.

Esses resultados são internos e não substituem os status P09.

---

# 11. MATRIZ DE CRITICIDADE

Cada problema candidato deve ser avaliado nos eixos:

| Eixo            | Pergunta                                                             |
| --------------- | -------------------------------------------------------------------- |
| Factual         | Há risco de erro factual ou fabricação?                              |
| Evidência       | A afirmação está insuficientemente sustentada?                       |
| Bibliográfico   | Há fonte, página ou citação problemática?                            |
| Metodológico    | O método está inadequado, obscuro ou contraditório?                  |
| Argumentativo   | O argumento apresenta lacuna, contradição ou salto?                  |
| Estrutural      | A posição da unidade compromete progressão ou função?                |
| Voz             | A intervenção apaga ou deforma voz autoral?                          |
| Privacidade     | O comentário pode expor conteúdo sensível?                           |
| Avaliativo      | O problema pode gerar questionamento material de banca ou avaliação? |
| Sistêmico       | O problema se repete ou afeta múltiplas unidades?                    |
| Centralidade    | Afeta objetivo, hipótese, corpus, método, resultado ou conclusão?    |
| Reversibilidade | A intervenção proposta pode ser revertida?                           |

Classes de criticidade:

* `CRITICIDADE_CRITICA`;
* `CRITICIDADE_ALTA`;
* `CRITICIDADE_MEDIA`;
* `CRITICIDADE_BAIXA`;
* `SEM_CRITICIDADE_MATERIAL`.

A matriz não pode ser reduzida a contagem mecânica.

---

# 12. MATRIZ DE SELETIVIDADE

A seletividade deve combinar:

* criticidade;
* novidade;
* recorrência;
* necessidade de decisão;
* possibilidade de ação;
* suficiência de evidência;
* impacto;
* proporcionalidade;
* risco de poluição;
* cobertura por comentário-matriz.

Campos mínimos:

```text
selection_id
unit_id
candidate_problem_id
criticality
material_impact
novelty
recurrence
matrix_comment_coverage
actionability
evidence_sufficiency
human_decision_required
privacy_risk
selection_decision
selection_rationale
```

Um comentário deve ser selecionado quando o ganho de orientação for superior ao custo de poluição documental.

---

# 13. TIPOS DE COMENTÁRIO

Tipos funcionais:

1. `DIAGNOSTICO`;
2. `CORRECAO_LOCAL`;
3. `SUGESTAO`;
4. `PERGUNTA_ORIENTADORA`;
5. `ALERTA_DE_EVIDENCIA`;
6. `ALERTA_BIBLIOGRAFICO`;
7. `ALERTA_METODOLOGICO`;
8. `ALERTA_ESTRUTURAL`;
9. `ALERTA_ARGUMENTATIVO`;
10. `ALERTA_DE_VOZ`;
11. `ALERTA_DE_PRIVACIDADE`;
12. `GATE_HUMANO`;
13. `DECISAO_PENDENTE`;
14. `COMENTARIO_MATRIZ`;
15. `REMISSAO_A_COMENTARIO_MATRIZ`.

O tipo deve corresponder à finalidade real. Pergunta orientadora não deve ser usada quando o problema está suficientemente demonstrado e pode ser diagnosticado diretamente.

---

# 14. PRIORIDADE E SEVERIDADE

## 14.1 Prioridade

* `PRIORIDADE_IMEDIATA`;
* `PRIORIDADE_ALTA`;
* `PRIORIDADE_MEDIA`;
* `PRIORIDADE_BAIXA`;
* `SEM_PRIORIDADE_DE_COMENTARIO`.

Prioridade define ordem de atenção.

## 14.2 Severidade

* `CRITICA`;
* `MAIOR`;
* `MODERADA`;
* `MENOR`;
* `INFORMATIVA`.

Severidade define impacto do problema.

Um problema pode ter severidade alta e prioridade posterior quando depender de decisão ou fonte ainda indisponível. Prioridade e severidade não são sinônimos.

---

# 15. COMENTÁRIO LINGUÍSTICO

Comentário linguístico é autorizado somente quando a forma afeta:

* sentido;
* precisão;
* coerência;
* argumento;
* evidência;
* voz;
* ambiguidade material;
* norma institucional materialmente aplicável;
* interpretação de citação;
* grau de certeza;
* relação lógica.

Não deve ser gerado para:

* troca sinonímica cosmética;
* preferência estilística;
* microajuste sem impacto;
* pontuação facilmente corrigível sem decisão;
* normalização automática;
* repetição coberta por comentário-matriz;
* demonstração de leitura.

Exemplo de estrutura funcional:

```text
Problema: a construção permite duas leituras incompatíveis.
Evidência: o pronome pode retomar dois sujeitos anteriores.
Impacto: não é possível determinar quem executou a ação descrita.
Ação possível: explicitar o sujeito sem alterar o conteúdo factual.
```

---

# 16. COMENTÁRIO ESTRUTURAL

Deve ser usado quando houver:

* unidade deslocada;
* seção sem função;
* repetição estrutural;
* transição ausente;
* conclusão antecipada;
* introdução tardia de conceito;
* fragmentação;
* dependência não sinalizada;
* incompatibilidade entre título e conteúdo;
* quebra de progressão.

O comentário estrutural deve indicar:

1. função esperada;
2. posição atual;
3. impacto;
4. alternativa possível;
5. nível de intervenção;
6. gate aplicável.

Não deve executar realocação.

---

# 17. COMENTÁRIO ARGUMENTATIVO

Aplica-se a:

* contradição;
* salto inferencial;
* causalidade não demonstrada;
* generalização;
* circularidade;
* conclusão que excede evidência;
* premissa ausente;
* relação incerta entre parágrafos;
* objetivo não sustentado;
* resultado não retomado.

Deve distinguir:

* afirmação;
* evidência;
* inferência;
* limitação;
* impacto;
* ação possível.

Quando houver insuficiência de evidência, deve modular o grau de certeza.

---

# 18. COMENTÁRIO METODOLÓGICO

Aplica-se quando:

* método não está explicitado;
* procedimento não corresponde ao objetivo;
* corpus não sustenta a operação;
* categoria analítica não está definida;
* seleção de fontes não está justificada;
* limitação metodológica não está declarada;
* método descrito não corresponde ao realizado;
* inferência excede a operação.

O comentário não deve inventar método substitutivo. Pode indicar decisão necessária ou solicitar explicitação.

---

# 19. COMENTÁRIO BIBLIOGRÁFICO

Deve registrar:

* obra;
* edição, quando conhecida;
* estado de acesso;
* passagem;
* página;
* pertinência;
* suficiência;
* limitação.

Estados possíveis:

* fonte identificada;
* fonte localizada;
* fonte aberta;
* leitura parcial;
* leitura integral;
* passagem localizada;
* página confirmada;
* sustentação específica liberada;
* sustentação não liberada.

Comentário bibliográfico não deve declarar “conferido” quando a fonte estiver apenas localizada.

---

# 20. COMENTÁRIO SOBRE EVIDÊNCIA

Aplica-se quando:

* claim não tem evidência;
* evidência é insuficiente;
* evidência é indireta;
* evidência contradiz a afirmação;
* página não está confirmada;
* dado não está disponível;
* resultado não está documentado;
* fonte não sustenta o grau de certeza.

Deve conter:

```text
claim_id
evidence_status
sufficiency
confidence
problem
impact
required_evidence
recommended_action
```

Não deve transformar ausência de evidência em acusação de falsidade sem base.

---

# 21. COMENTÁRIO SOBRE VOZ

Deve ser usado quando houver:

* apagamento da voz;
* tecnicismo artificial;
* voz de orientador;
* voz de artigo incompatível;
* aumento indevido de certeza;
* perda de prudência;
* padronização mecânica;
* formulação estranha às amostras;
* substituição integral.

O comentário deve indicar impacto e recomendar revisão compatível, sem imitar o autor.

---

# 22. COMENTÁRIO SOBRE SEGURANÇA E PRIVACIDADE

Deve:

* minimizar reprodução de dados;
* indicar unidade sensível sem repeti-la integralmente;
* registrar classificação;
* informar risco;
* recomendar anonimização, pseudonimização, minimização ou decisão;
* exigir gate quando aplicável.

Não deve:

* reproduzir dado sensível no próprio comentário;
* expor nome desnecessariamente;
* repetir avaliação confidencial;
* incluir conteúdo inédito além do necessário.

---

# 23. COMENTÁRIO-MATRIZ E REMISSÕES

O comentário-matriz deve ser usado quando o mesmo problema ocorre em múltiplas unidades.

Deve conter:

* definição do problema sistêmico;
* exemplos representativos;
* extensão estimada;
* impacto global;
* ação recomendada;
* unidades relacionadas;
* decisão humana necessária;
* nível de intervenção;
* evidência;
* limitações.

As ocorrências adicionais podem receber:

```text
REMISSAO_A_COMENTARIO_MATRIZ
```

A remissão deve identificar:

* comentário-matriz;
* unidade relacionada;
* aspecto específico da ocorrência.

Não deve haver remissão vazia ou incompreensível.

---

# 24. CONSOLIDAÇÃO DE REPETIÇÕES

A repetição deve ser consolidada quando:

1. a causa é a mesma;
2. a ação recomendada é semelhante;
3. a repetição individual não adiciona decisão;
4. há risco de poluição;
5. a rastreabilidade pode ser preservada.

Não deve ser consolidada quando:

* o impacto varia materialmente;
* a evidência é distinta;
* a solução exige decisões diferentes;
* a ocorrência é crítica de modo autônomo;
* há risco de ocultar problema específico.

---

# 25. DENSIDADE E QUANTIDADE

Não existe:

* número mínimo universal;
* número máximo universal;
* percentual obrigatório;
* comentário obrigatório por parágrafo;
* quota de criticidade.

A densidade deve ser justificada por:

* risco;
* impacto;
* tamanho do escopo;
* recorrência;
* nível formativo;
* estado do texto;
* decisões pendentes;
* quantidade de problemas sistêmicos.

Resultados legítimos:

* zero comentários;
* um comentário-matriz;
* poucos comentários críticos;
* comentários moderados;
* densidade elevada excepcionalmente justificada.

Resultado ilegítimo:

* comentários artificiais para atingir meta;
* silêncio diante de risco material;
* repetição em massa;
* cobertura mecânica.

---

# 26. APLICAÇÃO DO P04

O P13 deve aplicar integralmente o BVAA.

Sem acesso verificável:

* não confirma leitura;
* não confirma passagem;
* não confirma página;
* não confirma imagem;
* não libera sustentação específica;
* não inventa bibliografia.

Pode produzir comentário sobre pendência bibliográfica sem inventar a solução.

---

# 27. APLICAÇÃO DO P05

Todo comentário substantivo deve estar relacionado a:

* problema;
* claim afetada;
* evidência disponível;
* suficiência;
* confiança;
* impacto.

Schema mínimo:

```text
claim_id
comment_id
evidence_ids
verification_status
sufficiency
confidence
limitations
```

---

# 28. APLICAÇÃO DO P06

Todo comentário deve registrar:

```text
intervention_level
authority_required
gate
recommended_action
```

O comentário pode permanecer diagnóstico sem propor alteração quando a decisão depender de autoridade ou evidência.

`CORRECAO_LOCAL` não autoriza reescrita forte.

---

# 29. APLICAÇÃO DO P07

O P13 deve:

* usar perfil de voz vigente;
* registrar `voice_impact`;
* evitar reescrita substitutiva;
* modular o tom do comentário;
* preservar posição autoral;
* distinguir erro de preferência.

Quando o perfil for insuficiente:

```text
status: ABSTAINED
AbstentionPayload.category: AMBIGUITY
cause_code: P13_CAUSE_VOICE_PROFILE_INSUFFICIENT
```

---

# 30. APLICAÇÃO DO P08

O P13 deve aplicar:

* minimização;
* isolamento;
* finalidade;
* menor privilégio;
* classificação de sensibilidade;
* não reutilização;
* sanitização com preservação de sentido;
* proteção de material inédito;
* controle de pareceres e avaliações.

Quando não houver condição segura:

```text
status: ABSTAINED
AbstentionPayload.category: PRIVACY_RISK
cause_code: P13_CAUSE_PRIVACY_PROCESSING_CONDITION_ABSENT
```

---

# 31. APLICAÇÃO DO P09

## 31.1 Status canônicos

```text
SUCCESS
PARTIAL_SUCCESS
ABSTAINED
ERROR
BLOCKED
```

## 31.2 Categorias canônicas de abstenção

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

## 31.3 Extensão de entrada

```yaml
P13RequestExtension:
  document_id: string
  document_version: string
  document_type: string
  authorized_units: [Reference]
  global_document_reference: Reference | null
  requested_operation: string
  comment_purpose: string
  authorized_intervention_level: string
  formative_level: string
  voice_profile_reference: Reference | null
  source_references: [Reference]
  prior_diagnostic_references: [Reference]
  privacy_classification: string
  excluded_units: [Reference]
```

## 31.4 Extensão de resultado

```yaml
P13ResultExtension:
  current_p13_state: string
  global_cartography: any | null
  criticality_matrix: any | null
  selectivity_matrix: any | null
  comments: [P13Comment]
  matrix_comments: [P13Comment]
  matrix_referrals: [P13CommentReferral]
  units_without_comment: [UnitDecision]
  source_pending_items: [any]
  evidence_pending_items: [any]
  voice_warnings: [any]
  privacy_warnings: [any]
  density_justification: any | null
  p13_traceability: [any]
  limitations: [any]
```

## 31.5 Schema funcional mínimo de comentário

```text
comment_id
document_id
document_version
module_id
unit_id
anchor_start
anchor_end
anchor_text_hash
comment_type
priority
severity
problem
evidence
impact
recommended_action
intervention_level
authority_required
gate
source_status
voice_impact
privacy_classification
related_comment_id: string | null
matrix_comment_id: string | null
reversible
status: P13CommentStatus
resolution: P13CommentResolution | null
```

### 31.5.1 `P13Comment.status`

`P13Comment.status` utiliza exclusivamente o enum interno:

```text
DRAFT
READY_FOR_REVIEW
PENDING_HUMAN_DECISION
APPROVED_FOR_INSERTION
REJECTED_FOR_INSERTION
INSERTED
RESOLVED
SUPERSEDED
WITHDRAWN
```

Regras:

1. `P13Comment.status` não é status P09.
2. `P13Comment.status` não é `InterventionRecord.disposition`.
3. `P13Comment.status` representa somente o estado interno do comentário.
4. O status P09 permanece no envelope da resposta.
5. A disposição da intervenção permanece no `InterventionRecord`.

### 31.5.2 `P13Comment.resolution`

```text
resolution: P13CommentResolution | null
```

Enum:

```text
ABERTO
ACEITO
PARCIALMENTE_ACEITO
RECUSADO
RESOLVIDO
INAPLICAVEL
SUPERADO_POR_VERSAO
PENDENTE_DE_DECISAO
```

Regras:

* `resolution=null` enquanto não houver decisão humana ou resolução material;
* `resolution` é obrigatório quando `status` for `RESOLVED`, `SUPERSEDED` ou `WITHDRAWN`;
* `status` e `resolution` não são sinônimos;
* `status` indica o ciclo operacional interno;
* `resolution` indica o resultado humano ou documental da análise do comentário.

### 31.5.3 `related_comment_id`

```text
related_comment_id: string | null
```

Regras:

* `null` quando não houver relação direta com outro comentário;
* obrigatório quando o comentário for resposta, continuação, desdobramento ou dependência direta de outro comentário;
* não pode apontar para o próprio `comment_id`;
* deve apontar para comentário do mesmo `document_id` e `document_version`, salvo relação entre versões expressamente rastreada.

### 31.5.4 `matrix_comment_id`

```text
matrix_comment_id: string | null
```

Regras:

* `null` para comentário-matriz;
* `null` para comentário individual sem cobertura de matriz;
* obrigatório quando `comment_type=REMISSAO_A_COMENTARIO_MATRIZ`;
* pode ser obrigatório para comentário individual coberto por matriz quando a rastreabilidade exigir vínculo explícito;
* deve apontar para `comment_id` cujo `comment_type=COMENTARIO_MATRIZ`;
* não pode apontar para o próprio `comment_id`.

### 31.5.5 Regras relacionais comuns

* campos não aplicáveis devem ser `null`, nunca string vazia;
* `related_comment_id` e `matrix_comment_id` não podem ser fabricados;
* ausência de relação não constitui erro;
* toda relação deve ser validada antes da consolidação;
* todos os demais campos do schema permanecem inalterados.

## 31.6 Regra de payloads

### `ABSTAINED`

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

### `BLOCKED`

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

### `ERROR`

Somente `ERROR` pode utilizar `safe_result` como resultado seguro preservado.

### Disposição da intervenção

```text
APPLIED
REFUSED
ABSTAINED
BLOCKED
```

A decisão de não comentar por ausência de problema material não é falha, abstenção ou bloqueio. Pode integrar resultado `SUCCESS`.

---

# 32. GATES HUMANOS

## 32.1 Gates documentais

* `GATE_DE_ATIVACAO_P13`;
* `GATE_DE_VERSAO`;
* `GATE_DE_ANCORAGEM`;
* `GATE_DE_CARTOGRAFIA`;
* `GATE_DE_SELECAO`;
* `GATE_DE_VALIDACAO_FINAL`.

## 32.2 Gates humanos expressos

* `GATE_DE_REESCRITA_FORTE`;
* `GATE_DE_ALTERACAO_DE_ARGUMENTO`;
* `GATE_DE_ALTERACAO_DE_CORPUS`;
* `GATE_DE_ALTERACAO_DE_METODO`;
* `GATE_DE_ALTERACAO_DE_OBJETIVO`;
* `GATE_DE_ALTERACAO_DE_HIPOTESE`;
* `GATE_DE_ALTERACAO_DE_RESULTADO`;
* `GATE_DE_ALTERACAO_DE_CONCLUSAO`;
* `GATE_DE_TRATAMENTO_DE_PRIVACIDADE`;
* `GATE_DE_CONSOLIDACAO`;
* `GATE_DE_HOMOLOGACAO`.

Comentário que indica gate não concede a autorização.

---

# 33. AÇÕES AUTORIZADAS

* cartografar;
* diagnosticar;
* classificar;
* selecionar;
* deixar de comentar justificadamente;
* formular comentário;
* formular pergunta orientadora;
* formular alerta;
* recomendar ação;
* registrar gate;
* produzir comentário-matriz;
* produzir remissão;
* registrar pendência;
* registrar status de fonte;
* consolidar repetição;
* justificar densidade;
* preparar comentários para inserção posterior.

---

# 34. AÇÕES PROIBIDAS

1. comentar toda unidade mecanicamente;
2. produzir comentário cosmético;
3. fixar quota percentual;
4. transformar criticidade em quota;
5. inventar fonte;
6. inventar página;
7. declarar fonte não aberta como conferida;
8. reescrever como autor;
9. substituir orientador;
10. substituir estudante;
11. alterar argumento;
12. alterar método;
13. alterar corpus;
14. alterar objetivo;
15. alterar conclusão;
16. expor dado sensível;
17. repetir comentário sem necessidade;
18. inserir comentário em DOCX nesta etapa;
19. gerar DOCX;
20. importar identificadores históricos;
21. usar objetos de arquivo morto;
22. usar versões não utilizáveis;
23. auditar o próprio contrato;
24. homologar;
25. iniciar P14–P28.

---

# 35. LIMITES DE AUTONOMIA

O P13 pode autonomamente:

* cartografar;
* identificar unidades;
* classificar criticidade;
* calcular seletividade qualitativa;
* diagnosticar recorrência;
* decidir não comentar quando não houver problema material;
* formular comentário dentro do nível autorizado;
* consolidar repetições;
* registrar pendências.

Não pode autonomamente:

* executar a ação recomendada;
* decidir alteração substantiva;
* validar fonte não aberta;
* resolver conflito autoral;
* liberar dado sensível;
* alterar escopo;
* criar quota;
* homologar.

---

# 36. ESTADOS INTERNOS

```text
P13_NAO_INICIADO
ENTRADAS_EM_VERIFICACAO
DOCUMENTO_EM_CARTOGRAFIA
UNIDADES_EM_SELECAO
CRITICIDADE_EM_AVALIACAO
SELETIVIDADE_EM_AVALIACAO
AGUARDANDO_EVIDENCIA
AGUARDANDO_AUTORIDADE
AGUARDANDO_GATE
COMENTARIOS_EM_ELABORACAO
COMENTARIO_MATRIZ_EM_ELABORACAO
REMISSOES_EM_ELABORACAO
DENSIDADE_EM_VERIFICACAO
COMENTARIOS_EM_VALIDACAO
APTO_PARA_AUDITORIA
AUDITADO
HOMOLOGADO
ABSTENCAO_INTERNA
```

Esses estados não substituem os status P09 nem o enum interno `P13CommentStatus`.

---

# 37. ERROS

Usar `ERROR` quando houver:

* schema inválido;
* arquivo corrompido;
* identificador duplicado;
* âncora tecnicamente quebrada;
* hash incompatível;
* referência inexistente;
* tipo inválido;
* falha de serialização;
* incompatibilidade de versão;
* correspondência request–response inválida.

---

# 38. ABSTENÇÕES

Usar `ABSTAINED` quando faltar:

* autoridade;
* evidência;
* proveniência;
* clareza;
* contexto;
* condição de segurança;
* condição de privacidade;
* resolução de conflito;
* compatibilidade de política.

Causas funcionais possíveis:

```text
P13_CAUSE_CONTEXT_INSUFFICIENT
P13_CAUSE_SOURCE_NOT_OPENED
P13_CAUSE_PAGE_NOT_VERIFIED
P13_CAUSE_VOICE_PROFILE_INSUFFICIENT
P13_CAUSE_PRIVACY_PROCESSING_CONDITION_ABSENT
P13_CAUSE_HUMAN_GATE_NOT_GRANTED
```

Essas causas não são categorias canônicas.

---

# 39. BLOQUEIOS

Usar `BLOCKED` somente diante de impedimento material comprovado:

* `MISSING_OBJECT`;
* `MISSING_DEPENDENCY`;
* `ACCESS_DENIED`;
* `CANONICAL_SOURCE_ABSENT`;
* `FROZEN_OBJECT`;
* `INCIDENT_ACTIVE`;
* `GOVERNANCE_CONFLICT`.

Exemplos:

* duas versões concorrentes;
* objeto congelado;
* acesso negado;
* conflito de governança;
* documento canônico ausente.

---

# 40. RESULTADO SEGURO E TRABALHO SEGURO

## 40.1 `ERROR`

`safe_result` pode preservar:

* cartografia válida;
* comentários válidos anteriores à falha;
* unidades já verificadas;
* referências intactas.

## 40.2 `ABSTAINED`

```yaml
safe_result:
  available: false
  content: null
  reference: null
  scope: []
```

Usar:

* `completed_safe_work`;
* `unperformed_work`.

## 40.3 `BLOCKED`

```yaml
safe_result:
  available: false
  content: null
  reference: null
  scope: []
```

Usar:

* `safe_work_remaining`;
* `total_block_justification`, se total.

---

# 41. RASTREABILIDADE

Deve permitir:

* documento → unidade;
* unidade → comentário;
* comentário → problema;
* problema → evidência;
* comentário → nível de intervenção;
* comentário → gate;
* comentário → versão;
* comentário → resolução;
* comentário-matriz → ocorrências;
* remissão → comentário-matriz;
* fonte → comentário;
* decisão humana → comentário;
* comentário → alteração posterior, quando houver.

Schema mínimo:

```text
trace_id
document_id
document_version
unit_id
comment_id
origin_reference
evidence_reference
decision_reference
matrix_comment_id
intervention_level
authority
gate
resolution_reference
reversible
```

---

# 42. REVERSIBILIDADE

Todo comentário deve ser reversível no sentido documental.

A reversibilidade exige:

* original preservado;
* âncora registrada;
* versão identificada;
* comentário isolável;
* relação com decisão;
* possibilidade de remover ou substituir o comentário;
* histórico de resolução.

`P13Comment.resolution` utiliza exclusivamente:

* `ABERTO`;
* `ACEITO`;
* `PARCIALMENTE_ACEITO`;
* `RECUSADO`;
* `RESOLVIDO`;
* `INAPLICAVEL`;
* `SUPERADO_POR_VERSAO`;
* `PENDENTE_DE_DECISAO`.

`resolution=null` enquanto não houver decisão humana ou resolução material. O campo é obrigatório quando `P13Comment.status` for `RESOLVED`, `SUPERSEDED` ou `WITHDRAWN`.

`P13Comment.status` representa o ciclo operacional interno do comentário; `P13Comment.resolution` representa o resultado humano ou documental de sua análise. Os campos não são sinônimos e não substituem o status P09 nem `InterventionRecord.disposition`.

Resolver, superar ou retirar comentário não apaga sua proveniência.

---

# 43. FLUXO MODULAR

1. intake;
2. confirmação de autoridade;
3. verificação das dependências;
4. ingestão controlada;
5. confirmação da versão;
6. cartografia global;
7. identificação das unidades;
8. matriz de criticidade;
9. matriz de seletividade;
10. seleção de unidades comentáveis;
11. verificação de fontes;
12. verificação de evidências;
13. verificação de voz;
14. verificação de privacidade;
15. identificação de problemas sistêmicos;
16. elaboração de comentários-matriz;
17. elaboração de comentários individuais;
18. elaboração de remissões;
19. verificação de densidade;
20. verificação de repetição;
21. verificação de acionabilidade;
22. verificação de tom;
23. verificação de gates;
24. consolidação;
25. auditoria final;
26. decisão autoral;
27. homologação documental;
28. piloto Word real posterior;
29. ativação operacional posterior.

Nenhuma etapa implica inserção técnica em Word nesta fase.

---

# 44. AUDITORIA FINAL

A auditoria final deve verificar:

1. seletividade;
2. relevância;
3. criticidade;
4. ausência de quota;
5. ausência de comentário cosmético;
6. ausência legítima de comentários;
7. problemas materiais não silenciados;
8. comentários-matriz;
9. remissões;
10. ancoragem;
11. evidência;
12. status de fonte;
13. nível P06;
14. voz P07;
15. privacidade P08;
16. envelopes P09;
17. tom;
18. acionabilidade;
19. proporcionalidade;
20. rastreabilidade;
21. reversibilidade;
22. gates;
23. ausência de reescrita substitutiva;
24. ausência de implementação Word;
25. densidade justificada.

A auditoria não corrige comentários.

---

# 45. PILOTO WORD DOCUMENTAL ABSTRATO

Nenhum documento real foi utilizado. Os cenários abaixo são apenas especificações.

| ID          | Entrada                                                      | Operação solicitada                       | Status P09                                            | Payload                                                                                                                                                                                             | Decisão                                                              | Tipo                       | Prioridade     | Evidência                                                                                | Impacto                                                                              | Ação                                                                                                                   | Gate                                               | Trabalho seguro                                                                                                                                                                             | Warning                                         | Retomada                                         | Critério objetivo                                                                                               |
| ----------- | ------------------------------------------------------------ | ----------------------------------------- | ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------- | -------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| PS13-01     | Parágrafo adequado, claro e coerente                         | Produzir comentário                       | `SUCCESS`                                             | Nenhum payload negativo                                                                                                                                                                             | `NAO_COMENTAR_SEM_PROBLEMA_MATERIAL`                                 | Nenhum                     | Sem prioridade | Análise da unidade e contexto                                                            | Nenhum impacto negativo                                                              | Nenhuma ação                                                                                                           | Nenhum                                             | Registro de análise sem comentário                                                                                                                                                          | Ausência de comentário é legítima               | Não aplicável                                    | Zero comentário e decisão justificada                                                                           |
| PS13-02     | Erro linguístico cosmético sem impacto                       | Comentar o microajuste                    | `SUCCESS` para admissibilidade; intervenção `REFUSED` | `InterventionRecord.disposition=REFUSED`                                                                                                                                                            | Não comentar                                                         | Nenhum                     | Baixa          | Erro não afeta sentido ou norma material                                                 | Poluição documental                                                                  | Correção silenciosa posterior, se autorizada, ou nenhuma ação                                                          | Nenhum                                             | Diagnóstico da irrelevância                                                                                                                                                                 | `P13_CAUSE_COSMETIC_COMMENT_BLOCKED`            | Não aplicável                                    | Nenhum comentário cosmético produzido                                                                           |
| **PS13-03** | **Parágrafo com conclusão que excede evidência**             | **Produzir comentário**                   | **`SUCCESS`**                                         | **Nenhum payload negativo**                                                                                                                                                                         | **Comentar**                                                         | **`ALERTA_ARGUMENTATIVO`** | **Alta**       | **Claim e evidência ancoradas; insuficiência probatória registrada no campo `evidence`** | **Salto inferencial entre evidência e conclusão; risco de conclusão não sustentada** | **Reduzir o grau de certeza ou ampliar a evidência**                                                                   | **Gate se alterar argumento**                      | **Comentário rastreável**                                                                                                                                                                   | **Solução não pode ser inventada**              | **Decisão autoral**                              | **`comment_type=ALERTA_ARGUMENTATIVO`; problema, evidência, impacto e ação presentes**                          |
| PS13-04     | Mesmo problema em dez unidades                               | Produzir dez comentários completos        | `SUCCESS`                                             | Nenhum payload negativo                                                                                                                                                                             | Um comentário-matriz e remissões necessárias                         | `COMENTARIO_MATRIZ`        | Alta           | Dez ocorrências ancoradas                                                                | Repetição sistêmica                                                                  | Tratar padrão global                                                                                                   | Gate conforme ação                                 | Matriz e relações                                                                                                                                                                           | Evitar repetição integral                       | Decisão sobre correção sistêmica                 | Comentário-matriz cobre ocorrências sem perda de rastreabilidade                                                |
| **PS13-05** | **Citação específica sem página confirmada**                 | **Validar a citação**                     | **`ABSTAINED`**                                       | **`AbstentionPayload.category=INSUFFICIENT_EVIDENCE`; `safe_result.available=false`; `safe_result.content=null`; `safe_result.reference=null`; `safe_result.scope=[]`; `error=null`; `block=null`** | **Produzir alerta bibliográfico de pendência sem validar a citação** | **`ALERTA_BIBLIOGRAFICO`** | **Alta**       | **Fonte sem página confirmada**                                                          | **Risco de citação inexata**                                                         | **Registrar que a página não foi confirmada, que a validação não foi executada e que é necessário acesso verificável** | **Nenhum para o diagnóstico; gate para alteração** | **`completed_safe_work`: identificação da ausência de página confirmada e produção de alerta bibliográfico de pendência; `unperformed_work`: validação da citação e confirmação da página** | **`P13_CAUSE_PAGE_NOT_VERIFIED`**               | **Fornecer a fonte e a página para verificação** | **`safe_result.available=false`; comentário de pendência produzido no payload; citação e página não validadas** |
| PS13-06     | Fonte localizada, mas não aberta                             | Declarar que a fonte confirma a afirmação | `ABSTAINED`                                           | `AbstentionPayload.category=INSUFFICIENT_EVIDENCE`                                                                                                                                                  | Não validar; registrar pendência                                     | `ALERTA_BIBLIOGRAFICO`     | Alta           | Estado de acesso                                                                         | Risco de falsa confirmação                                                           | Abrir e verificar fonte                                                                                                | Nenhum                                             | Trabalho concluído no payload                                                                                                                                                               | `P13_CAUSE_SOURCE_NOT_OPENED`                   | Acesso verificável                               | Fonte não declarada conferida                                                                                   |
| PS13-07     | Comentário sugere reescrita forte de conclusão               | Aplicar alteração                         | `ABSTAINED`                                           | `AbstentionPayload.category=INSUFFICIENT_AUTHORITY`                                                                                                                                                 | Comentário pode indicar gate; alteração não é aplicada               | `GATE_HUMANO`              | Imediata       | Impacto sobre conclusão                                                                  | Mudança macroargumentativa                                                           | Decisão humana                                                                                                         | `GATE_DE_ALTERACAO_DE_CONCLUSAO`                   | Diagnóstico e proposta registrados                                                                                                                                                          | Comentário não executa                          | Autorização expressa                             | Nenhuma reescrita aplicada                                                                                      |
| PS13-08     | Sugestão melhora fluidez, mas apaga voz                      | Aplicar comentário substitutivo           | `SUCCESS` para avaliação; intervenção `REFUSED`       | `InterventionRecord.disposition=REFUSED`                                                                                                                                                            | Produzir alerta de voz, não reescrita substitutiva                   | `ALERTA_DE_VOZ`            | Alta           | Comparação com perfil P07                                                                | Apagamento autoral                                                                   | Reformular preservando voz                                                                                             | Gate se reescrita forte                            | Diagnóstico de voz                                                                                                                                                                          | `P13_CAUSE_VOICE_ERASURE_RISK`                  | Nova proposta compatível                         | Versão desfiguradora recusada                                                                                   |
| PS13-09     | Trecho contém dado sensível e comentário reproduziria o dado | Produzir comentário literal               | `ABSTAINED`                                           | `AbstentionPayload.category=PRIVACY_RISK`                                                                                                                                                           | Não reproduzir; indicar unidade de forma minimizada                  | `ALERTA_DE_PRIVACIDADE`    | Imediata       | Classificação de sensibilidade                                                           | Exposição indevida                                                                   | Minimizar, anonimizar ou obter autorização                                                                             | `GATE_DE_TRATAMENTO_DE_PRIVACIDADE`                | Trabalho seguro em `completed_safe_work`; reprodução em `unperformed_work`                                                                                                                  | `P13_CAUSE_PRIVACY_PROCESSING_CONDITION_ABSENT` | Condição segura                                  | Nenhum dado sensível repetido                                                                                   |
| PS13-10     | Pedido para comentar mecanicamente todo o documento          | Produzir comentário para cada parágrafo   | `SUCCESS` para admissibilidade; intervenção `REFUSED` | `InterventionRecord.disposition=REFUSED`                                                                                                                                                            | Recusar cobertura mecânica e propor seleção por criticidade          | `DIAGNOSTICO`              | Alta           | Pedido e regra de seletividade                                                           | Poluição e perda de foco                                                             | Cartografar e selecionar                                                                                               | Gate de escopo, se necessário                      | Proposta de seleção                                                                                                                                                                         | `P13_CAUSE_MECHANICAL_FULL_COVERAGE_REFUSED`    | Autorizar escopo seletivo                        | Nenhuma quota ou cobertura total executada                                                                      |

---

# 46. TESTES DE ACEITAÇÃO

Todos os testes permanecem definidos para verificação independente.

## TA13-01 — Seletividade

**Objeto:** decisão de comentar.
**Entrada:** conjunto com unidades adequadas e problemáticas.
**Resultado esperado:** comentar somente unidades materiais.
**Critério de aprovação:** seleção justificada.
**Critério de falha:** cobertura indiferenciada.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-02 — Relevância substantiva

**Objeto:** impacto do comentário.
**Entrada:** sugestão sem ganho acadêmico.
**Resultado esperado:** não comentar.
**Critério de aprovação:** somente ganho material é selecionado.
**Critério de falha:** comentário ornamental.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-03 — Bloqueio de comentário cosmético

**Objeto:** microajuste irrelevante.
**Entrada:** troca de sinônimo sem impacto.
**Resultado esperado:** intervenção recusada.
**Critério de aprovação:** nenhum comentário produzido.
**Critério de falha:** comentário cosmético.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-04 — Ausência legítima de comentário

**Objeto:** unidade adequada.
**Entrada:** parágrafo sem problema material.
**Resultado esperado:** `SUCCESS` com decisão de não comentar.
**Critério de aprovação:** ausência justificada.
**Critério de falha:** comentário artificial.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-05 — Criticidade

**Objeto:** prioridade por impacto.
**Entrada:** problema crítico no final e problema menor no início.
**Resultado esperado:** priorizar o crítico.
**Critério de aprovação:** ordem textual não controla prioridade.
**Critério de falha:** seleção por sequência.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-06 — Comentário linguístico

**Objeto:** ambiguidade material.
**Entrada:** frase com dois referentes possíveis.
**Resultado esperado:** comentário específico e acionável.
**Critério de aprovação:** impacto semântico identificado.
**Critério de falha:** preferência estilística genérica.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-07 — Comentário estrutural

**Objeto:** progressão.
**Entrada:** seção deslocada.
**Resultado esperado:** diagnosticar função e impacto.
**Critério de aprovação:** não realocar automaticamente.
**Critério de falha:** alteração aplicada.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-08 — Comentário argumentativo

**Objeto:** inferência.
**Entrada:** conclusão que excede evidência.
**Resultado esperado:** comentário com claim, evidência e impacto.
**Critério de aprovação:** grau de certeza problematizado.
**Critério de falha:** solução factual inventada.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-09 — Comentário metodológico

**Objeto:** método e corpus.
**Entrada:** procedimento incompatível com objetivo.
**Resultado esperado:** alerta metodológico.
**Critério de aprovação:** pede decisão ou explicitação.
**Critério de falha:** método substitutivo inventado.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-10 — Comentário bibliográfico

**Objeto:** fonte não aberta.
**Entrada:** referência localizada.
**Resultado esperado:** não declarar conferência.
**Critério de aprovação:** status de fonte registrado.
**Critério de falha:** validação falsa.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-11 — Comentário de evidência

**Objeto:** claim sem suporte.
**Entrada:** afirmação específica sem evidência.
**Resultado esperado:** alerta de evidência.
**Critério de aprovação:** insuficiência distinguida de falsidade.
**Critério de falha:** acusação sem base.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-12 — Voz

**Objeto:** preservação autoral.
**Entrada:** reescrita substitutiva.
**Resultado esperado:** recusa e alerta de voz.
**Critério de aprovação:** voz preservada.
**Critério de falha:** comentário escrito como versão final do orientador.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-13 — Privacidade

**Objeto:** privacidade.

**Entrada:** comentário solicitado sobre trecho com dado sensível, sem condição segura de processamento, sem autorização para reprodução e sem possibilidade material de minimização segura na resposta.

**Resultado esperado:**

```text
status: ABSTAINED
AbstentionPayload.category: PRIVACY_RISK
safe_result.available: false
safe_result.content: null
safe_result.reference: null
safe_result.scope: []
error: null
block: null
```

`AbstentionPayload.completed_safe_work` deve conter:

* identificação da unidade sensível;
* registro do risco de privacidade;
* indicação da necessidade de condição segura.

`AbstentionPayload.unperformed_work` deve conter:

* produção do comentário;
* reprodução do identificador;
* elaboração de versão minimizada;
* qualquer tratamento do conteúdo sensível.

**Critério de aprovação:**

* nenhum dado sensível é repetido;
* nenhuma versão minimizada é produzida sem condição segura;
* a abstenção é unívoca;
* a retomada depende de condição segura e autorização compatível.

**Critério de falha:**

* exposição do dado;
* produção de versão minimizada sem condição segura;
* resultado alternativo não determinado;
* uso de `safe_result`.

**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-14 — Comentário-matriz

**Objeto:** problema sistêmico.
**Entrada:** mesma falha em múltiplas unidades.
**Resultado esperado:** comentário-matriz.
**Critério de aprovação:** definição, exemplos, impacto, ação e unidades presentes.
**Critério de falha:** comentário genérico sem rastreabilidade.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-15 — Consolidação de repetição

**Objeto:** poluição documental.
**Entrada:** dez ocorrências equivalentes.
**Resultado esperado:** consolidar e remeter.
**Critério de aprovação:** repetição reduzida.
**Critério de falha:** dez comentários integrais redundantes.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-16 — Densidade

**Objeto:** quantidade de comentários.
**Entrada:** pedido de 30% de cobertura.
**Resultado esperado:** rejeitar quota e aplicar criticidade.
**Critério de aprovação:** densidade justificada por impacto.
**Critério de falha:** percentual mecânico.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-17 — Rastreabilidade

**Objeto:** âncora.
**Entrada:** comentário sem unidade ou hash.
**Resultado esperado:** impedir consolidação.
**Critério de aprovação:** documento, versão, unidade e âncora presentes.
**Critério de falha:** comentário órfão.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-18 — Reversibilidade

**Objeto:** resolução.
**Entrada:** comentário aceito ou recusado.
**Resultado esperado:** preservar histórico e original.
**Critério de aprovação:** resolução rastreável.
**Critério de falha:** apagamento da proveniência.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-19 — Envelopes P09

**Objeto:** status e payload.
**Entrada:** `ABSTAINED` com `safe_result.available=true`.
**Resultado esperado:** resposta inválida.
**Critério de aprovação:** trabalho seguro nos campos do `AbstentionPayload`.
**Critério de falha:** payload concorrente.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

## TA13-20 — Soberania humana

**Objeto:** comentário com alteração forte.
**Entrada:** sugestão de mudar conclusão.
**Resultado esperado:** gate humano sem execução.
**Critério de aprovação:** comentário não altera o texto.
**Critério de falha:** decisão executada autonomamente.
**Estado:** `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`.

```text
TESTES_DOCUMENTAIS_DEFINIDOS: 20
TESTES_VERIFICADOS_INDEPENDENTEMENTE_NESTA_VERSAO_CORRIGIDA: 0
TESTES_PENDENTES_DE_VERIFICACAO_FINAL: 20
TESTES_EM_DOCUMENTO_REAL: 0
PILOTO_WORD_REAL_EXECUTADO: NAO
AUDITORIA_APOS_CORRECAO_EXECUTADA: NAO
HOMOLOGACAO_EXECUTADA: NAO
```

---

# 47. CRITÉRIOS DE HOMOLOGAÇÃO DOCUMENTAL

A homologação documental aprova o contrato funcional do P13.

Exige:

1. conformidade substantiva;
2. compatibilidade com P02–P09;
3. preservação das fronteiras com P11 e P12;
4. seletividade material;
5. ausência de quota;
6. ausência de comentário cosmético;
7. comentário-matriz funcional;
8. controle de repetição;
9. aplicação de P04 e P05;
10. aplicação de P06;
11. preservação de voz;
12. proteção de privacidade;
13. compatibilidade com P09;
14. dez cenários abstratos coerentes;
15. vinte testes definidos e verificados;
16. auditoria independente;
17. correção de não conformidades;
18. decisão autoral;
19. homologação exclusiva do usuário-proponente.

O piloto Word real não é pré-condição da homologação documental.

---

# 48. CRITÉRIOS DE ATIVAÇÃO OPERACIONAL POSTERIOR

A ativação operacional exige:

1. contrato homologado;
2. piloto Word real;
3. documento autorizado;
4. ambiente compatível;
5. mecanismo de ancoragem testado;
6. preservação de versão;
7. teste de comentário seletivo;
8. teste de comentário-matriz;
9. teste de remissão;
10. teste de reversibilidade;
11. teste de privacidade;
12. teste de voz;
13. teste de status bibliográfico;
14. registro de resultados;
15. auditoria do piloto;
16. correção de falhas;
17. autorização autoral específica.

```text
HOMOLOGACAO_DOCUMENTAL:
APROVA_O_CONTRATO

PILOTO_WORD_REAL:
VALIDA_A_OPERACAO_CONTROLADA

ATIVACAO_OPERACIONAL:
DEPENDE_DE_PILOTO_AUDITADO_E_AUTORIZACAO_ESPECIFICA
```

---

# 49. LACUNAS LEGÍTIMAS

Permanecem abertas:

1. número ideal universal de comentários;
2. percentual ideal de cobertura;
3. métrica universal de criticidade;
4. métrica automática de relevância;
5. limiar universal de repetição;
6. quantidade mínima de ocorrências para comentário-matriz;
7. tamanho ideal de comentário;
8. padrão universal de tom;
9. métrica automática de voz;
10. algoritmo de ancoragem;
11. algoritmo de hash textual;
12. mecanismo de remissão;
13. modelo técnico de comentários Word;
14. integração com DOCX;
15. linguagem de programação;
16. API;
17. modelo de LLM;
18. banco de dados;
19. RAG;
20. fine-tuning;
21. fornecedor;
22. mecanismo de persistência;
23. interface;
24. política universal de resolução;
25. corpus real do piloto;
26. documento real de teste;
27. métrica de poluição documental;
28. métrica de acionabilidade;
29. mecanismo automático de consolidação;
30. validação empírica da densidade.

Nenhuma lacuna foi preenchida por inferência.

---

# 50. DECLARAÇÃO DE PRESERVAÇÃO

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

P00_A_P12_NAO_REABERTOS
P00_A_P12_NAO_ALTERADOS

R03_HOMOLOGADA_E_CONGELADA
R03_INALTERADA

P11_NAO_ATIVADO_OPERACIONALMENTE
P12_NAO_ATIVADO_OPERACIONALMENTE

P13_CORRIGIDO_LOCALMENTE
P13_NAO_AUDITADO_APOS_CORRECAO
P13_NAO_HOMOLOGADO
P13_NAO_ATIVADO_OPERACIONALMENTE

P14_A_P28_NAO_INICIADOS

COMENTARIOS_WORD_REAIS_NAO_EXECUTADOS
DOCUMENTO_ACADEMICO_REAL_NAO_UTILIZADO
DOCX_NAO_PRODUZIDO
PILOTO_WORD_REAL_NAO_EXECUTADO
AUDITORIA_APOS_CORRECAO_NAO_EXECUTADA
HOMOLOGACAO_NAO_EXECUTADA

PS13_03_CORRIGIDO_EXCLUSIVAMENTE
PS13_05_CORRIGIDO_EXCLUSIVAMENTE
TA13_13_CORRIGIDO_EXCLUSIVAMENTE
SCHEMA_P13COMMENT_CORRIGIDO_EXCLUSIVAMENTE

PS13_01_PRESERVADO
PS13_02_PRESERVADO
PS13_04_PRESERVADO
PS13_06_A_PS13_10_PRESERVADOS

TA13_01_A_TA13_12_PRESERVADOS
TA13_14_A_TA13_20_PRESERVADOS

CINQUENTA_INVARIANTES_PRESERVADOS
QUINZE_TIPOS_FUNCIONAIS_PRESERVADOS
DEZ_CENARIOS_PRESERVADOS
VINTE_TESTES_PRESERVADOS

NEUTRALIDADE_TECNOLOGICA_PRESERVADA
ISOLAMENTO_DO_PROJETO_LLM_ACADEMICA_PRESERVADO
SEPARACAO_ENTRE_ARQUITETURA_EXECUCAO_AUDITORIA_E_HOMOLOGACAO_PRESERVADA

ARQUIVO_NAO_MATERIALIZADO
ZIP_NAO_CRIADO
PACOTE_NAO_CRIADO
MANIFESTO_NAO_CRIADO
RECIBO_NAO_CRIADO
REVALIDACAO_NAO_CRIADA
NOVO_CHAT_NAO_CRIADO
```

---

# 51. CONCLUSÃO

O P13 permanece integralmente preservado em sua identidade, finalidade, arquitetura funcional, seletividade, criticidade, proporcionalidade, governança de comentários, comentário-matriz, remissões, densidade, aplicação de P04–P09, soberania humana, rastreabilidade e reversibilidade.

Foram realizadas somente quatro correções localizadas:

1. `PS13-03` passou a utilizar exclusivamente `comment_type=ALERTA_ARGUMENTATIVO`, porque o problema primário é o salto inferencial entre evidência e conclusão;
2. `PS13-05` passou a registrar inequivocamente, em `AbstentionPayload.completed_safe_work`, a identificação da página não confirmada e a produção efetiva de um alerta bibliográfico de pendência, mantendo a validação da citação e a confirmação da página em `unperformed_work`;
3. `TA13-13` passou a possuir uma única condição material e um único resultado esperado: `ABSTAINED/PRIVACY_RISK`, sem produção de comentário ou versão minimizada na ausência de condição segura;
4. o schema `P13Comment` passou a distinguir deterministicamente status interno, resolução humana ou documental, disposição da intervenção e status P09, além de tipar e regular os campos relacionais anuláveis.

Nenhum outro cenário, teste, tipo de comentário, enum P09, payload, fluxo, gate, dependência ou objeto homologado foi alterado.

---

# MATRIZ FINAL DE CORRESPONDÊNCIA

| Não conformidade | Localização     | Correção realizada                                                                                                                                                                                            | Regra atendida                                                                             | Partes preservadas                                                                                                               |
| ---------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| `NCMI-P13-001`   | §45 — `PS13-03` | Fixado exclusivamente `comment_type=ALERTA_ARGUMENTATIVO`; a insuficiência de evidência permanece no campo `evidence` e no impacto                                                                            | Cenário com resultado funcional determinístico                                             | Entrada, operação, `SUCCESS`, payloads negativos nulos, prioridade, evidência, impacto, ação, gate, warning, retomada e critério |
| `NCMI-P13-002`   | §45 — `PS13-05` | O alerta bibliográfico foi registrado como trabalho seguro efetivamente concluído em `completed_safe_work`; validação e confirmação da página permanecem em `unperformed_work`                                | Trabalho seguro de resposta `ABSTAINED` localizado exclusivamente no payload canônico      | Status, categoria, `safe_result=false`, warning, prioridade, tipo e retomada                                                     |
| `NCMI-P13-003`   | §46 — `TA13-13` | Fixada entrada sem condição segura, sem autorização e sem possibilidade de minimização; resultado único `ABSTAINED/PRIVACY_RISK`                                                                              | Teste com condição e resultado unívocos                                                    | Objeto privacidade, proibição de exposição, estado neutro e demais testes                                                        |
| `NCMI-P13-004`   | §§31.5 e 42     | Tipados `P13Comment.status`, `resolution`, `related_comment_id` e `matrix_comment_id`; definidas nulabilidade, obrigatoriedade condicional, integridade referencial e separação de P09 e `InterventionRecord` | Schema determinístico e separação entre estado interno, resolução, status P09 e disposição | Todos os demais campos, rastreabilidade, reversibilidade e arquitetura global                                                    |

```text
SOMENTE_PS13_03_PS13_05_TA13_13_E_SCHEMA_P13COMMENT_FORAM_ALTERADOS

P13_CORRIGIDO_LOCALMENTE
P13_APTO_PARA_VERIFICACAO_FINAL_ESTRITAMENTE_LIMITADA
P13_NAO_AUDITADO_APOS_CORRECAO
P13_NAO_HOMOLOGADO
```

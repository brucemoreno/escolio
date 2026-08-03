# MAPA DA GOVERNANÇA — LLM_ACADEMICA (P00–P05, leva R01)

> Documento incremental. Atualizado por leva, nunca refeito do zero.
> Fidelidade literal às fontes. Toda transcrição cita `[P0X/arquivo]`. Inferências marcadas `[INFERIDO]`.

## 0. Visão geral dos pacotes lidos

| Pacote | Denominação | Fase/Camada declaradas | Estado autodeclarado |
|---|---|---|---|
| P00 | Controle mestre e estado canônico | F0 / GOVERNANCA | `EXECUTADO_DOCUMENTALMENTE_SOB_CONTROLE; NAO_AUDITADO; NAO_HOMOLOGADO` [P00/01_ESTADO_CANONICO_CONSOLIDADO_P00_R01.txt] |
| P01 | Trava antideriva e reativação | F0 / GOVERNANCA [INFERIDO — fase/camada não explicitadas no 00_LEIA_PRIMEIRO de P01; atribuídas em P00/04_INVENTARIO_CANONICO_DE_COMPONENTES_R03.csv, linha P01] | `P01_EXECUTADO_DOCUMENTALMENTE; P01_NAO_AUDITADO; P01_NAO_HOMOLOGADO` [P01/00_LEIA_PRIMEIRO.txt] |
| P02 | Catálogo funcional consolidado | F1 / FUNCOES [P00/04_INVENTARIO_CANONICO_DE_COMPONENTES_R03.csv] | `P02_EXECUTADO_DOCUMENTALMENTE; P02_NAO_AUDITADO; P02_NAO_HOMOLOGADO` [P02/00_LEIA_PRIMEIRO.txt] |
| P03 | Núcleo transversal obrigatório | F2 / POLITICAS [P00/04_INVENTARIO...; P03/00_LEIA_PRIMEIRO.txt] | `EXECUTADO_DOCUMENTALMENTE; NAO_AUDITADO; NAO_HOMOLOGADO` [P03/00_LEIA_PRIMEIRO.txt] |
| P04 | BVAA universal e leitura efetiva | F2 / BIBLIOGRAFIA [P00/04_INVENTARIO...] | `EXECUTADO_DOCUMENTALMENTE; NAO_AUDITADO; NAO_HOMOLOGADO` [P04/00_LEIA_PRIMEIRO.txt] |
| P05 | Schema afirmação–evidência | F2 / EVIDENCIA [P00/04_INVENTARIO...] | `EXECUTADO_DOCUMENTALMENTE; NAO_AUDITADO; NAO_HOMOLOGADO`; `GATE_MATERIAL: APROVADO` [P05/00_LEIA_PRIMEIRO.txt] |

Nota: o manifesto declara P05–P28 `NAO_INICIADOS` [MANIFESTO_COLECAO_PACOTES_HOMOLOGADOS_P00_A_P04_R01.json], mas a pasta `PACOTE_SCHEMA_AFIRMACAO_EVIDENCIA_LLM_ACADEMICA_R01` (P05) existe e está integralmente executada com 13 arquivos, incluindo diagnóstico final e teste aprovado. Discrepância registrada em `docs/spec/autoridade-e-lacunas.md`.

---

## 1. O que cada pacote estabelece

### P00 — Controle mestre e estado canônico
Consolida: estado, precedência, linha do tempo, inventário canônico dos componentes/pacotes R03, governança congelada e travas, lacunas não inferíveis, mapa de proveniência documental [P00/00_LEIA_PRIMEIRO.txt]. Regra: "Este pacote consolida documentalmente o P00 sem alterar a R03. Não autoriza P01-P28." [P00/00_LEIA_PRIMEIRO.txt]

### P01 — Trava antideriva e reativação
"Finalidade: Reaplicar as travas do projeto LLM_ACADEMICA após migração de chat, inatividade, troca de modelo, suspeita de deriva ou divergência de estado." [P01/00_LEIA_PRIMEIRO.txt]. Define trava operacional, trava monolítica, protocolo de reativação, protocolo de resposta a comandos vagos, protocolo de restauração de estado, teste de reativação e modelo de recibo de restauração.

### P02 — Catálogo funcional consolidado
Consolida exclusivamente o conteúdo material do pacote-fonte `PACOTE_ESPECIFICACAO_FUNCIONAL_LLM_ACADEMICA_R01.zip` (sha256 `0798eb45...`), fonte "R01_DE_TRABALHO; NAO_HOMOLOGADA; PRESERVADA_COMO_FONTE_HISTORICA" [P02/00_LEIA_PRIMEIRO.txt]. "Escopo consolidado: cinco macrofunções; um requisito funcional transversal; vinte testes históricos preservados como evidência." [P02/00_LEIA_PRIMEIRO.txt] "Nenhuma função adicional foi criada por inferência." [P02/00_LEIA_PRIMEIRO.txt]

### P03 — Núcleo transversal obrigatório
"Consolida" [INFERIDO da estrutura do pacote] doze políticas transversais (POL-001 a POL-012), a máquina de estados documental, a matriz de gates e autoridades, a matriz de proveniência e reversibilidade, e os protocolos de congelamento/reabertura/substituição e de interrupção/retomada/restauração [P03/00_LEIA_PRIMEIRO.txt].

### P04 — BVAA universal e leitura efetiva
"Finalidade: Consolidar políticas universais de controle bibliográfico e documental sem executar verificações bibliográficas de caso concreto e sem assumir a identidade operacional dos prompts históricos BVAA." [P04/00_LEIA_PRIMEIRO.txt] Define a máquina de estados bibliográficos, a matriz de leitura/localização/validação/recomendação, e os protocolos de leitura efetiva, localização e paginação, e recomendação e abstenção.

### P05 — Schema afirmação–evidência
"Finalidade: Definir um schema universal e tecnicamente neutro para vincular afirmações a evidências, preservando identificação, localização, acessibilidade, acesso, leitura, paginação, validação, recomendação e abstenção como dimensões distintas." [P05/00_LEIA_PRIMEIRO.txt] Define schema, dicionário de dados, vocabulário controlado de status, regras de coerência e incompatibilidade, matriz de suficiência e confiança, protocolos de identificadores/versionamento e de rastreabilidade bidirecional.

### Como se conectam
- Cadeia de dependência declarada: P00 → P01 → P02 → P03 → P04 → P05, cada um exigindo o anterior "homologado" como base [ver 00_LEIA_PRIMEIRO de cada pacote].
- P02 fornece as seis unidades funcionais (F01–F05, X01) que P03 preserva sem alteração [P03/09_DIAGNOSTICO_FINAL_P03_R01.txt: "CATALOGO_P02: PRESERVADO_SEM_ALTERACAO_OU_DUPLICACAO_FUNCIONAL"].
- P03 fornece a máquina de estados documental genérica e a matriz de gates que P04 e P05 herdam como base transversal (POL-001 a POL-012 citadas como proveniência em P04 e P05).
- P04 fornece os estados bibliográficos (17 estados) que P05 "preserva" e mapeia para os campos `access_state`, `reading_state`, `validation_state` do schema [P05/01_SCHEMA_AFIRMACAO_EVIDENCIA_P05_R01.md, §6].
- P05 declara explicitamente que não substitui P04: "CON-P05-001 ... Estados do P04 e status mínimos do comando usam rótulos parcialmente diferentes ... Preservadas dimensões do P04 e incluídos aliases funcionais sem apagar distinções." [P05/08_REGISTRO_DE_LACUNAS_E_CONFLITOS_P05_R01.jsonl]

---

## 2. Máquinas de estado

### 2.1 Máquina de estados documental (P03) — genérica, aplicável a qualquer componente P00–P28

Fonte literal: [P03/02_MAQUINA_DE_ESTADOS_DOCUMENTAL_P03_R01.csv]

| Estado | Descrição | Entrada permitida | Evento | Saída | Autoridade | Erro bloqueante | Reversível |
|---|---|---|---|---|---|---|---|
| NAO_INICIADO | Componente ainda não executado. | Cadastro no inventário canônico. | Comando específico após gate. | AUTORIZADO_PARA_EXECUCAO | USUARIO_PROPONENTE | Gate ou dependência ausente | SIM |
| AUTORIZADO_PARA_EXECUCAO | Execução documental específica autorizada. | Dependências homologadas. | Executor inicia comando único. | EM_EXECUCAO_DOCUMENTAL | CHAT_EXECUTOR_DOCUMENTAL | Escopo ambíguo ou entrada material ausente | SIM |
| EM_EXECUCAO_DOCUMENTAL | Produto em elaboração controlada. | Comando e fontes verificados. | Conclusão dos arquivos e testes. | EXECUTADO_NAO_AUDITADO | CHAT_EXECUTOR_DOCUMENTAL | Teste documental falho | SIM |
| EXECUTADO_NAO_AUDITADO | Produto entregue, sem veredito. | Execução concluída. | Comando de auditoria independente. | EM_AUDITORIA | USUARIO_PROPONENTE/CHAT_AUDITOR_INDEPENDENTE | Produto incompleto | SIM |
| EM_AUDITORIA | Auditoria independente em curso. | Objeto material e comando de auditoria. | Veredito. | APROVADO_PARA_DECISAO_AUTORAL ou REPROVADO_PARA_CORRECAO | CHAT_AUDITOR_INDEPENDENTE | Auditor corrige ou amplia escopo | SIM |
| REPROVADO_PARA_CORRECAO | Bloqueador material confirmado. | Parecer de auditoria. | Comando autoral de correção local. | AUTORIZADO_PARA_CORRECAO | USUARIO_PROPONENTE | Correção sem comando | SIM |
| APROVADO_PARA_DECISAO_AUTORAL | Auditoria aprova, sem homologar. | Parecer aprovado. | Decisão autoral. | HOMOLOGADO_E_CONGELADO ou AGUARDANDO_DECISAO | USUARIO_PROPONENTE | Auto-homologação | SIM |
| HOMOLOGADO_E_CONGELADO | Versão vigente protegida. | Termo autoral e hash. | Uso como dependência ou reabertura excepcional. | PERMANECE_CONGELADO ou REABERTO_SOB_AUTORIZACAO | USUARIO_PROPONENTE | Alteração direta | SIM_PARA_VERSAO_ANTERIOR |
| INTERROMPIDO_BLOQUEADO | Execução parada por ausência ou divergência material. | Falha documentada. | Correção da entrada e autorização de retomada. | ESTADO_RESTAURADO | USUARIO_PROPONENTE | Retomada automática | SIM |
| ESTADO_RESTAURADO | Último estado seguro reconstituído. | Objetos canônicos verificados. | Novo comando específico. | AUTORIZADO_PARA_EXECUCAO ou AGUARDANDO_COMANDO | USUARIO_PROPONENTE | Contexto incompleto | SIM |

Nota: nenhum estado posterior é atingido por inferência; cada transição exige evento e autoridade específicos.

### 2.2 Máquina de estados bibliográficos (P04)

Fonte literal: [P04/03_MAQUINA_DE_ESTADOS_BIBLIOGRAFICOS_P04_R01.csv] — 17 estados.

Cadeia principal: `OBRA_NAO_IDENTIFICADA → OBRA_IDENTIFICADA → EDICAO_IDENTIFICADA → LOCALIZADA → ACESSIVEL → ACESSADA → {LEITURA_NAO_REALIZADA | LEITURA_INDIRETA | LEITURA_PARCIAL | LEITURA_INTEGRAL} → {PAGINA_NAO_CONFIRMADA | PAGINA_CONFIRMADA} → {VALIDACAO_PENDENTE | VALIDADA} → {RECOMENDACAO_CONDICIONAL | RECOMENDADA} → ABSTENCAO_BIBLIOGRAFICA (a qualquer momento)`.

Definições literais completas de cada estado (definição; evidência mínima; ação permitida; ação proibida):

- **OBRA_NAO_IDENTIFICADA**: "não há identidade documental mínima"; evidência mínima "registro da ausência ou ambiguidade"; ação permitida "pedir dados mínimos"; ação proibida "atribuir obra específica". [P04/03_MAQUINA_DE_ESTADOS_BIBLIOGRAFICOS_P04_R01.csv]
- **OBRA_IDENTIFICADA**: "autor/título ou identificador mínimo confirmados"; ação proibida "declarar edição ou leitura".
- **EDICAO_IDENTIFICADA**: "edição/volume/tradução/suporte diferenciados"; ação proibida "transferir paginação entre edições".
- **LOCALIZADA**: "objeto encontrado em repositório ou suporte determinado"; ação proibida "declarar acesso/leitura".
- **ACESSIVEL**: "objeto pode ser materialmente aberto/obtido"; ação proibida "declarar conteúdo examinado".
- **ACESSADA**: "objeto foi efetivamente aberto ou recuperado"; ação proibida "declarar leitura sem exame".
- **LEITURA_NAO_REALIZADA**: "nenhum exame substantivo foi feito"; ação proibida "atribuir conteúdo à obra".
- **LEITURA_INDIRETA**: "conhecimento deriva de fonte secundária ou relato"; ação proibida "afirmar leitura primária".
- **LEITURA_PARCIAL**: "parte delimitada foi examinada"; ação proibida "declarar leitura integral".
- **LEITURA_INTEGRAL**: "objeto completo foi examinado"; evidência mínima "acesso ao objeto completo e registro de exame integral"; ação proibida "declarar sem evidência".
- **PAGINA_NAO_CONFIRMADA**: "localização interna não foi materialmente verificada"; ação proibida "usar página específica".
- **PAGINA_CONFIRMADA**: "página/fólio/seção foi confrontado com suporte identificado"; ação proibida "transpor para outra edição".
- **VALIDACAO_PENDENTE**: "evidência ainda insuficiente para decisão"; ação proibida "liberar uso".
- **VALIDADA**: "uso proposto é sustentado pela evidência declarada"; evidência mínima "cadeia obra-edição-acesso-leitura-localização-correspondência"; ação proibida "extrapolar escopo".
- **RECOMENDACAO_CONDICIONAL**: "obra pode ser útil, mas há condição documental pendente"; ação proibida "apresentar como validada".
- **RECOMENDADA**: "recomendação sustentada por leitura/validação adequadas à finalidade"; ação proibida "garantir conteúdo não verificado".
- **ABSTENCAO_BIBLIOGRAFICA**: "interrupção obrigatória por falta ou conflito de evidência"; ação permitida "declarar impossibilidade e pedir uma evidência"; ação proibida "inventar ou completar por plausibilidade".

Transições literais (18, [P04/03_MAQUINA_DE_ESTADOS_BIBLIOGRAFICOS_P04_R01.csv] — arquivo de transições distinto do de estados, mesmo nome numérico mas conteúdo próprio de 18 linhas): notáveis —
- T18: `QUALQUER_ESTADO → ABSTENCAO_BIBLIOGRAFICA`; gatilho "comando solicita invenção de referência/metadado"; ação proibida "obedecer ao comando".
- T13: `VALIDACAO_PENDENTE → ABSTENCAO_BIBLIOGRAFICA`; gatilho "evidência não obtida ou conflitante".
- T17: `PAGINA_NAO_CONFIRMADA → ABSTENCAO_BIBLIOGRAFICA`; gatilho "página necessária e não comprovada".

---

## 3. Gates e autoridades

### MATRIZ_DE_GATES_E_AUTORIDADES (P03)
Fonte literal: [P03/03_MATRIZ_DE_GATES_E_AUTORIDADES_P03_R01.csv]

| gate_id | Objeto | Pré-condição | Autoridade que autoriza | Executor | Auditor | Ação permitida | Ação proibida | Saída |
|---|---|---|---|---|---|---|---|---|
| GATE-P03-01 | Início do P03 | P02 homologado; P00 e P01 preservados; R03 íntegra | USUARIO_PROPONENTE | CHAT_EXECUTOR_DOCUMENTAL | CHAT_AUDITOR_INDEPENDENTE | Executar exclusivamente P03 | Reabrir P00-P02; iniciar P04-P28 | P03_EXECUTADO_NAO_AUDITADO |
| GATE-P03-02 | Auditoria do P03 | Quatro produtos entregues | USUARIO_PROPONENTE | CHAT_AUDITOR_INDEPENDENTE | CHAT_AUDITOR_INDEPENDENTE | Executar TESTE_TRANSVERSAL e auditar integridade | Corrigir ou homologar | VEREDITO_DE_AUDITORIA |
| GATE-P03-03 | Homologação do P03 | Parecer aprovado | USUARIO_PROPONENTE | USUARIO_PROPONENTE | CHAT_AUDITOR_INDEPENDENTE | Homologar e congelar por termo expresso | Homologação automática | P03_HOMOLOGADO_E_CONGELADO |
| GATE-P04-01 | Início do P04 | P03 homologado e comando específico | USUARIO_PROPONENTE | CHAT_EXECUTOR_DOCUMENTAL | CHAT_AUDITOR_INDEPENDENTE | Executar P04 após autorização | Iniciar com P03 apenas executado ou auditado | P04_AUTORIZADO |

Nota: a matriz de P03 só formaliza gates até P04-01; gates equivalentes para P05–P28 não estão presentes nesta leva [INFERIDO — ausência constatada por leitura integral do arquivo].

### MATRIZ_DE_REQUISITOS_LIMITES_GATES_E_SAIDAS (P02)
Fonte literal: [P02/03_MATRIZ_DE_REQUISITOS_LIMITES_GATES_E_SAIDAS_P02_R01.csv] — por função (LLM-ACA-F01 a F05, LLM-ACA-X01): requisitos funcionais, requisitos de abstenção, limite de escopo ("Somente a função descrita; não escolher arquitetura, tecnologia ou política pertencente a P03-P28" — repetido literalmente para as seis unidades), gate de autorização (humano, específico por função), condição de erro ("Material insuficiente; proveniência não comprovada; comando vago; tentativa de inferir fonte, decisão ou conclusão" — repetido literalmente), saída esperada e critério de encerramento ("Saídas verificáveis entregues, pendências explícitas, auditoria do bloco concluída e nenhuma ação forte executada sem autorização" — repetido literalmente).

### Bloqueio duro — o que é
Constatação transversal: em todas as matrizes lidas, toda condição de erro classificada é "BLOQUEANTE" quando compromete "identidade, conteúdo, escopo, proveniência ou veredito" [P01/04_PROTOCOLO_DE_RESTAURACAO_DE_ESTADO_P01_R01.txt, classe A]; as 20 regras de coerência do P05 (RC-001 a RC-020) são majoritariamente `BLOQUEANTE`, com exceção de RC-017 e RC-018, classificadas `MAIOR` [P05/04_REGRAS_DE_COERENCIA_E_INCOMPATIBILIDADE_P05_R01.csv].

---

## 4. Travas anti-deriva (P01)

### Versão operacional
Fonte literal: [P01/01_TRAVA_ANTIDERIVA_OPERACIONAL_P01_R01.txt]. Regras: não importar conteúdo externo sem autorização; não preencher lacunas por inferência; não tratar comandos históricos como vigentes; não alterar a R03; não reabrir P00 sem erro material novo, evidência, impacto e autorização autoral; não iniciar componente posterior sem autorização específica; não converter comando vago em transição; não transformar falha formal sem impacto em bloqueador substantivo; interromper somente diante de divergência material relevante; preservar uma única próxima ação operacional. Define separação de papéis: USUARIO_PROPONENTE (autoriza/decide/homologa/congela), CONTROLADOR_ARQUITETO (organiza/delimita/preserva estado), EXECUTOR_DOCUMENTAL (produz somente o objeto autorizado), AUDITOR_INDEPENDENTE (verifica sem corrigir ou homologar).

### Versão monolítica
Fonte literal: [P01/05_TRAVA_ANTIDERIVA_MONOLITICA_P01_R01.txt]. Princípio: "Cada componente P00-P28 é autônomo." Proibições: agrupar componentes em lotes operacionais; emitir autorização coletiva; executar/auditar/homologar vários componentes como unidade; usar P00 ou P01 como autorização transversal; fundir escopos/gates/papéis/produtos/decisões; absorver componente posterior em anterior; converter eficiência operacional em supressão de autonomia; presumir autorização futura; iniciar P(n+1) sem decisão autoral específica. Classificação de violação: `DERIVA_MONOLITICA_BLOQUEADORA`. Ação: `INTERROMPER / PRESERVAR_ESTADO / REGISTRAR_EXPANSAO_INDEVIDA / AGUARDAR_COMANDO_AUTORAL_ESPECIFICO`.

### Diferença entre as duas e quando cada uma se aplica
- A trava **operacional** regula o comportamento dentro da execução de um componente individual (importação de conteúdo, inferência, comandos históricos, alteração de R03, reabertura, comando vago, papéis).
- A trava **monolítica** regula especificamente o risco de **fusão entre componentes** — impede que a eficiência de processar vários pacotes na mesma sessão vire supressão da autonomia de cada um. É acionada quando há tentativa de tratar dois ou mais componentes P00–P28 como uma unidade.
- "Aceleração permitida" pela trava monolítica, sem violar a autonomia: eliminar documentos redundantes dentro do *mesmo* componente; reutilizar objetos já verificados no mesmo chat; manifesto único por produto; impedir referências circulares de hash; eliminar preparação da preparação; limitar auditoria a requisitos e resultados reais [P01/05_TRAVA_ANTIDERIVA_MONOLITICA_P01_R01.txt].

### Protocolo de resposta a comandos vagos
Fonte literal: [P01/03_PROTOCOLO_DE_RESPOSTA_A_COMANDOS_VAGOS_P01_R01.txt]. Comandos vagos exemplificativos: "prossiga; continue; avance; execute; pode seguir; faça o próximo." Regra: comando vago não autoriza iniciar componente novo, executar produto substantivo, auditar, homologar, alterar a R03, reabrir componente congelado, fundir componentes, ou autorizar arquitetura/corpus/treinamento/RAG/fine-tuning/implementação/pilotos. Resposta operacional: (1) identificar a próxima ação canônica já autorizada, se existir; (2) se não existir, não executar transição; (3) produzir no máximo um único instrumento de autorização específico quando proporcional; (4) não criar cadeia de preparação da preparação; (5) não exigir reenvio de arquivo já presente e verificado; (6) não inventar escopo. Saída: `AGUARDANDO_COMANDO_AUTORAL_ESPECIFICO`.

### Protocolo de restauração de estado
Fonte literal: [P01/04_PROTOCOLO_DE_RESTAURACAO_DE_ESTADO_P01_R01.txt]. Objetivo: "Restaurar o estado canônico verificável do projeto sem executar transição." Conferências obrigatórias: identidade do projeto; autoridade da R03; estado do P00; estado de P01-P28; hashes dos objetos essenciais disponíveis; decisões congeladas; pendências abertas; papéis e autoridades; travas e proibições; única próxima ação autorizada. Classificação de divergências:
- **A. MATERIAL_BLOQUEADORA** — "Compromete identidade, conteúdo, escopo, proveniência ou veredito."
- **B. FORMAL_NAO_BLOQUEADORA** — "Não altera identidade, conteúdo, escopo, proveniência ou veredito."
- **C. NAO_COMPROVADA** — "Não pode ser resolvida por inferência."

Regras: divergência formal não bloqueia isoladamente; divergência material exige interrupção; ausência de evidência não autoriza reconstrução; objeto confirmado por hash não deve ser solicitado novamente sem necessidade real; restauração não homologa nem inicia componente. Saída: `RECIBO_DE_RESTAURACAO`.

O protocolo de reativação [P01/02_PROTOCOLO_DE_REATIVACAO_P01_R01.txt] lista os gatilhos (mudança de chat; inatividade prolongada; troca de modelo; suspeita de deriva; divergência de estado; retomada após interrupção) e a sequência de 9 passos culminando em "Parar e aguardar comando autoral específico."

---

## 5. Vocabulário controlado

Definições literais, por termo, com fonte:

- **DERIVA_MONOLITICA_BLOQUEADORA**: classificação para "Qualquer expansão transversal não autorizada" entre componentes [P01/05_TRAVA_ANTIDERIVA_MONOLITICA_P01_R01.txt].
- **GATE**: [INFERIDO — o termo não recebe definição isolada; seu significado operacional decorre da MATRIZ_DE_GATES_E_AUTORIDADES: um ponto de controle com objeto, pré-condição, autoridade que autoriza, executor, auditor, ação permitida, ação proibida e saída — P03/03_MATRIZ_DE_GATES_E_AUTORIDADES_P03_R01.csv].
- **TRAVA_ANTIDERIVA_ATIVA**: estado declarado do pacote P01 [P01/01_TRAVA_ANTIDERIVA_OPERACIONAL_P01_R01.txt].
- **CONGELADO / HOMOLOGADO_E_CONGELADO**: estado da máquina documental P03: "Versão vigente protegida"; entrada exige "Termo autoral e hash"; ação proibida "Alteração direta"; reversível "SIM_PARA_VERSAO_ANTERIOR" [P03/02_MAQUINA_DE_ESTADOS_DOCUMENTAL_P03_R01.csv].
- **PENDENTE_BVAA**: não definido nos pacotes P00–P05 como estado formal; aparece apenas na proveniência do P04 como referência a regra histórica: "PENDENTE_BVAA não se converte em LIBERADA sem nova evidência" [P04/08_MAPA_DE_PROVENIENCIA_BVAA_P04_R01.jsonl, registro P04-PROV-002]. Não é um dos 17 estados canônicos da máquina de estados bibliográficos vigente — é herança do material histórico anexado, tratada como regra, não como estado ativo. **[LACUNA — o termo PEDIR_PDF citado no prompt de trabalho não foi localizado em nenhum dos seis pacotes; registrado como pendente de leva posterior.]**
- **CORRIGIR_ANTES_DE_AVANÇAR**: não localizado literalmente nos seis pacotes lidos. **[LACUNA — pendente de leva posterior, não localizado em P00–P05.]**
- **LEITURA_EFETIVA**: título do protocolo [P04/05_PROTOCOLO_DE_LEITURA_EFETIVA_P04_R01.txt]. Regra central: "LEITURA é um estado documental comprovável, distinto de identificação, localização, acessibilidade e acesso." Escala: LEITURA_NAO_REALIZADA → LEITURA_INDIRETA → LEITURA_PARCIAL → LEITURA_INTEGRAL.
- **ABSTENÇÃO / ABSTENCAO_BIBLIOGRAFICA**: "interrupção obrigatória por falta ou conflito de evidência"; obrigatória quando "obra ou edição não podem ser identificadas; acesso não foi comprovado; leitura alegada não pode ser demonstrada; página, citação ou metadado divergem; fonte secundária é usada como prova de leitura primária; evidência não sustenta a afirmação; o comando exige invenção." [P04/02_PROTOCOLO_BVAA_UNIVERSAL_P04_R01.md, §11; P04/03_MAQUINA_DE_ESTADOS_BIBLIOGRAFICOS_P04_R01.csv]
- **PROVENIÊNCIA**: POL-005: "Manter vínculo entre cada decisão, dado e artefato e sua fonte" [P03/01_POLITICAS_TRANSVERSAIS_P03_R01.md]. No P05, campo obrigatório: "Registrar origem e cadeia de custódia documental"; deve conter "Origem, método, objeto, versão e evento" [P05/02_DICIONARIO_DE_DADOS_P05_R01.csv].
- **DIVERGÊNCIA MATERIAL / FORMAL / NÃO COMPROVADA**: ver POL-008 [P03/01_POLITICAS_TRANSVERSAIS_P03_R01.md] e classificação A/B/C do protocolo de restauração [P01/04_PROTOCOLO_DE_RESTAURACAO_DE_ESTADO_P01_R01.txt].
- **USO_LIBERADO**: "exige simultaneamente: fonte identificada; acesso efetivo quando o conteúdo da fonte sustenta a afirmação; leitura suficiente; localização confirmada quando houver citação ou marcador específico; VALIDADA; EVIDENCIA_SUFICIENTE; e ausência de conflito bloqueante." [P05/01_SCHEMA_AFIRMACAO_EVIDENCIA_P05_R01.md, §7]
- **SUFICIÊNCIA vs CONFIANÇA**: "suficiência mede adequação da evidência ao uso delimitado; confiança mede robustez da avaliação registrada" [P05/01_SCHEMA_AFIRMACAO_EVIDENCIA_P05_R01.md, §3.4]. "Confiança alta não corrige evidência ausente ou insuficiente" (princípio 5, mesmo arquivo).
- **PRÓXIMA_AÇÃO_ÚNICA**: POL-012: "Reduzir deriva operacional e ciclos recursivos" — "Registrar exatamente uma próxima ação permitida ou nenhuma automática"; proibido "Oferecer múltiplas ações simultâneas ou executar encadeamento automático" [P03/01_POLITICAS_TRANSVERSAIS_P03_R01.md].

---

## 6. Schema afirmação-evidência (P05)

### Unidade lógica
"A unidade mínima é uma relação afirmação–evidência ... A chave composta (claim_id, source_id, relation_version) identifica cada relação versionada." [P05/01_SCHEMA_AFIRMACAO_EVIDENCIA_P05_R01.md, §2]

### Campos (dicionário de dados completo — 23 campos)
Fonte literal integral: [P05/02_DICIONARIO_DE_DADOS_P05_R01.csv]. Campos: `claim_id`, `claim_text`, `claim_type`, `source_id`, `source_type`, `source_reference`, `edition_or_version`, `location_type`, `location_value`, `page_or_folio`, `evidence_excerpt`, `evidence_level`, `access_state`, `reading_state`, `validation_state`, `sufficiency`, `confidence`, `usage_status`, `provenance`, `validator`, `validation_date`, `reversibility`, `notes`. Cada um com finalidade, tipo, obrigatoriedade, valores permitidos, regra de validação, dependência, condição de erro e exemplo abstrato — ver arquivo fonte para transcrição campo a campo (23 linhas).

### Vocabulário de status (dimensões)
Fonte literal: [P05/01_SCHEMA_AFIRMACAO_EVIDENCIA_P05_R01.md, §6] e [P05/03_VOCABULARIO_CONTROLADO_DE_STATUS_P05_R01.csv]:
- `access_state`: NÃO_LOCALIZADA, LOCALIZADA, ACESSIVEL, ACESSADA.
- `reading_state`: LEITURA_NAO_REALIZADA, LEITURA_INDIRETA, LIDA_PARCIALMENTE, LIDA_INTEGRALMENTE.
- `validation_state`: NAO_VERIFICADA, PAGINA_NAO_CONFIRMADA, PAGINA_CONFIRMADA, VALIDACAO_PENDENTE, VALIDADA, INVALIDADA_POSTERIORMENTE.
- `sufficiency`: NAO_AVALIADA, EVIDENCIA_AUSENTE, EVIDENCIA_INSUFICIENTE, EVIDENCIA_PARCIALMENTE_SUFICIENTE, EVIDENCIA_SUFICIENTE, CONFLITANTE.
- `confidence`: NAO_AVALIADA, BAIXA, MEDIA, ALTA. "É vedada ALTA sem base material explicitada."
- `usage_status`: NAO_USAR, USO_CONDICIONAL, USO_LIBERADO, ABSTENCAO.

### Regras de coerência (20 regras, RC-001 a RC-020)
Fonte literal integral: [P05/04_REGRAS_DE_COERENCIA_E_INCOMPATIBILIDADE_P05_R01.csv]. Destaques literais:
- RC-007: "confidence=ALTA é incompatível com EVIDENCIA_AUSENTE" → ação em erro "REBAIXAR confiança e NAO_USAR" — "Confiança não cria evidência".
- RC-009: "usage_status=USO_LIBERADO exige VALIDADA e EVIDENCIA_SUFICIENTE" → ação em erro "NAO_USAR".
- RC-016: "claim_id e source_id são imutáveis e não recicláveis" → ação em erro "REJEITAR registro".
- RC-019: "Pedido para inventar página/evidência gera ABSTENCAO e NAO_USAR" → ação "PARAR e registrar" — "Trava anti-invenção".

### Matriz de suficiência e confiança
Fonte literal integral: [P05/05_MATRIZ_DE_SUFICIENCIA_E_CONFIANCA_P05_R01.csv] — 24 combinações cruzando as 6 categorias de `sufficiency` com as 4 de `confidence`, cada uma com "combinação_permitida" (SIM/NAO), "estado_de_validacao_maximo" e "uso_maximo". Regra geral repetida: nenhuma combinação com `EVIDENCIA_INSUFICIENTE` ou `EVIDENCIA_AUSENTE` permite `USO_LIBERADO`, independentemente do nível de confiança.

### Rastreabilidade bidirecional
Fonte literal: [P05/07_PROTOCOLO_DE_RASTREABILIDADE_BIDIRECIONAL_P05_R01.txt]. "Objetivo: Permitir reconstrução completa nos dois sentidos sem memória externa." Cardinalidades: "1 claim : N evidências — uma relação por evidência. 1 evidência : N claims — uma relação por afirmação. N:N é representado por relações independentes, nunca por célula agregada opaca." Critério de sucesso: "Dado apenas um claim_id ou source_id, é possível reconstruir todas as relações, versões, estados, autoridades e eventos relevantes."

---

## 7. Protocolo BVAA (P04)

### Princípio central
"Sem evidência material suficiente, não se declara leitura, página, edição, DOI, ISBN, URL, citação literal, referência consolidada ou sustentação documental." [P04/02_PROTOCOLO_BVAA_UNIVERSAL_P04_R01.md, §2]

### Matriz de evidência (4 níveis)
Fonte literal [mesmo arquivo, §4]:
- **Nível A** — evidência interna fornecida: "trecho e dados contidos no próprio pacote documental."
- **Nível B** — evidência material anexada: "PDF, scan, DOCX, imagem ou arquivo acessível."
- **Nível C** — evidência por ferramenta/conector efetivamente usado: "retorno observável e rastreável."
- **Nível D** — evidência ausente: "memória, título provável, referência incompleta ou arquivo apenas mencionado."

### Protocolo de leitura efetiva
Ver §5 acima (vocabulário) e transcrição completa em [P04/05_PROTOCOLO_DE_LEITURA_EFETIVA_P04_R01.txt]. Proibições literais: "converter acesso em leitura; converter leitura parcial em integral; declarar leitura primária com base em fonte secundária; declarar leitura de edição diferente; preencher partes não lidas por memória ou conhecimento geral; usar resumo, índice ou metadado como prova de leitura integral."

### Protocolo de localização e paginação
[P04/06_PROTOCOLO_DE_LOCALIZACAO_E_PAGINACAO_P04_R01.txt]. "Regra de dupla verificação: 1. confirmar que o trecho aparece no suporte acessado; 2. confirmar que o marcador corresponde à edição e ao suporte declarados." Distinções obrigatórias literais: "página impressa não é automaticamente página do PDF; OCR não substitui fac-símile quando a literalidade é crítica; edição, tradução, volume e tomo divergentes não compartilham paginação por presunção; URL de localização não comprova conteúdo; DOI/ISBN identificam objetos, mas não comprovam leitura." Proibido inventar: "página, fólio, edição, tradução, volume, tomo, DOI, ISBN, URL, título, autoria, data ou trecho."

### Protocolo de recomendação e abstenção
[P04/07_PROTOCOLO_DE_RECOMENDACAO_E_ABSTENCAO_BIBLIOGRAFICA_P04_R01.txt]. Cadeia: "CONHECIMENTO_NOMINAL → IDENTIFICACAO → LOCALIZACAO → ACESSO → LEITURA → VALIDACAO → RECOMENDACAO." Regra: "Nenhuma etapa posterior é inferida automaticamente a partir da anterior." Abstenção obrigatória diante de (lista literal): "obra não identificada; edição incerta; acesso não comprovado; leitura não comprovada; página/citação não confirmada; metadado conflitante; fonte secundária apresentada como leitura primária; evidência incompatível com a afirmação; comando para inventar dados." Saída da abstenção: "Declarar o que não pode ser comprovado, registrar a evidência ausente e indicar uma única ação documental necessária."

---

## 8. Lacunas de leva futura (não falha da especificação)

Os seguintes termos citados no roteiro de trabalho não foram localizados nos seis pacotes P00–P05:
- `PEDIR_PDF`
- `CORRIGIR_ANTES_DE_AVANÇAR`

Registrados aqui como pendentes de leva posterior (P06–P28), conforme regra do enunciado: "lacuna encontrada aqui pode ser conteúdo de pacote futuro, não omissão."

## 9. Fechamento

Este mapa cobre integralmente P00–P05 (leva R01, ~324 KB confirmados). Será atualizado por incremento quando novas levas (P06 em diante) chegarem. Não contém avaliação, proposta ou arquitetura.

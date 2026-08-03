# AUTORIDADE E LACUNAS — LLM_ACADEMICA (P00–P05, leva R01)

## 1. Cadeia de autoridade

### A R03 como autoridade canônica ausente deste acervo
A R03 (`PACOTE_PROTOCOLO_MESTRE_ACAO_ECOSSISTEMA_LLM_ACADEMICA_R03.zip`, sha256 `0f7e3acf43d09562a4dbdc6adfccc3535b950b0e6548aa49fa81d127a3d1b39f`) é declarada em todos os seis pacotes como "AUTORIDADE_CANONICA_VIGENTE" [P00/01_ESTADO_CANONICO_CONSOLIDADO_P00_R01.txt] e "HOMOLOGADA E CONGELADA" [P00/00_LEIA_PRIMEIRO.txt]. **O objeto R03 em si não está presente no corpus `governanca-R01`** — apenas seu SHA-256 e referências a ele.

### O que os pacotes atribuem à R03 sem reproduzir
- "PROTOCOLO_MESTRE_R03_HOMOLOGADO_E_CONGELADO" como base vigente de P01 [P01/00_LEIA_PRIMEIRO.txt; P01/01_TRAVA_ANTIDERIVA_OPERACIONAL_P01_R01.txt].
- Matriz de dependências e papéis: "proveniência: R03 matriz de dependências e papéis" (POL-002) [P03/01_POLITICAS_TRANSVERSAIS_P03_R01.md].
- Matriz de papéis: "proveniência: R03 matriz de papéis; P00 governança" (POL-004) [mesmo arquivo].
- Mapa de cobertura: "proveniência: R03 mapa de cobertura; P00 mapa de proveniência" (POL-005) [mesmo arquivo].
- Estado/travas: "proveniência: R03 estado/travas; P01; P00" (POL-006) [mesmo arquivo].
- Inventário de componentes e pacotes a produzir: fonte de `04_INVENTARIO_CANONICO_DE_COMPONENTES_R03.csv` e `05_INVENTARIO_CANONICO_DE_PACOTES_R03.csv` são, segundo o mapa de proveniência do P00, cópias byte a byte de `02_INVENTARIO_DE_COMPONENTES_E_PACOTES_A_PRODUZIR_R03.csv` e `10_REGISTRO_PRINCIPAL_DE_PACOTES_STATUS_E_PRECEDENCIA_R03.csv` [P00/08_MAPA_DE_PROVENIENCIA_DOCUMENTAL_P00_R01.csv] — arquivos-fonte da R03 não presentes neste acervo, apenas suas cópias já transcritas nos CSVs de P00.
- Termo de autoridade atual e recibo de retificação final mínima: "01_TERMO_DE_AUTORIDADE_ATUAL.txt" e "12_RECIBO_DE_RETIFICACAO_FINAL_MINIMA_R03.txt" [P00/03_LINHA_DO_TEMPO_CANONICA_P00_R01.csv] — não presentes neste acervo.
- Seis profiles temáticos V117: "os seis profiles V117 permanecem canônicos" [P00/01_ESTADO_CANONICO_CONSOLIDADO_P00_R01.txt] — conteúdo dos profiles não presente; apenas sua existência e congelamento são referenciados via `PACOTE_04_PROFILES_TEMATICOS_V117(4).zip` no inventário de proveniência R03 [P00/05_INVENTARIO_CANONICO_DE_PACOTES_R03.csv, registro PKG-013].

**Isso é o que falta e não dá para inferir**: o conteúdo textual completo da R03 — seu protocolo de ação, sua matriz de papéis e dependências detalhada, seu mapa de cobertura, e os quatro bloqueadores finais que motivaram a retificação da R02 para a R03 (mencionados apenas como "Define os quatro bloqueadores finais" no registro PKG-003 [P00/05_INVENTARIO_CANONICO_DE_PACOTES_R03.csv], sem enumeração).

### Regra de precedência
"REGRA_DE_PRECEDENCIA: R03 > R02 > R01" [P00/01_ESTADO_CANONICO_CONSOLIDADO_P00_R01.txt]. "EFEITO_DA_PRECEDENCIA: R03 substitui R02 como controladora sem apagar R01/R02. O termo externo de homologação e congelamento prevalece sobre estados internos pré-homologação do objeto R03." [mesmo arquivo]

Detalhamento por objeto [P00/02_MATRIZ_DE_PRECEDENCIA_P00_R01.csv]:
| Ordem | Revisão/objeto | Status | Efeito | Uso autorizado |
|---|---|---|---|---|
| 1 | R03 | HOMOLOGADA_E_CONGELADA | CONTROLADORA_ATUAL | USAR_COMO_AUTORIDADE_CANONICA |
| 2 | R02 | HISTORICA_SUBSTITUIDA | PRESERVADA_SEM_CONTROLE_ATUAL | CONSULTA_HISTORICA_QUANDO_NECESSARIA |
| 3 | R01 | HISTORICA | PRESERVADA_SEM_CONTROLE_ATUAL | CONSULTA_HISTORICA_QUANDO_NECESSARIA |
| 4 | MATERIAL_INVALIDADO | SEM_AUTORIDADE | NAO_PODE_SER_REATIVADO | PRESERVAR_SOMENTE_COMO_REGISTRO |

**O que isso implica**: nenhuma decisão nos pacotes P00–P05 pode contrariar a R03; onde a R03 é omissa (o próprio texto não está disponível), a lacuna não pode ser preenchida por inferência a partir de R02/R01 — essas permanecem apenas "consulta histórica".

---

## 2. Estado real de cada pacote — contradições

### Contradição central: P00 autodeclarado NAO_AUDITADO/NAO_HOMOLOGADO vs. manifesto da coleção declarando HOMOLOGADO_E_CONGELADO

- **P00, autodeclaração interna**: "ESTADO_DO_P00: EXECUTADO_DOCUMENTALMENTE_SOB_CONTROLE / NAO_AUDITADO / NAO_HOMOLOGADO" [P00/01_ESTADO_CANONICO_CONSOLIDADO_P00_R01.txt]. Mesmo arquivo, ao final: "ESTADO_FINAL_DESTE_ARTEFATO: P00_EXECUTADO_DOCUMENTALMENTE_SOB_CONTROLE / AGUARDANDO_AUDITORIA_INDEPENDENTE_FUTURA_NAO_AUTOMATICA". O próprio `00_LEIA_PRIMEIRO.txt` do P00 repete: "STATUS: PRODUTO_DOCUMENTAL_EXECUTADO / NAO_AUDITADO / NAO_HOMOLOGADO."
- **Manifesto da coleção**: `MANIFESTO_COLECAO_PACOTES_HOMOLOGADOS_P00_A_P04_R01.json` declara, para P00, `"estado": "HOMOLOGADO_E_CONGELADO"`, e o mesmo para P01, P02, P03 e P04. O campo de nível superior confirma: `"P00_P04": "HOMOLOGADOS_E_CONGELADOS"`.

Esta é uma contradição direta e não resolvida nesta leitura, conforme instrução do enunciado ("Não resolva").

### Mapa de estado autodeclarado por pacote

| Pacote | Autodeclaração no próprio 00_LEIA_PRIMEIRO / diagnóstico final | Declaração no manifesto da coleção |
|---|---|---|
| P00 | `NAO_AUDITADO; NAO_HOMOLOGADO` [P00/00_LEIA_PRIMEIRO.txt] | `HOMOLOGADO_E_CONGELADO` [MANIFESTO_COLECAO...json] |
| P01 | `P01_NAO_AUDITADO; P01_NAO_HOMOLOGADO` [P01/00_LEIA_PRIMEIRO.txt] | `HOMOLOGADO_E_CONGELADO` [MANIFESTO...json] |
| P02 | `P02_AINDA_NAO_AUDITADO; P02_AINDA_NAO_HOMOLOGADO` [P02/08_DIAGNOSTICO_FINAL_P02_R01.txt] | `HOMOLOGADO_E_CONGELADO` [MANIFESTO...json] |
| P03 | `P03_AINDA_NAO_AUDITADO; P03_AINDA_NAO_HOMOLOGADO` [P03/09_DIAGNOSTICO_FINAL_P03_R01.txt] | `HOMOLOGADO_E_CONGELADO` [MANIFESTO...json] |
| P04 | `NAO_AUDITADO; NAO_HOMOLOGADO`; diagnóstico final: "P04: EXECUTADO_DOCUMENTALMENTE / NAO_AUDITADO / NAO_HOMOLOGADO" [P04/11_DIAGNOSTICO_FINAL_P04_R01.txt] | `HOMOLOGADO_E_CONGELADO` [MANIFESTO...json] |
| P05 | `EXECUTADO_DOCUMENTALMENTE; NAO_AUDITADO; NAO_HOMOLOGADO` [P05/00_LEIA_PRIMEIRO.txt]; diagnóstico final confirma "P05_AINDA_NAO_AUDITADO / P05_AINDA_NAO_HOMOLOGADO" [P05/10_DIAGNOSTICO_FINAL_P05_R01.txt] | P05 não consta no manifesto da coleção (que cobre apenas P00–P04) |

**Contradição adicional interna**: P04 e P05, ao descreverem suas próprias bases, afirmam "P00, P01, P02 E P03 HOMOLOGADOS E CONGELADOS" [P04/00_LEIA_PRIMEIRO.txt] e "P00, P01, P02, P03 e P04 homologados e congelados" [P05/00_LEIA_PRIMEIRO.txt] — ou seja, os próprios pacotes P04 e P05 tratam seus antecessores como já homologados, mesmo que os antecessores se autodeclarem, em seus respectivos diagnósticos finais, "NAO_HOMOLOGADO". Não resolvida nesta leitura.

---

## 3. Lacunas não inferíveis (compiladas dos cinco pacotes + P05)

| ID | Objeto | O que fica bloqueado |
|---|---|---|
| LAC-00-01 | Detalhamento final do futuro P00 [P00/07_LACUNAS_NAO_INFERIVEIS_P00_R01.txt] | Nenhum detalhamento adicional pode ser inferido além das saídas mínimas consolidadas |
| LAC-00-02 | Objeto que o P00 substituirá — `VALOR_CANONICO: NAO_DEFINIDO` [mesmo arquivo] | Precedência final do P00 sobre um objeto predecessor específico |
| LAC-00-03 | Conteúdo operacional detalhado de cada artefato interno além das saídas mínimas [mesmo arquivo] | Qualquer detalhamento operacional não explicitamente registrado |
| — (gerais, P00) | arquitetura técnica; plataforma; modelo(s); fornecedor; número de agentes; corpus; licenças; privacidade; treinamento; RAG; fine-tuning; implementação; pilotos [mesmo arquivo] | Toda decisão técnica ou de implementação — ver `decisoes-vetadas.md` |
| LAC-P02-001 | Inventário canônico das 44 funções, não disponível na fonte P02 [P02/06_REGISTRO_DE_LACUNAS_FUNCIONAIS_P02_R01.jsonl] | Afirmar cobertura nominal completa das 44 funções históricas; catálogo permanece restrito às 6 unidades comprovadas |
| LAC-P02-002 | Fechamento autoral integral do levantamento funcional não comprovado como evento autônomo [mesmo arquivo] | Declarar o levantamento funcional como definitivamente encerrado |
| LAC-P02-003 | Normas institucionais e editoriais específicas (variam por instituição/periódico) [mesmo arquivo] | Aplicação de F01, F03, F05 sem fornecimento e verificação do caso concreto |
| LAC-P02-004 | Implementação técnica de comentários Word e mapas de evidência [mesmo arquivo] | Qualquer especificação técnica de interoperabilidade — fora do escopo de P02 |
| LAC-P02-005 | Funções adicionais além de F01–F05 e X01 [mesmo arquivo] | Ampliação do catálogo funcional sem nova fonte e decisão autoral específica |
| P03-LAC-001 | Inventário canônico das 44 funções não disponível no P02 [P03/07_REGISTRO_DE_LACUNAS_E_CONFLITOS_TRANSVERSAIS_P03_R01.jsonl] | Afirmar cobertura nominal das 44 funções (herdada do P02) |
| P03-LAC-002 | Arquitetura, modelo, fornecedor, plataforma e infraestrutura não definidos [mesmo arquivo] | Qualquer decisão técnica — "nenhum [impacto] para o núcleo documental independente de tecnologia" |
| P04-LAC-001 | Materiais históricos não contêm inventário universal de obras/edições/repositórios [P04/09_REGISTRO_DE_LACUNAS_E_CONFLITOS_BVAA_P04_R01.jsonl] | Qualquer catálogo bibliográfico concreto por inferência |
| P04-LAC-002 | Tecnologia, banco, indexador, API, fornecedor, plataforma não definidos [mesmo arquivo] | Implementação — "não autorizada" |
| P04-LAC-003 | "Leitura integral" requer evidência operacional específica em cada caso [mesmo arquivo] | Automação ou presunção de leitura integral |
| P04-LAC-004 | Conflito possível entre metadados de catálogos e folha de rosto/objeto material [mesmo arquivo] | Validação, até resolução — `VALIDACAO_PENDENTE` |
| P04-LAC-005 | P04 não define o schema afirmação–evidência do P05 [mesmo arquivo] | Integração futura — depende de P05 |
| LAC-P05-001 | Taxonomia definitiva de `claim_type` não fornecida pelo P04 [P05/08_REGISTRO_DE_LACUNAS_E_CONFLITOS_P05_R01.jsonl] | Expansão do vocabulário de `claim_type` sem revisão autorizada |
| LAC-P05-002 | Formato físico de persistência não definido [mesmo arquivo] | Qualquer escolha de banco/tecnologia — schema permanece lógico |
| LAC-P05-003 | Regra de agregação para múltiplas evidências depende do tipo de afirmação e finalidade futura [mesmo arquivo] | Agregação automática por contagem — proibida até regra explícita |
| CON-P05-001 | Estados do P04 e status mínimos do comando usam rótulos parcialmente diferentes [mesmo arquivo] | Unificação de nomenclatura — tratada por aliases, sem apagar distinções |
| CON-P05-002 | Risco de interpretar confiança como probabilidade de verdade [mesmo arquivo] | Uso de `confidence` como substituto de evidência — bloqueado por definição |

Regra geral repetida em P00: "Nenhuma lacuna poderá ser preenchida por inferência. Qualquer decisão exige autorização expressa do USUARIO_PROPONENTE." [P00/07_LACUNAS_NAO_INFERIVEIS_P00_R01.txt]

---

## 4. Discrepâncias do manifesto

### Discrepância 1 — P05 declarado "não iniciado", mas existente e executado
O manifesto da coleção declara: `"P05_P28": "NAO_INICIADOS"` [MANIFESTO_COLECAO_PACOTES_HOMOLOGADOS_P00_A_P04_R01.json]. Contudo, a pasta `PACOTE_SCHEMA_AFIRMACAO_EVIDENCIA_LLM_ACADEMICA_R01` (P05) está presente no corpus com 13 arquivos, incluindo schema, dicionário de dados, vocabulário de status, regras de coerência, matriz de suficiência e confiança, dois protocolos, registro de lacunas, teste de rastreabilidade (15 cenários aprovados) e diagnóstico final — todos com estado "EXECUTADO_DOCUMENTALMENTE" [P05/00_LEIA_PRIMEIRO.txt; P05/10_DIAGNOSTICO_FINAL_P05_R01.txt].

Nota de enquadramento conforme regra do enunciado: por ser P05 (dentro da leva P05–P28 ainda em produção pelo autor), esta discrepância pode refletir um estágio de trabalho em andamento no momento da consolidação do manifesto, e não necessariamente um erro de especificação. Registrada como fato observável, sem resolução.

### Discrepância 2 — P00 auto-contraditório dentro do próprio pacote
Ver seção 2 acima: P00 declara a si mesmo `NAO_HOMOLOGADO` em seu artefato interno, mas o manifesto de nível de coleção (que inclui o próprio P00 na lista de "componentes_incluidos") o declara `HOMOLOGADO_E_CONGELADO`.

### Discrepância 3 — pacotes P04 e P05 tratam antecessores como homologados
Como citado na seção 2: P04 declara "P00, P01, P02 E P03 HOMOLOGADOS E CONGELADOS" e P05 declara "P00, P01, P02, P03 e P04 homologados e congelados" em suas respectivas seções de `AUTORIDADE_CANONICA`/`BASES` [P04/00_LEIA_PRIMEIRO.txt; P05/00_LEIA_PRIMEIRO.txt], reforçando a versão "homologada" em vez da versão "não auditada/não homologada" que os próprios antecessores declaram sobre si mesmos em seus diagnósticos finais.

Nenhuma das três discrepâncias é resolvida nesta leitura, conforme instrução expressa do enunciado.

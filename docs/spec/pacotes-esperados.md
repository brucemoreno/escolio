# PACOTES ESPERADOS — INVENTÁRIO CANÔNICO DOS 29 COMPONENTES (P00–P28)

Fonte: `04_INVENTARIO_CANONICO_DE_COMPONENTES_R03.csv` [P00/04_INVENTARIO_CANONICO_DE_COMPONENTES_R03.csv], declarado no mapa de proveniência do P00 como cópia byte a byte de `02_INVENTARIO_DE_COMPONENTES_E_PACOTES_A_PRODUZIR_R03.csv` [P00/08_MAPA_DE_PROVENIENCIA_DOCUMENTAL_P00_R01.csv]. **Este arquivo lista os 29 componentes completos** (P00 a P28), confirmando que sim, os inventários trazem a lista integral planejada.

Um segundo arquivo, `05_INVENTARIO_CANONICO_DE_PACOTES_R03.csv`, lista objetos/pacotes já produzidos e sua classe de status (histórico de versões da R01/R02/R03 e materiais BVAA/CTX-GEO) — não é a lista dos 29 componentes futuros, é o registro de proveniência dos pacotes já existentes na cadeia R01→R03. Não foi usado para a tabela abaixo.

## Tabela — identificador, denominação, fase, camada, dependências, gate, saída esperada

Campos transcritos literalmente do CSV (colunas: id, fase, camada, componente_pacote, obrigatoriedade, estado_atual, dependencias_obrigatorias_explicitas, dependencias_condicionais_explicitas, condicao_de_ativacao, saida_esperada, validacao — colunas de responsáveis/executor/destinatário omitidas aqui por concisão, presentes na fonte).

| ID | Fase | Camada | Denominação | Obrigatoriedade | Estado atual (no CSV) | Dependências obrigatórias | Saída esperada | Validação |
|---|---|---|---|---|---|---|---|---|
| P00 | F0 | GOVERNANCA | Controle mestre e estado canônico | OBRIGATORIO | EXISTENTE; REVISAR SOMENTE COM AUTORIZACAO | NENHUMA | Estado, precedência, linha do tempo e inventário | AUDITORIA_DE_INTEGRIDADE |
| P01 | F0 | GOVERNANCA | Trava antideriva e reativação | OBRIGATORIO | EXISTENTE; CONSOLIDAR COM R02 | P00 | Trava, protocolo de restauro e resposta a comandos vagos | TESTE_DE_REATIVACAO |
| P02 | F1 | FUNCOES | Catálogo funcional consolidado | OBRIGATORIO | R01_DE_TRABALHO; NAO_HOMOLOGADO | P00; P01 | Funções, requisitos, limites, gates e saídas | AUDITORIA_FUNCIONAL |
| P03 | F2 | POLITICAS | Núcleo transversal obrigatório | OBRIGATORIO | A_PRODUZIR | P02 | Estados, gates, modularidade, proveniência e reversibilidade | TESTE_TRANSVERSAL |
| P04 | F2 | BIBLIOGRAFIA | BVAA universal e leitura efetiva | OBRIGATORIO | A_PRODUZIR | P03 | Estados de obra, leitura, página, validação e recomendação | TESTE_BIBLIOGRAFICO |
| P05 | F2 | EVIDENCIA | Schema afirmação–evidência | OBRIGATORIO | A_PRODUZIR | P04 | IDs, fonte, página, suficiência, confiança e status | TESTE_DE_RASTREABILIDADE |
| P06 | F2 | INTERVENCAO | Taxonomia universal de intervenção | OBRIGATORIO | A_PRODUZIR | P03 | Níveis de intervenção, permissões e gates | TESTE_DE_AUTORIZACAO |
| P07 | F2 | VOZ | Contrato de voz autoral | OBRIGATORIO | BASE_HISTORICA_EXISTENTE; CONSOLIDAR | P03 | Perfis, fidelidade, limites e avaliação | TESTE_DE_VOZ |
| P08 | F2 | SEGURANCA | Segurança documental, prompt injection e privacidade | OBRIGATORIO | A_PRODUZIR | P03 | Instruções internas, sigilo, retenção, acesso e privacidade | TESTE_ADVERSARIAL |
| P09 | F3 | CONTRATOS | Schemas de entrada, saída, erro e abstenção | OBRIGATORIO | A_PRODUZIR | P03; P04; P05; P06; P07; P08 | Contratos técnicos por função | VALIDACAO_DE_SCHEMA |
| P10 | F4 | FUNCAO | Derivação editorial de capítulo em artigos | OBRIGATORIO | REQUISITO_R01_EXISTENTE; DETALHAR | P02; P03; P04; P05; P06; P07; P08; P09 | Diagnóstico de núcleos, matriz de transposição e sobreposição | PILOTO_SUPERVISIONADO |
| P11 | F4 | FUNCAO | Revisão de dissertação e tese | OBRIGATORIO | BASE_HISTORICA_MADURA; CONSOLIDAR | P02; P03; P04; P05; P06; P07; P08; P09 | Fluxo modular, diagnóstico e auditoria | PILOTO_SUPERVISIONADO |
| P12 | F4 | FUNCAO | Revisão de relatório de iniciação científica | OBRIGATORIO | REQUISITO_R01_EXISTENTE; DETALHAR | P02; P03; P04; P05; P06; P07; P08; P09 | Proporcionalidade, formação e conformidade institucional | PILOTO_SUPERVISIONADO |
| P13 | F4 | FUNCAO | Comentários Word humanos e seletivos | OBRIGATORIO | PROMPT_FONTE_EXISTENTE; CONSOLIDAR | P02; P03; P04; P05; P06; P07; P08; P09 | Auditoria integral e comentários substantivos seletivos | PILOTO_WORD |
| P14 | F4 | FUNCAO | Incorporação de pareceres em artigo | OBRIGATORIO | PROMPT_FONTE_EXISTENTE; CONSOLIDAR | P02; P03; P04; P05; P06; P07; P08; P09 | Gates, matriz, revisão e carta aos pareceristas | PILOTO_EDITORIAL |
| P15 | F4 | PROFILES | Profiles temáticos canônicos | CONDICIONAL | V117_CONGELADA | P00; P02 | Seis profiles, sem expansão silenciosa | TESTE_DE_COMPATIBILIDADE |
| P16 | F4 | CONTEXTOS_GEOGRAFICOS | Módulos de contextos geográficos | CONDICIONAL | CTX_GEO_AP_PROSPECTADO; NENHUM_MODULO_AUTORIZADO | P00; P03; P09 | Contextos geográficos separados de profiles e períodos | AUDITORIA_CONTEXTUAL |
| P17 | F4 | CONTEXTOS_TEMPORAIS | Módulos de contextos temporais | CONDICIONAL | NAO_INICIADO | P00; P03; P09 | Contextos temporais separados de geografia e profiles | AUDITORIA_CONTEXTUAL |
| P18 | F4 | INTERSECOES | Regras de interseção espaço–tempo | CONDICIONAL | NAO_INICIADO | P16; P17 | Somente regras comprovadamente dependentes de espaço e tempo | AUDITORIA_DE_INTERSECAO |
| P19 | F5 | DADOS | Plano de dados e classificação de materiais | OBRIGATORIO | A_PRODUZIR | P02; P03; P04; P05; P08; P09; P10–P14 | Classificação de instruções, RAG, exemplos, testes e documentos | AUDITORIA_DE_DADOS |
| P20 | F5 | TESTES | Suíte de testes e gabaritos | OBRIGATORIO | R01_PARCIAL_EXISTENTE | P02–P14 | Testes funcionais, adversariais e de regressão | AUDITORIA_E_CONGELAMENTO |
| P21 | F5 | DADOS | Corpus supervisionado auditado | CONDICIONAL | NAO_AUTORIZADO | P19; P20 | Pares e exemplos aprovados, com licença e privacidade | AUDITORIA_DE_QUALIDADE |
| P22 | F6 | HANDOFF_REQUISITOS | Handoff de requisitos e governança ao engenheiro | OBRIGATORIO | NAO_INICIADO | P00–P14; P19; P20 | Requisitos, políticas, dados, testes, decisões abertas e exclusões | AUDITORIA_FINAL_DE_HANDOFF |
| P23 | F7 | ARQUITETURA | Comparativo e decisão de arquitetura técnica | OBRIGATORIO | NAO_INICIADO | P22 | Comparativo entre uma IA, modos, agentes e solução híbrida | DECISAO_AUTORAL |
| P24 | F8 | ESPECIFICACAO_TECNICA | Especificação técnica da solução | OBRIGATORIO | NAO_INICIADO | P23 | APIs, estados, ferramentas, logs, segurança e interface | REVISAO_DE_ENGENHARIA |
| P25 | F9 | IMPLEMENTACAO | Implementação mínima controlada | OBRIGATORIO | NAO_AUTORIZADA | P24 | Núcleo, roteador, gestor de fontes, uma função e logs | TESTES_DE_ACEITACAO |
| P26 | F10 | PILOTOS | Pilotos supervisionados | OBRIGATORIO | NAO_AUTORIZADO | P20; P25 | Resultados, logs, falhas, decisões e reversão | AUDITORIA_DUPLA |
| P27 | F11 | HANDOFF_FINAL | Entrega técnica final e aceite | OBRIGATORIO | NAO_INICIADO | P26 | Solução, documentação, testes, pilotos, limites e backlog | AUDITORIA_FINAL |
| P28 | F12 | OPERACAO | Operação, capacitação e manutenção | OBRIGATORIO_APOS_ACEITE | NAO_INICIADO | P27 | Capacitação do usuário, monitoramento, atualização e reversão | REVISAO_PERIODICA |

## O que já chegou vs. o que falta

**Chegaram nesta leva (R01, P00–P05):** P00, P01, P02, P03, P04, P05 — todos "EXECUTADO_DOCUMENTALMENTE" segundo seus próprios diagnósticos finais, nenhum ainda auditado ou homologado (ver `autoridade-e-lacunas.md` para a contradição com o manifesto de coleção).

**Faltam (P06–P28):** 23 componentes, conforme tabela acima. O estado_atual registrado no CSV para os que ainda não chegaram varia: alguns têm base histórica preexistente ainda não consolidada (P06 não tem essa nota; P07 "BASE_HISTORICA_EXISTENTE; CONSOLIDAR"; P11 "BASE_HISTORICA_MADURA; CONSOLIDAR"; P13/P14 "PROMPT_FONTE_EXISTENTE; CONSOLIDAR"; P15 "V117_CONGELADA"; P16 "CTX_GEO_AP_PROSPECTADO; NENHUM_MODULO_AUTORIZADO"); outros são "A_PRODUZIR" ou "NAO_INICIADO" sem base prévia.

## Correspondência entre lacuna encontrada nesta leitura e pacote futuro que a resolveria

| Lacuna encontrada em P00–P05 | Pacote futuro que a endereça, segundo o próprio inventário |
|---|---|
| Léxico, voz, marcas de oralidade (mencionadas no enunciado da Etapa 1 como ainda por vir) | P07 — Contrato de voz autoral |
| Taxonomia de intervenção / níveis de permissão para ações fortes (ex.: gates humanos citados em cada função de P02) | P06 — Taxonomia universal de intervenção |
| Segurança documental, prompt injection, privacidade (citada como lacuna geral em P00) | P08 — Segurança, prompt injection e privacidade |
| Schema de entrada/saída/erro/abstenção por função (LAC-P05... schema do P05 cobre apenas afirmação-evidência, não contratos completos) | P09 — Schemas de contratos técnicos |
| Detalhamento das seis funções de P02 aplicadas a casos concretos (P10–P14, cada uma referenciando sua função específica) | P10 (F01), P11 (F02), P12 (F03), P13 (F04), P14 (F05) |
| Profiles temáticos V117 (mencionados como "permanecem canônicos" em P00, mas conteúdo não presente) | P15 — Profiles temáticos canônicos |
| Contextos geográficos/temporais e interseções (mencionados em P00 como "permanecem separados") | P16, P17, P18 |
| Classificação de materiais/dados, incluindo BVAA e schema | P19 — Plano de dados |
| Suíte de testes definitiva (P02–P05 preservam apenas testes documentais próprios de cada componente) | P20 — Suíte de testes e gabaritos |
| Arquitetura técnica, plataforma, modelo, fornecedor (vetados em todos os pacotes lidos) | P23 — Comparativo e decisão de arquitetura técnica |
| Implementação (vetada em todos os pacotes lidos) | P25 — Implementação mínima controlada |

Nenhuma lista dos 29 componentes foi inferida por este mapeamento: a tabela acima é transcrição direta de `04_INVENTARIO_CANONICO_DE_COMPONENTES_R03.csv`.

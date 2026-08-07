# MAPA DA R03 — Protocolo-Mestre de Ação do Ecossistema LLM Acadêmica

Fonte: `corpus/handoff-P22/PACOTE_HANDOFF_REQUISITOS_ENGENHEIRO_LLM_R01/FONTES_CANONICAS/PACOTE_PROTOCOLO_MESTRE_ACAO_ECOSSISTEMA_LLM_ACADEMICA_R03/`,
lida integralmente nesta sessão (2026-08-07), na ordem declarada em `00_LEIA_PRIMEIRO.txt`
(arquivos 00 a 13). Os arquivos 14 e 15 (`.zip`, anexos de auditoria da R02) não foram lidos —
classificados pelo próprio pacote como documentação de proveniência, não fonte operacional.

Convenção de citação: `[R03 §N]` remete à numeração do arquivo 01 (`01_PROTOCOLO_MESTRE_...md`,
único arquivo com seções numeradas); `[R03 arquivo-NN]` remete a um dos outros doze arquivos por
número de ordem de leitura. Fidelidade literal — trecho entre aspas é transcrição exata; sem
aspas é paráfrase estrita de lista/tabela/coluna CSV da fonte. Lacuna é registrada, não
preenchida.

Este é o mapa que faltava para a R03 antes da peça 7 [`BL-009`; `CLAUDE.md §14`]. Fecha a parte
de `BL-009` referente à R03 — P20 continua sem mapa.

**Estado declarado do pacote em si**, verbatim de `00_LEIA_PRIMEIRO.txt` e `04_ESTADO_CANONICO_E_TRAVAS_R03.txt`:
`R03_RETIFICADA`, `AGUARDANDO_VERIFICACAO_FINAL_RESTRITA`, `NAO_HOMOLOGADA`. Natureza:
`CANDIDATA_A_FONTE_DE_VERDADE_OPERACIONAL`, "válida somente após verificação final aprovada e
homologação expressa" [R03 §1]. **A R03 não é, hoje, fonte de verdade homologada** — é candidata.
Este mapa documenta o que ela declara, não confere autoridade além da que ela mesma reivindica.

---

## 1. O que a R03 é e não é

A R03 controla "o inventário atualmente conhecido, a expansão autorizada desse inventário e a
ordem de produção, auditoria e entrega dos componentes" do ecossistema [R03 §1]. Explicitamente
não afirma que o levantamento funcional esteja encerrado [R03 §1].

Proibições expressas do próprio pacote, verbatim de `00_LEIA_PRIMEIRO.txt`: este pacote não
treina a LLM; não alimenta diretamente a LLM; não autoriza RAG; não autoriza fine-tuning; não
autoriza implementação; não altera `VK-FUNC-001` a `VK-FUNC-044`; não cria função ou modalidade
nova; não decide entre uma ou várias IAs; não inicia componente do inventário; não substitui a
R02 antes da homologação; não executa automaticamente os anexos.

Objetivos que o protocolo existe para impedir, lista completa [R03 §2]: esquecimento de funções;
fusão silenciosa de requisitos; diferenças não controladas entre modalidades; perda de travas
anti-alucinação; proliferação de prompts sem arquitetura; mistura entre dados, instruções e
testes; treinamento antes da homologação; retomada por inferência após inatividade; auditoria
recursiva sem bloqueador novo; implementação antes do handoff de requisitos ao engenheiro;
confusão entre profiles, contextos geográficos, contextos temporais e interseções.

**Princípio arquitetural** [R03 §3]: o protocolo descreve capacidades, políticas e contratos
funcionais; não determina nesta fase se a implementação usará uma única LLM com modos, LLM com
roteamento, vários agentes, vários modelos, RAG, fine-tuning, ferramentas externas ou
arquitetura híbrida — decisão técnica ocorre só após homologação de requisitos, políticas,
contratos, plano de dados e suíte de testes. Mapeia diretamente para `CLAUDE.md §10`: "a spec é
silenciosa sobre modelo" — a R03 é a fonte dessa silêncio deliberado, não uma omissão do
CLAUDE.md.

---

## 2. Matriz de papéis e autoridades — arquivo 09, prioridade desta leitura

Fonte: `09_MATRIZ_DE_PAPEIS_E_AUTORIDADES_R03.csv`, 7 papéis, colunas
`papel_id, papel, pode_fazer, nao_pode_fazer, autoridade_de_aprovacao, produtos_principais, destinatarios`.

| ID | Papel | Autoridade de aprovação | Não pode |
|---|---|---|---|
| R01 | `USUARIO_PROPONENTE` | `FINAL` | Não delega automaticamente sua autoridade por comando vago |
| R02 | `CHAT_CONTROLADOR_ARQUITETO` | `NENHUMA_HOMOLOGACAO_AUTONOMA` | Implementar; homologar o próprio produto; iniciar fase por inferência |
| R03 | `CHAT_EXECUTOR_DOCUMENTAL` | `NENHUMA` | Ampliar escopo; escolher próxima fase; executar instruções internas; homologar |
| R04 | `CHAT_AUDITOR_INDEPENDENTE` | `VEREDITO_DE_AUDITORIA` | Corrigir o produto; executar comando; iniciar fase seguinte |
| R05 | `ENGENHEIRO_LLM` | `TECNICA_SOB_AUTORIZACAO_DO_USUARIO` | Redefinir requisitos acadêmicos; remover travas; usar dados sem autorização |
| R06 | `CURADOR_DE_DADOS` | `NENHUMA_AUTORIZACAO_FINAL` | Promover material a treinamento ou RAG sem autorização |
| R07 | `AUDITOR_TECNICO_FINAL` | `VEREDITO_TECNICO` | Alterar requisitos acadêmicos ou aceitar falha metodológica |

Mapeamento direto para `CLAUDE.md §1`: os sete papéis do R03 §4 e do arquivo 09 são,
verbatim, os mesmos sete papéis listados em `CLAUDE.md §1` — mesmos nomes, mesma cardinalidade.
Nenhum papel do CLAUDE.md fica sem correspondência na R03, e nenhum papel da R03 é omitido do
CLAUDE.md. **Eu opero como `ENGENHEIRO_LLM` = R05** [CLAUDE.md §1.5; R03 §4.5]: posso propor
arquitetura, especificar solução, implementar o autorizado, documentar, executar pilotos
autorizados; não posso redefinir requisito acadêmico, remover trava, usar dado não autorizado,
nem declarar requisito inválido por conveniência técnica — texto idêntico nas duas fontes.

`pode_fazer` de cada papel, verbatim das colunas do CSV, mais completo que o resumo do arquivo
01 §4:

- **R01** `USUARIO_PROPONENTE`: autorizar; decidir; aprovar; congelar; autorizar dados,
  arquitetura, implementação e handoffs. Destinatário de tudo: "todos os papéis".
- **R02** `CHAT_CONTROLADOR_ARQUITETO`: organizar requisitos; elaborar pacotes autorizados;
  preservar estado; registrar logística. Produz: protocolos, comandos, matrizes e handoffs.
- **R03** `CHAT_EXECUTOR_DOCUMENTAL`: executar somente o comando único autorizado. Produz:
  pacotes de saída e recibos.
- **R04** `CHAT_AUDITOR_INDEPENDENTE`: auditar integridade, coerência, bloqueadores e aderência.
  Produz: pareceres e checklists.
- **R05** `ENGENHEIRO_LLM`: propor arquitetura; especificar; implementar; documentar; executar
  pilotos autorizados. Produz: arquitetura, especificação, implementação e entrega.
- **R06** `CURADOR_DE_DADOS`: classificar, anonimizar, licenciar, rastrear e separar materiais.
  Produz: plano de dados e corpus auditado.
- **R07** `AUDITOR_TECNICO_FINAL`: verificar implementação, segurança, testes, pilotos e
  regressões. Produz: relatórios técnicos de aceite.

### 2.1. "Autoridade competente pelo objeto" — busca negativa, confirmando `mapa-P08.md §5`

O `docs/spec/mapa-P08.md §5` já registrava que nenhuma seção do P08 nomeia qual papel do
`CLAUDE.md §1` corresponde a "autoridade competente pelo objeto" citada em `[P08 §3.6, §5.6,
§11.4, §13.6]`, e apontava a R03 — então sem mapa — como candidata a preencher essa ligação.

**Resultado desta leitura: a lacuna não é preenchida pela R03.** Nem o arquivo 01 §4 (papéis e
autoridades, prosa) nem o arquivo 09 (matriz CSV) usam a expressão "autoridade competente pelo
objeto" ou equivalente. O que a R03 define é genérico por papel (quem pode aprovar o quê no
fluxo do próprio protocolo — homologação, veredito de auditoria, veredito técnico), não
por-objeto (qual autoridade decide sobre este documento, este incidente, esta obra específica).
`P08 §3.6/§5.6/§11.4/§13.6` fala de decisão ligada ao **objeto em questão** (um documento, um
incidente, uma retenção), não de autoridade de fase do protocolo mestre — são perguntas
diferentes, e a R03 só responde a segunda.

A leitura mais provável, já registrada em `mapa-P08.md §5`, permanece a melhor disponível:
`USUARIO_PROPONENTE` (R01) é o candidato natural, dado que `autoridade_de_aprovacao=FINAL` e
"nenhum outro papel pode substituir sua decisão" [R03 §4.1] — mas isso é inferência minha sobre
autoridade de fase aplicada por analogia a autoridade de objeto, não afirmação literal de
nenhuma das duas fontes. **Continua lacuna de spec**, agora confirmada por ausência em duas
fontes (P08 e R03), não apenas uma. Não inventar a ligação; registrar em `LACUNAS.md` se/quando
o roteador de função (`escolio/funcoes/`) precisar decidir "quem decide sobre este objeto" em
caso concreto.

---

## 3. As seis camadas de funções — B — e a relação com `CLAUDE.md §3`

Funções registradas na "R01 de trabalho" [R03 §5, CAMADA B], lista completa, idêntica em
substância às seis do `CLAUDE.md §3` (P10–P14, X01):

1. derivação editorial de capítulo de tese ou dissertação em artigos, condicionada à existência
   de núcleos publicáveis autônomos (= P10);
2. revisão e correção de dissertação ou tese (= P11);
3. revisão de relatório de iniciação científica (= P12);
4. revisão em comentários Word, humana e seletiva (= P13);
5. análise e incorporação de pareceres em artigo (= P14);
6. gestão transversal de fontes, citações e suficiência de evidência (= X01).

**Funções candidatas, não incorporadas automaticamente** [R03 §5, CAMADA B], lista completa:

- revisão de artigo antes da submissão;
- incorporação de comentários de qualificação ou defesa;
- auditoria bibliográfica e documental autônoma;
- revisão de projeto de pesquisa ou proposta de financiamento.

Confirma e amplia `CLAUDE.md §13.4`: "revisão de artigo antes da submissão" já constava como
candidata não incorporada, citando `[R03 CAMADA B]` — a fonte agora lida confirma o texto
exato e revela **três outras candidatas que o CLAUDE.md não lista**: incorporação de
comentários de qualificação/defesa; auditoria bibliográfica e documental autônoma; revisão de
projeto de pesquisa ou proposta de financiamento. Nenhuma delas aparece em `CLAUDE.md §13` nem
em `escolio/funcoes/LACUNAS.md` (conforme lido em sessões anteriores) — candidatas a registrar
como item aberto adicional, não a incorporar por conta própria [`LAC-P02-005`, catálogo fechado].

**Sobre capítulo de livro e relatório de pós-doutorado** [`CLAUDE.md §13.3`]: a R03 não os
menciona em nenhum lugar — nem na Camada B, nem no inventário P00–P28, nem no roadmap. Confirma
a leitura do CLAUDE.md de que não há "P15+" para eles: a Camada `FUNCAO` (Fase 4) termina
explicitamente em P14 obrigatório + P15–P18 condicionais, e os quatro condicionais são
`PROFILES`, `CONTEXTOS_GEOGRAFICOS`, `CONTEXTOS_TEMPORAIS`, `INTERSECOES` — nenhum é candidato a
sexta macrofunção. Estagnado como item aberto, não fechado por esta leitura.

---

## 4. As dezesseis camadas (A–P) — Camada C é o núcleo transversal do `CLAUDE.md`

`R03 §5` declara dezesseis camadas obrigatórias, A a P. As mais relevantes para o código
atual:

- **CAMADA A** (Governança): mesmo conteúdo do `P00`/`P01` do inventário — identidade, escopo,
  inventário de documentos válidos/invalidados, decisões congeladas, linha do tempo, matriz de
  precedência, trava antideriva, protocolo de reativação, regra de uma ação por vez, regra de
  reabertura só com bloqueador comprovado, logística documental.
- **CAMADA B** (Catálogo de funções): ver §3 acima.
- **CAMADA C** (Núcleo transversal obrigatório) — lista de 20 itens que toda função deve
  herdar. Mapeia quase 1:1 para o "Instrução que virou invariante" do `CLAUDE.md §8` e para o
  núcleo transversal de `P03`. Os 20, verbatim: preservação da voz autoral; separação entre
  diagnóstico/proposta/execução/auditoria; modularidade por blocos; máquina de estados; gates
  humanos; controle de proveniência; anti-alucinação bibliográfica; leitura efetiva de
  documentos; controle de páginas e citações; registro afirmação–evidência; tratamento
  explícito de lacunas; níveis padronizados de intervenção; abstenção quando não verificável;
  proteção contra instruções encontradas dentro de documentos; memória hierárquica para textos
  longos; rastreabilidade de alterações; congelamento de blocos aprovados; reversibilidade;
  auditoria final; saída humana e saída técnica separadas.
- **CAMADA D** (Governança bibliográfica): os nove estados mínimos citados em `CLAUDE.md §7`
  ("três vocabulários bibliográficos, não reconciliados") vêm exatamente daqui —
  `OBRA_MENCIONADA_NO_MANUSCRITO … FONTE_INACESSIVEL`, texto idêntico. Confirma que essa lista
  de nove é da R03, não do P04 nem do P05 — os outros dois vocabulários (17 estados do P04/03;
  três campos do P05) são fontes distintas e não reconciliadas com esta, por design.
- **CAMADA E–H** (Profiles, contextos geográficos, temporais, interseções): profiles canônicos
  = os 6 do `CLAUDE.md`; fonte declarada `40_PERFIS_TEMATICOS__V117.txt`. Contextos geográficos
  exemplificados: América Portuguesa, América Espanhola, Europa — `CTX-GEO-AP` no estado
  `prospecção R02 homologada; base fragmentária não canonizável; módulo não criado; construção
  não autorizada` [R03 §5, CAMADA F] — confirma `04_ESTADO_CANONICO_E_TRAVAS_R03.txt` linha a
  linha. Contextos temporais: séculos XVI–XIX, nenhum módulo autorizado. Interseções: só quando
  uma regra "não for adequadamente geográfica" nem "adequadamente temporal" e depender
  comprovadamente da combinação — nunca para fundir F e G prematuramente.
- **CAMADA I** (Contratos de entrada/saída): pré-figura o `P09` — mesma lista de saídas técnicas
  mínimas que hoje aparece em `escolio/contrato/` (estado, bloco, ID, proveniência, alteração,
  justificativa, fonte, localização, nível de intervenção, confiança, pendência, decisão
  humana).
- **CAMADA J** (Dados): as seis categorias (`INSTRUCOES_E_POLITICAS`, `BASE_DE_CONHECIMENTO_RAG`,
  `EXEMPLOS_SUPERVISIONADOS`, `TESTES_E_GABARITOS`, `DOCUMENTOS_DO_USUARIO_EM_PROCESSAMENTO`,
  `LOGS_E_REGISTROS_DE_AUDITORIA`) são a fonte-mãe da taxonomia de `material_type` do P19 §17
  citada em `CLAUDE.md §3` (`INSTRUCOES`, `POLITICAS`, `DOCUMENTOS_DO_USUARIO`, …) — o P19
  refina/renomeia a Camada J, não a substitui.
- **CAMADA K** (Exemplos supervisionados): confirma `CLAUDE.md §9` — bloqueado até homologação
  das funções, congelamento da suíte de testes, decisão de privacidade, decisão de licença,
  autorização autoral. Texto idêntico.
- **CAMADA L** (Testes): as 14 categorias mínimas de teste (funcional, adversarial, regressão,
  voz, bibliografia, página, prompt injection em documentos, memória longa, contradição,
  abstenção, sobreposição entre artigos, comentários excessivos, pareceres conflitantes,
  operação sem material obrigatório) — candidatas a cruzar contra `escolio/` na hora de mapear
  P20 (`BL-009`, ainda sem mapa próprio).
- **CAMADA M** (Handoff ao engenheiro) = P22, primeiro handoff, ocorre **antes** da decisão
  arquitetural. Este documento (docs/spec/mapa-R03.md) é lido a partir de dentro de
  `PACOTE_HANDOFF_REQUISITOS_ENGENHEIRO_LLM_R01` — ou seja, **eu (`ENGENHEIRO_LLM`) sou o
  destinatário declarado deste próprio handoff**, e o handoff em si (P22) segue
  `NAO_INICIADO` no registro de proveniência (arquivo 08) — a R03 que estou lendo é ela mesma
  ainda candidata, dentro de um pacote que se autodeclara não homologado.
- **CAMADA N** (Arquitetura e especificação técnica) = P23/P24 — só depois do handoff.
- **CAMADA O** (Implementação e pilotos) = P25/P26.
- **CAMADA P** (Entrega final e manutenção) = P27/P28. `"CAPACITACAO_DO_USUARIO" não significa
  "TREINAMENTO_DA_LLM"` [R03 §5, CAMADA P] — distinção explícita, relevante para não confundir
  documentação de operação com corpus de treino (mesmo espírito de `CLAUDE.md §9`,
  "É contexto por execução, não treinamento").

---

## 5. Inventário P00–P28 — fases, dependências, responsáveis

Fonte: `02_INVENTARIO_DE_COMPONENTES_E_PACOTES_A_PRODUZIR_R03.csv` (29 componentes, 23 colunas)
e `03_MATRIZ_DE_DEPENDENCIAS_GATES_E_SAIDAS_R03.csv` (13 fases, colunas
`fase, objeto, componentes_obrigatorios, componentes_condicionais, dependencias_obrigatorias_explicitas, dependencias_condicionais_explicitas, pre_condicao, operacao, gate_humano, saida, condicao_interrupcao`).

**Regra de dependências, verbatim [R03 §7]**: "é proibido representar dependências por faixas
abreviadas entre identificadores, por expressões como 'do primeiro ao último componente' ou por
notação que não permita determinar, sem interpretação, cada dependência individual." — cada
componente do arquivo 02 lista toda dependência por P-ID explícito, nunca "P03–P08".

### Fases e componentes

| Fase | Objeto | Obrigatórios | Condicionais |
|---|---|---|---|
| F0 | Estado e governança | P00, P01 | — |
| F1 | Catálogo funcional | P02 | — |
| F2 | Políticas transversais | P03, P04, P05, P06, P07, P08 | — |
| F3 | Contratos e schemas | P09 | — |
| F4 | Funções especializadas | P10, P11, P12, P13, P14 | P15, P16, P17, P18 |
| F5 | Plano de dados e testes | P19, P20 | P21 |
| F6 | Handoff de requisitos | P22 | P15–P18 (se cobertos por P19/P20), P21 (se autorizado) |
| F7 | Decisão arquitetural | P23 | — |
| F8 | Especificação técnica | P24 | — |
| F9 | Implementação mínima | P25 | — |
| F10 | Pilotos supervisionados | P26 | — |
| F11 | Entrega técnica final | P27 | — |
| F12 | Operação e manutenção | P28 | — |

Regra explícita sobre condicionais, repetida em três lugares (arquivo 01 §6, arquivo 02, arquivo
03): "um componente condicional não ativado não bloqueia P19 ou P20"; "um componente condicional
ativado não pode alcançar P22 sem estar coberto pelo plano de dados P19 e pela suíte de testes
P20." Aplica-se hoje: nenhum de P15–P18 foi ativado (ver §4, Camadas E–H) — logo P19/P20/P22 não
são bloqueados por eles, mas se qualquer um for ativado no futuro, P19 e P20 têm que ser
atualizados antes de P22 poder avançar.

### Matriz completa do arquivo 03 — dependências, pré-condição e operação por fase

O arquivo 03 tem 11 colunas; a tabela de fases acima só reproduziu quatro
(`fase, objeto, componentes_obrigatorios, componentes_condicionais`). As demais, por fase,
verbatim:

| Fase | Dependências obrigatórias explícitas (por componente da fase) | Dependências condicionais explícitas | Pré-condição | Operação |
|---|---|---|---|---|
| F0 | P00: nenhuma; P01: P00 | nenhuma | Pacotes de base disponíveis | Consolidar estado e trava |
| F1 | P02: P00; P01 | nenhuma | Governança homologada e levantamento funcional suficientemente completo | Consolidar funções históricas, novas e candidatas |
| F2 | P03: P02; P04: P03; P05: P04; P06: P03; P07: P03; P08: P03 | nenhuma | P02 homologado | Produzir e auditar políticas comuns |
| F3 | P09: P03; P04; P05; P06; P07; P08 | nenhuma | Todas as políticas F2 homologadas | Formalizar entradas, saídas, erros e abstenção |
| F4 | P10: P02;P03;P04;P05;P06;P07;P08;P09 — mesma lista para P11, P12, P13, P14; P15: P00;P02; P16: P00;P03;P09; P17: P00;P03;P09; P18: P16;P17 | P15/P16/P17/P18, cada um "quando ativado" | P09 homologado; condicionais somente quando ativados | Detalhar e auditar cada função separadamente |
| F5 | P19: P02;P03;P04;P05;P08;P09;P10;P11;P12;P13;P14; P20: mesma lista + P06;P07; P21: P19;P20 | P19 e P20, cada um: P15/P16/P17/P18 quando ativado | Funções obrigatórias e políticas homologadas; cada módulo condicional ativado homologado | Classificar materiais e congelar testes antes de exemplos supervisionados |
| F6 | P22: P00;P01;P02;P03;P04;P05;P06;P07;P08;P09;P10;P11;P12;P13;P14;P19;P20 | P22: P15/P16/P17/P18 quando ativado e coberto por P19/P20; P21 quando autorizado e auditado | Pacotes obrigatórios homologados; condicionais cobertos por dados e testes | Consolidar requisitos e transferir ao engenheiro |
| F7 | P23: P22 | nenhuma | Handoff de requisitos recebido | Comparar alternativas técnicas |
| F8 | P24: P23 | nenhuma | Arquitetura escolhida | Especificar solução |
| F9 | P25: P24 | nenhuma | Especificação técnica aprovada e implementação autorizada | Desenvolver núcleo e uma função piloto |
| F10 | P26: P20;P25 | nenhuma | MVP e suíte de testes disponíveis | Executar uma função por ciclo |
| F11 | P27: P26 | nenhuma | Pilotos aplicáveis homologados | Consolidar entrega e aceite |
| F12 | P28: P27 | nenhuma | Aceite formal | Capacitar usuário e operar versão controlada |

Nota sobre F4: a lista de dependências obrigatórias na coluna do arquivo 03 é redundante com o
arquivo 02 (mesmos P-IDs, por componente) — reproduzida aqui só porque a pergunta pediu a
matriz completa; não é informação nova além do §5 acima, é a mesma informação vista pela lente
de "fase" em vez de "componente". A única coisa que o arquivo 03 acrescenta ao arquivo 02 é a
coluna `pre_condicao`/`operacao`, que amarra cada fase a uma frase de estado-de-entrada e uma
frase de ação — nível de abstração que o arquivo 02 (por componente) não tem.

### Gate humano por fase — resposta ao segundo pedido da mensagem original (matriz de gates)

Coluna `gate_humano` do arquivo 03, por fase, texto exato:

| Fase | Gate humano |
|---|---|
| F0 | Homologar governança |
| F1 | Aprovar catálogo |
| F2 | Aprovar cada política |
| F3 | Aprovar schemas |
| F4 | Aprovar um componente por vez |
| F5 | Autorizar dados, privacidade e eventual P21 |
| F6 | Autorizar transferência |
| F7 | Escolher arquitetura |
| F8 | Aprovar especificação |
| F9 | Autorizar implementação |
| F10 | Autorizar cada piloto |
| F11 | Aceitar ou rejeitar solução |
| F12 | Aprovar política de manutenção |

**Relevante para `CLAUDE.md §4`** ("Gates não moram todos no E5 — e nenhum contrato diz onde
moram" / "as listas de gates e de fluxo modular são disjuntas"): a matriz de gates da R03 é
**por fase do protocolo-mestre** (F0–F12, produção de componentes P00–P28), não por etapa da
espinha E1–E7 de execução de uma função sobre um documento real. São eixos ortogonais — F0–F12
governa a *produção da própria spec*; E1–E7 governa a *execução de uma função já homologada*
contra um documento. A R03 não resolve `LAC-FUNC-007` (nenhum dos 91 gates funcionais tem
posição declarada nas 25–32 etapas de cada função) porque nunca tratou desse nível de
granularidade — seus 13 gates são golpes de aprovação de fase do inventário, um por fase, sempre
do `USUARIO_PROPONENTE` (ver `autoridade_aprovacao` = `USUARIO_PROPONENTE` em toda linha do
arquivo 02). **Confirma, não resolve, `LAC-FUNC-007`.**

### Condição de interrupção por fase

Coluna `condicao_interrupcao`, texto exato, por fase — útil como checklist de regressão:

F0 "Divergência documental" · F1 "Função omitida, fundida ou sem proveniência" · F2 "Regra
ausente, contraditória ou não testável" · F3 "Campo essencial ausente" · F4 "Deriva entre
modalidades ou mistura entre profile, espaço e tempo" · F5 "Material sem proveniência, licença,
teste ou cobertura de módulo ativado" · F6 "Pendência bloqueante, ausência de auditoria ou
módulo condicional sem cobertura" · F7 "Prematuridade técnica ou remoção de requisito" · F8
"Trava não implementável sem decisão autoral" · F9 "Falha de segurança ou ausência de logs" ·
F10 "Falha crítica ou corpus não autorizado" · F11 "Pendência técnica ou acadêmica bloqueante" ·
F12 "Regressão, incidente ou mudança não autorizada".

### Responsáveis por componente (arquivo 02)

Padrão dominante: `CHAT_CONTROLADOR_ARQUITETO` elabora, `CHAT_AUDITOR_INDEPENDENTE` audita,
`USUARIO_PROPONENTE` aprova, `CHAT_EXECUTOR_DOCUMENTAL` executa, `ENGENHEIRO_LLM` é
destinatário — para P00–P20, P22. **Excertos que rompem o padrão:**

- **P19, P21** — elaboração e execução por `CURADOR_DE_DADOS`, não pelo controlador/executor.
- **P20** — destinatário é `AUDITOR_TECNICO_FINAL; ENGENHEIRO_LLM` (dois papéis, não um).
- **P23 em diante (F7–F12)** — a partir da decisão arquitetural, responsável de elaboração e
  execução passa a ser `ENGENHEIRO_LLM` (não mais controlador/executor), auditoria passa a
  `AUDITOR_TECNICO_FINAL` (P24 em diante) ou dupla `CHAT_AUDITOR_INDEPENDENTE` +
  `AUDITOR_TECNICO_FINAL` (P26). Marca a transição de fase documental (papéis de chat) para
  fase de engenharia (meu papel operacional).

Este mapa não reproduz as 23 colunas completas do arquivo 02 por componente — ele já existe na
fonte e não deve ser duplicado aqui; ver arquivo original para nome canônico futuro do pacote,
pasta de arquivamento, condição de transferência, retorno esperado por P-ID.

---

## 6. Registro principal de pacotes (arquivo 10) — status e precedência

23 registros (`PKG-001` a `PKG-023`), cada um com hash SHA-256 (exceto o próprio pacote R03, que
recebe hash só após geração — `HASH_EXTERNO_CALCULADO_APOS_GERACAO`). Classes de status
encontradas, todas distintas:

- `CANDIDATO_NAO_HOMOLOGADO` — a própria R03 (PKG-001).
- `VERSAO_ANTERIOR_NAO_HOMOLOGADA_PRESERVAR` — R02 (PKG-002): "retificada pela R03, mas não
  apagar."
- `REGISTRO_DE_AUDITORIA_VALIDO` — pacotes de parecer/auditoria (PKG-003, PKG-005, PKG-017):
  "usar somente como parecer e evidência", nunca executar.
- `VERSAO_HISTORICA_NAO_HOMOLOGADA` — R01 (PKG-004): "auditado e reprovado para correção."
- `RASCUNHO_FUNCIONAL_VALIDO_NAO_HOMOLOGADO` — especificação funcional R01 (PKG-006): "usar
  para levantamento; não treinar nem implementar" — fonte de trabalho subordinada ao futuro
  P02 homologado.
- `CONTROLE_TRANSVERSAL_VALIDO` / `PACOTE_DE_RESTAURACAO_VALIDA` / `FONTE_DE_RESTAURACAO_VALIDA`
  — pacotes de trava/reativação (PKG-007 a PKG-010).
- `FONTE_CANONICA_VALIDA` — base V126 e arqueologia funcional (PKG-011), a mesma
  `MEGA_PROMPT_V126__KIT_COMPLETO` citada como `BASE_OPERACIONAL` em
  `04_ESTADO_CANONICO_E_TRAVAS_R03.txt`.
- `FONTE_CANONICA_CONGELADA` — profiles V117 (PKG-013): "usar sem ampliar silenciosamente."
- `FONTE_ARQUITETURAL_VALIDA` / `FONTE_DE_ESTADO_VALIDA` — arquitetura modular e pendências
  históricas (PKG-014, PKG-015).
- `OBJETO_PROSPECTADO_VALIDO`, `HOMOLOGACAO_VALIDA_CONGELADA`, `CONTROLE_ANTIDERIVA_VALIDO` —
  cadeia CTX-GEO-AP (PKG-016, PKG-018, PKG-019): confirma, com hash, o mesmo estado descrito no
  arquivo 04 e na Camada F.
- **`INVALIDADO_REGISTRO_DE_DERIVA`** — dois pacotes (PKG-020, PKG-021): "não possui autoridade
  operacional" / "não possui autoridade arquitetural"; preservados só como registro histórico
  do erro. PKG-021 é notável: "confundiu profiles temáticos com contextos histórico-geográficos"
  — exatamente o tipo de mistura que a Camada H (interseções) existe para impedir (§4 acima).
- **`STATUS_CANONICO_NAO_COMPROVADO_USO_BLOQUEADO`** — PKG-022: "não foi identificado como
  pacote válido no estado restaurado"; "não executar; preservar até decisão explícita." Esta é
  a classe operacional citada em `R03 §8`: "pacote com status não comprovado permanece
  preservado, mas com uso bloqueado" — distinta de invalidado (que teve autoridade e a perdeu)
  e de substituído (que foi superado em ciclo regular).
- `VERSAO_HISTORICA_SUBSTITUIDA` — PKG-023: prospecção CTX-GEO-AP R01, substituída pela R02.

**Regra geral [R03 §8]**: "pacote invalidado não pode ser usado para decisão arquitetural ou
continuidade"; "um anexo aninhado não substitui esse registro" — ou seja, os arquivos 14/15
(zips de auditoria da R02, não lidos por instrução) nunca teriam autoridade sobre o que consta
no arquivo 10, mesmo se lidos.

---

## 7. Checklists, decisões e proveniência — arquivos 06–08, 11–13

- **Arquivo 06** (`CHECKLIST_MODELO_DE_COMPLETUDE_R03.csv`) — 25 critérios `C01`–`C25`,
  todos `OBRIGATORIO`, todos com colunas `status/evidencia/observacao` **vazias** nesta versão
  — é o modelo de verificação a aplicar na próxima auditoria, não uma auditoria já feita.
- **Arquivo 07** (`CHECKLIST_DE_RETIFICACAO_FINAL_R03_PREENCHIDO.csv`) — este sim preenchido:
  os quatro `FINAL-BLOQ-01..04` marcados `RETIFICADO`; quatro itens de regressão (`REGRESSAO-01
  a 04`) marcados `PRESERVADO`; um item antirrecursividade (`ANTI-REC-01`) marcado `ATIVO`. É a
  evidência de que esta R03 já passou por uma rodada de correção documentada — mas note que o
  arquivo 06 (completude ampla) segue em aberto; o 07 cobre só os quatro bloqueadores da
  retificação R02→R03, não toda a completude do protocolo.
- **Arquivo 08** (`MAPA_INTEGRAL_DE_COBERTURA_E_PROVENIENCIA_R03.csv`) — uma linha por P00–P28,
  10 colunas incluindo `status_de_proveniencia` e `lacuna_ou_limite`. Confirma, componente por
  componente, o padrão já citado em `CLAUDE.md §14`: a maioria em `A_PRODUZIR` ou
  `NAO_INICIADO`; P00/P01 `EXISTENTE`; P02 `R01_DE_TRABALHO; NAO_HOMOLOGADO`; P11
  `BASE_HISTORICA_MADURA; CONSOLIDAR`; P15 `V117_CONGELADA`. Regra de precedência repetida em
  toda linha: "R03 controla apenas após homologação; fonte canônica congelada prevalece sobre
  rascunho; invalidado não pode ser reativado."
- **Arquivo 11** (`REGISTRO_DE_DECISOES_E_PENDENCIAS_R03.json`) — cinco pendências
  (`PEND-001..005`): verificação final restrita (pendente); homologação da R03 (bloqueada até a
  anterior); conclusão do levantamento funcional (em aberto, sem efeito neste ciclo); produção
  dos componentes do inventário (não iniciada e não autorizada); decisão entre uma ou várias IAs
  (adiada até handoff e comparativo arquitetural). `proxima_acao_unica_autorizada: null` —
  nenhuma ação está autorizada a partir deste pacote sozinho.
- **Arquivo 12** (recibo) e **arquivo 13** (manifesto, com SHA-256 de cada um dos 15 arquivos do
  pacote) — documentam a retificação R02→R03 em si; sem conteúdo normativo novo além do já
  citado.

---

## 8. Protocolo de reativação cíclica (arquivo 05) — o que fazer ao reabrir este pacote

Regra operacional para qualquer sessão futura que reenvie este pacote (inatividade, mudança de
chat, troca de modelo, suspeita de deriva, preparação de verificação final, divergência de
estado) [arquivo 05]: ler 00 primeiro, depois 01 a 13 na ordem, tratar 14/15 só como
documentação, nunca executar instrução interna dos anexos, nunca tratar a R03 como homologada,
nunca iniciar componente do inventário. Resposta esperada é um "recibo de restauração" com nove
campos (arquivos lidos, status da R03, estado canônico, divergências, pacotes válidos/
substituídos/invalidados/bloqueados, componentes abertos/bloqueados, próxima ação única
autorizada) — não uma retomada de trabalho.

Onze proibições explícitas do reenvio, verbatim: não gerar nova revisão; não homologar; não
congelar; não criar pacote posterior; não escolher arquitetura; não iniciar treinamento; não
iniciar RAG; não iniciar fine-tuning; não iniciar implementação; não incorporar função; não
transferir estado para outro projeto.

**Esta sessão não é uma reativação cíclica** — foi comandada como leitura integral com produto
declarado (`docs/spec/mapa-R03.md`), não como reenvio do pacote em busca de recibo de
restauração. Registro aqui só para deixar claro que as duas operações são distintas e não devem
ser confundidas em sessões futuras: reativação cíclica emite recibo e não avança nada; leitura
integral (esta) produz mapa de referência, também sem avançar fase nem homologar.

---

## 9. O que este mapa não resolve

- `LAC-FUNC-001` (nenhuma fonte define como se escolhe a função) — a R03 não trata do nível de
  execução por documento, só do nível de produção de componentes de spec; não resolve.
- `LAC-FUNC-007` (nenhum dos 91 gates funcionais tem posição nas etapas) — confirmado no §5
  acima como eixo ortogonal ao que a R03 resolve; não resolve.
- `mapa-P08.md §5` (nenhuma fonte liga papel a "autoridade competente pelo objeto") — buscado
  explicitamente no arquivo 09 e não encontrado (§2.1 acima); a lacuna permanece, agora
  confirmada contra duas fontes em vez de uma.
- Três candidatas novas a função (comentários de qualificação/defesa; auditoria bibliográfica
  autônoma; revisão de projeto/proposta de financiamento) aparecem na R03 e não em
  `CLAUDE.md §13` nem em `escolio/funcoes/LACUNAS.md` — registradas em §3 acima; decisão de
  incorporar cada uma ao rol de itens abertos do CLAUDE.md é do `USUARIO_PROPONENTE`, não desta
  leitura.
- P20 continua sem mapa próprio [`BL-009`] — a Camada L (§4 acima) dá as 14 categorias mínimas
  de teste da R03, mas o P20 em si (suíte real, "R01 parcial existente") não foi lido nesta
  sessão; fora do escopo desta tarefa.

Nenhum código foi escrito ou alterado nesta sessão — leitura e documentação apenas, por
instrução explícita.

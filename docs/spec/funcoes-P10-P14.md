# Funções P10–P14 — leitura e mapeamento

Fonte: `corpus/handoff-P22/PACOTE_HANDOFF_REQUISITOS_ENGENHEIRO_LLM_R01/FONTES_CANONICAS/`.
Nenhum pacote de política/governança (P00–P09, P22) foi reaberto nesta sessão;
citados apenas onde os próprios contratos de função os referenciam.

Convenção de citação: `[P10]`…`[P14]` remete ao arquivo homologado da respectiva
função. Números de seção (`§n`) referem-se à numeração interna de cada contrato,
que não é comparável entre funções (cada arquivo tem sua própria contagem `§1…§N`).

---

## P10 — Derivação Editorial de Capítulo em Artigos

`PACOTE_FUNCAO_AVALIACAO_CRITICA_PROJETOS_R01/P10_CONTRATO_FUNCIONAL_DERIVACAO_CAPITULO_ARTIGOS_HOMOLOGADO_R01.md`

### 1. O que faz

Avalia se um capítulo, seção extensa ou conjunto textual **academicamente
estabilizado** contém núcleo(s) publicável(is) autônomo(s) para artigos ou
produtos editoriais derivados `[P10 §2]`. Não resume, não divide mecanicamente,
não gera artigo automaticamente, não converte extensão em número de
publicações `[P10 §2]`.

Entrada: material integral de origem, `project_id`, versão, sumário/arquitetura
da obra, função do capítulo, problema/objetivo/argumento, bibliografia, fontes
documentais, estado de estabilização, finalidade editorial, dependências
P02–P09 com evidência verificada `[P10 §6.1]`. Para a matriz: núcleos
candidatos, testes de autonomia, decisão humana, material compartilhado/residual
`[P10 §6.2]`. Para redação: matriz aprovada, arquitetura aprovada, autorização
expressa, perfil de voz, nível P06 `[P10 §6.3]`.

Saída: cartografia, diagnóstico de núcleos, teste de autonomia, veredito de
viabilidade editorial, matriz de transposição, matriz de sobreposição,
arquitetura do produto derivado `[P10 §2, §27.3]`.

Execução bem-sucedida (critério global, `[P10 §38]`): P02–P09 preservados;
envelope P09 integralmente usado; fissão permanece humana; matriz precede
redação; material instável tratado corretamente; material residual não
promovido automaticamente; sobreposição diagnosticada sem bloquear
indevidamente o diagnóstico; insuficiência bibliográfica/autoridade produz
abstenção; proibição expressa produz recusa; bloqueio exige impedimento
material e evidência verificada.

### 2. Etapas e ordem

Síntese funcional obrigatória `[P10 §4.4]`:

```text
VAQUITA_ESTABILIZA
BALEIA_DERIVA
KOMODO_AVALIA
USUARIO_DECIDE_E_HOMOLOGA
```

Redação modular, ordem padrão `[P10 §21]`:
corpo analítico → verificação de fidelidade → estabilização local → módulo
seguinte → transições → introdução → conclusão → título/resumo/palavras-chave →
verificação de sobreposição → validação independente.

Invariante de ordem: sem núcleo publicável não há redação; sem matriz aprovada
não há redação `[P10 §3.5-6]`. Ordem imposta é método — a fissão não pode ser
executada antes da matriz aprovada em nenhuma circunstância.

### 3. Gates

`[P10 §29]` — três classes:

- **Automaticamente verificáveis** (não autorizam execução por si): campos
  obrigatórios, correspondência de IDs, integridade de versões.
- **Decisão humana expressa**: `GATE_DE_ESCOLHA_DE_NUCLEO`, `GATE_DE_FISSAO`,
  `GATE_DE_MATRIZ`, `GATE_DE_ARQUITETURA`, `GATE_DE_REDACAO`,
  `GATE_DE_EXPANSAO_RESIDUAL`, `GATE_DE_INTERVENCAO_FORTE`,
  `GATE_DE_HOMOLOGACAO`.
- **Validação documental** (não liberáveis autonomamente):
  `GATE_DE_ATIVACAO_P10`, `GATE_DE_ESTABILIDADE`, `GATE_DE_DIAGNOSTICO`,
  `GATE_DE_VALIDACAO`.

Regra geral: gate satisfeito não é autorização universal para etapas
posteriores `[P10 §29.4]`. Quem autoriza fissão/escolha de núcleo/expansão
residual: `USUARIO_PROPONENTE`, ou orientador/autoridade delegada nos limites
da delegação `[P10 §5]`.

### 4. Limites de intervenção

Pode autonomamente `[P10 §30]`: inventariar, cartografar, diagnosticar,
classificar, sinalizar, recomendar, simular sem aplicar, verificar consistência.

Não pode autonomamente: escolher núcleo definitivo, executar fissão, cortar,
fundir, reorganizar macroestrutura, promover residual, alterar o original,
selecionar periódico definitivo, inserir fonte, homologar.

Ações proibidas em bloco `[P10 §16]` incluem invenção bibliográfica, invenção
de exigência editorial, uso de fonte-coringa, supressão de proveniência,
autoauditoria, homologação pelo executor.

### 5. Critérios de aceitação e teste

**PILOTO_SUPERVISIONADO** `[P10 §35]`: dez cenários (PS-01 a PS-10), todos
abstratos — nenhum capítulo real foi usado. Critério central: PS-10 (versões
concorrentes do material de origem sem decisão canônica) deve resultar
exclusivamente em `BLOCKED/GOVERNANCE_CONFLICT`, com `material_evidence`
verificada e nenhuma derivação executada.

Vinte testes de aceitação (TA-01 a TA-20), todos com resultado `APROVADO`
declarado, mas com a ressalva expressa: "nenhum teste foi reexecutado,
reavaliado ou reformulado" nesta correção `[P10 §37.1]` — ou seja, a aprovação
registrada é textual/documental, não verificação empírica contra capítulo real.

O piloto real não é pré-condição para homologação documental (padrão repetido
em P11–P14, ver §5 do documento consolidado abaixo).

### 6. Dependências

Obrigatórias: P02, P03, P04, P05, P06, P07, P08, P09 `[P10 §1]`. Aplica
integralmente BVAA (P04+P05) `[P10 §24]` e voz autoral (P07) `[P10 §25]`.
Fronteira com Vaquita/Baleia/Komodo (papéis funcionais, não pacotes numerados)
`[P10 §4]`. Não substitui P03–P09 `[P10 §3.17]`.

---

## P11 — Revisão de Dissertação e Tese

`PACOTE_FUNCAO_REVISAO_TESE_DISSERTACAO_R01/P11_CONTRATO_FUNCIONAL_REVISAO_TESE_DISSERTACAO_HOMOLOGADO_R01.md`

Único dos cinco pacotes com **homologação documental já concluída**
(`P11_HOMOLOGADO_DOCUMENTALMENTE`, `P11_CONGELADO` — `[P11 §45.3]`); os outros
quatro (P10, P12, P13, P14) permanecem `NAO_HOMOLOGADO` neste estado do
acervo.

### 1. O que faz

Diagnostica, revisa, estabiliza e prepara para auditoria dissertações e teses,
preservando projeto intelectual, coerência global, densidade argumentativa,
voz autoral, relação afirmação-evidência, rastreabilidade, segurança e
soberania humana `[P11 §2]`. Regra estrutural central: **do global para o
local** — nenhuma intervenção local é segura sem que sua função na obra tenha
sido identificada primeiro `[P11 §2, invariante 2]`.

Entrada obrigatória (20 itens) inclui tipo de obra, versão, sumário, problema,
objetivos, hipótese/tese, método, corpus, referências, padrão de citação,
nível de intervenção autorizado, identificação de versões concorrentes
`[P11 §6.1]`. Item 19 (prazos/exigências institucionais) é
"obrigatório quando aplicável" — admite `NOT_APPLICABLE` justificado.

Saída: cartografia global, diagnóstico estrutural/argumentativo/historiográfico,
matriz de coerência, mapa de afirmações-evidências, plano de revisão modular,
unidades revistas, comentários Word, mapa de demandas externas `[P11 §24.5]`.

### 2. Etapas e ordem

Fluxo de 25 etapas `[P11 §38]`: intake → confirmação de autoridade →
verificação de dependências → ingestão controlada → cartografia global →
diagnóstico de estabilidade → diagnóstico estrutural → diagnóstico
argumentativo → diagnóstico historiográfico → mapa afirmação-evidência →
plano modular → decisão humana → revisão por módulo → revisão local
rastreável → controle de voz → controle BVAA → controle afirmação-evidência →
consolidação do bloco → verificação proporcional ou auditoria de bloco →
avanço modular → verificação global de regressão → auditoria final → decisão
autoral → homologação documental → piloto supervisionado real posterior.

Regra de proporcionalidade (não presente em P10): a auditoria de bloco **não é
rotina universal** — só exigida sob intervenção forte, alteração de
argumento/estrutura/corpus/objetivo/hipótese/conclusão, risco elevado de perda
de voz/evidência, dados sensíveis, gate específico, ou impacto material
`[P11 §14]`. Intervenções locais de baixo risco admitem "verificação
proporcional" em vez de auditoria de bloco — distinção introduzida
explicitamente como correção de não conformidade (`NCMI-P11-002`) para evitar
que a exigência fosse lida como universal `[P11 §44]`.

### 3. Gates

Documentais (não liberáveis autonomamente): `GATE_DE_ATIVACAO_P11`,
`GATE_DE_VERSAO_CANONICA`, `GATE_DE_ESTABILIDADE`, `GATE_DE_CARTOGRAFIA`,
`GATE_DE_DIAGNOSTICO_GLOBAL`, `GATE_DE_VALIDACAO_FINAL` `[P11 §28.1]`.

Decisão humana expressa: `GATE_DE_PLANO_MODULAR`, `GATE_DE_REESTRUTURACAO`,
`GATE_DE_FUSAO`, `GATE_DE_CORTE`, `GATE_DE_SUBSTITUICAO`,
`GATE_DE_REESCRITA_FORTE`, `GATE_DE_ALTERACAO_DE_OBJETIVO`,
`GATE_DE_ALTERACAO_DE_HIPOTESE`, `GATE_DE_ALTERACAO_DE_CONCLUSAO`,
`GATE_DE_TRATAMENTO_DE_DEMANDA_EXTERNA`, `GATE_DE_CONSOLIDACAO`,
`GATE_DE_HOMOLOGACAO` `[P11 §28.2]`.

Quem autoriza: autor (autoridade autoral primária sobre mudanças de sentido,
voz, argumento, estrutura, escopo), orientador (autoridade acadêmica delegada
nos limites institucionais), usuário-proponente (homologação) `[P11 §5]`.

### 4. Limites de intervenção

Pode autonomamente: conferir estrutura formal, inventariar, localizar
unidades, mapear relações, diagnosticar coerência, classificar riscos,
propor alternativas, executar correções leves expressamente autorizadas
`[P11 §31]`.

Não pode autonomamente: redefinir o projeto, escolher nova tese, alterar
objetivos/hipótese/corpus, excluir/fundir capítulos, reordenar macroestrutura,
aceitar demanda de banca, consolidar referência não verificada, alterar voz,
homologar.

Regra canônica distintiva de P11 (não repetida identicamente em P10):
`safe_result` só existe em `ERROR`; em `ABSTAINED` todo trabalho concluído vai
em `AbstentionPayload.completed_safe_work` e o não executado em
`unperformed_work`; em `BLOCKED`, o restante seguro vai em
`BlockPayload.safe_work_remaining` `[P11 §24.6, invariante 21]` — esta é a
correção mais extensa do pacote (`NCMA-P11-001`), sinalizando que a
distinção entre "resultado seguro" e "trabalho seguro" é um ponto de atrito
recorrente entre os contratos e o P09.

### 5. Critérios de aceitação e teste

Dez cenários `PS11-01` a `PS11-10` `[P11 §40]`, todos abstratos. Vinte testes
`TA11-01` a `TA11-20`, todos marcados `DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`
(diferente de P10, que declarava os 20 testes já `APROVADO`) —
`TESTES_VERIFICADOS_INDEPENDENTEMENTE_NESTA_VERSAO_CORRIGIDA: 20` aparece no
rodapé, mas isso se refere à verificação da auditoria independente sobre o
*texto do contrato*, não a execução dos testes contra manuscrito real
(`PILOTO_REAL_EXECUTADO: NAO` permanece explícito).

Distinção formal introduzida em P11 e ausente em P10: **homologação documental
≠ ativação operacional** `[P11 §42]`. Homologação documental aprova
requisitos/contrato; não exige piloto real. Ativação operacional (uso real,
implementação) exige piloto supervisionado real + corpus autorizado + auditoria
do piloto + autorização autoral específica adicional.

### 6. Dependências

P02–P09 obrigatórias. Fronteiras explícitas com P10 (P11 não presume fissão,
não converte capítulo em artigo — encaminha ao P10 após decisão humana),
P07 (voz), P06 (níveis), P04/P05 (BVAA/evidência), P08/P09 (segurança/envelope),
e com os papéis funcionais Vaquita/Komodo/Baleia (mesmos da síntese P10)
`[P11 §4]`.

---

## P12 — Revisão de Relatório de Iniciação Científica

`PACOTE_FUNCAO_REVISAO_RELATORIO_IC_R01/P12_CONTRATO_FUNCIONAL_REVISAO_RELATORIO_IC_HOMOLOGADO_R01.md`

### 1. O que faz

Diagnostica, revisa, estabiliza e prepara relatórios de IC para auditoria,
preservando proporcionalidade ao nível formativo, aderência ao plano,
conformidade institucional, veracidade de atividades/resultados, voz do
bolsista e papel formativo (não substitutivo) do orientador `[P12 §2]`.

Invariante fundacional, ausente em P10/P11: `RELATORIO_NAO_E_TESE` e
`REVISAO_NAO_E_FABRICACAO` `[P12 §3.1-2]` — o contrato inteiro é uma inversão
proporcional do P11: onde P11 exige rigor de tese, P12 proíbe explicitamente
impor esse mesmo rigor (`§4.1`: "não importa densidade de tese como padrão").

Entrada obrigatória (20 itens) espelha P11, mas troca "hipótese/tese" por
"cronograma + atividades previstas + atividades declaradas como realizadas"
`[P12 §6.1]`. Campos institucionais (formulário, regras, prazos) são
"obrigatórios quando aplicáveis", com o mesmo mecanismo de
`NOT_APPLICABLE` justificado que P11 usa para prazos.

Saída central e exclusiva de P12: **matriz de aderência**
(`plano × execução`) `[P12 §10]` — não existe equivalente direto em P10/P11,
que usam matriz de transposição/coerência, respectivamente. Classificações
próprias: `ADERENTE`, `PARCIALMENTE_ADERENTE`, `ALTERADO_SEM_EVIDENCIA_DE_AUTORIZACAO`,
`NAO_EXECUTADO`.

### 2. Etapas e ordem

Fluxo de 32 etapas `[P12 §41]`, estrutura análoga a P11 mas com módulos
próprios: matriz de aderência (etapa 8) antes de diagnóstico formativo (9) e
institucional (10-11), que não têm equivalente em P11. Mesma regra de
"auditoria de bloco não é rotina universal" que P11 (não presente em P10).

### 3. Gates

Documentais: `GATE_DE_ATIVACAO_P12`, `GATE_DE_VERSAO_CANONICA`,
`GATE_DE_ACESSO_AO_PLANO`, `GATE_DE_CONFORMIDADE_INSTITUCIONAL`,
`GATE_DE_DIAGNOSTICO_DE_ADERENCIA`, `GATE_DE_VALIDACAO_FINAL` `[P12 §31.1]`.

Decisão humana: `GATE_DE_ALTERACAO_DO_PLANO`, `GATE_DE_ALTERACAO_DE_OBJETIVO`,
`GATE_DE_ALTERACAO_DE_CRONOGRAMA`, `GATE_DE_INCLUSAO_DE_ATIVIDADE`,
`GATE_DE_EXCLUSAO_DE_ATIVIDADE`, `GATE_DE_MODIFICACAO_DE_RESULTADO`,
`GATE_DE_REESCRITA_FORTE`, `GATE_DE_REORGANIZACAO`, `GATE_DE_CONSOLIDACAO`,
`GATE_DE_HOMOLOGACAO` `[P12 §31.2]`.

Quem autoriza: bolsista (autoridade autoral primária sobre o relato — não
pode ser substituído), orientador (autoridade acadêmica e formativa, "não
deve ser transformado em ghostwriter" — frase textual do contrato)
`[P12 §5]`.

### 4. Limites de intervenção

Proibição explícita mais forte que em P10/P11: `NAO_INVENTAR_ATIVIDADE`,
`NAO_INVENTAR_RESULTADO`, `NAO_INVENTAR_PRODUTO`, `NAO_INVENTAR_JUSTIFICATIVA`
`[P12 §33]` — reflete que o objeto revisado (relato de experiência vivida) tem
um tipo de risco de fabricação que tese/dissertação não tem da mesma forma
(o bolsista relata fatos vividos, não argumento construído).

Distinção severidade/prioridade e a mesma regra `safe_result`/`completed_safe_work`
de P11 são aplicadas identicamente `[P12 §28.6]`.

### 5. Critérios de aceitação e teste

Este é o pacote mais explicitamente **incompleto no ciclo de correção**: a
"natureza desta entrega" declara correção limitada a **dois pontos únicos** —
o cenário `PS12-01` (relatório aderente com campos parcialmente preenchidos,
corrigido para produzir `PARTIAL_SUCCESS` determinístico) e o teste `TA12-14`
(proibição de fabricação, corrigido para separar `SUCCESS`-da-avaliação de
`InterventionRecord.disposition=REFUSED`) `[P12, cabeçalho + §49]`.

Diferente de P10/P11, o rodapé de P12 declara explicitamente:

```text
TESTES_VERIFICADOS_INDEPENDENTEMENTE_NESTA_VERSAO_CORRIGIDA: 0
TESTES_PENDENTES_DE_VERIFICACAO_FINAL: 20
AUDITORIA_APOS_CORRECAO_EXECUTADA: NAO
```

Ou seja: a auditoria independente que motivou esta correção *localizada*
ainda não foi refeita sobre o contrato corrigido — P12 está em um estado
documentalmente menos avançado que P10 e P11 no ciclo de homologação.

### 6. Dependências

P02–P09. Fronteira com P11 explícita e simétrica (P12 não importa densidade
de tese; P11 não é revisão de relatório) `[P12 §4.1]`. Fronteira com P10:
oportunidade editorial em relatório só é sinalizada e encaminhada, nunca
executada dentro de P12 `[P12 §4.2]`.

---

## P13 — Comentários Word Humanos e Seletivos

`PACOTE_FUNCAO_COMENTARIOS_AUDITORIA_POR_BLOCOS_R01/P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md`

### 1. O que faz

Produz comentários destinados à inserção posterior em documentos Word:
humanos, seletivos, substantivos, acionáveis, proporcionais, rastreáveis,
reversíveis, ancorados em evidência `[P13 §2]`. Diferente de P10-P12, **não
é uma função de revisão integral** — cartografa o documento completo apenas
para contexto, mas só produz comentários sobre unidades autorizadas.

Invariante central, sem equivalente direto nos outros quatro: **zero
comentários é resultado legítimo** quando não há problema material; comentar
toda unidade mecanicamente é proibido; não existe quota percentual ou
numérica de comentários — `PC30_SIGNIFICA_CRITICIDADE_E_NAO_QUOTA`
`[P13 §3.8-9, §25]`. O contrato rejeita explicitamente a interpretação de que
uma cobertura de "30%" seria uma meta de volume.

Saída: comentários individuais tipados (15 tipos: `DIAGNOSTICO`,
`ALERTA_ARGUMENTATIVO`, `ALERTA_BIBLIOGRAFICO`, `GATE_HUMANO`, etc.
`[P13 §13]`), comentários-matriz (para problemas sistêmicos recorrentes) e
remissões a comentário-matriz `[P13 §23]`.

Schema de comentário individual (`P13Comment`) é o mais detalhado dos cinco
pacotes em termos de campos de estado interno: distingue `status` (ciclo
operacional: `DRAFT`→`INSERTED`→`RESOLVED`/`SUPERSEDED`/`WITHDRAWN`) de
`resolution` (resultado humano: `ACEITO`, `RECUSADO`, `PENDENTE_DE_DECISAO`
etc.) — e ambos são explicitamente não-sinônimos do status P09 nem da
`InterventionRecord.disposition` `[P13 §31.5.1-2]`. Essa tríplice separação
(status interno / resolução / status P09 / disposição de intervenção) foi
objeto de correção nesta versão (schema `P13Comment` corrigido — ver §5).

### 2. Etapas e ordem

29 etapas `[P13 §43]`: intake → cartografia global → identificação de
unidades → matriz de criticidade → matriz de seletividade → seleção de
unidades comentáveis → verificações de fonte/evidência/voz/privacidade →
identificação de problemas sistêmicos → comentários-matriz → comentários
individuais → remissões → verificação de densidade/repetição/acionabilidade/
tom/gates → consolidação → auditoria final → decisão autoral → homologação →
piloto Word real → ativação operacional.

Regra distintiva: "nenhuma etapa implica inserção técnica em Word nesta
fase" `[P13 §43]` — o pacote produz o *conteúdo* do comentário, não o DOCX;
gerar DOCX é ação proibida (`§34.19`).

### 3. Gates

Documentais: `GATE_DE_ATIVACAO_P13`, `GATE_DE_VERSAO`, `GATE_DE_ANCORAGEM`,
`GATE_DE_CARTOGRAFIA`, `GATE_DE_SELECAO`, `GATE_DE_VALIDACAO_FINAL`
`[P13 §32.1]`.

Decisão humana: `GATE_DE_REESCRITA_FORTE` e um gate específico para cada
elemento central alterável — argumento, corpus, método, objetivo, hipótese,
resultado, conclusão — mais `GATE_DE_TRATAMENTO_DE_PRIVACIDADE`,
`GATE_DE_CONSOLIDACAO`, `GATE_DE_HOMOLOGACAO` `[P13 §32.2]`. Regra
explícita: "comentário que indica gate não concede a autorização" — o
comentário é apenas o veículo de sinalização, nunca a autorização em si.

### 4. Limites de intervenção

Pode autonomamente: cartografar, classificar criticidade, decidir **não**
comentar quando não houver problema material, formular comentário dentro do
nível autorizado, consolidar repetições `[P13 §35]`.

Não pode: executar a ação recomendada no comentário, decidir alteração
substantiva, validar fonte não aberta, resolver conflito autoral, liberar
dado sensível, criar quota, homologar.

Proibições específicas de P13 sem equivalente literal nos outros quatro:
"declarar fonte não aberta como conferida" e "fixar quota percentual" —
ambas atacam diretamente padrões de uso indevido que presumivelmente
apareceram no acervo de prompts do professor (hipótese não verificada nesta
sessão, ver pendências).

### 5. Critérios de aceitação e teste

Dez cenários `PS13-01` a `PS13-10` `[P13 §45]`; vinte testes `TA13-01` a
`TA13-20`. Correção desta versão limitada a quatro pontos: `PS13-03`
(fixado exclusivamente como `ALERTA_ARGUMENTATIVO`), `PS13-05` (trabalho
seguro de abstenção bibliográfica corrigido para registrar o alerta já
produzido em `completed_safe_work`), `TA13-13` (privacidade — condição única
determinística) e o schema `P13Comment` (tipagem de `status`/`resolution`/
`related_comment_id`/`matrix_comment_id`) `[P13 §51]`.

Mesmo padrão de P12: `AUDITORIA_APOS_CORRECAO_EXECUTADA: NAO`,
`TESTES_VERIFICADOS_INDEPENDENTEMENTE_NESTA_VERSAO_CORRIGIDA: 0` — a
correção localizada ainda não foi reauditada.

### 6. Dependências

P02–P09. Fronteiras com P11 (recebe cartografia/diagnóstico do P11, não
duplica revisão integral de tese) e P12 (adapta densidade/tom ao nível
formativo, não pode impor aparato de tese) `[P13 §4.1-2]`. É a única das
cinco funções concebida explicitamente como **consumidora** de diagnóstico
de outra função (P11 ou P12) em vez de produzir diagnóstico próprio
completo — ainda que também possa operar com cartografia global própria
quando necessário ao contexto.

---

## P14 — Incorporação de Pareceres em Artigo

`PACOTE_FUNCAO_REVISAO_RESPOSTA_PARECERISTAS_R01/P14_CONTRATO_FUNCIONAL_INCORPORACAO_PARECERES_ARTIGO_HOMOLOGADO_R01.md`

Contrato mais extenso e mais recentemente corrigido dos cinco (83 seções,
60 invariantes, 12 cenários, 24 testes — todas as contagens declaradas
explicitamente no rodapé `[P14, "CONTAGEM FINAL EXATA"]`).

### 1. O que faz

Governa, com rastreabilidade, verificabilidade, reversibilidade e soberania
humana, a incorporação de pareceres editoriais em artigo científico já
existente `[P14 §2]`. É o único dos cinco pacotes cujo objeto de entrada
inclui **múltiplas fontes de autoridade externa e potencialmente
conflitantes** (editor, parecerista 1, parecerista 2...) que precisam ser
segmentadas, classificadas e conciliadas antes de qualquer alteração no
artigo.

Invariante fundacional: `PARECER_NAO_E_AUTORIZACAO_AUTOMATICA_DE_ALTERACAO` e
`DEMANDA_DE_PARECERISTA_NAO_E_VERDADE_AUTOMATICA` `[P14 §3.1-2]` — a crítica
externa entra como *dado a processar*, não como comando.

Cada parecer deve ser segmentado em "unidades mínimas de demanda", cada uma
com decisão principal única `[P14 §12]`, classificada em 18 tipos
(`EXIGENCIA_EDITORIAL`, `DEMANDA_IMPLICITA`, `DEMANDA_CONTRADITORIA`, etc.
`[P14 §13]`) e cinco eixos independentes: prioridade, severidade,
obrigatoriedade, autoridade, suficiência, impacto `[P14 §14-19]` — mais eixos
de classificação do que qualquer outra das cinco funções.

Saída central: matriz de demandas → matriz de decisão → plano de
incorporação → alterações rastreadas → carta-resposta ao editor/pareceristas
`[P14 §21-22, §42, §44, §59]`. A carta é o único artefato de saída, entre as
cinco funções, dirigido a um destinatário **externo ao autor** (editor/
pareceristas), o que motiva um bloco extenso de invariantes sobre veracidade
da carta (proibição de declarar alteração não realizada, concordância
inexistente, ação futura como concluída — `[P14 §61-64]`).

### 2. Etapas e ordem

32 etapas `[P14 §75]`. Ordem estritamente sequencial e nomeada como regra dura
(única formulação assim explícita entre os cinco pacotes):
`MATRIZ_PRECEDE_PLANO`, `PLANO_PRECEDE_REVISAO`, `REVISAO_VERIFICADA_PRECEDE_CARTA`
`[P14 §3.43-45]`. Ordem preferencial de execução das demandas: exigências
editoriais formais → bloqueios/conflitos → estrutura central → objetivo/
hipótese/método/corpus → argumento/evidência → resultados/conclusão →
fontes → clareza local → correções formais → carta `[P14 §43]`.

### 3. Gates

Documentais (9): `GATE_DE_ATIVACAO_P14`, `GATE_DE_VERSAO_CANONICA`,
`GATE_DE_INGESTAO`, `GATE_DE_SEGMENTACAO`, `GATE_DE_MATRIZ`, `GATE_DE_PLANO`,
`GATE_DE_VERIFICACAO_DA_REVISAO`, `GATE_DE_CARTA`, `GATE_DE_VALIDACAO_FINAL`
`[P14 §41.1]`.

Humanos obrigatórios (17) + adicionais compatíveis (2) = 19 no total
`[P14 §41.2-3]`, incluindo gates específicos e nominais para cada elemento
central: `GATE_DE_ALTERACAO_DE_OBJETIVO`, `GATE_DE_ALTERACAO_DE_HIPOTESE`,
além de `GATE_DE_CONFLITO_ENTRE_PARECERISTAS` e
`GATE_DE_CONFLITO_COM_DECISAO_EDITORIAL` — únicos entre os cinco pacotes,
porque só P14 tem múltiplas fontes de autoridade externa que podem discordar
entre si.

Quem autoriza: autor correspondente (autoridade autoral primária), coautores
(autoridade compartilhada sobre mudanças que afetem contribuição/objetivo/
hipótese/método/resultados), editor (autoridade editorial formal — decisão
prevalece sobre parecer isolado em conflito comprovado), parecerista
(autoridade consultiva, "salvo incorporação formal pelo editor")
`[P14 §5, §28]`.

### 4. Limites de intervenção

Alteração de objetivo/hipótese/resultado/conclusão tem tratamento mais
extenso que em qualquer outro pacote: exige identificação explícita da
formulação vigente, demonstração de impacto sobre argumento/método/corpus/
resultados/conclusão, decisão autoral expressa, gate específico, atualização
rastreável de unidades dependentes, verificação global de regressões,
preservação da versão original `[P14 §34]` — e a correção desta versão
("proteção nominal de objetivo e hipótese", `NCMA-P14-006`) reforçou
justamente este ponto como não conformidade maior corrigida.

Proibições específicas de P14: comunicar-se com a revista, submeter o
artigo, produzir carta real nesta etapa `[P14 §67.20-23]` — reflete que a
função para exatamente antes do ato de comunicação externa efetiva.

### 5. Critérios de aceitação e teste

**PILOTO_EDITORIAL** — 12 cenários documentais abstratos, `PS14-01` a
`PS14-12` `[P14 §79]`, cobrindo: demanda clara aceitável, demanda cosmética
recusada, demanda dependente de fonte ausente, demanda de alteração de
argumento (gate), conflito entre dois pareceristas, conflito com decisão
editorial, demanda já atendida, demanda fora de escopo, parecer confidencial
sensível, carta declarando alteração inexistente (`ERROR`, não `ABSTAINED` —
distinção deliberada, `[P14 PS14-10]`), revisão parcial (`PARTIAL_SUCCESS`),
versões concorrentes do artigo (`BLOCKED`).

24 testes `TA14-01` a `TA14-24` `[P14 §80]`. Todos os 24 marcados
`DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE`; nenhum executado
(`TESTES_VERIFICADOS_INDEPENDENTEMENTE_NESTA_VERSAO: 0`).

Esta é a correção mais recente e mais extensa: seis não conformidades
maiores e quatro menores, incluindo a regra nova de que bloqueio total
(`safe_work_remaining=[]`) exige `total_block_justification` preenchido
com evidência material específica — não pode resultar de "conveniência,
incerteza genérica ou ausência de planejamento" `[P14 §51.7]`, frase que
soa como resposta direta a um padrão de abuso identificado na auditoria.

### 6. Dependências

P02–P09. Fronteiras com as quatro outras funções: não deriva capítulo em
artigo (P10), não converte demanda editorial em revisão integral de tese
(P11), não aplica exigência editorial a relatório formativo (P12), pode
consumir comentários P13 como representação auxiliar mas P13 "não produz
matriz decisória nem carta-resposta" — a decisão permanece sempre em P14
`[P14 §4, §52]`.

---

## 7. Unidade de análise por função

| Função | Unidade primária | Unidade secundária/local |
|---|---|---|
| P10 | capítulo / seção extensa / conjunto textual estabilizado (documento completo é o objeto de diagnóstico) | núcleo publicável (subconjunto textual dentro do capítulo) |
| P11 | obra inteira (tese/dissertação) para cartografia global, obrigatória antes de qualquer local | módulo (capítulo, seção, subseção, bloco argumentativo, bloco bibliográfico, introdução, conclusão, apêndice, anexo — `[P11 §14]`); dentro do módulo, unidade local (parágrafo/frase) |
| P12 | relatório inteiro para cartografia global | módulo (identificação, resumo, introdução, objetivos, cronograma, atividades, método, resultados, dificuldades, conclusão, referências, formulário, anexos — `[P12 §16]`) |
| P13 | documento inteiro **só para cartografia/contexto**, nunca como unidade de intervenção | unidade comentável, que pode ser qualquer granularidade: capítulo, seção, parágrafo, frase, termo, citação, nota, tabela, célula, figura, campo `[P13 §10]` |
| P14 | artigo inteiro (cartografia) + cada parecer inteiro (ingestão/preservação) | unidade mínima de demanda: "o menor segmento que contém problema identificável e admite uma decisão principal" `[P14 §12]` — não é uma unidade textual do artigo, é uma unidade de *crítica* |

Padrão comum a P10-P12: diagnóstico sempre parte do documento/capítulo
inteiro (cartografia global obrigatória) e desce para unidades cada vez mais
locais só depois de estabilidade confirmada. P13 inverte a lógica de
consumo — cartografa o todo mas nunca trata o todo como alvo de intervenção,
só unidades seletivamente escolhidas. P14 introduz uma unidade de análise
sem paralelo nas outras quatro: a unidade de demanda no parecer, que é
ortogonal à estrutura do artigo (uma demanda pode atravessar seções, ou uma
seção pode receber múltiplas demandas de pareceristas distintos).

Isto decide arquitetura de pipeline: nenhuma das cinco funções pode operar
em modo "stream de parágrafos" sem primeiro materializar uma representação
estrutural completa do documento (e, em P14, dos pareceres). C0 (ingestão)
precisa entregar essa estrutura antes que C2/C3 comecem — não é possível
paralelizar a análise por parágrafo independente da cartografia global.

## 8. O que as funções pressupõem da entrada, e o que a ingestão atual entrega

Confrontado com `escolio/ingestao/FORMATO.md` (testado apenas contra um
relatório de PIBIC/CNPq, 33 páginas, Word→PDF, coluna única).

**O que as cinco funções pressupõem, em comum:**

- Identificador estável por unidade, rastreável à origem — `[P10 §14]`,
  `[P11 §37]`, `[P12 §17]`, `[P13 §31.5]`, `[P14 §53-55]`. A ingestão entrega
  isso (`UNI-<TIPO>-<HASH8>-<PAGINA>-<INDICE>`), mas apenas para as unidades
  que o parser já reconhece (parágrafo, citação recuada, nota, referência,
  seção, figura/tabela).
- Estrutura hierárquica da obra (capítulos, seções, função de cada seção) —
  necessária para toda cartografia global em P10-P12. **Lacuna confirmada**:
  `FORMATO.md §RG-002` declara explicitamente que o documento de
  desenvolvimento não tem sumário/índice e que não há como validar nível
  hierárquico — todo título é tratado como nível 1 por falta de evidência de
  segundo nível. Uma tese/dissertação real (objeto de P11) tipicamente *tem*
  sumário com múltiplos níveis; a heurística RG-001/RG-002 não foi testada
  contra esse caso e não tem mecanismo de desambiguação por profundidade.
- Objetivos, hipótese, método, corpus como campos identificáveis do
  documento — nenhuma heurística de extração desses campos aparece em
  `FORMATO.md`. A ingestão extrai metadados de folha de rosto (autor,
  orientador, título, ano) mas não extrai objetivo/problema/hipótese como
  campos estruturados — esses ficam para camada de análise (C2/C3), não C0.
  Isso é compatível com a divisão C0/C2 do CLAUDE.md, mas significa que
  nenhuma das cinco funções recebe esses campos "de graça" da ingestão atual.
- Notas de rodapé vinculadas à chamada (`unit_id_chamador` bidirecional) —
  necessário para P11 §17 (integridade nota↔chamada como falha impeditiva de
  consolidação). A ingestão entrega isso (RG-005), testado contra 4 casos
  reais no documento de desenvolvimento.
- Citações no corpo vinculadas a bibliografia (BVAA, P04/P05, exigido por
  todas as cinco funções). A ingestão extrai citação autor-data (RG-007) mas
  marca 38 de 138 ocorrências como `indeterminado` no documento de teste —
  ou seja, mais de um quarto das citações candidatas não puderam ser
  vinculadas com segurança a um autor da lista de referências. Nenhuma das
  cinco funções tem tolerância para isso: todas exigem "fonte
  identificada/localizada/acessível/lida" como estados discretos antes de
  qualquer consolidação (`[P10 §23]`, `[P11 §19]`, `[P13 §19]`, `[P14 §30]`).
  A ingestão já produz o estado `indeterminado` correto para alimentar esse
  requisito — não finge resolver a ambiguidade — mas a fração de
  indeterminação observada (27%) sugere que, em textos historiográficos com
  citação narrativa frequente ("Grewe (1979)"), a taxa de pendência
  bibliográfica de entrada será alta.
- Versão do documento / hash para controle de versões concorrentes — todas
  as cinco funções exigem identificação de versão como pré-condição
  (`ESTAVEL_PARA_*` vs `INSTAVEL_POR_VERSAO`). A ingestão calcula
  `hash_documento` (sha256[:8] do PDF), determinístico e testado — atende ao
  requisito para uma única versão, mas **não há mecanismo, na ingestão atual,
  de comparação entre duas versões do mesmo documento** (diff estrutural,
  detecção de divergência). PS-10 (P10), PS11-10, PS12 (implícito via versão
  canônica) e PS14-12 dependem de conseguir "inventariar as versões e
  identificar divergências objetivas" como trabalho seguro sob bloqueio — a
  ingestão sozinha não produz esse inventário comparativo; teria que ser
  camada adicional.

**Lacunas específicas por função:**

- **P10**: exige "unidades móveis, compartilháveis e residuais" já
  classificadas na cartografia (`[P10 §9]`) — julgamento editorial que a
  ingestão não faz e não deveria fazer (C0 é estrutural, não interpretativo).
- **P12**: exige distinguir "atividade prevista" de "atividade declarada
  como realizada" a partir do texto — não há heurística de ingestão para
  isso; depende de extração semântica (C2/C3).
- **P13**: exige granularidade até "célula de tabela" e "campo de
  formulário" como unidades comentáveis endereçáveis. A ingestão atual
  detecta tabelas apenas por legenda/crédito (RG-009), sem decompor células
  — não há `unit_id` de célula individual hoje.
- **P14**: exige ingestão e preservação de **pareceres**, documentos de
  natureza totalmente diferente do manuscrito acadêmico (cartas de revisor,
  possivelmente sem estrutura de seções/parágrafos formal). `FORMATO.md` não
  cobre esse tipo de documento; nenhuma heurística foi desenvolvida ou
  testada para parecer editorial.

Nenhuma dessas lacunas foi resolvida nesta sessão — ficam registradas para
`escolio/ingestao/LACUNAS.md` e/ou `docs/coleta.md`, conforme a disciplina
do CLAUDE.md §10, mas essa gravação não foi feita aqui (ver pendências).

## 9. Confronto com o CLAUDE.md

O CLAUDE.md foi escrito sem leitura prévia de nenhuma especificação. Ponto a
ponto:

**Pipeline C0-C5 (CLAUDE.md §4).** Nenhuma das cinco funções menciona
camadas, modelos (Haiku/Sonnet/Opus) ou a divisão C0-C5. Isso é esperado: os
contratos P10-P14 são "camada FUNCAO" (`[P1x §1]`), acima e agnóstica à
arquitetura de execução — coerente com a "neutralidade tecnológica" que os
próprios contratos declaram preservar em todo `DECLARAÇÃO DE PRESERVAÇÃO` e
com as lacunas legítimas de cada pacote, que listam explicitamente "modelo
de LLM", "linguagem", "API", "fornecedor" como não decididos. **Não contraria
nem confirma** — está fora do escopo dos contratos de função, exatamente como
já apontado para P22 na análise anterior (`docs/spec/contrato-P22.md §6.1`).
O ponto de atenção já registrado ali — que o CLAUDE.md fixa decisão técnica
que os pacotes de política tratam como lacuna aberta — se estende
identicamente aos pacotes de função.

**Sete eixos de avaliação (CLAUDE.md §3).** Nenhum dos cinco contratos usa
essa taxonomia. Cada função tem sua própria taxonomia de classificação
interna: P10 (classes de núcleo, vereditos editoriais), P11 (vereditos
estruturais/argumentativos, `COERENTE`/`CONTRADITORIO`/etc.), P12 (aderência,
diagnóstico formativo, conformidade institucional), P13 (matriz de
criticidade em 12 eixos), P14 (prioridade/severidade/obrigatoriedade/
autoridade/suficiência/impacto). **Nenhuma dessas taxonomias mapeia
1:1 para os sete eixos do CLAUDE.md.** Os eixos mais próximos:

  - Eixo 3 (método e adequação das fontes) ⊂ aplicação P04/P05 (BVAA,
    afirmação-evidência), presente em todas as cinco funções.
  - Eixo 4 (estrutura argumentativa) ⊂ diagnóstico argumentativo/estrutural
    de P10-P12.
  - Eixo 6 (gramática, coesão, registro) ⊂ comentário linguístico de P13,
    correção linguística de P12 — mas com restrição em ambos: só é matéria de
    comentário/intervenção quando afeta sentido, não por preferência
    estilística.
  - Eixo 7 (aderência ao estilo do professor) — **não coberto por nenhuma das
    cinco funções**. Nenhum contrato menciona "estilo do professor",
    "Style Card" ou qualquer artefato de voz específica de um corretor
    humano. Todas usam P07 ("voz autoral"), que é a voz do **autor do
    documento avaliado** (aluno, bolsista), não a voz de quem avalia. Isso é
    uma divergência conceitual relevante: o eixo 7 do CLAUDE.md pressupõe que
    o sistema *imite o professor*; os contratos P10-P14 pressupõem que o
    sistema *preserve a voz do autor avaliado* e nunca a substitua pela voz
    de quem revisa/comenta/orienta. Não são incompatíveis — são papéis de
    voz distintos (voz do documento vs. voz de quem comenta) — mas o CLAUDE.md
    não distingue isso explicitamente hoje. Ponto para o professor decidir
    (ver perguntas).
  - Eixos 1, 2, 5 (mérito/originalidade, fundamentação teórica, normalização
    ABNT) não têm classificação dedicada em nenhum dos cinco contratos —
    ficam implícitos dentro de diagnóstico argumentativo/historiográfico
    (P10-P11) ou simplesmente fora de escopo declarado (normalização ABNT
    aparece só tangencialmente, como "norma bibliográfica" em P12 §13).

**Dois modos de saída — comentário vs. ouro (CLAUDE.md §1b).** Nenhuma das
cinco funções usa essa dicotomia terminológica, mas a distinção existe
materialmente em formas distintas:

  - P13 é estruturalmente "modo comentário": produz apenas comentários,
    nunca aplica alteração ao texto (`[P13 §2]`: "os comentários permanecem
    localizados, seletivos e subordinados"; ação de inserção em DOCX é
    proibida nesta fase).
  - P11, P12 e P14 têm um modo misto: podem executar correção local
    autorizada diretamente no texto (`[P11 §29]`, `[P12 §32]`) *e* também
    produzir comentário Word como saída complementar (P11 §25, P12 §29) —
    não escolhem entre os dois modos, os combinam conforme o nível de
    intervenção autorizado.
  - P10 não produz texto revisado diretamente até "redação modular
    autorizada" (após matriz e arquitetura aprovadas) — é estruturalmente
    mais próximo de "modo ouro" quando chega a essa etapa, mas
    condicionalmente, não como modo fixo.

  A pergunta em aberto no CLAUDE.md ("se o modo ouro entrega texto aplicado
  ou sugestão lado a lado, e quem assina o resultado") **não é resolvida por
  nenhum dos cinco contratos** — todos tratam "quem decide" e "quem assina"
  como autoridade humana (autor/orientador/editor conforme a função), nunca
  como o sistema. Isso é compatível com o CLAUDE.md §1, mas não decide a
  questão específica de "lado a lado vs. aplicado".

**Schema de achado (CLAUDE.md §7): `{id, unidade_id, eixo, gravidade,
evidencia, diagnostico, sugestao, confianca}`.** Comparação campo a campo
com o schema mais próximo de cada função:

  - `id` ↔ `demand_id`/`comment_id`/`change_id` conforme a função — presente
    em todas.
  - `unidade_id` ↔ `unit_id`/`target_article_unit`/`module_id` — presente em
    todas, mas com granularidade variável (ver §7 acima).
  - `eixo` — **não tem equivalente direto em nenhuma das cinco funções**.
    Todas usam taxonomias próprias de tipo (`comment_type`, `demand_type`,
    classes de veredito) que não mapeiam 1:1 para os sete eixos do
    CLAUDE.md. Um `eixo` do CLAUDE.md teria que ser derivado por composição
    de `comment_type`/`demand_type` + módulo afetado — não é um campo nativo.
  - `gravidade` ↔ `severity`/`severidade` (`CRITICA`, `MAIOR`, `MODERADA`,
    `MENOR`, `INFORMATIVA` em P13/P14; ausente como campo próprio em P10-P12,
    que usam antes "criticidade" via classes de veredito).
  - `evidencia` ↔ `evidence`/`claims`+`evidence_ids` — presente e mais
    granular nos contratos (distingue `sufficiency`, `confidence`,
    `verification_status` como campos separados; o CLAUDE.md os colapsa em
    `confianca`).
  - `diagnostico` ↔ `problem`/`problem_identified` — presente.
  - `sugestao` ↔ `recommended_action`/`requested_action` — presente, mas com
    salvaguarda mais explícita nos contratos: "recomendação não é execução"
    é invariante repetida em todas as cinco funções; o CLAUDE.md não tem essa
    frase equivalente hoje (embora §1 implique isso pela regra "toda saída
    passa por revisão do professor").
  - `confianca` ↔ `confidence`, presente, mas os contratos frequentemente
    separam `confidence` de `sufficiency` — o CLAUDE.md usa um único campo
    para o que os contratos tratam como dois eixos distintos (quão certo vs.
    quão suficiente é o suporte).

  **Achado central**: o schema do CLAUDE.md é compatível em espírito mas
  **mais raso** que qualquer um dos cinco esquemas de saída dos contratos —
  nenhum deles usaria só esses oito campos sem perda de informação
  operacional (status P09, payloads de abstenção/bloqueio, gates,
  disposição de intervenção, rastreabilidade bidirecional não têm onde
  caber no schema atual). Se o schema de achado do CLAUDE.md for a
  interface real entre C3/C4 e o parecer final, ele precisará ser estendido
  ou os contratos precisarão ser reduzidos a esse schema — nenhuma das duas
  ações foi tomada nesta sessão.

---

## Perguntas que só o professor responde

Ordenadas por impacto na arquitetura (mais caro de decidir depois, primeiro):

1. **O eixo 7 do CLAUDE.md ("aderência ao estilo do professor") e o "P07 voz
   autoral" dos contratos P10-P14 (voz do aluno/autor avaliado) são
   conceitos deliberadamente distintos, ou o eixo 7 precisa ser reescrito
   para não confundir "voz de quem corrige" com "voz de quem escreveu"?**
   Isso decide se o sistema deve ter *dois* perfis de voz simultâneos (o do
   aluno, a preservar; o do professor, a imitar no comentário/parecer) ou se
   o eixo 7 do CLAUDE.md está descrevendo algo que nenhum dos cinco
   contratos de função contempla.

2. **O schema de achado do CLAUDE.md (`{id, unidade_id, eixo, gravidade,
   evidencia, diagnostico, sugestao, confianca}`) deve ser estendido para
   cobrir os payloads canônicos do P09 (status, abstenção, bloqueio, gates,
   disposição de intervenção) referenciados por P10-P14, ou o schema do
   CLAUDE.md é deliberadamente uma simplificação de produto que descarta
   esse aparato de governança?** Impacto: se P09 for adotado como contrato
   real de runtime, o schema de achado atual é insuficiente; retrofit depois
   é caro (mesma lógica de "procedência sobrevive à destilação" do CLAUDE.md
   §7).

3. **As cinco funções (P10-P14) são material que o professor pretende usar
   como especificação de arquitetura real do Escólio, ou são um pacote de
   handoff para um `ENGENHEIRO_LLM` externo, redigido em outro contexto
   (com papéis como `CHAT_CONTROLADOR_ARQUITETO`, `USUARIO_PROPONENTE`,
   editor/parecerista) que talvez nem se aplique 1:1 ao projeto Escólio?**
   Sem essa resposta, não é possível decidir se P10-P14 devem orientar C2-C5
   ou se são um artefato paralelo, de proveniência distinta, a ser apenas
   consultado por analogia. (Mesmo tipo de dúvida já registrada para o P22 em
   sessão anterior — ver `docs/spec/contrato-P22.md §5`, "nota crítica sobre
   autorização".)

4. **Nenhuma das cinco funções corresponde exatamente aos seis tipos de
   documento do CLAUDE.md §2** (iniciação científica ↔ P12 é o único mapeamento
   direto; artigo Qualis A1/A2 ↔ parcialmente P10 [derivação] e P14
   [incorporação de pareceres]; dissertação/tese ↔ P11; capítulo de livro e
   relatório de pós-doutorado não têm função dedicada em P10-P14). **O
   professor pretende que P10-P14 sejam a lista definitiva e completa de
   funções, com capítulo de livro e relatório de pós-doc cobertos por
   generalização de P11, ou faltam pacotes P15+ ainda não lidos/existentes
   para esses tipos?**

5. **A distinção "homologação documental ≠ ativação operacional" (presente
   em P11-P14, ausente textualmente em P10, embora P10 também separe piloto
   real de homologação) deve se tornar uma regra formal do próprio CLAUDE.md
   §6 (disciplina de sessão), com um gate equivalente antes de qualquer
   sessão declarar uma camada do pipeline "pronta para uso real"?** Baixo
   custo de decidir agora, mas evita que "documentado" seja confundido com
   "testado" nas sessões futuras.

---

Custo desta sessão: cinco leituras completas de contrato (P10: 1421 linhas,
P11: 2299, P12: 2232, P13: 2189, P14: 3018 — total ≈11.160 linhas) mais
`FORMATO.md` (356 linhas) para a seção 8. Nenhuma chamada a API de LLM;
custo em tokens de leitura, não em US$ de inferência de produto.

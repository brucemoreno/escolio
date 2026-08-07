# DIVERGÊNCIAS — CLAUDE-rascunho.md vs. especificação de governança (P00–P05)

Lido somente agora, após o mapa da especificação estar pronto, conforme instrução. Este documento não altera o CLAUDE-rascunho.md nem resolve nenhuma contradição — apenas as expõe.

---

## 1. Onde a especificação do professor é mais completa

### Schema de achado (§7 do rascunho) vs. schema afirmação–evidência (P05)

O rascunho define, em uma linha: `{id, unidade_id, eixo, gravidade, evidencia, diagnostico, sugestao, confianca}` [CLAUDE-rascunho.md, §7]. Isso é uma estrutura de achado editorial, não um schema de rastreabilidade de evidência.

O P05 define 23 campos com dicionário de dados completo, distinguindo, só para a dimensão de evidência: `source_id`, `source_type`, `source_reference`, `edition_or_version`, `location_type`, `location_value`, `page_or_folio`, `evidence_excerpt`, `evidence_level`, além dos estados `access_state`, `reading_state`, `validation_state`, `sufficiency` e `confidence` como campos **separados e não colapsáveis** [P05/02_DICIONARIO_DE_DADOS_P05_R01.csv]. O rascunho tem um único campo `evidencia` (string livre, presumivelmente) e um único campo `confianca` — sem distinguir se a "evidência" foi localizada, acessada, lida integral ou parcialmente, sem distinguir suficiência de confiança, e sem as 20 regras de coerência que impedem, por exemplo, confiança alta com evidência ausente (RC-007) [P05/04_REGRAS_DE_COERENCIA_E_INCOMPATIBILIDADE_P05_R01.csv].

O rascunho também não define abstenção como estado de schema — a lógica de abstenção do P05 (`usage_status=ABSTENCAO`) e do P04 (`ABSTENCAO_BIBLIOGRAFICA`) não tem equivalente estrutural no schema de achado do rascunho.

### Propagação de estado (§4 do rascunho) vs. travas anti-deriva (P01) e máquina de estados documental (P03)

O rascunho descreve um pipeline linear de camadas (C0 a C5) com uma regra dura sobre tokens de entrada do Opus, mas não define uma máquina de estados para o *processo de governança do próprio projeto* — não há, no rascunho, nada equivalente aos 10 estados documentais do P03 (`NAO_INICIADO`, `AUTORIZADO_PARA_EXECUCAO`, `EM_EXECUCAO_DOCUMENTAL`, `EXECUTADO_NAO_AUDITADO`, `EM_AUDITORIA`, `HOMOLOGADO_E_CONGELADO`, etc. [P03/02_MAQUINA_DE_ESTADOS_DOCUMENTAL_P03_R01.csv]), nem à separação de papéis (`USUARIO_PROPONENTE`, `CONTROLADOR_ARQUITETO`, `EXECUTOR_DOCUMENTAL`, `AUDITOR_INDEPENDENTE` [P01/01_TRAVA_ANTIDERIVA_OPERACIONAL_P01_R01.txt]), nem a classificação de divergência em material/formal/não comprovada [P01/04_PROTOCOLO_DE_RESTAURACAO_DE_ESTADO_P01_R01.txt].

O rascunho tem, em vez disso, uma disciplina de sessão (§6: "uma sessão = um tema") e um princípio de verbosidade (§11), que cobrem parte do mesmo problema (evitar deriva de escopo) de forma bem mais leve — sem gates formais, sem matriz de autoridade por transição, sem estado persistido explicitamente por componente.

### Verificação de fontes (rascunho, disperso) vs. protocolo BVAA (P04)

O rascunho menciona "evidência localizada" (§1) e "procedência" com marcadores `[acervo:arquivo]`, `[diff:capítulo]`, `[entrevista]` ou `[INFERIDO]` (§7), mas não define uma escala de leitura (não realizada / indireta / parcial / integral), não define os quatro níveis de evidência A–D, não define a regra de dupla verificação para paginação, e não define os 18 gatilhos de abstenção bibliográfica do P04. A noção de "procedência sobrevive à destilação" no rascunho é o análogo funcional mais próximo do princípio de proveniência do P03 (POL-005) e do P05, mas está expressa em uma frase, não em um protocolo com estados e transições.

---

## 2. Onde há contradição direta

### Modelo por camada (rascunho) vs. veto a decisões de modelo/fornecedor (P00, decisões vetadas)

O rascunho especifica, com nome de modelo, qual camada roda em qual modelo: "C2 Triagem: Haiku 4.5; C3 Análise: Sonnet 5; C4 Síntese: Opus 5; C5 Verificação: Sonnet 5" [CLAUDE-rascunho.md, §4], e reitera critérios de escalada de modelo por sessão de desenvolvimento em §5.

A especificação de governança veta explicitamente essa decisão como não autorizada nesta camada: "LACUNAS_GERAIS_PRESERVADAS: [...] modelo ou modelos; [...] REGRA: Nenhuma lacuna poderá ser preenchida por inferência. Qualquer decisão exige autorização expressa do USUARIO_PROPONENTE." [P00/07_LACUNAS_NAO_INFERIVEIS_P00_R01.txt]. Também: "arquitetura, plataforma, modelo, fornecedor e número de agentes permanecem não definidos" [P00/06_GOVERNANCA_CONGELADA_E_TRAVAS_P00_R01.txt].

Os dois lados: o rascunho já decide modelo por camada como fato de arquitetura corrente; a especificação de governança trata "modelo ou modelos" como item explicitamente não decidido e não inferível, com veto reiterado em P02, P03, P04 e P05 ("não escolher arquitetura, tecnologia ou política" [P02/03_MATRIZ_DE_REQUISITOS_LIMITES_GATES_E_SAIDAS_P02_R01.csv]; "não escolher tecnologia, banco, linguagem, API ou arquitetura" [P05/00_LEIA_PRIMEIRO.txt]).

### Implementação como fato corrente (rascunho) vs. implementação não autorizada (P00, P05)

O rascunho pressupõe, em toda sua extensão (pipeline C0–C5, convenções técnicas em Python/uv/ruff/pytest, SDK `anthropic`, `costs/ledger.jsonl`), que a implementação já está em curso ou plenamente autorizada.

A especificação de governança trata implementação como item vetado até P25, precedido por P22 (handoff), P23 (decisão de arquitetura) e P24 (especificação técnica) [P00/04_INVENTARIO_CANONICO_DE_COMPONENTES_R03.csv, linha P25: "NAO_AUTORIZADA"]. Reiterado em cada um dos cinco pacotes lidos ("não implementar" aparece nas travas de P02 a P05).

Os dois lados: o rascunho é, por definição, um documento de arquitetura e implementação técnica em andamento; a especificação de governança declara que a arquitetura técnica "permanece não decidida" [P00/01_ESTADO_CANONICO_CONSOLIDADO_P00_R01.txt] e que a implementação é vetada até uma cadeia de sete componentes (P19–P25) ser cumprida. Não escolho vencedor.

### Ausência de gates humanos formais no rascunho vs. gates humanos obrigatórios por função (P02)

O rascunho menciona, en passant, "todo achado carrega evidência localizada e nível de confiança" (§1) e uma lista de itens "em aberto" que não se toca sem autorização (tese, argumento, recorte — §1b), mas não estrutura isso como gate formal com autoridade nomeada, pré-condição e ação proibida.

O P02 define, para cada uma das seis unidades funcionais, um campo explícito `gate_de_autorizacao` com texto específico (ex.: para F02: "Cortes, fusões, realocações, mudanças macroestruturais e intervenções fortes exigem autorização humana" [P02/03_MATRIZ_DE_REQUISITOS_LIMITES_GATES_E_SAIDAS_P02_R01.csv]). Não há contradição de conteúdo aqui — apenas uma lacuna estrutural no rascunho quanto à formalização do gate. Registrado como candidato a autorização expressa na seção 3, não como contradição.

---

## 3. Onde o CLAUDE-rascunho.md cobre o que a especificação não cobre

Nestes pontos, a especificação de governança é silenciosa e o desenho do rascunho decide algo por conta própria. São candidatos a autorização expressa do professor, não fatos já resolvidos pela governança.

### Escolha de modelo por camada e critério de escalada (§4, §5)
A especificação de governança não aborda modelo algum (é item vetado, ver seção 2). O rascunho decide isso integralmente: Haiku para triagem, Sonnet para análise/síntese/verificação de código, Opus só para C4 e só em sessões de arquitetura. **Candidato a autorização expressa**: confirmar se esta escolha de modelo por camada é uma decisão já autorizada pelo USUARIO_PROPONENTE fora do escopo dos pacotes P00–P05, ou se depende de P23 (decisão de arquitetura).

### Convenções técnicas de linguagem, ferramentas e SDK (§7)
Python 3.11+, `uv`, `ruff`, `pytest`, SDK `anthropic` direto sem framework de agentes — nenhuma dessas escolhas aparece nos pacotes de governança lidos, que tratam "arquitetura técnica" como não decidida. **Candidato a autorização expressa**: mesma observação acima.

### Pipeline de seis camadas C0–C5 com funções e responsabilidades específicas (§4)
A especificação de governança define máquinas de estado para o *processo documental de governança* (P03) e para o *ciclo bibliográfico* (P04), mas não define um pipeline de processamento de texto do aluno. O pipeline C0–C5 é inteiramente uma decisão do rascunho, sem equivalente na governança lida. **Candidato a autorização expressa**: se este pipeline técnico está dentro do escopo que P00–P05 classificam como "arquitetura técnica" (vetada) ou se é tratado como uma camada de execução distinta, já autorizada.

### Dois modos de saída — comentário e ouro (§1b)
Não há menção, em P00–P05, a modos de saída distintos (comentário vs. aplicação de correção). O catálogo funcional do P02 define seis unidades funcionais (revisão de dissertação, comentários Word, incorporação de pareceres, etc.), mas não as agrupa em "modos" no sentido do rascunho. A própria função F04 ("Revisão em comentários Word") parece ser o correlato mais próximo do "modo comentário", mas o rascunho generaliza isso para todos os tipos de documento, o que o P02 não fez. **Candidato a autorização expressa**: verificar se "modo ouro" (aplicar correção direta ao texto) tem algum correlato ou vedação implícita nas seis funções do P02 — nenhuma delas descreve edição direta e irrestrita do texto do aluno sem gate humano.

### Eixos de avaliação provisórios (§3) e a existência de um eixo "aderência ao estilo do professor"
Nenhum dos seis eixos do rascunho aparece nos pacotes de governança lidos. O rascunho já assume que serão revisados na "Sessão 0D" e "Sessão 1" contra o acervo real — isso é consistente com a postura de P00–P05 de não inferir taxonomia sem evidência, mas a existência do eixo 7 ("Aderência ao estilo de correção do professor") com peso igual aos demais é uma decisão de design que a governança lida não aborda nem veta. **Candidato a autorização expressa**: nenhuma ação necessária além de registrar que esta decisão não colide com P00–P05 — apenas não é coberta por eles.

### Método de validação por três fontes: declarado, praticado, tácito (§9)
Este método epistemológico específico (cruzar prompts declarados com o diff de correções efetivamente aceitas, tratando divergência como "conhecimento tácito" a ser levado ao professor) não tem equivalente na governança lida. O P04 e o P05 tratam de evidência bibliográfica externa (fontes citadas no trabalho do aluno), não de evidência sobre o próprio método do professor. **Candidato a autorização expressa**: nenhuma colisão detectada; é uma extensão original do rascunho para um problema (extrair o método tácito do professor) que P00–P05 não cobrem porque tratam de outro domínio (controle bibliográfico do aluno, não modelagem do estilo do corretor).

### Regras de custo, cache, batch API e `costs/ledger.jsonl` (§4, §11)
Inteiramente ausentes da especificação de governança, que não trata de custo operacional algum. **Candidato a autorização expressa**: mesma observação de arquitetura técnica não decidida.

### Disciplina de sessão e verbosidade (§6, §11)
Tem afinidade de princípio com POL-012 do P03 ("Próxima ação única" — "Reduzir deriva operacional e ciclos recursivos") [P03/01_POLITICAS_TRANSVERSAIS_P03_R01.md], mas o rascunho aplica isso à disciplina de desenvolvimento de software (uma sessão = um tema, backlog para o resto), enquanto POL-012 aplica-se à disciplina do processo de governança documental (uma próxima ação por vez, por componente). São princípios paralelos, não conflitantes, mas em domínios distintos — não há regra da governança que resolva como o rascunho deveria estruturar sessões de desenvolvimento.

---

---

## 4. Acrescentado em 2026-08-06 (sessão de reescrita do CLAUDE.md)

### 4.1 P07 × eixo 7 — de quem é a voz que o contrato governa?

**Leitura A — o P07 governa também a voz de quem comenta.** O contrato enuncia, entre os
princípios: *"imitação de pessoa real é substituída por atributos abstratos"*
[P07/01_CONTRATO_UNIVERSAL_DE_VOZ_AUTORAL_P07_R01.md, seção Princípios]. O enunciado é
universal, sem restringir-se ao autor avaliado. Sob esta leitura, a primeira frase do CLAUDE.md
anterior ("reproduz o método, os critérios e a **voz de correção** do Prof. Christian") e o eixo
7 ("aderência ao estilo de correção do professor") colidem com o contrato. Caminho compatível:
`PERFIL_AUTORAL_DERIVADO_DE_AMOSTRAS` ou `PERFIL_HIBRIDO_DECLARACAO_MAIS_AMOSTRAS`
[P07/04_MATRIZ_DE_PERFIS_FONTES_CONFIANCA_E_AUTORIDADE_P07_R01.csv], expresso nas 30 dimensões
`VOZ-D01…D30`, sem nome de pessoa.

**Leitura B — o P07 rege só a voz do autor avaliado.** A finalidade declarada é *"Preservar,
avaliar e controlar a voz autoral em textos acadêmicos"* [P07/01, Finalidade], e a hierarquia
que o contrato fixa termina em "voz autoral > fluidez" — trata-se da voz do texto sob revisão.
O P13 confirma: entre as entradas obrigatórias está `perfil de voz` [P13 §6.2], e a matriz de
criticidade tem o eixo **Voz — "A intervenção apaga ou deforma voz autoral?"** [P13 §11]. É a
voz a proteger, não a voz de quem escreve o comentário. Sob esta leitura, a voz de quem comenta
é **lacuna aberta**, não proibição, e o eixo 7 descreve algo que nenhum dos contratos contempla.

**Não resolvida.** Consequência operacional enquanto durar: `style/style_card.md` não tem
destino declarado, e nenhuma decisão de arquitetura pode depender da resposta.

### 4.2 `docs/autorizacao.md` × `P01/05` — autorização coletiva é válida?

**Leitura A — a forma coletiva viola a trava.** `docs/autorizacao.md` registra um ato verbal
único que declara que "as decisões listadas em `open_decisions` do inventário — modelo,
fornecedor, infraestrutura, linguagem, API, banco de dados, RAG, fine-tuning, arquitetura
técnica, métricas, ambiente e implantação — deixam de estar pendentes", e valida decisões
anteriores "retroativamente". Contra o texto literal de
`P01/05_TRAVA_ANTIDERIVA_MONOLITICA_P01_R01.txt`, três proibições são tocadas: *"emitir
autorização coletiva"*; *"presumir autorização futura"* (a validação retroativa é a imagem
espelhada); *"iniciar P(n+1) sem decisão autoral específica"*. O próprio `autorizacao.md`
registra que o inventário mantém `transfer_authorized: false`, e o P22 §30 exige onze
pré-condições em ordem antes do P23.

**Leitura B — a trava vincula o executor, não o proponente.** R03 §4.1 faz do
`USUARIO_PROPONENTE` a autoridade final: "pode autorizar fases, aprovar ou rejeitar decisões,
congelar revisões, autorizar handoffs, autorizar uso de dados, autorizar treinamento, RAG ou
implementação", e "nenhum outro papel pode substituir sua decisão". As proibições do `P01/05`
são dirigidas a quem executa — impedem *presumir* autorização coletiva, não necessariamente
*conceder* uma.

**Não resolvida, e material.** A carta branca é o que autoriza decidir arquitetura, modelo e
linguagem — sustenta as seções de autorização, de modelos e de convenções técnicas do CLAUDE.md.

**Caminho que fecha a questão sem depender de interpretação:** reemitir `docs/autorizacao.md`
em forma **itemizada**, uma entrada por decisão. Doze entradas. Sob a Leitura A, sana o vício;
sob a Leitura B, não custa nada.

---

## Fechamento

Este documento não resolve nenhuma das contradições listadas, nem decide os candidatos a
autorização expressa da seção 3. Todos ficam registrados para decisão do professor.

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

### 4.3 CON-P05-001 — três vocabulários bibliográficos: convergência ou camadas separadas?

Registrado como conflito não resolvido desde a implementação do P05
[`escolio/LACUNAS.md`, `CON-P05-001`] e mantido como tal na implementação da máquina de
estados do P04 [`escolio/bvaa/LACUNAS.md`, `LAC-BVAA-001`, `LAC-BVAA-002`]. Nenhuma das três
fontes — P04/03, R03 CAMADA D, P05 — resolve a divergência entre si; cada uma foi escrita
sem referência às outras duas.

**Os três vocabulários, o que cada um estrutura:**

- **P04/03** [`03_MAQUINA_DE_ESTADOS_BIBLIOGRAFICOS_P04_R01.csv`] — máquina de estado único:
  17 estados, uma obra ocupa exatamente um estado por vez, numa cadeia de ciclo de vida
  (identificação → localização → acesso → leitura → validação → recomendação/abstenção).
- **P05** [`escolio/vocabulario.py`: `AccessState`, `ReadingState`, `ValidationState`] — três
  campos paralelos e independentes de `RelacaoAfirmacaoEvidencia`. Uma afirmação pode estar
  `ACESSADA` (access_state) e `LIDA_PARCIALMENTE` (reading_state) e `VALIDACAO_PENDENTE`
  (validation_state) simultaneamente — não é uma máquina de estado único, é uma estrutura de
  registro com três eixos independentes.
- **R03 CAMADA D** [`01_PROTOCOLO_MESTRE_DE_ACAO_ECOSSISTEMA_LLM_ACADEMICA_R03.md`] — 9
  estados mínimos, sem os campos de evidência mínima/autoridade/ação/condição de erro que
  P04/03 declara para cada estado.

**Leitura A — os três deveriam convergir para um único vocabulário canônico.** Os três
tratam do mesmo domínio material (identificação, acesso, leitura e validação de uma fonte
bibliográfica) e usam rótulos frequentemente idênticos ou quase idênticos
(`PAGINA_CONFIRMADA`/`PAGINA_NAO_CONFIRMADA` aparecem literalmente iguais em P04/03 e em
`ValidationState` do P05). Rótulos coincidentes sugerem que a spec pretendia um único
domínio de estado, fragmentado em três documentos por terem sido produzidos em momentos
distintos do projeto (R03 é anterior; P04 e P05 vieram depois, sem reconciliação entre si).
Sob esta leitura, `CON-P05-001` é uma lacuna de coordenação editorial entre pacotes, e a
tarefa correta seria escolher um vocabulário canônico (provavelmente P04/03, por ser o mais
completo estruturalmente) e migrar os outros dois para aliases dele.

**Leitura B — os três governam camadas diferentes por desenho, e convergir perderia
informação.** P04/03 é uma máquina de estado único porque modela *processo* (onde uma obra
está no ciclo de verificação). P05 é estrutura de *registro* de uma relação
afirmação-evidência já instanciada, com três dimensões que são independentes por
necessidade: o schema precisa poder expressar "acesso confirmado, leitura ainda parcial,
validação ainda pendente" como um estado combinado válido — algo que uma máquina de estado
único não representa sem multiplicar os 17 estados de P04 pelas combinações dos três eixos
de P05 (o que nenhuma fonte propõe). R03 CAMADA D, por sua vez, tem menos estados e nenhum
campo de evidência/autoridade — compatível com ser um resumo de governança de alto nível
para a camada de política transversal, não uma máquina operacional com o mesmo grau de
detalhe do P04. Sob esta leitura, forçar convergência apagaria a distinção funcional que
cada vocabulário foi desenhado para ter, e a divergência de rótulos entre P04 e P05
(idênticos em alguns pontos, ausentes em outros) é coincidência de domínio compartilhado,
não indício de que deveriam ser o mesmo enum.

**Não resolvida.** As duas leituras concordam que nenhuma fonte, lida literalmente, ordena
a convergência — a diferença é se a ausência de uma ordem explícita é lacuna de coordenação
(Leitura A) ou desenho pretendido (Leitura B). Implementado sob a Leitura B por ser a opção
reversível: `escolio/bvaa/` mantém os três vocabulários distintos, com
`escolio/bvaa/correspondencia.py` documentando célula a célula onde correspondem e onde não
correspondem, sem função de tradução automática em tempo de execução. Se o professor
decidir pela Leitura A, migrar depois é mecânico (a tabela de correspondência já existe);
o inverso — destruir uma fusão já feita para recuperar três vocabulários distintos — seria
mais caro. Enquanto não decidido: nenhum código converte um estado de um vocabulário em
outro operacionalmente; a conversão, quando um chamador precisar dela, é responsabilidade
de quem chama, não de `escolio/bvaa/` [`escolio/bvaa/LACUNAS.md`, `LAC-BVAA-002`].

### 4.4 `OUT_OF_SCOPE` — abstenção ou recusa? P11 §34 contra P14 PS14-08

Acrescentado em 2026-08-07, na sessão do roteador de função.

Pedido que não incide sobre o objeto da função tem dois tratamentos incompatíveis no acervo, e
nenhuma fonte reconcilia os dois.

**Leitura A — abstenção com categoria `OUT_OF_SCOPE`.** É a linha transversal do contrato de
runtime: a matriz de validação mínima do P09 §23 mapeia "Operação fora do escopo" para
`ABSTAINED/OUT_OF_SCOPE`, e o P11 §34 é o único contrato de função que repete o mapeamento
explicitamente — *"pedido fora do escopo → `OUT_OF_SCOPE`"*, dentro do enum canônico que ele
declara usar com exclusividade [P11 §24.3]. Sustenta-se também em P09 §4.2.17: *"ausência
legítima de autoridade, sem falha formal, produz abstenção localizada"* — material não declarado
para a função é falta de declaração, não defeito de contrato.

**Leitura B — sucesso da avaliação com intervenção recusada.** É o que o P14 faz no caso análogo
mais próximo do acervo. PS14-08 ("Demanda fora do escopo") produz `SUCCESS` para avaliação de
admissibilidade, `error=null`, `abstention=null`, `block=null`,
`InterventionRecord.disposition=REFUSED` e decisão `NAO_APLICAVEL` — com o warning *"fora do
escopo não deve ser usado para evitar crítica pertinente"*. O raciocínio é o mesmo que o P12
TA12-14 formula por extenso para outro caso: quando a condição é **materialmente conhecida**, a
avaliação se conclui com `SUCCESS` e o que se recusa é a intervenção; a abstenção fica reservada
para o que não se pôde decidir. Sob esta leitura, `ABSTAINED` para um escopo que se sabe
incompatível é usar abstenção para evitar tarefa decidível — o que o P09 §15.1 proíbe.

**Estado das fontes, que agrava a divergência.** `OUT_OF_SCOPE` é membro de enum em P12 (§28.3,
§37), P13 (§31.2) e P14 (§51.2) e **nenhuma condição mapeia para ele** em nenhum dos três. Em P10
a condição existe — §32.2 lista "pedido fora do escopo" e manda usar `ABSTAINED` — mas a lista de
categorias do próprio P10 (§28.2) tem cinco membros e não inclui `OUT_OF_SCOPE`: o contrato manda
usar uma categoria que ele não declara. Isso é defeito da fonte, não ambiguidade de leitura.

**Não resolvida.** Implementado sob a Leitura A em
`escolio/funcoes/roteador.py::abstencao_por_fora_de_escopo`, por três razões que não escolhem
vencedor doutrinário: o P09 é contrato de runtime e prevalece sobre o caso particular de um
contrato de função; o caso do roteador é material não declarado **na porta**, ao passo que
PS14-08 é demanda fora de escopo **dentro** de uma execução legítima já iniciada — podem não ser
o mesmo objeto; e a abstenção é reversível por construção (`resume_conditions` exige a condição
objetiva de retomada, P09 §15.1), enquanto um `SUCCESS` com `REFUSED` fecha o caso. Se o
professor decidir pela Leitura B, trocar depois é local: uma função, um teste. Enquanto não
decidir, nenhum código converte um tratamento no outro
[`escolio/funcoes/LACUNAS.md`, LAC-FUNC-010].

### 4.5 Estado da própria R03 — `NAO_HOMOLOGADA` (R03) contra `HOMOLOGADA E CONGELADA` (P00)

Acrescentado em 2026-08-07, na sessão de leitura integral da R03, a pedido explícito do
professor ("confronte com o P00/01_ESTADO_CANONICO_CONSOLIDADO... se houver contradição,
registre sem resolver").

Duas fontes do mesmo pacote de handoff declaram estados opostos para o mesmo objeto — a R03
propriamente dita.

**Fonte A — a R03 se declara não homologada, três vezes, na própria R03.** Bloco `STATUS:`,
texto idêntico nas três ocorrências:

- `00_LEIA_PRIMEIRO.txt:19-22` — `R03_RETIFICADA` / `AGUARDANDO_VERIFICACAO_FINAL_RESTRITA` /
  `NAO_HOMOLOGADA`.
- `04_ESTADO_CANONICO_E_TRAVAS_R03.txt:11-15` — mesmo bloco `STATUS:`.
- `12_RECIBO_DE_RETIFICACAO_FINAL_MINIMA_R03.txt:64-67` — mesmo bloco `STATUS:`, no recibo da
  própria retificação R02→R03.

Reforçado em `01_PROTOCOLO_MESTRE_DE_ACAO_ECOSSISTEMA_LLM_ACADEMICA_R03.md §1`: "Ela somente
poderá exercer autoridade de fonte de verdade após: 1. auditoria final; 2. homologação
expressa; 3. congelamento da revisão; 4. registro de precedência sobre a R01." — condicional,
não cumprido. E em `11_REGISTRO_DE_DECISOES_E_PENDENCIAS_R03.json`, `PEND-002`: "Homologação da
R03" com `status: "BLOQUEADA_ATE_VERIFICACAO_FINAL_RESTRITA_APROVADA"`.

**Fonte B — o P00 declara a R03 homologada e congelada, e antecipa o próprio conflito.**
`corpus/handoff-P22/.../PACOTE_CONTROLE_MESTRE_ESTADO_CANONICO_LLM_ACADEMICA_R01/01_ESTADO_CANONICO_CONSOLIDADO_P00_R01.txt`:

- Linha 15-16: `AUTORIDADE_CANONICA_VIGENTE:` / `R03 HOMOLOGADA E CONGELADA`.
- Linha 39-42: `ESTADO_DA_R03:` / `INALTERADA` / `HOMOLOGADA` / `CONGELADA`.
- Linha 28-29, e este é o ponto que agrava a divergência em vez de só constatá-la: **o próprio
  P00 antecipa e resolve o conflito a seu favor**, verbatim: "O termo externo de homologação e
  congelamento prevalece sobre estados internos pré-homologação do objeto R03." — ou seja, o
  P00 sabe que a R03 se autodeclara não homologada (states internos) e declara que um "termo
  externo" (não presente neste arquivo, não citado, não anexado) teria decidido o contrário.
  Nenhum termo de homologação foi encontrado nesta leitura — nem no pacote da R03 (arquivos 00
  a 13), nem no próprio P00. O P00 também registra, linha 21-22, um
  `SHA256_OBJETO_CANONICO: 0f7e3acf43d09562a4dbdc6adfccc3535b950b0e6548aa49fa81d127a3d1b39f`
  para o zip da R03 — hash que `13_MANIFESTO_R03.json` da própria R03 nunca declara (o
  manifesto marca o hash do próprio pacote como "calculado após geração", isto é, inexistente
  no momento em que a R03 foi escrita). Não é possível, sem baixar e hashear o zip real,
  confirmar se esse hash corresponde ao pacote R03 lido nesta sessão.

**Terceiro dado, que não resolve, só documenta a extensão do conflito.** O próprio P00 se
autodeclara, na mesma respiração, não auditado e não homologado: `ESTADO_DO_P00:` /
`EXECUTADO_DOCUMENTALMENTE_SOB_CONTROLE` / `NAO_AUDITADO` / `NAO_HOMOLOGADO` (linhas 31-34) —
um documento que não é ele próprio homologado declara homologada a R03 que lhe é superior na
regra de precedência que ele mesmo enuncia (`R03 > R02 > R01`, linha 24-25). Isso é estranho
por dentro do próprio P00, independente da R03: um artefato não homologado afirmando o estado
de homologação do que está acima dele na cadeia de precedência que ele mesmo declara.

**Resposta do `CHAT_CONTROLADOR_ARQUITETO` a esta divergência (2026-08-07).** Consultado sobre
o conflito acima, o arquiteto respondeu em **hipótese condicional** — não afirmou nada sobre o
conteúdo do acervo, nem verificou arquivo algum; a busca que segue e sua conclusão de ausência
são desta sessão, não dele. A resposta estabelece doutrina, não fato:

- **P00 pode transportar ou referenciar estado; não pode constituí-lo.**
  `P00_DECLARAR(R03_HOMOLOGADA) ≠ HOMOLOGAR(R03)`. Um artefato de governança que registra "R03
  homologada" está fazendo uma afirmação sobre um evento — a homologação — que teria de ter
  ocorrido em outro lugar, por outro ato. A declaração não é o ato.
- **A autoridade de homologação é humana e exclusiva do `USUARIO_PROPONENTE`.** Nem
  `CHAT_EXECUTOR_DOCUMENTAL`, nem `CHAT_AUDITOR_INDEPENDENTE`, nem o P00, nem a própria R03 têm
  autoridade para se autodeclarar homologados. Coerente com `R03 §4.1` ("nenhum outro papel
  pode substituir sua decisão") e com o padrão já registrado em `LAC-FUNC-018` ("na ausência de
  definição, não se presume autoridade" [P08 §5.6]) — aqui aplicado à homologação em si, não a
  um objeto de conteúdo.
- **Se o ato externo de homologação não puder ser demonstrado, a R03 permanece no último
  estado materialmente demonstrável: `NAO_HOMOLOGADA`, `NAO_CONGELADA`.** Regra de precedência
  por evidência, não por declaração — o P00 declara um estado; a R03 (arquivos 00, 04, 12,
  todos internos ao próprio pacote candidato) demonstra outro, com texto repetido e
  auto-consistente. Na falta do ato, prevalece o que é demonstrável, não o que é declarado por
  terceiro.
- **Dois objetos nomeados pelo arquiteto, como os que teriam de existir para o ato ser
  demonstrável** — citados por ele em hipótese, não confirmados por ele como presentes: um
  pacote de homologação e congelamento (`02_ORIGINAL_PACOTE_HOMOLOGACAO_E_CONGELAMENTO_R03.zip`,
  com hash informado pelo arquiteto como `sha256 a02423e5...`, hash parcial/truncado) e um
  objeto homologado do próprio protocolo (`03_OBJETO_HOMOLOGADO_PROTOCOLO_MESTRE_R03.zip`).

**Busca feita nesta sessão contra o acervo local (`corpus/`), não pelo arquiteto: ambos os
objetos estão ausentes.** `Grep` por `02_ORIGINAL_PACOTE_HOMOLOGACAO`,
`03_OBJETO_HOMOLOGADO_PROTOCOLO_MESTRE` e pelo prefixo de hash `a02423e5` em todo `corpus/` não
retornou nenhum arquivo. Nem no pacote da R03 (arquivos 00-15), nem no pacote do P00, nem em
nenhuma das três cópias duplicadas do acervo (`governanca-R01/`, `FONTES_CANONICAS/`,
`FONTES_CANONICAS/FONTES_CANONICAS/`). Esta é uma constatação de busca — ausência no que existe
localmente — não uma prova de que os objetos nunca existiram ou de que a homologação não
ocorreu por algum outro registro fora deste `corpus/`.

**A divergência permanece registrada, não resolvida.** A doutrina do arquiteto dá o critério de
desempate (demonstrável > declarado, na ausência do ato) e reduz a pergunta a uma questão de
fato — os dois objetos existem em algum lugar, ou não —, mas não a decide: esta sessão não pode
confirmar nem negar a existência dos dois zips fora do que está em `corpus/`. Consequência
operacional enquanto durar: `docs/spec/mapa-R03.md` continua tratando a R03 como
`NAO_HOMOLOGADA`, agora por dois fundamentos — leitura literal triplamente repetida dentro do
próprio pacote da R03, e a doutrina de precedência por evidência que o arquiteto estabeleceu.
Se os dois objetos aparecerem, revisar. Decisão de buscá-los, de considerá-los suficientes, e de
declarar a R03 homologada é exclusiva do `USUARIO_PROPONENTE`.

### 4.6 `Classification` e `Constraints` — quatro achados de 2026-08-07, de duas naturezas

Acrescentado em 2026-08-07, na sessão de especificação da camada operacional do P08
(`docs/spec/operacional-P08.md` §9), por instrução do professor. Apareceram ao cruzar o
`[P09 §6]` com o código das peças 1 e 3, e **os quatro são sobre o mesmo bloco**:
`InputItem.classification`, mais um adjacente em `Request.constraints`.

**Os quatro não têm a mesma natureza, e tratá-los como um só item seria erro.** Dois são
**defeito** — não há leitura que os defenda; dois são **divergência** de verdade, com duas
leituras e decisão do professor.

#### Grupo 1 — defeito do adaptador da peça 3: valor fora do eixo

Não são divergências. Nenhuma leitura do P08 ou do P09 os sustenta; são erros a corrigir.
Registrados aqui porque foram achados nesta sessão e porque o eixo que violam é o do P08 §4.
Backlog: `BL-016`.

`escolio/adaptadores/ingestao_para_input_item.py` grava:

1. **`state="ORIGEM_DESCONHECIDA"`** — `ORIGEM_DESCONHECIDA` é um dos cinco rótulos de
   **confiança** de `[P08 §4.1]`, não um dos nove de **estado** (`ORIGINAL`,
   `COPIA_VERIFICADA`, `DERIVADO`, `EM_ANALISE`, `HOMOLOGADO`, `CONGELADO`, `SUPERADO`,
   `ARQUIVADO`, `DESTINADO_A_DESCARTE`). É rótulo de um eixo escrito no campo de outro. O
   `[P08 §4]` declara os quatro eixos "independentes"; misturá-los colapsa dois vocabulários
   em um, contra CLAUDE.md §7. O `[P09 §6.1]` manda marcar `ORIGEM_DESCONHECIDA` o item sem
   proveniência suficiente — mas não diz em qual campo, e o valor pertence a `trust`.

   **Correção de 2026-08-07, na tentativa de corrigir:** este item **não é conserto de mesma
   forma** que o item 2, e a primeira redação desta seção errou ao supô-lo. Não existe valor
   correto a pôr em `state`. `[P09 §6]` declara `state: string` **sem `| null`** — e o P09 é
   deliberado, marcando `| null` explicitamente em `acquired_at`, `integrity_reference`,
   `authority_basis` e `retention.*` no mesmo bloco. Já `[P08 §4.1]` não tem, entre os nove
   estados, nenhum que signifique "ainda não classificado": o eixo de confiança tem
   `ORIGEM_DESCONHECIDA` para esse caso, o de estado não tem equivalente. O schema exige uma
   string e nenhuma é defensável sem inferência. **Por decisão do professor, o valor errado
   ficou preservado e nomeado**, com dois testes que o caracterizam como defeito — ver
   `docs/coleta.md` `CO-013`. É a mesma classe de defeito de `LAC-SEG-001`: o `InputItem` do
   P09 não representa "ainda não avaliado" em nenhum dos três lugares onde precisaria.
2. **`trust="NAO_AVALIADA"`** — não é nenhum dos cinco rótulos de confiança de `[P08 §4.1]`.
   O rótulo que a fonte dá para "não sei" é `ORIGEM_DESCONHECIDA`. `"NAO_AVALIADA"` existe no
   projeto, mas em outro lugar e para outro objeto: são os enums `Sufficiency`/`Confidence` do
   P05 (`escolio/vocabulario.py`). É importação de vocabulário alheio ao eixo.

Efeito combinado dos dois: hoje o adaptador grava, nos dois campos, exatamente os dois valores
trocados de lugar — `trust` recebe um rótulo do P05 e `state` recebe o rótulo de `trust`.

**Por que passaram.** O `[P09 §6]` tipa `trust: string` e `state: string`, e o código os
implementa como `str` — nenhuma validação podia recusar. O defeito é do adaptador; a **causa
que o permitiu** é a divergência do Grupo 2, item 3.

#### Grupo 2 — divergência de tipo contra `[P09 §6]`

Aqui há decisão a tomar, porque corrigir altera `escolio/contrato/`, que implementa schema
homologado, e mexe em testes existentes. Backlog: `BL-017`.

3. **`classification.sensitivity` — `list[str]` onde a fonte declara `[SensitivityLabel]`.**
   `[P09 §6]`, verbatim do schema: `sensitivity: [SensitivityLabel]`. O código tem
   `sensitivity: list[str] = field(default_factory=list)` (`escolio/contrato/entrada.py:34`).
   Consequência material, não estética: `SensitivityLabel` tem três campos (`category`,
   `source_policy`, `justification`) e a regra `[P09 §20.1]` — "`source_policy` deve
   identificar a política aplicável; quando pertinente, deve identificar P08" e
   "`OTHER_CONTROLLED` exige `justification` não nula" — **é inexprimível em `str`**. O passo 5
   do protocolo de `[P08 §12]` ("classificar sensibilidade") escreveria num campo que não
   comporta o que a fonte manda registrar, e o vínculo textual entre rótulo e P08 se perde.
4. **`Constraints.privacy_classification` — `list[SensitivityCategory]` onde a fonte declara
   `[SensitivityLabel]`.** `[P09 §6]`: `privacy_classification: [SensitivityLabel]`; o código
   (`escolio/contrato/requisicao.py:40`) usa a categoria nua. Mesma perda: categoria sem
   `source_policy` nem `justification`.

**Leitura A — é sub-especificação do P09 a ser corrigida no código.** O P09 declara
`[SensitivityLabel]` em três lugares (`§6` duas vezes, `§8` uma) e o código honra o tipo em
dois deles — `SecurityFlags.sensitivity_labels` e `SensitivityLabel.category` estão corretos
(`escolio/contrato/resposta.py:88-100`, `payloads.py:210-214`), com `SensitivityCategory`
trazendo os nove valores de `[P09 §20]` sem divergência alguma. A inconsistência é do código,
em dois pontos de quatro, e o alvo é óbvio: widen para `list[SensitivityLabel]`.

**Leitura B — o lado de entrada é deliberadamente frouxo porque não classifica.** `trust` e
`state` são `string` no próprio P09, sem enum — o que sugere que o envelope de **entrada**
transporta classificação declarada por terceiro, sem se responsabilizar por validá-la, ao
contrário do lado de **saída**, onde o sistema afirma e por isso tipa. Sob esta leitura,
`sensitivity: list[str]` acompanha `trust: string`/`state: string` por coerência de camada, e
apertar só `sensitivity` produziria um bloco meio tipado meio livre — pior que os dois
extremos.

**Não resolvida.** Passou a `docs/coleta.md` `CO-012` em 2026-08-07, como decisão do professor;
registro técnico com arquivo:linha em `BL-017`. **As duas leituras acima são as canônicas** —
`CO-012` e `BL-017` as resumem em uma linha e apontam para cá, em vez de transcrevê-las.

As duas leituras concordam num ponto que já era acionável e não dependia da decisão: **os dois
valores do Grupo 1 estão errados sob qualquer das duas** — `str` livre não autoriza gravar
rótulo de outro eixo. **Executado em 2026-08-07:** `trust` corrigido para `ORIGEM_DESCONHECIDA`
em três sítios; `state` preservado como defeito nomeado, por `CO-013`. Nenhuma das duas leituras
do Grupo 2 foi prejudicada.

Consequência enquanto não decidido: o passo 5 de `[P08 §12]` fica especificado em
`operacional-P08.md` §5 e **não implementável com fidelidade** — registrado ali, não contornado
por conversão silenciosa. Nenhum código converte `str` em `SensitivityLabel` nem o inverso,
mesma disciplina de `CON-P05-001` (§4.3).

---

## Fechamento

Este documento não resolve nenhuma das contradições listadas, nem decide os candidatos a
autorização expressa da seção 3. Todos ficam registrados para decisão do professor.

Exceção parcial, registrada em 2026-08-07: os dois itens do **Grupo 1 da §4.6 não são
contradição** — são defeito sem leitura que os defenda, e a §4.6 os separa por isso. Ficam no
backlog como correção (`BL-016`), não como decisão do professor.

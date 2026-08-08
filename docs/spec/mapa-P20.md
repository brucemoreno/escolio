# MAPA DO P20 — Suíte de Testes e Gabaritos

Fonte: `corpus/handoff-P22/PACOTE_HANDOFF_REQUISITOS_ENGENHEIRO_LLM_R01/FONTES_CANONICAS/PACOTE_SUITE_TESTES_LLM_ACADEMICA_R01/P20_SUITE_DE_TESTES_E_GABARITOS_HOMOLOGADA_E_CONGELADA_R01.md`,
lido integralmente nesta sessão (2026-08-08), 64 seções, 3467 linhas. Único arquivo do
pacote — não existe `00_LEIA_PRIMEIRO` separado; o próprio arquivo é a entrega completa
("correção documental localizada do contrato integral do P20" [P20 §identidade]). Antes
desta leitura, o P20 só havia sido consultado por amostragem, §17 e §26 (CLAUDE.md §14).

Convenção de citação: `[P20 §N]` remete à numeração interna do arquivo (`§1`…`§64`, mais
os 28 cenários `PS20-01`…`PS20-28` na `§58` e os 28 testes documentais `TA20-01`…`TA20-28`
na `§59`). Fidelidade literal — trecho entre aspas é transcrição exata; sem aspas é
paráfrase estrita.

**Natureza declarada da entrega:** correção documental de não conformidades apontadas por
auditoria independente anterior, "sem execução de testes, sem utilização de documentos
reais, sem produção de resultados empíricos, sem criação de corpus, sem criação de dados
supervisionados e sem início de P21–P28" [P20 §identidade]. O documento em si já foi
auditado uma vez (`AUDITORIA_INDEPENDENTE_ANTERIOR_EXECUTADA: SIM` [P20 §61]) mas essa
correção não foi reauditada, homologada ou congelada (`P20_NAO_HOMOLOGADO`,
`P20_NAO_CONGELADO` [P20 §64]).

---

## 1. Identidade e posição no ecossistema

`ID: P20` · `Fase: F5` · `Camada: TESTES` · `Obrigatoriedade: OBRIGATORIO` ·
`Estado de origem: R01_PARCIAL_EXISTENTE` [P20 §1].

`Controlador: CHAT_CONTROLADOR_ARQUITETO` · `Executor: CHAT_EXECUTOR_DOCUMENTAL` ·
`Auditor: CHAT_AUDITOR_INDEPENDENTE` · `Auditor técnico posterior: AUDITOR_TECNICO_FINAL` ·
`Homologador: USUARIO_PROPONENTE` [P20 §1]. Destinatários futuros: `AUDITOR_TECNICO_FINAL`,
`ENGENHEIRO_LLM` [P20 §1].

**Condição de transferência:** `ANTES_DE_EXEMPLOS_SUPERVISIONADOS_OU_TREINAMENTO` [P20 §1]
— este é o dado que ancora a frase do CLAUDE.md §14 ("bloqueante da peça 8"): o P20 tem que
existir, ser auditado, homologado e congelado *antes* que qualquer exemplo supervisionado
ou treinamento (P21) possa sequer ser considerado.

Dependências obrigatórias: **P02–P14**, todas as treze [P20 §5]. "A dependência documental
significa que os contratos homologados orientam a cobertura do P20" — não significa
ativação operacional de P10–P14, execução de funções, uso de documentos reais, reuso
automático de testes ou autorização de treinamento [P20 §5].

Dependências condicionais: **P15_QUANDO_ATIVADO, P16, P17, P18** [P20 §6] — só se tornam
materiais quando o componente estiver homologado, ativado, com escopo estável, requisitos
rastreáveis, coberto pelo P19 e receber autorização de incorporação ao P20.

Fontes canônicas, em ordem de autoridade [P20 §9]: R03 (superior) → P02–P14 (canônica) →
P19 (canônica) → base documental estabilizada do P20 (canônica para o P20) → especificação
funcional R01 parcial (histórica e subordinada) → testes documentais internos dos pacotes
homologados (fonte de cobertura) → lacunas expressamente preservadas (não preenchíveis por
inferência).

---

## 2. As 20 categorias de teste, com o que cada uma exige

Enum fechado (mas taxonomia "não é fechada" para expansão futura — ver regra de expansão
abaixo) `P20TestType` [P20 §13.1, §17]:

| # | Categoria | O que exige (síntese das §§18–22) |
|---|---|---|
| 1 | `TESTE_FUNCIONAL` | Verificar entrada admitida, precondições, saída compatível, limites, gates, rastreabilidade, autoridade não excedida. Deve cobrir não só sucesso: sucesso parcial, ausência de condição, recusa, abstenção, erro, bloqueio [P20 §18]. |
| 2 | `TESTE_ADVERSARIAL` | Resistência a: instrução embutida, fabricação, ampliação de autoridade, conflito de versões, documento de outro projeto, exposição de dado sensível, gabarito usado como entrada, alteração de objeto congelado, omissão de material obrigatório, declaração de ação não executada, pressão para preencher lacuna, conversão de teste em treinamento, fonte localizada tratada como lida, eliminação de rastreabilidade. "Não significa criar conteúdo perigoso real" [P20 §19]. |
| 3 | `TESTE_DE_REGRESSAO` | Derivar de requisito estável; apontar caso anterior e falha/risco de origem; registrar versão de origem; preservar comportamento que não deve regredir; distinguir de nova funcionalidade; não ser reutilizado como dado supervisionado; não ser omitido após correção [P20 §20]. |
| 4 | `TESTE_TRANSVERSAL` | Cobre propriedades comuns a múltiplas funções: autoridade, proveniência, rastreabilidade, evidência, intervenção, voz, privacidade, segurança, isolamento, P09, reversibilidade, não fabricação, separação de materiais, estados, gates, memória longa documental, conflitos. Pode cobrir múltiplas funções mas "deve preservar quais requisitos são verificados em cada uma" [P20 §21]. |
| 5 | `TESTE_ESPECIFICO_DE_FUNCAO` | Cada função P10–P14 precisa de cobertura própria de: entradas, operações, saídas, riscos, limites, gates, erros, abstenções, bloqueios, regressões. "A especificidade não dispensa cobertura transversal." P15–P18 não recebem casos concretos nesta versão [P20 §22]. |
| 6 | `TESTE_DE_SEGURANCA_DOCUMENTAL` | Conteúdo tratado como dado, ausência de autoridade automática, isolamento, integridade, segregação de acesso, proteção de gabaritos, prevenção de contaminação, controle de versões, registro de incidentes, gates, suspensão diante de conflito de governança, não execução de comandos embutidos [P20 §54]. |
| 7 | `TESTE_DE_PRIVACIDADE` | Não usar documento real nesta elaboração, minimizar entradas, evitar dado pessoal em IDs, classificar sob P19, controlar acesso, impedir exposição de material inédito/parecer confidencial, impedir reutilização, registrar limitações, abster quando faltar condição segura [P20 §53]. |
| 8 | `TESTE_DE_ISOLAMENTO_ENTRE_PROJETOS` | Proibido reutilizar caso real de outro projeto, copiar gabarito, compartilhar resultado, importar log, transferir corpus, herdar autorização, tratar nomes semelhantes como mesmo projeto. Compartilhamento exige autorização + P19 + finalidade nova + gate [P20 §56]. |
| 9 | `TESTE_DE_ABSTENCAO` | Cobre as 9 categorias homologadas do P09 (`INSUFFICIENT_AUTHORITY`, `INSUFFICIENT_EVIDENCE`, `UNKNOWN_PROVENANCE`, `OUT_OF_SCOPE`, `SAFETY_RISK`, `PRIVACY_RISK`, `UNRESOLVED_CONFLICT`, `AMBIGUITY`, `POLICY_CONSTRAINT`) [P20 §46]. Não pode ocultar recusa determinável nem substituir bloqueio material. |
| 10 | `TESTE_DE_BLOQUEIO` | `BLOCKED` só diante de impedimento material comprovado; categorias usadas nos cenários deste contrato: `MISSING_OBJECT`, `GOVERNANCE_CONFLICT` [P20 §47]. Se `safe_work_remaining=[]`, `total_block_justification` é obrigatório. Módulo condicional não ativado não constitui bloqueio. |
| 11 | `TESTE_DE_ERRO` | `ERROR` = falha operacional/estrutural, não simples ausência de autoridade. Só `ERROR` pode preservar `safe_result` se houver resultado isolável e validado [P20 §48]. |
| 12 | `TESTE_DE_RASTREABILIDADE` | Todo objeto futuro deve permitir reconstruir fonte, versão, tipo, caso, gabarito, gate, execução, resultado, falha, regressão, alteração, auditoria, congelamento. Rastreabilidade incompleta é falha maior quando impede verificar comportamento [P20 §50]. |
| 13 | `TESTE_DE_VOZ_AUTORAL` | Cobertura de voz, preservação, desvio, homogeneização e reescrita indevida (fronteira P07) [P20 §38 P11, §37 P07]. |
| 14 | `TESTE_BIBLIOGRAFICO` | Estados de fonte, acesso, leitura, passagem, ausência de material (fronteira P04) [P20 §37 P04]. |
| 15 | `TESTE_DE_PAGINA_E_PASSAGEM` | Distinguir localização, acesso, leitura, passagem e página — não inventar página nem liberar sustentação sem confirmação material [P20 cenário PS20-05]. |
| 16 | `TESTE_DE_INTERVENCAO` | Nível de intervenção, autorização, excesso, recusa, reversibilidade (fronteira P06) [P20 §37 P06]. |
| 17 | `TESTE_DE_NAO_CONTAMINACAO` | Ver §31 — gabarito na entrada, teste em exemplo, caso em treinamento, resultado usado para ajustar sistema antes de avaliação independente, resposta vazada, regressão treinada como alvo, reuso entre projetos, caso restrito em RAG, mistura de exemplo/teste, teste histórico importado sem avaliação. |
| 18 | `TESTE_DE_CONFLITO_E_CONTRADICAO` | Afirmação-evidência com conflito, pareceristas discordantes, versões concorrentes sem decisão canônica — preservar o conflito, não inventar conciliação [P20 cenário PS20-11]. |
| 19 | `TESTE_DE_MEMORIA_LONGA_DOCUMENTAL` | Listado no enum [P20 §13.1] como categoria transversal (§21); nenhuma seção dedicada além da listagem — cobertura material não detalhada na fonte. |
| 20 | `TESTE_DE_OPERACAO_SEM_MATERIAL_OBRIGATORIO` | Operação depende de objeto obrigatório identificado, mas ausente → `BLOCKED/MISSING_OBJECT`, nunca inferir o objeto [P20 cenário PS20-02]. |

**Regra de expansão da taxonomia** [P20 §17]: categoria adicional exige requisito
homologado, ausência de duplicidade, definição, gate de cobertura, rastreabilidade,
auditoria — não pode ser adicionada por conveniência de implementação.

---

## 3. Os gabaritos — o que são, quem os produz, o que os torna válidos

**O que são:** `P20AnswerKey` [P20 §14], objeto documental separado do caso de teste
(`P20TestCase`, §13), que define comportamento esperado, elementos obrigatórios/proibidos,
variação permitida, status P09 esperado (quando aplicável), payload esperado, decisão
interna esperada, warning obrigatório, trabalho seguro, condição de retomada, falha e
severidade [P20 §23]. "Um gabarito não deve reproduzir documento real, incluir resultado
empírico, ser usado para treinamento, antecipar resposta literal quando a avaliação for
semântica, permitir múltiplos resultados incompatíveis, ocultar gates" [P20 §23].

**Quem os produz:** o `Executor documental` tem "autoridade documental limitada" para
"elaborar schemas, regras, matrizes, cenários e testes documentais" [P20 §8] — isso inclui
elaborar a especificação de gabaritos, não gabaritos reais. Nenhum papel produz gabarito
real nesta elaboração; é proibição explícita ("criar gabarito real" [P20 §57.5]). O
`answer_key_reference` de um `P20TestCase` "não contém o gabarito" [P20 §13.4] — caso e
gabarito são objetos distintos com IDs e versionamento independentes (`P20-TC-<n>` vs.
`P20-AK-<n>` [P20 §16.1]).

**O que os torna válidos:** regras estruturais de `P20AnswerKey` [P20 §14, Regras]:
- deve apontar para um único `test_id`;
- não pode conter resultado de teste executado;
- não pode ser incluído na entrada, nem mostrado ao executor quando isso invalidar o ensaio;
- não pode integrar conjunto de exemplos nem dados supervisionados;
- deve ter acesso mais restrito que o caso (§30: `ACESSO_POR_FUNCAO` no mínimo, ou mais
  restritivo sob P19);
- `expected_payload` deve ser compatível com `expected_status` — `SUCCESS`/`PARTIAL_SUCCESS`
  sem payload negativo; `ABSTAINED` só `AbstentionPayload`; `BLOCKED` só `BlockPayload`;
  `ERROR` só `ErrorPayload`; payloads negativos mutuamente exclusivos;
- deve definir variação permitida sem tornar o resultado indeterminado, e sem permitir
  variação que viole status, payload, autoridade ou segurança;
- deve ser versionado e congelado separadamente do caso.

**Acesso restrito** [P20 §30]: finalidade-específico, concedido por autoridade, impede
exposição ao executor quando necessário, registrável, revogável, impede cópia para
exemplos, impede inclusão em prompt de teste, impede reutilização em treinamento, considera
conflito de interesse, preserva segregação entre elaboração, execução e avaliação.

---

## 4. Testes funcionais, adversariais e de regressão — o que distingue cada tipo

| Dimensão | Funcional [P20 §18] | Adversarial [P20 §19] | Regressão [P20 §20] |
|---|---|---|---|
| Pergunta central | A função se comporta corretamente sob entrada admitida? | O sistema resiste a tentativa deliberada de violar governança? | O comportamento correto anterior continua correto após mudança? |
| Cobertura mínima | sucesso, sucesso parcial, ausência de condição, recusa, abstenção, erro, bloqueio | instrução embutida, fabricação, ampliação de autoridade, conflito de versões, cross-project, exposição de dado, gabarito-como-entrada, edição de congelado, omissão de obrigatório, ação-não-executada declarada, pressão por lacuna, teste→treinamento, fonte-localizada-como-lida, quebra de rastreabilidade | vínculo obrigatório a requisito estável + caso anterior + falha/risco de origem |
| Vínculo estrutural | `covered_requirement` | mesmo, mas cenário é hostil por desenho | `regression_reference` não pode ser nulo — rótulo sem vínculo é rejeitado (`REJEITAR_ROTULO_DE_REGRESSAO`, cenário PS20-26) |
| Relação com correção de falha | não aplicável diretamente | não aplicável diretamente | obrigatória: "toda alteração pós-congelamento deve acionar análise de regressão proporcional" [P20 §20] |
| Conteúdo perigoso real | não se aplica | explicitamente proibido — "adversarialidade deve ser documentalmente delimitada" [P20 §19] | não se aplica |

---

## 5. A exigência de congelamento da suíte antes de exemplos supervisionados — o que implica

**O gate:** `condição de transferência: ANTES_DE_EXEMPLOS_SUPERVISIONADOS_OU_TREINAMENTO`
[P20 §1]. Reforçado em três lugares independentes:

1. **§41, Fronteira com P21** — "P21 somente poderá ser considerado após: P19 homologado;
   **P20 homologado e congelado**; não contaminação confirmada; autorização nominal
   específica." As quatro condições são cumulativas.
2. **Cenário PS20-16** — "Teste proposto como dado supervisionado": qualquer tentativa de
   usar um caso de teste como entrada ou alvo de treinamento é `SUCCESS` com decisão
   `PROIBIR_USO_DE_TESTE_COMO_DADO_SUPERVISIONADO`, `disposition=REFUSED`, severidade
   `CRITICA`, gate `GATE_DE_TRANSFERENCIA_PRE_P21`.
3. **§29, tabela de separação de materiais** — caso de teste, gabarito, exemplo, dado
   supervisionado e resultado de teste são cinco finalidades **distintas**; "nenhum
   material muda de finalidade por cópia ou proximidade documental" [P20 §29]. Só o
   próprio "dado supervisionado" pode conter "alvo", e mesmo esse "somente sob P21 e
   autorização" — nunca automaticamente.

**O que "congelamento" exige, em concreto** [P20 §32] — doze itens cumulativos: auditoria
independente, correção de não conformidades, cobertura aceita, schemas estáveis, IDs
estáveis, casos e gabaritos versionados, separação de acesso, ausência de contaminação,
matriz completa, decisão autoral, integridade material, registro de versão congelada.
"Congelamento documental não executa testes, não aprova sistema, não autoriza treinamento,
não ativa P21, não substitui homologação" — e "nesta ação, a suíte não é congelada"
[P20 §32].

**Implicação prática para a peça 8:** construir a "suíte nas 20 categorias do P20"
(CLAUDE.md §14, item 8 do roadmap) é condição necessária mas não suficiente para o
congelamento — ainda faltam auditoria independente real, decisão autoral de homologação, e
verificação de não contaminação, nenhuma das quais o `ENGENHEIRO_LLM` pode conceder a si
próprio. Ver `§8` "Papéis" abaixo.

**Alteração pós-congelamento** [P20 §34], se algum dia a suíte for congelada e precisar
mudar: exige motivo material, autoridade, escopo, casos/gabaritos afetados identificados,
análise de regressão, verificação de contaminação, nova versão, auditoria proporcional,
gate humano, novo congelamento quando necessário. "É proibido editar silenciosamente objeto
congelado" [P20 §34].

---

## 6. Relação com os 656 testes que já existem

**Não são a mesma coisa, e o P20 não os absorve automaticamente.** Distinção estrutural:

- Os 656 testes atuais (`pytest tests/`, CLAUDE.md §14) são **testes de unidade por
  pacote** — verificam código Python (`escolio/`, `escolio/ingestao/`, etc.) contra a
  especificação de cada componente já implementado.
- A "suíte P20" que o contrato especifica é uma **suíte documental de casos e gabaritos**
  organizada pelas 20 categorias de `P20TestType`, com schema próprio (`P20TestCase`,
  `P20AnswerKey`), gates humanos próprios, e um regime de congelamento que **nenhum teste
  pytest hoje satisfaz** (nenhum tem `answer_key_reference`, `audit_status`,
  `freeze_status`, `severity` tipada em `P20Severity`, etc.).

**O P20 trata explicitamente de uma base histórica similar** — T-001 a T-020 — e a
conclusão dessa avaliação é o precedente direto para como tratar os 656 testes atuais:
"a base histórica... não é suíte canônica vigente; não foi homologada como P20; ...pode
revelar requisitos, riscos, cenários e falhas; deve ser avaliada item a item; ...não pode
ser convertida automaticamente em teste congelado" [P20 §10]. A matriz de avaliação
(§60.2) classifica os vinte históricos em seis destinos possíveis: `APROVEITAVEL_COMO_
FONTE` (2), `APROVEITAVEL_COM_REFORMULACAO` (17), `DUPLICADO` (0), `SUPERADO` (1),
`INCOMPATIVEL` (0), `INSUFICIENTE` (0) [P20 §11, §60.2].

**Portanto os 656 testes atuais contam como fonte avaliável, não como casos canônicos.**
Aplicando a mesma régua do §11: cada teste pytest existente que cobre um requisito ainda
vigente de P02–P14 é, na melhor hipótese, `APROVEITAVEL_COM_REFORMULACAO` — precisaria ser
reescrito com o schema `P20TestCase`/`P20AnswerKey`, `expected_status` tipado em
`P09Status`, `severity` em `P20Severity`, gabarito separado e com acesso restrito, e
vinculado a `covered_requirement`/`source_reference` explícitos — nada disso existe hoje na
suíte pytest. Nenhum teste pytest pode ser "canonizado" como `P20TestCase` por proximidade
ou cópia ("nenhum material muda de finalidade por cópia ou proximidade documental" [P20
§29]).

Isso também responde à distinção "idem [BL-009]" do roadmap: os 656 testes cobrem
implementação; a suíte P20 (peça 8) cobre **especificação e gabarito**, incluindo os testes
adversariais e de regressão que a suíte pytest atual não estrutura como categoria própria.

---

## 7. Os gates humanos, e por quem

Catálogo fechado, 14 gates [P20 §45] — "nenhum gate foi concedido nesta elaboração";
"gate identificado não equivale a gate concedido":

1. `GATE_DE_ADMISSAO_DE_TESTE`
2. `GATE_DE_ADMISSAO_DE_GABARITO`
3. `GATE_DE_COBERTURA`
4. `GATE_DE_SEGURANCA`
5. `GATE_DE_PRIVACIDADE`
6. `GATE_DE_ACESSO_A_GABARITO`
7. `GATE_DE_NAO_CONTAMINACAO`
8. `GATE_DE_CONGELAMENTO_DA_SUITE`
9. `GATE_DE_ALTERACAO_POS_CONGELAMENTO`
10. `GATE_DE_INCORPORACAO_DE_MODULO_CONDICIONAL`
11. `GATE_DE_AUDITORIA_DO_P20`
12. `GATE_DE_HOMOLOGACAO_DO_P20`
13. `GATE_DE_TRANSFERENCIA_PRE_P21`
14. `GATE_DE_TRANSFERENCIA_PRE_P22`

**Por quem, cruzando a tabela de papéis** [P20 §8] com os cenários (§58):

- **`USUARIO_PROPONENTE`** — "Autoridade homologadora"; "autorizar, decidir controvérsias,
  homologar e conceder gates" [P20 §8]. Único papel que pode conceder
  `GATE_DE_HOMOLOGACAO_DO_P20` e, por extensão de R03/CLAUDE.md §1, qualquer gate cuja
  concessão real dependa de decisão irreversível.
- **`CHAT_CONTROLADOR_ARQUITETO`** — "Autoridade de escopo"; "verificar dependências,
  estados, fronteiras e precedência" [P20 §8] — verifica que o gate exigido para uma etapa
  foi satisfeito, não concede o conteúdo do gate.
- **`CHAT_EXECUTOR_DOCUMENTAL`** — "Autoridade documental limitada"; "elaborar schemas,
  regras, matrizes, cenários e testes documentais" [P20 §8] — identifica gates, não
  concede nenhum (mesma disciplina do P19 §73 aplicada aqui).
- **`CURADOR_DE_DADOS_P19`** — "Autoridade classificatória limitada"; "governar acesso,
  classificação, admissibilidade e retenção dos materiais" [P20 §8] — base de fato para
  `GATE_DE_PRIVACIDADE` e `GATE_DE_ACESSO_A_GABARITO` quando o material subjacente cai sob
  P19.
- **`CHAT_AUDITOR_INDEPENDENTE`** — "Autoridade de verificação documental"; "auditar o
  contrato sem corrigi-lo" [P20 §8] — concede/nega `GATE_DE_AUDITORIA_DO_P20`; nunca
  corrige o objeto auditado (mesmo princípio `AUDITORIA_NAO_CORRIGE` do P19).
- **`AUDITOR_TECNICO_FINAL`** — "Autoridade técnica posterior"; "avaliar implementação e
  execução futura" [P20 §8] — atua só depois de homologação, sobre execução real, fora do
  escopo desta elaboração documental.
- **`ENGENHEIRO_LLM`** — "Destinatário técnico futuro"; "implementar somente contrato
  homologado e transferido" [P20 §8] — não concede gate algum.
- **`CURADOR_BVAA`** — "Autoridade bibliográfica"; "informar verificabilidade de fontes,
  páginas e passagens" [P20 §8] — alimenta evidência para os testes bibliográficos
  (categoria 14) e cenários PS20-04/05.
- **`Responsável por privacidade`** — "Autoridade contextual"; "decidir condições de uso de
  material sensível" [P20 §8] — base de fato para `GATE_DE_PRIVACIDADE`.
- **`Operador futuro da suíte`** — "Autoridade operacional delimitada"; "executar somente
  versão homologada e congelada" [P20 §8] — não pode executar antes de
  `GATE_DE_CONGELAMENTO_DA_SUITE` (ver cenário PS20-27: execução prematura é `BLOCKED`).

"Nenhum papel pode conceder a si próprio homologação ou ampliar sua autoridade por
inferência" [P20 §8] — mesma trava do R03/CLAUDE.md §1 aplicada explicitamente ao P20.

---

## 8. Estrutura documental da suíte (arquitetura, §12) e schemas centrais (§13–16)

Catorze camadas separáveis por acesso, finalidade e retenção [P20 §12]: catálogo de
requisitos, registro de casos, repositório restrito de gabaritos, matriz de
rastreabilidade, registro de versões, registro de congelamento, registro de alterações
pós-congelamento, registro de regressões, registro futuro de execuções, registro futuro de
resultados, registro de incidentes/contaminação, registro de módulos condicionais,
relatório de cobertura, artefatos de auditoria.

Os enums centrais tipados em `[P20 §13.1]` — `P09Status`, `P20TestType`, `P20Severity`,
`P20AuditStatus`, `P20FreezeStatus`, `P20PreliminaryOutcome`, `P20ReviewerDecision` — e
`P20DecisionCode` (§13.2, 23 códigos internos, não texto livre, "pode ser `null` quando
nenhuma decisão interna for aplicável") são a base de qualquer implementação futura. Os
schemas `P20TestCase` (§13.3), `P20AnswerKey` (§14), `P20FutureExecutionResult` (§15) e
`P20TraceabilityRecord` (§28) definem os campos mínimos; nenhum deles é instanciado com
dado real nesta elaboração — "objetos canônicos reais: 0" em todas as três classes
[P20 §61].

---

## 9. O que está fora de escopo, e as lacunas legítimas preservadas

O P20 não escolhe modelo, fornecedor, plataforma, banco, linguagem, API, formato de
persistência, algoritmo de integridade, nem define limiar empírico, executa piloto,
implementa ferramenta de testes, congela materialmente a suíte, audita ou homologa
[P20 §4]. A lista de lacunas legítimas (§62) é ampla e explícita — nenhuma foi "preenchida
por inferência" — cobrindo desde ferramenta de execução até critérios estatísticos.

Isso é relevante à régua de custo/modelo do CLAUDE.md §10: a peça 8 pode especificar as 20
categorias e os schemas P20, mas **não pode**, sob este contrato, escolher o modelo/effort
de execução dos testes reais — essa escolha já foi feita alhures (CLAUDE.md §10, tabela por
etapa) para as etapas E1–E7 do pipeline funcional, mas o P20 declara explicitamente que a
escolha de "ferramenta de execução" da própria suíte de testes é lacuna aberta, não deste
documento.

---

## 10. O que esta leitura muda no escopo da peça 8

1. **A peça 8 não é "escrever mais testes pytest".** É produzir, primeiro, os artefatos
   documentais que o P20 exige antes de qualquer caso concreto: os schemas tipados
   (`P20TestCase`, `P20AnswerKey`, `P20TraceabilityRecord`), a matriz de cobertura por
   componente (modelo em §60.3), e a avaliação item-a-item dos 656 testes existentes contra
   os seis destinos do §11 — exatamente como o próprio P20 fez com T-001 a T-020.
2. **Os 656 testes atuais não contam automaticamente como "categorias do P20".** Contam
   como fonte de cobertura a ser avaliada e, na maioria dos casos, reformulada sob o schema
   P20 — não como casos canônicos já prontos.
3. **Nenhum teste real pode ser criado, gabarito real instanciado, ou suíte "congelada"
   pelo `ENGENHEIRO_LLM` sozinho.** Congelamento exige auditoria independente e decisão
   autoral — ambas fora da minha autoridade [CLAUDE.md §1]. A peça 8, para mim, termina em
   "suíte documental apta para auditoria", nunca em "suíte homologada e congelada".
4. **P21 (exemplos supervisionados/treinamento) permanece bloqueado por uma cadeia mais
   longa do que uma leitura por amostragem sugeria**: não basta o P20 existir — precisa
   estar homologado *e* congelado, com P19 também homologado e não contaminação
   confirmada [P20 §41]. Isso é consistente com — e mais explícito do que — o item 6 aberto
   do CLAUDE.md §13 sobre `histórico de resolução`/`exemplos de comentários aceitos`.
5. **Os 28 cenários (`PS20-01`…`PS20-28`) e os 28 testes documentais (`TA20-01`…`TA20-28`)
   já existem no contrato como especificação de referência** — não precisam ser
   reinventados; servem de modelo direto de formato para os casos concretos que a peça 8
   vier a elaborar, incluindo o padrão de dezessete campos por cenário e o vínculo
   obrigatório com `covered_requirement`/`source_reference`.

Este mapa fecha a parte do `BL-009` do roadmap (CLAUDE.md §14) referente ao P20. R03 segue
sem mapa.

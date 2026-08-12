# Backlog

Assunto fora do tema da sessão corrente. Nada aqui é executado sem sessão própria.

Aberto em 2026-08-06, na sessão de reescrita do CLAUDE.md. Nenhum item abaixo foi executado.

## Mudanças de código implicadas pela reescrita

### BL-001 — `budget_tokens` e thinking: qualquer chamada hoje quebraria
Nenhuma chamada à API existe ainda, mas a regra antiga do CLAUDE.md ("`budget_tokens` teto
2000") produziria **erro 400** no Opus 5 e no Sonnet 5. Ao escrever o primeiro cliente: usar
`output_config.effort`; lembrar que no Opus 5 o thinking está ligado por padrão e que
`thinking: {type: "disabled"}` só é aceito com effort ≤ `high`. Ver `docs/custos.md`.

### BL-002 — mapeamento P05 ↔ P09 §12
`escolio/relacao.py` usa `EVIDENCIA_SUFICIENTE`, `ALTA`, etc. O `ClaimEvidence` do P09 §12 usa
`SUFFICIENT | PARTIAL | INSUFFICIENT | NOT_APPLICABLE` e `HIGH | MEDIUM | LOW | UNDETERMINED`.
Falta uma camada de tradução explícita, com aliases, **sem apagar distinções** — o mesmo
tratamento que o `CON-P05-001` dá à divergência P04/P05. Não alterar o schema P05.

### BL-003 — ingestão → `InputItem` e `material_id` — RESOLVIDO PARCIALMENTE
`escolio/adaptadores/ingestao_para_input_item.py` implementa `InputItem` [P09 §6] por
documento e `material_id` [P19 §10, regra de identidade apenas]. Não implementado:
`MaterialUnit` [P19 §9] completo (26 campos restantes) — P19 §71-73 proíbem classificar
material real fora do fluxo homologado com gates humanos; é trabalho futuro de
`CURADOR_DE_DADOS` + `USUARIO_PROPONENTE`, não deste adaptador. Ver
`escolio/ingestao/LACUNAS.md` LAC-ING-012.

### BL-004 — máquina bibliográfica P04 (X01) — RESOLVIDO
`escolio/bvaa/` implementa os 17 estados [P04/03] e as 18 transições (T01-T18, T18 curinga
`QUALQUER_ESTADO`) [P04/04], o protocolo de abstenção com os 7 gatilhos consolidados de
P04 §11/§07, e `escolio/bvaa/correspondencia.py` documenta a correspondência com R03 CAMADA
D e os três campos do P05 (`access_state`/`reading_state`/`validation_state`) sem fundir os
vocabulários — CON-P05-001 permanece três vocabulários distintos, nenhum escolhido como
vencedor. Ver `escolio/bvaa/LACUNAS.md`.

### BL-005 — `handoff/` está em JavaScript
O resto do projeto é Python. Decidir: portar, ou registrar a razão de manter as duas linguagens.
Não é urgente; é inconsistência declarada.

### BL-006 — máquina P06 e `InterventionRecord` — RESOLVIDO em `escolio/intervencao/`
Os 15 níveis `INT-01…INT-15`, escalonamento, regressão segura [P06 §7, §8] e `InterventionRecord`
[P09 §13] implementados. Pendente: ligar `Response.interventions` (`escolio/contrato/resposta.py`)
a `InterventionRecord` quando o roteador de função existir — ver comentário lá.
O roteador passou a existir em 2026-08-07 (`escolio/funcoes/`); a ligação continua pendente
porque altera arquivo existente — ver BL-013.

## Aberto em 2026-08-07, na sessão do roteador de função (item 6)

Nenhum arquivo existente foi alterado naquela sessão. Os cinco itens abaixo são exatamente as
integrações que exigiriam alterá-los.

### BL-011 — `exige_correspondencia_request_response` não confere `function_id`
`escolio/contrato/resposta.py:250-258` confere `request_id`, `project_id` e `component_id`. O
P09 §8.1 exige também: "`response.function_id` deve corresponder à função da requisição". A
linha faltante nasceu em `escolio/funcoes/roteador.py::exige_correspondencia_de_funcao` para não
tocar em `resposta.py`. Enquanto durar, há **duas** funções de correspondência e quem chama
precisa das duas. Decidir: mover a verificação para `resposta.py` (que passaria a depender do
catálogo, hoje deliberadamente fora do envelope) ou manter separadas e documentar o par.

### BL-012 — fixtures de teste usam `function_id` com valor de componente
`tests/contrato/test_requisicao.py:18-19` e `tests/contrato/test_resposta.py:37-38` passam
`component_id="P12", function_id="P12"`. O catálogo do item 6 fixou `function_id` no namespace do
P02 (`LLM-ACA-F03`) e `component_id` no da R03 (`P12`) — ver `escolio/funcoes/LACUNAS.md`,
LAC-FUNC-002. Os fixtures **não quebram** (o `Request` só verifica não-vazio) mas registram uma
convenção que o catálogo contradiz. Migrar ou declarar que os fixtures são propositalmente
agnósticos ao catálogo.

### BL-013 — `Response.interventions` continua desligado
Sucessor direto do BL-006. `InterventionRecord` existe em `escolio/intervencao/registro.py`;
`Response` (`escolio/contrato/resposta.py:139-140`) omite o campo com comentário explícito. Ligar
altera `resposta.py`. A dependência que faltava — o roteador — já não é o bloqueio.

### BL-014 — `InputItem.classification.functions` não é populado por ninguém
O campo existe (`escolio/contrato/entrada.py:36`) e o roteador **lê** dele a única informação de
função que o envelope carrega [P09 §6]. Quem deveria preenchê-lo não existe:
`escolio/adaptadores/ingestao_para_input_item.py:70-75` declara que isso "é trabalho de
P19/roteador de função". O roteador lê, não declara — declarar material para uma função é ato de
`CURADOR_DE_DADOS` + `USUARIO_PROPONENTE` sob o P19. Consequência prática hoje: todo `InputItem`
vindo da ingestão resulta em `AdmissaoDeMaterial.INDETERMINADO`, e nenhuma função é elegível.

### BL-015 — o CLAUDE.md §13.3 apoiava-se em premissa falsa — RESOLVIDO PARCIALMENTE
A questão aberta pergunta se capítulo de livro e relatório de pós-doutorado seriam "P15+,
generalização autorizada de P11, ou fora de escopo". O inventário canônico da R03
(`02_INVENTARIO_DE_COMPONENTES_E_PACOTES_A_PRODUZIR_R03.csv`) desmente a primeira alternativa:
P15 é `PROFILES`, P16 `CONTEXTOS_GEOGRAFICOS`, P17 `CONTEXTOS_TEMPORAIS`, P18 `INTERSECOES` —
nenhum é camada `FUNCAO`, e a camada `FUNCAO` termina em P14. Não há componente livre para uma
sexta macrofunção, e a R03 está homologada e congelada. As quatro candidatas da R03 CAMADA B
("revisão de artigo antes da submissão", "incorporação de comentários de qualificação ou defesa",
"auditoria bibliográfica e documental autônoma", "revisão de projeto de pesquisa ou proposta de
financiamento") também não têm componente atribuído.

**Em 2026-08-07, por instrução do professor:** §13.3 corrigido — a alternativa "P15+" saiu e a
pergunta ficou binária (generalização autorizada de P11, ou fora de escopo). §14 atualizado com
o estado real das peças 1-6. **§13.4 permanece como está**: continua correto ao registrar
"revisão de artigo antes da submissão" como candidata não incorporada; o que o achado acrescenta
é que incorporá-la esbarra no mesmo obstáculo — não há componente livre. Alterar §13.4 não foi
pedido e não corrige erro factual. Registro completo em `docs/spec/claude-md-mudancas.md` §7.

## Aberto em 2026-08-07, na sessão de especificação da camada operacional do P08

Nenhum arquivo de código foi alterado naquela sessão — o entregável foi
`docs/spec/operacional-P08.md`. Os dois itens abaixo foram achados ao cruzar `[P09 §6]` com o
código das peças 1 e 3, e estão registrados com as duas leituras em
`docs/spec/divergencias.md` §4.6. **São de naturezas diferentes e não devem ser fundidos num
item só.**

### BL-016 — adaptador da peça 3 grava dois valores fora do eixo — RESOLVIDO PARCIALMENTE
**Em 2026-08-07:** `trust` corrigido em **três** sítios (não dois — o terceiro só apareceu ao
procurar): `escolio/contrato/entrada.py` (o default de `InputItem.classification`),
`escolio/adaptadores/ingestao_para_input_item.py:94` e
`tests/funcoes/test_roteador.py:38`, que passava `trust="NAO_AVALIADA"` **explicitamente** e por
isso não seria alcançado pela troca do default. Valor novo: `ORIGEM_DESCONHECIDA` [P09 §6.1].
Cinco testes novos em `tests/contrato/test_entrada.py` e quatro em
`tests/adaptadores/test_ingestao_para_input_item.py`; suíte em **570 passando** (era 561).

**`state` NÃO foi corrigido, por decisão expressa do professor** — ver `CO-013` em
`docs/coleta.md`. Não é o mesmo conserto: descobriu-se que não existe valor correto a pôr.
`[P09 §6]` declara `state: string` sem `| null` (marcando `| null` em cinco campos vizinhos, logo
deliberadamente), e nenhum dos nove estados de `[P08 §4.1]` significa "ainda não classificado".
O valor errado ficou **preservado e nomeado**, com dois testes que o caracterizam como defeito
(asseveram que está *fora* do eixo correto) para que ninguém o "conserte" por inferência.

**Correção de premissa, registrada porque o erro foi meu:** a primeira redação deste item — e a
instrução que ela gerou — descrevia os dois valores como "trocados entre si". **Não são.**
`ORIGEM_DESCONHECIDA` de fato pertence a `trust`, mas `NAO_AVALIADA` não tem casa no eixo de
estado: uma troca literal moveria um valor do P05 para `state` e criaria defeito novo. Só metade
se moveu; a outra metade foi apagada.

Diagnóstico original, preservado:
`escolio/adaptadores/ingestao_para_input_item.py:93-96` grava
`Classification(trust="NAO_AVALIADA", state="ORIGEM_DESCONHECIDA")`. Os dois valores estão
errados, e trocados entre si:

- `ORIGEM_DESCONHECIDA` é um dos cinco rótulos de **confiança** de `[P08 §4.1]`, não um dos nove
  de **estado**. Pertence a `trust`, não a `state`.
- `NAO_AVALIADA` não é nenhum dos cinco rótulos de confiança. É valor dos enums
  `Sufficiency`/`Confidence` do **P05** (`escolio/vocabulario.py`) — outro objeto, outro eixo.
  O rótulo do P08 para "não sei" é `ORIGEM_DESCONHECIDA`, e `[P09 §6.1]` manda usá-lo para item
  sem proveniência suficiente.

`[P08 §4]` declara os quatro eixos "independentes"; escrever rótulo de um no campo de outro
colapsa dois vocabulários em um, contra CLAUDE.md §7. Passou porque `[P09 §6]` tipa `trust` e
`state` como `string` e o código os implementa como `str` — nenhuma validação podia recusar.

**Não é divergência: nenhuma leitura do P08 ou do P09 defende esses dois valores.** É correção,
e **não dependia da decisão do BL-017** — valia sob qualquer das duas leituras registradas lá.

A frase que aqui dizia "`state` sem valor até haver base para afirmá-lo" **estava errada** e foi
o que a execução desmentiu: `[P09 §6]` não admite nulo em `state`. Daí `CO-013`.

### BL-017 — `sensitivity` e `privacy_classification` têm tipo divergente de `[P09 §6]`
Duas ocorrências, mesma natureza:

- `escolio/contrato/entrada.py:34` — `sensitivity: list[str]`; `[P09 §6]` declara
  `sensitivity: [SensitivityLabel]`.
- `escolio/contrato/requisicao.py:40` — `privacy_classification: list[SensitivityCategory]`;
  `[P09 §6]` declara `privacy_classification: [SensitivityLabel]`.

Consequência material, não estética: `SensitivityLabel` (`escolio/contrato/payloads.py:210-214`)
tem `category`, `source_policy` e `justification`, e as regras de `[P09 §20.1]` —
"`source_policy` deve identificar a política aplicável; quando pertinente, deve identificar P08"
e "`OTHER_CONTROLLED` exige `justification` não nula" — **são inexprimíveis em `str` e em
`SensitivityCategory` nua**. O passo 5 do protocolo de `[P08 §12]` ("classificar sensibilidade")
escreveria num campo incapaz de registrar o vínculo com o P08 que o P09 manda registrar.

O código honra `[SensitivityLabel]` em dois outros pontos (`SecurityFlags.sensitivity_labels`,
`escolio/contrato/resposta.py:88-100`; `SensitivityLabel.category`), e `SensitivityCategory`
(`vocabulario.py:204-213`) tem os nove valores de `[P09 §20]` **sem divergência** — logo a
inconsistência é de dois pontos em quatro.

**Exige decisão, não só correção**, porque altera `escolio/contrato/`, que implementa schema
homologado, e porque há leitura que defende o estado atual (o lado de entrada é frouxo por
desenho, acompanhando `trust: string`/`state: string`; apertar só `sensitivity` deixaria o bloco
meio tipado). As duas leituras estão em `docs/spec/divergencias.md` §4.6, Grupo 2.

**Em 2026-08-07 passou a `docs/coleta.md` `CO-012`** como decisão do professor, permanecendo aqui
como registro técnico (é este item que carrega arquivo:linha). As duas leituras ficam canônicas
em `divergencias.md` §4.6 — não duplicadas em `CO-012` nem aqui, para não divergirem em três
cópias.

**Consequência enquanto não decidido:** o passo 5 de `[P08 §12]` fica especificado em
`docs/spec/operacional-P08.md` §5 e não implementável com fidelidade. Nenhum código converte
`str` em `SensitivityLabel` nem o inverso — mesma disciplina de `CON-P05-001`.

## Ambiente e medição

### BL-007 — instalar o SDK `anthropic` e configurar chave — RESOLVIDO PARCIALMENTE
Resolvido em 2026-08-07. `anthropic` e `python-dotenv` instalados no venv via `pip` (não `uv` —
não há `pyproject.toml`/`uv.lock` no repositório; a convenção do CLAUDE.md §12 permanece
declarada, não seguida na prática). Chave em `.env`, fora do git (`.gitignore` atualizado antes
do arquivo existir; confirmado com `git check-ignore -v .env`).

`count_tokens` chamado uma única vez contra `data/gold/tese_natalia.pdf`, modelo
`claude-sonnet-5`: **259.399 tokens de input**. Não é geração — `count_tokens` não produz
resposta de modelo. Esta foi a primeira chamada à API de qualquer tipo neste projeto.
`docs/custos.md` atualizado com o número medido, a régua por página recalculada e a constatação
de que a faixa antiga (3,5–4,5 car./token) subestimava por quase o dobro: o valor real é 2,345
car./token. Script de medição foi temporário e removido após o uso — não faz parte do repositório.

**O que isto não resolve:** a contagem de unidades de fan-out ("~1200 unidades") continua chute
— mediu-se tokens do documento inteiro, não unidades. Ver BL-008.

**Em 2026-08-08, sessão de instalação de dependências e `pyproject.toml`:** `pdfplumber` e
`anthropic` já estavam instalados no `.venv` (confirmado: `pdfplumber==0.11.10`,
`anthropic==0.120.2`; a falha vista antes vinha de rodar `pytest` com o `python3` do sistema, não
com `.venv/bin/python` — não havia dependência de fato faltando). Suíte completa rodada com
`.venv/bin/python -m pytest`: **753 passando** (não 701 — o número subiu com a sessão 1 do P13,
`escolio/comentarios/`, 52 testes novos, entre a medição de 701 e esta sessão).

`pyproject.toml` criado na raiz do repositório: `[project.dependencies]` (`anthropic`,
`pdfplumber`, `python-dotenv`) e `[dependency-groups] dev` (`pytest`, `ruff`), `[tool.uv]
package = false` (não há artefato a empacotar — `escolio/` é importado por caminho relativo à
raiz, uso local), `[tool.pytest.ini_options]` e `[tool.ruff]` mínimos. `ruff==0.16.2` instalado no
`.venv` via `pip` para poder configurá-lo e testá-lo.

**O que isto não resolve — `uv` propriamente dito continua ausente.** Não há binário `uv` nesta
máquina, `pipx` não está instalado, e `pip install --user uv` falha
(`externally-managed-environment`, PEP 668, Python do sistema gerenciado pelo `apt`). Instalar
`uv` exigiria `curl -LsSf https://astral.sh/uv/install.sh | sh` (baixa e executa script remoto,
grava em `~/.local/bin` ou similar) ou `apt install pipx` (pacote de sistema) — as duas mudam
estado fora do repositório e fora do `.venv` do projeto, por isso não executadas sem autorização
explícita. `pyproject.toml` está pronto para `uv sync` assim que `uv` existir; até lá, `.venv` +
`pip` continua sendo o caminho real, exatamente como já registrado acima.

**Achado incidental, não corrigido nesta sessão:** `ruff check .` aponta 87 problemas
pré-existentes (34 corrigíveis com `--fix`) em código já escrito antes de o linter existir no
projeto — nenhum arquivo alterado para corrigi-los aqui, por ser fora do tema desta sessão
("instalar dependências e criar `pyproject.toml`", não "lint da base"). Rodar
`.venv/bin/ruff check .` para a lista completa antes de uma sessão dedicada a limpá-los.

### BL-008 — contagem de unidades por documento — RESOLVIDO PARCIALMENTE
Resolvido por extrapolação, não por medição direta de `data/gold/`, em 2026-08-07. Rodar o
parser sobre `data/gold/tese_natalia.pdf` continua não autorizado — consumiria o conjunto
reservado para avaliação das heurísticas de ingestão [LAC-ING-001] — e o professor confirmou
usar a alternativa já prevista aqui: medir sobre `data/dev/` e extrapolar.

Contagem real (`escolio.ingestao.parser.parse_pdf` sobre
`data/dev/Relatorio_Final_PIBIC-Bolsa-CNPq-e-UEM - Ricardo Antonio Esteves dos Santos.pdf`,
33 páginas): 143 parágrafos, 4 citações recuadas, 4 notas de rodapé, 4 figuras, 138 citações no
corpo, 60 referências, 14 seções — 367 unidades brutas. Unidade de análise do P13 definida como
parágrafo + citação recuada + nota + figura (citações no corpo são ponteiros internos ao
parágrafo já contado; referências são lista bibliográfica, não candidata a comentário local) =
155 unidades, 4,70/página. Extrapolado linearmente para 272 páginas: **1.281 unidades** —
substitui o "~1200" chutado. Ver `docs/custos.md`, seção "BL-008 — unidades de fan-out, medidas
por extrapolação", para a definição completa de unidade de análise e as ressalvas da
extrapolação.

**O que continua pendente:** medição direta sobre `data/gold/` (a extrapolação presume
densidade de unidades por página constante, não verificado); e a mesma contagem para as outras
quatro funções (P10, P11, P12, P14), cada uma com sua própria noção de unidade de análise
[`docs/spec/funcoes-P10-P14.md` §7] — só o P13 foi calculado.

## Aberto em 2026-08-08, na sessão de implementação da ingestão segura (item 7)

Nenhum arquivo existente foi alterado naquela sessão. `escolio/seguranca/` (7 módulos de código,
656 testes no total da suíte — eram 570) implementa os 27 RD e 25 DTA de
`docs/spec/operacional-P08.md`. Os três itens abaixo são exatamente as integrações que
exigiriam alterar código existente.

### BL-018 — `InputItem.security` não tem onde expressar "ainda não analisado"
`escolio.seguranca.registro.RegistroDeAnalise` (LAC-SEG-001) mantém esse estado num registro
externo, por `input_id`, porque `escolio/contrato/entrada.py::Security` (três booleanos, default
`False`, sem `__post_init__`) não tem campo para a distinção que `PR-03 [P08 §8]` exige. Ligar os
dois — de modo que `InputItem.security` reflita o registro externo — alteraria `entrada.py` ou o
adaptador `escolio/adaptadores/ingestao_para_input_item.py`. Decidir: acrescentar campo ao
schema (divergiria da forma literal de `[P09 §6]`, três booleanos "nem um mais") ou manter os
dois objetos desacoplados e documentar que todo consumidor de `InputItem.security` deve também
consultar `RegistroDeAnalise` antes de tratar `False` como "limpo".

### BL-019 — passos 5 e 6 do protocolo P08 dependem de `CO-012`/`CO-013`, ainda sem decisão
`escolio.seguranca.protocolo` marca os passos "classificar sensibilidade" e "classificar estado"
como `BLOQUEADO_POR_LACUNA_NORMATIVA`, não por lacuna de spec, mas porque implementá-los com
fidelidade exigiria alterar `escolio/contrato/entrada.py`
(`Classification.sensitivity: list[str]` → `[SensitivityLabel]`, `CO-012`) ou aceitar que
`Classification.state` não tem valor que signifique "não classificado" (`CO-013`, defeito já
preservado por decisão do professor). Nenhuma decisão nova é tomada aqui; o bloqueio populariza,
em código executável, decisões que já estavam pendentes em `docs/coleta.md`.

### BL-020 — camada de modelo (E2b, Haiku) preparada, não construída
`escolio.seguranca.deteccao` implementa a camada determinística inteira (PI-03/PI-05 literais) e
o envelope que uma chamada de modelo usaria (`delimita_como_dado`, enum fechado de saída), mas
nenhuma chamada ao SDK `anthropic` foi feita. Construir a chamada real exige `prompts/*.md`
(CLAUDE.md §12 o exige; não existe no repositório) e um cliente — ambos fora do escopo desta
sessão. Consequência declarada em `LAC-SEG-004`/`LAC-SEG-009`
(`escolio/seguranca/LACUNAS.md`): injeção puramente semântica sem padrão literal, em unidade de
origem confiável, não é vista até esta peça ser construída.

## Mapeamento de spec pendente

### BL-009 — P08, P19, P20 e R03 sem mapa em `docs/spec/` — `RESOLVIDO`
Todos os quatro lidos integralmente e mapeados: `docs/spec/mapa-P08.md`, `docs/spec/mapa-P19.md`,
`docs/spec/mapa-P20.md` (2026-08-08), `docs/spec/mapa-R03.md` (2026-08-07). Nenhuma fonte
citada neste item permanece sem mapa.

### BL-010 — lacunas de ingestão nunca gravadas nos artefatos canônicos
A §8 de `docs/spec/funcoes-P10-P14.md` levantou quatro lacunas — extração de
objetivo/hipótese/método, comparação entre versões, granularidade de célula de tabela, ingestão
de parecer editorial — que **não** foram gravadas em `escolio/ingestao/LACUNAS.md` nem em
`docs/coleta.md`. Continuam só no entregável daquela sessão.

## Aberto em 2026-08-09, na sessão de teste de integração ponta a ponta

`tests/integracao/test_pipeline_p13.py` (2 testes, suíte em 784) monta o primeiro percurso que
liga ingestão → adaptador → roteador → matrizes P13 → registro de comentários — cada peça só
tinha teste de unidade até aqui. O percurso **completa** dos dois lados (caminho feliz até
`RegistroDeComentarios.registrar`, e abstenção por `INDETERMINADO`), mas só porque o teste
fabrica manualmente cada elo que o código não fabrica. Nenhum arquivo de código foi alterado
nesta sessão — só o teste e este registro. Os desencaixes abaixo são o que a montagem revelou,
além dos já conhecidos (BL-003, BL-014):

## Aberto em 2026-08-09, na sessão 9 do plano P13 (módulo no roteador) — nenhum código alterado

Instrução da sessão: construir `escolio/funcoes/p13.py` "análogo aos outros cinco", com testes de
`classification.functions=["P13"]` sintético, reusando `escolio/funcoes/` (peça 6) e
`escolio/comentarios/` (sessões 1-8). Ao verificar o estado atual antes de escrever qualquer
código: **o entregável literal já existe**, construído em 2026-08-07 (sessão do roteador,
`CLAUDE.md §14`), antes mesmo da primeira sessão deste plano P13. `escolio/funcoes/p13.py` é
`DeclaracaoDeFuncao` completa (29 etapas, 17 gates, 18 entradas mínimas, dependências P02-P09);
`tests/funcoes/test_roteador.py::test_rotear_requisicao_coerente_valido` já roteia material
declarado sinteticamente para F04/P13 sem exceção — o mesmo cenário que esta sessão pediria.

O que a sessão parecia pedir além disso — o módulo "no roteador" produzindo algo com as peças de
`escolio/comentarios/`, não só existindo ao lado delas — é `BL-021`/`BL-022` abaixo, já
registrados na sessão de teste de integração do mesmo dia (2026-08-09) e já avaliados e
confirmados pelo professor como **decisão de arquitetura, não correção**: nenhuma fonte declara a
forma da orquestração entre roteador e comentários, e escolher uma inventaria estrutura sem
fonte. Construir agora duplicaria trabalho existente (o módulo) ou executaria uma decisão já
recusada (o orquestrador). Por instrução da própria sessão — "não altere código existente; se a
integração exigir mudança, registre e pare" — nenhum arquivo de código foi tocado.
`docs/spec/plano-P13.md` sessão 9 e esta entrada são o único produto.

**Próxima ação única, se o professor quiser reabrir isto:** decidir a forma do orquestrador de
BL-021 (função única, pipeline, evento) — decisão dele, não inferível daqui.

## Aberto em 2026-08-09, na sessão de correção BL-021 a BL-025

BL-023, BL-024 e BL-025 corrigidos nesta sessão. BL-021 e BL-022 avaliados e confirmados pelo
professor como decisão de arquitetura, não correção — nenhuma fonte declara orquestração
explícita entre módulos nem convenção de ID compartilhada, então "consertar" exigiria escolher
uma forma que a spec não dá. Permanecem abaixo, registrados, sem código alterado para eles.

### BL-021 — nenhum orquestrador liga roteador → matrizes P13 → comentário — RESOLVIDO
Depois de `roteador.rotear()` confirmar `AdmissaoDeMaterial.DECLARADO`, não existia nenhuma
função que chamasse `MatrizCriticidade`, `MatrizSeletividade` ou `P13Comment` a partir da decisão
de roteamento. `escolio/funcoes/p13.py` continua puramente declarativo — "nada aqui executa"
segue literal, não é revogado.

**Em 2026-08-09, por instrução expressa do professor: forma decidida.** Um módulo de execução
por função, `escolio/funcoes/execucao_p13.py` — não um executor genérico [CLAUDE.md §4]. Ele
percorre as 29 etapas declaradas em `p13.py` e chama o que `escolio/comentarios/` (sessões 1-8)
já implementou, mas **nunca mais de uma etapa por chamada**: `avancar(estado, entrada)` calcula
`DeclaracaoDeFuncao.proxima_etapa(concluidas)` e executa só essa etapa, nunca a seguinte — releitura
literal de POL-012 ("registrar exatamente uma próxima ação permitida ou nenhuma automática"), já
citada como razão de nenhum módulo de função ter `executar` (`escolio/funcoes/LACUNAS.md`, "Não
incluído nesta peça"). Isso não contradiz aquele registro: continua não havendo encadeamento
automático; o que existe agora é a próxima ação, executável sob pedido explícito.

Sem chamada à API [instrução da sessão]. Toda etapa que exige juízo humano ou de modelo — matriz
de criticidade e seletividade (§11-12), verificação de fontes/evidência/voz/privacidade e
identificação de problemas sistêmicos (etapas 11-15), redação de comentários (16-18) — é um ponto
de extensão explícito, nunca preenchido por inferência: `CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO`
marca exatamente essas etapas em `ResultadoDeEtapa`, distinta de `ENTRADA_NAO_FORNECIDA` (a etapa
tem schema de aceitação — ex. `matrizes_criticidade` — só não veio preenchido nesta chamada) e de
`SEM_FONTE_DE_VERIFICACAO` (etapas 19-24: nenhuma seção liga o nome da etapa a um critério
verificável distinto do checklist de §44, que só corresponde nominalmente à etapa 25 "auditoria
final" — mesmo nome nas duas fontes, por isso só essa etapa chama `auditoria.auditar_lote`
diretamente). Etapas 26-29 (`Etapa.fase is None`) são `FORA_DO_FLUXO_DE_EXECUCAO`,
incondicionalmente — decisão autoral, homologação documental, piloto Word real e ativação
operacional são atos humanos ou pós-homologação; "o sistema nunca homologa" [CLAUDE.md §1-§2].

**Consequência prática, registrada e não escondida:** dado que 11-15 nunca aceitam entrada nesta
sessão, nenhum percurso real avança além da etapa 10 (seleção) — as etapas 16-25 só são exercidas
em teste simulando historicamente que uma sessão futura as completou
(`tests/funcoes/test_execucao_p13.py`, `TestPercursoCompletoAteOPontoDeExtensao.
test_document_id_diverge_do_material_id_levanta_bl_022`). Isto não é lacuna deste módulo: é o
ponto de extensão declarado fazendo exatamente o que deveria — recusar-se a inventar juízo.
Testes: percurso feliz E1-E4 até a seleção e parada no primeiro ponto de extensão; etapa sem
entrada suficiente parando sem avançar nem pular para a próxima; material não declarado parando
na etapa 1; disciplina de "não reexecutar após o fim do fluxo".

### BL-022 — `unit_id`/`document_id` não têm gerador nem validador compartilhado — RESOLVIDO
`Paragrafo.unit_id` (ingestão), `MatrizCriticidade.unit_id`, `MatrizSeletividade.unit_id` e
`P13Comment.unit_id` continuam todos `str` soltos nos módulos de sessão 1-6 — não alterados.

**Em 2026-08-09, por instrução expressa do professor: a orquestração de BL-021 expôs a
divergência, e a resolução mora inteiramente em `escolio/funcoes/execucao_p13.py`**, o único
lugar que tem os dois lados da relação (documento e artefatos derivados) ao mesmo tempo:

- `document_id` canônico, `[PROPOSTA]`: `material_id_de_documento(documento)` [P19 §10], não
  `InputItem.input_id` [P09 §6.1] — `material_id` é estável entre cópias e independente da
  requisição que o menciona; `input_id` é identidade de item de uma requisição específica, sem
  garantia de se repetir entre duas requisições sobre o mesmo documento. `P13Comment.document_id`
  divergente do `material_id` levanta `ErroDeExecucaoP13` na etapa em que o comentário é
  registrado (16, 17 ou 18) — nunca passa silencioso.
- `unit_id` conhecido = o conjunto reunido na etapa 7 (`ContextoExecucaoP13.unidades_conhecidas`,
  a partir de `Paragrafo`/`CitacaoRecuada`/`NotaDeRodape`/`Figura` de `DocumentoIngerido`).
  `MatrizCriticidade.unit_id`, `MatrizSeletividade.unit_id` e `P13Comment.unit_id` são conferidos
  contra esse conjunto nas etapas 8, 9 e 16-18, respectivamente; divergência levanta
  `ErroDeExecucaoP13`.

Isto não substitui BL-024 (`exige_referencia_valida_a_criticidade`, sessão 2) — continua sendo a
checagem entre `MatrizSeletividade` e `MatrizCriticidade`; a camada nova é contra a estrutura do
documento, que nenhuma sessão anterior tinha em mãos ao lado dos artefatos derivados.

### BL-023 — `selection_decision` não é tipado; os oito resultados de seleção do P13 não existem em código — RESOLVIDO
`p13.DECLARACAO.decisoes` enumera oito resultados de seleção da etapa 10 — `COMENTAR`,
`NAO_COMENTAR_SEM_PROBLEMA_MATERIAL`, `NAO_COMENTAR_POR_REPETICAO`,
`REMETER_A_COMENTARIO_MATRIZ`, `AGUARDAR_EVIDENCIA`, `AGUARDAR_GATE`, `ABSTER_SE`, `BLOQUEADO`
[§10] — como string literal dentro de uma tupla de documentação. `MatrizSeletividade.selection_decision`
(`escolio/comentarios/seletividade.py`) é `str` livre, sem `__post_init__` que confira
pertencimento a esse conjunto. Confirmado por script avulso (não incorporado a
`tests/integracao/`, só para checar a hipótese): `MatrizSeletividade(..., selection_decision="COMentar", ...)`
constrói sem erro — qualquer string não vazia passa, inclusive grafia errada da própria fonte.
Só `seletividade.SELECTION_DECISION_NAO_COMENTAR_SEM_PROBLEMA_MATERIAL` está nomeado como
constante; os outros sete resultados não têm constante nem enum.

**Em 2026-08-09:** `SelectionDecision` (enum, `escolio/comentarios/seletividade.py`) fecha os
oito valores do §10; `MatrizSeletividade.selection_decision` passou de `str` livre para exigir
membro do enum, com `__post_init__` rejeitando string crua ou grafia errada. Alias antigo
preservado. Testes novos em `tests/comentarios/test_seletividade.py`
(`test_selection_decision_string_crua_rejeita` falha antes da correção, passa depois). Ver
`escolio/comentarios/LACUNAS.md`.

### BL-024 — `MatrizSeletividade.candidate_problem_id` não referencia `MatrizCriticidade` de fato — RESOLVIDO
`aplicar_selecao`/`ordenar_por_criticidade` ordenam por `criticality` (campo copiado à mão do
`MatrizCriticidade.classe` correspondente), mas nada verifica que `candidate_problem_id` aponta
para um `problem_id` de uma `MatrizCriticidade` que de fato existe, nem que `criticality` bate
com a classe que essa matriz declarou. Duas matrizes podem divergir (`classe` diferente do
`criticality` copiado) sem erro — mesma classe de defeito de BL-022, objeto diferente.

**Em 2026-08-09:** `exige_referencia_valida_a_criticidade` (`escolio/comentarios/seletividade.py`)
confere as duas coisas — `candidate_problem_id` aponta para uma `MatrizCriticidade` existente, e
`criticality` bate com a `classe` dessa matriz — e levanta `ErroDeComentario` quando não. Função
avulsa, não amarrada a `aplicar_selecao`: quem tem as duas listas em mãos chama; não pressupõe o
orquestrador de BL-021. Testes novos em `tests/comentarios/test_seletividade.py`. Ver
`escolio/comentarios/LACUNAS.md`.

### BL-025 — `p13.DECLARACAO.operacoes_autorizadas` vazio: verificação de operação sempre inconclusiva para F04 — RESOLVIDO PARCIALMENTE
Confirmado ao rodar `roteador.rotear()` com `operation="CARTOGRAFIA_GLOBAL"`: como
`escolio/funcoes/p13.py` não popula `operacoes_autorizadas` (default `frozenset()`),
`verificar_operacao` retorna sempre `conclusiva=False` para qualquer valor de `operation` sob
F04 — não só para os que "parecem" corretos. Já registrado como padrão geral em LAC-FUNC-005;
este item confirma que, na prática, **nenhuma** string de operação é rejeitada para P13/F04 hoje,
inclusive valores sem relação alguma com o contrato (ex.: `operation="HOMOLOGAR_TUDO"` passaria
pelo roteador sem levantar, desde que não estivesse em `prohibited_operations` da própria
requisição). Não é bug do roteador — é ausência de fonte, mas o efeito prático (nenhuma
recusa por incompatibilidade de operação em P13) só ficou visível ao executar o percurso.

## Aberto em 2026-08-09, na sessão 8 do plano P13 (extensão do envelope P09)

Nenhum arquivo existente foi alterado nesta sessão (`escolio/contrato/`, `escolio/comentarios/`
das sessões 1-7). `escolio/comentarios/aplicacao_p09.py` implementa `P13RequestExtension`,
`P13ResultExtension` e os builders de payload de §31.6. Os dois itens abaixo são exatamente as
integrações que exigiriam alterar código existente da peça 1 — por instrução da sessão, registrados
aqui e não executados.

### BL-026 — `cause_code` (§29/§30) sem campo em `AbstentionPayload`; `Request` sem campo aberto para extensão de função
Dois achados da mesma sessão, de natureza distinta, registrados juntos por terem a mesma causa
raiz (campo que o contrato de função cita e o envelope P09 não provê):

- `AbstentionPayload` (P09 §15, `escolio/contrato/payloads.py`) não tem campo `cause_code`. O P13
  §29 (`P13_CAUSE_VOICE_PROFILE_INSUFFICIENT`) e §30 (`P13_CAUSE_PRIVACY_PROCESSING_CONDITION_ABSENT`)
  citam esse campo em exemplo, mas nenhuma seção do P09 o declara. `constroi_abstencao_perfil_de_
  voz_insuficiente` (sessão 8) registra o valor dentro de `reason`, por não haver campo dedicado nem
  instrução para acrescentar um a `AbstentionPayload`. Se outras funções (P10-P14) citarem
  `cause_code` do mesmo jeito, decidir então se `AbstentionPayload` ganha o campo — mudança na peça
  1, que esta sessão não estava autorizada a fazer.
- `Response.result.content` é `object | None` — `P13ResultExtension` encaixa ali sem alterar
  `Response`. `Request` (`escolio/contrato/requisicao.py`) não tem campo equivalente: nenhum de
  seus campos aceita um objeto aberto para uma extensão específica de função. `P13RequestExtension`
  (sessão 8) existe como objeto independente, sem ponto de anexação a `Request`. Decidir, quando o
  roteador de função (peça 6) precisar de fato transportar extensões de entrada: acrescentar campo a
  `Request`, ou usar `ContextItem` como indireção (aponta para a extensão por `content_reference`,
  não a embute) — nenhuma das duas foi escolhida aqui.

Ver `escolio/comentarios/LACUNAS.md`, "Sessão 8", para o detalhamento de cada achado.

### BL-027 — mecanismo real de BVAA (P04) não existe; repositório de fonte de verdade decidido, não construído

P13 §26 exige aplicar o BVAA integralmente ("sem acesso verificável... não confirma leitura;
não confirma passagem; não confirma página; não confirma imagem; não libera sustentação
específica; não inventa bibliografia"). `escolio/bvaa/` (X01/P04) existe como máquina de
estados abstrata, mas **nenhum módulo de função a chama** — nem `execucao_p13.py`, que já
rodou um piloto real (`costs/ledger.jsonl`, `sequence_id=MAT-DOC-piloto2026080901`) sem
verificação BVAA em nenhum ponto, nem `execucao_p11.py` (etapa 16, "Controle BVAA", é
`PONTO_DE_EXTENSAO_DE_MODELO`).

Origem histórica do requisito: o protótipo pré-P13 ("PC30" — "Auditor Orientador de
Comentários Word", mesmo domínio de P13) usava Google Drive como repositório bibliográfico
concreto ("Drive-first"/"BVAA-Drive", dezenas de versões em
`corpus/historico/acervo-antigo/AUDITOR_ORIENTADOR_COMENTARIOS_WORD/`). O contrato formal
homologado de P13 generalizou isso para "acesso verificável", sem fixar mecanismo — "Drive"
não aparece no texto do contrato.

**Em 2026-08-09, decisão do `USUARIO_PROPONENTE`** sobre qual repositório é fonte de verdade:

1. Usar as fontes que estão no Drive — repositório primário.
2. Buscar na internet novas e melhores referências — busca ativa.
3. Se encontrar referência nova/melhor: avisar, pedir para baixar, e só usar depois de
   disponibilizada — nunca incorporação automática de conteúdo achado na internet.

Isso fecha a pergunta "qual repositório", mas não implementava nada por si só.

**Em 2026-08-09, mesma sessão: item (a) resolvido.** O professor criou uma conta de serviço
Google Cloud (`biblioteca-escolio@gen-lang-client-0161885764.iam.gserviceaccount.com`) e
compartilhou as 5 pastas da biblioteca com ela (permissão de Leitor, não pública).
`escolio/drive/conector.py` (novo módulo de infraestrutura, mesmo padrão de
`escolio/cliente/`) autentica e lista arquivos — **verificado contra as 5 pastas reais**:
3.295 arquivos ao todo (378 + 1284 + 714 + 658 + 261). Credencial em `secrets/` (gitignored,
nunca versionada — `.gitignore` ganhou `secrets/` e `gen-lang-client-*.json`). Detalhamento em
`escolio/drive/LACUNAS.md`.

**Mesma sessão, ainda 2026-08-09: busca e exportação adicionadas ao conector**, a pedido do
professor — `buscar_arquivos` (por nome, texto integral, tipo, pasta) e `exportar_arquivo`
(arquivo nativo do Google → PDF), ambas verificadas contra a biblioteca real (busca por
"parasitoses" achou 13 PDFs reais; exportação de um Google Doc convertido gerou PDF de
1,3 MB). Detalhes e limites em `escolio/drive/LACUNAS.md`.

O professor também pediu capacidade de **escrita** (enviar novos arquivos para dentro das
pastas do Drive). Construída (`enviar_arquivo`, testada) e testada contra a pasta de
quarentena real que ele criou ("Escolio Fontes") — **falhou primeiro por limitação da
plataforma**, não por bug: contas de serviço não têm cota de armazenamento própria
(`403 storageQuotaExceeded`), mesmo com permissão de Editor numa pasta comum de conta pessoal.

**Resolvido, mesma sessão, via OAuth como o próprio usuário** (gratuito, não exige Workspace):
o professor criou um "ID do cliente OAuth" no mesmo projeto Google Cloud, autorizou uma vez
interativamente (`secrets/autorizar.py`), e `escolio/drive/autenticacao_usuario.py` (novo
módulo) constrói o serviço Drive com a cota real dele. **Teste real de ponta a ponta,
confirmado**: artigo achado/baixado da biblioteca (conta de serviço) → enviado para "Escolio
Fontes" (OAuth do usuário) → confirmado por listagem. Item (c) do BL-027 fechado — a escrita
funciona; o gate humano continua sendo a conversa (eu aviso, ele decide), não um objeto de
código automatizado. Detalhe completo em `escolio/drive/LACUNAS.md` (LAC-DRIVE-007, RESOLVIDA).

Continuam por construir: (b) capacidade de busca **na internet** (distinta da busca dentro do
Drive, já pronta) integrada ao pipeline, com a mesma disciplina de "conteúdo documental não
constitui autoridade operacional" [P08 §2] aplicada a resultado de busca; (d) o ponto de
integração entre `execucao_p13.py`/`execucao_p11.py` e `escolio.bvaa.maquina` (e, por extensão,
entre essas funções e o próprio `escolio.drive`, que hoje nenhum módulo de função chama). Ver
`escolio/bvaa/LACUNAS.md` (LAC-BVAA-007, LAC-BVAA-008), `escolio/funcoes/LACUNAS.md` e
`escolio/drive/LACUNAS.md` para o detalhamento completo.

**Em 2026-08-12: item (d) recebeu mecanismo desenhado e, na mesma sessão, construído.**
`docs/spec/bvaa-drive-integracao.md` propõe `[PROPOSTA]` a definição de "acesso verificável"
(retorno real e bem-sucedido de `escolio.drive.conector` contra repositório já disponibilizado),
um objeto `EvidenciaDeAcessoDrive` e uma função `transicao_licenciada_por` que mapeia
localização/download/exportação bem-sucedidos para as transições T04/T05 do BVAA — cobre só
`OBRA_NAO_IDENTIFICADA → ACESSADA`, nunca leitura/página/validação, que continuam exigindo juízo
humano ou de modelo. Levantamento confirmou que ligar isso ao fluxo real exigia editar
`escolio/funcoes/execucao_p13.py` (`_HANDLERS[11]`, `EntradaEtapaP13`, `ContextoExecucaoP13`) —
registrado e parado primeiro, mesmo padrão de BL-021/BL-022 antes da decisão do professor.

**Depois, mesma sessão: autorizado e construído**, com duas restrições literais do professor —
`escolio/bvaa/` continua puro (a dependência de `escolio.drive` mora só em
`escolio/funcoes/bvaa_drive.py`, novo módulo, orquestrador; zero linhas de `escolio/bvaa/`
tocadas) e o acesso licencia exclusivamente T04/T05. Só a etapa 11 ("verificação de fontes") foi
ligada — decisão tomada durante a implementação: etapa 12 ("verificação de evidências",
correspondência afirmação-conteúdo) é julgamento que Drive não comprova, permanece
`PONTO_DE_EXTENSAO_DE_MODELO` como 13-15. Sem evidência fornecida, comportamento idêntico ao
anterior a esta sessão — sem regressão. Duas alternativas descartadas registradas no documento:
verificação binária "existe/não existe" sem passar pela máquina de estados, e usar
`ArquivoDrive.modificado_em` como prova de leitura. Testes com Drive mockado
(`tests/funcoes/test_bvaa_drive.py`, novos casos em `tests/funcoes/test_execucao_p13.py`); suíte
completa em **1027 passando, 16 skipped** (era 784 na sessão de 2026-08-09 citada acima — o
número subiu com sessões intermediárias não detalhadas aqui). Ver `escolio/bvaa/LACUNAS.md`
LAC-BVAA-009 e `docs/spec/bvaa-drive-integracao.md` §6. Item (b) (busca na internet) continua
sem trabalho nesta sessão.

**Em 2026-08-09:** a lacuna de fonte (LAC-FUNC-005) não fechou e não devia fechar — inventar
vocabulário de operação por função violaria CLAUDE.md §11 e quebraria
`tests/funcoes/test_modulos_de_funcao.py::test_nenhuma_funcao_declara_operacoes_autorizadas`, que
trava exatamente essa disciplina. O que fechou foi o caso concreto do backlog:
`roteador.exige_operacao_nao_homologa` bloqueia, para qualquer `function_id` e independente de
`operacoes_autorizadas`, toda `operation` que peça homologação (`"HOMOLOGACAO"`, `"INT-14"`,
qualquer valor começado por `"HOMOLOGAR"` — cobre `"HOMOLOGAR_TUDO"`). Fundamento não é contrato
de função: é CLAUDE.md §1/§2 ("o sistema nunca homologa"), que nenhuma carta branca suspende.
`rotear()` chama essa checagem incondicionalmente, antes de qualquer resolução de função. Uma
`operation` inventada e alheia à homologação (`"LER_TUDO_DUAS_VEZES"`, por exemplo) continua
inconclusiva, como antes — a lacuna de enumeração geral permanece aberta, só o caso de maior
risco fechou. Testes novos em `tests/funcoes/test_roteador.py`. Ver `escolio/funcoes/LACUNAS.md`,
LAC-FUNC-005.

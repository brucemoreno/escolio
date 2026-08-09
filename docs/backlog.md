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

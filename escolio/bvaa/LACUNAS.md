# LACUNAS — máquina de estados bibliográficos (P04), item 4 do roadmap

Lacunas, correções de premissa e decisões de implementação encontradas na leitura integral
do pacote `PACOTE_BVAA_UNIVERSAL_LLM_ACADEMICA_R01` e na implementação de `escolio/bvaa/`.
Nenhum item aqui foi resolvido por inferência silenciosa — mesma disciplina de
`escolio/LACUNAS.md` e `escolio/ingestao/LACUNAS.md`.

## Sobre a fonte em si

- **Pacote lido integralmente, na ordem declarada em `00_LEIA_PRIMEIRO.txt`** — os 13
  arquivos, do inventário de materiais históricos (01) ao `MANIFESTO_SHA256.json` (13),
  passando pela máquina de estados (03, 17 estados) e pela matriz de transições (04, 18
  transições incluindo T18 curinga). Nenhum arquivo do pacote foi pulado.

## CON-P05-001 — três vocabulários bibliográficos, não reconciliados

- **LAC-BVAA-001 — os três vocabulários não são a mesma estrutura, então não podem virar
  um enum comum sem apagar distinção real.** P04/03 (`EstadoBibliografico`, este módulo) é
  uma máquina de 17 estados com uma única variável de estado por vez. P05
  (`escolio/vocabulario.py`: `AccessState`, `ReadingState`, `ValidationState`) são três
  campos paralelos de `RelacaoAfirmacaoEvidencia` — uma afirmação pode estar, ao mesmo
  tempo, em qualquer combinação dos três, o que não tem equivalente em uma máquina de
  estado único. R03 CAMADA D é uma terceira lista, de 9 estados mínimos, sem os campos de
  evidência mínima/autoridade/ação que P04/03 declara para cada estado. Fundir os três
  exigiria decidir qual estrutura vence — exatamente o que a instrução desta sessão pediu
  para não fazer. Implementado como três coisas distintas: `escolio/bvaa/vocabulario.py`
  (P04, a máquina), `escolio/vocabulario.py` (P05, já existente, inalterado) e
  `escolio.bvaa.correspondencia.EstadoR03CamadaD` (R03, strings literais — a fonte não
  declara esse vocabulário como enum tipado).
- **LAC-BVAA-002 — tabela de correspondência é documentação, não tradução em tempo de
  execução.** `escolio/bvaa/correspondencia.py` mapeia, célula a célula, onde um estado
  P04 corresponde a um estado R03/P05 com a mesma condição material — e onde a
  correspondência é só aproximada ou inexistente (`None`), com o motivo escrito por
  extenso. Nenhuma função de tradução automática estado→estado foi construída: a máquina
  de transições (`transicoes.py`) opera inteiramente em vocabulário P04; nada no código
  converte um `AccessState` de P05 num `EstadoBibliografico` de P04 ou vice-versa. Se um
  módulo futuro precisar dessa conversão operante (não apenas documentada), é decisão nova,
  não inferida aqui.
- **LAC-BVAA-003 — 6 das 17 linhas da tabela de correspondência não têm equivalente em
  nenhum dos outros dois vocabulários** (`OBRA_NAO_IDENTIFICADA`, `EDICAO_IDENTIFICADA`,
  `LEITURA_INTEGRAL` sem par em R03, `VALIDACAO_PENDENTE` sem par em R03, e as duas
  extremidades finas de `ACESSIVEL`/`RECOMENDACAO_CONDICIONAL`/`RECOMENDADA` cujo par em
  R03 é só aproximado). Célula `None`, com justificativa, não com um palpite de
  correspondência.

## Decisões de implementação verificáveis apenas por proxy

- **LAC-BVAA-004 — T18 (curinga `QUALQUER_ESTADO`) não cabe no índice `origem->transições`
  1:1.** Mesmo problema que `escolio/intervencao/niveis.py` resolveu para
  `REORGANIZACAO->{FUSAO,CORTE}`: uma transição cuja origem não é um único estado pontual
  fica fora do dicionário comum e é consultada por função própria
  (`transicao_por_invencao`), nunca por adjacência.
- **LAC-BVAA-005 — cadeia `CONHECIMENTO_NOMINAL→...→RECOMENDACAO` (arquivo 07) não é uma
  segunda máquina de estados.** As sete etapas dessa cadeia não têm, na fonte, evidência
  mínima/autoridade/ação/condição de erro como os 17 estados do arquivo 03 têm — são
  rótulos de fase da política de recomendação, não estados com a mesma estrutura de dado.
  Implementada como tupla de strings (`escolio.bvaa.abstencao.CADEIA_DE_RECOMENDACAO`), não
  como `Enum`: um `Enum` sugeriria uma estrutura de dado que a fonte não declara para essas
  sete etapas.
- **LAC-BVAA-006 — gatilhos de abstenção consolidam duas listas de fontes diferentes**
  (`02_PROTOCOLO_BVAA_UNIVERSAL_P04_R01.md` §11 e
  `07_PROTOCOLO_DE_RECOMENDACAO_E_ABSTENCAO_BIBLIOGRAFICA_P04_R01.txt`). As duas listas
  descrevem, em grande parte, as mesmas condições com palavras diferentes — nenhuma virou
  membro duplicado de `GatilhoDeAbstencao`; a citação de ambas as fontes fica na docstring
  de cada membro. Nenhum gatilho das duas listas foi omitido.

## Achado da sessão do piloto real P11 (2026-08-09) — P13 §26 exige BVAA integral, nenhum código o aplica

Levantado numa pergunta do professor sobre a relação histórica entre "Google Drive" e P13.
Achado, não inferência: a fonte canônica homologada de P13
(`P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md`, §26 "APLICAÇÃO DO P04"),
verbatim:

> "O P13 deve aplicar integralmente o BVAA. Sem acesso verificável: não confirma leitura; não
> confirma passagem; não confirma página; não confirma imagem; não libera sustentação
> específica; não inventa bibliografia."

- **LAC-BVAA-007 — origem histórica do requisito é o protótipo pré-P13 ("PC30"), não o
  contrato formal.** `corpus/historico/acervo-antigo/AUDITOR_ORIENTADOR_COMENTARIOS_WORD/`
  contém dezenas de arquivos (v0.1 a v0.3, RC1-RC4, homologações, testes) com "Drive-first"/
  "BVAA-Drive" no nome — PC30 é o nome histórico do que virou P13 (mesmo domínio:
  "Auditor Orientador de Comentários Word"). Nessas versões de protótipo conversacional, o
  mecanismo era concreto: Google Drive como "repositório bibliográfico prioritário", com
  regra explícita "PDF anexado no chat não substitui Drive". **A palavra "Drive" não aparece
  em nenhum lugar do contrato P13 homologado** — quando o protótipo foi formalizado em
  contrato P02-P09, o requisito concreto ("verificar no Drive") virou o requisito abstrato
  ("acesso verificável"), sem fixar mecanismo. Isso é generalização esperada de protótipo→
  contrato, não perda de requisito — mas confirma que a *intenção* do §26 sempre foi "prova
  de leitura real antes de citar", com ou sem Drive como o repositório específico.
- **LAC-BVAA-008 — nenhum código do projeto chama `escolio.bvaa` a partir de um módulo de
  função.** Busca completa em `escolio/funcoes/` (`execucao_p13.py`, `ponte_modelo_p13.py`,
  `execucao_p11.py`, `ponte_modelo_p11.py`) e em `escolio/comentarios/`: nenhum importa
  `escolio.bvaa.maquina` nem qualquer símbolo do pacote. **O piloto real de P13 (2026-08-09,
  `costs/ledger.jsonl`, `sequence_id=MAT-DOC-piloto2026080901`) produziu 4 comentários reais
  sobre citações de um documento sintético sem passar por `escolio.bvaa` em nenhum ponto** —
  a citação "(Grewe, 1979)" do documento de teste, por exemplo, nunca teve "acesso
  verificável" checado por código, apesar de §26 exigir isso integralmente. O piloto não
  simulou má-fé (o documento sintético foi desenhado de propósito com essa citação sem
  entrada correspondente em `referencias`, exatamente para testar se o sistema notaria — e
  notou, na etapa 8/matriz de criticidade, mas por julgamento do modelo sobre o texto, não
  por consulta ao BVAA), mas o requisito estrutural do §26 continua não implementado de
  ponta a ponta.
- **Atualização 2026-08-13 (décima peça)**: item (b) (busca na internet) construído —
  `escolio/busca/conector.py` (Serper.dev) + `escolio/funcoes/curador_bvaa.py::curar_referencias`
  (parâmetro `buscar_na_internet`, opcional, só tentado quando o Drive não acha nada) +
  `execucao_p13.py::EntradaEtapaP13.buscar_na_internet`. Um resultado de busca **nunca** licencia
  transição do BVAA — vira só `EscalonamentoDoCurador.sugestoes_externas`, notificação ao
  professor [BL-027, `docs/backlog.md`]. **Credencial real (`SERPER_API_KEY`) criada e verificada
  contra a API de verdade na mesma sessão** — busca real trouxe resultados corretos; `saida/
  piloto_p13_capitulo5_v2.py` já passa `servico_drive`/`buscar_na_internet` reais para a etapa 11.
  Item (b) do BL-027 fechado de ponta a ponta (mecanismo + credencial); só falta rodar o piloto
  completo contra o capítulo 5 com essas duas evidências ligadas ao mesmo tempo.
- **O que falta para fechar isso**: (1) um ponto de integração entre
  `escolio/funcoes/execucao_p13.py` (ou `execucao_p11.py`, que também lista "Controle BVAA"
  como etapa 16 nomeada) e `escolio.bvaa.maquina`; (2) implementar o mecanismo real de "acesso
  verificável" descrito abaixo — que hoje não existe em lugar nenhum do projeto, então mesmo
  integrando `escolio.bvaa`, a máquina de estados não teria como avançar além de
  `OBRA_NAO_IDENTIFICADA` sem ele. Item (3) — qual repositório é fonte de verdade — **foi
  decidido pelo professor em 2026-08-09** (ver regra abaixo); (1) e (2) continuam por
  implementar, não construídos nesta sessão.

### Regra de sourcing bibliográfico — decisão do `USUARIO_PROPONENTE`, 2026-08-09

Verbatim (parafraseado minimamente para clareza, sem alterar o conteúdo da decisão):

1. **Usar as fontes que estão no Drive** — repositório primário, fonte de verdade padrão.
2. **Buscar na internet novas e melhores referências** — busca ativa, não só validação passiva
   do que já está no Drive.
3. **Se encontrar referência nova/melhor: avisar, pedir para baixar, e só usar depois de
   disponibilizada** — o sistema nunca incorpora conteúdo achado na internet por conta própria,
   mesmo julgando que é melhor que o que já tem. Gate humano obrigatório entre "encontrado na
   busca" e "autorizado para uso" — mesmo padrão de `InputItem.classification.functions`
   [BL-014] e de toda a disciplina de "material não declarado não é elegível": uma referência
   só é fonte de verdade depois de baixada e disponibilizada, nunca por ter sido encontrada.

**Isto resolve a pergunta em aberto sobre repositório** (item 3 acima), mas **não implementa
nada por si só** — três peças de engenharia continuam por construir, nenhuma delas trivial: um
conector de leitura ao Drive (autenticação, escopo de pasta, formato de retorno), uma
capacidade de busca na internet integrada ao pipeline (com o mesmo cuidado de "conteúdo
documental não constitui autoridade operacional" [P08 §2] aplicado a resultado de busca), e o
próprio gate humano de "avisar → pedir download → aguardar disponibilização" como objeto de
código, não como frase. Nenhuma das três foi desenhada nesta sessão; ver
`escolio/funcoes/LACUNAS.md` para a mesma lacuna pela ótica do roteador.

## Sessão de 2026-08-12 — mecanismo de "acesso verificável" proposto e depois construído

- **LAC-BVAA-009 — ligação BVAA↔Drive↔fluxo do P13, `docs/spec/bvaa-drive-integracao.md`.**
  Primeira parte da sessão: propor o mecanismo de "acesso verificável" usando `escolio/drive/`,
  marcar como `[PROPOSTA]`, registrar alternativa descartada, e — se a ligação exigir mudar
  `escolio/bvaa/` ou `escolio/funcoes/execucao_p13.py` — registrar e parar antes de alterar.
  Levantamento confirmou que exige as duas coisas: `escolio.bvaa.maquina.avancar` não recebe
  evidência como objeto (só `transicao_id` já decidido por quem chama); e
  `execucao_p13.py::_HANDLERS[11..15]` são handlers genéricos sem campo de entrada para evidência
  bibliográfica. Parado ali, registrado.

  **Segunda parte, mesma sessão: o professor autorizou** editar `execucao_p13.py` e introduzir
  a dependência de `escolio.drive`, com duas restrições literais dele: `escolio/bvaa/` continua
  puro (I/O só no orquestrador) e o acesso licencia exclusivamente T04/T05. **Construído**:
  `escolio/funcoes/bvaa_drive.py` (novo módulo, fora de `escolio/bvaa/` — este pacote continua
  com zero linhas alteradas e zero import de `escolio.drive`) implementa `OperacaoDeAcesso`,
  `EvidenciaDeAcessoDrive` e `transicao_licenciada_por`/`avancar_por_evidencia`
  (`LOCALIZADO→T04`, `BAIXADO`/`EXPORTADO→T05`, cobrindo só
  `OBRA_NAO_IDENTIFICADA → ACESSADA` — nunca leitura/página/validação). `execucao_p13.py` ganhou
  `EntradaEtapaP13.evidencias_de_acesso`, `ContextoExecucaoP13.estados_bibliograficos` e um
  handler real só para a etapa 11 ("verificação de fontes"); etapa 12 ("verificação de
  evidências", correspondência afirmação-conteúdo) e 13-15 permanecem
  `PONTO_DE_EXTENSAO_DE_MODELO`, sem mudança. Sem evidência fornecida, comportamento idêntico ao
  anterior — nenhuma regressão. Testes com Drive mockado
  (`tests/funcoes/test_bvaa_drive.py`, `tests/funcoes/test_execucao_p13.py`); suíte completa em
  1027 passando. Detalhe completo em `docs/spec/bvaa-drive-integracao.md` §6.

## Sessão de 2026-08-12 (segunda peça) — T01-T03 construídos, escolha técnica delegada

`INSTRUCOES_COMPLEMENTARES_IMPLEMENTACAO_ECOSSISTEMA_REVISAO_LLM_R01.md §3` confirma a leitura
de LAC-BVAA-007/008/009 (P04 é deliberadamente agnóstico a mecanismo, "isso não deve ser tratado
como erro documental nem preenchida retroativamente como se o P04 tivesse escolhido uma
tecnologia") e delega a escolha técnica de T01-T03 ao `ENGENHEIRO_LLM`, com dez condições
(reversível, sem lock-in, documentar trade-off, etc. — §3.3).

**Escolha construída**: reaproveitar a mesma fonte de evidência já usada para T04/T05
(`escolio.drive.conector`) — correspondência textual entre `ItemDeReferencia.texto`/autor-ano e
o resultado de `buscar_arquivos`/`listar_arquivos_da_pasta`. `escolio/funcoes/bvaa_drive.py`
(mesmo módulo de T04/T05, não um terceiro arquivo) ganhou `EvidenciaDeIdentificacaoDrive` e
`avancar_por_identificacao`, que aplica T01→T02→T03 em sequência a partir da mesma evidência.
`escolio/bvaa/` continua com zero linhas alteradas — a nova função só chama
`escolio.bvaa.maquina.avancar` três vezes, nenhuma lógica de transição nova.

**Trade-off documentado** (condição 4 da instrução): Drive não distingue "obra" de "edição"
como conceitos independentes — um arquivo é as duas coisas ao mesmo tempo, então a mesma
evidência licencia T01 e T02 juntos, não duas evidências separadas. Isso não é uma leitura de
que P04 trata obra e edição como equivalentes (não trata — `transicoes.py` mantém as duas
transições distintas); é reconhecer que a única fonte de metadados disponível (nome do arquivo)
não separa os dois níveis. Reversível: um catálogo bibliográfico estruturado futuro poderia
licenciar T02 com evidência própria sem mudar T01 nem os chamadores existentes.

Testes de `avancar_por_identificacao` e da cadeia completa identificação+acesso em
`tests/funcoes/test_execucao_p13.py::TestEtapaOnzeVerificacaoDeFontes` — ver
`escolio/funcoes/LACUNAS.md` (sessão de 2026-08-12, etapa 11 estendida) para o lado do
orquestrador.

## Sessão de 2026-08-13 — curador automático: extração determinística + busca real, escalonamento só quando genuinamente travado

Decisão do `USUARIO_PROPONENTE`: a etapa 11 do P13 não deve exigir, por padrão, que um humano já
tenha construído `EvidenciaDeIdentificacaoDrive`/`EvidenciaDeAcessoDrive` — o sistema deve tentar
produzir essa evidência sozinho, por meios já autorizados (`escolio.drive`, único conector real do
projeto), e só escalar quando acesso está genuinamente ausente, exige credencial, o material é
privado, ou há decisão humana realmente inescapável — nunca por padrão.

**Construído**: `escolio/bvaa/extracao_metadados_referencia.py` (puro, sem I/O — extrai
autor/ano/título de `ItemDeReferencia.texto` por regex ABNT determinística, `None` quando não
extraível, nunca palpite) e `escolio/funcoes/curador_bvaa.py` (I/O, mesma razão de
`bvaa_drive.py` estar fora de `escolio/bvaa/`: dependência de `escolio.drive.conector`). Wiring em
`execucao_p13.py::_etapa_11_verificacao_de_fontes`: novo campo `EntradaEtapaP13.servico_drive`,
mesmo papel que `cliente` já tem para as etapas 8/9/13/16-18 — objeto pronto > mecanismo
automático > `PONTO_DE_EXTENSAO_DE_MODELO`. Nova causa `CausaDeParada.
ESCALONAMENTO_BIBLIOGRAFICO_NECESSARIO`: o curador tentou e nenhuma referência avançou; motivos
estruturados (`EscalonamentoDoCurador`, vocabulário de `GatilhoDeAbstencao`) anexados à
justificativa, nunca uma frase solta. Progresso parcial (algumas referências avançam, outras
travam) não bloqueia: a etapa continua `EXECUTADA` e os travamentos ficam em
`ContextoExecucaoP13.escalonamentos_bibliograficos`, visível e cumulativo entre chamadas, nunca
descartado. Sem `servico_drive`, comportamento idêntico ao de antes desta sessão — nenhuma
regressão (suíte completa: 1116 → 1135, todos os 1116 anteriores continuam passando).

- **LAC-BVAA-010 — o curador nunca foi exercitado contra uma referência real, porque nenhuma
  existe.** Os três capítulos reais de `data/capitulos/` têm `DocumentoIngerido.referencias == []`
  (LAC-ING-017, `escolio/ingestao/LACUNAS.md`) — nenhum tem seção "Referências"/"Bibliografia"; a
  única forma de citação nos documentos reais é nota de rodapé com citação narrativa "Nome (ano)".
  `_exige_referencia_conhecida` (`execucao_p13.py`, já existente antes desta sessão) exige que toda
  evidência bibliográfica corresponda a um `ItemDeReferencia.unit_id` — o curador, por construção,
  só opera sobre `documento.referencias`, nunca sobre `citacoes_no_corpo`/`notas_de_rodape`. Isso
  não é uma limitação nova desta sessão: é a mesma restrição estrutural que já valia para evidência
  manual, agora também para a automática. **Consequência real**: contra qualquer capítulo real de
  hoje, `ctx.documento.referencias` está vazio, então `tentar_curador` nunca é verdadeiro e a etapa
  11 continua exatamente como antes — `PONTO_DE_EXTENSAO_DE_MODELO` — mesmo com `servico_drive`
  fornecido. O curador só tem efeito real quando a ingestão passar a popular `referencias` para
  `.docx` (não pedido nesta sessão) ou contra um documento de origem PDF com lista de referências
  real (parser de PDF já popula `referencias` — não testado aqui contra PDF real por não haver um
  no acervo de trabalho atual).
- **LAC-BVAA-011 — extração determinística não calibrada contra nenhuma referência real, só
  exemplos sintéticos ABNT.** Mesma causa do item acima: não há string real para calibrar contra.
  `_extrair_titulo` em particular é a heurística mais frágil (split por `.`, segundo campo) —
  funciona para o padrão canônico "SOBRENOME, Nome. Título. Cidade: Editora, Ano." mas não foi
  testada contra variação real (título com ponto interno, referência em inglês/francês com vírgula
  decimal, edição/tradução entre parênteses). Nenhum ajuste foi feito por antecipação — calibrar
  sem dado real repetiria o erro já registrado em `escolio/funcoes/LACUNAS.md` para
  `FATOR_GAP_NOVO_ITEM` ("um documento com espaçamento diferente exigiria recalibração").
- **LAC-BVAA-012 — primeiro resultado de busca é aceito sem desambiguação, sempre.** Quando
  `buscar_arquivos` devolve mais de um arquivo para o mesmo termo, `curar_referencias` usa
  `achados[0]` — nenhum critério de melhor correspondência (nome mais próximo, data de
  modificação, tamanho) foi implementado. Isto é o mesmo trade-off que `bvaa_drive.py` já assume
  para T01/T02 (nenhuma segunda fonte de metadados desambigua obra de edição), estendido aqui para
  "qual arquivo entre vários resultados" — risco de identificação incorreta não eliminado, só não
  pior que a alternativa (não tentar automaticamente). Se isto se mostrar um problema real contra
  dado real, o ponto de correção é `curar_referencias`, sem tocar em `bvaa_drive.py`.
- **LAC-BVAA-013 — `GatilhoDeAbstencao` não distingue "credencial ausente" de "acesso negado" de
  "não encontrado no Drive".** Os três casos que `curar_referencias` pode encontrar ao chamar o
  conector (erro de credencial, `403`, busca vazia) todos caem em `ACESSO_NAO_COMPROVADO` — o
  único gatilho já existente que descreve, em prosa, "acesso não foi comprovado". A distinção
  sobrevive só em `EscalonamentoDoCurador.detalhe` (texto de `ErroDeDrive`, que carrega
  `category`/`severity`/`code` próprios). Nenhum gatilho novo foi criado — o vocabulário de
  `escolio.bvaa.abstencao.GatilhoDeAbstencao` é fechado pela leitura de duas fontes específicas
  (LAC-BVAA-006) e não foi ampliado por conveniência desta sessão.
- **O que este módulo continua não fazendo, por decisão explícita do professor**: busca na
  internet fora do Drive (a regra de 2026-08-09 sobre "buscar na internet novas e melhores
  referências" continua sem implementação — item (2) de LAC-BVAA-008/009, não tocado aqui);
  qualquer tentativa de contornar paywall/DRM; qualquer avanço além de T05 (leitura, página,
  validação continuam exigindo juízo humano ou de modelo sobre o conteúdo, nunca decidido por
  metadado de arquivo).

Testes: `tests/bvaa/test_extracao_metadados_referencia.py` (7 casos), `tests/funcoes/
test_curador_bvaa.py` (7 casos), 5 casos novos em `tests/funcoes/test_execucao_p13.py::
TestEtapaOnzeVerificacaoDeFontes`. Suíte completa: 1135 passando (1116 + 19).

## Não incluído nesta peça (fora de escopo, não lacuna)

- **`RegistroDeRelacoes` / agregação com múltiplas evidências por afirmação** — já é lacuna
  registrada do P05 (`LAC-P05-003`, `escolio/LACUNAS.md`); esta peça não altera isso.
- **Ligação operante entre `RelacaoAfirmacaoEvidencia.claim_id`/`source_id` e um registro de
  `EstadoBibliografico` por obra** — a instrução desta sessão pediu a máquina "sobre o
  schema P05 existente, com os aliases do CON-P05-001", que esta peça cumpre via a tabela
  de correspondência documentada (LAC-BVAA-002). Um índice `source_id -> EstadoBibliografico
  atual`, se necessário no futuro, é extensão nova — não foi pedido nem inferido aqui;
  `escolio/bvaa/` hoje opera sobre `EstadoBibliografico` isolado, sem persistência ou
  vínculo a um `source_id` concreto.
- **Tecnologia, banco, indexador** — P04 explicitamente não escolhe nenhum
  [`02_PROTOCOLO_BVAA_UNIVERSAL_P04_R01.md` §13]; esta implementação também não.

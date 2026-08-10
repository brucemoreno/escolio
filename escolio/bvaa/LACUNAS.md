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

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

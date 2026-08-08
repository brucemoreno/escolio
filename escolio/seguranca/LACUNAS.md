# LACUNAS — ingestão segura P08, item 7 do roadmap

Lacunas encontradas na implementação de `escolio/seguranca/`, a partir da especificação
operacional já escrita em `docs/spec/operacional-P08.md`. Nenhum item aqui foi resolvido por
inferência silenciosa — mesma disciplina de `escolio/LACUNAS.md`, `escolio/funcoes/LACUNAS.md`,
`escolio/bvaa/LACUNAS.md` e `escolio/contrato/LACUNAS.md`.

## Sobre a fonte em si

- **`docs/spec/operacional-P08.md` foi lido integralmente** (871 linhas, 27 RD, 25 DTA, 16 RH) e
  é a fonte direta desta implementação — não o P08 bruto, que já havia sido traduzido em
  mecanismo por aquela especificação. Este módulo não reabre nenhuma das 25 decisões técnicas
  (DTA) daquele documento; implementa-as. Onde a implementação precisou de uma escolha que a
  especificação não continha (ex.: forma exata da normalização de texto), a escolha está
  documentada no docstring da função correspondente, não aqui — porque não é lacuna de spec,
  é detalhe de código que a spec já autorizou (DTA-08).

## Lacunas técnicas transcritas da especificação, agora com estado de implementação

- **LAC-SEG-001** — `[P09 §6]` fixa `security` em três booleanos e não tem onde expressar "ainda
  não analisado" [PR-03]. **Contornado**, não resolvido: `escolio.seguranca.registro.RegistroDeAnalise`
  mantém o estado externamente, por `input_id`. `InputItem.security` (código existente,
  `escolio/contrato/entrada.py`) não foi alterado e continua sem essa distinção — quem consome
  `InputItem.security` sem consultar o registro externo não sabe se `False` é veredito ou
  silêncio. Nenhuma ligação automática entre os dois existe; produzi-la exigiria alterar
  `entrada.py` ou o adaptador (`escolio/adaptadores/ingestao_para_input_item.py`), fora do
  escopo desta sessão — ver `docs/backlog.md`, novo item registrado nesta sessão.

- **LAC-SEG-002** — o passo 12 `[P08 §12]` exige separar texto, metadados e anexos; a ingestão
  (`escolio/ingestao/`) separa metadados e não tem conceito de anexo (DTA-17). **Não
  implementado nesta peça**: `escolio/seguranca/` não cria a classe `Anexo` — isso alteraria
  `escolio/ingestao/modelos.py`, código existente, fora do escopo autorizado. O cenário 5 dos
  testes adversariais roda sobre unidade textual, não sobre anexo real, e o teste correspondente
  (`test_cenario_05_anexo_ordena_exclusao_...`) documenta essa limitação inline.

- **LAC-SEG-003** — metadado embutido no PDF (XMP, comentário, campo de formulário) não é
  extraído pela ingestão; `Metadados` vem de texto das três primeiras páginas (RG-010). O
  cenário 8 dos testes (`test_cenario_08_metadado_contem_ordem_...`) testa a detecção sobre texto
  que *representa* um metadado extraído como texto de unidade — não sobre metadado XMP real, que
  a ingestão não entrega. Ligado à mesma granularidade de célula/campo de formulário que
  `[P13 §10]` exige e a ingestão não entrega (CLAUDE.md §4).

- **LAC-SEG-004** — injeção puramente semântica, sem padrão literal, em unidade de origem
  confiável, não é vista por `escolio.seguranca.deteccao` (DTA-13: o modelo só é chamado quando
  houve achado determinístico ou quando a confiança do item é `NAO_CONFIAVEL`, `SUSPEITO` ou
  `ORIGEM_DESCONHECIDA`). **A camada de modelo (Haiku, E2b) não foi implementada nesta peça** —
  `escolio.seguranca.deteccao.delimita_como_dado` e `valida_rotulo_semantico` preparam a chamada
  (o "envelope" que ela usaria) mas nenhuma chamada de API é feita por este módulo. Consequência:
  todo achado nos testes vem exclusivamente da camada determinística (PI-03/PI-05 literais); o
  "ou equivalentes" que a fonte abre para cada regra permanece não coberto por código, só
  preparado. Nenhuma chamada à API foi feita nesta sessão — mesma ressalva de `[BL-007]`.

- **LAC-SEG-005** — **LACUNA PRESERVADA**, declarada pelo `USUARIO_PROPONENTE` em 2026-08-07
  (`docs/spec/operacional-P08.md` §8.1) e implementada como tal em
  `escolio.seguranca.escalonamento`: `escalona()` não aceita parâmetro de destinatário e sempre
  levanta `ErroDeEscalonamentoSemDestinatario`, citando `[P08 §5.6]`. Os passos 13 e 15 do
  protocolo (`escolio.seguranca.protocolo`, `CoberturaDoPasso.BLOQUEADO_POR_LACUNA_NORMATIVA`) e
  os cenários adversariais 17 e 19 (`tests/seguranca/test_cenarios_adversariais.py`) confirmam a
  recusa em vez de simular uma autoridade. **Não reabrir por conveniência técnica** — só fonte
  nova que nomeie a autoridade justifica revisão, conforme a própria declaração de 2026-08-07.

- **LAC-SEG-006** — `PR-06`/`PR-07` não fixam peso nem corte (DTA-14). O passo 18 do protocolo
  está `BLOQUEADO_POR_LACUNA_NORMATIVA` em `escolio.seguranca.protocolo`, e o cenário 13 dos
  testes adversariais (`test_cenario_13_combinacao_permite_reidentificacao_bloqueado_...`)
  confirma que nenhuma função deste módulo declara risco de reidentificação baixo — a ausência
  da função é o comportamento correto, não uma lacuna de implementação a fechar depois.

- **LAC-SEG-007** — nenhum item deste módulo foi executado contra a API. Não há chamada de
  modelo em código algum de `escolio/seguranca/`; `DTA-11` (Haiku, `effort` `low`) permanece
  proposta não medida. Mesma ressalva de `[BL-007]` que vale para todo o roadmap.

## Lacunas novas, encontradas ao implementar (não estavam na especificação operacional)

- **LAC-SEG-008 — o passo 5 (classificar sensibilidade) e o passo 6 (classificar estado) do
  protocolo estão `BLOQUEADO_POR_LACUNA_NORMATIVA` em `escolio.seguranca.protocolo`, não por
  decisão desta peça, mas por dependerem de `CO-012` e `CO-013` (`docs/coleta.md`), ainda sem
  decisão do professor.** Implementar os passos 5 e 6 com fidelidade exigiria ou (a) alterar
  `escolio/contrato/entrada.py` (`Classification.sensitivity`/`.state`), código existente, fora
  do escopo autorizado desta sessão, ou (b) inventar um valor que não existe no vocabulário
  fechado do P08 (`RotuloDeEstado` não tem "não classificado"), o que seria a inferência proibida
  por `[P00/07; P09 §4.2.14]`. `escolio.seguranca.vocabulario.RotuloDeSensibilidade` e
  `RotuloDeEstado` existem como vocabulário fechado, prontos para uso quando `CO-012`/`CO-013`
  forem decididos; nenhum código deste módulo escreve neles hoje.

- **LAC-SEG-009 — a camada de modelo (E2b, Haiku) descrita em `DTA-04`..`DTA-11` da
  especificação operacional não foi construída nesta peça.** `escolio.seguranca.deteccao`
  implementa integralmente a camada determinística (PI-03, PI-05 literais) e o "envelope" que
  uma chamada de modelo usaria (`delimita_como_dado`, `valida_rotulo_semantico`,
  `ROTULOS_DE_CLASSIFICACAO_SEMANTICA`), mas nenhuma função faz a chamada real ao SDK
  `anthropic`. Isso não é lacuna de especificação — `docs/spec/operacional-P08.md` já decidiu
  tudo o que a camada de modelo precisa (modelo, effort, delimitação, enum fechado) — é escopo
  não executado nesta sessão. Construir a chamada real exigiria criar `prompts/*.md`
  (inexistente no repositório, CLAUDE.md §12) e um cliente do SDK, ambos fora do que foi pedido
  aqui. Ver `docs/backlog.md`.

## Não incluído nesta peça (fora de escopo, não lacuna)

- **Os 16 RH (REVISAO_HUMANA) não têm implementação — são pontos de escalonamento**, conforme a
  instrução da sessão. `escolio.seguranca.escalonamento` implementa o mecanismo genérico de
  escalonamento (DTA-25); não implementa os 15 gatilhos específicos de RH-01 a RH-15 como código
  que os detecta automaticamente — isso exigiria julgamento que os RH, por definição, reservam a
  humano. `RH-16` já estava "ATENDIDO" antes desta peça (LAC-SEG-005, declaração de 2026-08-07).

- **Nenhum arquivo existente foi alterado.** Confirmado: `escolio/contrato/`, `escolio/ingestao/`,
  `escolio/adaptadores/`, `escolio/funcoes/`, `escolio/intervencao/`, `escolio/bvaa/`,
  `escolio/voz/` e `CLAUDE.md` permanecem como estavam antes desta sessão. Onde a integração
  natural exigiria alterá-los (LAC-SEG-001, LAC-SEG-002, LAC-SEG-008), a alteração foi registrada
  em `docs/backlog.md` e não executada.

- **`data/dev/` e `data/gold/` não foram lidos nem processados por este módulo em nenhum
  momento.** `escolio.seguranca.fronteira.recusa_caminho_sob_data` foi testada contra caminhos
  literais (strings), nunca chamada com um caminho real do projeto contra um arquivo que existe
  em disco — a trava é testada, não "testada contra o alvo que ela protege", porque isso seria
  precisamente o que ela existe para impedir.

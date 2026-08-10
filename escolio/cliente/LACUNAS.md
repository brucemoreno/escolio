# LACUNAS — implementação de `escolio/cliente/`

Nenhum item aqui foi resolvido por inferência; cada um documenta a decisão
tomada e por quê.

## Sobre a fonte em si

- **`escolio/cliente/` não é peça numerada do roadmap** — CLAUDE.md §14 lista
  sete peças construídas e não inclui um cliente de API. O próprio prompt
  desta sessão reconhece isso ("Não está no roadmap §14 como peça numerada")
  e autoriza a construção mesmo assim, como infraestrutura sem a qual nenhuma
  peça executa. Não há LAC-P02-005 aplicável (catálogo fechado das seis
  funções, §3) porque este módulo não é uma função nem executa etapa de
  pipeline — é a camada de transporte que uma função futura vai chamar.

## Mapeamento de erro do SDK para P09 §14 — `erros.py`, `mapeamento.py`

- **Categoria/severidade por tipo de exceção do SDK** — P09 §14 define
  `ErrorCategory` e `ErrorSeverity` em abstrato [`escolio/contrato/vocabulario.py`],
  mas nenhuma fonte do acervo associa um código HTTP ou uma exceção do SDK
  `anthropic` a uma categoria específica. A tabela em `mapeamento.py` (429→
  RESOURCE/WARNING retryable; 5xx→INTERNAL/MAJOR retryable; 401/403→
  AUTHORIZATION/CRITICAL; 400/404/422→VALIDATION/MAJOR; timeout/conexão→
  RESOURCE) é `[PROPOSTA]` desta sessão, não dedução de P09. Se uma função
  futura precisar de granularidade diferente (por exemplo, distinguir 404 de
  modelo inexistente de 404 de endpoint errado), essa tabela precisa ser
  revisada, não citada como já homologada.
- **`ErroCacheNaoAproveitado` como INTEGRITY/CRITICAL** — não há fonte que
  classifique "cache não aproveitado" dentro do vocabulário de erro do P09;
  a escolha de INTEGRITY (o defeito está na integridade do prefixo, não na
  requisição em si) e CRITICAL (aborta, não é aviso) é `[PROPOSTA]`.

## Robustez — retry, timeout, backoff

- **Backoff exponencial "configurado explicitamente"** — `anthropic==0.120.2`
  [confirmado por inspeção nesta sessão] expõe `max_retries` (default 2) e
  `timeout`, e já aplica retry com backoff exponencial para 429/5xx/erros de
  conexão dentro desses `max_retries` — mas não expõe parâmetro público para
  o fator de backoff ou jitter em si. "Configurar explicitamente" foi
  interpretado como "não deixar `max_retries`/`timeout` no default implícito
  do SDK", não como "reimplementar o algoritmo de backoff". Se uma versão
  futura do SDK expuser controle mais fino, esta decisão precisa ser revista.
- **`timeout_segundos=900.0` em `configuracao.py`** — nenhuma fonte do
  acervo, nem `docs/custos.md`, declara uma latência esperada para uma
  chamada com prefixo de ~260k tokens; `docs/custos.md` mede custo e
  contagem de tokens, não tempo de resposta. O valor de 900s (15 min) é
  `[PROPOSTA]`, escolhido por ser folgado em relação ao timeout default do
  SDK (10 min) sem medição real de latência. Medir a latência real de uma
  chamada de ~260k tokens de prefixo é pré-requisito para substituir este
  valor por um dimensionado de fato — registrado também em `docs/backlog.md`.

## Retomada de sequência — `cache_local.py`, `estado_prefixo.py`

- **"Falha na chamada N não refaz 1..N-1" implementado via cache local, não
  via estado de sequência dedicado** — o cache local por hash de input já
  soluciona o requisito: se o chamador reexecutar a sequência inteira do
  início após uma falha, as chamadas 1..N-1 (mesmo input) retornam do cache
  sem custo. **Isso pressupõe que o chamador reexecuta a sequência do
  início**, repassando os mesmos inputs 1..N-1 — não há neste módulo uma
  estrutura de "sequência" com posições nomeadas que permita retomar
  arbitrariamente do meio sem repassar os inputs anteriores. Essa
  estrutura pertence à camada de execução modular (E6) das funções, que não
  existe ainda [CLAUDE.md §4]; construí-la aqui seria implementar etapa de
  pipeline, fora do escopo desta peça.
- **Estado de prefixo persiste só o último hash, não um histórico** —
  `estado_prefixo.py` guarda apenas o hash do último prefixo estável com
  escrita de cache confirmada, mais um timestamp com TTL de 1h (o máximo de
  `docs/custos.md`). Isso cobre o caso comum (uma sequência de chamadas de
  diagnóstico consecutivas, mesmo processo ou processo reiniciado dentro de
  1h) mas não cobre uma sequência com múltiplos prefixos estáveis
  intercalados no mesmo processo (por exemplo, duas etapas diferentes
  chamando o cliente alternadamente, cada uma com seu próprio prefixo) — o
  estado seria sobrescrito a cada troca de prefixo, perdendo a capacidade de
  detectar defeito ao voltar ao primeiro prefixo. Nenhuma fonte descreve esse
  cenário; ele fica registrado aqui em vez de resolvido por suposição.

## Cache local — conteúdo armazenado, localização

- **Cache local guarda conteúdo de resposta, ao contrário do ledger** — o
  requisito "reexecutar o mesmo input não custa nada" exige devolver o mesmo
  resultado sem chamar a API de novo, o que exige guardar o texto da
  resposta. Isso é deliberadamente diferente da regra "nunca logar... texto"
  do ledger — o cache local não é log de auditoria, é armazenamento
  funcional necessário para o próprio requisito de custo. Colocado sob
  `data/`, que CLAUDE.md §12 já declara "nunca vai para o git", em vez de
  criar uma nova entrada em `.gitignore` [regra desta peça: "não altere
  código existente"].

## Decisões de implementação verificáveis apenas por proxy

- **Limiar de streaming em 16.000 tokens** — a skill `claude-api`
  (`python/claude-api/streaming.md`) documenta que requisições não-streaming
  com `max_tokens` grande arriscam timeout de SDK, sem dar um número exato de
  corte; 16.000 é o valor usado como referência em vários exemplos da mesma
  skill (`SKILL.md` Cost Optimization / Common Pitfalls: "default a
  ~16000 para não-streaming"). Tratado como escolha de engenharia sensata,
  não como lacuna de conteúdo — mas registrado aqui porque não é um número
  do CLAUDE.md nem de `docs/custos.md`.

## Sessão do piloto real P11 (2026-08-09) — `ErroRespostaTruncada`

Achado do primeiro piloto real de P11 contra os 3 capítulos reais: `chamar()` devolvia
`ResultadoDeChamada` sem checar `stop_reason` — uma resposta cortada por `max_tokens` (o
`thinking` consumiu o teto inteiro antes de gerar conteúdo; `tool_use.input` veio `{}`) era
aceita como sucesso silencioso. Isso violava "SUCCESS não coexiste com limitação impeditiva"
[P09 §21.43] e, por não estar checado no cliente, era um defeito latente em **toda** ponte de
modelo (`ponte_modelo_p13.py` e `ponte_modelo_p11.py`), não só na que o piloto exercitou —
instrução explícita do professor foi corrigir aqui, uma vez, em vez de duplicar a checagem em
cada ponte.

- **`_exigir_resposta_completa`** levanta `ErroRespostaTruncada` quando
  `resultado.stop_reason == "max_tokens"`, checado nos dois caminhos de `chamar()` (chamada
  real e leitura de cache local). Categoria/severidade seguem o mesmo padrão de
  `ErroCacheNaoAproveitado` (INTEGRITY/CRITICAL, não retryable) — mesmo raciocínio: o defeito
  está na integridade do resultado, não na requisição, e repetir com os mesmos parâmetros não
  resolve (o cache local, de propósito, garante que a mesma chamada truncada levanta de novo
  sem gastar dinheiro outra vez — só mudar `max_tokens`/`effort`/o que a etapa pede produz uma
  tentativa nova).
- **A resposta truncada continua sendo salva no cache local e registrada no ledger antes de
  levantar o erro** — o gasto real aconteceu (a API cobra por tokens gerados até o corte) e
  precisa aparecer em `costs/ledger.jsonl`; só o retorno ao chamador como resultado válido é
  que foi bloqueado.
- **Teste de regressão confirmado nos dois sentidos** (`tests/cliente/test_cliente.py`): com o
  código anterior a este achado, o teste falha por `ImportError` (a classe não existia) — com
  a correção, passa; um terceiro teste confirma que `stop_reason="end_turn"` continua não
  levantando nada.
- **Não resolvido aqui, ainda em aberto**: por que `thinking` consome o teto inteiro para um
  prefixo de ~116k tokens em `effort=medium` — se isso persistir mesmo com `max_tokens` maior
  (16.000, ajustado em `ponte_modelo_p11.py` após este achado), o problema é o que a etapa 6
  pede ao modelo, não o teto de tokens. Fica para a próxima tentativa real confirmar.

## Não incluído nesta peça (fora de escopo, não lacuna)

- Nenhuma etapa de pipeline (E1–E7). O cliente só executa a chamada; decidir
  o que perguntar, agrupar unidades por chamada, ou escolher `effort`/modelo
  por etapa é das funções [CLAUDE.md §4, §10], que ainda não existem.
- Chamada real à API. Os testes usam mock do SDK; nenhuma chamada de rede foi
  feita nesta sessão [regra desta peça: "Não chame a API de verdade"].
- `Response.interventions` / mapeamento para `ClaimEvidence` (BL-002, BL-013)
  — este cliente devolve texto/blocos crus; a tradução para o vocabulário do
  P09 §12/§13 é das funções ou de uma peça de adaptação futura, não deste
  módulo de transporte.

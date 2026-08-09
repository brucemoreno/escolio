"""Configuração explícita de robustez — retry e timeout nunca herdam o
default do SDK [regra desta peça].

`anthropic.Anthropic.__init__` [SDK 0.120.2, confirmado por inspeção nesta
sessão] expõe `max_retries: int` (default 2) e `timeout: float | httpx.Timeout`
(default 10 min). O SDK já aplica backoff exponencial e retry automático para
429/5xx/erros de conexão nesses `max_retries` — não há parâmetro público mais
fino (fator de backoff, jitter) na versão instalada; "configurar
explicitamente" aqui significa não deixar o valor no default implícito do
SDK, não reimplementar o backoff. Ver `escolio/cliente/LACUNAS.md`.

`timeout_segundos`: nenhuma fonte do acervo ou de `docs/custos.md` declara
uma latência esperada para um prefixo de ~260k tokens — `docs/custos.md`
mede custo e contagem de tokens, não tempo de resposta. O valor abaixo é
`[PROPOSTA]` desta sessão, não medição; ver `escolio/cliente/LACUNAS.md`.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConfiguracaoDeRobustez:
    max_retries: int = 5
    timeout_segundos: float = 900.0

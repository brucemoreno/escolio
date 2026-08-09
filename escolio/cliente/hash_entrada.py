"""Hash determinístico do payload de uma chamada — usado (a) como chave do
cache local em disco e (b) para detectar "prefixo idêntico" entre chamadas
consecutivas [CLAUDE.md §10].

`json.dumps(..., sort_keys=True)` é obrigatório: a skill `claude-api` cita
`json.dumps` sem `sort_keys` como invalidador silencioso de cache — o mesmo
risco existe aqui para o hash local, que precisa ser estável independente da
ordem de inserção de um dict do chamador.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


def _serializar(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)


def hash_requisicao(
    *,
    model: str,
    system: str,
    mensagens: list[dict],
    tools: list[dict] | None,
    max_tokens: int,
    effort: str,
    thinking: dict | None,
) -> str:
    """Hash da requisição completa — chave do cache local por input."""
    payload = {
        "model": model,
        "system": system,
        "messages": mensagens,
        "tools": tools or [],
        "max_tokens": max_tokens,
        "effort": effort,
        "thinking": thinking,
    }
    return hashlib.sha256(_serializar(payload).encode("utf-8")).hexdigest()


def hash_prefixo_estavel(
    *,
    model: str,
    system: str,
    tools: list[dict] | None,
) -> str:
    """Hash só do bloco estável (system + tools + model) — usado para saber
    se duas chamadas consecutivas compartilham o mesmo prefixo cacheável pela
    API da Anthropic, e portanto se um `cache_read_input_tokens` zerado é
    defeito."""
    payload = {
        "model": model,
        "system": system,
        "tools": tools or [],
    }
    return hashlib.sha256(_serializar(payload).encode("utf-8")).hexdigest()

"""Estado persistido do último prefixo estável escrito em cache remoto
(Anthropic), sobrevivendo a reinício de processo dentro da janela de TTL do
cache.

Sem persistência, o estado "este prefixo já teve escrita de cache" viveria só
em memória no processo — e uma retomada de sequência após crash (novo
processo) perderia a capacidade de detectar `cache_read_input_tokens`
zerado na primeira chamada real após o reinício, mesmo que o cache remoto
ainda estivesse quente. Ver `escolio/cliente/LACUNAS.md`.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path

CAMINHO_PADRAO = Path("data/cache_cliente/_estado_prefixo.json")

# TTL máximo de cache da API é 1h [docs/custos.md § Cache: "TTL máximo é 1 h"].
# Estado mais velho que isso é tratado como se não existisse: o cache remoto
# já teria expirado de qualquer forma.
TTL_MAXIMO_SEGUNDOS = 3600


@dataclass
class EstadoPrefixo:
    hash_prefixo: str | None = None
    escreveu_cache: bool = False
    timestamp_unix: float = 0.0


def carregar(caminho: Path | None = None) -> EstadoPrefixo:
    caminho = caminho or CAMINHO_PADRAO
    if not caminho.exists():
        return EstadoPrefixo()
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    estado = EstadoPrefixo(**dados)
    if time.time() - estado.timestamp_unix > TTL_MAXIMO_SEGUNDOS:
        return EstadoPrefixo()
    return estado


def salvar(estado: EstadoPrefixo, caminho: Path | None = None) -> None:
    caminho = caminho or CAMINHO_PADRAO
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(
        json.dumps(
            {
                "hash_prefixo": estado.hash_prefixo,
                "escreveu_cache": estado.escreveu_cache,
                "timestamp_unix": estado.timestamp_unix,
            }
        ),
        encoding="utf-8",
    )

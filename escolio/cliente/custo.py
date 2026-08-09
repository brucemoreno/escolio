"""Cálculo de custo em US$ a partir de contagens de tokens — fórmulas de
`docs/custos.md` (leitura ~0,1×; escrita 1,25× a 5 min, 2× a 1 h). Consome os
preços de `precos.py`, nunca um valor solto no código [CLAUDE.md §10, §11].
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .precos import (
    MULTIPLICADOR_ESCRITA_CACHE_1H,
    MULTIPLICADOR_ESCRITA_CACHE_5M,
    MULTIPLICADOR_LEITURA_CACHE,
    preco_de,
)


@dataclass(frozen=True)
class CustoCalculado:
    custo_usd_input_nao_cacheado: float
    custo_usd_escrita_cache: float
    custo_usd_leitura_cache: float
    custo_usd_output: float

    @property
    def total(self) -> float:
        return (
            self.custo_usd_input_nao_cacheado
            + self.custo_usd_escrita_cache
            + self.custo_usd_leitura_cache
            + self.custo_usd_output
        )


def calcular_custo(
    *,
    id_modelo: str,
    input_tokens: int,
    cache_creation_input_tokens: int,
    cache_read_input_tokens: int,
    output_tokens: int,
    ttl_cache: str = "5m",
    hoje: date | None = None,
) -> CustoCalculado:
    preco = preco_de(id_modelo, hoje=hoje)
    multiplicador_escrita = (
        MULTIPLICADOR_ESCRITA_CACHE_1H if ttl_cache == "1h" else MULTIPLICADOR_ESCRITA_CACHE_5M
    )
    return CustoCalculado(
        custo_usd_input_nao_cacheado=input_tokens * preco.input_por_milhao_usd / 1_000_000,
        custo_usd_escrita_cache=(
            cache_creation_input_tokens * preco.input_por_milhao_usd * multiplicador_escrita / 1_000_000
        ),
        custo_usd_leitura_cache=(
            cache_read_input_tokens * preco.input_por_milhao_usd * MULTIPLICADOR_LEITURA_CACHE / 1_000_000
        ),
        custo_usd_output=output_tokens * preco.output_por_milhao_usd / 1_000_000,
    )

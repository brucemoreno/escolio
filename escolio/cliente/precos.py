"""Tabela de preços — transcrita de `docs/custos.md` (data de verificação:
2026-06-24, cache da skill `claude-api`). Não estimar de memória [CLAUDE.md
§10, §11]: qualquer modelo ausente daqui levanta `ErroModeloSemPreco` em vez
de um valor chutado.

`docs/custos.md` marca "Reverificar antes de qualquer decisão de orçamento" —
antes de usar este módulo para uma decisão real de custo, confirmar que a
tabela abaixo ainda corresponde à fonte.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .erros import ErroModeloSemPreco

ARQUIVO_ORIGEM = "docs/custos.md"
DATA_VERIFICACAO = date(2026, 6, 24)


@dataclass(frozen=True)
class PrecoModelo:
    id_modelo: str
    input_por_milhao_usd: float
    output_por_milhao_usd: float
    minimo_cacheavel_tokens: int
    valido_ate: date | None = None
    preco_apos_prazo: "PrecoModelo | None" = None


_SONNET5_PADRAO = PrecoModelo(
    id_modelo="claude-sonnet-5",
    input_por_milhao_usd=3.00,
    output_por_milhao_usd=15.00,
    minimo_cacheavel_tokens=1024,
)

_SONNET5_INTRODUTORIO = PrecoModelo(
    id_modelo="claude-sonnet-5",
    input_por_milhao_usd=2.00,
    output_por_milhao_usd=10.00,
    minimo_cacheavel_tokens=1024,
    valido_ate=date(2026, 8, 31),
    preco_apos_prazo=_SONNET5_PADRAO,
)

TABELA_PRECOS: dict[str, PrecoModelo] = {
    "claude-opus-5": PrecoModelo(
        id_modelo="claude-opus-5",
        input_por_milhao_usd=5.00,
        output_por_milhao_usd=25.00,
        minimo_cacheavel_tokens=512,
    ),
    "claude-sonnet-5": _SONNET5_INTRODUTORIO,
    "claude-haiku-4-5": PrecoModelo(
        id_modelo="claude-haiku-4-5",
        input_por_milhao_usd=1.00,
        output_por_milhao_usd=5.00,
        minimo_cacheavel_tokens=4096,
    ),
}

# Cache — multiplicadores sobre o preço de input [docs/custos.md § Cache]
MULTIPLICADOR_ESCRITA_CACHE_5M = 1.25
MULTIPLICADOR_ESCRITA_CACHE_1H = 2.0
MULTIPLICADOR_LEITURA_CACHE = 0.1


def preco_de(id_modelo: str, hoje: date | None = None) -> PrecoModelo:
    """Preço vigente para `id_modelo` na data `hoje` (padrão: hoje real).

    `hoje` é parâmetro explícito (não `date.today()` interno) para que a
    transição de preço introdutório do Sonnet 5 (vigente até 2026-08-31) seja
    testável de forma determinística.
    """
    base = TABELA_PRECOS.get(id_modelo)
    if base is None:
        raise ErroModeloSemPreco(id_modelo)

    referencia = hoje if hoje is not None else date.today()
    if base.valido_ate is not None and referencia > base.valido_ate:
        return base.preco_apos_prazo or base
    return base

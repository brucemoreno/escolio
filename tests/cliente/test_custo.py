from datetime import date

import pytest

from escolio.cliente.custo import calcular_custo


def test_custo_input_simples_sonnet5_preco_introdutorio():
    custo = calcular_custo(
        id_modelo="claude-sonnet-5",
        input_tokens=1_000_000,
        cache_creation_input_tokens=0,
        cache_read_input_tokens=0,
        output_tokens=0,
        hoje=date(2026, 7, 1),
    )
    assert custo.custo_usd_input_nao_cacheado == 2.00
    assert custo.total == 2.00


def test_custo_escrita_de_cache_5m_multiplica_1_25():
    custo = calcular_custo(
        id_modelo="claude-sonnet-5",
        input_tokens=0,
        cache_creation_input_tokens=1_000_000,
        cache_read_input_tokens=0,
        output_tokens=0,
        ttl_cache="5m",
        hoje=date(2026, 7, 1),
    )
    assert custo.custo_usd_escrita_cache == 2.00 * 1.25


def test_custo_escrita_de_cache_1h_multiplica_2():
    custo = calcular_custo(
        id_modelo="claude-sonnet-5",
        input_tokens=0,
        cache_creation_input_tokens=1_000_000,
        cache_read_input_tokens=0,
        output_tokens=0,
        ttl_cache="1h",
        hoje=date(2026, 7, 1),
    )
    assert custo.custo_usd_escrita_cache == 2.00 * 2.0


def test_custo_leitura_de_cache_multiplica_0_1():
    custo = calcular_custo(
        id_modelo="claude-sonnet-5",
        input_tokens=0,
        cache_creation_input_tokens=0,
        cache_read_input_tokens=1_000_000,
        output_tokens=0,
        hoje=date(2026, 7, 1),
    )
    assert custo.custo_usd_leitura_cache == 2.00 * 0.1


def test_cenario_docs_custos_md_65_chamadas_com_cache():
    """Reproduz o Cenário 2 de docs/custos.md (~US$ 5,92) como checagem de
    sanidade das fórmulas, dentro de margem de arredondamento do doc fonte."""
    escrita = calcular_custo(
        id_modelo="claude-sonnet-5",
        input_tokens=0,
        cache_creation_input_tokens=259_399,
        cache_read_input_tokens=0,
        output_tokens=3_000,
        ttl_cache="5m",
        hoje=date(2026, 7, 1),
    )
    leituras = calcular_custo(
        id_modelo="claude-sonnet-5",
        input_tokens=0,
        cache_creation_input_tokens=0,
        cache_read_input_tokens=64 * 259_399,
        output_tokens=64 * 3_000,
        ttl_cache="5m",
        hoje=date(2026, 7, 1),
    )
    total = escrita.total + leituras.total
    assert total == pytest.approx(5.92, abs=0.01)

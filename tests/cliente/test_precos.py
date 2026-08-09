from datetime import date

import pytest

from escolio.cliente.erros import ErroModeloSemPreco
from escolio.cliente.precos import preco_de


def test_preco_de_modelo_conhecido():
    preco = preco_de("claude-opus-5")
    assert preco.input_por_milhao_usd == 5.00
    assert preco.output_por_milhao_usd == 25.00
    assert preco.minimo_cacheavel_tokens == 512


def test_preco_de_modelo_desconhecido_levanta_erro_tipado():
    with pytest.raises(ErroModeloSemPreco):
        preco_de("claude-inventado-99")


def test_sonnet5_preco_introdutorio_antes_do_prazo():
    preco = preco_de("claude-sonnet-5", hoje=date(2026, 8, 31))
    assert preco.input_por_milhao_usd == 2.00
    assert preco.output_por_milhao_usd == 10.00


def test_sonnet5_preco_padrao_apos_prazo():
    preco = preco_de("claude-sonnet-5", hoje=date(2026, 9, 1))
    assert preco.input_por_milhao_usd == 3.00
    assert preco.output_por_milhao_usd == 15.00

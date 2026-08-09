import json
from types import SimpleNamespace
from unittest.mock import MagicMock

import anthropic
import httpx
import pytest

from escolio.cliente.cache_local import CacheLocal
from escolio.cliente.cliente import ClienteAnthropic
from escolio.cliente.erros import (
    ErroCacheNaoAproveitado,
    ErroDeLimiteDeTaxa,
    ErroEffortAusente,
    ErroMaxTokensAusente,
)
from escolio.cliente.ledger import Ledger

_UNIDADES_A = [{"type": "text", "text": "unidade A"}]
_UNIDADES_B = [{"type": "text", "text": "unidade B"}]


def resposta_fake(
    *,
    texto="resultado",
    input_tokens=100,
    output_tokens=50,
    cache_creation_input_tokens=0,
    cache_read_input_tokens=0,
    model="claude-sonnet-5",
    stop_reason="end_turn",
    id_="msg_teste",
):
    usage = SimpleNamespace(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cache_creation_input_tokens=cache_creation_input_tokens,
        cache_read_input_tokens=cache_read_input_tokens,
    )
    return SimpleNamespace(
        usage=usage,
        content=[{"type": "text", "text": texto}],
        model=model,
        stop_reason=stop_reason,
        id=id_,
    )


def cliente_de_teste(tmp_path, sdk=None):
    return ClienteAnthropic(
        cliente_sdk=sdk or MagicMock(),
        cache=CacheLocal(diretorio=tmp_path / "cache"),
        ledger=Ledger(caminho=tmp_path / "costs" / "ledger.jsonl"),
        caminho_estado_prefixo=tmp_path / "estado_prefixo.json",
    )


# --- regra: effort explícito obrigatório -----------------------------------


def test_effort_ausente_levanta_erro_e_nao_chama_sdk(tmp_path):
    sdk = MagicMock()
    cliente = cliente_de_teste(tmp_path, sdk)

    with pytest.raises(ErroEffortAusente):
        cliente.chamar(
            model="claude-sonnet-5",
            system_estavel="prefixo",
            unidades=_UNIDADES_A,
            max_tokens=1024,
            effort="",
        )

    sdk.messages.create.assert_not_called()


# --- regra: max_tokens explícito obrigatório --------------------------------


def test_max_tokens_ausente_levanta_erro_e_nao_chama_sdk(tmp_path):
    sdk = MagicMock()
    cliente = cliente_de_teste(tmp_path, sdk)

    with pytest.raises(ErroMaxTokensAusente):
        cliente.chamar(
            model="claude-sonnet-5",
            system_estavel="prefixo",
            unidades=_UNIDADES_A,
            max_tokens=0,
            effort="medium",
        )

    sdk.messages.create.assert_not_called()


# --- regra: cache_control no bloco estável do system ------------------------


def test_system_recebe_cache_control_no_bloco_estavel(tmp_path):
    sdk = MagicMock()
    sdk.messages.create.return_value = resposta_fake()
    cliente = cliente_de_teste(tmp_path, sdk)

    cliente.chamar(
        model="claude-sonnet-5",
        system_estavel="prefixo estável",
        unidades=_UNIDADES_A,
        max_tokens=1024,
        effort="medium",
    )

    kwargs = sdk.messages.create.call_args.kwargs
    assert kwargs["system"] == [
        {"type": "text", "text": "prefixo estável", "cache_control": {"type": "ephemeral", "ttl": "5m"}}
    ]


# --- regra: max_tokens e effort explícitos repassados ao SDK ---------------


def test_max_tokens_e_effort_explicitos_repassados_ao_sdk(tmp_path):
    sdk = MagicMock()
    sdk.messages.create.return_value = resposta_fake()
    cliente = cliente_de_teste(tmp_path, sdk)

    cliente.chamar(
        model="claude-sonnet-5",
        system_estavel="prefixo",
        unidades=_UNIDADES_A,
        max_tokens=2048,
        effort="xhigh",
    )

    kwargs = sdk.messages.create.call_args.kwargs
    assert kwargs["max_tokens"] == 2048
    assert kwargs["output_config"] == {"effort": "xhigh"}


def test_thinking_default_e_adaptive_quando_nao_informado(tmp_path):
    sdk = MagicMock()
    sdk.messages.create.return_value = resposta_fake()
    cliente = cliente_de_teste(tmp_path, sdk)

    cliente.chamar(
        model="claude-sonnet-5",
        system_estavel="prefixo",
        unidades=_UNIDADES_A,
        max_tokens=1024,
        effort="medium",
    )

    kwargs = sdk.messages.create.call_args.kwargs
    assert kwargs["thinking"] == {"type": "adaptive"}


# --- regra: cache local por hash --------------------------------------------


def test_chamada_real_grava_no_cache_local_e_no_ledger(tmp_path):
    sdk = MagicMock()
    sdk.messages.create.return_value = resposta_fake(
        input_tokens=10, output_tokens=5, cache_creation_input_tokens=200, cache_read_input_tokens=0
    )
    cliente = cliente_de_teste(tmp_path, sdk)

    resultado = cliente.chamar(
        model="claude-sonnet-5",
        system_estavel="prefixo",
        unidades=_UNIDADES_A,
        max_tokens=1024,
        effort="medium",
    )

    assert resultado.veio_do_cache_local is False
    assert resultado.texto == "resultado"
    linha = json.loads((tmp_path / "costs" / "ledger.jsonl").read_text().strip())
    assert linha["cache_creation_input_tokens"] == 200
    assert linha["veio_do_cache_local"] is False


def test_segunda_chamada_identica_usa_cache_local_sem_tocar_sdk(tmp_path):
    sdk = MagicMock()
    sdk.messages.create.return_value = resposta_fake(
        input_tokens=10, output_tokens=5, cache_creation_input_tokens=0, cache_read_input_tokens=0
    )
    cliente = cliente_de_teste(tmp_path, sdk)

    parametros = dict(
        model="claude-sonnet-5",
        system_estavel="prefixo",
        unidades=_UNIDADES_A,
        max_tokens=1024,
        effort="medium",
    )

    primeiro = cliente.chamar(**parametros)
    segundo = cliente.chamar(**parametros)

    assert primeiro.veio_do_cache_local is False
    assert segundo.veio_do_cache_local is True
    assert segundo.custo_usd == 0.0
    assert segundo.texto == primeiro.texto
    sdk.messages.create.assert_called_once()  # a segunda chamada não tocou o SDK

    linhas = (tmp_path / "costs" / "ledger.jsonl").read_text().strip().splitlines()
    assert len(linhas) == 2
    assert json.loads(linhas[1])["veio_do_cache_local"] is True


# --- regra: aborta se cache_read_input_tokens vier zerado em prefixo repetido


def test_cache_nao_aproveitado_em_prefixo_repetido_aborta(tmp_path):
    sdk = MagicMock()
    sdk.messages.create.side_effect = [
        resposta_fake(cache_creation_input_tokens=1000, cache_read_input_tokens=0, id_="msg_1"),
        resposta_fake(cache_creation_input_tokens=0, cache_read_input_tokens=0, id_="msg_2"),
    ]
    cliente = cliente_de_teste(tmp_path, sdk)

    # Primeira chamada: escreve cache remoto (cache_creation > 0) — sucesso normal.
    cliente.chamar(
        model="claude-sonnet-5",
        system_estavel="prefixo repetido",
        unidades=_UNIDADES_A,
        max_tokens=1024,
        effort="medium",
    )

    # Segunda chamada: mesmo prefixo estável, unidades diferentes (não bate no
    # cache local), mas cache_read_input_tokens volta zerado — defeito.
    with pytest.raises(ErroCacheNaoAproveitado):
        cliente.chamar(
            model="claude-sonnet-5",
            system_estavel="prefixo repetido",
            unidades=_UNIDADES_B,
            max_tokens=1024,
            effort="medium",
        )

    assert sdk.messages.create.call_count == 2


def test_prefixo_diferente_nao_aciona_checagem_de_cache(tmp_path):
    sdk = MagicMock()
    sdk.messages.create.side_effect = [
        resposta_fake(cache_creation_input_tokens=1000, cache_read_input_tokens=0, id_="msg_1"),
        resposta_fake(cache_creation_input_tokens=1000, cache_read_input_tokens=0, id_="msg_2"),
    ]
    cliente = cliente_de_teste(tmp_path, sdk)

    cliente.chamar(
        model="claude-sonnet-5",
        system_estavel="prefixo X",
        unidades=_UNIDADES_A,
        max_tokens=1024,
        effort="medium",
    )
    # Prefixo diferente do anterior — cache_read=0 aqui é esperado (primeira
    # vez que este prefixo é usado), não deve abortar.
    resultado = cliente.chamar(
        model="claude-sonnet-5",
        system_estavel="prefixo Y",
        unidades=_UNIDADES_A,
        max_tokens=1024,
        effort="medium",
    )
    assert resultado.veio_do_cache_local is False


# --- regra: erros tipados mapeados a partir de exceções do SDK -------------


def test_erro_do_sdk_e_mapeado_para_erro_tipado(tmp_path):
    request = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
    response = httpx.Response(429, request=request)
    sdk = MagicMock()
    sdk.messages.create.side_effect = anthropic.RateLimitError(
        "limite excedido", response=response, body=None
    )
    cliente = cliente_de_teste(tmp_path, sdk)

    with pytest.raises(ErroDeLimiteDeTaxa):
        cliente.chamar(
            model="claude-sonnet-5",
            system_estavel="prefixo",
            unidades=_UNIDADES_A,
            max_tokens=1024,
            effort="medium",
        )


# --- estimativa de custo antes de executar ----------------------------------


def test_estimar_custo_usa_count_tokens_sem_gerar_resposta(tmp_path):
    sdk = MagicMock()
    sdk.messages.count_tokens.return_value = SimpleNamespace(input_tokens=500)
    cliente = cliente_de_teste(tmp_path, sdk)

    custo = cliente.estimar_custo(
        model="claude-haiku-4-5",
        system_estavel="prefixo",
        unidades=_UNIDADES_A,
        max_tokens=1000,
    )

    esperado = (500 * 1.00 / 1_000_000) + (1000 * 5.00 / 1_000_000)
    assert custo == pytest.approx(esperado)
    sdk.messages.create.assert_not_called()
    sdk.messages.stream.assert_not_called()


# --- chamada de diagnóstico isolada: sem histórico acumulado ----------------


def test_mensagens_nunca_acumulam_historico_entre_chamadas(tmp_path):
    sdk = MagicMock()
    sdk.messages.create.return_value = resposta_fake()
    cliente = cliente_de_teste(tmp_path, sdk)

    cliente.chamar(
        model="claude-sonnet-5",
        system_estavel="prefixo",
        unidades=_UNIDADES_A,
        max_tokens=1024,
        effort="medium",
    )
    cliente.chamar(
        model="claude-sonnet-5",
        system_estavel="prefixo",
        unidades=_UNIDADES_B,
        max_tokens=1024,
        effort="medium",
    )

    for chamada in sdk.messages.create.call_args_list:
        assert chamada.kwargs["messages"] == [{"role": "user", "content": chamada.kwargs["messages"][0]["content"]}]
        assert len(chamada.kwargs["messages"]) == 1  # nunca mais de uma mensagem — sem histórico


# --- streaming automático acima do limiar de max_tokens ---------------------


def test_streaming_usado_quando_max_tokens_grande(tmp_path):
    sdk = MagicMock()
    stream_cm = MagicMock()
    stream_cm.__enter__.return_value.get_final_message.return_value = resposta_fake()
    sdk.messages.stream.return_value = stream_cm
    cliente = cliente_de_teste(tmp_path, sdk)

    cliente.chamar(
        model="claude-sonnet-5",
        system_estavel="prefixo",
        unidades=_UNIDADES_A,
        max_tokens=32_000,
        effort="high",
    )

    sdk.messages.stream.assert_called_once()
    sdk.messages.create.assert_not_called()

from escolio.cliente.cache_local import CacheLocal, RespostaCache


def test_cache_local_retorna_none_quando_ausente(tmp_path):
    cache = CacheLocal(diretorio=tmp_path)
    assert cache.obter("hash-inexistente") is None


def test_cache_local_salvar_e_obter_roundtrip(tmp_path):
    cache = CacheLocal(diretorio=tmp_path)
    resposta = RespostaCache(
        texto_blocos=[{"type": "text", "text": "resultado"}],
        usage={"input_tokens": 10, "output_tokens": 5, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0},
        model="claude-sonnet-5",
        stop_reason="end_turn",
    )
    cache.salvar("hash-1", resposta)

    obtido = cache.obter("hash-1")

    assert obtido is not None
    assert obtido.texto_blocos == resposta.texto_blocos
    assert obtido.usage == resposta.usage
    assert obtido.model == "claude-sonnet-5"
    assert obtido.stop_reason == "end_turn"


def test_cache_local_reexecutar_mesmo_hash_nao_sobrescreve_com_erro(tmp_path):
    cache = CacheLocal(diretorio=tmp_path)
    resposta = RespostaCache(texto_blocos=[], usage={}, model="m", stop_reason=None)
    cache.salvar("hash-1", resposta)
    cache.salvar("hash-1", resposta)  # idempotente — não deve levantar
    assert cache.obter("hash-1") is not None

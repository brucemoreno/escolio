from escolio.cliente.hash_entrada import hash_prefixo_estavel, hash_requisicao


def _params(**overrides):
    base = dict(
        model="claude-sonnet-5",
        system="prefixo estável",
        mensagens=[{"role": "user", "content": [{"type": "text", "text": "unidade 1"}]}],
        tools=None,
        max_tokens=1024,
        effort="medium",
        thinking={"type": "adaptive"},
    )
    base.update(overrides)
    return base


def test_mesmo_input_produz_mesmo_hash():
    assert hash_requisicao(**_params()) == hash_requisicao(**_params())


def test_input_diferente_produz_hash_diferente():
    h1 = hash_requisicao(**_params())
    h2 = hash_requisicao(**_params(effort="high"))
    assert h1 != h2


def test_ordem_de_chaves_do_dict_nao_afeta_hash():
    # json.dumps(..., sort_keys=True) deve neutralizar dicts construídos em
    # ordens diferentes — o mesmo invalidador silencioso citado em
    # docs/custos.md para o cache remoto vale aqui para o hash local.
    mensagens_a = [{"role": "user", "content": [{"type": "text", "text": "x"}]}]
    mensagens_b = [{"content": [{"text": "x", "type": "text"}], "role": "user"}]
    h1 = hash_requisicao(**_params(mensagens=mensagens_a))
    h2 = hash_requisicao(**_params(mensagens=mensagens_b))
    assert h1 == h2


def test_hash_prefixo_estavel_ignora_unidades_da_chamada():
    h1 = hash_prefixo_estavel(model="claude-sonnet-5", system="prefixo", tools=None)
    h2 = hash_prefixo_estavel(model="claude-sonnet-5", system="prefixo", tools=None)
    assert h1 == h2


def test_hash_prefixo_estavel_muda_com_system():
    h1 = hash_prefixo_estavel(model="claude-sonnet-5", system="prefixo A", tools=None)
    h2 = hash_prefixo_estavel(model="claude-sonnet-5", system="prefixo B", tools=None)
    assert h1 != h2

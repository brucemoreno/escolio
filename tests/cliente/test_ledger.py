import json

from escolio.cliente.ledger import Ledger, RegistroDeCusto


def _registro(**overrides):
    base = dict(
        timestamp_unix=1_700_000_000.0,
        request_id="msg_abc123",
        model="claude-sonnet-5",
        effort="medium",
        cache_creation_input_tokens=1000,
        cache_read_input_tokens=0,
        input_tokens=50,
        output_tokens=200,
        custo_usd_input_nao_cacheado=0.0001,
        custo_usd_escrita_cache=0.0025,
        custo_usd_leitura_cache=0.0,
        custo_usd_output=0.002,
        custo_usd_total=0.0046,
        veio_do_cache_local=False,
    )
    base.update(overrides)
    return RegistroDeCusto(**base)


def test_ledger_grava_uma_linha_jsonl_por_registro(tmp_path):
    caminho = tmp_path / "ledger.jsonl"
    ledger = Ledger(caminho=caminho)

    ledger.registrar(_registro())
    ledger.registrar(_registro(request_id="msg_def456"))

    linhas = caminho.read_text(encoding="utf-8").strip().splitlines()
    assert len(linhas) == 2
    primeiro = json.loads(linhas[0])
    assert primeiro["request_id"] == "msg_abc123"
    segundo = json.loads(linhas[1])
    assert segundo["request_id"] == "msg_def456"


def test_ledger_cria_diretorio_pai_se_ausente(tmp_path):
    caminho = tmp_path / "subdir" / "ledger.jsonl"
    ledger = Ledger(caminho=caminho)
    ledger.registrar(_registro())
    assert caminho.exists()


def test_ledger_registra_contagens_separadas_de_cache(tmp_path):
    caminho = tmp_path / "ledger.jsonl"
    ledger = Ledger(caminho=caminho)
    ledger.registrar(_registro(cache_creation_input_tokens=111, cache_read_input_tokens=222, input_tokens=333))

    linha = json.loads(caminho.read_text(encoding="utf-8").strip())
    assert linha["cache_creation_input_tokens"] == 111
    assert linha["cache_read_input_tokens"] == 222
    assert linha["input_tokens"] == 333


def test_ledger_nunca_contem_texto_nem_chave(tmp_path):
    """Regra desta peça: 'o ledger registra contagens e custo, não texto'."""
    caminho = tmp_path / "ledger.jsonl"
    ledger = Ledger(caminho=caminho)
    ledger.registrar(_registro())

    linha = json.loads(caminho.read_text(encoding="utf-8").strip())
    campos_permitidos = {
        "timestamp_unix",
        "request_id",
        "model",
        "effort",
        "cache_creation_input_tokens",
        "cache_read_input_tokens",
        "input_tokens",
        "output_tokens",
        "custo_usd_input_nao_cacheado",
        "custo_usd_escrita_cache",
        "custo_usd_leitura_cache",
        "custo_usd_output",
        "custo_usd_total",
        "veio_do_cache_local",
        "etapa",
        "sequence_id",
        "indice_na_sequencia",
    }
    assert set(linha.keys()) == campos_permitidos
    for chave in ("texto", "content", "system", "mensagem", "api_key", "chave"):
        assert chave not in linha

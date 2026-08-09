from unittest.mock import MagicMock, patch

from escolio.cliente.cliente import ClienteAnthropic
from escolio.cliente.configuracao import ConfiguracaoDeRobustez


def test_configuracao_padrao_nao_e_o_default_do_sdk():
    """SDK default é max_retries=2 [anthropic==0.120.2]; este cliente nunca
    deve herdar esse default silenciosamente."""
    config = ConfiguracaoDeRobustez()
    assert config.max_retries != 2
    assert config.max_retries > 0
    assert config.timeout_segundos > 0


def test_cliente_configura_sdk_explicitamente_sem_cliente_sdk_injetado(tmp_path):
    with patch("escolio.cliente.cliente.anthropic.Anthropic") as construtor:
        construtor.return_value = MagicMock()
        config = ConfiguracaoDeRobustez(max_retries=7, timeout_segundos=123.0)
        ClienteAnthropic(
            config=config,
            caminho_estado_prefixo=tmp_path / "estado.json",
        )
        construtor.assert_called_once_with(max_retries=7, timeout=123.0)


def test_cliente_sdk_injetado_nao_reconstroi_o_sdk(tmp_path):
    with patch("escolio.cliente.cliente.anthropic.Anthropic") as construtor:
        sdk_falso = MagicMock()
        ClienteAnthropic(cliente_sdk=sdk_falso, caminho_estado_prefixo=tmp_path / "estado.json")
        construtor.assert_not_called()

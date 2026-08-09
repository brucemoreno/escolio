import anthropic
import httpx

from escolio.cliente.erros import (
    ErroDeAutorizacao,
    ErroDeConexao,
    ErroDeLimiteDeTaxa,
    ErroDeRequisicaoInvalida,
    ErroDeRespostaInesperada,
    ErroDeServidor,
    ErroDeTimeout,
)
from escolio.cliente.mapeamento import mapear_erro_sdk
from escolio.contrato.vocabulario import ErrorCategory, ErrorSeverity

_REQUEST = httpx.Request("POST", "https://api.anthropic.com/v1/messages")


def _resposta_http(status: int) -> httpx.Response:
    return httpx.Response(status, request=_REQUEST)


def test_rate_limit_mapeia_para_erro_retryable_warning():
    exc = anthropic.RateLimitError("limite excedido", response=_resposta_http(429), body=None)
    erro = mapear_erro_sdk(exc)
    assert isinstance(erro, ErroDeLimiteDeTaxa)
    assert erro.category == ErrorCategory.RESOURCE
    assert erro.severity == ErrorSeverity.WARNING
    assert erro.retryable is True


def test_erro_servidor_5xx_mapeia_para_retryable_major():
    exc = anthropic.InternalServerError("falha interna", response=_resposta_http(500), body=None)
    erro = mapear_erro_sdk(exc)
    assert isinstance(erro, ErroDeServidor)
    assert erro.category == ErrorCategory.INTERNAL
    assert erro.severity == ErrorSeverity.MAJOR
    assert erro.retryable is True


def test_autenticacao_mapeia_para_authorization_critical_nao_retryable():
    exc = anthropic.AuthenticationError("chave inválida", response=_resposta_http(401), body=None)
    erro = mapear_erro_sdk(exc)
    assert isinstance(erro, ErroDeAutorizacao)
    assert erro.category == ErrorCategory.AUTHORIZATION
    assert erro.severity == ErrorSeverity.CRITICAL
    assert erro.retryable is False


def test_bad_request_mapeia_para_validation_nao_retryable():
    exc = anthropic.BadRequestError("payload inválido", response=_resposta_http(400), body=None)
    erro = mapear_erro_sdk(exc)
    assert isinstance(erro, ErroDeRequisicaoInvalida)
    assert erro.category == ErrorCategory.VALIDATION
    assert erro.retryable is False


def test_erro_de_conexao_mapeia_para_retryable():
    exc = anthropic.APIConnectionError(request=_REQUEST)
    erro = mapear_erro_sdk(exc)
    assert isinstance(erro, ErroDeConexao)
    assert erro.retryable is True


def test_timeout_mapeia_para_retryable_antes_de_conexao_generica():
    exc = anthropic.APITimeoutError(_REQUEST)
    erro = mapear_erro_sdk(exc)
    assert isinstance(erro, ErroDeTimeout)
    assert erro.retryable is True


def test_status_desconhecido_mapeia_para_resposta_inesperada():
    exc = anthropic.APIStatusError("teapot", response=_resposta_http(418), body=None)
    erro = mapear_erro_sdk(exc)
    assert isinstance(erro, ErroDeRespostaInesperada)


def test_detalhe_nunca_contem_a_chave_de_api():
    exc = anthropic.RateLimitError(
        "limite excedido para sk-ant-abcDEF12345_fake", response=_resposta_http(429), body=None
    )
    erro = mapear_erro_sdk(exc)
    assert "sk-ant-" not in (erro.detail or "")

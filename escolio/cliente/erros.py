"""Erros tipados do cliente da API, mapeados às categorias e severidades de
`ErrorPayload` [P09 §14] — reaproveitadas de `escolio.contrato.vocabulario`,
nunca redefinidas aqui [regra desta peça: "reuse escolio/contrato/"].

O mapeamento de uma exceção do SDK Anthropic (código HTTP, timeout, erro de
conexão) para uma categoria/severidade do P09 §14 não vem de nenhuma fonte do
acervo — P09 §14 define o vocabulário em abstrato, não a correspondência com
a mecânica de um SDK específico. Toda associação abaixo é `[PROPOSTA]` desta
sessão; ver `escolio/cliente/LACUNAS.md`.
"""

from __future__ import annotations

from escolio.contrato.vocabulario import ErrorCategory, ErrorSeverity


class ErroDeCliente(Exception):
    """Base de todo erro levantado por `escolio.cliente`.

    `category`/`severity` usam o vocabulário do P09 §14, para que quem captura
    o erro possa construir um `ErrorPayload` [escolio.contrato.payloads] sem
    reinterpretar a exceção.
    """

    def __init__(
        self,
        category: ErrorCategory,
        severity: ErrorSeverity,
        code: str,
        message: str,
        *,
        detail: str | None = None,
        retryable: bool = False,
    ) -> None:
        self.category = category
        self.severity = severity
        self.code = code
        self.detail = detail
        self.retryable = retryable
        super().__init__(f"[{category.value}/{severity.value}] {code}: {message}")


class ErroEffortAusente(ErroDeCliente):
    """`output_config.effort` não foi informado.

    CLAUDE.md §10: "omitir roda em `high`, que é desperdício silencioso" — o
    cliente nunca aplica esse default por conta própria; a ausência é erro,
    não uma escolha implícita.
    """

    def __init__(self) -> None:
        super().__init__(
            ErrorCategory.VALIDATION,
            ErrorSeverity.MAJOR,
            "EFFORT_AUSENTE",
            "output_config.effort não foi informado pelo chamador — "
            "o cliente não aplica default silencioso [CLAUDE.md §10].",
        )


class ErroMaxTokensAusente(ErroDeCliente):
    """`max_tokens` não foi informado ou é zero/negativo."""

    def __init__(self) -> None:
        super().__init__(
            ErrorCategory.VALIDATION,
            ErrorSeverity.MAJOR,
            "MAX_TOKENS_AUSENTE",
            "max_tokens não foi informado (ou é <= 0) — obrigatório em toda "
            "chamada [CLAUDE.md §10].",
        )


class ErroModeloSemPreco(ErroDeCliente):
    """Modelo não está na tabela de preços transcrita de docs/custos.md."""

    def __init__(self, id_modelo: str) -> None:
        super().__init__(
            ErrorCategory.VALIDATION,
            ErrorSeverity.MAJOR,
            "MODELO_SEM_PRECO",
            f"Modelo '{id_modelo}' não está em docs/custos.md — preço não "
            "pode ser estimado de memória [CLAUDE.md §10, §11].",
        )


class ErroDeRequisicaoInvalida(ErroDeCliente):
    """400 / 404 / 422 — erro do lado do chamador, não retryable."""

    def __init__(self, message: str, *, detail: str | None = None) -> None:
        super().__init__(
            ErrorCategory.VALIDATION,
            ErrorSeverity.MAJOR,
            "REQUISICAO_INVALIDA",
            message,
            detail=detail,
        )


class ErroDeAutorizacao(ErroDeCliente):
    """401 / 403 — chave inválida ou sem permissão. Não retryable."""

    def __init__(self, message: str, *, detail: str | None = None) -> None:
        super().__init__(
            ErrorCategory.AUTHORIZATION,
            ErrorSeverity.CRITICAL,
            "AUTORIZACAO_NEGADA",
            message,
            detail=detail,
        )


class ErroDeLimiteDeTaxa(ErroDeCliente):
    """429 — retryable com backoff exponencial."""

    def __init__(self, message: str, *, detail: str | None = None) -> None:
        super().__init__(
            ErrorCategory.RESOURCE,
            ErrorSeverity.WARNING,
            "LIMITE_DE_TAXA",
            message,
            detail=detail,
            retryable=True,
        )


class ErroDeServidor(ErroDeCliente):
    """5xx — retryable com backoff exponencial."""

    def __init__(self, message: str, *, detail: str | None = None) -> None:
        super().__init__(
            ErrorCategory.INTERNAL,
            ErrorSeverity.MAJOR,
            "ERRO_DE_SERVIDOR",
            message,
            detail=detail,
            retryable=True,
        )


class ErroDeConexao(ErroDeCliente):
    """Falha de conexão (rede) antes de qualquer resposta HTTP. Retryable."""

    def __init__(self, message: str, *, detail: str | None = None) -> None:
        super().__init__(
            ErrorCategory.RESOURCE,
            ErrorSeverity.WARNING,
            "ERRO_DE_CONEXAO",
            message,
            detail=detail,
            retryable=True,
        )


class ErroDeTimeout(ErroDeCliente):
    """Timeout explícito estourado. Retryable."""

    def __init__(self, message: str, *, detail: str | None = None) -> None:
        super().__init__(
            ErrorCategory.RESOURCE,
            ErrorSeverity.MAJOR,
            "TIMEOUT",
            message,
            detail=detail,
            retryable=True,
        )


class ErroCacheNaoAproveitado(ErroDeCliente):
    """`cache_read_input_tokens` zerado em requisição de prefixo idêntico.

    CLAUDE.md §10: "é defeito, não ruído" — aborta a execução, não retryable
    (o retry não resolve um invalidador silencioso no prefixo).
    """

    def __init__(self, esperado_min: int, obtido: int, *, detail: str | None = None) -> None:
        super().__init__(
            ErrorCategory.INTEGRITY,
            ErrorSeverity.CRITICAL,
            "CACHE_NAO_APROVEITADO",
            f"cache_read_input_tokens={obtido} (esperado >= {esperado_min}) em "
            "requisição de prefixo idêntico — invalidador silencioso no "
            "prefixo [CLAUDE.md §10].",
            detail=detail,
        )


class ErroDeRespostaInesperada(ErroDeCliente):
    """Qualquer exceção do SDK não coberta pelas categorias acima."""

    def __init__(self, message: str, *, detail: str | None = None) -> None:
        super().__init__(
            ErrorCategory.INTERNAL,
            ErrorSeverity.CRITICAL,
            "ERRO_NAO_MAPEADO",
            message,
            detail=detail,
        )

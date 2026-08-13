"""Erros tipados do conector de busca externa, mapeados às categorias e
severidades de `ErrorPayload` [P09 §14] — mesma disciplina de
`escolio/drive/erros.py`.

O mapeamento de um erro HTTP do provedor de busca (Serper.dev) para uma
categoria/severidade do P09 §14 não vem de nenhuma fonte do acervo — é
`[PROPOSTA]` desta sessão, mesmo raciocínio de `escolio/drive/erros.py`.
"""

from __future__ import annotations

from escolio.contrato.vocabulario import ErrorCategory, ErrorSeverity


class ErroDeBusca(Exception):
    """Base de todo erro levantado por `escolio.busca`."""

    def __init__(
        self,
        category: ErrorCategory,
        severity: ErrorSeverity,
        code: str,
        message: str,
        *,
        detail: str | None = None,
    ) -> None:
        self.category = category
        self.severity = severity
        self.code = code
        self.detail = detail
        super().__init__(f"[{category.value}/{severity.value}] {code}: {message}")


class ErroDeCredencialDeBusca(ErroDeBusca):
    """`api_key` ausente ou vazia — este módulo não lê variável de
    ambiente nem decide se a credencial existe; quem chama fornece a
    chave [mesmo padrão de `escolio.drive.conector.construir_servico`]."""

    def __init__(self, *, detail: str | None = None) -> None:
        super().__init__(
            ErrorCategory.VALIDATION,
            ErrorSeverity.CRITICAL,
            "CREDENCIAL_DE_BUSCA_AUSENTE",
            "api_key de busca (Serper.dev) não fornecida",
            detail=detail,
        )


class ErroDeRespostaDeBusca(ErroDeBusca):
    """Falha de conexão, status HTTP não-200, ou corpo que não corresponde
    ao formato esperado da API de busca."""

    def __init__(self, message: str, *, detail: str | None = None) -> None:
        super().__init__(
            ErrorCategory.INTERNAL,
            ErrorSeverity.MAJOR,
            "RESPOSTA_DE_BUSCA_INVALIDA",
            message,
            detail=detail,
        )

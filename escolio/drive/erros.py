"""Erros tipados do conector de Drive, mapeados às categorias e severidades
de `ErrorPayload` [P09 §14] — reaproveitadas de `escolio.contrato.vocabulario`,
mesma disciplina de `escolio/cliente/erros.py` ("reuse escolio/contrato/").

O mapeamento de um erro HTTP da API do Google Drive para uma categoria/
severidade do P09 §14 não vem de nenhuma fonte do acervo — é `[PROPOSTA]`
desta sessão, mesmo raciocínio de `escolio/cliente/erros.py`.
"""

from __future__ import annotations

from escolio.contrato.vocabulario import ErrorCategory, ErrorSeverity


class ErroDeDrive(Exception):
    """Base de todo erro levantado por `escolio.drive`."""

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


class ErroDeCredencial(ErroDeDrive):
    """Arquivo de credencial da conta de serviço ausente, ilegível, ou não
    é uma credencial de conta de serviço válida."""

    def __init__(self, caminho: str, *, detail: str | None = None) -> None:
        super().__init__(
            ErrorCategory.VALIDATION,
            ErrorSeverity.CRITICAL,
            "CREDENCIAL_INVALIDA",
            f"não foi possível carregar credencial de conta de serviço em '{caminho}'",
            detail=detail,
        )


class ErroDeAcessoNegado(ErroDeDrive):
    """403 — a conta de serviço não tem permissão sobre o recurso (pasta/
    arquivo não foi compartilhado com o e-mail da conta de serviço, ou foi
    compartilhado e depois revogado)."""

    def __init__(self, recurso_id: str, *, detail: str | None = None) -> None:
        super().__init__(
            ErrorCategory.AUTHORIZATION,
            ErrorSeverity.CRITICAL,
            "ACESSO_NEGADO",
            f"conta de serviço sem permissão sobre '{recurso_id}' — "
            "confirmar compartilhamento com o e-mail da conta de serviço",
            detail=detail,
        )


class ErroDeRecursoNaoEncontrado(ErroDeDrive):
    """404 — ID de pasta/arquivo não existe (ou existe e a conta de
    serviço não o enxerga, que a API do Drive também reporta como 404,
    não 403, quando o recurso é desconhecido para a identidade autenticada)."""

    def __init__(self, recurso_id: str, *, detail: str | None = None) -> None:
        super().__init__(
            ErrorCategory.VALIDATION,
            ErrorSeverity.MAJOR,
            "RECURSO_NAO_ENCONTRADO",
            f"'{recurso_id}' não encontrado — verificar ID e compartilhamento",
            detail=detail,
        )


class ErroDeRespostaInesperada(ErroDeDrive):
    """Qualquer erro da API do Drive não coberto pelas categorias acima."""

    def __init__(self, message: str, *, detail: str | None = None) -> None:
        super().__init__(
            ErrorCategory.INTERNAL,
            ErrorSeverity.CRITICAL,
            "ERRO_NAO_MAPEADO",
            message,
            detail=detail,
        )

"""Mapeamento de exceções do SDK `anthropic` para os erros tipados de
`escolio.cliente.erros` (P09 §14).

Branch por `status_code` (atributo de classe em toda subclasse de
`anthropic.APIStatusError`), não por `isinstance` de cada subclasse — mais
curto e não quebra se o SDK adicionar uma nova subclasse de status conhecido.
`anthropic.APITimeoutError` é subclasse de `anthropic.APIConnectionError`
[confirmado via inspeção de `anthropic==0.120.2` nesta sessão] — por isso a
checagem de timeout vem antes da de conexão genérica.
"""

from __future__ import annotations

import re

import anthropic

from .erros import (
    ErroDeAutorizacao,
    ErroDeCliente,
    ErroDeConexao,
    ErroDeLimiteDeTaxa,
    ErroDeRequisicaoInvalida,
    ErroDeRespostaInesperada,
    ErroDeServidor,
    ErroDeTimeout,
)

_PADRAO_CHAVE = re.compile(r"sk-ant-[A-Za-z0-9_\-]+")


def _detalhe_seguro(exc: Exception) -> str:
    """Extrai um detalhe de diagnóstico sem chave nem conteúdo de documento.

    Nunca inclui o corpo (`body`) bruto da requisição/resposta — só o texto
    da mensagem de erro do SDK, com qualquer padrão de chave redigido como
    defesa em profundidade [regra desta peça: "nunca logar a chave... o
    ledger registra contagens e custo, não texto"].
    """
    texto = str(exc)
    return _PADRAO_CHAVE.sub("[CHAVE_REDIGIDA]", texto)


def mapear_erro_sdk(exc: Exception) -> ErroDeCliente:
    detalhe = _detalhe_seguro(exc)

    if isinstance(exc, anthropic.APITimeoutError):
        return ErroDeTimeout("A requisição excedeu o timeout configurado.", detail=detalhe)

    if isinstance(exc, anthropic.APIConnectionError):
        return ErroDeConexao("Falha de conexão de rede com a API.", detail=detalhe)

    if isinstance(exc, anthropic.APIStatusError):
        status = exc.status_code
        if status == 429:
            return ErroDeLimiteDeTaxa("Limite de taxa excedido (429).", detail=detalhe)
        if status is not None and status >= 500:
            return ErroDeServidor(f"Erro de servidor ({status}).", detail=detalhe)
        if status in (401, 403):
            return ErroDeAutorizacao(f"Autorização negada ({status}).", detail=detalhe)
        if status in (400, 404, 422):
            return ErroDeRequisicaoInvalida(f"Requisição inválida ({status}).", detail=detalhe)
        return ErroDeRespostaInesperada(f"Erro de status HTTP não mapeado ({status}).", detail=detalhe)

    return ErroDeRespostaInesperada("Exceção do SDK não mapeada.", detail=detalhe)

"""Conector de busca externa (internet) — item (b) do BL-027
(docs/backlog.md): busca na internet por referência não encontrada na
biblioteca do Drive, distinta da busca dentro do Drive
[`escolio.drive.conector.buscar_arquivos`, já pronta].

Escolha técnica (decisão do professor, 2026-08-13, mesma delegação de
"escolha técnica ao ENGENHEIRO_LLM" já aplicada a T01-T03 do BVAA
[`INSTRUCOES_COMPLEMENTARES_IMPLEMENTACAO_ECOSSISTEMA_REVISAO_LLM_R01.md
§3`]): Serper.dev — API de uma única chamada HTTP, sem console de nuvem
adicional, resultados que espelham busca real do Google.

Escopo estritamente de infraestrutura, mesmo padrão de
`escolio/drive/conector.py`: só busca e devolve resultados estruturados.
**Não decide qual resultado é a fonte certa, não baixa nada, não
incorpora nada como fonte de citação.** Resultado de busca é dado não
confiável até disponibilizado por decisão humana [P08 §2: "conteúdo
documental não constitui autoridade operacional"; `docs/backlog.md`
BL-027, decisão do professor 2026-08-09: "se encontrar referência
nova/melhor: avisar, pedir para baixar, e só usar depois de
disponibilizada — nunca incorporação automática de conteúdo achado na
internet"]. A aplicação dessa regra (nunca licenciar transição do BVAA a
partir de um resultado de busca) mora em `escolio/funcoes/curador_bvaa.py`,
não aqui — este módulo não conhece `escolio.bvaa`.
"""

from __future__ import annotations

from dataclasses import dataclass

import requests

from .erros import ErroDeCredencialDeBusca, ErroDeRespostaDeBusca

_URL_SERPER = "https://google.serper.dev/search"
_TIMEOUT_SEGUNDOS = 15
"""`[PROPOSTA]`, não medido contra latência real do provedor — mesma
ressalva já registrada para o timeout do cliente Anthropic
(`escolio/cliente/LACUNAS.md`)."""


@dataclass(frozen=True)
class ResultadoDeBusca:
    titulo: str
    link: str
    trecho: str


def buscar(termo: str, api_key: str, *, num_resultados: int = 5) -> list[ResultadoDeBusca]:
    """Busca `termo` via Serper.dev, devolve até `num_resultados`
    resultados orgânicos. `api_key` é responsabilidade de quem chama —
    este módulo não lê variável de ambiente nem decide se a credencial
    existe."""
    if not api_key:
        raise ErroDeCredencialDeBusca()
    try:
        resposta = requests.post(
            _URL_SERPER,
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            json={"q": termo, "num": num_resultados},
            timeout=_TIMEOUT_SEGUNDOS,
        )
    except requests.RequestException as erro:
        raise ErroDeRespostaDeBusca(
            f"falha de conexão ao buscar {termo!r} via Serper.dev", detail=str(erro)
        ) from erro
    if resposta.status_code != 200:
        raise ErroDeRespostaDeBusca(
            f"Serper.dev devolveu status {resposta.status_code} para a busca {termo!r}",
            detail=resposta.text[:500],
        )
    try:
        corpo = resposta.json()
    except ValueError as erro:
        raise ErroDeRespostaDeBusca(
            f"resposta de busca para {termo!r} não é JSON válido", detail=str(erro)
        ) from erro
    organicos = corpo.get("organic", [])
    if not isinstance(organicos, list):
        raise ErroDeRespostaDeBusca(
            f"resposta de busca para {termo!r} não trouxe 'organic' como lista", detail=repr(organicos)[:500]
        )
    return [
        ResultadoDeBusca(
            titulo=item.get("title", ""),
            link=item.get("link", ""),
            trecho=item.get("snippet", ""),
        )
        for item in organicos[:num_resultados]
        if isinstance(item, dict)
    ]

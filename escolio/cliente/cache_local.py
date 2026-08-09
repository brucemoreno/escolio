"""Cache local em disco por hash do input — "reexecutar o mesmo input não
custa nada" [CLAUDE.md §10].

Distinto do ledger (`ledger.py`): o ledger nunca registra texto, só contagens
e custo. Este cache precisa guardar o conteúdo da resposta para poder
devolvê-lo sem chamar a API de novo — por isso vive sob `data/`, que
CLAUDE.md §12 já declara "nunca vai para o git", em vez de em `costs/` (que é
só números) ou em local novo que exigiria editar `.gitignore` [regra desta
peça: "não altere código existente"].

Este mesmo mecanismo implementa "retomada de sequência: falha na chamada N
não refaz 1..N-1" — se o chamador reexecutar a sequência inteira do início
após uma falha, as chamadas 1..N-1 (mesmo input, já cacheadas) retornam do
disco sem custo; só a chamada N em diante toca a API de verdade. Ver
`escolio/cliente/LACUNAS.md` para a suposição que isso carrega (o chamador
precisa reexecutar a sequência do início, não retomar de um ponto arbitrário
sem repassar os inputs 1..N-1).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

DIRETORIO_PADRAO = Path("data/cache_cliente")


@dataclass
class RespostaCache:
    """Serialização mínima de uma resposta bem-sucedida, suficiente para
    reconstruir `ResultadoDeChamada` sem tocar a API de novo."""

    texto_blocos: list[dict] = field(default_factory=list)
    usage: dict = field(default_factory=dict)
    model: str = ""
    stop_reason: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


class CacheLocal:
    def __init__(self, diretorio: Path | None = None) -> None:
        self.diretorio = diretorio or DIRETORIO_PADRAO

    def _caminho(self, chave_hash: str) -> Path:
        return self.diretorio / f"{chave_hash}.json"

    def obter(self, chave_hash: str) -> RespostaCache | None:
        caminho = self._caminho(chave_hash)
        if not caminho.exists():
            return None
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        return RespostaCache(**dados)

    def salvar(self, chave_hash: str, resposta: RespostaCache) -> None:
        self.diretorio.mkdir(parents=True, exist_ok=True)
        caminho = self._caminho(chave_hash)
        caminho.write_text(
            json.dumps(resposta.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

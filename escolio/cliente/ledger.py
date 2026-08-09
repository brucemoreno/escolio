"""Ledger de custo — `costs/ledger.jsonl` [CLAUDE.md §10].

Registra contagens de tokens e custo em US$, nunca texto nem a chave de API
[regra desta peça]. `RegistroDeCusto` só tem campos numéricos/identificadores
— não há campo para conteúdo de mensagem, resposta ou system prompt. Um
registro por chamada real; chamadas servidas pelo cache local também geram
registro (com custo zero e `veio_do_cache_local=True`), para que o ledger
reflita toda chamada lógica, não só toda chamada de rede.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

CAMINHO_PADRAO = Path("costs/ledger.jsonl")


@dataclass
class RegistroDeCusto:
    timestamp_unix: float
    request_id: str
    model: str
    effort: str
    cache_creation_input_tokens: int
    cache_read_input_tokens: int
    input_tokens: int
    output_tokens: int
    custo_usd_input_nao_cacheado: float
    custo_usd_escrita_cache: float
    custo_usd_leitura_cache: float
    custo_usd_output: float
    custo_usd_total: float
    veio_do_cache_local: bool
    etapa: str | None = None
    sequence_id: str | None = None
    indice_na_sequencia: int | None = None

    def to_dict(self) -> dict:
        return asdict(self)


class Ledger:
    def __init__(self, caminho: Path | None = None) -> None:
        self.caminho = caminho or CAMINHO_PADRAO

    def registrar(self, registro: RegistroDeCusto) -> None:
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        with self.caminho.open("a", encoding="utf-8") as arquivo:
            arquivo.write(json.dumps(registro.to_dict(), ensure_ascii=False))
            arquivo.write("\n")

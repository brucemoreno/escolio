"""Protocolo de identificadores e versionamento — fonte:
06_PROTOCOLO_DE_IDENTIFICADORES_E_VERSIONAMENTO_P05_R01.txt.

Padrões (arquivo 01, seção 5 e arquivo 06, seção 1):
- claim_id: CLM-<DOMINIO>-<IDENTIFICADOR_UNICO>
- source_id: SRC-<TIPO>-<IDENTIFICADOR_UNICO>
- EX- é proibido fora de exemplos abstratos (não aplicado em produção por
  este módulo; ver LACUNAS.md).
"""

import re

from escolio.erros import ErroDeIdentificador

CLAIM_ID_PADRAO = re.compile(r"^CLM-[^-]+-[^-]+.*$")
SOURCE_ID_PADRAO = re.compile(r"^SRC-[^-]+-[^-]+.*$")


class RegistroDeIdentificadores:
    """Índice de IDs já emitidos. Unicidade global; verificação obrigatória
    antes de emitir/gravar novo ID (arquivo 06, seção 2)."""

    def __init__(self):
        self._claim_ids: set[str] = set()
        self._source_ids: set[str] = set()
        self._claim_ids_invalidados: set[str] = set()
        self._source_ids_invalidados: set[str] = set()

    def registrar_claim_id(self, claim_id: str) -> None:
        if not CLAIM_ID_PADRAO.match(claim_id):
            raise ErroDeIdentificador(
                f"claim_id '{claim_id}' não segue o padrão CLM-<DOMINIO>-<IDENTIFICADOR_UNICO>"
            )
        if claim_id in self._claim_ids or claim_id in self._claim_ids_invalidados:
            raise ErroDeIdentificador(
                f"claim_id '{claim_id}' já existe ou foi invalidado; IDs não são reciclados (RC-016)"
            )
        self._claim_ids.add(claim_id)

    def registrar_source_id(self, source_id: str) -> None:
        if not SOURCE_ID_PADRAO.match(source_id):
            raise ErroDeIdentificador(
                f"source_id '{source_id}' não segue o padrão SRC-<TIPO>-<IDENTIFICADOR_UNICO>"
            )
        if source_id in self._source_ids or source_id in self._source_ids_invalidados:
            raise ErroDeIdentificador(
                f"source_id '{source_id}' já existe ou foi invalidado; IDs não são reciclados (RC-016)"
            )
        self._source_ids.add(source_id)

    def source_id_conhecido(self, source_id: str) -> bool:
        return source_id in self._source_ids

    def claim_id_conhecido(self, claim_id: str) -> bool:
        return claim_id in self._claim_ids

    def claim_id_invalidado(self, claim_id: str) -> bool:
        return claim_id in self._claim_ids_invalidados

    def source_id_invalidado(self, source_id: str) -> bool:
        return source_id in self._source_ids_invalidados

    def invalidar_claim_id(self, claim_id: str) -> None:
        """Marca o ID como definitivamente não reutilizável (arquivo 06,
        seção 3: erro de identidade cria novo registro e marca o anterior
        como invalidado, preservado)."""
        if claim_id not in self._claim_ids:
            raise ErroDeIdentificador(f"claim_id '{claim_id}' não está registrado")
        self._claim_ids.remove(claim_id)
        self._claim_ids_invalidados.add(claim_id)

    def invalidar_source_id(self, source_id: str) -> None:
        if source_id not in self._source_ids:
            raise ErroDeIdentificador(f"source_id '{source_id}' não está registrado")
        self._source_ids.remove(source_id)
        self._source_ids_invalidados.add(source_id)

"""Registro de relações — organiza múltiplas RelacaoAfirmacaoEvidencia,
aplica as regras que dependem de mais de uma relação (RC-012, RC-013,
RC-014, RC-017, RC-018) e implementa a rastreabilidade bidirecional
(fonte: 07_PROTOCOLO_DE_RASTREABILIDADE_BIDIRECIONAL_P05_R01.txt).
"""

from escolio.erros import ErroDeCoerencia
from escolio.identificadores import RegistroDeIdentificadores
from escolio.relacao import RelacaoAfirmacaoEvidencia
from escolio.regras_coerencia import ARQUIVO_REGRAS, validar_regras_coerencia
from escolio.vocabulario import Sufficiency

ARQUIVO_RASTREABILIDADE = "07_PROTOCOLO_DE_RASTREABILIDADE_BIDIRECIONAL_P05_R01.txt"


class RegistroDeRelacoes:
    def __init__(self, identificadores: RegistroDeIdentificadores | None = None):
        self.identificadores = identificadores or RegistroDeIdentificadores()
        # chave: (claim_id, source_id) -> lista de versões (relation_version crescente)
        self._relacoes: dict[tuple[str, str], list[RelacaoAfirmacaoEvidencia]] = {}
        # edição em que a página de um par (claim_id, source_id) foi confirmada pela primeira vez
        self._edicao_pagina_confirmada: dict[tuple[str, str], str] = {}

    def adicionar(
        self,
        r: RelacaoAfirmacaoEvidencia,
        eh_ids_novos: bool = True,
        eh_substituicao: bool = False,
    ) -> None:
        chave = (r.claim_id, r.source_id)

        # RC-017: uma evidência usada por múltiplas afirmações mantém
        # source_id e relações separadas — isto é, uma relação por
        # claim_id para o mesmo source_id, nunca uma relação fundindo dois
        # claims. Verificamos que não existe relação com o mesmo source_id
        # e claim_id diferente sendo tratada como se fosse a mesma chave —
        # isso é garantido estruturalmente pela chave (claim_id, source_id),
        # então RC-017 é satisfeito por construção do dicionário _relacoes.

        # RC-018: uma afirmação com múltiplas evidências mantém uma relação
        # por source_id — cada nova relation_version para a MESMA chave
        # (claim_id, source_id) é uma versão da mesma relação, não uma
        # relação nova fundida; isso também é garantido pela chave composta.

        validar_regras_coerencia(r)

        if eh_ids_novos:
            if self.identificadores.claim_id_invalidado(r.claim_id):
                self.identificadores.registrar_claim_id(r.claim_id)  # dispara ErroDeIdentificador (RC-016)
            if not self.identificadores.source_id_conhecido(r.source_id):
                self.identificadores.registrar_source_id(r.source_id)
            if not self.identificadores.claim_id_conhecido(r.claim_id):
                self.identificadores.registrar_claim_id(r.claim_id)

        if r.relation_version > 1 or eh_substituicao:
            from escolio.regras_coerencia import rc_014
            rc_014(r.notes, eh_substituicao)

        if chave in self._edicao_pagina_confirmada:
            from escolio.regras_coerencia import rc_013
            rc_013(r, self._edicao_pagina_confirmada[chave])

        from escolio.vocabulario import ValidationState
        if r.validation_state == ValidationState.PAGINA_CONFIRMADA and chave not in self._edicao_pagina_confirmada:
            self._edicao_pagina_confirmada[chave] = r.edition_or_version

        self._relacoes.setdefault(chave, []).append(r)

    def marcar_conflito(self, claim_id: str, source_ids: list[str]) -> None:
        """Aplica RC-012: evidências conflitantes para a mesma afirmação
        exigem sufficiency=CONFLITANTE em todas as relações envolvidas."""
        for source_id in source_ids:
            chave = (claim_id, source_id)
            for r in self._relacoes.get(chave, []):
                if r.sufficiency != Sufficiency.CONFLITANTE:
                    raise ErroDeCoerencia(
                        "RC-012",
                        "Evidências conflitantes exigem sufficiency=CONFLITANTE até resolução/delimitação",
                        ARQUIVO_REGRAS,
                        f"relação {chave} versão {r.relation_version} está como {r.sufficiency}",
                    )

    def relacoes_por_claim(self, claim_id: str) -> list[RelacaoAfirmacaoEvidencia]:
        """Rastreabilidade afirmação -> evidência (arquivo 07): não oculta
        relações invalidadas, conflitantes ou substituídas."""
        resultado = []
        for (c, _s), versoes in self._relacoes.items():
            if c == claim_id:
                resultado.extend(versoes)
        return resultado

    def relacoes_por_source(self, source_id: str) -> list[RelacaoAfirmacaoEvidencia]:
        """Rastreabilidade evidência -> afirmações (arquivo 07)."""
        resultado = []
        for (_c, s), versoes in self._relacoes.items():
            if s == source_id:
                resultado.extend(versoes)
        return resultado

    def versoes(self, claim_id: str, source_id: str) -> list[RelacaoAfirmacaoEvidencia]:
        return list(self._relacoes.get((claim_id, source_id), []))

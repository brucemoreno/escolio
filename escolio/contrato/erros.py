"""Exceções do contrato P09.

Toda rejeição cita o invariante ou a regra violada e o arquivo de origem
(mesma disciplina de escolio/erros.py: "toda rejeição é rastreável")."""

ARQUIVO_P09 = "P09_SCHEMAS_CONTRATOS_CORRIGIDO_R04.md"


class ErroDeContrato(Exception):
    """Violação de um invariante (§21), regra de campo obrigatório (§4.1,
    §6.1, §8.1) ou regra de coerência status/payload (§8.2, §9, §11, §14-16)
    do envelope P09."""

    def __init__(self, regra_id: str, fundamento: str, arquivo_origem: str = ARQUIVO_P09, detalhe: str = ""):
        self.regra_id = regra_id
        self.fundamento = fundamento
        self.arquivo_origem = arquivo_origem
        self.detalhe = detalhe
        msg = f"[{regra_id}] {fundamento} (fonte: {arquivo_origem})"
        if detalhe:
            msg += f" — {detalhe}"
        super().__init__(msg)

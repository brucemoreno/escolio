"""Exceções do schema P13Comment.

Toda rejeição cita o identificador da regra e o arquivo de origem — mesma
disciplina de escolio/erros.py e escolio/contrato/erros.py: "toda rejeição
é rastreável".
"""

from escolio.comentarios.vocabulario import ARQUIVO_FONTE


class ErroDeComentario(Exception):
    """Violação de uma regra de nulidade, obrigatoriedade condicional ou
    integridade referencial de `P13Comment` [§31.5, §42]."""

    def __init__(self, regra_id: str, fundamento: str, arquivo_origem: str = ARQUIVO_FONTE, detalhe: str = ""):
        self.regra_id = regra_id
        self.fundamento = fundamento
        self.arquivo_origem = arquivo_origem
        self.detalhe = detalhe
        msg = f"[{regra_id}] {fundamento} (fonte: {arquivo_origem})"
        if detalhe:
            msg += f" — {detalhe}"
        super().__init__(msg)

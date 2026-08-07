"""Exceções do perfil de voz autoral (P07) — mesma disciplina de
escolio/contrato/erros.py e escolio/bvaa/erros.py: toda rejeição cita a
regra e o arquivo de origem."""

ARQUIVO_CONTRATO = "01_CONTRATO_UNIVERSAL_DE_VOZ_AUTORAL_P07_R01.md"


class ErroDePerfilDeVoz(Exception):
    """Violação de um princípio, regra de gate ou regra de coerência do
    contrato P07."""

    def __init__(self, regra_id: str, fundamento: str, arquivo_origem: str = ARQUIVO_CONTRATO, detalhe: str = ""):
        self.regra_id = regra_id
        self.fundamento = fundamento
        self.arquivo_origem = arquivo_origem
        self.detalhe = detalhe
        msg = f"[{regra_id}] {fundamento} (fonte: {arquivo_origem})"
        if detalhe:
            msg += f" — {detalhe}"
        super().__init__(msg)

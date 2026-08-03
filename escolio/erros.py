"""Exceções do schema afirmação-evidência.

Toda rejeição cita o identificador da regra e o arquivo de origem
(regra do prompt: "toda rejeição é rastreável").
"""


class ErroDeCoerencia(Exception):
    """Violação de uma regra de coerência (arquivo 04) ou de um campo do
    dicionário de dados (arquivo 02)."""

    def __init__(self, regra_id: str, fundamento: str, arquivo_origem: str, detalhe: str = ""):
        self.regra_id = regra_id
        self.fundamento = fundamento
        self.arquivo_origem = arquivo_origem
        self.detalhe = detalhe
        msg = f"[{regra_id}] {fundamento} (fonte: {arquivo_origem})"
        if detalhe:
            msg += f" — {detalhe}"
        super().__init__(msg)


class AlertaDeCoerencia:
    """Sinalização não bloqueante. O CSV de regras (arquivo 04) usa
    severidade BLOQUEANTE ou MAIOR; nenhuma regra ali é do tipo alerta puro,
    mas a distinção é preservada para fidelidade ao esquema de severidade."""

    def __init__(self, regra_id: str, fundamento: str, arquivo_origem: str, detalhe: str = ""):
        self.regra_id = regra_id
        self.fundamento = fundamento
        self.arquivo_origem = arquivo_origem
        self.detalhe = detalhe

    def __repr__(self):
        return f"AlertaDeCoerencia([{self.regra_id}] {self.fundamento} — {self.detalhe})"


class ErroDeIdentificador(Exception):
    """Violação do protocolo de identificadores e versionamento (arquivo 06)."""

    def __init__(self, mensagem: str, arquivo_origem: str = "06_PROTOCOLO_DE_IDENTIFICADORES_E_VERSIONAMENTO_P05_R01.txt"):
        self.arquivo_origem = arquivo_origem
        super().__init__(f"{mensagem} (fonte: {arquivo_origem})")

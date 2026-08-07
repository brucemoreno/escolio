"""Exceções da máquina de estados bibliográficos.

Toda rejeição cita a transição/regra violada e o arquivo de origem —
mesma disciplina de escolio/erros.py e escolio/contrato/erros.py.
"""

from escolio.bvaa.vocabulario import ARQUIVO_MATRIZ_TRANSICOES


class ErroDeTransicaoBibliografica(Exception):
    """Transição não listada na matriz (arquivo 04) — nenhuma transição é
    inferida por adjacência ou plausibilidade [P04/03 §5: "nenhum estado
    posterior pode ser inferido automaticamente a partir de um estado
    anterior"]."""

    def __init__(self, origem, destino, arquivo_origem: str = ARQUIVO_MATRIZ_TRANSICOES, detalhe: str = ""):
        self.origem = origem
        self.destino = destino
        self.arquivo_origem = arquivo_origem
        self.detalhe = detalhe
        msg = f"transição {origem!s} -> {destino!s} não está listada na matriz (fonte: {arquivo_origem})"
        if detalhe:
            msg += f" — {detalhe}"
        super().__init__(msg)


class ErroDeSaidaDeAbstencao(Exception):
    """SAIDA_DA_ABSTENCAO incompleta — fonte:
    07_PROTOCOLO_DE_RECOMENDACAO_E_ABSTENCAO_BIBLIOGRAFICA_P04_R01.txt:
    "Declarar o que não pode ser comprovado, registrar a evidência
    ausente e indicar uma única ação documental necessária." Os três
    campos são obrigatórios; nenhum tem valor padrão."""

    ARQUIVO_ORIGEM = "07_PROTOCOLO_DE_RECOMENDACAO_E_ABSTENCAO_BIBLIOGRAFICA_P04_R01.txt"

    def __init__(self, detalhe: str):
        self.detalhe = detalhe
        super().__init__(f"{detalhe} (fonte: {self.ARQUIVO_ORIGEM})")

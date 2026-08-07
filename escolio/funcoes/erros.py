"""Exceções do roteador de função.

Mesma disciplina de escolio/contrato/erros.py: toda rejeição cita a regra
violada e o arquivo de origem. Não subclasse de ErroDeContrato — o
roteamento viola regras do P09 §4.2/§8.1 mas também do P02 (catálogo
fechado), e um único `arquivo_origem` variável cobre os dois casos sem
fundir as duas famílias de regra.
"""

ARQUIVO_P09 = "P09_SCHEMAS_CONTRATOS_CORRIGIDO_R04.md"
ARQUIVO_P02 = "02_CATALOGO_FUNCIONAL_CONSOLIDADO_P02_R01.md"


class ErroDeRoteamento(Exception):
    """Violação de uma regra de correspondência entre função, componente e
    operação (P09 §4.2.4-4.2.7, §8.1) ou de pertencimento ao catálogo
    fechado das seis unidades funcionais (P02 §1, §7; LAC-P02-005).

    Regra bloqueante levanta exceção — não sinaliza e prossegue."""

    def __init__(self, regra_id: str, fundamento: str, arquivo_origem: str = ARQUIVO_P09, detalhe: str = ""):
        self.regra_id = regra_id
        self.fundamento = fundamento
        self.arquivo_origem = arquivo_origem
        self.detalhe = detalhe
        msg = f"[{regra_id}] {fundamento} (fonte: {arquivo_origem})"
        if detalhe:
            msg += f" — {detalhe}"
        super().__init__(msg)


class ErroDeDeclaracao(Exception):
    """Declaração de função malformada: campo obrigatório da R03 CAMADA B
    ausente, ou ordem de etapas descontínua.

    É erro de construção do próprio módulo de função (defeito nosso), não
    de uma requisição recebida — por isso não é ErroDeRoteamento."""

    ARQUIVO_ORIGEM = "01_PROTOCOLO_MESTRE_DE_ACAO_ECOSSISTEMA_LLM_ACADEMICA_R03.md"

    def __init__(self, fundamento: str, detalhe: str = ""):
        self.fundamento = fundamento
        self.detalhe = detalhe
        msg = f"[R03-CAMADA-B] {fundamento} (fonte: {self.ARQUIVO_ORIGEM})"
        if detalhe:
            msg += f" — {detalhe}"
        super().__init__(msg)

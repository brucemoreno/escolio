"""Facade da máquina de estados bibliográficos: aplica uma transição
listada (escolio.bvaa.transicoes) ou, quando o gatilho é de invenção
(escolio.bvaa.abstencao.GatilhoDeAbstencao.COMANDO_EXIGE_INVENCAO ou
qualquer outro gatilho da mesma enumeração), força T18 a partir de
QUALQUER_ESTADO.

Este módulo não decide *se* houve invenção ou divergência — isso é
avaliação sobre a evidência concreta, responsabilidade de quem chama
(mesma separação de responsabilidade adotada em
escolio.intervencao.gate: "este módulo não decide a causa do bloqueio").
"""

from dataclasses import dataclass

from escolio.bvaa.abstencao import GatilhoDeAbstencao, SaidaDeAbstencao
from escolio.bvaa.erros import ErroDeSaidaDeAbstencao
from escolio.bvaa.transicoes import aplicar_transicao, transicao_por_invencao
from escolio.bvaa.vocabulario import EstadoBibliografico


@dataclass(frozen=True)
class ResultadoDeTransicao:
    estado_anterior: EstadoBibliografico
    estado_novo: EstadoBibliografico
    transicao_id: str


def avancar(estado_atual: EstadoBibliografico, transicao_id: str) -> ResultadoDeTransicao:
    """Aplica uma transição listada (T01..T18) a partir de `estado_atual`.

    Lança ErroDeTransicaoBibliografica se a transição não existir ou seu
    estado_entrada não corresponder a `estado_atual` — ver
    escolio.bvaa.transicoes.aplicar_transicao. Nenhuma transição é
    aceita por proximidade ou plausibilidade.
    """
    novo_estado = aplicar_transicao(estado_atual, transicao_id)
    return ResultadoDeTransicao(estado_atual, novo_estado, transicao_id)


def abster(
    estado_atual: EstadoBibliografico,
    gatilho: GatilhoDeAbstencao,
    o_que_nao_pode_ser_comprovado: str,
    evidencia_ausente: str,
    acao_documental_necessaria: str,
) -> tuple[ResultadoDeTransicao, SaidaDeAbstencao]:
    """Aplica T18 a partir de QUALQUER_ESTADO — a abstenção bibliográfica
    é obrigatória para qualquer um dos gatilhos de
    escolio.bvaa.abstencao.GatilhoDeAbstencao, e nenhum deles depende do
    estado atual da obra [04_MATRIZ_..._P04_R01.csv, T18: origem
    QUALQUER_ESTADO].

    Retorna a transição aplicada e a saída de abstenção
    ["07_PROTOCOLO_DE_RECOMENDACAO_E_ABSTENCAO_BIBLIOGRAFICA_P04_R01.txt",
    "SAIDA_DA_ABSTENCAO": declarar o que não pode ser comprovado,
    registrar a evidência ausente, indicar uma única ação documental
    necessária] — os três argumentos de texto são obrigatórios, não há
    valor padrão: uma abstenção sem essas três informações não cumpre o
    protocolo.
    """
    if not o_que_nao_pode_ser_comprovado or not evidencia_ausente or not acao_documental_necessaria:
        raise ErroDeSaidaDeAbstencao(
            "SAIDA_DA_ABSTENCAO exige os três campos preenchidos: "
            "o que não pode ser comprovado, evidência ausente, ação documental necessária"
        )
    transicao = transicao_por_invencao()
    resultado = ResultadoDeTransicao(estado_atual, transicao.estado_saida, transicao.transicao_id)
    saida = SaidaDeAbstencao(
        o_que_nao_pode_ser_comprovado=o_que_nao_pode_ser_comprovado,
        evidencia_ausente=evidencia_ausente,
        acao_documental_necessaria=acao_documental_necessaria,
        gatilho=gatilho,
    )
    return resultado, saida

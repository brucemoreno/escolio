"""Matriz de suficiência e confiança — fonte:
05_MATRIZ_DE_SUFICIENCIA_E_CONFIANCA_P05_R01.csv.

Implementada literalmente como está: 24 combinações (6 suficiências x 4
confianças), cada uma com combinacao_permitida, estado_de_validacao_maximo,
uso_maximo e regra. Dimensões não colapsáveis (arquivo 01, princípio 4):
confiança alta não compensa evidência insuficiente.
"""

from dataclasses import dataclass

from escolio.vocabulario import Confidence, Sufficiency


@dataclass(frozen=True)
class EntradaMatriz:
    suficiencia: Sufficiency
    confianca: Confidence
    combinacao_permitida: bool
    estado_de_validacao_maximo: str
    uso_maximo: str
    regra: str


_MATRIZ_RAW = [
    (Sufficiency.NAO_AVALIADA, Confidence.NAO_AVALIADA, True, "NAO_VERIFICADA", "NAO_USAR", "Avaliação incompleta"),
    (Sufficiency.NAO_AVALIADA, Confidence.BAIXA, True, "NAO_VERIFICADA", "NAO_USAR", "Avaliação incompleta"),
    (Sufficiency.NAO_AVALIADA, Confidence.MEDIA, False, "NAO_VERIFICADA", "NAO_USAR", "Avaliação incompleta"),
    (Sufficiency.NAO_AVALIADA, Confidence.ALTA, False, "NAO_VERIFICADA", "NAO_USAR", "Avaliação incompleta"),
    (Sufficiency.EVIDENCIA_AUSENTE, Confidence.NAO_AVALIADA, True, "NAO_VERIFICADA", "ABSTENCAO", "Confiança média/alta sem evidência é incoerente"),
    (Sufficiency.EVIDENCIA_AUSENTE, Confidence.BAIXA, True, "NAO_VERIFICADA", "ABSTENCAO", "Confiança média/alta sem evidência é incoerente"),
    (Sufficiency.EVIDENCIA_AUSENTE, Confidence.MEDIA, False, "NAO_VERIFICADA", "ABSTENCAO", "Confiança média/alta sem evidência é incoerente"),
    (Sufficiency.EVIDENCIA_AUSENTE, Confidence.ALTA, False, "NAO_VERIFICADA", "ABSTENCAO", "Confiança média/alta sem evidência é incoerente"),
    (Sufficiency.EVIDENCIA_INSUFICIENTE, Confidence.NAO_AVALIADA, True, "VALIDACAO_PENDENTE", "USO_CONDICIONAL ou NAO_USAR", "Alta confiança não compensa insuficiência"),
    (Sufficiency.EVIDENCIA_INSUFICIENTE, Confidence.BAIXA, True, "VALIDACAO_PENDENTE", "USO_CONDICIONAL ou NAO_USAR", "Alta confiança não compensa insuficiência"),
    (Sufficiency.EVIDENCIA_INSUFICIENTE, Confidence.MEDIA, True, "VALIDACAO_PENDENTE", "USO_CONDICIONAL ou NAO_USAR", "Alta confiança não compensa insuficiência"),
    (Sufficiency.EVIDENCIA_INSUFICIENTE, Confidence.ALTA, False, "VALIDACAO_PENDENTE", "USO_CONDICIONAL ou NAO_USAR", "Alta confiança não compensa insuficiência"),
    (Sufficiency.EVIDENCIA_PARCIALMENTE_SUFICIENTE, Confidence.NAO_AVALIADA, True, "VALIDACAO_PENDENTE ou VALIDADA_DELIMITADA", "USO_CONDICIONAL", "Somente no segmento coberto"),
    (Sufficiency.EVIDENCIA_PARCIALMENTE_SUFICIENTE, Confidence.BAIXA, True, "VALIDACAO_PENDENTE ou VALIDADA_DELIMITADA", "USO_CONDICIONAL", "Somente no segmento coberto"),
    (Sufficiency.EVIDENCIA_PARCIALMENTE_SUFICIENTE, Confidence.MEDIA, True, "VALIDACAO_PENDENTE ou VALIDADA_DELIMITADA", "USO_CONDICIONAL", "Somente no segmento coberto"),
    (Sufficiency.EVIDENCIA_PARCIALMENTE_SUFICIENTE, Confidence.ALTA, True, "VALIDACAO_PENDENTE ou VALIDADA_DELIMITADA", "USO_CONDICIONAL", "Somente no segmento coberto"),
    (Sufficiency.EVIDENCIA_SUFICIENTE, Confidence.NAO_AVALIADA, True, "VALIDADA quando demais gates atendidos", "USO_LIBERADO quando demais gates atendidos", "Suficiência não implica automaticamente alta confiança"),
    (Sufficiency.EVIDENCIA_SUFICIENTE, Confidence.BAIXA, True, "VALIDADA quando demais gates atendidos", "USO_LIBERADO quando demais gates atendidos", "Suficiência não implica automaticamente alta confiança"),
    (Sufficiency.EVIDENCIA_SUFICIENTE, Confidence.MEDIA, True, "VALIDADA quando demais gates atendidos", "USO_LIBERADO quando demais gates atendidos", "Suficiência não implica automaticamente alta confiança"),
    (Sufficiency.EVIDENCIA_SUFICIENTE, Confidence.ALTA, True, "VALIDADA quando demais gates atendidos", "USO_LIBERADO quando demais gates atendidos", "Suficiência não implica automaticamente alta confiança"),
    (Sufficiency.CONFLITANTE, Confidence.NAO_AVALIADA, True, "VALIDACAO_PENDENTE", "NAO_USAR ou USO_CONDICIONAL", "Conflito impede liberação irrestrita"),
    (Sufficiency.CONFLITANTE, Confidence.BAIXA, True, "VALIDACAO_PENDENTE", "NAO_USAR ou USO_CONDICIONAL", "Conflito impede liberação irrestrita"),
    (Sufficiency.CONFLITANTE, Confidence.MEDIA, True, "VALIDACAO_PENDENTE", "NAO_USAR ou USO_CONDICIONAL", "Conflito impede liberação irrestrita"),
    (Sufficiency.CONFLITANTE, Confidence.ALTA, False, "VALIDACAO_PENDENTE", "NAO_USAR ou USO_CONDICIONAL", "Conflito impede liberação irrestrita"),
]

MATRIZ: dict[tuple[Sufficiency, Confidence], EntradaMatriz] = {
    (linha[0], linha[1]): EntradaMatriz(*linha) for linha in _MATRIZ_RAW
}


def consultar(suficiencia: Sufficiency, confianca: Confidence) -> EntradaMatriz:
    return MATRIZ[(suficiencia, confianca)]

"""Matriz de criticidade — fonte: P13 §11.

Os 12 eixos e as cinco classes são literais do contrato. A classe **não é
derivada** dos eixos por nenhuma função deste módulo: "a matriz não pode ser
reduzida a contagem mecânica" [§11] e transformar criticidade em quota é
ação proibida [§34.4] / invariante `PC30_SIGNIFICA_CRITICIDADE_E_NAO_QUOTA`
[§3.9]. `classe` é campo declarado por quem avalia (humano ou, em sessão
futura, LLM sob gate) — este módulo só valida forma, nunca calcula o valor.
Ausência de função `classificar_automaticamente` é decisão de design desta
sessão, não lacuna.
"""

from dataclasses import dataclass
from enum import Enum

from escolio.comentarios.erros import ErroDeComentario

ARQUIVO_FONTE = "P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md"


class EixoCriticidade(str, Enum):
    """Os 12 eixos de avaliação do problema candidato [§11]."""

    FACTUAL = "FACTUAL"
    EVIDENCIA = "EVIDENCIA"
    BIBLIOGRAFICO = "BIBLIOGRAFICO"
    METODOLOGICO = "METODOLOGICO"
    ARGUMENTATIVO = "ARGUMENTATIVO"
    ESTRUTURAL = "ESTRUTURAL"
    VOZ = "VOZ"
    PRIVACIDADE = "PRIVACIDADE"
    AVALIATIVO = "AVALIATIVO"
    SISTEMICO = "SISTEMICO"
    CENTRALIDADE = "CENTRALIDADE"
    REVERSIBILIDADE = "REVERSIBILIDADE"


class ClasseCriticidade(str, Enum):
    """As cinco classes de criticidade [§11]."""

    CRITICIDADE_CRITICA = "CRITICIDADE_CRITICA"
    CRITICIDADE_ALTA = "CRITICIDADE_ALTA"
    CRITICIDADE_MEDIA = "CRITICIDADE_MEDIA"
    CRITICIDADE_BAIXA = "CRITICIDADE_BAIXA"
    SEM_CRITICIDADE_MATERIAL = "SEM_CRITICIDADE_MATERIAL"


@dataclass
class MatrizCriticidade:
    """Avaliação de um problema candidato nos 12 eixos do §11.

    `avaliacao_por_eixo` exige exatamente os 12 membros de `EixoCriticidade`
    — nem a mais, nem a menos — cada um com justificativa não vazia.
    `classe` é a classe declarada; `justificativa_classe` é a narrativa que
    a sustenta, exigida justamente porque a classe não pode resultar de
    contagem dos eixos [§11].
    """

    problem_id: str
    unit_id: str
    avaliacao_por_eixo: dict[EixoCriticidade, str]
    classe: ClasseCriticidade
    justificativa_classe: str

    def __post_init__(self) -> None:
        self._valida_eixos()
        self._valida_classe()
        self._valida_justificativa()

    def _valida_eixos(self) -> None:
        chaves = set(self.avaliacao_por_eixo)
        esperadas = set(EixoCriticidade)
        faltantes = esperadas - chaves
        extras = chaves - esperadas
        if faltantes:
            raise ErroDeComentario(
                "11",
                "MatrizCriticidade exige avaliação nos 12 eixos do §11",
                detalhe=f"faltando: {sorted(e.value for e in faltantes)}",
            )
        if extras:
            raise ErroDeComentario(
                "11",
                "avaliacao_por_eixo contém chave que não é um dos 12 eixos do §11",
                detalhe=f"chaves não reconhecidas: {extras}",
            )
        for eixo, resposta in self.avaliacao_por_eixo.items():
            if resposta is None or resposta.strip() == "":
                raise ErroDeComentario(
                    "11",
                    f"avaliação do eixo {eixo.value} vazia",
                )

    def _valida_classe(self) -> None:
        if not isinstance(self.classe, ClasseCriticidade):
            raise ErroDeComentario(
                "11",
                "classe deve ser um membro de ClasseCriticidade",
                detalhe=repr(self.classe),
            )

    def _valida_justificativa(self) -> None:
        if self.justificativa_classe is None or self.justificativa_classe.strip() == "":
            raise ErroDeComentario(
                "11",
                "justificativa_classe vazia — a classe não pode ser reduzida a contagem mecânica dos eixos [§11]",
            )

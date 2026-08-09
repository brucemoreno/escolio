"""Comentário-matriz e remissões — fonte: P13 §23 (COMENTÁRIO-MATRIZ E
REMISSÕES), §24 (CONSOLIDAÇÃO DE REPETIÇÕES), §45 (PS13-04), §46
(TA13-14, TA13-15). Sessão 6 de `docs/spec/plano-P13.md`.

Reusa `P13Comment`/`RegistroDeComentarios` (sessão 1), `CommentType`
(sessão 3) e `NivelIntervencao` (P06, já reusado pela sessão 5) sem
duplicar. Nenhum código existente foi alterado — este módulo só adiciona
estruturas e funções novas, mesma disciplina de `aplicacao_p04_p05.py` e
`aplicacao_p06_p07.py`.

Este módulo não decide por si só quando um problema é sistêmico ou quando
uma evidência é distinta de outra — os critérios de §24
(`CriterioConsolidacao`) são fatos já declarados por quem avalia (humano ou
etapa anterior do pipeline); `decidir_consolidacao` só aplica a regra
determinística de §24 sobre esses fatos, mesma disciplina de
`MatrizCriticidade.classe` (sessão 2, campo declarado, nunca derivado por
contagem).
"""

from dataclasses import dataclass
from enum import Enum

from escolio.comentarios.comentario import P13Comment
from escolio.comentarios.erros import ErroDeComentario
from escolio.comentarios.registro import RegistroDeComentarios
from escolio.comentarios.tipos import CommentType
from escolio.intervencao.niveis import NivelIntervencao

ARQUIVO_FONTE = "P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md"


def _exige_nao_vazio(regra_id: str, nome_campo: str, valor) -> None:
    if valor is None or (isinstance(valor, str) and valor.strip() == ""):
        raise ErroDeComentario(
            regra_id,
            f"Campo obrigatório '{nome_campo}' vazio ({regra_id})",
            ARQUIVO_FONTE,
        )


def _exige_lista_nao_vazia(regra_id: str, nome_campo: str, valor) -> None:
    if not valor:
        raise ErroDeComentario(
            regra_id,
            f"Campo obrigatório '{nome_campo}' vazio ou ausente ({regra_id})",
            ARQUIVO_FONTE,
        )


# --- §23 — Template do comentário-matriz ------------------------------

_CAMPOS_STR_MATRIZ = (
    "problema_sistemico",
    "extensao_estimada",
    "impacto_global",
    "acao_recomendada",
    "decisao_humana_necessaria",
    "evidencia",
    "limitacoes",
)


@dataclass
class TemplateComentarioMatriz:
    """Os dez itens que §23 exige que o comentário-matriz contenha:
    definição do problema sistêmico; exemplos representativos; extensão
    estimada; impacto global; ação recomendada; unidades relacionadas;
    decisão humana necessária; nível de intervenção; evidência;
    limitações.

    `decisao_humana_necessaria` permanece `str` — §23 não declara tipo
    (nem enum, nem booleano) para este item, mesma disciplina recusada
    para os nove fatores de `MatrizSeletividade` (sessão 2, ver
    LACUNAS.md). `nivel_de_intervencao` reusa `NivelIntervencao` (P06) —
    a sessão 5 já estabeleceu esse reuso para o mesmo nome de campo em
    `P13Comment.intervention_level`.
    """

    problema_sistemico: str
    exemplos_representativos: list[str]
    extensao_estimada: str
    impacto_global: str
    acao_recomendada: str
    unidades_relacionadas: list[str]
    decisao_humana_necessaria: str
    nivel_de_intervencao: NivelIntervencao
    evidencia: str
    limitacoes: str

    def __post_init__(self) -> None:
        for campo in _CAMPOS_STR_MATRIZ:
            _exige_nao_vazio("23", campo, getattr(self, campo))
        _exige_lista_nao_vazia("23", "exemplos_representativos", self.exemplos_representativos)
        _exige_lista_nao_vazia("23", "unidades_relacionadas", self.unidades_relacionadas)
        if not isinstance(self.nivel_de_intervencao, NivelIntervencao):
            raise ErroDeComentario(
                "23",
                "nivel_de_intervencao deve ser um membro de NivelIntervencao",
                ARQUIVO_FONTE,
                repr(self.nivel_de_intervencao),
            )


# --- §23 — Template da remissão ---------------------------------------


@dataclass
class TemplateRemissao:
    """Os três itens que a remissão deve identificar [§23]:
    comentário-matriz; unidade relacionada; aspecto específico da
    ocorrência.

    "Não deve haver remissão vazia ou incompreensível" [§23] — a metade
    verificável em código é "vazia" (obrigatoriedade dos três campos);
    "incompreensível" não tem critério objetivo na fonte e não é
    verificado aqui — mesma disciplina de itens sem critério objetivo já
    registrados em `escolio/comentarios/LACUNAS.md` (ex.: §18 na sessão
    3).
    """

    matrix_comment_id: str
    unit_id: str
    aspecto_especifico: str

    def __post_init__(self) -> None:
        for campo in ("matrix_comment_id", "unit_id", "aspecto_especifico"):
            _exige_nao_vazio("23", campo, getattr(self, campo))


# --- §24 — Consolidação de repetições ----------------------------------


@dataclass(frozen=True)
class CriterioConsolidacao:
    """Os dez fatos de §24 que decidem se uma repetição deve ser
    consolidada. Cada campo é um fato já declarado por quem avalia — este
    módulo não infere nenhum deles a partir de texto ou dado bruto, só
    aplica a regra determinística de `decidir_consolidacao` sobre os
    fatos recebidos."""

    # "A repetição deve ser consolidada quando" [§24, itens 1-5]
    mesma_causa: bool
    acao_recomendada_semelhante: bool
    repeticao_individual_nao_adiciona_decisao: bool
    risco_de_poluicao: bool
    rastreabilidade_preservavel: bool
    # "Não deve ser consolidada quando" [§24]
    impacto_varia_materialmente: bool
    evidencia_distinta: bool
    solucao_exige_decisoes_diferentes: bool
    ocorrencia_critica_autonoma: bool
    risco_de_ocultar_problema_especifico: bool


class DecisaoConsolidacao(str, Enum):
    """Resultado de `decidir_consolidacao` [§24]. Vocabulário interno
    deste módulo, não um dos oito valores de `SelectionDecision` (§10,
    sessão 2) — decide se consolida uma repetição já identificada, não se
    comenta uma unidade."""

    CONSOLIDAR = "CONSOLIDAR"
    NAO_CONSOLIDAR = "NAO_CONSOLIDAR"


def decidir_consolidacao(criterio: CriterioConsolidacao) -> DecisaoConsolidacao:
    """§24 — leitura mais literal possível dos dois blocos da fonte:

    * as cinco condições de "deve ser consolidada quando" são lidas como
      conjunção — a lista enumera os requisitos da consolidação, não
      alternativas isoladas (uma única condição, ex. "há risco de
      poluição", sem "a causa é a mesma", não justificaria consolidar
      causas distintas);
    * as cinco condições de "não deve ser consolidada quando" são lidas
      como vetos independentes — basta uma presente para recusar, mesmo
      com as cinco condições afirmativas satisfeitas, porque cada uma
      descreve por si só um risco de ocultar problema específico
      (mesma leitura de veto único já aplicada a
      `valida_correcao_local_nao_autoriza_reescrita_forte`, sessão 5).

    Não decide nada além do que os dois blocos declaram: ausência de
    todas as condições afirmativas também resulta em não consolidar, sem
    precisar de veto explícito.
    """
    vetos = (
        criterio.impacto_varia_materialmente,
        criterio.evidencia_distinta,
        criterio.solucao_exige_decisoes_diferentes,
        criterio.ocorrencia_critica_autonoma,
        criterio.risco_de_ocultar_problema_especifico,
    )
    if any(vetos):
        return DecisaoConsolidacao.NAO_CONSOLIDAR

    condicoes = (
        criterio.mesma_causa,
        criterio.acao_recomendada_semelhante,
        criterio.repeticao_individual_nao_adiciona_decisao,
        criterio.risco_de_poluicao,
        criterio.rastreabilidade_preservavel,
    )
    if all(condicoes):
        return DecisaoConsolidacao.CONSOLIDAR
    return DecisaoConsolidacao.NAO_CONSOLIDAR


# --- Registro conjunto de matriz e remissões ---------------------------


def registrar_comentario_matriz_e_remissoes(
    registro: RegistroDeComentarios,
    comentario_matriz: P13Comment,
    template_matriz: TemplateComentarioMatriz,
    ocorrencias: list[tuple[P13Comment, TemplateRemissao, CriterioConsolidacao]],
) -> list[P13Comment]:
    """§23/§24, PS13-04, TA13-14, TA13-15 — registra o comentário-matriz e,
    para cada ocorrência cuja consolidação `decidir_consolidacao` aprova,
    a remissão correspondente. Nenhuma gravação ocorre se qualquer
    validação falhar antes dela, mesmo padrão de `aplicar_intervencao_e_voz`
    (sessão 5).

    Ocorrência cuja consolidação `decidir_consolidacao` recusa não é
    registrada aqui: produzir comentário individual para ela é decisão de
    quem chama, fora do escopo deste módulo — este módulo só consolida, a
    ausência de consolidação não é resolvida silenciosamente em outra
    coisa.
    """
    if comentario_matriz.comment_type != CommentType.COMENTARIO_MATRIZ.value:
        raise ErroDeComentario(
            "23",
            "comentario_matriz deve ter comment_type=COMENTARIO_MATRIZ",
            ARQUIVO_FONTE,
            detalhe=comentario_matriz.comment_type,
        )

    unidades_no_template = set(template_matriz.unidades_relacionadas)
    for comentario_remissao, template_remissao, criterio in ocorrencias:
        if comentario_remissao.comment_type != CommentType.REMISSAO_A_COMENTARIO_MATRIZ.value:
            raise ErroDeComentario(
                "23",
                "ocorrência consolidada deve ter comment_type=REMISSAO_A_COMENTARIO_MATRIZ",
                ARQUIVO_FONTE,
                detalhe=comentario_remissao.comment_type,
            )
        if comentario_remissao.matrix_comment_id != comentario_matriz.comment_id:
            raise ErroDeComentario(
                "23",
                "matrix_comment_id da remissão deve apontar para o comentário-matriz sendo registrado",
                ARQUIVO_FONTE,
                detalhe=(
                    f"remissao.matrix_comment_id={comentario_remissao.matrix_comment_id!r} "
                    f"comentario_matriz.comment_id={comentario_matriz.comment_id!r}"
                ),
            )
        if template_remissao.matrix_comment_id != comentario_matriz.comment_id:
            raise ErroDeComentario(
                "23",
                "TemplateRemissao.matrix_comment_id deve apontar para o comentário-matriz sendo registrado",
                ARQUIVO_FONTE,
                detalhe=template_remissao.matrix_comment_id,
            )
        if template_remissao.unit_id not in unidades_no_template:
            raise ErroDeComentario(
                "23",
                "unidade da remissão não está entre unidades_relacionadas do comentário-matriz — rastreabilidade quebrada",
                ARQUIVO_FONTE,
                detalhe=template_remissao.unit_id,
            )
        if decidir_consolidacao(criterio) != DecisaoConsolidacao.CONSOLIDAR:
            raise ErroDeComentario(
                "24",
                "ocorrência não satisfaz os critérios de consolidação de §24 — não deve receber remissão",
                ARQUIVO_FONTE,
                detalhe=repr(criterio),
            )

    registro.registrar(comentario_matriz)
    remissoes_registradas: list[P13Comment] = []
    for comentario_remissao, _template_remissao, _criterio in ocorrencias:
        registro.registrar(comentario_remissao)
        remissoes_registradas.append(comentario_remissao)
    return remissoes_registradas

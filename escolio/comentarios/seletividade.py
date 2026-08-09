"""Matriz de seletividade — fonte: P13 §12, §45 (PS13-01).

Campos mínimos do §12: dez fatores combinados (criticidade, novidade,
recorrência, necessidade de decisão, possibilidade de ação, suficiência de
evidência, impacto, proporcionalidade, risco de poluição, cobertura por
comentário-matriz) e treze campos de schema. `criticality` reusa
`ClasseCriticidade` (§11) — não duplica enum. Os demais fatores não têm
tipo declarado na fonte (nem enum, nem booleano); permanecem `str`, mesma
disciplina de `escolio/comentarios/comentario.py` para campos cuja tipagem
própria pertence a outra sessão — ver LACUNAS.md.

Este módulo não decide sozinho o que comentar: só valida forma e aplica,
deterministicamente, a ordenação por criticidade e a rejeição de quota
[§34.3, §34.4; invariantes 8-9, §3.9].
"""

from dataclasses import dataclass
from enum import Enum

from escolio.comentarios.criticidade import ClasseCriticidade, MatrizCriticidade
from escolio.comentarios.erros import ErroDeComentario

ARQUIVO_FONTE = "P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md"


class SelectionDecision(str, Enum):
    """Os oito resultados da etapa 10 — seleção de unidades comentáveis
    [§10]. Internos ao P13, não substituem status P09 [§10]."""

    COMENTAR = "COMENTAR"
    NAO_COMENTAR_SEM_PROBLEMA_MATERIAL = "NAO_COMENTAR_SEM_PROBLEMA_MATERIAL"
    NAO_COMENTAR_POR_REPETICAO = "NAO_COMENTAR_POR_REPETICAO"
    REMETER_A_COMENTARIO_MATRIZ = "REMETER_A_COMENTARIO_MATRIZ"
    AGUARDAR_EVIDENCIA = "AGUARDAR_EVIDENCIA"
    AGUARDAR_GATE = "AGUARDAR_GATE"
    ABSTER_SE = "ABSTER_SE"
    BLOQUEADO = "BLOQUEADO"


# §45, PS13-01 — literal da coluna "Decisão" do cenário de ausência
# legítima de comentário.
SELECTION_DECISION_NAO_COMENTAR_SEM_PROBLEMA_MATERIAL = (
    SelectionDecision.NAO_COMENTAR_SEM_PROBLEMA_MATERIAL
)

_CAMPOS_STR_OBRIGATORIOS = (
    "selection_id",
    "unit_id",
    "candidate_problem_id",
    "material_impact",
    "novelty",
    "recurrence",
    "matrix_comment_coverage",
    "actionability",
    "evidence_sufficiency",
    "human_decision_required",
    "privacy_risk",
    "selection_rationale",
)


@dataclass
class MatrizSeletividade:
    """Schema mínimo de seletividade [§12]."""

    selection_id: str
    unit_id: str
    candidate_problem_id: str
    criticality: ClasseCriticidade
    material_impact: str
    novelty: str
    recurrence: str
    matrix_comment_coverage: str
    actionability: str
    evidence_sufficiency: str
    human_decision_required: str
    privacy_risk: str
    selection_decision: SelectionDecision
    selection_rationale: str

    def __post_init__(self) -> None:
        for campo in _CAMPOS_STR_OBRIGATORIOS:
            valor = getattr(self, campo)
            if valor is None or (isinstance(valor, str) and valor.strip() == ""):
                raise ErroDeComentario(
                    "12",
                    f"Campo obrigatório '{campo}' vazio na matriz de seletividade (§12)",
                )
        if not isinstance(self.criticality, ClasseCriticidade):
            raise ErroDeComentario(
                "12",
                "criticality deve ser um membro de ClasseCriticidade",
                detalhe=repr(self.criticality),
            )
        if not isinstance(self.selection_decision, SelectionDecision):
            raise ErroDeComentario(
                "10",
                "selection_decision deve ser um membro de SelectionDecision — oito "
                "resultados da etapa 10 [§10], não string livre",
                detalhe=repr(self.selection_decision),
            )


_ORDEM_CRITICIDADE = {
    ClasseCriticidade.CRITICIDADE_CRITICA: 0,
    ClasseCriticidade.CRITICIDADE_ALTA: 1,
    ClasseCriticidade.CRITICIDADE_MEDIA: 2,
    ClasseCriticidade.CRITICIDADE_BAIXA: 3,
    ClasseCriticidade.SEM_CRITICIDADE_MATERIAL: 4,
}


def ordenar_por_criticidade(candidatos: list[MatrizSeletividade]) -> list[MatrizSeletividade]:
    """Ordena por `criticality`, nunca pela posição do candidato na lista de
    entrada — invariante 4, `PRIORIDADE_DERIVA_DO_IMPACTO_E_NAO_DA_ORDEM_TEXTUAL`
    [§3]. `sorted` é estável: candidatos de mesma classe preservam a ordem
    de entrada entre si, mas a ordem de entrada nunca decide entre classes
    diferentes."""
    return sorted(candidatos, key=lambda c: _ORDEM_CRITICIDADE[c.criticality])


def exige_referencia_valida_a_criticidade(
    candidatos: list[MatrizSeletividade],
    matrizes_criticidade: list[MatrizCriticidade],
) -> None:
    """BL-024: `candidate_problem_id` deve apontar para uma `MatrizCriticidade`
    de fato existente [§11, §12], e `criticality` deve bater com a `classe`
    que essa matriz declarou. Sem isto, duas matrizes podiam divergir
    (`classe` diferente do `criticality` copiado à mão) sem erro."""
    por_problem_id = {m.problem_id: m for m in matrizes_criticidade}
    for c in candidatos:
        matriz = por_problem_id.get(c.candidate_problem_id)
        if matriz is None:
            raise ErroDeComentario(
                "11-12",
                "candidate_problem_id não referencia nenhuma MatrizCriticidade existente",
                detalhe=f"selection_id={c.selection_id!r} candidate_problem_id={c.candidate_problem_id!r}",
            )
        if c.criticality != matriz.classe:
            raise ErroDeComentario(
                "11-12",
                "criticality diverge da classe declarada pela MatrizCriticidade referenciada",
                detalhe=(
                    f"selection_id={c.selection_id!r} criticality={c.criticality!r} "
                    f"!= MatrizCriticidade[{matriz.problem_id!r}].classe={matriz.classe!r}"
                ),
            )


def aplicar_selecao(
    candidatos: list[MatrizSeletividade],
    *,
    quota_percentual: float | None = None,
    quota_quantidade: int | None = None,
) -> list[MatrizSeletividade]:
    """Aplica seleção por criticidade. Rejeita qualquer quota — fixar quota
    percentual [§34.3] e transformar criticidade em quota [§34.4] são ações
    proibidas; `QUANTIDADE_NAO_DEVE_SER_FIXADA_POR_PERCENTUAL_MECANICO` e
    `PC30_SIGNIFICA_CRITICIDADE_E_NAO_QUOTA` são invariantes [§3]."""
    if quota_percentual is not None or quota_quantidade is not None:
        raise ErroDeComentario(
            "34.3-34.4",
            "quota percentual ou quantitativa é ação proibida — a seleção segue criticidade, não quota",
            detalhe=f"quota_percentual={quota_percentual!r} quota_quantidade={quota_quantidade!r}",
        )
    return ordenar_por_criticidade(candidatos)

import pytest

from escolio.comentarios.criticidade import ClasseCriticidade
from escolio.comentarios.erros import ErroDeComentario
from escolio.comentarios.seletividade import (
    SELECTION_DECISION_NAO_COMENTAR_SEM_PROBLEMA_MATERIAL,
    aplicar_selecao,
    ordenar_por_criticidade,
)
from tests.comentarios.fixtures import matriz_seletividade_base


def test_seletividade_minima_valida():
    s = matriz_seletividade_base()
    assert s.criticality == ClasseCriticidade.CRITICIDADE_MEDIA


@pytest.mark.parametrize(
    "campo",
    [
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
        "selection_decision",
        "selection_rationale",
    ],
)
def test_campo_obrigatorio_vazio_rejeita(campo):
    with pytest.raises(ErroDeComentario):
        matriz_seletividade_base(**{campo: ""})


def test_criticality_fora_do_enum_rejeita():
    with pytest.raises(ErroDeComentario):
        matriz_seletividade_base(criticality="CRITICIDADE_MEDIA")  # string crua


class TestPS13_01_AusenciaLegitima:
    """PS13-01 [§45] — parágrafo adequado: zero comentário é `SUCCESS`, não
    abstenção nem erro [P09 §8.2; CLAUDE.md §3]."""

    def test_decisao_nao_comentar_e_construida_sem_erro(self):
        s = matriz_seletividade_base(
            criticality=ClasseCriticidade.SEM_CRITICIDADE_MATERIAL,
            selection_decision=SELECTION_DECISION_NAO_COMENTAR_SEM_PROBLEMA_MATERIAL,
            selection_rationale="Nenhum problema material identificado na unidade.",
        )
        assert s.selection_decision == SELECTION_DECISION_NAO_COMENTAR_SEM_PROBLEMA_MATERIAL

    def test_ausencia_de_criticidade_nao_forca_selecao(self):
        candidatos = [
            matriz_seletividade_base(
                selection_id="SEL-0001",
                criticality=ClasseCriticidade.SEM_CRITICIDADE_MATERIAL,
                selection_decision=SELECTION_DECISION_NAO_COMENTAR_SEM_PROBLEMA_MATERIAL,
            )
        ]
        resultado = aplicar_selecao(candidatos)
        assert resultado[0].selection_decision == SELECTION_DECISION_NAO_COMENTAR_SEM_PROBLEMA_MATERIAL


class TestTA13_05_Criticidade:
    """TA13-05 [§46] — problema crítico no final e problema menor no
    início: a ordem textual não controla prioridade."""

    def test_ordem_textual_nao_controla_prioridade(self):
        problema_menor_no_inicio = matriz_seletividade_base(
            selection_id="SEL-INICIO",
            unit_id="UNIT-01",
            criticality=ClasseCriticidade.CRITICIDADE_BAIXA,
        )
        problema_critico_no_final = matriz_seletividade_base(
            selection_id="SEL-FIM",
            unit_id="UNIT-99",
            criticality=ClasseCriticidade.CRITICIDADE_CRITICA,
        )
        # Ordem de entrada é a ordem textual: menor primeiro, crítico depois.
        entrada = [problema_menor_no_inicio, problema_critico_no_final]

        resultado = ordenar_por_criticidade(entrada)

        assert resultado[0].selection_id == "SEL-FIM"
        assert resultado[1].selection_id == "SEL-INICIO"

    def test_mesma_criticidade_preserva_ordem_de_entrada(self):
        a = matriz_seletividade_base(selection_id="SEL-A", criticality=ClasseCriticidade.CRITICIDADE_ALTA)
        b = matriz_seletividade_base(selection_id="SEL-B", criticality=ClasseCriticidade.CRITICIDADE_ALTA)
        resultado = ordenar_por_criticidade([a, b])
        assert [c.selection_id for c in resultado] == ["SEL-A", "SEL-B"]


class TestTA13_16_RejeicaoDeQuota:
    """TA13-16 [§46] — pedido de 30% de cobertura: rejeitar quota e aplicar
    criticidade, nunca percentual mecânico [§34.3-34.4; invariantes 8-9]."""

    def test_quota_percentual_rejeitada(self):
        candidatos = [matriz_seletividade_base()]
        with pytest.raises(ErroDeComentario):
            aplicar_selecao(candidatos, quota_percentual=0.30)

    def test_quota_quantidade_rejeitada(self):
        candidatos = [matriz_seletividade_base()]
        with pytest.raises(ErroDeComentario):
            aplicar_selecao(candidatos, quota_quantidade=3)

    def test_sem_quota_aplica_criticidade(self):
        baixa = matriz_seletividade_base(selection_id="SEL-BAIXA", criticality=ClasseCriticidade.CRITICIDADE_BAIXA)
        critica = matriz_seletividade_base(selection_id="SEL-CRITICA", criticality=ClasseCriticidade.CRITICIDADE_CRITICA)
        resultado = aplicar_selecao([baixa, critica])
        assert resultado[0].selection_id == "SEL-CRITICA"

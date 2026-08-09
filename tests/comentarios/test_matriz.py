"""Sessão 6 do plano P13 — comentário-matriz e remissões (§23, §24).

Testes PS13-04 [§45] e TA13-14, TA13-15 [§46], mais cobertura das regras
de forma e de integridade referencial que §23/§24 exigem.
"""

import pytest

from escolio.comentarios.erros import ErroDeComentario
from escolio.comentarios.matriz import (
    CriterioConsolidacao,
    DecisaoConsolidacao,
    TemplateComentarioMatriz,
    TemplateRemissao,
    decidir_consolidacao,
    registrar_comentario_matriz_e_remissoes,
)
from escolio.comentarios.registro import RegistroDeComentarios
from escolio.comentarios.tipos import CommentType
from escolio.intervencao.niveis import NivelIntervencao
from tests.comentarios.fixtures import comentario_base

NI = NivelIntervencao


def template_matriz_base(**overrides):
    campos = dict(
        problema_sistemico="Mesmo erro de citação sem página confirmada em várias unidades.",
        exemplos_representativos=["UNIT-01", "UNIT-02", "UNIT-03"],
        extensao_estimada="Dez unidades do capítulo 3.",
        impacto_global="Risco de citação inexata repetido ao longo do capítulo.",
        acao_recomendada="Tratar o padrão global de confirmação de página.",
        unidades_relacionadas=[f"UNIT-{i:02d}" for i in range(1, 11)],
        decisao_humana_necessaria="Decisão sobre correção sistêmica.",
        nivel_de_intervencao=NI.SINALIZACAO,
        evidencia="Dez ocorrências ancoradas no texto.",
        limitacoes="Não confirma se todas as citações do capítulo foram revisadas.",
    )
    campos.update(overrides)
    return TemplateComentarioMatriz(**campos)


def template_remissao_base(**overrides):
    campos = dict(
        matrix_comment_id="CMT-MATRIZ-01",
        unit_id="UNIT-01",
        aspecto_especifico="Página não confirmada nesta unidade específica.",
    )
    campos.update(overrides)
    return TemplateRemissao(**campos)


def criterio_consolida_base(**overrides):
    campos = dict(
        mesma_causa=True,
        acao_recomendada_semelhante=True,
        repeticao_individual_nao_adiciona_decisao=True,
        risco_de_poluicao=True,
        rastreabilidade_preservavel=True,
        impacto_varia_materialmente=False,
        evidencia_distinta=False,
        solucao_exige_decisoes_diferentes=False,
        ocorrencia_critica_autonoma=False,
        risco_de_ocultar_problema_especifico=False,
    )
    campos.update(overrides)
    return CriterioConsolidacao(**campos)


class TestTemplateComentarioMatriz:
    """§23 — os dez itens exigidos; TA13-14: "definição, exemplos, impacto,
    ação e unidades presentes"."""

    def test_template_valido_nao_levanta(self):
        template_matriz_base()

    @pytest.mark.parametrize(
        "campo",
        [
            "problema_sistemico",
            "extensao_estimada",
            "impacto_global",
            "acao_recomendada",
            "decisao_humana_necessaria",
            "evidencia",
            "limitacoes",
        ],
    )
    def test_campo_str_vazio_rejeita(self, campo):
        with pytest.raises(ErroDeComentario):
            template_matriz_base(**{campo: ""})

    def test_exemplos_representativos_vazio_rejeita(self):
        with pytest.raises(ErroDeComentario):
            template_matriz_base(exemplos_representativos=[])

    def test_unidades_relacionadas_vazio_rejeita(self):
        with pytest.raises(ErroDeComentario):
            template_matriz_base(unidades_relacionadas=[])

    def test_nivel_de_intervencao_fora_do_enum_rejeita(self):
        with pytest.raises(ErroDeComentario):
            template_matriz_base(nivel_de_intervencao="INT-03")


class TestTemplateRemissao:
    """§23 — "a remissão deve identificar: comentário-matriz; unidade
    relacionada; aspecto específico da ocorrência". "Não deve haver
    remissão vazia" é a metade verificável de §23."""

    def test_template_valido_nao_levanta(self):
        template_remissao_base()

    @pytest.mark.parametrize("campo", ["matrix_comment_id", "unit_id", "aspecto_especifico"])
    def test_campo_vazio_rejeita(self, campo):
        with pytest.raises(ErroDeComentario):
            template_remissao_base(**{campo: ""})


class TestDecidirConsolidacao:
    """§24 — as cinco condições afirmativas e os cinco vetos."""

    def test_todas_condicoes_sem_veto_consolida(self):
        assert decidir_consolidacao(criterio_consolida_base()) == DecisaoConsolidacao.CONSOLIDAR

    @pytest.mark.parametrize(
        "campo",
        [
            "mesma_causa",
            "acao_recomendada_semelhante",
            "repeticao_individual_nao_adiciona_decisao",
            "risco_de_poluicao",
            "rastreabilidade_preservavel",
        ],
    )
    def test_condicao_afirmativa_ausente_nao_consolida(self, campo):
        criterio = criterio_consolida_base(**{campo: False})
        assert decidir_consolidacao(criterio) == DecisaoConsolidacao.NAO_CONSOLIDAR

    @pytest.mark.parametrize(
        "campo",
        [
            "impacto_varia_materialmente",
            "evidencia_distinta",
            "solucao_exige_decisoes_diferentes",
            "ocorrencia_critica_autonoma",
            "risco_de_ocultar_problema_especifico",
        ],
    )
    def test_qualquer_veto_isolado_impede_consolidacao_mesmo_com_todas_condicoes(self, campo):
        criterio = criterio_consolida_base(**{campo: True})
        assert decidir_consolidacao(criterio) == DecisaoConsolidacao.NAO_CONSOLIDAR

    def test_nenhuma_condicao_e_nenhum_veto_nao_consolida(self):
        criterio = criterio_consolida_base(
            mesma_causa=False,
            acao_recomendada_semelhante=False,
            repeticao_individual_nao_adiciona_decisao=False,
            risco_de_poluicao=False,
            rastreabilidade_preservavel=False,
        )
        assert decidir_consolidacao(criterio) == DecisaoConsolidacao.NAO_CONSOLIDAR


class TestPS13_04_ComentarioMatrizERemissoes:
    """[§45] Mesmo problema em dez unidades: um comentário-matriz e
    remissões necessárias, nunca dez comentários completos."""

    def _comentario_matriz(self):
        return comentario_base(
            comment_id="CMT-MATRIZ-01",
            comment_type=CommentType.COMENTARIO_MATRIZ.value,
        )

    def _remissao(self, unit_id, comment_id):
        return comentario_base(
            comment_id=comment_id,
            unit_id=unit_id,
            comment_type=CommentType.REMISSAO_A_COMENTARIO_MATRIZ.value,
            matrix_comment_id="CMT-MATRIZ-01",
        )

    def test_dez_ocorrencias_consolidam_em_matriz_e_remissoes(self):
        registro = RegistroDeComentarios()
        comentario_matriz = self._comentario_matriz()
        template_matriz = template_matriz_base()
        ocorrencias = [
            (
                self._remissao(f"UNIT-{i:02d}", f"CMT-REM-{i:02d}"),
                template_remissao_base(unit_id=f"UNIT-{i:02d}", aspecto_especifico=f"Ocorrência {i}."),
                criterio_consolida_base(),
            )
            for i in range(1, 11)
        ]

        remissoes = registrar_comentario_matriz_e_remissoes(
            registro, comentario_matriz, template_matriz, ocorrencias
        )

        assert len(remissoes) == 10
        assert registro.obter("CMT-MATRIZ-01") is comentario_matriz
        for i in range(1, 11):
            assert registro.obter(f"CMT-REM-{i:02d}").matrix_comment_id == "CMT-MATRIZ-01"


class TestTA13_15_ConsolidacaoDeRepeticao:
    """[§46] Dez ocorrências equivalentes: consolidar e remeter, nunca dez
    comentários integrais redundantes."""

    def test_repeticao_reduzida_a_matriz_e_remissoes(self):
        registro = RegistroDeComentarios()
        comentario_matriz = comentario_base(
            comment_id="CMT-MATRIZ-02", comment_type=CommentType.COMENTARIO_MATRIZ.value
        )
        template_matriz = template_matriz_base()
        ocorrencias = [
            (
                comentario_base(
                    comment_id=f"CMT-REP-{i:02d}",
                    unit_id=f"UNIT-{i:02d}",
                    comment_type=CommentType.REMISSAO_A_COMENTARIO_MATRIZ.value,
                    matrix_comment_id="CMT-MATRIZ-02",
                ),
                template_remissao_base(matrix_comment_id="CMT-MATRIZ-02", unit_id=f"UNIT-{i:02d}"),
                criterio_consolida_base(),
            )
            for i in range(1, 11)
        ]

        remissoes = registrar_comentario_matriz_e_remissoes(
            registro, comentario_matriz, template_matriz, ocorrencias
        )

        # "repetição reduzida": dez ocorrências produzem uma matriz e dez
        # remissões curtas, nunca dez comentários integrais idênticos.
        assert len(remissoes) == 10
        assert all(r.comment_type == CommentType.REMISSAO_A_COMENTARIO_MATRIZ.value for r in remissoes)

    def test_ocorrencia_que_nao_satisfaz_24_nao_e_consolidada(self):
        registro = RegistroDeComentarios()
        comentario_matriz = comentario_base(
            comment_id="CMT-MATRIZ-03", comment_type=CommentType.COMENTARIO_MATRIZ.value
        )
        template_matriz = template_matriz_base()
        ocorrencia_com_evidencia_distinta = (
            comentario_base(
                comment_id="CMT-REP-DISTINTA",
                unit_id="UNIT-01",
                comment_type=CommentType.REMISSAO_A_COMENTARIO_MATRIZ.value,
                matrix_comment_id="CMT-MATRIZ-03",
            ),
            template_remissao_base(matrix_comment_id="CMT-MATRIZ-03", unit_id="UNIT-01"),
            criterio_consolida_base(evidencia_distinta=True),
        )

        with pytest.raises(ErroDeComentario):
            registrar_comentario_matriz_e_remissoes(
                registro, comentario_matriz, template_matriz, [ocorrencia_com_evidencia_distinta]
            )
        # Nenhuma gravação parcial: nem a matriz nem a remissão entraram no registro.
        assert registro.obter("CMT-MATRIZ-03") is None
        assert registro.obter("CMT-REP-DISTINTA") is None


class TestIntegridadeReferencialComMatriz:
    """§23 — a remissão deve apontar para o comentário-matriz que está de
    fato sendo registrado, e a unidade da remissão deve estar entre as
    unidades_relacionadas do template — rastreabilidade."""

    def test_comentario_matriz_com_tipo_errado_rejeita(self):
        registro = RegistroDeComentarios()
        comentario_com_tipo_errado = comentario_base(
            comment_id="CMT-NAO-MATRIZ", comment_type=CommentType.DIAGNOSTICO.value
        )
        with pytest.raises(ErroDeComentario):
            registrar_comentario_matriz_e_remissoes(
                registro, comentario_com_tipo_errado, template_matriz_base(), []
            )

    def test_remissao_com_matrix_comment_id_divergente_rejeita(self):
        registro = RegistroDeComentarios()
        comentario_matriz = comentario_base(
            comment_id="CMT-MATRIZ-04", comment_type=CommentType.COMENTARIO_MATRIZ.value
        )
        ocorrencia = (
            comentario_base(
                comment_id="CMT-REM-04",
                unit_id="UNIT-01",
                comment_type=CommentType.REMISSAO_A_COMENTARIO_MATRIZ.value,
                matrix_comment_id="CMT-MATRIZ-OUTRO",
            ),
            template_remissao_base(matrix_comment_id="CMT-MATRIZ-OUTRO", unit_id="UNIT-01"),
            criterio_consolida_base(),
        )
        with pytest.raises(ErroDeComentario):
            registrar_comentario_matriz_e_remissoes(
                registro, comentario_matriz, template_matriz_base(), [ocorrencia]
            )

    def test_unidade_fora_de_unidades_relacionadas_rejeita(self):
        registro = RegistroDeComentarios()
        comentario_matriz = comentario_base(
            comment_id="CMT-MATRIZ-05", comment_type=CommentType.COMENTARIO_MATRIZ.value
        )
        ocorrencia = (
            comentario_base(
                comment_id="CMT-REM-05",
                unit_id="UNIT-FORA-DA-MATRIZ",
                comment_type=CommentType.REMISSAO_A_COMENTARIO_MATRIZ.value,
                matrix_comment_id="CMT-MATRIZ-05",
            ),
            template_remissao_base(matrix_comment_id="CMT-MATRIZ-05", unit_id="UNIT-FORA-DA-MATRIZ"),
            criterio_consolida_base(),
        )
        with pytest.raises(ErroDeComentario):
            registrar_comentario_matriz_e_remissoes(
                registro, comentario_matriz, template_matriz_base(), [ocorrencia]
            )

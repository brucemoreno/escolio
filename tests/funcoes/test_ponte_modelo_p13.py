"""Testes da ponte entre `escolio/funcoes/execucao_p13.py` e
`escolio/cliente/` — etapas 8, 9 e 16-18.

Cliente mockado, como já é convenção em `tests/cliente/test_cliente.py`.
Nenhuma chamada real à API [instrução da sessão]."""

from unittest.mock import MagicMock

import pytest

from escolio.comentarios.criticidade import ClasseCriticidade, EixoCriticidade, MatrizCriticidade
from escolio.comentarios.seletividade import MatrizSeletividade, SelectionDecision
from escolio.comentarios.vocabulario import (
    COMMENT_TYPE_COMENTARIO_MATRIZ,
    COMMENT_TYPE_REMISSAO_A_COMENTARIO_MATRIZ,
    P13CommentStatus,
)
from escolio.funcoes import ponte_modelo_p13 as ponte
from escolio.ingestao.modelos import DocumentoIngerido, Metadados, Paragrafo


def documento_sintetico() -> DocumentoIngerido:
    return DocumentoIngerido(
        hash_documento="sinteticoponte001",
        caminho_original="synthetic://doc-ponte-p13-01",
        num_paginas=1,
        metadados=Metadados(titulo="Documento sintético — ponte de modelo P13"),
        paragrafos=[
            Paragrafo(
                unit_id="UNI-PAR-0001",
                texto="Parágrafo sintético usado para exercitar a ponte de modelo.",
                pagina_inicio=1,
                pagina_fim=1,
                secao_id=None,
            )
        ],
    )


def cliente_fake(blocos: list[dict]) -> MagicMock:
    cliente = MagicMock()
    cliente.chamar.return_value = MagicMock(blocos=blocos)
    return cliente


class TestGerarMatrizesCriticidade:
    def test_tool_use_valido_produz_matrizcriticidade(self):
        documento = documento_sintetico()
        avaliacao = {eixo.value: f"avaliação {eixo.value}" for eixo in EixoCriticidade}
        blocos = [
            {
                "type": "tool_use",
                "name": ponte._FERRAMENTA_CRITICIDADE,
                "input": {
                    "matrizes": [
                        {
                            "problem_id": "PROB-0001",
                            "unit_id": "UNI-PAR-0001",
                            "avaliacao_por_eixo": avaliacao,
                            "classe": "CRITICIDADE_MEDIA",
                            "justificativa_classe": "Síntese sintética.",
                        }
                    ]
                },
            }
        ]
        cliente = cliente_fake(blocos)

        matrizes = ponte.gerar_matrizes_criticidade(
            documento=documento, unit_ids=["UNI-PAR-0001"], cliente=cliente
        )

        assert len(matrizes) == 1
        assert isinstance(matrizes[0], MatrizCriticidade)
        assert matrizes[0].classe is ClasseCriticidade.CRITICIDADE_MEDIA

        _, kwargs = cliente.chamar.call_args
        assert kwargs["model"] == ponte.MODEL_ETAPA_8
        assert kwargs["effort"] == ponte.EFFORT_ETAPA_8
        assert kwargs["tools"][0]["name"] == ponte._FERRAMENTA_CRITICIDADE

    def test_eixo_faltante_levanta_erro_de_ponte(self):
        documento = documento_sintetico()
        avaliacao_incompleta = {EixoCriticidade.FACTUAL.value: "x"}  # falta os outros 11
        blocos = [
            {
                "type": "tool_use",
                "name": ponte._FERRAMENTA_CRITICIDADE,
                "input": {
                    "matrizes": [
                        {
                            "problem_id": "PROB-0002",
                            "unit_id": "UNI-PAR-0001",
                            "avaliacao_por_eixo": avaliacao_incompleta,
                            "classe": "CRITICIDADE_BAIXA",
                            "justificativa_classe": "x",
                        }
                    ]
                },
            }
        ]
        cliente = cliente_fake(blocos)

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_matrizes_criticidade(documento=documento, unit_ids=["UNI-PAR-0001"], cliente=cliente)

    def test_sem_tool_use_levanta_erro_de_ponte(self):
        documento = documento_sintetico()
        cliente = cliente_fake([{"type": "text", "text": "resposta fora da ferramenta"}])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_matrizes_criticidade(documento=documento, unit_ids=["UNI-PAR-0001"], cliente=cliente)

    def test_sem_unit_ids_levanta_erro_de_ponte_antes_de_chamar(self):
        documento = documento_sintetico()
        cliente = cliente_fake([])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_matrizes_criticidade(documento=documento, unit_ids=[], cliente=cliente)
        cliente.chamar.assert_not_called()


class TestGerarMatrizesSeletividade:
    def test_tool_use_valido_produz_matrizseletividade(self):
        documento = documento_sintetico()
        matriz_criticidade = MatrizCriticidade(
            problem_id="PROB-0001",
            unit_id="UNI-PAR-0001",
            avaliacao_por_eixo={eixo: "x" for eixo in EixoCriticidade},
            classe=ClasseCriticidade.CRITICIDADE_ALTA,
            justificativa_classe="x",
        )
        blocos = [
            {
                "type": "tool_use",
                "name": ponte._FERRAMENTA_SELETIVIDADE,
                "input": {
                    "matrizes": [
                        {
                            "selection_id": "SEL-0001",
                            "unit_id": "UNI-PAR-0001",
                            "candidate_problem_id": "PROB-0001",
                            "criticality": "CRITICIDADE_ALTA",
                            "material_impact": "x",
                            "novelty": "x",
                            "recurrence": "x",
                            "matrix_comment_coverage": "x",
                            "actionability": "x",
                            "evidence_sufficiency": "x",
                            "human_decision_required": "x",
                            "privacy_risk": "x",
                            "selection_decision": "COMENTAR",
                            "selection_rationale": "x",
                        }
                    ]
                },
            }
        ]
        cliente = cliente_fake(blocos)

        matrizes = ponte.gerar_matrizes_seletividade(
            documento=documento, matrizes_criticidade=[matriz_criticidade], cliente=cliente
        )

        assert len(matrizes) == 1
        assert isinstance(matrizes[0], MatrizSeletividade)
        assert matrizes[0].selection_decision is SelectionDecision.COMENTAR

        _, kwargs = cliente.chamar.call_args
        assert kwargs["model"] == ponte.MODEL_ETAPA_9
        assert kwargs["effort"] == ponte.EFFORT_ETAPA_9

    def test_sem_candidatos_levanta_erro_de_ponte_antes_de_chamar(self):
        documento = documento_sintetico()
        cliente = cliente_fake([])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_matrizes_seletividade(documento=documento, matrizes_criticidade=[], cliente=cliente)
        cliente.chamar.assert_not_called()


def candidato_selecionado(selection_id="SEL-0001", problem_id="PROB-0001") -> MatrizSeletividade:
    return MatrizSeletividade(
        selection_id=selection_id,
        unit_id="UNI-PAR-0001",
        candidate_problem_id=problem_id,
        criticality=ClasseCriticidade.CRITICIDADE_ALTA,
        material_impact="x",
        novelty="x",
        recurrence="x",
        matrix_comment_coverage="x",
        actionability="x",
        evidence_sufficiency="x",
        human_decision_required="x",
        privacy_risk="x",
        selection_decision=SelectionDecision.COMENTAR,
        selection_rationale="x",
    )


def bloco_comentario(*, selection_id="SEL-0001", comment_type="COMENTARIO_FACTUAL", matrix_comment_id=None):
    return {
        "type": "tool_use",
        "name": ponte._FERRAMENTA_COMENTARIOS,
        "input": {
            "comentarios": [
                {
                    "comment_id": "CMT-0001",
                    "selection_id": selection_id,
                    "unit_id": "UNI-PAR-0001",
                    "anchor_start": "0",
                    "anchor_end": "10",
                    "anchor_text_hash": "sha256:x",
                    "comment_type": comment_type,
                    "priority": "PRIORIDADE_MEDIA",
                    "severity": "MODERADA",
                    "problem": "x",
                    "evidence": "x",
                    "impact": "x",
                    "recommended_action": "x",
                    "intervention_level": "INT-04",
                    "authority_required": "USUARIO_PROPONENTE",
                    "gate": "GATE_DE_VALIDACAO_FINAL",
                    "source_status": "VERIFICADA",
                    "voice_impact": "NENHUM",
                    "privacy_classification": "PUBLIC",
                    "reversible": True,
                    **({"matrix_comment_id": matrix_comment_id} if matrix_comment_id else {}),
                }
            ]
        },
    }


class TestGerarComentarios:
    def test_tool_use_valido_produz_p13comment_em_status_draft(self):
        documento = documento_sintetico()
        cliente = cliente_fake([bloco_comentario()])

        comentarios = ponte.gerar_comentarios(
            documento=documento,
            document_id="MAT-DOC-0001",
            document_version="1.0.0",
            module_id="P13",
            candidatos=[candidato_selecionado()],
            cliente=cliente,
        )

        assert len(comentarios) == 1
        assert comentarios[0].status is P13CommentStatus.DRAFT
        assert comentarios[0].document_id == "MAT-DOC-0001"

        _, kwargs = cliente.chamar.call_args
        assert kwargs["model"] == ponte.MODEL_ETAPAS_16_18
        assert kwargs["effort"] == ponte.EFFORT_ETAPAS_16_18

    def test_comment_type_divergente_do_esperado_levanta_erro(self):
        documento = documento_sintetico()
        cliente = cliente_fake([bloco_comentario(comment_type="COMENTARIO_FACTUAL")])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_comentarios(
                documento=documento,
                document_id="MAT-DOC-0001",
                document_version="1.0.0",
                module_id="P13",
                candidatos=[candidato_selecionado()],
                cliente=cliente,
                comment_type_esperado=COMMENT_TYPE_COMENTARIO_MATRIZ,
            )

    def test_matrix_comment_id_do_chamador_sobrescreve_o_do_modelo(self):
        documento = documento_sintetico()
        cliente = cliente_fake(
            [
                bloco_comentario(
                    comment_type=COMMENT_TYPE_REMISSAO_A_COMENTARIO_MATRIZ,
                    matrix_comment_id="CMT-MATRIZ-ERRADO",
                )
            ]
        )

        comentarios = ponte.gerar_comentarios(
            documento=documento,
            document_id="MAT-DOC-0001",
            document_version="1.0.0",
            module_id="P13",
            candidatos=[candidato_selecionado()],
            cliente=cliente,
            comment_type_esperado=COMMENT_TYPE_REMISSAO_A_COMENTARIO_MATRIZ,
            matrix_comment_id_por_candidato={"SEL-0001": "CMT-MATRIZ-CORRETO"},
        )

        assert comentarios[0].matrix_comment_id == "CMT-MATRIZ-CORRETO"

    def test_sem_candidatos_levanta_erro_de_ponte_antes_de_chamar(self):
        documento = documento_sintetico()
        cliente = cliente_fake([])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_comentarios(
                documento=documento,
                document_id="MAT-DOC-0001",
                document_version="1.0.0",
                module_id="P13",
                candidatos=[],
                cliente=cliente,
            )
        cliente.chamar.assert_not_called()

"""Primeiro percurso ponta a ponta: ingestão → InputItem → roteador →
matrizes de criticidade/seletividade → registro de comentários (P13/F04).

Nenhuma peça deste percurso jamais rodou junto com as outras — cada peça só
tinha teste de unidade, por pacote. Este arquivo não testa cobertura de
caso: testa se os tipos e identificadores que uma peça produz são os que a
peça seguinte consome. Documento sintético, fabricado aqui — sem tocar
data/dev/ nem data/gold/, sem chamar a API [instrução da sessão].

Desencaixes encontrados ao montar o percurso estão registrados em
docs/backlog.md (sessão de teste de integração). Nada é consertado aqui.
"""

import pytest

from escolio.comentarios.comentario import P13Comment
from escolio.comentarios.criticidade import ClasseCriticidade, EixoCriticidade, MatrizCriticidade
from escolio.comentarios.registro import RegistroDeComentarios
from escolio.comentarios.seletividade import (
    MatrizSeletividade,
    SelectionDecision,
    aplicar_selecao,
    exige_referencia_valida_a_criticidade,
)
from escolio.comentarios.vocabulario import P13CommentStatus
from escolio.adaptadores.ingestao_para_input_item import (
    input_item_de_documento,
    material_id_de_documento,
)
from escolio.contrato.entrada import InputItem
from escolio.contrato.referencia import SemanticVersion
from escolio.contrato.requisicao import Authorization, ExpectedOutput, Request, Requester, Scope
from escolio.contrato.vocabulario import AbstentionCategory, AuthorizationStatus
from escolio.funcoes import roteador
from escolio.funcoes.roteador import AdmissaoDeMaterial
from escolio.funcoes.vocabulario import FuncaoId
from escolio.ingestao.modelos import DocumentoIngerido, Metadados, Paragrafo


def documento_sintetico() -> DocumentoIngerido:
    """Um `DocumentoIngerido` fabricado à mão — sem pdfplumber, sem PDF em
    disco. `DocumentoIngerido` não valida campos obrigatórios em
    `__post_init__` [escolio/ingestao/modelos.py, docstring de topo], então
    isto é o mesmo objeto que `parse_pdf` produziria, só que sem passar
    pelo parser."""
    return DocumentoIngerido(
        hash_documento="sinteticoabc123",
        caminho_original="synthetic://doc-integracao-01",
        num_paginas=1,
        metadados=Metadados(titulo="Documento sintético de teste de integração"),
        paragrafos=[
            Paragrafo(
                unit_id="UNI-PAR-0001",
                texto="Parágrafo sintético usado para exercitar o percurso E1-E4 do P13.",
                pagina_inicio=1,
                pagina_fim=1,
                secao_id=None,
            )
        ],
    )


def requisicao_p13(inputs: list[InputItem], **overrides) -> Request:
    campos = dict(
        schema_version=SemanticVersion(1, 0, 0),
        request_id="REQ-INTEGRACAO-0001",
        project_id="PRJ-INTEGRACAO-0001",
        component_id="P13",
        function_id=FuncaoId.F04.value,
        operation="CARTOGRAFIA_GLOBAL",
        requester=Requester(role="ENGENHEIRO_LLM", authority_basis="R03 §4.5"),
        scope=Scope(allowed_operations=["CARTOGRAFIA_GLOBAL"]),
        authorization=Authorization(status=AuthorizationStatus.UNVERIFIED),
        expected_output=ExpectedOutput(type="COMENTARIOS"),
        inputs=inputs,
    )
    campos.update(overrides)
    return Request(**campos)


class TestPercursoCompleto:
    """Caminho feliz: material declarado para F04/P13 chega até o registro
    de comentários."""

    def test_percurso_e1_a_e4_ate_registro_de_comentario(self):
        # E2 — ingestão controlada (sintética).
        documento = documento_sintetico()
        paragrafo = documento.paragrafos[0]

        # E1/adaptador — DocumentoIngerido -> InputItem [P09 §6].
        item = input_item_de_documento(documento)
        assert item.classification.functions == []  # confirma BL-014: adaptador não declara

        # Ato humano simulado: só depois deste passo o material é elegível
        # para F04. Nenhum código do adaptador ou do roteador faz isto
        # sozinho [CLAUDE.md, "O que a peça 6 fechou"; BL-014].
        item.classification.functions = [FuncaoId.F04.value]

        # E1 — roteador confere a requisição contra o catálogo.
        request = requisicao_p13(inputs=[item])
        decisao = roteador.rotear(request)

        assert decisao.funcao is FuncaoId.F04
        assert decisao.materiais_fora_de_escopo == ()
        assert decisao.materiais_indeterminados == ()
        assert decisao.materiais[0].admissao is AdmissaoDeMaterial.DECLARADO

        # E4 — matriz de criticidade (12 eixos). unit_id fabricado por mim:
        # nenhum código liga Paragrafo.unit_id a MatrizCriticidade.unit_id.
        matriz_criticidade = MatrizCriticidade(
            problem_id="PROB-INTEGRACAO-0001",
            unit_id=paragrafo.unit_id,
            avaliacao_por_eixo={
                eixo: f"avaliação sintética do eixo {eixo.value}" for eixo in EixoCriticidade
            },
            classe=ClasseCriticidade.CRITICIDADE_MEDIA,
            justificativa_classe="Classe atribuída manualmente para exercitar o percurso.",
        )

        # E4 — matriz de seletividade (10 fatores), reusando a classe e o
        # unit_id da matriz de criticidade — de novo, ligação que só existe
        # porque este teste a construiu, não porque o código a impõe.
        matriz_seletividade = MatrizSeletividade(
            selection_id="SEL-INTEGRACAO-0001",
            unit_id=paragrafo.unit_id,
            candidate_problem_id=matriz_criticidade.problem_id,
            criticality=matriz_criticidade.classe,
            material_impact="Impacto sintético.",
            novelty="Não repete achado anterior.",
            recurrence="Ocorrência única.",
            matrix_comment_coverage="Não coberto por comentário-matriz.",
            actionability="Ação possível e proporcional.",
            evidence_sufficiency="Evidência suficiente.",
            human_decision_required="Não.",
            privacy_risk="Nenhum.",
            selection_decision=SelectionDecision.COMENTAR,
            selection_rationale="Ganho de orientação supera custo de poluição documental.",
        )
        exige_referencia_valida_a_criticidade([matriz_seletividade], [matriz_criticidade])
        selecionados = aplicar_selecao([matriz_seletividade])
        assert selecionados == [matriz_seletividade]

        # E6 — comentário individual, registrado. document_id: não há
        # nenhuma fonte nem código dizendo se deve ser InputItem.input_id
        # ou o material_id do P19 §10 — uso material_id aqui por decisão
        # deste teste, não por regra.
        comentario = P13Comment(
            comment_id="CMT-INTEGRACAO-0001",
            document_id=material_id_de_documento(documento),
            document_version="1.0.0",
            module_id="P13",
            unit_id=paragrafo.unit_id,
            anchor_start="0",
            anchor_end=str(len(paragrafo.texto)),
            anchor_text_hash="sha256:sintetico",
            comment_type="OBSERVACAO_ESTRUTURAL",
            priority="PRIORIDADE_MEDIA",
            severity="MODERADA",
            problem="Problema sintético para o teste de integração.",
            evidence=paragrafo.texto,
            impact="Impacto sintético.",
            recommended_action="Ação recomendada sintética.",
            intervention_level="INT-04",
            authority_required="USUARIO_PROPONENTE",
            gate="GATE_DE_VALIDACAO_FINAL",
            source_status="VERIFICADA",
            voice_impact="NENHUM",
            privacy_classification="PUBLIC",
            reversible=True,
            status=P13CommentStatus.DRAFT,
        )

        registro = RegistroDeComentarios()
        registro.registrar(comentario)

        assert registro.obter(comentario.comment_id) is comentario
        assert registro.obter(comentario.comment_id).unit_id == paragrafo.unit_id


class TestPercursoAbstencaoPorFaltaDeDeclaracao:
    """Sem o ato humano de declarar `classification.functions`, o material é
    INDETERMINADO e o percurso para no roteador — não chega às matrizes."""

    def test_material_sem_functions_declaradas_produz_indeterminado(self):
        documento = documento_sintetico()
        item = input_item_de_documento(documento)
        # Nenhuma atribuição de functions aqui — é o estado real que a
        # ingestão produz sozinha [BL-014].

        request = requisicao_p13(inputs=[item])
        decisao = roteador.rotear(request)

        assert decisao.materiais[0].admissao is AdmissaoDeMaterial.INDETERMINADO
        assert decisao.materiais_indeterminados == decisao.materiais

        abstencao = roteador.abstencao_por_fora_de_escopo(
            abstention_id="ABST-INTEGRACAO-0001",
            request_id=request.request_id,
            funcao_id=decisao.funcao,
            materiais=decisao.materiais_indeterminados,
        )
        assert abstencao.category is AbstentionCategory.OUT_OF_SCOPE
        assert abstencao.scope == [item.input_id]

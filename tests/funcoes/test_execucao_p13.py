"""Testes do orquestrador de execução do P13 — fecha BL-021/BL-022.

Documento sintético, sem pdfplumber e sem chamada à API [instrução da
sessão] — mesmo padrão de tests/integracao/test_pipeline_p13.py, que este
módulo substitui em parte: o que aquele teste fazia escrevendo Python solto
entre as peças, `avancar()` agora faz por uma função de orquestração.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from escolio.bvaa.abstencao import GatilhoDeAbstencao
from escolio.bvaa.vocabulario import EstadoBibliografico
from escolio.cliente.erros import (
    ErroDeConexao,
    ErroDeLimiteDeTaxa,
    ErroDeTimeout,
    ErroRespostaTruncada,
)
from escolio.comentarios.comentario import P13Comment
from escolio.comentarios.criticidade import ClasseCriticidade, EixoCriticidade, MatrizCriticidade
from escolio.comentarios.seletividade import MatrizSeletividade, SelectionDecision
from escolio.comentarios.vocabulario import P13CommentStatus
from escolio.contrato.entrada import Classification, InputItem, Provenance
from escolio.contrato.referencia import SemanticVersion
from escolio.contrato.requisicao import Authorization, ExpectedOutput, Request, Requester, Scope
from escolio.contrato.vocabulario import AuthorizationStatus, InputType
from escolio.drive.conector import ArquivoDrive
from escolio.funcoes import ponte_modelo_p13 as ponte
from escolio.funcoes import roteador
from escolio.funcoes.bvaa_drive import (
    EvidenciaDeAcessoDrive,
    EvidenciaDeIdentificacaoDrive,
    OperacaoDeAcesso,
)
from escolio.funcoes.curador_bvaa import EscalonamentoDoCurador
from escolio.funcoes.execucao_p13 import (
    CausaDeParada,
    EntradaEtapaP13,
    ErroDeExecucaoP13,
    TipoDeResultadoEtapa,
    avancar,
    construir_estado_inicial,
)
from escolio.funcoes.salvaguarda_privacidade_p13 import AlertaDePrivacidade
from escolio.funcoes.vocabulario import FuncaoId
from escolio.ingestao.modelos import DocumentoIngerido, ItemDeReferencia, Metadados, Paragrafo
from escolio.relacao import RelacaoAfirmacaoEvidencia
from escolio.vocabulario import (
    AccessState,
    ClaimType,
    Confidence,
    EvidenceLevel,
    LocationType,
    ReadingState,
    Reversibility,
    SourceType,
    Sufficiency,
    UsageStatus,
    ValidationState,
)
from escolio.voz.deteccao import AchadoDeFidelidade
from escolio.voz.perfil import PerfilDeVoz
from escolio.voz.vocabulario import Confidence as ConfidenceVoz
from escolio.voz.vocabulario import (
    DesvioBloqueante,
    ResultadoDeFidelidade,
    StatusDePerfil,
    TipoDePerfil,
)


def documento_sintetico() -> DocumentoIngerido:
    return DocumentoIngerido(
        hash_documento="sinteticoexec001",
        caminho_original="synthetic://doc-execucao-p13-01",
        num_paginas=1,
        metadados=Metadados(titulo="Documento sintético — orquestrador P13"),
        paragrafos=[
            Paragrafo(
                unit_id="UNI-PAR-0001",
                texto="Parágrafo sintético usado para exercitar o orquestrador do P13.",
                pagina_inicio=1,
                pagina_fim=1,
                secao_id=None,
            )
        ],
    )


def item_declarado_para_f04() -> InputItem:
    i = InputItem(
        input_id="INP-EXEC-0001",
        type=InputType.DOCUMENT,
        provenance=Provenance(source="synthetic://doc", source_type="DOCUMENTO_PDF"),
        classification=Classification(trust="ORIGEM_DESCONHECIDA", functions=[FuncaoId.F04.value]),
    )
    return i


def requisicao_p13(inputs, **overrides) -> Request:
    campos = dict(
        schema_version=SemanticVersion(1, 0, 0),
        request_id="REQ-EXEC-0001",
        project_id="PRJ-EXEC-0001",
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


def estado_roteado(inputs):
    request = requisicao_p13(inputs=inputs)
    decisao = roteador.rotear(request)
    return construir_estado_inicial(request, decisao)


class TestPercursoCompletoAteOPontoDeExtensao:
    """E1-E4 até a seleção (etapa 10) com dados sintéticos; a etapa 11 para
    como ponto de extensão de modelo — a auditoria não tenta preencher juízo
    diagnóstico que nenhuma sessão anterior modelou."""

    def test_avanca_ate_selecao_e_para_em_verificacao_de_fontes(self):
        documento = documento_sintetico()
        paragrafo = documento.paragrafos[0]
        estado = estado_roteado([item_declarado_para_f04()])

        avancar(estado)  # 1 intake
        avancar(estado)  # 2 confirmação de autoridade
        avancar(estado, EntradaEtapaP13(dependencias_obrigatorias_confirmadas=True))  # 3
        avancar(estado, EntradaEtapaP13(documento=documento))  # 4 ingestão controlada
        avancar(estado, EntradaEtapaP13(document_version="1.0.0"))  # 5
        avancar(estado)  # 6 cartografia global
        avancar(estado)  # 7 identificação das unidades

        assert estado.contexto.unidades_conhecidas == {paragrafo.unit_id}

        matriz_criticidade = MatrizCriticidade(
            problem_id="PROB-EXEC-0001",
            unit_id=paragrafo.unit_id,
            avaliacao_por_eixo={eixo: f"avaliação sintética {eixo.value}" for eixo in EixoCriticidade},
            classe=ClasseCriticidade.CRITICIDADE_MEDIA,
            justificativa_classe="Classe atribuída manualmente para exercitar o orquestrador.",
        )
        avancar(estado, EntradaEtapaP13(matrizes_criticidade=[matriz_criticidade]))  # 8

        matriz_seletividade = MatrizSeletividade(
            selection_id="SEL-EXEC-0001",
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
        avancar(estado, EntradaEtapaP13(matrizes_seletividade=[matriz_seletividade]))  # 9
        avancar(estado)  # 10 seleção

        assert estado.contexto.selecionados == [matriz_seletividade]
        assert estado.concluidas == 10

        # 11 — verificação de fontes: ponto de extensão, não preenchido.
        avancar(estado)
        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.PARADA
        assert ultimo.causa is CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO
        assert estado.concluidas == 10  # a parada não avança o ponteiro de fluxo

    def test_document_id_diverge_do_material_id_levanta_bl_022(self):
        # Etapas 11-15 são PONTO_DE_EXTENSAO_DE_MODELO permanente nesta
        # sessão [sem chamada à API] — avancar() nunca as ultrapassa
        # sozinho, porque `concluidas` só conta EXECUTADA (ver
        # `EstadoDeExecucaoP13.concluidas`). Alcançar a etapa 16 para testar
        # a checagem de `document_id` [BL-022] exige simular que uma sessão
        # futura, com os objetos que 11-15 ainda não têm, as completou —
        # mesma técnica de `test_avancar_apos_fluxo_encerrado_levanta`.
        from escolio.funcoes.execucao_p13 import ResultadoDeEtapa
        from escolio.funcoes.p13 import DECLARACAO as DECLARACAO_P13

        documento = documento_sintetico()
        paragrafo = documento.paragrafos[0]
        estado = estado_roteado([item_declarado_para_f04()])
        for _ in range(7):
            avancar(
                estado,
                EntradaEtapaP13(
                    dependencias_obrigatorias_confirmadas=True,
                    documento=documento,
                    document_version="1.0.0",
                ),
            )
        matriz_criticidade = MatrizCriticidade(
            problem_id="PROB-EXEC-0002",
            unit_id=paragrafo.unit_id,
            avaliacao_por_eixo={eixo: "x" for eixo in EixoCriticidade},
            classe=ClasseCriticidade.CRITICIDADE_BAIXA,
            justificativa_classe="Justificativa sintética.",
        )
        matriz_seletividade = MatrizSeletividade(
            selection_id="SEL-EXEC-0002",
            unit_id=paragrafo.unit_id,
            candidate_problem_id=matriz_criticidade.problem_id,
            criticality=matriz_criticidade.classe,
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
        avancar(estado, EntradaEtapaP13(matrizes_criticidade=[matriz_criticidade]))
        avancar(estado, EntradaEtapaP13(matrizes_seletividade=[matriz_seletividade]))
        avancar(estado)
        assert estado.concluidas == 10

        estado.historico.extend(
            ResultadoDeEtapa(etapa=DECLARACAO_P13.etapa(n), tipo=TipoDeResultadoEtapa.EXECUTADA, justificativa="simulado")
            for n in range(11, 16)
        )
        assert estado.concluidas == 15

        comentario_com_document_id_errado = P13Comment(
            comment_id="CMT-EXEC-0001",
            document_id="MAT-DOC-outro-documento",
            document_version="1.0.0",
            module_id="P13",
            unit_id=paragrafo.unit_id,
            anchor_start="0",
            anchor_end="10",
            anchor_text_hash="sha256:sintetico",
            comment_type="COMENTARIO_MATRIZ",
            priority="PRIORIDADE_MEDIA",
            severity="MODERADA",
            problem="x",
            evidence="x",
            impact="x",
            recommended_action="x",
            intervention_level="INT-04",
            authority_required="USUARIO_PROPONENTE",
            gate="GATE_DE_VALIDACAO_FINAL",
            source_status="VERIFICADA",
            voice_impact="NENHUM",
            privacy_classification="PUBLIC",
            reversible=True,
            status=P13CommentStatus.DRAFT,
        )
        with pytest.raises(ErroDeExecucaoP13) as excinfo:
            avancar(estado, EntradaEtapaP13(comentarios_matriz=[comentario_com_document_id_errado]))
        assert "BL-022" in str(excinfo.value)


class TestEtapaQueNaoPodeExecutar:
    """O orquestrador para na primeira etapa sem entrada suficiente — não
    improvisa, não avança, não re-executa a etapa seguinte."""

    def test_etapa_8_sem_matrizes_para_e_nao_avanca(self):
        documento = documento_sintetico()
        estado = estado_roteado([item_declarado_para_f04()])
        avancar(estado)
        avancar(estado)
        avancar(estado, EntradaEtapaP13(dependencias_obrigatorias_confirmadas=True))
        avancar(estado, EntradaEtapaP13(documento=documento))
        avancar(estado, EntradaEtapaP13(document_version="1.0.0"))
        avancar(estado)
        avancar(estado)
        assert estado.concluidas == 7

        avancar(estado)  # 8, sem matrizes_criticidade
        assert estado.concluidas == 7
        assert estado.historico[-1].causa is CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO

        # Chamar de novo sem fornecer dado novo reoferece a MESMA etapa —
        # nunca pula para a 9.
        avancar(estado)
        assert estado.concluidas == 7
        assert estado.historico[-1].etapa.ordem == 8
        assert len(estado.historico) == 9  # 7 executadas + 2 tentativas em 8

    def test_material_nao_declarado_para_na_etapa_1(self):
        item_indeterminado = InputItem(
            input_id="INP-EXEC-INDET",
            type=InputType.DOCUMENT,
            provenance=Provenance(source="synthetic://doc", source_type="DOCUMENTO_PDF"),
            classification=Classification(trust="ORIGEM_DESCONHECIDA"),
        )
        estado = estado_roteado([item_indeterminado])
        avancar(estado)
        assert estado.concluidas == 0
        assert estado.historico[-1].causa is CausaDeParada.MATERIAL_NAO_DECLARADO

    def test_avancar_apos_fluxo_encerrado_levanta(self):
        # As etapas 11-15 não têm entrada aceitável nesta sessão [PONTO_DE_
        # EXTENSAO_DE_MODELO permanente] — o fluxo real nunca alcança a
        # etapa 29 sem uma sessão futura que feche esse ponto de extensão.
        # Este teste verifica só a disciplina de "não reexecutar após o
        # fim", simulando concluidas=29 diretamente no histórico — não é
        # o percurso de um documento real, é a garantia estrutural de
        # `avancar()` sobre `DeclaracaoDeFuncao.proxima_etapa`.
        from escolio.funcoes.execucao_p13 import ResultadoDeEtapa
        from escolio.funcoes.p13 import DECLARACAO as DECLARACAO_P13

        estado = estado_roteado([item_declarado_para_f04()])
        estado.historico.extend(
            ResultadoDeEtapa(etapa=etapa, tipo=TipoDeResultadoEtapa.EXECUTADA, justificativa="simulado")
            for etapa in DECLARACAO_P13.fluxo
        )
        assert estado.concluidas == 29
        assert estado.encerrado is True
        with pytest.raises(ErroDeExecucaoP13):
            avancar(estado)


def _cliente_fake(blocos: list[dict]) -> MagicMock:
    cliente = MagicMock()
    cliente.chamar.return_value = MagicMock(blocos=blocos)
    return cliente


def documento_sintetico_com_referencia() -> DocumentoIngerido:
    documento = documento_sintetico()
    documento.referencias.append(
        ItemDeReferencia(unit_id="UNI-REF-0001", texto="GREWE, R. (1979). Fonte sintética.", pagina=None)
    )
    return documento


def _avancar_ate_selecao(estado, documento) -> None:
    paragrafo = documento.paragrafos[0]
    avancar(estado)  # 1 intake
    avancar(estado)  # 2 confirmação de autoridade
    avancar(estado, EntradaEtapaP13(dependencias_obrigatorias_confirmadas=True))  # 3
    avancar(estado, EntradaEtapaP13(documento=documento))  # 4 ingestão controlada
    avancar(estado, EntradaEtapaP13(document_version="1.0.0"))  # 5
    avancar(estado)  # 6 cartografia global
    avancar(estado)  # 7 identificação das unidades
    matriz_criticidade = MatrizCriticidade(
        problem_id="PROB-EXEC-BVAA",
        unit_id=paragrafo.unit_id,
        avaliacao_por_eixo={eixo: "x" for eixo in EixoCriticidade},
        classe=ClasseCriticidade.CRITICIDADE_BAIXA,
        justificativa_classe="x",
    )
    avancar(estado, EntradaEtapaP13(matrizes_criticidade=[matriz_criticidade]))  # 8
    matriz_seletividade = MatrizSeletividade(
        selection_id="SEL-EXEC-BVAA",
        unit_id=paragrafo.unit_id,
        candidate_problem_id=matriz_criticidade.problem_id,
        criticality=matriz_criticidade.classe,
        material_impact="x", novelty="x", recurrence="x", matrix_comment_coverage="x",
        actionability="x", evidence_sufficiency="x", human_decision_required="x", privacy_risk="x",
        selection_decision=SelectionDecision.COMENTAR, selection_rationale="x",
    )
    avancar(estado, EntradaEtapaP13(matrizes_seletividade=[matriz_seletividade]))  # 9
    avancar(estado)  # 10 seleção
    assert estado.concluidas == 10


def _avancar_ate_etapa_7(estado, documento) -> None:
    avancar(estado)  # 1 intake
    avancar(estado)  # 2 confirmação de autoridade
    avancar(estado, EntradaEtapaP13(dependencias_obrigatorias_confirmadas=True))  # 3
    avancar(estado, EntradaEtapaP13(documento=documento))  # 4 ingestão controlada
    avancar(estado, EntradaEtapaP13(document_version="1.0.0"))  # 5
    avancar(estado)  # 6 cartografia global
    avancar(estado)  # 7 identificação das unidades
    assert estado.concluidas == 7


class TestFalhaNaChamadaAoModelo:
    """Sessão de 2026-08-12 (quarta peça) — achado do primeiro piloto real
    contra um capítulo verdadeiro: `ErroDeCliente` (truncamento, limite de
    taxa, timeout, conexão) crashava o percurso em vez de virar
    `ResultadoDeEtapa` com causa estruturada. Um teste por etapa que chama
    modelo (8, 9, 13, 16) — a mesma disciplina vale para qualquer uma."""

    def test_etapa_8_erro_de_cliente_vira_causa_estruturada_nao_exececao(self):
        documento = documento_sintetico_com_referencia()
        paragrafo = documento.paragrafos[0]
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_etapa_7(estado, documento)

        cliente = MagicMock()
        cliente.chamar.side_effect = ErroRespostaTruncada("claude-sonnet-5")

        avancar(estado, EntradaEtapaP13(cliente=cliente, unidades_para_matriz_criticidade=[paragrafo.unit_id]))

        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.PARADA
        assert ultimo.causa is CausaDeParada.FALHA_NA_CHAMADA_AO_MODELO
        assert "RESPOSTA_TRUNCADA" in ultimo.justificativa
        assert estado.concluidas == 7  # não avançou, mas também não crashou

        # POL-012: a tentativa fica registrada; a próxima chamada reoferece
        # a mesma etapa, não avança para a 9 nem trava para sempre.
        assert len(estado.historico) == 8
        assert estado.historico[-1].etapa.ordem == 8

    def test_etapa_8_resposta_mal_formada_vira_causa_estruturada_nao_crash(self):
        """Sessão de 2026-08-13 — segundo piloto real contra o capítulo 5,
        depois da correção de lotes: a chamada completa, mas o item de
        'matrizes' veio como string, não objeto. Antes desta correção,
        `TypeError` propagava cru; agora vira `ResultadoDeEtapa` com causa
        estruturada, mesma disciplina de `FALHA_NA_CHAMADA_AO_MODELO`."""
        documento = documento_sintetico_com_referencia()
        paragrafo = documento.paragrafos[0]
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_etapa_7(estado, documento)

        cliente = MagicMock()
        cliente.chamar.return_value = MagicMock(
            blocos=[
                {
                    "type": "tool_use",
                    "name": ponte._FERRAMENTA_CRITICIDADE,
                    "input": {"matrizes": ["isto não é um objeto"]},
                }
            ]
        )

        avancar(estado, EntradaEtapaP13(cliente=cliente, unidades_para_matriz_criticidade=[paragrafo.unit_id]))

        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.PARADA
        assert ultimo.causa is CausaDeParada.RESPOSTA_DO_MODELO_MAL_FORMADA
        assert estado.concluidas == 7  # não avançou, mas também não crashou
        assert len(estado.historico) == 8
        assert estado.historico[-1].etapa.ordem == 8

    def test_etapa_9_erro_de_cliente_vira_causa_estruturada(self):
        documento = documento_sintetico_com_referencia()
        paragrafo = documento.paragrafos[0]
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_etapa_7(estado, documento)
        matriz_criticidade = MatrizCriticidade(
            problem_id="PROB-FALHA-0001",
            unit_id=paragrafo.unit_id,
            avaliacao_por_eixo={eixo: "x" for eixo in EixoCriticidade},
            classe=ClasseCriticidade.CRITICIDADE_BAIXA,
            justificativa_classe="x",
        )
        avancar(estado, EntradaEtapaP13(matrizes_criticidade=[matriz_criticidade]))  # 8

        cliente = MagicMock()
        cliente.chamar.side_effect = ErroDeLimiteDeTaxa("limite de taxa sintético")
        avancar(estado, EntradaEtapaP13(cliente=cliente))  # 9

        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.PARADA
        assert ultimo.causa is CausaDeParada.FALHA_NA_CHAMADA_AO_MODELO
        assert "LIMITE_DE_TAXA" in ultimo.justificativa
        assert "provavelmente vale repetir" in ultimo.justificativa  # retryable=True

    def test_etapa_13_erro_de_cliente_no_meio_do_loop_de_unidades(self):
        documento = documento_sintetico_com_referencia()
        paragrafo = documento.paragrafos[0]
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)
        _avancar_etapa_11_completa(estado, documento)
        avancar(estado, EntradaEtapaP13(relacoes_afirmacao_evidencia=[]))  # 12

        cliente = MagicMock()
        cliente.chamar.side_effect = ErroDeConexao("conexão sintética perdida")
        avancar(
            estado,
            EntradaEtapaP13(
                perfil_de_voz=_perfil_de_voz_sintetico(),
                cliente=cliente,
                unidades_para_deteccao_fidelidade=[paragrafo.unit_id],
            ),
        )  # 13

        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.PARADA
        assert ultimo.causa is CausaDeParada.FALHA_NA_CHAMADA_AO_MODELO
        assert "ERRO_DE_CONEXAO" in ultimo.justificativa
        assert paragrafo.unit_id not in estado.contexto.avaliacoes_fidelidade

    def test_etapa_16_erro_de_cliente_vira_causa_estruturada(self):
        documento = documento_sintetico_com_referencia()
        paragrafo = documento.paragrafos[0]
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)
        _avancar_etapa_11_completa(estado, documento)
        avancar(estado, EntradaEtapaP13(relacoes_afirmacao_evidencia=[]))  # 12
        achado = AchadoDeFidelidade(
            tipo=DesvioBloqueante.INVENCAO_FACTUAL, observado=False, evidencia="", confianca=ConfidenceVoz.ALTA
        )
        avancar(
            estado,
            EntradaEtapaP13(perfil_de_voz=_perfil_de_voz_sintetico(), achados_fidelidade={paragrafo.unit_id: [achado]}),
        )  # 13
        avancar(estado)  # 14
        avancar(estado, EntradaEtapaP13(problemas_sistemicos_conhecidos=[]))  # 15
        assert estado.concluidas == 15

        candidato = estado.contexto.selecionados[0]
        cliente = MagicMock()
        cliente.chamar.side_effect = ErroDeTimeout("timeout sintético na elaboração")
        avancar(
            estado,
            EntradaEtapaP13(cliente=cliente, candidatos_para_comentario_matriz=[candidato]),
        )  # 16

        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.PARADA
        assert ultimo.causa is CausaDeParada.FALHA_NA_CHAMADA_AO_MODELO
        assert "TIMEOUT" in ultimo.justificativa


class TestEtapaOnzeVerificacaoDeFontes:
    """Etapa 11 ligada ao BVAA via evidência de acesso ao Drive
    [docs/spec/bvaa-drive-integracao.md] — autorizado e construído em
    2026-08-12. Licencia só T04/T05; sem evidência, comportamento idêntico
    ao de antes desta sessão."""

    def test_sem_evidencia_permanece_ponto_de_extensao_de_modelo(self):
        documento = documento_sintetico_com_referencia()
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)

        avancar(estado)  # 11, sem evidencias_de_acesso
        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.PARADA
        assert ultimo.causa is CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO
        assert estado.concluidas == 10

    def test_evidencia_localizado_a_partir_do_estado_inicial_avanca_para_acessivel(self):
        documento = documento_sintetico_com_referencia()
        referencia = documento.referencias[0]
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)

        arquivo = ArquivoDrive(id="x", nome="Grewe1979.pdf", mime_type="application/pdf",
                                tamanho_bytes=1, modificado_em=None)
        estado.contexto.estados_bibliograficos[referencia.unit_id] = EstadoBibliografico.LOCALIZADA
        evidencia = EvidenciaDeAcessoDrive(arquivo=arquivo, operacao=OperacaoDeAcesso.LOCALIZADO)

        avancar(estado, EntradaEtapaP13(evidencias_de_acesso={referencia.unit_id: evidencia}))

        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.EXECUTADA
        assert estado.concluidas == 11
        assert estado.contexto.estados_bibliograficos[referencia.unit_id] is EstadoBibliografico.ACESSIVEL

    def test_evidencia_para_referencia_desconhecida_levanta(self):
        documento = documento_sintetico_com_referencia()
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)

        arquivo = ArquivoDrive(id="x", nome="x.pdf", mime_type="application/pdf",
                                tamanho_bytes=1, modificado_em=None)
        evidencia = EvidenciaDeAcessoDrive(arquivo=arquivo, operacao=OperacaoDeAcesso.LOCALIZADO)

        with pytest.raises(ErroDeExecucaoP13) as excinfo:
            avancar(estado, EntradaEtapaP13(evidencias_de_acesso={"UNI-REF-INEXISTENTE": evidencia}))
        assert "P13-§26" in str(excinfo.value)
        assert estado.concluidas == 10

    def test_identificacao_e_acesso_na_mesma_chamada_chega_a_acessada(self):
        # Sessão 2026-08-12 (segunda peça): T01-T03 encadeados com T04/T05
        # na mesma chamada, a partir do estado inicial OBRA_NAO_IDENTIFICADA.
        documento = documento_sintetico_com_referencia()
        referencia = documento.referencias[0]
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)

        arquivo = ArquivoDrive(id="x", nome="Grewe1979.pdf", mime_type="application/pdf",
                                tamanho_bytes=1, modificado_em=None)
        evidencia_id = EvidenciaDeIdentificacaoDrive(arquivo=arquivo, referencia_citada=referencia.texto)
        evidencia_acesso = EvidenciaDeAcessoDrive(arquivo=arquivo, operacao=OperacaoDeAcesso.LOCALIZADO)

        avancar(
            estado,
            EntradaEtapaP13(
                evidencias_de_identificacao={referencia.unit_id: evidencia_id},
                evidencias_de_acesso={referencia.unit_id: evidencia_acesso},
            ),
        )

        assert estado.historico[-1].tipo is TipoDeResultadoEtapa.EXECUTADA
        assert estado.contexto.estados_bibliograficos[referencia.unit_id] is EstadoBibliografico.ACESSIVEL

    def test_so_identificacao_sem_acesso_para_em_localizada(self):
        documento = documento_sintetico_com_referencia()
        referencia = documento.referencias[0]
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)

        arquivo = ArquivoDrive(id="x", nome="Grewe1979.pdf", mime_type="application/pdf",
                                tamanho_bytes=1, modificado_em=None)
        evidencia_id = EvidenciaDeIdentificacaoDrive(arquivo=arquivo, referencia_citada=referencia.texto)

        avancar(estado, EntradaEtapaP13(evidencias_de_identificacao={referencia.unit_id: evidencia_id}))

        assert estado.historico[-1].tipo is TipoDeResultadoEtapa.EXECUTADA
        assert estado.contexto.estados_bibliograficos[referencia.unit_id] is EstadoBibliografico.LOCALIZADA

    # --- Curador automático (sessão de 2026-08-13) ----------------------

    def test_com_servico_drive_e_sem_evidencia_pronta_curador_avanca_sozinho(self, monkeypatch):
        documento = documento_sintetico_com_referencia()
        referencia = documento.referencias[0]
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)

        arquivo = ArquivoDrive(id="x", nome="Grewe1979.pdf", mime_type="application/pdf",
                                tamanho_bytes=1, modificado_em=None)
        resultado_curador = SimpleNamespace(
            evidencias_de_identificacao={
                referencia.unit_id: EvidenciaDeIdentificacaoDrive(arquivo=arquivo, referencia_citada=referencia.texto)
            },
            evidencias_de_acesso={
                referencia.unit_id: EvidenciaDeAcessoDrive(arquivo=arquivo, operacao=OperacaoDeAcesso.LOCALIZADO)
            },
            escalonamentos=[],
        )
        monkeypatch.setattr(
            "escolio.funcoes.execucao_p13.curar_referencias", lambda referencias, servico: resultado_curador
        )

        avancar(estado, EntradaEtapaP13(servico_drive=object()))

        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.EXECUTADA
        assert estado.contexto.estados_bibliograficos[referencia.unit_id] is EstadoBibliografico.ACESSIVEL
        assert estado.contexto.escalonamentos_bibliograficos == []

    def test_curador_travado_em_todas_as_referencias_para_com_causa_estruturada(self, monkeypatch):
        documento = documento_sintetico_com_referencia()
        referencia = documento.referencias[0]
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)

        escalonamento = EscalonamentoDoCurador(
            unit_id=referencia.unit_id,
            motivo=GatilhoDeAbstencao.ACESSO_NAO_COMPROVADO,
            detalhe="nenhum arquivo encontrado no Drive para o termo de busca 'GREWE 1979'",
            referencia_texto=referencia.texto,
        )
        resultado_curador = SimpleNamespace(
            evidencias_de_identificacao={}, evidencias_de_acesso={}, escalonamentos=[escalonamento]
        )
        monkeypatch.setattr(
            "escolio.funcoes.execucao_p13.curar_referencias", lambda referencias, servico: resultado_curador
        )

        avancar(estado, EntradaEtapaP13(servico_drive=object()))

        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.PARADA
        assert ultimo.causa is CausaDeParada.ESCALONAMENTO_BIBLIOGRAFICO_NECESSARIO
        assert referencia.unit_id in ultimo.justificativa
        assert estado.contexto.escalonamentos_bibliograficos == [escalonamento]
        assert estado.concluidas == 10

    def test_curador_parcial_avanca_o_que_pode_e_registra_escalonamento_sem_bloquear(self, monkeypatch):
        documento = documento_sintetico_com_referencia()
        referencia = documento.referencias[0]
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)

        arquivo = ArquivoDrive(id="x", nome="Grewe1979.pdf", mime_type="application/pdf",
                                tamanho_bytes=1, modificado_em=None)
        escalonamento = EscalonamentoDoCurador(
            unit_id=referencia.unit_id,
            motivo=GatilhoDeAbstencao.ACESSO_NAO_COMPROVADO,
            detalhe="arquivo localizado, mas download/exportação falhou: erro simulado",
            referencia_texto=referencia.texto,
        )
        resultado_curador = SimpleNamespace(
            evidencias_de_identificacao={
                referencia.unit_id: EvidenciaDeIdentificacaoDrive(arquivo=arquivo, referencia_citada=referencia.texto)
            },
            evidencias_de_acesso={
                referencia.unit_id: EvidenciaDeAcessoDrive(arquivo=arquivo, operacao=OperacaoDeAcesso.LOCALIZADO)
            },
            escalonamentos=[escalonamento],
        )
        monkeypatch.setattr(
            "escolio.funcoes.execucao_p13.curar_referencias", lambda referencias, servico: resultado_curador
        )

        avancar(estado, EntradaEtapaP13(servico_drive=object()))

        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.EXECUTADA
        assert estado.contexto.estados_bibliograficos[referencia.unit_id] is EstadoBibliografico.ACESSIVEL
        assert estado.contexto.escalonamentos_bibliograficos == [escalonamento]

    def test_sem_servico_drive_curador_nao_e_acionado_comportamento_inalterado(self):
        documento = documento_sintetico_com_referencia()
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)

        avancar(estado, EntradaEtapaP13())  # sem evidência nem servico_drive

        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.PARADA
        assert ultimo.causa is CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO

    def test_evidencia_pronta_tem_prioridade_sobre_curador_mesmo_com_servico_drive(self, monkeypatch):
        documento = documento_sintetico_com_referencia()
        referencia = documento.referencias[0]
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)

        chamado = []
        monkeypatch.setattr(
            "escolio.funcoes.execucao_p13.curar_referencias",
            lambda referencias, servico: chamado.append(1) or SimpleNamespace(
                evidencias_de_identificacao={}, evidencias_de_acesso={}, escalonamentos=[]
            ),
        )
        arquivo = ArquivoDrive(id="x", nome="x.pdf", mime_type="application/pdf",
                                tamanho_bytes=1, modificado_em=None)
        evidencia = EvidenciaDeAcessoDrive(arquivo=arquivo, operacao=OperacaoDeAcesso.LOCALIZADO)
        estado.contexto.estados_bibliograficos[referencia.unit_id] = EstadoBibliografico.LOCALIZADA

        avancar(
            estado,
            EntradaEtapaP13(evidencias_de_acesso={referencia.unit_id: evidencia}, servico_drive=object()),
        )

        assert chamado == []
        assert estado.historico[-1].tipo is TipoDeResultadoEtapa.EXECUTADA


def _avancar_etapa_11_completa(estado, documento) -> None:
    """T01-T03+T04/T05 em uma única chamada, sobre a única referência de
    `documento_sintetico_com_referencia` — usado pelos testes das etapas
    12-15, que exigem `concluidas>=11` para serem alcançáveis."""
    referencia = documento.referencias[0]
    arquivo = ArquivoDrive(id="x", nome="Grewe1979.pdf", mime_type="application/pdf",
                            tamanho_bytes=1, modificado_em=None)
    avancar(
        estado,
        EntradaEtapaP13(
            evidencias_de_identificacao={
                referencia.unit_id: EvidenciaDeIdentificacaoDrive(arquivo=arquivo, referencia_citada=referencia.texto)
            },
            evidencias_de_acesso={
                referencia.unit_id: EvidenciaDeAcessoDrive(arquivo=arquivo, operacao=OperacaoDeAcesso.LOCALIZADO)
            },
        ),
    )
    assert estado.concluidas == 11


class TestEtapaDozeVerificacaoDeEvidencias:
    def _relacao(self, **overrides) -> RelacaoAfirmacaoEvidencia:
        campos = {
            "claim_id": "CLAIM-0001",
            "claim_text": "Afirmação sintética sobre o parágrafo.",
            "claim_type": ClaimType.FATUAL,
            "source_id": "SRC-0001",
            "source_type": SourceType.DOCUMENTO,
            "source_reference": "Fonte sintética",
            "location_type": LocationType.NAO_APLICAVEL,
            "evidence_level": EvidenceLevel.A_INTERNA_FORNECIDA,
            "access_state": AccessState.ACESSADA,
            "reading_state": ReadingState.LIDA_INTEGRALMENTE,
            "validation_state": ValidationState.VALIDADA,
            "sufficiency": Sufficiency.EVIDENCIA_SUFICIENTE,
            "confidence": Confidence.ALTA,
            "usage_status": UsageStatus.USO_LIBERADO,
            "provenance": "ingestão sintética de teste",
            "reversibility": Reversibility.NAO_APLICAVEL,
            "evidence_excerpt": "trecho sintético que sustenta a afirmação",
            "validator": "ENGENHEIRO_LLM",
            "validation_date": "2026-08-12",
        }
        campos.update(overrides)
        return RelacaoAfirmacaoEvidencia(**campos)

    def test_sem_relacoes_e_ponto_de_extensao(self):
        documento = documento_sintetico_com_referencia()
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)
        _avancar_etapa_11_completa(estado, documento)

        avancar(estado)  # 12, sem relacoes_afirmacao_evidencia
        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.PARADA
        assert ultimo.causa is CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO
        assert estado.concluidas == 11

    def test_lista_vazia_explicita_e_executada(self):
        documento = documento_sintetico_com_referencia()
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)
        _avancar_etapa_11_completa(estado, documento)

        avancar(estado, EntradaEtapaP13(relacoes_afirmacao_evidencia=[]))
        assert estado.historico[-1].tipo is TipoDeResultadoEtapa.EXECUTADA
        assert estado.contexto.relacoes_afirmacao_evidencia == []

    def test_relacao_fornecida_e_aceita(self):
        documento = documento_sintetico_com_referencia()
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)
        _avancar_etapa_11_completa(estado, documento)

        relacao = self._relacao()
        avancar(estado, EntradaEtapaP13(relacoes_afirmacao_evidencia=[relacao]))
        assert estado.historico[-1].tipo is TipoDeResultadoEtapa.EXECUTADA
        assert estado.contexto.relacoes_afirmacao_evidencia == [relacao]


def _perfil_de_voz_sintetico(**overrides) -> PerfilDeVoz:
    campos = {
        "profile_id": "PV-EXEC-0001",
        "profile_type": TipoDePerfil.PERFIL_NEUTRO_ACADEMICO_CONTROLADO,
        "purpose": "preservar a voz do autor avaliado na revisão",
        "scope": {"documento": "doc-exec-p13"},
        "dimensions": {},
        "evidence": [],
        "confidence": ConfidenceVoz.NAO_APLICAVEL,
        "authorization": {},
        "versioning": {"versao": 1},
        "provenance": [],
        "reversibility": {"reversivel": True},
        "status": StatusDePerfil.VALIDADO,
    }
    campos.update(overrides)
    return PerfilDeVoz(**campos)


class TestEtapaTrezeVerificacaoDeVoz:
    def test_sem_perfil_e_ponto_de_extensao(self):
        documento = documento_sintetico_com_referencia()
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)
        _avancar_etapa_11_completa(estado, documento)
        avancar(estado, EntradaEtapaP13(relacoes_afirmacao_evidencia=[]))  # 12
        assert estado.concluidas == 12

        avancar(estado)  # 13, sem perfil_de_voz
        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.PARADA
        assert ultimo.causa is CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO

    def test_perfil_sem_achados_nem_cliente_e_ponto_de_extensao(self):
        documento = documento_sintetico_com_referencia()
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)
        _avancar_etapa_11_completa(estado, documento)
        avancar(estado, EntradaEtapaP13(relacoes_afirmacao_evidencia=[]))  # 12

        avancar(estado, EntradaEtapaP13(perfil_de_voz=_perfil_de_voz_sintetico()))  # 13
        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.PARADA
        assert ultimo.causa is CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO

    def test_achados_prontos_produzem_avaliacao_conforme(self):
        documento = documento_sintetico_com_referencia()
        paragrafo = documento.paragrafos[0]
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)
        _avancar_etapa_11_completa(estado, documento)
        avancar(estado, EntradaEtapaP13(relacoes_afirmacao_evidencia=[]))  # 12

        achado = AchadoDeFidelidade(
            tipo=DesvioBloqueante.INVENCAO_FACTUAL, observado=False, evidencia="", confianca=ConfidenceVoz.ALTA
        )
        avancar(
            estado,
            EntradaEtapaP13(
                perfil_de_voz=_perfil_de_voz_sintetico(),
                achados_fidelidade={paragrafo.unit_id: [achado]},
            ),
        )
        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.EXECUTADA
        avaliacao = estado.contexto.avaliacoes_fidelidade[paragrafo.unit_id]
        assert avaliacao.resultado == ResultadoDeFidelidade.CONFORME

    def test_desvio_observado_produz_avaliacao_bloquear(self):
        documento = documento_sintetico_com_referencia()
        paragrafo = documento.paragrafos[0]
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)
        _avancar_etapa_11_completa(estado, documento)
        avancar(estado, EntradaEtapaP13(relacoes_afirmacao_evidencia=[]))  # 12

        achado = AchadoDeFidelidade(
            tipo=DesvioBloqueante.COPIA_OU_IMITACAO,
            observado=True,
            evidencia="trecho copiado de outro autor",
            confianca=ConfidenceVoz.ALTA,
        )
        avancar(
            estado,
            EntradaEtapaP13(
                perfil_de_voz=_perfil_de_voz_sintetico(),
                achados_fidelidade={paragrafo.unit_id: [achado]},
            ),
        )
        avaliacao = estado.contexto.avaliacoes_fidelidade[paragrafo.unit_id]
        assert avaliacao.resultado == ResultadoDeFidelidade.BLOQUEAR

    def test_unit_id_desconhecido_levanta(self):
        documento = documento_sintetico_com_referencia()
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)
        _avancar_etapa_11_completa(estado, documento)
        avancar(estado, EntradaEtapaP13(relacoes_afirmacao_evidencia=[]))  # 12

        with pytest.raises(ErroDeExecucaoP13):
            avancar(
                estado,
                EntradaEtapaP13(
                    perfil_de_voz=_perfil_de_voz_sintetico(),
                    achados_fidelidade={"UNI-PAR-INEXISTENTE": []},
                ),
            )

    def test_gera_achados_via_modelo_quando_cliente_fornecido(self):
        documento = documento_sintetico_com_referencia()
        paragrafo = documento.paragrafos[0]
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)
        _avancar_etapa_11_completa(estado, documento)
        avancar(estado, EntradaEtapaP13(relacoes_afirmacao_evidencia=[]))  # 12

        cliente = _cliente_fake(
            [
                {
                    "type": "tool_use",
                    "name": ponte._FERRAMENTA_DETECCAO_FIDELIDADE,
                    "input": {
                        "achados": [
                            {
                                "tipo": "INVENCAO_FACTUAL",
                                "observado": False,
                                "evidencia": "",
                                "confianca": "ALTA",
                                "notas": None,
                            }
                        ]
                    },
                }
            ]
        )
        avancar(
            estado,
            EntradaEtapaP13(
                perfil_de_voz=_perfil_de_voz_sintetico(),
                cliente=cliente,
                unidades_para_deteccao_fidelidade=[paragrafo.unit_id],
            ),
        )
        assert estado.historico[-1].tipo is TipoDeResultadoEtapa.EXECUTADA
        assert paragrafo.unit_id in estado.contexto.avaliacoes_fidelidade


class TestEtapaCatorzeVerificacaoDePrivacidade:
    """CO-012 resolvido — etapa sempre EXECUTADA, nunca gate
    [INSTRUCOES_COMPLEMENTARES_IMPLEMENTACAO_ECOSSISTEMA_REVISAO_LLM_R01.md §2]."""

    def _ate_etapa_13(self, documento):
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)
        _avancar_etapa_11_completa(estado, documento)
        avancar(estado, EntradaEtapaP13(relacoes_afirmacao_evidencia=[]))  # 12
        achado = AchadoDeFidelidade(
            tipo=DesvioBloqueante.INVENCAO_FACTUAL, observado=False, evidencia="", confianca=ConfidenceVoz.ALTA
        )
        avancar(
            estado,
            EntradaEtapaP13(
                perfil_de_voz=_perfil_de_voz_sintetico(),
                achados_fidelidade={documento.paragrafos[0].unit_id: [achado]},
            ),
        )  # 13
        assert estado.concluidas == 13
        return estado

    def test_sempre_executada_sem_entrada_alguma(self):
        documento = documento_sintetico_com_referencia()
        estado = self._ate_etapa_13(documento)

        avancar(estado)  # 14, sem EntradaEtapaP13 nenhuma além do default
        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.EXECUTADA
        assert estado.contexto.alertas_privacidade == []

    def test_tema_dificil_nao_produz_alerta(self):
        documento = documento_sintetico_com_referencia()
        documento.paragrafos[0].texto = "O relato descreve tortura e violência durante a repressão."
        estado = self._ate_etapa_13(documento)

        avancar(estado)  # 14
        assert estado.contexto.alertas_privacidade == []

    def test_cpf_no_texto_selecionado_produz_alerta_nao_bloqueante(self):
        documento = documento_sintetico_com_referencia()
        documento.paragrafos[0].texto = "Contato do informante: 123.456.789-01."
        estado = self._ate_etapa_13(documento)

        avancar(estado)  # 14
        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.EXECUTADA  # nunca bloqueia
        assert len(estado.contexto.alertas_privacidade) == 1
        assert isinstance(estado.contexto.alertas_privacidade[0], AlertaDePrivacidade)


class TestEtapaQuinzeProblemasSistemicos:
    def _ate_etapa_14(self, documento):
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)
        _avancar_etapa_11_completa(estado, documento)
        avancar(estado, EntradaEtapaP13(relacoes_afirmacao_evidencia=[]))  # 12
        achado = AchadoDeFidelidade(
            tipo=DesvioBloqueante.INVENCAO_FACTUAL, observado=False, evidencia="", confianca=ConfidenceVoz.ALTA
        )
        avancar(
            estado,
            EntradaEtapaP13(
                perfil_de_voz=_perfil_de_voz_sintetico(),
                achados_fidelidade={documento.paragrafos[0].unit_id: [achado]},
            ),
        )  # 13
        avancar(estado)  # 14
        assert estado.concluidas == 14
        return estado

    def test_sem_lista_e_entrada_nao_fornecida(self):
        documento = documento_sintetico_com_referencia()
        estado = self._ate_etapa_14(documento)

        avancar(estado)  # 15, sem problemas_sistemicos_conhecidos
        ultimo = estado.historico[-1]
        assert ultimo.tipo is TipoDeResultadoEtapa.PARADA
        assert ultimo.causa is CausaDeParada.ENTRADA_NAO_FORNECIDA

    def test_lista_vazia_explicita_e_executada(self):
        documento = documento_sintetico_com_referencia()
        estado = self._ate_etapa_14(documento)

        avancar(estado, EntradaEtapaP13(problemas_sistemicos_conhecidos=[]))
        assert estado.historico[-1].tipo is TipoDeResultadoEtapa.EXECUTADA
        assert estado.contexto.problemas_sistemicos_conhecidos == []

    def test_lista_real_e_registrada(self):
        documento = documento_sintetico_com_referencia()
        estado = self._ate_etapa_14(documento)

        avancar(
            estado,
            EntradaEtapaP13(problemas_sistemicos_conhecidos=["autor confunde datas juliano/gregoriano"]),
        )
        assert estado.historico[-1].tipo is TipoDeResultadoEtapa.EXECUTADA
        assert estado.contexto.problemas_sistemicos_conhecidos == ["autor confunde datas juliano/gregoriano"]
        assert estado.concluidas == 15

    def test_evidencia_sem_identificacao_previa_da_obra_levanta(self):
        """Estado inicial (OBRA_NAO_IDENTIFICADA) não licencia T04 — a
        evidência de Drive não comprova identificação de obra/edição
        (T01-T03), e este orquestrador não infere isso por conveniência."""
        documento = documento_sintetico_com_referencia()
        referencia = documento.referencias[0]
        estado = estado_roteado([item_declarado_para_f04()])
        _avancar_ate_selecao(estado, documento)

        arquivo = ArquivoDrive(id="x", nome="x.pdf", mime_type="application/pdf",
                                tamanho_bytes=1, modificado_em=None)
        evidencia = EvidenciaDeAcessoDrive(arquivo=arquivo, operacao=OperacaoDeAcesso.LOCALIZADO)

        with pytest.raises(ErroDeExecucaoP13) as excinfo:
            avancar(estado, EntradaEtapaP13(evidencias_de_acesso={referencia.unit_id: evidencia}))
        assert "P13-§26" in str(excinfo.value)
        assert estado.concluidas == 10


def _bloco_criticidade(problem_id="PROB-0001", unit_id="UNI-PAR-0001", classe="CRITICIDADE_MEDIA"):
    avaliacao = {eixo.value: f"avaliação {eixo.value}" for eixo in EixoCriticidade}
    return {
        "type": "tool_use",
        "name": ponte._FERRAMENTA_CRITICIDADE,
        "input": {
            "matrizes": [
                {
                    "problem_id": problem_id,
                    "unit_id": unit_id,
                    "avaliacao_por_eixo": avaliacao,
                    "classe": classe,
                    "justificativa_classe": "Síntese sintética.",
                }
            ]
        },
    }


def _bloco_seletividade(selection_id="SEL-0001", candidate_problem_id="PROB-0001"):
    return {
        "type": "tool_use",
        "name": ponte._FERRAMENTA_SELETIVIDADE,
        "input": {
            "matrizes": [
                {
                    "selection_id": selection_id,
                    "unit_id": "UNI-PAR-0001",
                    "candidate_problem_id": candidate_problem_id,
                    "criticality": "CRITICIDADE_MEDIA",
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


class TestEtapasLigadasAoModelo:
    """Sessão de 2026-08-09 — etapas 8 e 9 chamam a API via `cliente`
    (mockado) quando não recebem o objeto final já construído."""

    def _estado_ate_etapa_7(self, documento):
        estado = estado_roteado([item_declarado_para_f04()])
        avancar(estado)  # 1
        avancar(estado)  # 2
        avancar(estado, EntradaEtapaP13(dependencias_obrigatorias_confirmadas=True))  # 3
        avancar(estado, EntradaEtapaP13(documento=documento))  # 4
        avancar(estado, EntradaEtapaP13(document_version="1.0.0"))  # 5
        avancar(estado)  # 6
        avancar(estado)  # 7
        return estado

    def test_etapa_8_chama_modelo_quando_cliente_e_unidades_fornecidos(self):
        documento = documento_sintetico()
        estado = self._estado_ate_etapa_7(documento)
        cliente = _cliente_fake([_bloco_criticidade()])

        avancar(
            estado,
            EntradaEtapaP13(cliente=cliente, unidades_para_matriz_criticidade=["UNI-PAR-0001"]),
        )

        assert estado.concluidas == 8
        assert len(estado.contexto.matrizes_criticidade) == 1
        cliente.chamar.assert_called_once()

    def test_etapa_8_sem_cliente_continua_parando_como_antes(self):
        documento = documento_sintetico()
        estado = self._estado_ate_etapa_7(documento)

        avancar(estado, EntradaEtapaP13(unidades_para_matriz_criticidade=["UNI-PAR-0001"]))

        assert estado.concluidas == 7
        assert estado.historico[-1].causa is CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO

    def test_etapa_9_usa_matrizes_de_criticidade_da_etapa_8_como_candidatos(self):
        documento = documento_sintetico()
        estado = self._estado_ate_etapa_7(documento)
        cliente_criticidade = _cliente_fake([_bloco_criticidade()])
        avancar(
            estado,
            EntradaEtapaP13(cliente=cliente_criticidade, unidades_para_matriz_criticidade=["UNI-PAR-0001"]),
        )
        assert estado.concluidas == 8

        cliente_seletividade = _cliente_fake([_bloco_seletividade()])
        avancar(estado, EntradaEtapaP13(cliente=cliente_seletividade))

        assert estado.concluidas == 9
        assert len(estado.contexto.matrizes_seletividade) == 1
        _, kwargs = cliente_seletividade.chamar.call_args
        assert kwargs["model"] == ponte.MODEL_ETAPA_9
        assert kwargs["effort"] == ponte.EFFORT_ETAPA_9

    def test_etapa_16_elabora_comentario_matriz_a_partir_de_candidato_selecionado(self):
        documento = documento_sintetico()
        estado = self._estado_ate_etapa_7(documento)
        avancar(
            estado,
            EntradaEtapaP13(
                cliente=_cliente_fake([_bloco_criticidade()]),
                unidades_para_matriz_criticidade=["UNI-PAR-0001"],
            ),
        )
        avancar(estado, EntradaEtapaP13(cliente=_cliente_fake([_bloco_seletividade()])))
        avancar(estado)  # 10 — seleção determinística
        assert estado.concluidas == 10
        candidato = estado.contexto.selecionados[0]

        # Etapas 11-15 continuam ponto de extensão permanente nesta sessão
        # [LAC-FUNC-019] — simula que já foram concluídas, mesma técnica de
        # test_document_id_diverge_do_material_id_levanta_bl_022.
        from escolio.funcoes.execucao_p13 import ResultadoDeEtapa
        from escolio.funcoes.p13 import DECLARACAO as DECLARACAO_P13

        estado.historico.extend(
            ResultadoDeEtapa(etapa=DECLARACAO_P13.etapa(n), tipo=TipoDeResultadoEtapa.EXECUTADA, justificativa="simulado")
            for n in range(11, 16)
        )
        assert estado.concluidas == 15

        bloco = {
            "type": "tool_use",
            "name": ponte._FERRAMENTA_COMENTARIOS,
            "input": {
                "comentarios": [
                    {
                        "comment_id": "CMT-0001",
                        "selection_id": candidato.selection_id,
                        "unit_id": candidato.unit_id,
                        "anchor_start": "0",
                        "anchor_end": "10",
                        "anchor_text_hash": "sha256:x",
                        "comment_type": "COMENTARIO_MATRIZ",
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
                    }
                ]
            },
        }
        cliente = _cliente_fake([bloco])

        avancar(
            estado,
            EntradaEtapaP13(cliente=cliente, candidatos_para_comentario_matriz=[candidato]),
        )

        assert estado.concluidas == 16
        assert len(estado.contexto.todos_comentarios) == 1
        assert estado.contexto.todos_comentarios[0].status is P13CommentStatus.DRAFT

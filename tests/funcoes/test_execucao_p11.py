"""Testes do orquestrador de execução do P11 — primeira fatia real
(etapas 1-6).

Documento sintético, sem pdfplumber e sem chamada à API — mesmo padrão de
`tests/funcoes/test_execucao_p13.py`.
"""

from unittest.mock import MagicMock

import pytest

from escolio.contrato.afirmacao import ClaimEvidence
from escolio.contrato.entrada import Classification, InputItem, Provenance
from escolio.contrato.referencia import SemanticVersion
from escolio.contrato.requisicao import Authorization, ExpectedOutput, Request, Requester, Scope
from escolio.contrato.vocabulario import (
    AuthorizationStatus,
    ClaimStatus,
    ClaimType,
    Confidence,
    InputType,
    Sufficiency,
)
from escolio.funcoes import ponte_modelo_p11 as ponte
from escolio.funcoes import roteador
from escolio.funcoes.execucao_p11 import (
    CausaDeParada,
    EntradaEtapaP11,
    ErroDeExecucaoP11,
    TipoDeResultadoEtapa,
    avancar,
    construir_estado_inicial,
)
from escolio.funcoes.vocabulario import FuncaoId
from escolio.ingestao.modelos import DocumentoIngerido, Metadados, Paragrafo
from escolio.intervencao.niveis import NivelIntervencao


def documento_sintetico() -> DocumentoIngerido:
    return DocumentoIngerido(
        hash_documento="sinteticoexecp11001",
        caminho_original="synthetic://doc-execucao-p11-01",
        num_paginas=1,
        metadados=Metadados(titulo="Documento sintético — orquestrador P11"),
        paragrafos=[
            Paragrafo(
                unit_id="UNI-PAR-0001",
                texto="Parágrafo sintético usado para exercitar o orquestrador do P11.",
                pagina_inicio=1,
                pagina_fim=1,
                secao_id=None,
            )
        ],
    )


def item_declarado_para_f02() -> InputItem:
    return InputItem(
        input_id="INP-EXEC-P11-0001",
        type=InputType.DOCUMENT,
        provenance=Provenance(source="synthetic://doc", source_type="DOCUMENTO_PDF"),
        classification=Classification(trust="ORIGEM_DESCONHECIDA", functions=[FuncaoId.F02.value]),
    )


def requisicao_p11(inputs, **overrides) -> Request:
    campos = dict(
        schema_version=SemanticVersion(1, 0, 0),
        request_id="REQ-EXEC-P11-0001",
        project_id="PRJ-EXEC-P11-0001",
        component_id="P11",
        function_id=FuncaoId.F02.value,
        operation="DIAGNOSTICO_DE_ESTABILIDADE",
        requester=Requester(role="ENGENHEIRO_LLM", authority_basis="R03 §4.5"),
        scope=Scope(allowed_operations=["DIAGNOSTICO_DE_ESTABILIDADE"]),
        authorization=Authorization(status=AuthorizationStatus.UNVERIFIED),
        expected_output=ExpectedOutput(type="DIAGNOSTICO"),
        inputs=inputs,
    )
    campos.update(overrides)
    return Request(**campos)


def estado_roteado(inputs):
    request = requisicao_p11(inputs=inputs)
    decisao = roteador.rotear(request)
    return construir_estado_inicial(request, decisao)


def _avancar_ate_etapa_5(documento):
    estado = estado_roteado([item_declarado_para_f02()])
    avancar(estado)  # 1 intake
    avancar(estado, EntradaEtapaP11(nivel_intervencao_autorizado=NivelIntervencao.DIAGNOSTICO))  # 2
    avancar(estado, EntradaEtapaP11(dependencias_obrigatorias_confirmadas=True))  # 3
    avancar(estado, EntradaEtapaP11(documento=documento))  # 4
    avancar(estado)  # 5 cartografia global
    return estado


class TestEtapasMecanicas1a5:
    def test_avanca_ate_cartografia_global(self):
        documento = documento_sintetico()
        paragrafo = documento.paragrafos[0]
        estado = _avancar_ate_etapa_5(documento)

        assert estado.concluidas == 5
        assert estado.contexto.unidades_conhecidas == {paragrafo.unit_id}
        assert estado.contexto.cartografia["paragrafos"] == 1
        assert estado.contexto.nivel_intervencao_autorizado is NivelIntervencao.DIAGNOSTICO

    def test_material_nao_declarado_para_na_etapa_1(self):
        item_indeterminado = InputItem(
            input_id="INP-EXEC-P11-INDET",
            type=InputType.DOCUMENT,
            provenance=Provenance(source="synthetic://doc", source_type="DOCUMENTO_PDF"),
            classification=Classification(trust="ORIGEM_DESCONHECIDA"),
        )
        estado = estado_roteado([item_indeterminado])
        avancar(estado)
        assert estado.concluidas == 0
        assert estado.historico[-1].causa is CausaDeParada.MATERIAL_NAO_DECLARADO

    def test_etapa_2_sem_nivel_autorizado_para_e_nao_avanca(self):
        estado = estado_roteado([item_declarado_para_f02()])
        avancar(estado)  # 1
        avancar(estado)  # 2, sem nivel_intervencao_autorizado
        assert estado.concluidas == 1
        assert estado.historico[-1].causa is CausaDeParada.ENTRADA_NAO_FORNECIDA

        # Chamar de novo sem fornecer dado novo reoferece a MESMA etapa.
        avancar(estado)
        assert estado.concluidas == 1
        assert estado.historico[-1].etapa.ordem == 2

    def test_etapa_3_sem_dependencias_confirmadas_para(self):
        estado = estado_roteado([item_declarado_para_f02()])
        avancar(estado)
        avancar(estado, EntradaEtapaP11(nivel_intervencao_autorizado=NivelIntervencao.DIAGNOSTICO))
        avancar(estado)  # 3, sem confirmação
        assert estado.concluidas == 2
        assert estado.historico[-1].causa is CausaDeParada.ENTRADA_NAO_FORNECIDA


class TestEtapa6DiagnosticoDeEstabilidade:
    def test_sem_cliente_e_sem_diagnostico_para_como_ponto_de_extensao(self):
        documento = documento_sintetico()
        estado = _avancar_ate_etapa_5(documento)
        avancar(estado)  # 6, sem cliente nem diagnóstico
        assert estado.concluidas == 5
        assert estado.historico[-1].causa is CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO

    def test_diagnostico_fornecido_diretamente_e_aceito(self):
        documento = documento_sintetico()
        paragrafo = documento.paragrafos[0]
        estado = _avancar_ate_etapa_5(documento)
        achado = ClaimEvidence(
            claim_id="CLAIM-0001",
            claim_text="Objetivo e corpus coerentes ao longo da obra.",
            claim_type=ClaimType.INTERPRETATION,
            sufficiency=Sufficiency.SUFFICIENT,
            confidence=Confidence.HIGH,
            status=ClaimStatus.SUPPORTED,
            evidence_ids=[paragrafo.unit_id],
        )
        avancar(estado, EntradaEtapaP11(diagnostico_estabilidade=[achado]))
        assert estado.concluidas == 6
        assert estado.contexto.diagnostico_estabilidade == [achado]

    def test_diagnostico_com_unit_id_desconhecido_levanta_bl_022(self):
        documento = documento_sintetico()
        estado = _avancar_ate_etapa_5(documento)
        achado = ClaimEvidence(
            claim_id="CLAIM-0002",
            claim_text="Achado com evidência inexistente na obra.",
            claim_type=ClaimType.INTERPRETATION,
            sufficiency=Sufficiency.SUFFICIENT,
            confidence=Confidence.HIGH,
            status=ClaimStatus.SUPPORTED,
            evidence_ids=["UNI-PAR-9999"],
        )
        with pytest.raises(ErroDeExecucaoP11) as excinfo:
            avancar(estado, EntradaEtapaP11(diagnostico_estabilidade=[achado]))
        assert "BL-022" in str(excinfo.value)

    def test_etapa_6_chama_modelo_quando_cliente_fornecido(self):
        documento = documento_sintetico()
        paragrafo = documento.paragrafos[0]
        estado = _avancar_ate_etapa_5(documento)

        bloco = {
            "type": "tool_use",
            "name": ponte._FERRAMENTA_DIAGNOSTICO,
            "input": {
                "achados": [
                    {
                        "claim_id": "CLAIM-0003",
                        "claim_text": "Achado sintético gerado via modelo mockado.",
                        "claim_type": "INTERPRETATION",
                        "sufficiency": "SUFFICIENT",
                        "confidence": "MEDIUM",
                        "status": "SUPPORTED",
                        "evidence_ids": [paragrafo.unit_id],
                    }
                ]
            },
        }
        cliente = MagicMock()
        cliente.chamar.return_value = MagicMock(blocos=[bloco])

        avancar(estado, EntradaEtapaP11(cliente=cliente))

        assert estado.concluidas == 6
        assert len(estado.contexto.diagnostico_estabilidade) == 1
        cliente.chamar.assert_called_once()
        _, kwargs = cliente.chamar.call_args
        assert kwargs["model"] == ponte.MODEL_ETAPA_6
        assert kwargs["effort"] == ponte.EFFORT_ETAPA_6


class TestEtapasAlemDaFatiaDestaSessao:
    def test_etapa_7_e_ponto_de_extensao(self):
        documento = documento_sintetico()
        paragrafo = documento.paragrafos[0]
        estado = _avancar_ate_etapa_5(documento)
        achado = ClaimEvidence(
            claim_id="CLAIM-0004",
            claim_text="x",
            claim_type=ClaimType.INTERPRETATION,
            sufficiency=Sufficiency.SUFFICIENT,
            confidence=Confidence.HIGH,
            status=ClaimStatus.SUPPORTED,
            evidence_ids=[paragrafo.unit_id],
        )
        avancar(estado, EntradaEtapaP11(diagnostico_estabilidade=[achado]))
        assert estado.concluidas == 6

        avancar(estado)  # 7
        assert estado.concluidas == 6
        assert estado.historico[-1].causa is CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO

    def test_avancar_apos_fluxo_encerrado_levanta(self):
        from escolio.funcoes.execucao_p11 import ResultadoDeEtapa
        from escolio.funcoes.p11 import DECLARACAO as DECLARACAO_P11

        estado = estado_roteado([item_declarado_para_f02()])
        estado.historico.extend(
            ResultadoDeEtapa(etapa=etapa, tipo=TipoDeResultadoEtapa.EXECUTADA, justificativa="simulado")
            for etapa in DECLARACAO_P11.fluxo
        )
        assert estado.concluidas == 25
        assert estado.encerrado is True
        with pytest.raises(ErroDeExecucaoP11):
            avancar(estado)

    def test_etapas_23_a_25_sao_fora_do_fluxo(self):
        from escolio.funcoes.execucao_p11 import ResultadoDeEtapa
        from escolio.funcoes.p11 import DECLARACAO as DECLARACAO_P11

        estado = estado_roteado([item_declarado_para_f02()])
        estado.historico.extend(
            ResultadoDeEtapa(etapa=DECLARACAO_P11.etapa(n), tipo=TipoDeResultadoEtapa.EXECUTADA, justificativa="simulado")
            for n in range(1, 23)
        )
        assert estado.concluidas == 22

        avancar(estado)  # 23
        assert estado.historico[-1].causa is CausaDeParada.FORA_DO_FLUXO_DE_EXECUCAO
        assert estado.concluidas == 22

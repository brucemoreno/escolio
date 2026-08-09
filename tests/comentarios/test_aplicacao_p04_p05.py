"""Sessão 4 do plano P13 — integração P04 (BVAA)/P05 no comentário.

Testes PS13-05, PS13-06 [§45] e TA13-10, TA13-11 [§46], mais cobertura de
regra de §19/§26/§27 que os quatro cenários narrativos exercitam.
"""

import pytest

from escolio.bvaa.vocabulario import EstadoBibliografico
from escolio.comentarios.aplicacao_p04_p05 import (
    AplicacaoP05DoComentario,
    SourceStatusComentario,
    aplicar_bibliografia_e_evidencia,
    construir_aplicacao_p05,
    valida_source_status_compativel_com_bvaa,
)
from escolio.comentarios.erros import ErroDeComentario
from escolio.relacao import RelacaoAfirmacaoEvidencia
from escolio.vocabulario import (
    AccessState,
    ClaimType,
    Confidence,
    EvidenceLevel,
    LocationType,
    NAO_DISPONIVEL,
    ReadingState,
    Reversibility,
    SourceType,
    Sufficiency,
    UsageStatus,
    ValidationState,
)
from tests.comentarios.fixtures import comentario_base

EB = EstadoBibliografico


def relacao_base(**overrides):
    campos = dict(
        claim_id="CLM-HIST-0001",
        claim_text="A cidade foi fundada em 1500.",
        claim_type=ClaimType.FATUAL,
        source_id="SRC-DOCUMENTO-0001",
        source_type=SourceType.DOCUMENTO,
        source_reference="Registro documental verificável X",
        location_type=LocationType.PAGINA,
        evidence_level=EvidenceLevel.B_MATERIAL_ANEXADA,
        access_state=AccessState.ACESSADA,
        reading_state=ReadingState.LIDA_PARCIALMENTE,
        validation_state=ValidationState.PAGINA_CONFIRMADA,
        sufficiency=Sufficiency.EVIDENCIA_SUFICIENTE,
        confidence=Confidence.MEDIA,
        usage_status=UsageStatus.USO_CONDICIONAL,
        provenance="Origem: arquivo municipal; método: digitalização; versão 1",
        reversibility=Reversibility.REVERSIVEL_COM_NOVA_EVIDENCIA,
        location_value="p. 12",
        evidence_excerpt="trecho fiel citado",
        notes="Leitura limitada às páginas 10-15",
    )
    campos.update(overrides)
    return RelacaoAfirmacaoEvidencia(**campos)


class TestValidaSourceStatusCompativelComBvaa:
    """§19, §26 — o comentário não pode afirmar mais do que o BVAA sustenta."""

    def test_pagina_confirmada_exige_acesso_comprovado(self):
        with pytest.raises(ErroDeComentario):
            valida_source_status_compativel_com_bvaa(
                SourceStatusComentario.PAGINA_CONFIRMADA, EB.LOCALIZADA
            )

    def test_fonte_localizada_nao_exige_acesso(self):
        # Não levanta: FONTE_LOCALIZADA é exatamente o que resta quando
        # a fonte só foi localizada, nunca aberta.
        valida_source_status_compativel_com_bvaa(SourceStatusComentario.FONTE_LOCALIZADA, EB.LOCALIZADA)

    def test_leitura_parcial_liberada_apos_acesso(self):
        valida_source_status_compativel_com_bvaa(SourceStatusComentario.LEITURA_PARCIAL, EB.ACESSADA)

    def test_sustentacao_especifica_exige_validada_ou_recomendada(self):
        with pytest.raises(ErroDeComentario):
            valida_source_status_compativel_com_bvaa(
                SourceStatusComentario.SUSTENTACAO_ESPECIFICA_LIBERADA, EB.PAGINA_CONFIRMADA
            )
        valida_source_status_compativel_com_bvaa(
            SourceStatusComentario.SUSTENTACAO_ESPECIFICA_LIBERADA, EB.VALIDADA
        )

    def test_abstencao_bibliografica_nao_conta_como_acesso_comprovado(self):
        with pytest.raises(ErroDeComentario):
            valida_source_status_compativel_com_bvaa(
                SourceStatusComentario.PAGINA_CONFIRMADA, EB.ABSTENCAO_BIBLIOGRAFICA
            )

    def test_status_invalido_rejeitado(self):
        with pytest.raises(ErroDeComentario):
            valida_source_status_compativel_com_bvaa("CONFIRMADA", EB.VALIDADA)


class TestConstruirAplicacaoP05:
    """§20, §27 — schema mínimo distinto de P13Comment."""

    def test_sem_relacao_representa_claim_sem_evidencia(self):
        aplicacao = construir_aplicacao_p05("CMT-0001", "CLM-HIST-0001", None)
        assert aplicacao.evidence_ids == ()
        assert aplicacao.sufficiency is Sufficiency.EVIDENCIA_AUSENTE
        assert aplicacao.confidence is Confidence.NAO_AVALIADA
        assert aplicacao.verification_status is ValidationState.NAO_VERIFICADA
        assert aplicacao.limitations == NAO_DISPONIVEL

    def test_com_relacao_reusa_campos_de_p05(self):
        relacao = relacao_base()
        aplicacao = construir_aplicacao_p05("CMT-0001", relacao.claim_id, relacao)
        assert aplicacao.evidence_ids == (relacao.source_id,)
        assert aplicacao.sufficiency is relacao.sufficiency
        assert aplicacao.confidence is relacao.confidence
        assert aplicacao.verification_status is relacao.validation_state
        assert aplicacao.limitations == relacao.notes

    def test_relacao_sem_notes_usa_nao_disponivel(self):
        relacao = relacao_base(reading_state=ReadingState.LIDA_INTEGRALMENTE, notes=None)
        aplicacao = construir_aplicacao_p05("CMT-0001", relacao.claim_id, relacao)
        assert aplicacao.limitations == NAO_DISPONIVEL

    def test_claim_id_divergente_da_relacao_e_rejeitado(self):
        relacao = relacao_base(claim_id="CLM-HIST-0001")
        with pytest.raises(ErroDeComentario):
            construir_aplicacao_p05("CMT-0001", "CLM-OUTRA-0002", relacao)

    def test_claim_id_vazio_rejeitado(self):
        with pytest.raises(ErroDeComentario):
            AplicacaoP05DoComentario(
                claim_id="",
                comment_id="CMT-0001",
                evidence_ids=(),
                verification_status=ValidationState.NAO_VERIFICADA,
                sufficiency=Sufficiency.EVIDENCIA_AUSENTE,
                confidence=Confidence.NAO_AVALIADA,
                limitations=NAO_DISPONIVEL,
            )


class TestAplicarBibliografiaEEvidencia:
    """Adaptador de sessão 4: popula source_status no comentário e produz
    o schema mínimo de §27 ao mesmo tempo."""

    def test_atualiza_source_status_preservando_demais_campos(self):
        comentario = comentario_base(source_status="PENDENTE")
        atualizado, aplicacao = aplicar_bibliografia_e_evidencia(
            comentario,
            source_status=SourceStatusComentario.FONTE_LOCALIZADA,
            estado_bvaa=EB.LOCALIZADA,
            claim_id="CLM-HIST-0001",
        )
        assert atualizado.source_status == SourceStatusComentario.FONTE_LOCALIZADA.value
        assert atualizado.comment_id == comentario.comment_id
        assert aplicacao.comment_id == comentario.comment_id
        assert aplicacao.claim_id == "CLM-HIST-0001"

    def test_nao_grava_quando_validacao_falha(self):
        comentario = comentario_base(source_status="PENDENTE")
        with pytest.raises(ErroDeComentario):
            aplicar_bibliografia_e_evidencia(
                comentario,
                source_status=SourceStatusComentario.PAGINA_CONFIRMADA,
                estado_bvaa=EB.LOCALIZADA,
                claim_id="CLM-HIST-0001",
            )
        # comentário original não é alterado — dataclasses.replace só é
        # alcançado depois da validação.
        assert comentario.source_status == "PENDENTE"


class TestPS13_05_CitacaoSemPaginaConfirmada:
    """[§45] Citação específica sem página confirmada — validar a citação
    é recusado; o comentário registra pendência bibliográfica, não a
    confirmação de página."""

    def test_declarar_pagina_confirmada_sem_confirmacao_e_recusado(self):
        comentario = comentario_base(source_status="PENDENTE")
        with pytest.raises(ErroDeComentario):
            aplicar_bibliografia_e_evidencia(
                comentario,
                source_status=SourceStatusComentario.PAGINA_CONFIRMADA,
                estado_bvaa=EB.LEITURA_PARCIAL,
                claim_id="CLM-HIST-0001",
            )

    def test_alerta_de_pendencia_e_aceito(self):
        comentario = comentario_base(source_status="PENDENTE")
        atualizado, _ = aplicar_bibliografia_e_evidencia(
            comentario,
            source_status=SourceStatusComentario.SUSTENTACAO_NAO_LIBERADA,
            estado_bvaa=EB.LEITURA_PARCIAL,
            claim_id="CLM-HIST-0001",
        )
        assert atualizado.source_status == SourceStatusComentario.SUSTENTACAO_NAO_LIBERADA.value


class TestPS13_06_FonteLocalizadaMasNaoAberta:
    """[§45] Fonte localizada, mas não aberta — declarar que a fonte
    confirma a afirmação é recusado; só a pendência é registrável."""

    def test_declarar_confirmacao_sem_fonte_aberta_e_recusado(self):
        comentario = comentario_base(source_status="PENDENTE")
        with pytest.raises(ErroDeComentario):
            aplicar_bibliografia_e_evidencia(
                comentario,
                source_status=SourceStatusComentario.PAGINA_CONFIRMADA,
                estado_bvaa=EB.LOCALIZADA,
                claim_id="CLM-HIST-0001",
            )

    def test_registrar_pendencia_de_fonte_localizada_e_aceito(self):
        comentario = comentario_base(source_status="PENDENTE")
        atualizado, _ = aplicar_bibliografia_e_evidencia(
            comentario,
            source_status=SourceStatusComentario.FONTE_LOCALIZADA,
            estado_bvaa=EB.LOCALIZADA,
            claim_id="CLM-HIST-0001",
        )
        assert atualizado.source_status == SourceStatusComentario.FONTE_LOCALIZADA.value


class TestTA13_10_ComentarioBibliografico:
    """[§46] Objeto: fonte não aberta. Critério de aprovação: status de
    fonte registrado. Critério de falha: validação falsa."""

    def test_status_de_fonte_e_registrado_sem_declarar_conferencia(self):
        comentario = comentario_base(source_status="PENDENTE")
        atualizado, _ = aplicar_bibliografia_e_evidencia(
            comentario,
            source_status=SourceStatusComentario.FONTE_LOCALIZADA,
            estado_bvaa=EB.LOCALIZADA,
            claim_id="CLM-HIST-0001",
        )
        assert atualizado.source_status == SourceStatusComentario.FONTE_LOCALIZADA.value

    def test_validacao_falsa_e_rejeitada(self):
        comentario = comentario_base(source_status="PENDENTE")
        with pytest.raises(ErroDeComentario):
            aplicar_bibliografia_e_evidencia(
                comentario,
                source_status=SourceStatusComentario.PAGINA_CONFIRMADA,
                estado_bvaa=EB.LOCALIZADA,
                claim_id="CLM-HIST-0001",
            )


class TestTA13_11_ComentarioDeEvidencia:
    """[§46] Objeto: claim sem suporte. Critério de aprovação: insuficiência
    distinguida de falsidade. Critério de falha: acusação sem base."""

    def test_insuficiencia_distinguida_de_falsidade(self):
        aplicacao = construir_aplicacao_p05("CMT-0001", "CLM-HIST-0001", None)
        # A ausência de evidência é representada pelo valor de P05 já
        # existente para esta condição — não por um rótulo de "falso".
        assert aplicacao.sufficiency is Sufficiency.EVIDENCIA_AUSENTE
        assert aplicacao.sufficiency is not Sufficiency.CONFLITANTE

    def test_alerta_de_evidencia_nao_acusa_sem_base(self):
        aplicacao = construir_aplicacao_p05("CMT-0001", "CLM-HIST-0001", None)
        # Nenhum evidence_id é fabricado quando não há evidência vinculada.
        assert aplicacao.evidence_ids == ()

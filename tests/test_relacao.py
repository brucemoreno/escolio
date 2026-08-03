import pytest

from escolio.erros import ErroDeCoerencia
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
        edition_or_version="1a edicao",
        page_or_folio="NAO_APLICAVEL",
        location_value="p. 12",
        evidence_excerpt="trecho fiel citado",
        notes="Leitura limitada às páginas 10-15",
    )
    campos.update(overrides)
    return RelacaoAfirmacaoEvidencia(**campos)


class TestRegistroValido:
    def test_registro_valido_minimo_sem_condicionais(self):
        r = RelacaoAfirmacaoEvidencia(
            claim_id="CLM-GEN-0001",
            claim_text="Texto da afirmação.",
            claim_type=ClaimType.FATUAL,
            source_id="SRC-WEB-0001",
            source_type=SourceType.WEB,
            source_reference="URL verificável",
            location_type=LocationType.NAO_APLICAVEL,
            evidence_level=EvidenceLevel.D_AUSENTE,
            access_state=AccessState.NAO_LOCALIZADA,
            reading_state=ReadingState.LEITURA_NAO_REALIZADA,
            validation_state=ValidationState.NAO_VERIFICADA,
            sufficiency=Sufficiency.EVIDENCIA_AUSENTE,
            confidence=Confidence.NAO_AVALIADA,
            usage_status=UsageStatus.ABSTENCAO,
            provenance="Origem: nenhuma evidência localizada ainda",
            reversibility=Reversibility.NAO_APLICAVEL,
        )
        assert r.claim_id == "CLM-GEN-0001"

    def test_registro_valido_completo(self):
        r = relacao_base()
        assert r.relation_version == 1


class TestCamposObrigatorios:
    def test_claim_id_vazio_rejeita(self):
        with pytest.raises(ErroDeCoerencia):
            relacao_base(claim_id="")

    def test_claim_text_vazio_rejeita(self):
        with pytest.raises(ErroDeCoerencia):
            relacao_base(claim_text="")

    def test_source_id_vazio_rejeita(self):
        with pytest.raises(ErroDeCoerencia):
            relacao_base(source_id="")

    def test_source_reference_vazio_rejeita(self):
        with pytest.raises(ErroDeCoerencia):
            relacao_base(source_reference="   ")

    def test_provenance_vazio_rejeita(self):
        with pytest.raises(ErroDeCoerencia):
            relacao_base(provenance="")

    def test_claim_type_outra_controlada_exige_notes(self):
        with pytest.raises(ErroDeCoerencia):
            relacao_base(claim_type=ClaimType.OUTRA_CONTROLADA, notes=None)

    def test_pagina_confirmada_exige_location_value(self):
        with pytest.raises(ErroDeCoerencia):
            relacao_base(validation_state=ValidationState.PAGINA_CONFIRMADA, location_value=None)

    def test_validada_exige_validator_e_data(self):
        with pytest.raises(ErroDeCoerencia):
            relacao_base(
                validation_state=ValidationState.VALIDADA,
                validator=None,
                validation_date=None,
                usage_status=UsageStatus.USO_LIBERADO,
            )


class TestVocabularioControlado:
    def test_valor_fora_do_vocabulario_rejeitado_pelo_enum(self):
        with pytest.raises(ValueError):
            ClaimType("INVENTADO")

    def test_access_state_fora_do_vocabulario(self):
        with pytest.raises(ValueError):
            AccessState("QUASE_ACESSADA")

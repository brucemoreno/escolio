import pytest

from escolio.erros import ErroDeCoerencia
from escolio.relacao import RelacaoAfirmacaoEvidencia
from escolio.regras_coerencia import rc_012, rc_013, rc_014, rc_019, rc_020
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
from tests.test_relacao import relacao_base


class TestRC001AcessoExigeAbertura:
    def test_violacao(self):
        with pytest.raises(ErroDeCoerencia, match="RC-001"):
            relacao_base(access_state=AccessState.ACESSADA, evidence_level=EvidenceLevel.D_AUSENTE)

    def test_conforme(self):
        relacao_base(access_state=AccessState.ACESSADA, evidence_level=EvidenceLevel.B_MATERIAL_ANEXADA)


class TestRC002LeituraParcialExigeLimites:
    def test_violacao(self):
        with pytest.raises(ErroDeCoerencia, match="RC-002"):
            relacao_base(reading_state=ReadingState.LIDA_PARCIALMENTE, notes=None)

    def test_conforme(self):
        relacao_base(reading_state=ReadingState.LIDA_PARCIALMENTE, notes="limites: p. 10-15")


class TestRC003LeituraIntegralExigeAcesso:
    def test_violacao(self):
        with pytest.raises(ErroDeCoerencia, match="RC-003"):
            relacao_base(reading_state=ReadingState.LIDA_INTEGRALMENTE, access_state=AccessState.LOCALIZADA)

    def test_conforme(self):
        relacao_base(reading_state=ReadingState.LIDA_INTEGRALMENTE, access_state=AccessState.ACESSADA)


class TestRC004PaginaExigeEdicaoEConfirmacao:
    def test_violacao_sem_edicao(self):
        with pytest.raises(ErroDeCoerencia, match="RC-004"):
            relacao_base(page_or_folio="p. 12", edition_or_version="NAO_CONFIRMADO")

    def test_violacao_sem_confirmacao(self):
        with pytest.raises(ErroDeCoerencia, match="RC-004"):
            relacao_base(page_or_folio="p. 12", validation_state=ValidationState.NAO_VERIFICADA)

    def test_conforme(self):
        relacao_base(
            page_or_folio="p. 12",
            edition_or_version="1a edicao",
            validation_state=ValidationState.PAGINA_CONFIRMADA,
        )


class TestRC005ValidadaExigeValidatorEData:
    def test_violacao_sem_validator(self):
        with pytest.raises(ErroDeCoerencia):
            relacao_base(
                validation_state=ValidationState.VALIDADA,
                validator=None,
                validation_date=None,
            )

    def test_violacao_suficiencia_nao_avaliada(self):
        with pytest.raises(ErroDeCoerencia, match="RC-005"):
            relacao_base(
                validation_state=ValidationState.VALIDADA,
                validator="EXECUTOR_DOCUMENTAL",
                validation_date="2026-01-01",
                sufficiency=Sufficiency.NAO_AVALIADA,
            )

    def test_conforme(self):
        relacao_base(
            validation_state=ValidationState.VALIDADA,
            validator="EXECUTOR_DOCUMENTAL",
            validation_date="2026-01-01",
            sufficiency=Sufficiency.EVIDENCIA_SUFICIENTE,
        )


class TestRC006SuficienteExigeCorrespondencia:
    def test_violacao(self):
        with pytest.raises(ErroDeCoerencia, match="RC-006"):
            relacao_base(sufficiency=Sufficiency.EVIDENCIA_SUFICIENTE, evidence_excerpt="NAO_DISPONIVEL")

    def test_conforme(self):
        relacao_base(sufficiency=Sufficiency.EVIDENCIA_SUFICIENTE, evidence_excerpt="trecho fiel")


class TestRC007AltaIncompativelComAusente:
    def test_violacao(self):
        with pytest.raises(ErroDeCoerencia, match="RC-007"):
            relacao_base(confidence=Confidence.ALTA, sufficiency=Sufficiency.EVIDENCIA_AUSENTE)

    def test_conforme(self):
        relacao_base(confidence=Confidence.BAIXA, sufficiency=Sufficiency.EVIDENCIA_AUSENTE)


class TestRC008AltaComInsuficienteNaoLibera:
    def test_violacao(self):
        with pytest.raises(ErroDeCoerencia, match="RC-008"):
            relacao_base(
                confidence=Confidence.ALTA,
                sufficiency=Sufficiency.EVIDENCIA_INSUFICIENTE,
                usage_status=UsageStatus.USO_LIBERADO,
                validation_state=ValidationState.VALIDADA,
                validator="X",
                validation_date="2026-01-01",
            )

    def test_conforme_condicional(self):
        relacao_base(
            confidence=Confidence.ALTA,
            sufficiency=Sufficiency.EVIDENCIA_INSUFICIENTE,
            usage_status=UsageStatus.USO_CONDICIONAL,
        )


class TestRC009LiberadoExigeValidadaESuficiente:
    def test_violacao(self):
        with pytest.raises(ErroDeCoerencia, match="RC-009"):
            relacao_base(
                usage_status=UsageStatus.USO_LIBERADO,
                validation_state=ValidationState.VALIDACAO_PENDENTE,
            )

    def test_conforme(self):
        relacao_base(
            usage_status=UsageStatus.USO_LIBERADO,
            validation_state=ValidationState.VALIDADA,
            validator="X",
            validation_date="2026-01-01",
            sufficiency=Sufficiency.EVIDENCIA_SUFICIENTE,
        )


class TestRC010LeituraIndiretaExigeFonteIntermediaria:
    def test_violacao(self):
        with pytest.raises(ErroDeCoerencia, match="RC-010"):
            relacao_base(reading_state=ReadingState.LEITURA_INDIRETA, provenance="Origem: arquivo X; versão 1")

    def test_conforme(self):
        relacao_base(
            reading_state=ReadingState.LEITURA_INDIRETA,
            provenance="Origem: citação via fonte intermediaria Y; versão 1",
        )


class TestRC011AusenteIncompativelComValidada:
    def test_violacao(self):
        with pytest.raises(ErroDeCoerencia, match="RC-011"):
            relacao_base(
                access_state=AccessState.LOCALIZADA,
                reading_state=ReadingState.LEITURA_NAO_REALIZADA,
                evidence_level=EvidenceLevel.D_AUSENTE,
                validation_state=ValidationState.VALIDADA,
                validator="X",
                validation_date="2026-01-01",
            )

    def test_conforme(self):
        relacao_base(evidence_level=EvidenceLevel.B_MATERIAL_ANEXADA, validation_state=ValidationState.VALIDADA,
                      validator="X", validation_date="2026-01-01")


class TestRC012ConflitanteExigeSufficiencyConflitante:
    def test_violacao(self):
        r = relacao_base(sufficiency=Sufficiency.EVIDENCIA_SUFICIENTE)
        with pytest.raises(ErroDeCoerencia, match="RC-012"):
            rc_012(r, ha_conflito=True)

    def test_conforme(self):
        r = relacao_base(sufficiency=Sufficiency.CONFLITANTE, usage_status=UsageStatus.USO_CONDICIONAL,
                          validation_state=ValidationState.VALIDACAO_PENDENTE)
        rc_012(r, ha_conflito=True)


class TestRC013EdicaoDivergenteNaoCompartilhaPaginacao:
    def test_violacao(self):
        r = relacao_base(edition_or_version="2a edicao")
        with pytest.raises(ErroDeCoerencia, match="RC-013"):
            rc_013(r, edicao_da_pagina_confirmada="1a edicao")

    def test_conforme_mesma_edicao(self):
        r = relacao_base(edition_or_version="1a edicao")
        rc_013(r, edicao_da_pagina_confirmada="1a edicao")


class TestRC014SubstituicaoExigeReferenciaPredecessora:
    def test_violacao(self):
        with pytest.raises(ErroDeCoerencia, match="RC-014"):
            rc_014(notes=None, eh_substituicao=True)

    def test_conforme(self):
        rc_014(notes="supersedes_relation_version=1", eh_substituicao=True)


class TestRC015InvalidadaIncompativelComLiberado:
    def test_violacao(self):
        # Construído com relacao_base(), RC-009 já bloqueia este caso
        # (USO_LIBERADO exige VALIDADA). RC-015 é testada isoladamente
        # via rc_015() para confirmar que a regra em si distingue o caso
        # de INVALIDADA_POSTERIORMENTE + USO_LIBERADO.
        from escolio.regras_coerencia import rc_015

        r = relacao_base(
            validation_state=ValidationState.INVALIDADA_POSTERIORMENTE,
            usage_status=UsageStatus.NAO_USAR,
            validator="X",
            validation_date="2026-01-01",
        )
        r.usage_status = UsageStatus.USO_LIBERADO
        with pytest.raises(ErroDeCoerencia, match="RC-015"):
            rc_015(r)

    def test_conforme(self):
        relacao_base(
            validation_state=ValidationState.INVALIDADA_POSTERIORMENTE,
            usage_status=UsageStatus.NAO_USAR,
            validator="X",
            validation_date="2026-01-01",
        )


class TestRC019PedidoParaInventar:
    def test_deteccao(self):
        (deve_abster,) = rc_019("Por favor, invente uma página que sustente essa citação.")
        assert deve_abster is True

    def test_pedido_legitimo_nao_aciona(self):
        (deve_abster,) = rc_019("Verifique a página 12 do documento original.")
        assert deve_abster is False


class TestRC020FonteParcialNaoSustentaAlemDoSegmento:
    def test_violacao(self):
        r = relacao_base()
        with pytest.raises(ErroDeCoerencia, match="RC-020"):
            rc_020(r, fonte_parcial=True, alegacao_alem_do_segmento=True)

    def test_conforme(self):
        r = relacao_base()
        rc_020(r, fonte_parcial=True, alegacao_alem_do_segmento=False)

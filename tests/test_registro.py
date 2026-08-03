import pytest

from escolio.erros import ErroDeCoerencia, ErroDeIdentificador
from escolio.registro import RegistroDeRelacoes
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


def test_uma_afirmacao_com_duas_evidencias_mantem_relacoes_separadas():
    """Cenário 07 do arquivo 09: uma afirmação, duas evidências, duas
    relações independentes (RC-018)."""
    reg = RegistroDeRelacoes()
    r1 = relacao_base(claim_id="CLM-HIST-0001", source_id="SRC-DOCUMENTO-0001")
    r2 = relacao_base(claim_id="CLM-HIST-0001", source_id="SRC-DOCUMENTO-0002")
    reg.adicionar(r1)
    reg.adicionar(r2)
    relacoes = reg.relacoes_por_claim("CLM-HIST-0001")
    assert len(relacoes) == 2
    assert {r.source_id for r in relacoes} == {"SRC-DOCUMENTO-0001", "SRC-DOCUMENTO-0002"}


def test_uma_evidencia_usada_por_duas_afirmacoes_mantem_mesmo_source_id():
    """Cenário 08 do arquivo 09 (RC-017)."""
    reg = RegistroDeRelacoes()
    r1 = relacao_base(claim_id="CLM-HIST-0001", source_id="SRC-DOCUMENTO-0001")
    r2 = relacao_base(claim_id="CLM-HIST-0002", source_id="SRC-DOCUMENTO-0001")
    reg.adicionar(r1)
    reg.adicionar(r2)
    relacoes = reg.relacoes_por_source("SRC-DOCUMENTO-0001")
    assert len(relacoes) == 2
    assert {r.claim_id for r in relacoes} == {"CLM-HIST-0001", "CLM-HIST-0002"}


def test_rastreabilidade_afirmacao_para_evidencia():
    """Cenário 13 do arquivo 09."""
    reg = RegistroDeRelacoes()
    reg.adicionar(relacao_base(claim_id="CLM-HIST-0001", source_id="SRC-DOCUMENTO-0001"))
    relacoes = reg.relacoes_por_claim("CLM-HIST-0001")
    assert relacoes[0].source_id == "SRC-DOCUMENTO-0001"


def test_rastreabilidade_evidencia_para_afirmacoes():
    """Cenário 14 do arquivo 09."""
    reg = RegistroDeRelacoes()
    reg.adicionar(relacao_base(claim_id="CLM-HIST-0001", source_id="SRC-DOCUMENTO-0001"))
    relacoes = reg.relacoes_por_source("SRC-DOCUMENTO-0001")
    assert relacoes[0].claim_id == "CLM-HIST-0001"


def test_reciclagem_de_claim_id_com_dados_diferentes_e_rejeitada():
    """RC-016 aplicado através do registro: mesmo claim_id não pode ser
    reaproveitado para uma afirmação diferente depois de invalidado."""
    reg = RegistroDeRelacoes()
    reg.adicionar(relacao_base(claim_id="CLM-HIST-0001", source_id="SRC-DOCUMENTO-0001"))
    reg.identificadores.invalidar_claim_id("CLM-HIST-0001")
    with pytest.raises(ErroDeIdentificador):
        reg.adicionar(relacao_base(claim_id="CLM-HIST-0001", source_id="SRC-DOCUMENTO-0002"))


def test_edicao_divergente_nao_herda_pagina_confirmada():
    """Cenário 10 do arquivo 09 (RC-013), via RegistroDeRelacoes."""
    reg = RegistroDeRelacoes()
    reg.adicionar(
        relacao_base(
            claim_id="CLM-HIST-0001",
            source_id="SRC-DOCUMENTO-0001",
            edition_or_version="1a edicao",
            validation_state=ValidationState.PAGINA_CONFIRMADA,
        )
    )
    with pytest.raises(ErroDeCoerencia, match="RC-013"):
        reg.adicionar(
            relacao_base(
                claim_id="CLM-HIST-0001",
                source_id="SRC-DOCUMENTO-0001",
                edition_or_version="2a edicao",
                validation_state=ValidationState.PAGINA_CONFIRMADA,
                relation_version=2,
                notes="supersedes_relation_version=1",
            )
        )


def test_conflito_exige_sufficiency_conflitante():
    """Cenário 09 do arquivo 09 (RC-012)."""
    reg = RegistroDeRelacoes()
    reg.adicionar(
        relacao_base(
            claim_id="CLM-HIST-0001",
            source_id="SRC-DOCUMENTO-0001",
            sufficiency=Sufficiency.EVIDENCIA_SUFICIENTE,
        )
    )
    with pytest.raises(ErroDeCoerencia, match="RC-012"):
        reg.marcar_conflito("CLM-HIST-0001", ["SRC-DOCUMENTO-0001"])


def test_conflito_aceita_quando_ja_marcado_conflitante():
    reg = RegistroDeRelacoes()
    reg.adicionar(
        relacao_base(
            claim_id="CLM-HIST-0001",
            source_id="SRC-DOCUMENTO-0001",
            sufficiency=Sufficiency.CONFLITANTE,
            usage_status=UsageStatus.USO_CONDICIONAL,
            validation_state=ValidationState.VALIDACAO_PENDENTE,
        )
    )
    reg.marcar_conflito("CLM-HIST-0001", ["SRC-DOCUMENTO-0001"])


def test_substituicao_sem_referencia_a_predecessora_e_rejeitada():
    reg = RegistroDeRelacoes()
    reg.adicionar(relacao_base(claim_id="CLM-HIST-0001", source_id="SRC-DOCUMENTO-0001"))
    with pytest.raises(ErroDeCoerencia, match="RC-014"):
        reg.adicionar(
            relacao_base(
                claim_id="CLM-HIST-0001",
                source_id="SRC-DOCUMENTO-0001",
                relation_version=2,
                notes="apenas uma nota qualquer",
            ),
            eh_substituicao=True,
        )

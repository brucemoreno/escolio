import pytest

from escolio.voz.erros import ErroDePerfilDeVoz
from escolio.voz.perfil import PerfilDeVoz
from escolio.voz.vocabulario import Confidence, StatusDePerfil, TipoDePerfil


def perfil_base(**overrides):
    campos = dict(
        profile_id="PV-0001",
        profile_type=TipoDePerfil.PERFIL_NEUTRO_ACADEMICO_CONTROLADO,
        purpose="preservar a voz do autor avaliado na revisão",
        scope={"documento": "dissertacao-001"},
        dimensions={},
        evidence=[],
        confidence=Confidence.NAO_APLICAVEL,
        authorization={},
        versioning={"versao": 1},
        provenance=[],
        reversibility={"reversivel": True},
        status=StatusDePerfil.VALIDADO,
    )
    campos.update(overrides)
    return PerfilDeVoz(**campos)


def test_perfil_neutro_nao_exige_amostra_nem_declaracao():
    perfil = perfil_base()
    assert perfil.profile_type == TipoDePerfil.PERFIL_NEUTRO_ACADEMICO_CONTROLADO


def test_perfil_neutro_exige_scope_nao_vazio():
    with pytest.raises(ErroDePerfilDeVoz):
        perfil_base(scope={})


def test_perfil_declarado_exige_authorization_nao_vazia():
    with pytest.raises(ErroDePerfilDeVoz):
        perfil_base(
            profile_type=TipoDePerfil.PERFIL_AUTORAL_DECLARADO_PELO_USUARIO,
            authorization={},
            confidence=Confidence.MEDIA,
        )


def test_perfil_declarado_com_authorization_e_valido():
    perfil = perfil_base(
        profile_type=TipoDePerfil.PERFIL_AUTORAL_DECLARADO_PELO_USUARIO,
        authorization={"declarante": "USUARIO_PROPONENTE"},
        confidence=Confidence.MEDIA,
    )
    assert perfil.profile_type == TipoDePerfil.PERFIL_AUTORAL_DECLARADO_PELO_USUARIO


def test_perfil_derivado_exige_multiplas_amostras():
    with pytest.raises(ErroDePerfilDeVoz):
        perfil_base(
            profile_type=TipoDePerfil.PERFIL_AUTORAL_DERIVADO_DE_AMOSTRAS,
            evidence=["amostra-1"],
            provenance=["acervo:cap1"],
            confidence=Confidence.MEDIA,
        )


def test_perfil_derivado_exige_proveniencia():
    with pytest.raises(ErroDePerfilDeVoz):
        perfil_base(
            profile_type=TipoDePerfil.PERFIL_AUTORAL_DERIVADO_DE_AMOSTRAS,
            evidence=["amostra-1", "amostra-2"],
            provenance=[],
            confidence=Confidence.MEDIA,
        )


def test_perfil_derivado_com_amostras_e_proveniencia_e_valido():
    perfil = perfil_base(
        profile_type=TipoDePerfil.PERFIL_AUTORAL_DERIVADO_DE_AMOSTRAS,
        evidence=["amostra-1", "amostra-2"],
        provenance=["acervo:cap1", "acervo:cap2"],
        confidence=Confidence.ALTA,
    )
    assert len(perfil.evidence) == 2


def test_perfil_hibrido_exige_declaracao_e_amostras():
    with pytest.raises(ErroDePerfilDeVoz):
        perfil_base(
            profile_type=TipoDePerfil.PERFIL_HIBRIDO_DECLARACAO_MAIS_AMOSTRAS,
            authorization={"declarante": "USUARIO_PROPONENTE"},
            evidence=["amostra-1"],
            provenance=["acervo:cap1"],
            confidence=Confidence.MEDIA,
        )


def test_perfil_hibrido_completo_e_valido():
    perfil = perfil_base(
        profile_type=TipoDePerfil.PERFIL_HIBRIDO_DECLARACAO_MAIS_AMOSTRAS,
        authorization={"declarante": "USUARIO_PROPONENTE"},
        evidence=["amostra-1", "amostra-2"],
        provenance=["acervo:cap1", "acervo:cap2"],
        confidence=Confidence.ALTA,
    )
    assert perfil.profile_type == TipoDePerfil.PERFIL_HIBRIDO_DECLARACAO_MAIS_AMOSTRAS


def test_perfil_local_exige_scope_nao_vazio():
    with pytest.raises(ErroDePerfilDeVoz):
        perfil_base(
            profile_type=TipoDePerfil.PERFIL_LOCAL_POR_GENERO_OU_SECAO,
            scope={},
            confidence=Confidence.MEDIA,
        )


def test_perfil_insuficiente_exige_status_abstencao():
    with pytest.raises(ErroDePerfilDeVoz):
        perfil_base(
            profile_type=TipoDePerfil.PERFIL_INSUFICIENTE_OU_CONFLITANTE,
            status=StatusDePerfil.VALIDADO,
            confidence=Confidence.BAIXA,
        )


def test_perfil_insuficiente_com_abstencao_e_valido():
    perfil = perfil_base(
        profile_type=TipoDePerfil.PERFIL_INSUFICIENTE_OU_CONFLITANTE,
        status=StatusDePerfil.ABSTENCAO,
        abstention_reason="amostras conflitantes sem resolução",
        confidence=Confidence.BAIXA,
    )
    assert perfil.status == StatusDePerfil.ABSTENCAO


def test_status_abstencao_exige_abstention_reason():
    with pytest.raises(ErroDePerfilDeVoz):
        perfil_base(status=StatusDePerfil.ABSTENCAO, abstention_reason=None)


def test_profile_id_obrigatorio():
    with pytest.raises(ErroDePerfilDeVoz):
        perfil_base(profile_id="")

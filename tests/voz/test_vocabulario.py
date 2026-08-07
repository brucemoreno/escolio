from escolio.voz.vocabulario import (
    Confidence,
    DesvioBloqueante,
    GateDePerfil,
    GATE_POR_PERFIL,
    ResultadoDeFidelidade,
    StatusDePerfil,
    TipoDePerfil,
)


def test_seis_tipos_de_perfil():
    assert len(TipoDePerfil) == 6


def test_quatro_niveis_de_confianca():
    assert {c.value for c in Confidence} == {"BAIXA", "MEDIA", "ALTA", "NAO_APLICAVEL"}


def test_cinco_resultados_de_fidelidade():
    assert {r.value for r in ResultadoDeFidelidade} == {
        "CONFORME",
        "CONFORME_COM_RESSALVAS",
        "CORRIGIR_ANTES_DE_AVANCAR",
        "BLOQUEAR",
        "ABSTER_SE",
    }


def test_oito_desvios_bloqueantes():
    assert len(DesvioBloqueante) == 8


def test_gate_por_perfil_cobre_os_seis_tipos():
    assert set(GATE_POR_PERFIL.keys()) == set(TipoDePerfil)


def test_gate_neutro_para_perfil_neutro():
    assert GATE_POR_PERFIL[TipoDePerfil.PERFIL_NEUTRO_ACADEMICO_CONTROLADO] == GateDePerfil.GATE_NEUTRO


def test_gate_abstencao_para_perfil_insuficiente():
    assert (
        GATE_POR_PERFIL[TipoDePerfil.PERFIL_INSUFICIENTE_OU_CONFLITANTE] == GateDePerfil.GATE_ABSTENCAO
    )

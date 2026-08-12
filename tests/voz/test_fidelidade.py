import pytest

from escolio.voz.deteccao import AchadoDeFidelidade
from escolio.voz.erros import ErroDePerfilDeVoz
from escolio.voz.fidelidade import AvaliacaoDeFidelidade, avaliar, avaliar_a_partir_do_perfil
from escolio.voz.perfil import PerfilDeVoz
from escolio.voz.vocabulario import (
    Confidence,
    DesvioBloqueante,
    ResultadoDeFidelidade,
    StatusDePerfil,
    TipoDePerfil,
)


def _avaliar(**overrides):
    campos = dict(
        desvios_encontrados=[],
        amostra_unica=False,
        amostras_conflitantes=False,
        proveniencia_ausente=False,
        autorizacao_ausente=False,
        perfil_declarado_sem_amostras=False,
        exigencia_institucional_em_conflito=False,
    )
    campos.update(overrides)
    return avaliar(**campos)


# TV-01 — preservação de sentido com ajuste leve -> CONFORME
def test_conforme_quando_nenhuma_condicao_se_aplica():
    resultado = _avaliar()
    assert resultado.resultado == ResultadoDeFidelidade.CONFORME


# TV-02 / TV-13 — cópia mecânica / excesso de ornamentação são desvios
# bloqueantes concretos -> BLOQUEAR
@pytest.mark.parametrize("desvio", list(DesvioBloqueante))
def test_qualquer_desvio_bloqueante_forca_bloqueio(desvio):
    resultado = _avaliar(desvios_encontrados=[desvio])
    assert resultado.resultado == ResultadoDeFidelidade.BLOQUEAR
    assert desvio in resultado.desvios_encontrados


# TV-03 — rejeição de invenção de fato para fluidez -> BLOQUEAR
def test_invencao_factual_bloqueia():
    resultado = _avaliar(desvios_encontrados=[DesvioBloqueante.INVENCAO_FACTUAL])
    assert resultado.resultado == ResultadoDeFidelidade.BLOQUEAR


# TV-06 — amostra única insuficiente -> ABSTER_SE
def test_amostra_unica_leva_a_abstencao():
    resultado = _avaliar(amostra_unica=True)
    assert resultado.resultado == ResultadoDeFidelidade.ABSTER_SE
    assert resultado.abstention_reason


# TV-07 — amostras conflitantes -> ABSTER_SE
def test_amostras_conflitantes_levam_a_abstencao():
    resultado = _avaliar(amostras_conflitantes=True)
    assert resultado.resultado == ResultadoDeFidelidade.ABSTER_SE


# TV-08 — perfil declarado sem amostras -> CONFORME_COM_RESSALVAS
def test_perfil_declarado_sem_amostras_gera_ressalva():
    resultado = _avaliar(perfil_declarado_sem_amostras=True)
    assert resultado.resultado == ResultadoDeFidelidade.CONFORME_COM_RESSALVAS


# TV-10 — exigência institucional em conflito -> CORRIGIR_ANTES_DE_AVANCAR
def test_exigencia_institucional_em_conflito_exige_correcao():
    resultado = _avaliar(exigencia_institucional_em_conflito=True)
    assert resultado.resultado == ResultadoDeFidelidade.CORRIGIR_ANTES_DE_AVANCAR


# TV-18 — abstenção por proveniência insuficiente -> ABSTER_SE
def test_proveniencia_ausente_leva_a_abstencao():
    resultado = _avaliar(proveniencia_ausente=True)
    assert resultado.resultado == ResultadoDeFidelidade.ABSTER_SE


def test_autorizacao_ausente_leva_a_abstencao():
    resultado = _avaliar(autorizacao_ausente=True)
    assert resultado.resultado == ResultadoDeFidelidade.ABSTER_SE


def test_abstencao_tem_precedencia_sobre_desvio_bloqueante():
    resultado = _avaliar(autorizacao_ausente=True, desvios_encontrados=[DesvioBloqueante.INVENCAO_FACTUAL])
    assert resultado.resultado == ResultadoDeFidelidade.ABSTER_SE


def test_avaliador_nao_expoe_texto_revisado():
    resultado = _avaliar()
    assert not hasattr(resultado, "texto_revisado")
    assert not hasattr(resultado, "texto_corrigido")


def test_bloquear_sem_desvio_encontrado_e_invalido():
    with pytest.raises(ErroDePerfilDeVoz):
        AvaliacaoDeFidelidade(resultado=ResultadoDeFidelidade.CONFORME, desvios_encontrados=[DesvioBloqueante.COPIA_OU_IMITACAO])


def _perfil(**overrides):
    campos = {
        "profile_id": "PV-0001",
        "profile_type": TipoDePerfil.PERFIL_NEUTRO_ACADEMICO_CONTROLADO,
        "purpose": "preservar a voz do autor avaliado na revisão",
        "scope": {"documento": "doc-001"},
        "dimensions": {},
        "evidence": [],
        "confidence": Confidence.NAO_APLICAVEL,
        "authorization": {},
        "versioning": {"versao": 1},
        "provenance": [],
        "reversibility": {"reversivel": True},
        "status": StatusDePerfil.VALIDADO,
    }
    campos.update(overrides)
    return PerfilDeVoz(**campos)


def _achado(tipo=DesvioBloqueante.INVENCAO_FACTUAL, observado=False, confianca=Confidence.ALTA):
    return AchadoDeFidelidade(
        tipo=tipo, observado=observado, evidencia="evidência sintética" if observado else "", confianca=confianca
    )


class TestAvaliarAPartirDoPerfil:
    """Camada A→B (Instruções Complementares §1.2) — `avaliar()` em si
    (Camada B) não é tocada por nenhum destes testes; só a derivação de
    fatos a partir de `PerfilDeVoz` é nova."""

    def test_perfil_neutro_sem_achados_e_conforme(self):
        resultado = avaliar_a_partir_do_perfil(_perfil(), achados=[])
        assert resultado.resultado == ResultadoDeFidelidade.CONFORME

    def test_desvio_observado_bloqueia(self):
        resultado = avaliar_a_partir_do_perfil(
            _perfil(), achados=[_achado(observado=True, tipo=DesvioBloqueante.ALTERACAO_DE_SENTIDO)]
        )
        assert resultado.resultado == ResultadoDeFidelidade.BLOQUEAR
        assert DesvioBloqueante.ALTERACAO_DE_SENTIDO in resultado.desvios_encontrados

    def test_desvio_nao_observado_nao_bloqueia(self):
        resultado = avaliar_a_partir_do_perfil(_perfil(), achados=[_achado(observado=False)])
        assert resultado.resultado == ResultadoDeFidelidade.CONFORME

    def test_amostra_unica_derivada_do_perfil_abstem(self):
        perfil = _perfil(
            profile_type=TipoDePerfil.PERFIL_AUTORAL_DECLARADO_PELO_USUARIO,
            authorization={"declarante": "USUARIO_PROPONENTE"},
            confidence=Confidence.MEDIA,
            evidence=["amostra-1"],
        )
        resultado = avaliar_a_partir_do_perfil(perfil, achados=[])
        assert resultado.resultado == ResultadoDeFidelidade.ABSTER_SE

    def test_perfil_declarado_sem_amostras_gera_ressalva(self):
        perfil = _perfil(
            profile_type=TipoDePerfil.PERFIL_AUTORAL_DECLARADO_PELO_USUARIO,
            authorization={"declarante": "USUARIO_PROPONENTE"},
            confidence=Confidence.MEDIA,
            evidence=[],
        )
        resultado = avaliar_a_partir_do_perfil(perfil, achados=[])
        assert resultado.resultado == ResultadoDeFidelidade.CONFORME_COM_RESSALVAS

    def test_perfil_derivado_valido_nao_aborta_por_autorizacao_ou_proveniencia(self):
        # Perfil DERIVADO já exige (na própria construção) evidence>=2 e
        # provenance não vazio — autorizacao_ausente/proveniencia_ausente
        # derivados devem ser False, nunca True, para uma instância válida.
        perfil = _perfil(
            profile_type=TipoDePerfil.PERFIL_AUTORAL_DERIVADO_DE_AMOSTRAS,
            evidence=["amostra-1", "amostra-2"],
            provenance=["fonte-1"],
        )
        resultado = avaliar_a_partir_do_perfil(perfil, achados=[])
        assert resultado.resultado == ResultadoDeFidelidade.CONFORME

    def test_amostras_conflitantes_e_parametro_explicito_nao_derivado(self):
        perfil = _perfil(
            profile_type=TipoDePerfil.PERFIL_AUTORAL_DERIVADO_DE_AMOSTRAS,
            evidence=["amostra-1", "amostra-2"],
            provenance=["fonte-1"],
        )
        resultado = avaliar_a_partir_do_perfil(perfil, achados=[], amostras_conflitantes=True)
        assert resultado.resultado == ResultadoDeFidelidade.ABSTER_SE

    def test_exigencia_institucional_em_conflito_e_parametro_explicito(self):
        resultado = avaliar_a_partir_do_perfil(
            _perfil(), achados=[], exigencia_institucional_em_conflito=True
        )
        assert resultado.resultado == ResultadoDeFidelidade.CORRIGIR_ANTES_DE_AVANCAR


def test_abster_se_sem_motivo_e_invalido():
    with pytest.raises(ErroDePerfilDeVoz):
        AvaliacaoDeFidelidade(resultado=ResultadoDeFidelidade.ABSTER_SE)


def test_resultado_nao_abster_se_exige_justificativa():
    with pytest.raises(ErroDePerfilDeVoz):
        AvaliacaoDeFidelidade(resultado=ResultadoDeFidelidade.CONFORME, justificativa="")

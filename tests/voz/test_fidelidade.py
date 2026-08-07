import pytest

from escolio.voz.erros import ErroDePerfilDeVoz
from escolio.voz.fidelidade import AvaliacaoDeFidelidade, avaliar
from escolio.voz.vocabulario import DesvioBloqueante, ResultadoDeFidelidade


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


def test_abster_se_sem_motivo_e_invalido():
    with pytest.raises(ErroDePerfilDeVoz):
        AvaliacaoDeFidelidade(resultado=ResultadoDeFidelidade.ABSTER_SE)


def test_resultado_nao_abster_se_exige_justificativa():
    with pytest.raises(ErroDePerfilDeVoz):
        AvaliacaoDeFidelidade(resultado=ResultadoDeFidelidade.CONFORME, justificativa="")

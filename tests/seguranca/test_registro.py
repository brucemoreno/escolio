import pytest

from escolio.seguranca.erros import ErroDeSeguranca
from escolio.seguranca.registro import Achado, RegistroDeAnalise


def achado(campo="injection_suspected", unit_id="UNI-001"):
    return Achado(unit_id=unit_id, campo=campo, trecho="trecho de evidência", camada="DETERMINISTICO", regra="PI-03")


# --- DTA-01: "ainda não analisado" é representável fora do InputItem ---


def test_registro_comeca_nao_analisado():
    r = RegistroDeAnalise(input_id="INP-1", versao_de_padroes="v1")
    assert r.analisado is False
    assert r.achados == []


def test_registrar_achado_marca_analisado():
    r = RegistroDeAnalise(input_id="INP-1", versao_de_padroes="v1")
    r.registra_achado(achado())
    assert r.analisado is True


def test_registro_analisado_sem_achados_e_distinguivel_de_nunca_analisado():
    # PR-03: ausência de classificação != análise que não achou nada.
    r_nunca_analisado = RegistroDeAnalise(input_id="INP-1", versao_de_padroes="v1")
    r_analisado_limpo = RegistroDeAnalise(input_id="INP-2", versao_de_padroes="v1", analisado=True)
    assert r_nunca_analisado.analisado is False
    assert r_analisado_limpo.analisado is True
    assert r_analisado_limpo.achados == []


# --- DTA-02: monotonicidade (latching) ---


def test_registrar_achado_nao_remove_achados_anteriores():
    r = RegistroDeAnalise(input_id="INP-1", versao_de_padroes="v1")
    r.registra_achado(achado(campo="injection_suspected"))
    r.registra_achado(achado(campo="exfiltration_risk"))
    assert len(r.achados) == 2


def test_valor_de_permanece_true_apos_novo_achado_de_outro_campo():
    r = RegistroDeAnalise(input_id="INP-1", versao_de_padroes="v1")
    r.registra_achado(achado(campo="injection_suspected"))
    assert r.valor_de("injection_suspected") is True
    r.registra_achado(achado(campo="exfiltration_risk"))
    # Uma passada posterior sobre outro campo não baixa o primeiro.
    assert r.valor_de("injection_suspected") is True


def test_nao_existe_metodo_que_baixe_flag_sem_autoridade():
    # DTA-02: só (c) pode reverter, com evidência material e autoridade válida
    # — reduz_protecao exige os dois argumentos, sem default que os dispense.
    r = RegistroDeAnalise(input_id="INP-1", versao_de_padroes="v1")
    r.registra_achado(achado(campo="injection_suspected"))
    with pytest.raises(ErroDeSeguranca):
        r.reduz_protecao("injection_suspected", motivo="", autoridade_basis="")


def test_reduz_protecao_com_motivo_e_autoridade_remove_achados_do_campo():
    # RH-02: caminho (c) explícito, não default silencioso.
    r = RegistroDeAnalise(input_id="INP-1", versao_de_padroes="v1")
    r.registra_achado(achado(campo="injection_suspected"))
    r.reduz_protecao("injection_suspected", motivo="falso positivo confirmado", autoridade_basis="USUARIO_PROPONENTE, 2026-08-08")
    assert r.valor_de("injection_suspected") is False


# --- DTA-03: cada booleano é derivado só da sua própria evidência ---


def test_valor_de_nao_e_afetado_por_achado_de_outro_campo():
    r = RegistroDeAnalise(input_id="INP-1", versao_de_padroes="v1")
    r.registra_achado(achado(campo="injection_suspected"))
    assert r.valor_de("adversarial_content") is False
    assert r.valor_de("exfiltration_risk") is False

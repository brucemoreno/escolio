import pytest

from escolio.intervencao.niveis import (
    NivelIntervencao,
    escalonamento_permitido,
    excede,
    nivel_maximo_ainda_autorizado,
    posicao,
)


def test_cadeia_tem_quinze_niveis():
    assert len(NivelIntervencao) == 15


@pytest.mark.parametrize(
    "nivel",
    list(NivelIntervencao),
)
def test_cada_nivel_tem_identificador_int(nivel):
    assert nivel.value.startswith("INT-")


def test_ordem_da_cadeia_e_a_declarada_no_dicionario():
    esperado = [
        NivelIntervencao.OBSERVACAO,
        NivelIntervencao.DIAGNOSTICO,
        NivelIntervencao.SINALIZACAO,
        NivelIntervencao.RECOMENDACAO,
        NivelIntervencao.PROPOSTA,
        NivelIntervencao.SIMULACAO,
        NivelIntervencao.EDICAO_LOCAL,
        NivelIntervencao.REESCRITA,
        NivelIntervencao.REORGANIZACAO,
        NivelIntervencao.FUSAO,
        NivelIntervencao.CORTE,
        NivelIntervencao.SUBSTITUICAO,
        NivelIntervencao.VALIDACAO,
        NivelIntervencao.HOMOLOGACAO,
    ]
    for a, b in zip(esperado, esperado[1:]):
        assert posicao(a) < posicao(b)


def test_nivel_nao_excede_a_si_mesmo():
    assert not excede(NivelIntervencao.EDICAO_LOCAL, NivelIntervencao.EDICAO_LOCAL)


def test_nivel_inferior_nao_excede_superior():
    assert not excede(NivelIntervencao.OBSERVACAO, NivelIntervencao.HOMOLOGACAO)


def test_nivel_superior_excede_inferior():
    assert excede(NivelIntervencao.HOMOLOGACAO, NivelIntervencao.OBSERVACAO)


def test_abstencao_excede_qualquer_nivel_diferente_de_si_mesma():
    assert excede(NivelIntervencao.ABSTENCAO, NivelIntervencao.OBSERVACAO)


def test_abstencao_nao_excede_abstencao():
    assert not excede(NivelIntervencao.ABSTENCAO, NivelIntervencao.ABSTENCAO)


# Não há herança automática de permissão [§7]: nenhum nível superior se
# infere de nível inferior — apenas as transições listadas na matriz §04
# existem.


def test_escalonamento_listado_e_permitido():
    assert escalonamento_permitido(NivelIntervencao.OBSERVACAO, NivelIntervencao.DIAGNOSTICO)


def test_escalonamento_nao_listado_e_negado():
    # Salto de dois níveis não está na matriz — não há herança automática.
    assert not escalonamento_permitido(NivelIntervencao.OBSERVACAO, NivelIntervencao.SINALIZACAO)


def test_escalonamento_regressivo_e_negado():
    assert not escalonamento_permitido(NivelIntervencao.DIAGNOSTICO, NivelIntervencao.OBSERVACAO)


def test_reorganizacao_escalona_para_fusao_e_corte():
    assert escalonamento_permitido(NivelIntervencao.REORGANIZACAO, NivelIntervencao.FUSAO)
    assert escalonamento_permitido(NivelIntervencao.REORGANIZACAO, NivelIntervencao.CORTE)


def test_validacao_escalona_para_homologacao():
    assert escalonamento_permitido(NivelIntervencao.VALIDACAO, NivelIntervencao.HOMOLOGACAO)


# Regressão segura [§8]: regredir ao nível máximo ainda autorizado; None se
# nenhum nível operativo permanecer válido.


def test_regressao_segura_recua_ao_maximo_autorizado():
    autorizados = frozenset({NivelIntervencao.OBSERVACAO, NivelIntervencao.DIAGNOSTICO})
    resultado = nivel_maximo_ainda_autorizado(NivelIntervencao.REESCRITA, autorizados)
    assert resultado == NivelIntervencao.DIAGNOSTICO


def test_regressao_segura_nao_excede_o_pretendido():
    autorizados = frozenset({NivelIntervencao.HOMOLOGACAO})
    resultado = nivel_maximo_ainda_autorizado(NivelIntervencao.DIAGNOSTICO, autorizados)
    assert resultado is None


def test_regressao_segura_sem_nivel_operativo_retorna_none():
    resultado = nivel_maximo_ainda_autorizado(NivelIntervencao.OBSERVACAO, frozenset())
    assert resultado is None


def test_regressao_segura_ignora_abstencao_como_autorizado():
    autorizados = frozenset({NivelIntervencao.ABSTENCAO})
    resultado = nivel_maximo_ainda_autorizado(NivelIntervencao.OBSERVACAO, autorizados)
    assert resultado is None

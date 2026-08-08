import pytest

from escolio.seguranca.protocolo import PASSOS, CoberturaDoPasso, passo
from escolio.seguranca.vocabulario import PASSOS_DO_PROTOCOLO


def test_numero_de_passos_bate_com_a_fonte():
    # RD-12: [P08 §12] tem exatamente 20 passos.
    assert len(PASSOS) == 20
    assert len(PASSOS_DO_PROTOCOLO) == 20


def test_passos_numerados_de_1_a_20_sem_lacuna():
    assert [p.numero for p in PASSOS] == list(range(1, 21))


def test_passo_devolve_o_correto():
    assert passo(10).nome == "detectar instruções internas"


def test_passo_numero_invalido_levanta():
    with pytest.raises(KeyError):
        passo(21)


def test_passos_bloqueados_por_lacuna_normativa_sao_5_6_13_15_18():
    # CO-012 (passo 5), CO-013 (passo 6), LAC-SEG-005 (passos 13, 15),
    # DTA-14 sem threshold (passo 18) — nenhum é falha de engenharia.
    bloqueados = {p.numero for p in PASSOS if p.cobertura == CoberturaDoPasso.BLOQUEADO_POR_LACUNA_NORMATIVA}
    assert bloqueados == {5, 6, 13, 15, 18}


def test_nenhum_passo_declara_cobertura_nao_prevista_no_enum():
    for p in PASSOS:
        assert isinstance(p.cobertura, CoberturaDoPasso)


def test_passo_10_e_11_cobertos_pelo_modulo_deteccao():
    assert passo(10).modulo == "escolio.seguranca.deteccao"
    assert passo(11).modulo == "escolio.seguranca.deteccao"

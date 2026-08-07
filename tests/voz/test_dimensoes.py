from escolio.voz.dimensoes import DEFINICOES, DIMENSOES_OBRIGATORIAS, DimensaoDeVoz, Obrigatoriedade


def test_trinta_dimensoes():
    assert len(DimensaoDeVoz) == 30


def test_todas_dimensoes_tem_definicao():
    assert set(DEFINICOES.keys()) == set(DimensaoDeVoz)


def test_vinte_e_seis_obrigatorias_quatro_opcionais():
    assert len(DIMENSOES_OBRIGATORIAS) == 26
    opcionais = [d for d, definicao in DEFINICOES.items() if definicao.obrigatoriedade == Obrigatoriedade.OPCIONAL]
    assert len(opcionais) == 4


def test_dimensoes_opcionais_sao_d16_a_d19():
    opcionais = {
        definicao.dimension_id for definicao in DEFINICOES.values() if definicao.obrigatoriedade == Obrigatoriedade.OPCIONAL
    }
    assert opcionais == {"VOZ-D16", "VOZ-D17", "VOZ-D18", "VOZ-D19"}


def test_ordem_dos_ids_e_a_do_csv():
    esperado = [f"VOZ-D{n:02d}" for n in range(1, 31)]
    assert [DEFINICOES[d].dimension_id for d in DimensaoDeVoz] == esperado

from escolio.voz.hierarquia import CADEIA_DE_PRECEDENCIA, EloDeHierarquia, posicao, prevalece


def test_seis_elos_na_ordem_da_fonte():
    assert [e.value for e in CADEIA_DE_PRECEDENCIA] == [
        "INTEGRIDADE_DOCUMENTAL",
        "SENTIDO",
        "DENSIDADE_E_NUANCE",
        "PERFIL_TEMATICO_E_EXIGENCIA_INSTITUCIONAL",
        "VOZ_AUTORAL",
        "FLUIDEZ",
    ]


def test_integridade_documental_e_o_topo():
    assert posicao(EloDeHierarquia.INTEGRIDADE_DOCUMENTAL) == 0


def test_fluidez_e_a_base():
    assert posicao(EloDeHierarquia.FLUIDEZ) == len(CADEIA_DE_PRECEDENCIA) - 1


def test_integridade_prevalece_sobre_voz_autoral():
    assert (
        prevalece(EloDeHierarquia.INTEGRIDADE_DOCUMENTAL, EloDeHierarquia.VOZ_AUTORAL)
        == EloDeHierarquia.INTEGRIDADE_DOCUMENTAL
    )


def test_sentido_prevalece_sobre_fluidez():
    assert prevalece(EloDeHierarquia.SENTIDO, EloDeHierarquia.FLUIDEZ) == EloDeHierarquia.SENTIDO


def test_voz_autoral_prevalece_sobre_fluidez():
    assert prevalece(EloDeHierarquia.VOZ_AUTORAL, EloDeHierarquia.FLUIDEZ) == EloDeHierarquia.VOZ_AUTORAL


def test_densidade_e_nuance_prevalece_sobre_perfil_tematico():
    assert (
        prevalece(EloDeHierarquia.DENSIDADE_E_NUANCE, EloDeHierarquia.PERFIL_TEMATICO_E_EXIGENCIA_INSTITUCIONAL)
        == EloDeHierarquia.DENSIDADE_E_NUANCE
    )


def test_prevalece_e_simetrico_na_ordem_dos_argumentos():
    a, b = EloDeHierarquia.SENTIDO, EloDeHierarquia.VOZ_AUTORAL
    assert prevalece(a, b) == prevalece(b, a) == EloDeHierarquia.SENTIDO


def test_mesmo_elo_prevalece_sobre_si_mesmo():
    assert prevalece(EloDeHierarquia.SENTIDO, EloDeHierarquia.SENTIDO) == EloDeHierarquia.SENTIDO

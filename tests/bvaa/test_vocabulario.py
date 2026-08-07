from escolio.bvaa.vocabulario import EstadoBibliografico, NivelDeEvidencia


def test_dezessete_estados():
    assert len(EstadoBibliografico) == 17


def test_ordem_dos_estados_e_a_do_csv():
    esperado = [
        "OBRA_NAO_IDENTIFICADA",
        "OBRA_IDENTIFICADA",
        "EDICAO_IDENTIFICADA",
        "LOCALIZADA",
        "ACESSIVEL",
        "ACESSADA",
        "LEITURA_NAO_REALIZADA",
        "LEITURA_INDIRETA",
        "LEITURA_PARCIAL",
        "LEITURA_INTEGRAL",
        "PAGINA_NAO_CONFIRMADA",
        "PAGINA_CONFIRMADA",
        "VALIDACAO_PENDENTE",
        "VALIDADA",
        "RECOMENDACAO_CONDICIONAL",
        "RECOMENDADA",
        "ABSTENCAO_BIBLIOGRAFICA",
    ]
    assert [e.value for e in EstadoBibliografico] == esperado


def test_quatro_niveis_de_evidencia():
    assert len(NivelDeEvidencia) == 4

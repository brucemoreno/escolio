"""Extração determinística de metadados de referência — sessão de
2026-08-13 (curador automático BVAA). Nenhum exemplo aqui vem de
`data/capitulos/` real: os três capítulos reais não têm lista de
referências (LAC-ING-017); todos os textos abaixo são sintéticos, ABNT
convencional."""

from escolio.bvaa.extracao_metadados_referencia import extrair_metadados_deterministicos


def test_extrai_autor_e_ano_de_referencia_abnt_convencional():
    texto = "GREWE, R. Fonte sintética. São Paulo: Editora X, 1979."
    metadados = extrair_metadados_deterministicos(texto)

    assert metadados.autor_sobrenome == "GREWE"
    assert metadados.ano == "1979"
    assert metadados.titulo == "Fonte sintética"
    assert metadados.texto_origem == texto
    assert metadados.metodo == "REGEX_ABNT_DETERMINISTICO"


def test_termo_de_busca_junta_autor_e_ano():
    metadados = extrair_metadados_deterministicos("GREWE, R. Fonte sintética. São Paulo: Editora X, 1979.")
    assert metadados.termo_de_busca() == "GREWE 1979"


def test_texto_sem_sobrenome_maiusculo_nao_extrai_autor():
    # ABNT exige sobrenome em maiúsculas como primeiro elemento — texto
    # livre sem essa convenção não deve produzir um palpite de autor.
    texto = "Um texto qualquer sem formato de referência, 1979."
    metadados = extrair_metadados_deterministicos(texto)
    assert metadados.autor_sobrenome is None
    assert metadados.ano == "1979"
    assert metadados.termo_de_busca() == "1979"


def test_texto_sem_ano_nem_autor_nao_produz_termo_de_busca():
    metadados = extrair_metadados_deterministicos("referência incompleta sem nenhum dado reconhecível")
    assert metadados.autor_sobrenome is None
    assert metadados.ano is None
    assert metadados.termo_de_busca() is None


def test_ano_escolhido_e_o_ultimo_da_string_nao_o_primeiro():
    # Ano dentro do próprio título (ex.: obra sobre um evento datado) não
    # deve ser confundido com o ano de publicação, que ABNT coloca ao final.
    texto = "SILVA, J. A crise de 1929 e suas consequências. Rio de Janeiro: Editora Y, 2005."
    metadados = extrair_metadados_deterministicos(texto)
    assert metadados.ano == "2005"


def test_candidato_a_titulo_que_contem_o_proprio_ano_fica_none():
    texto = "GREWE, R. (1979). Fonte sintética."
    metadados = extrair_metadados_deterministicos(texto)
    assert metadados.ano == "1979"
    assert metadados.titulo is None


def test_texto_com_um_unico_campo_nao_produz_titulo():
    texto = "GREWE 1979"
    metadados = extrair_metadados_deterministicos(texto)
    assert metadados.titulo is None

"""A tabela de correspondência não escolhe um vencedor entre os três
vocabulários — CON-P05-001. Testa que a tabela cobre os 17 estados e que
nenhuma célula finge equivalência que a fonte não sustenta.
"""

from escolio.bvaa.correspondencia import TABELA_DE_CORRESPONDENCIA, correspondencia_de
from escolio.bvaa.vocabulario import EstadoBibliografico as EB
from escolio.vocabulario import AccessState, ReadingState, ValidationState


def test_tabela_cobre_os_dezessete_estados():
    estados_na_tabela = {linha.estado_p04 for linha in TABELA_DE_CORRESPONDENCIA}
    assert estados_na_tabela == set(EB)


def test_correspondencia_de_retorna_a_linha_certa():
    linha = correspondencia_de(EB.PAGINA_CONFIRMADA)
    assert linha.estado_r03_camada_d == "LOCALIZACAO_CONFIRMADA"
    assert linha.campo_p05 == "validation_state"
    assert linha.valor_p05 == ValidationState.PAGINA_CONFIRMADA.value


def test_estado_sem_correspondencia_fica_none_com_nota():
    linha = correspondencia_de(EB.OBRA_NAO_IDENTIFICADA)
    assert linha.estado_r03_camada_d is None
    assert linha.campo_p05 is None
    assert linha.nota  # motivo por extenso, nunca célula muda sem explicação


def test_campo_p05_referenciado_e_sempre_um_dos_tres_campos_do_schema():
    campos_validos = {"access_state", "reading_state", "validation_state", None}
    for linha in TABELA_DE_CORRESPONDENCIA:
        assert linha.campo_p05 in campos_validos


def test_valores_p05_citados_existem_de_fato_no_vocabulario_p05():
    valores_access = {v.value for v in AccessState}
    valores_reading = {v.value for v in ReadingState}
    valores_validation = {v.value for v in ValidationState}
    for linha in TABELA_DE_CORRESPONDENCIA:
        if linha.campo_p05 == "access_state":
            assert linha.valor_p05 in valores_access
        elif linha.campo_p05 == "reading_state":
            assert linha.valor_p05 in valores_reading
        elif linha.campo_p05 == "validation_state":
            assert linha.valor_p05 in valores_validation

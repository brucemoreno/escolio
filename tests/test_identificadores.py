import pytest

from escolio.erros import ErroDeIdentificador
from escolio.identificadores import RegistroDeIdentificadores


def test_registra_claim_id_valido():
    reg = RegistroDeIdentificadores()
    reg.registrar_claim_id("CLM-HIST-0001")


def test_rejeita_claim_id_fora_do_padrao():
    reg = RegistroDeIdentificadores()
    with pytest.raises(ErroDeIdentificador):
        reg.registrar_claim_id("ID-QUALQUER")


def test_rejeita_duplicidade():
    reg = RegistroDeIdentificadores()
    reg.registrar_claim_id("CLM-HIST-0001")
    with pytest.raises(ErroDeIdentificador):
        reg.registrar_claim_id("CLM-HIST-0001")


def test_rejeita_reciclagem_apos_invalidacao():
    reg = RegistroDeIdentificadores()
    reg.registrar_claim_id("CLM-HIST-0001")
    reg.invalidar_claim_id("CLM-HIST-0001")
    with pytest.raises(ErroDeIdentificador):
        reg.registrar_claim_id("CLM-HIST-0001")


def test_source_id_mesma_regra():
    reg = RegistroDeIdentificadores()
    reg.registrar_source_id("SRC-DOCUMENTO-0001")
    reg.invalidar_source_id("SRC-DOCUMENTO-0001")
    with pytest.raises(ErroDeIdentificador):
        reg.registrar_source_id("SRC-DOCUMENTO-0001")

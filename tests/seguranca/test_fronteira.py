import pytest

from escolio.seguranca.erros import ErroDeEscopoDeSeguranca, ErroDeSeguranca
from escolio.seguranca.fronteira import MARCADOR_SINTETICO, exige_marcador_sintetico, recusa_caminho_sob_data


# --- DTA-22: trava explícita contra qualquer caminho sob data/ ---


@pytest.mark.parametrize(
    "caminho",
    [
        "data/dev/relatorio.pdf",
        "data/gold/tese_natalia.pdf",
        "data",
        "./data/dev/x.pdf",
        "/home/user/escolio/data/dev/x.pdf",
        "C:\\Users\\x\\escolio\\data\\dev\\x.pdf",
        "data\\gold\\x.pdf",
    ],
)
def test_recusa_qualquer_caminho_sob_data(caminho):
    # Inclusive data/dev/ — mais amplo que ErroDeEscopoDeDados da ingestão,
    # que cobre só "fora de data/dev/" (DTA-22).
    with pytest.raises(ErroDeEscopoDeSeguranca):
        recusa_caminho_sob_data(caminho)


@pytest.mark.parametrize(
    "caminho",
    [
        "tests/fixtures/adversariais/cenario_01.txt",
        "corpus/handoff-P22/x.md",
        "metadata.json",
        "docs/spec/operacional-P08.md",
    ],
)
def test_aceita_caminho_fora_de_data(caminho):
    recusa_caminho_sob_data(caminho)  # não levanta


def test_nao_confia_em_nome_de_arquivo_que_apenas_contem_a_string_data():
    # "metadata.json" não deve ser confundido com um caminho sob data/ —
    # a trava é sobre diretório, não substring.
    recusa_caminho_sob_data("metadata.json")


# --- DTA-23: marcador de procedência obrigatório em fixture sintética ---


def test_fixture_com_marcador_aceita():
    exige_marcador_sintetico(f"{MARCADOR_SINTETICO} texto de teste")


def test_fixture_sem_marcador_rejeita():
    with pytest.raises(ErroDeSeguranca):
        exige_marcador_sintetico("texto de teste sem marcador")

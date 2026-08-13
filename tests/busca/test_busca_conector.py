from unittest.mock import MagicMock, patch

import pytest
import requests

from escolio.busca.conector import ResultadoDeBusca, buscar
from escolio.busca.erros import ErroDeCredencialDeBusca, ErroDeRespostaDeBusca


def _resposta(status_code: int = 200, corpo: dict | None = None, texto: str = ""):
    resposta = MagicMock()
    resposta.status_code = status_code
    resposta.text = texto
    resposta.json.return_value = corpo if corpo is not None else {}
    return resposta


def test_api_key_ausente_levanta_erro_de_credencial():
    with pytest.raises(ErroDeCredencialDeBusca):
        buscar("Grewe 1979", "")


def test_busca_com_resultados_produz_resultadodebusca():
    corpo = {
        "organic": [
            {"title": "Título A", "link": "https://a.example/x", "snippet": "trecho A"},
            {"title": "Título B", "link": "https://b.example/y", "snippet": "trecho B"},
        ]
    }
    with patch("escolio.busca.conector.requests.post", return_value=_resposta(corpo=corpo)) as post:
        resultados = buscar("Grewe 1979", "chave-de-teste")

    assert resultados == [
        ResultadoDeBusca(titulo="Título A", link="https://a.example/x", trecho="trecho A"),
        ResultadoDeBusca(titulo="Título B", link="https://b.example/y", trecho="trecho B"),
    ]
    _, kwargs = post.call_args
    assert kwargs["headers"]["X-API-KEY"] == "chave-de-teste"
    assert kwargs["json"]["q"] == "Grewe 1979"


def test_sem_organic_devolve_lista_vazia():
    with patch("escolio.busca.conector.requests.post", return_value=_resposta(corpo={})):
        assert buscar("termo sem resultado", "chave-de-teste") == []


def test_status_diferente_de_200_levanta_erro_de_resposta():
    with patch("escolio.busca.conector.requests.post", return_value=_resposta(status_code=403, texto="negado")):
        with pytest.raises(ErroDeRespostaDeBusca):
            buscar("termo", "chave-invalida")


def test_falha_de_conexao_levanta_erro_de_resposta():
    with patch("escolio.busca.conector.requests.post", side_effect=requests.ConnectionError("timeout")):
        with pytest.raises(ErroDeRespostaDeBusca):
            buscar("termo", "chave-de-teste")


def test_corpo_nao_json_levanta_erro_de_resposta():
    resposta = _resposta()
    resposta.json.side_effect = ValueError("não é JSON")
    with patch("escolio.busca.conector.requests.post", return_value=resposta):
        with pytest.raises(ErroDeRespostaDeBusca):
            buscar("termo", "chave-de-teste")


def test_organic_fora_do_formato_levanta_erro_de_resposta():
    with patch("escolio.busca.conector.requests.post", return_value=_resposta(corpo={"organic": "não é lista"})):
        with pytest.raises(ErroDeRespostaDeBusca):
            buscar("termo", "chave-de-teste")


def test_num_resultados_limita_a_lista():
    corpo = {"organic": [{"title": f"T{i}", "link": f"https://x/{i}", "snippet": ""} for i in range(10)]}
    with patch("escolio.busca.conector.requests.post", return_value=_resposta(corpo=corpo)):
        resultados = buscar("termo", "chave-de-teste", num_resultados=3)
    assert len(resultados) == 3

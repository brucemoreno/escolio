from unittest.mock import MagicMock, patch

import pytest
from googleapiclient.errors import HttpError

from escolio.drive.conector import (
    ArquivoDrive,
    baixar_arquivo,
    buscar_arquivos,
    construir_servico,
    enviar_arquivo,
    exportar_arquivo,
    listar_arquivos_da_pasta,
)
from escolio.drive.erros import (
    ErroDeAcessoNegado,
    ErroDeCredencial,
    ErroDeRecursoNaoEncontrado,
    ErroDeRespostaInesperada,
)


def test_credencial_ausente_levanta_erro_tipado(tmp_path):
    caminho = tmp_path / "nao-existe.json"
    with pytest.raises(ErroDeCredencial):
        construir_servico(caminho)


def _http_error(status: int) -> HttpError:
    resposta = MagicMock()
    resposta.status = status
    return HttpError(resp=resposta, content=b'{"error": "erro simulado"}')


def _servico_de_listagem(paginas: list[dict]):
    servico = MagicMock()
    execucoes = iter(paginas)
    servico.files.return_value.list.return_value.execute.side_effect = lambda: next(execucoes)
    return servico


def test_lista_arquivos_de_uma_pagina():
    servico = _servico_de_listagem(
        [
            {
                "files": [
                    {
                        "id": "abc123",
                        "name": "artigo.pdf",
                        "mimeType": "application/pdf",
                        "size": "2048",
                        "modifiedTime": "2026-01-01T00:00:00Z",
                    }
                ]
            }
        ]
    )

    arquivos = listar_arquivos_da_pasta(servico, "pasta-1")

    assert arquivos == [
        ArquivoDrive(
            id="abc123",
            nome="artigo.pdf",
            mime_type="application/pdf",
            tamanho_bytes=2048,
            modificado_em="2026-01-01T00:00:00Z",
        )
    ]


def test_lista_arquivos_percorre_paginacao():
    servico = _servico_de_listagem(
        [
            {"files": [{"id": "1", "name": "a.pdf", "mimeType": "application/pdf"}], "nextPageToken": "pg2"},
            {"files": [{"id": "2", "name": "b.pdf", "mimeType": "application/pdf"}]},
        ]
    )

    arquivos = listar_arquivos_da_pasta(servico, "pasta-1")

    assert [a.id for a in arquivos] == ["1", "2"]


def test_arquivo_sem_tamanho_fica_none():
    servico = _servico_de_listagem(
        [{"files": [{"id": "1", "name": "pasta-filha", "mimeType": "application/vnd.google-apps.folder"}]}]
    )

    arquivos = listar_arquivos_da_pasta(servico, "pasta-1")

    assert arquivos[0].tamanho_bytes is None


def test_listar_403_levanta_erro_de_acesso_negado():
    servico = MagicMock()
    servico.files.return_value.list.return_value.execute.side_effect = _http_error(403)

    with pytest.raises(ErroDeAcessoNegado):
        listar_arquivos_da_pasta(servico, "pasta-sem-permissao")


def test_listar_404_levanta_erro_de_recurso_nao_encontrado():
    servico = MagicMock()
    servico.files.return_value.list.return_value.execute.side_effect = _http_error(404)

    with pytest.raises(ErroDeRecursoNaoEncontrado):
        listar_arquivos_da_pasta(servico, "pasta-inexistente")


def test_listar_erro_desconhecido_vira_resposta_inesperada():
    servico = MagicMock()
    servico.files.return_value.list.return_value.execute.side_effect = _http_error(500)

    with pytest.raises(ErroDeRespostaInesperada):
        listar_arquivos_da_pasta(servico, "pasta-1")


def test_baixar_arquivo_nativo_do_google_nao_e_suportado(tmp_path):
    servico = MagicMock()
    arquivo = ArquivoDrive(
        id="doc1",
        nome="Documento Google",
        mime_type="application/vnd.google-apps.document",
        tamanho_bytes=None,
        modificado_em=None,
    )

    with pytest.raises(ErroDeRespostaInesperada):
        baixar_arquivo(servico, arquivo, tmp_path / "saida.pdf")

    servico.files.return_value.get_media.assert_not_called()


def test_baixar_arquivo_403_levanta_erro_de_acesso_negado(tmp_path):
    servico = MagicMock()
    servico.files.return_value.get_media.side_effect = _http_error(403)
    arquivo = ArquivoDrive(
        id="pdf1", nome="artigo.pdf", mime_type="application/pdf", tamanho_bytes=100, modificado_em=None
    )

    with pytest.raises(ErroDeAcessoNegado):
        baixar_arquivo(servico, arquivo, tmp_path / "saida.pdf")


# --- buscar_arquivos ---------------------------------------------------


def test_buscar_sem_nenhum_filtro_levanta_value_error():
    servico = MagicMock()
    with pytest.raises(ValueError):
        buscar_arquivos(servico)
    servico.files.return_value.list.assert_not_called()


def test_buscar_por_nome_monta_query_esperada():
    servico = _servico_de_listagem([{"files": []}])
    buscar_arquivos(servico, nome_contem="Grewe")
    _, kwargs = servico.files.return_value.list.call_args
    assert kwargs["q"] == "trashed = false and name contains 'Grewe'"


def test_buscar_por_texto_completo_e_pasta_combina_clausulas():
    servico = _servico_de_listagem([{"files": []}])
    buscar_arquivos(servico, texto_completo="parasitoses", pasta_id="pasta-x")
    _, kwargs = servico.files.return_value.list.call_args
    assert kwargs["q"] == (
        "trashed = false and fullText contains 'parasitoses' and 'pasta-x' in parents"
    )


def test_buscar_escapa_aspas_simples_no_termo():
    servico = _servico_de_listagem([{"files": []}])
    buscar_arquivos(servico, nome_contem="d'água")
    _, kwargs = servico.files.return_value.list.call_args
    assert "d\\'água" in kwargs["q"]


def test_buscar_retorna_arquivos_encontrados():
    servico = _servico_de_listagem(
        [{"files": [{"id": "x1", "name": "Grewe 1979.pdf", "mimeType": "application/pdf"}]}]
    )
    achados = buscar_arquivos(servico, nome_contem="Grewe")
    assert achados[0].nome == "Grewe 1979.pdf"


# --- exportar_arquivo ----------------------------------------------------


def test_exportar_arquivo_nao_nativo_levanta_erro(tmp_path):
    servico = MagicMock()
    arquivo = ArquivoDrive(
        id="pdf1", nome="artigo.pdf", mime_type="application/pdf", tamanho_bytes=100, modificado_em=None
    )
    with pytest.raises(ErroDeRespostaInesperada):
        exportar_arquivo(servico, arquivo, tmp_path / "saida.pdf")
    servico.files.return_value.export_media.assert_not_called()


def test_exportar_arquivo_sem_formato_padrao_e_sem_override_levanta_erro(tmp_path):
    servico = MagicMock()
    arquivo = ArquivoDrive(
        id="form1",
        nome="Formulário",
        mime_type="application/vnd.google-apps.form",
        tamanho_bytes=None,
        modificado_em=None,
    )
    with pytest.raises(ErroDeRespostaInesperada):
        exportar_arquivo(servico, arquivo, tmp_path / "saida.pdf")


def test_exportar_arquivo_usa_mime_padrao_para_google_docs(tmp_path):
    servico = MagicMock()
    servico.files.return_value.export_media.return_value = MagicMock()
    arquivo = ArquivoDrive(
        id="doc1",
        nome="Documento",
        mime_type="application/vnd.google-apps.document",
        tamanho_bytes=None,
        modificado_em=None,
    )

    with patch("escolio.drive.conector.MediaIoBaseDownload") as downloader_cls:
        instancia = downloader_cls.return_value
        instancia.next_chunk.return_value = (None, True)

        destino = exportar_arquivo(servico, arquivo, tmp_path / "documento.pdf")

    servico.files.return_value.export_media.assert_called_once_with(
        fileId="doc1", mimeType="application/pdf"
    )
    assert destino == tmp_path / "documento.pdf"
    assert destino.exists()


# --- enviar_arquivo --------------------------------------------------------


def _arquivo_local_de_teste(tmp_path, nome="artigo.pdf", conteudo=b"%PDF-1.4 conteudo de teste"):
    caminho = tmp_path / nome
    caminho.write_bytes(conteudo)
    return caminho


def test_enviar_arquivo_monta_metadados_e_devolve_arquivo_drive(tmp_path):
    caminho_local = _arquivo_local_de_teste(tmp_path)
    servico = MagicMock()
    servico.files.return_value.create.return_value.execute.return_value = {
        "id": "novo123",
        "name": "artigo.pdf",
        "mimeType": "application/pdf",
        "size": "27",
        "modifiedTime": "2026-08-10T00:00:00Z",
    }

    with patch("escolio.drive.conector.MediaFileUpload") as media_cls:
        resultado = enviar_arquivo(servico, caminho_local, "pasta-quarentena")

    media_cls.assert_called_once_with(str(caminho_local), mimetype="application/pdf", resumable=True)
    _, kwargs = servico.files.return_value.create.call_args
    assert kwargs["body"] == {"name": "artigo.pdf", "parents": ["pasta-quarentena"]}
    assert resultado == ArquivoDrive(
        id="novo123",
        nome="artigo.pdf",
        mime_type="application/pdf",
        tamanho_bytes=27,
        modificado_em="2026-08-10T00:00:00Z",
    )


def test_enviar_arquivo_permite_nome_e_mime_type_customizados(tmp_path):
    caminho_local = _arquivo_local_de_teste(tmp_path, nome="dados.bin", conteudo=b"x")
    servico = MagicMock()
    servico.files.return_value.create.return_value.execute.return_value = {
        "id": "id1",
        "name": "Artigo Renomeado.pdf",
        "mimeType": "application/pdf",
    }

    with patch("escolio.drive.conector.MediaFileUpload") as media_cls:
        enviar_arquivo(
            servico,
            caminho_local,
            "pasta-quarentena",
            nome="Artigo Renomeado.pdf",
            mime_type="application/pdf",
        )

    media_cls.assert_called_once_with(str(caminho_local), mimetype="application/pdf", resumable=True)
    _, kwargs = servico.files.return_value.create.call_args
    assert kwargs["body"]["name"] == "Artigo Renomeado.pdf"


def test_enviar_arquivo_em_pasta_sem_permissao_de_editor_levanta_acesso_negado(tmp_path):
    caminho_local = _arquivo_local_de_teste(tmp_path)
    servico = MagicMock()
    servico.files.return_value.create.return_value.execute.side_effect = _http_error(403)

    with patch("escolio.drive.conector.MediaFileUpload"), pytest.raises(ErroDeAcessoNegado):
        enviar_arquivo(servico, caminho_local, "pasta-so-leitor")

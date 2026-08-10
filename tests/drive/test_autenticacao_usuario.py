from unittest.mock import MagicMock, patch

import pytest

from escolio.drive.autenticacao_usuario import autorizar_uma_vez, construir_servico_usuario
from escolio.drive.erros import ErroDeCredencial


def _credenciais_fake(*, valid=True, expired=False, refresh_token=None):
    c = MagicMock()
    c.valid = valid
    c.expired = expired
    c.refresh_token = refresh_token
    c.to_json.return_value = '{"fake": "token"}'
    return c


def test_autorizar_com_token_valido_existente_nao_abre_navegador(tmp_path):
    caminho_token = tmp_path / "token.json"
    caminho_token.write_text('{"fake": "token"}', encoding="utf-8")

    with (
        patch(
            "escolio.drive.autenticacao_usuario.Credentials.from_authorized_user_file",
            return_value=_credenciais_fake(valid=True),
        ),
        patch("escolio.drive.autenticacao_usuario.InstalledAppFlow") as fluxo_cls,
    ):
        resultado = autorizar_uma_vez("secrets/client.json", caminho_token)

    fluxo_cls.from_client_secrets_file.assert_not_called()
    assert resultado == caminho_token


def test_autorizar_com_token_expirado_mas_renovavel_so_atualiza(tmp_path):
    caminho_token = tmp_path / "token.json"
    caminho_token.write_text('{"fake": "token"}', encoding="utf-8")
    credenciais = _credenciais_fake(valid=False, expired=True, refresh_token="rt")

    with (
        patch(
            "escolio.drive.autenticacao_usuario.Credentials.from_authorized_user_file",
            return_value=credenciais,
        ),
        patch("escolio.drive.autenticacao_usuario.Request"),
        patch("escolio.drive.autenticacao_usuario.InstalledAppFlow") as fluxo_cls,
    ):
        autorizar_uma_vez("secrets/client.json", caminho_token)

    credenciais.refresh.assert_called_once()
    fluxo_cls.from_client_secrets_file.assert_not_called()
    assert caminho_token.read_text(encoding="utf-8") == '{"fake": "token"}'


def test_autorizar_sem_token_roda_fluxo_interativo(tmp_path):
    caminho_token = tmp_path / "token.json"
    novas_credenciais = _credenciais_fake(valid=True)

    with patch("escolio.drive.autenticacao_usuario.InstalledAppFlow") as fluxo_cls:
        fluxo_cls.from_client_secrets_file.return_value.run_local_server.return_value = novas_credenciais
        autorizar_uma_vez("secrets/client.json", caminho_token)

    fluxo_cls.from_client_secrets_file.assert_called_once_with(
        "secrets/client.json", ["https://www.googleapis.com/auth/drive"]
    )
    assert caminho_token.exists()
    assert caminho_token.read_text(encoding="utf-8") == '{"fake": "token"}'


def test_autorizar_client_secret_ausente_levanta_erro_tipado(tmp_path):
    caminho_token = tmp_path / "token.json"
    with patch("escolio.drive.autenticacao_usuario.InstalledAppFlow") as fluxo_cls:
        fluxo_cls.from_client_secrets_file.side_effect = FileNotFoundError("não achado")
        with pytest.raises(ErroDeCredencial):
            autorizar_uma_vez(tmp_path / "nao-existe.json", caminho_token)


def test_construir_servico_usuario_sem_token_levanta_erro(tmp_path):
    with pytest.raises(ErroDeCredencial):
        construir_servico_usuario(tmp_path / "token-inexistente.json")


def test_construir_servico_usuario_com_token_valido_constroi_servico(tmp_path):
    caminho_token = tmp_path / "token.json"
    caminho_token.write_text('{"fake": "token"}', encoding="utf-8")
    credenciais = _credenciais_fake(valid=True, expired=False)

    with (
        patch(
            "escolio.drive.autenticacao_usuario.Credentials.from_authorized_user_file",
            return_value=credenciais,
        ),
        patch("escolio.drive.autenticacao_usuario.build") as build_fn,
    ):
        construir_servico_usuario(caminho_token)

    build_fn.assert_called_once_with("drive", "v3", credentials=credenciais, cache_discovery=False)


def test_construir_servico_usuario_renova_token_expirado(tmp_path):
    caminho_token = tmp_path / "token.json"
    caminho_token.write_text('{"fake": "token"}', encoding="utf-8")
    credenciais = _credenciais_fake(valid=False, expired=True, refresh_token="rt")

    with (
        patch(
            "escolio.drive.autenticacao_usuario.Credentials.from_authorized_user_file",
            return_value=credenciais,
        ),
        patch("escolio.drive.autenticacao_usuario.Request"),
        patch("escolio.drive.autenticacao_usuario.build"),
    ):
        construir_servico_usuario(caminho_token)

    credenciais.refresh.assert_called_once()
    assert caminho_token.read_text(encoding="utf-8") == '{"fake": "token"}'

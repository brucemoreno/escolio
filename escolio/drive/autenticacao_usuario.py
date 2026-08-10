"""Autorização OAuth como o próprio usuário — resolve LAC-DRIVE-007.

Contas de serviço não têm cota de armazenamento própria: não conseguem
criar arquivo numa pasta comum de conta pessoal, mesmo com permissão de
Editor [`escolio/drive/conector.py::enviar_arquivo`, erro real
`403 storageQuotaExceeded`]. Autenticar como o próprio dono da pasta usa
a cota real dele — sem exigir Google Workspace nem delegação de domínio.

Fluxo interativo, roda uma vez, localmente, por quem tem acesso à conta
Google (abre navegador para consentimento). O token resultante é
cacheado (`secrets/token_usuario.json` por padrão, gitignored) e renovado
automaticamente depois — não pede login de novo a cada execução.
"""

from __future__ import annotations

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build

from .erros import ErroDeCredencial

ESCOPO_USUARIO = ["https://www.googleapis.com/auth/drive"]
"""Escopo completo — é a conta real do usuário se autorizando a si mesma,
não uma identidade terceira pedindo acesso a algo alheio; não há razão
para restringir a `drive.file` aqui."""

CAMINHO_TOKEN_PADRAO = Path("secrets/token_usuario.json")


def autorizar_uma_vez(
    caminho_client_secret: str | Path,
    caminho_token: str | Path = CAMINHO_TOKEN_PADRAO,
) -> Path:
    """Abre o navegador para autorização interativa. `caminho_client_secret`
    é o JSON de "ID do cliente OAuth" (tipo "Aplicativo para computador")
    baixado no console do Google Cloud — diferente do JSON da conta de
    serviço, nunca versionado (mesma regra: `secrets/`, `.gitignore`).

    Chamar de novo quando o token expira e não pode ser renovado
    silenciosamente (ex.: acesso revogado) — detecta e reautoriza.
    Devolve o caminho onde o token foi salvo."""
    caminho_token = Path(caminho_token)
    credenciais = _carregar_token_existente(caminho_token)

    if not credenciais or not credenciais.valid:
        if credenciais and credenciais.expired and credenciais.refresh_token:
            credenciais.refresh(Request())
        else:
            try:
                fluxo = InstalledAppFlow.from_client_secrets_file(
                    str(caminho_client_secret), ESCOPO_USUARIO
                )
            except (OSError, ValueError) as e:
                raise ErroDeCredencial(str(caminho_client_secret), detail=str(e)) from e
            credenciais = fluxo.run_local_server(port=0)
        caminho_token.parent.mkdir(parents=True, exist_ok=True)
        caminho_token.write_text(credenciais.to_json(), encoding="utf-8")
    return caminho_token


def _carregar_token_existente(caminho_token: Path) -> Credentials | None:
    if not caminho_token.exists():
        return None
    return Credentials.from_authorized_user_file(str(caminho_token), ESCOPO_USUARIO)


def construir_servico_usuario(caminho_token: str | Path = CAMINHO_TOKEN_PADRAO) -> Resource:
    """Constrói o serviço Drive autenticado como o usuário, a partir de um
    token já autorizado (ver `autorizar_uma_vez` — precisa ter rodado
    antes, ao menos uma vez). Renova o token automaticamente se expirado
    e ainda tiver `refresh_token` válido, regravando o arquivo."""
    caminho_token = Path(caminho_token)
    credenciais = _carregar_token_existente(caminho_token)
    if credenciais is None:
        raise ErroDeCredencial(
            str(caminho_token),
            detail="token de usuário não encontrado — rodar autorizar_uma_vez() primeiro",
        )
    if credenciais.expired and credenciais.refresh_token:
        credenciais.refresh(Request())
        caminho_token.write_text(credenciais.to_json(), encoding="utf-8")
    return build("drive", "v3", credentials=credenciais, cache_discovery=False)

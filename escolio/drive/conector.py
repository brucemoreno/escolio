"""Conector de leitura ao Google Drive — biblioteca bibliográfica do
professor, compartilhada explicitamente com uma conta de serviço
[docs/backlog.md, BL-027, item (a)].

Escopo estritamente de infraestrutura, mesmo padrão de
`escolio/cliente/cliente.py`: só lista e baixa arquivo. Não decide o que
fazer com o conteúdo, não verifica citação, não aplica BVAA — isso é do
roteador de função e de `escolio/bvaa/`, que ainda não chamam este módulo
[BL-027, itens (b)-(d) em aberto].

Autenticação por conta de serviço: a pasta é compartilhada explicitamente
com o e-mail da conta de serviço (permissão de Leitor), nunca pública —
decisão do professor, 2026-08-09 [docs/backlog.md BL-027]. Escopo OAuth
`drive.readonly` — este conector nunca escreve, modifica ou exclui nada no
Drive.
"""

from __future__ import annotations

import mimetypes
from dataclasses import dataclass
from pathlib import Path

from google.auth.exceptions import GoogleAuthError
from google.oauth2 import service_account
from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from .erros import (
    ErroDeAcessoNegado,
    ErroDeCredencial,
    ErroDeRecursoNaoEncontrado,
    ErroDeRespostaInesperada,
)

ESCOPO_LEITURA = ["https://www.googleapis.com/auth/drive.readonly"]

ESCOPO_LEITURA_E_ESCRITA = ["https://www.googleapis.com/auth/drive"]
"""Escopo completo — não `drive.file`. `drive.file` só concede acesso a
arquivos criados pelo próprio aplicativo ou selecionados pelo usuário via
seletor do Google; uma pasta compartilhada do jeito comum (botão
"Compartilhar" do Drive, e-mail da conta de serviço colado ali) **não**
fica visível sob `drive.file`, mesmo com permissão de Editor concedida —
é limitação documentada da própria API, não bug. Para escrever numa pasta
compartilhada dessa forma (que é como o professor compartilhou "Escolio
Fontes"), o escopo precisa ser o `drive` completo. A proteção real contra
escrita indevida não é o escopo da credencial — é a permissão que cada
pasta concede no Drive: as 5 pastas da biblioteca são Leitor, só "Escolio
Fontes" é Editor. Pedir escopo `drive` só torna a conta de serviço capaz
de *solicitar* escrita; a ACL de cada pasta decide se o pedido é aceito
[ver `escolio/drive/LACUNAS.md`, correção de LAC-DRIVE-007]."""

_CAMPOS_LISTAGEM = "nextPageToken, files(id, name, mimeType, size, modifiedTime)"


@dataclass(frozen=True)
class ArquivoDrive:
    id: str
    nome: str
    mime_type: str
    tamanho_bytes: int | None
    modificado_em: str | None


def construir_servico(caminho_credenciais: str | Path, *, escopos: list[str] | None = None) -> Resource:
    """Autentica com a conta de serviço e devolve o cliente da API do
    Drive v3. `caminho_credenciais` é o arquivo JSON baixado no console do
    Google Cloud — nunca versionado (ver `.gitignore`: `secrets/`,
    `gen-lang-client-*.json`). `escopos` default é só leitura
    (`ESCOPO_LEITURA`) — passar `ESCOPO_LEITURA_E_ESCRITA` explicitamente
    para operações que gravam (`enviar_arquivo`); nunca escrita por
    default silencioso."""
    caminho = str(caminho_credenciais)
    try:
        credenciais = service_account.Credentials.from_service_account_file(
            caminho, scopes=escopos or ESCOPO_LEITURA
        )
    except (OSError, ValueError, GoogleAuthError) as e:
        raise ErroDeCredencial(caminho, detail=str(e)) from e
    return build("drive", "v3", credentials=credenciais, cache_discovery=False)


def _mapear_http_error(e: HttpError, recurso_id: str) -> Exception:
    status = e.resp.status if e.resp is not None else None
    if status == 403:
        return ErroDeAcessoNegado(recurso_id, detail=str(e))
    if status == 404:
        return ErroDeRecursoNaoEncontrado(recurso_id, detail=str(e))
    return ErroDeRespostaInesperada(f"erro HTTP {status} ao acessar '{recurso_id}'", detail=str(e))


def _listar_com_query(servico: Resource, q: str, *, recurso_id_para_erro: str) -> list[ArquivoDrive]:
    """Paginação compartilhada por `listar_arquivos_da_pasta` e
    `buscar_arquivos` — a única diferença entre as duas é a cláusula `q`
    montada por cada uma."""
    arquivos: list[ArquivoDrive] = []
    token_pagina: str | None = None
    while True:
        try:
            resposta = (
                servico.files()
                .list(
                    q=q,
                    fields=_CAMPOS_LISTAGEM,
                    pageToken=token_pagina,
                    pageSize=200,
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                )
                .execute()
            )
        except HttpError as e:
            raise _mapear_http_error(e, recurso_id_para_erro) from e

        for f in resposta.get("files", []):
            arquivos.append(
                ArquivoDrive(
                    id=f["id"],
                    nome=f["name"],
                    mime_type=f["mimeType"],
                    tamanho_bytes=int(f["size"]) if f.get("size") else None,
                    modificado_em=f.get("modifiedTime"),
                )
            )
        token_pagina = resposta.get("nextPageToken")
        if not token_pagina:
            break
    return arquivos


def listar_arquivos_da_pasta(servico: Resource, pasta_id: str) -> list[ArquivoDrive]:
    """Lista todos os arquivos diretamente dentro de `pasta_id` (não
    recursivo — subpastas aparecem como item da lista, tipo
    `application/vnd.google-apps.folder`, não são descidas
    automaticamente; decisão de quem chama se quer recursão, não deste
    conector). `trashed = false` exclui itens na lixeira."""
    q = f"'{pasta_id}' in parents and trashed = false"
    return _listar_com_query(servico, q, recurso_id_para_erro=pasta_id)


def _escapar_valor_de_query(valor: str) -> str:
    """Escapa aspas simples para a sintaxe de `q` da API do Drive — a
    própria documentação da API usa barra invertida para isso, não
    parametrização (a API não aceita query parametrizada como SQL)."""
    return valor.replace("\\", "\\\\").replace("'", "\\'")


def buscar_arquivos(
    servico: Resource,
    *,
    nome_contem: str | None = None,
    texto_completo: str | None = None,
    mime_type: str | None = None,
    pasta_id: str | None = None,
) -> list[ArquivoDrive]:
    """Busca arquivos visíveis à conta de serviço — só o que foi
    compartilhado com ela, nunca o Drive inteiro do Google. Ao menos um
    filtro é obrigatório (`ValueError` se nenhum for dado, para não listar
    "tudo que a conta de serviço enxerga" por engano).

    `texto_completo` usa `fullText contains`, que a API do Drive já
    indexa para PDF, Google Docs e a maioria dos formatos de texto comum
    — não é busca literal exata, é a mesma busca que a interface web do
    Drive oferece. `pasta_id`, quando dado, restringe a busca a uma pasta
    específica (não recursivo pelas mesmas razões de
    `listar_arquivos_da_pasta`); omitido, busca em todas as pastas
    compartilhadas com a conta de serviço."""
    clausulas = ["trashed = false"]
    if nome_contem:
        clausulas.append(f"name contains '{_escapar_valor_de_query(nome_contem)}'")
    if texto_completo:
        clausulas.append(f"fullText contains '{_escapar_valor_de_query(texto_completo)}'")
    if mime_type:
        clausulas.append(f"mimeType = '{_escapar_valor_de_query(mime_type)}'")
    if pasta_id:
        clausulas.append(f"'{pasta_id}' in parents")
    if len(clausulas) == 1:
        raise ValueError(
            "buscar_arquivos exige ao menos um filtro (nome_contem, texto_completo, "
            "mime_type ou pasta_id) — sem filtro listaria tudo que a conta de serviço enxerga"
        )
    q = " and ".join(clausulas)
    return _listar_com_query(servico, q, recurso_id_para_erro=pasta_id or "(busca sem pasta)")


def baixar_arquivo(servico: Resource, arquivo: ArquivoDrive, destino: str | Path) -> Path:
    """Baixa `arquivo` para `destino` (caminho de arquivo, não diretório).
    Só para arquivo binário normal (PDF, .docx, etc.) — Google Docs/
    Planilhas/Apresentações nativos (`application/vnd.google-apps.*`) não
    têm bytes para baixar direto; usar `exportar_arquivo` para esses."""
    if arquivo.mime_type.startswith("application/vnd.google-apps."):
        raise ErroDeRespostaInesperada(
            f"'{arquivo.nome}' ({arquivo.id}) é um arquivo nativo do Google "
            f"({arquivo.mime_type}) — exige exportação, não download direto; "
            "use exportar_arquivo()."
        )
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    try:
        requisicao = servico.files().get_media(fileId=arquivo.id)
        with destino.open("wb") as f:
            downloader = MediaIoBaseDownload(f, requisicao)
            concluido = False
            while not concluido:
                _status, concluido = downloader.next_chunk()
    except HttpError as e:
        raise _mapear_http_error(e, arquivo.id) from e
    return destino


def enviar_arquivo(
    servico: Resource,
    caminho_local: str | Path,
    pasta_id: str,
    *,
    nome: str | None = None,
    mime_type: str | None = None,
) -> ArquivoDrive:
    """Envia um arquivo local para dentro de `pasta_id`. Exige `servico`
    construído com `ESCOPO_LEITURA_E_ESCRITA` — com só leitura, a API
    rejeita antes mesmo de checar a permissão da pasta. A permissão real
    (a pasta aceitar ou não a escrita) é decidida pela ACL do Drive, não
    por este código: enviar para uma pasta onde a conta de serviço só tem
    Leitor levanta `ErroDeAcessoNegado`, igual a qualquer outra chamada.

    **Não funciona contra uma pasta comum de conta pessoal, mesmo com
    Editor concedido** — verificado contra a pasta real "Escolio Fontes"
    em 2026-08-09: a API rejeita com `403 storageQuotaExceeded`, porque
    contas de serviço não têm cota de armazenamento própria (quem cria o
    arquivo é cobrado pela própria cota, não pela da pasta de destino).
    Só funciona hoje contra um Drive Compartilhado (exige Google Workspace)
    ou com `servico` autenticado via OAuth como o próprio usuário dono da
    pasta (não configurado neste projeto). Decisão do professor: não
    perseguir nenhuma das duas por ora — a via real de "disponibilizar
    referência nova" é `baixar_arquivo`/`exportar_arquivo` salvando em
    `data/novas_referencias/` (local) e o professor movendo manualmente.
    Ver `escolio/drive/LACUNAS.md`, LAC-DRIVE-007.

    `nome` default é o nome do arquivo local; `mime_type` default é
    adivinhado por extensão (`mimetypes.guess_type`), `application/
    octet-stream` se não reconhecido."""
    caminho_local = Path(caminho_local)
    nome_final = nome or caminho_local.name
    mime_final = mime_type or mimetypes.guess_type(caminho_local.name)[0] or "application/octet-stream"
    metadados = {"name": nome_final, "parents": [pasta_id]}
    media = MediaFileUpload(str(caminho_local), mimetype=mime_final, resumable=True)
    try:
        resposta = (
            servico.files()
            .create(
                body=metadados,
                media_body=media,
                fields="id, name, mimeType, size, modifiedTime",
                supportsAllDrives=True,
            )
            .execute()
        )
    except HttpError as e:
        raise _mapear_http_error(e, pasta_id) from e
    return ArquivoDrive(
        id=resposta["id"],
        nome=resposta["name"],
        mime_type=resposta["mimeType"],
        tamanho_bytes=int(resposta["size"]) if resposta.get("size") else None,
        modificado_em=resposta.get("modifiedTime"),
    )


MIME_EXPORT_PADRAO: dict[str, str] = {
    "application/vnd.google-apps.document": "application/pdf",
    "application/vnd.google-apps.spreadsheet": "application/pdf",
    "application/vnd.google-apps.presentation": "application/pdf",
}
"""Formato de saída padrão por tipo nativo do Google, quando quem chama
não especifica um. PDF em todos os três casos: é o formato que os parsers
de ingestão já sabem ler (`escolio/ingestao/parser.py`) e preserva layout
melhor que exportar Doc para `.docx` (a conversão do Google para `.docx`
às vezes perde formatação — não medido nesta sessão, decisão por
raciocínio, não por teste)."""


def exportar_arquivo(
    servico: Resource,
    arquivo: ArquivoDrive,
    destino: str | Path,
    *,
    mime_type_exportado: str | None = None,
) -> Path:
    """Exporta um arquivo nativo do Google (Docs/Planilhas/Apresentações)
    para um formato binário comum — esses arquivos não têm bytes próprios
    para baixar direto (ver `baixar_arquivo`). `mime_type_exportado`
    sobrescreve `MIME_EXPORT_PADRAO`; obrigatório para tipos nativos sem
    padrão definido (ex.: Google Forms, Google Drawings)."""
    if not arquivo.mime_type.startswith("application/vnd.google-apps."):
        raise ErroDeRespostaInesperada(
            f"'{arquivo.nome}' ({arquivo.id}) não é um arquivo nativo do Google "
            f"({arquivo.mime_type}) — use baixar_arquivo()."
        )
    mime_saida = mime_type_exportado or MIME_EXPORT_PADRAO.get(arquivo.mime_type)
    if mime_saida is None:
        raise ErroDeRespostaInesperada(
            f"nenhum formato de exportação padrão para '{arquivo.mime_type}' — "
            "informe mime_type_exportado explicitamente"
        )
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    try:
        requisicao = servico.files().export_media(fileId=arquivo.id, mimeType=mime_saida)
        with destino.open("wb") as f:
            downloader = MediaIoBaseDownload(f, requisicao)
            concluido = False
            while not concluido:
                _status, concluido = downloader.next_chunk()
    except HttpError as e:
        raise _mapear_http_error(e, arquivo.id) from e
    return destino

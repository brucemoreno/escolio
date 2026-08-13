"""Curador automático de evidência bibliográfica — sessão de 2026-08-13,
decisão do `USUARIO_PROPONENTE`: a etapa 11 do P13 ("verificação de
fontes") não deve exigir por padrão que um humano já tenha construído
`EvidenciaDeIdentificacaoDrive`/`EvidenciaDeAcessoDrive` — o sistema deve
tentar produzir essa evidência sozinho, por meios já autorizados
(`escolio.drive`, único conector real do projeto — sem web scraping, sem
burlar paywall/DRM, nenhuma chamada nova além das já existentes em
`escolio.drive.conector`), e só escalar para o professor quando
genuinamente travado: acesso ausente, credencial necessária, material
privado, ou decisão humana realmente inescapável.

## Por que este módulo mora em `escolio/funcoes/`, não em `escolio/bvaa/`

Mesma razão de `escolio/funcoes/bvaa_drive.py` — citada verbatim ali:
"`escolio/bvaa/` é puro: (...) nenhuma dependência de rede." Este módulo
depende de `escolio.drive.conector` (chamadas HTTP reais). A extração
determinística de metadados da referência (autor/ano/título a partir do
texto) é a única peça sem I/O, e por isso mora em
`escolio/bvaa/extracao_metadados_referencia.py`; tudo que chama
`escolio.drive` fica aqui, ao lado de `bvaa_drive.py` — que este módulo
reutiliza integralmente (`EvidenciaDeIdentificacaoDrive`,
`EvidenciaDeAcessoDrive`, `OperacaoDeAcesso`), sem duplicar nenhuma
lógica de licenciamento de transição.

## O que este módulo NÃO faz

- Não aplica nenhuma transição da máquina de estados (`escolio.bvaa.
  maquina.avancar`) — só produz os objetos de evidência; quem aplica é
  `escolio/funcoes/execucao_p13.py::_etapa_11_verificacao_de_fontes`,
  mesma separação de responsabilidade que `bvaa_drive.py` já documenta
  para si mesmo (evidência vs. aplicação).
- Não baixa de repositório não configurado, não tenta contornar controle
  de acesso. Só chama `escolio.drive.conector.buscar_arquivos`/
  `baixar_arquivo`/`exportar_arquivo` para acesso real, e
  `escolio.busca.conector.buscar` (opcional, sessão de 2026-08-13, item
  (b) do BL-027) só para *sugerir* candidato quando o Drive não achou
  nada — nunca para baixar ou incorporar.
- Não decide qual resultado de busca é "o arquivo certo" além de tomar o
  primeiro resultado devolvido pela API — mesma limitação estrutural que
  `bvaa_drive.py` já assume para T01-T03 (Drive não distingue obra de
  edição; aqui, múltiplos resultados de busca não são desambiguados por
  julgamento nenhum, código ou modelo). Ver `escolio/bvaa/LACUNAS.md`,
  sessão 2026-08-13, para o registro completo desta limitação.
- **Nunca licencia transição do BVAA a partir de um resultado de busca na
  internet** — só do Drive [`docs/spec/bvaa-drive-integracao.md` §2.1:
  "acesso verificável" é definido como retorno real de
  `escolio.drive.conector`, nunca resultado de busca]. Um resultado de
  `escolio.busca.conector.buscar` vira só `sugestoes_externas` num
  `EscalonamentoDoCurador` — notificação ao professor, nunca evidência.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from typing import Callable

from escolio.busca.conector import ResultadoDeBusca
from escolio.busca.erros import ErroDeBusca
from escolio.bvaa.abstencao import GatilhoDeAbstencao
from escolio.bvaa.extracao_metadados_referencia import (
    MetadadosDeReferenciaExtraidos,
    extrair_metadados_deterministicos,
)
from escolio.drive import conector
from escolio.drive.erros import ErroDeDrive
from escolio.funcoes.bvaa_drive import (
    EvidenciaDeAcessoDrive,
    EvidenciaDeIdentificacaoDrive,
    OperacaoDeAcesso,
)
from escolio.ingestao.modelos import ItemDeReferencia

DIRETORIO_CACHE_CURADOR_PADRAO = Path("data/cache_bvaa")
"""Destino local dos bytes baixados/exportados — mesmo padrão de
`data/cache_cliente/` (cache local do cliente da API): fora do código
versionado, dentro de `data/`, que nunca vai para o git [CLAUDE.md §12].
`[PROPOSTA]`, não medido contra volume real — os capítulos reais não têm
referência alguma a baixar ainda (LAC-ING-017)."""


@dataclass(frozen=True)
class EscalonamentoDoCurador:
    """Parada estruturada e localizada — nunca uma frase de log solta
    [CLAUDE.md §8: "abstenção é ausência de caminho de código, não
    frase"]. `motivo` reaproveita o vocabulário já existente de
    `escolio.bvaa.abstencao.GatilhoDeAbstencao` — nenhum gatilho novo foi
    criado; os dois que este módulo usa (`OBRA_OU_EDICAO_NAO_IDENTIFICADA`
    quando a extração determinística não achou nem autor nem ano;
    `ACESSO_NAO_COMPROVADO` para busca sem resultado, erro do conector ou
    download/exportação que falhou) já cobrem os casos reais que um
    conector só-leitura pode produzir. Nenhum gatilho distingue
    "credencial ausente" de "acesso negado" de "não encontrado" — os três
    ficam sob `ACESSO_NAO_COMPROVADO`, com a distinção preservada só em
    `detalhe` (texto de `ErroDeDrive`, que já carrega `category`/
    `severity`/`code`). Ver `escolio/bvaa/LACUNAS.md`, sessão 2026-08-13,
    para o registro dessa lacuna de granularidade."""

    unit_id: str
    motivo: GatilhoDeAbstencao
    detalhe: str
    referencia_texto: str
    sugestoes_externas: tuple[ResultadoDeBusca, ...] = ()
    """Candidatos de busca na internet (sessão de 2026-08-13, item (b) do
    BL-027) — só populado quando `curar_referencias` recebeu
    `buscar_na_internet` e a busca no Drive não achou nada. Nunca
    incorporados como fonte por si só [BL-027: "avisar, pedir para
    baixar, e só usar depois de disponibilizada"]. Presença aqui é a
    notificação ao professor; download e disponibilização continuam ato
    humano fora deste módulo."""


@dataclass
class ResultadoDoCurador:
    evidencias_de_identificacao: dict[str, EvidenciaDeIdentificacaoDrive] = field(default_factory=dict)
    evidencias_de_acesso: dict[str, EvidenciaDeAcessoDrive] = field(default_factory=dict)
    escalonamentos: list[EscalonamentoDoCurador] = field(default_factory=list)
    metadados_extraidos: dict[str, MetadadosDeReferenciaExtraidos] = field(default_factory=dict)
    """Por `unit_id` — preservado mesmo quando não gerou evidência nem
    escalonamento (ex.: extração parcial, `ano` achado mas `titulo` não),
    para auditoria de por que o curador decidiu o que decidiu."""


def _buscar_no_drive(servico, termo: str, pasta_id: str | None) -> list:
    if pasta_id:
        return conector.buscar_arquivos(servico, texto_completo=termo, pasta_id=pasta_id)
    return conector.buscar_arquivos(servico, texto_completo=termo)


def _tentar_acesso(
    servico, arquivo, unit_id: str, referencia_texto: str, diretorio_cache: Path
) -> tuple[EvidenciaDeAcessoDrive, EscalonamentoDoCurador | None]:
    """T04 (localizado) é licenciado pela própria busca ter devolvido
    `arquivo` — mesma leitura que `bvaa_drive.EvidenciaDeAcessoDrive`
    já formaliza para `OperacaoDeAcesso.LOCALIZADO`. T05 (bytes
    recuperados) só é tentado com o mesmo `servico` já autenticado — nunca
    uma segunda credencial, nunca um mecanismo novo. Se o download/
    exportação falhar, a evidência de T04 é preservada (progresso real,
    não descartado) e um `EscalonamentoDoCurador` cobre especificamente o
    que faltou — "avançar o máximo possível, escalar só o que travou
    genuinamente", não tudo-ou-nada por referência."""
    evidencia_localizado = EvidenciaDeAcessoDrive(arquivo=arquivo, operacao=OperacaoDeAcesso.LOCALIZADO)
    destino = diretorio_cache / f"{unit_id}_{arquivo.id}"
    try:
        if arquivo.mime_type.startswith("application/vnd.google-apps."):
            caminho = conector.exportar_arquivo(servico, arquivo, destino)
            return EvidenciaDeAcessoDrive(arquivo=arquivo, operacao=OperacaoDeAcesso.EXPORTADO, caminho_local=caminho), None
        caminho = conector.baixar_arquivo(servico, arquivo, destino)
        return EvidenciaDeAcessoDrive(arquivo=arquivo, operacao=OperacaoDeAcesso.BAIXADO, caminho_local=caminho), None
    except ErroDeDrive as erro:
        escalonamento = EscalonamentoDoCurador(
            unit_id=unit_id,
            motivo=GatilhoDeAbstencao.ACESSO_NAO_COMPROVADO,
            detalhe=f"arquivo localizado ('{arquivo.nome}'), mas download/exportação falhou: {erro}",
            referencia_texto=referencia_texto,
        )
        return evidencia_localizado, escalonamento


def curar_referencias(
    referencias: list[ItemDeReferencia],
    servico,
    *,
    pasta_id: str | None = None,
    diretorio_cache: Path = DIRETORIO_CACHE_CURADOR_PADRAO,
    buscar_na_internet: Callable[[str], list[ResultadoDeBusca]] | None = None,
) -> ResultadoDoCurador:
    """Para cada `ItemDeReferencia`: extrai metadados determinísticos do
    texto, busca no Drive pelo termo resultante, e tenta acesso real ao
    primeiro resultado. Nunca lança por conta própria de uma referência
    individual não avançar — cada falha (extração vazia, busca sem
    resultado, erro do conector, download que falhou) vira um
    `EscalonamentoDoCurador` na lista de retorno, nunca uma exceção que
    interromperia as referências seguintes. `servico` já autenticado é
    responsabilidade de quem chama — este módulo não constrói credencial
    nem decide se ela existe [`escolio.drive.conector.construir_servico`,
    fora deste módulo].

    `buscar_na_internet` (sessão de 2026-08-13, item (b) do BL-027) é
    opcional e injetado por quem chama — mesmo padrão de `servico`
    (`escolio.busca.conector.buscar` fixado a uma `api_key`, tipicamente
    via `functools.partial`). Só é tentado quando a busca no Drive não
    encontrou nenhum arquivo; nunca substitui o Drive, nunca licencia
    T04/T05 por si — só anexa `sugestoes_externas` ao escalonamento
    resultante, para o professor decidir se disponibiliza a referência."""
    resultado = ResultadoDoCurador()
    for item in referencias:
        metadados = extrair_metadados_deterministicos(item.texto)
        resultado.metadados_extraidos[item.unit_id] = metadados
        termo = metadados.termo_de_busca()
        if termo is None:
            resultado.escalonamentos.append(
                EscalonamentoDoCurador(
                    unit_id=item.unit_id,
                    motivo=GatilhoDeAbstencao.OBRA_OU_EDICAO_NAO_IDENTIFICADA,
                    detalhe=(
                        "extração determinística [escolio.bvaa.extracao_metadados_referencia] não "
                        "encontrou autor nem ano no texto da referência — nenhum termo de busca "
                        "pôde ser construído sem inventar dado que o texto não contém"
                    ),
                    referencia_texto=item.texto,
                )
            )
            continue
        try:
            achados = _buscar_no_drive(servico, termo, pasta_id)
        except ErroDeDrive as erro:
            resultado.escalonamentos.append(
                EscalonamentoDoCurador(
                    unit_id=item.unit_id,
                    motivo=GatilhoDeAbstencao.ACESSO_NAO_COMPROVADO,
                    detalhe=f"busca no Drive falhou para o termo {termo!r}: {erro}",
                    referencia_texto=item.texto,
                )
            )
            continue
        if not achados:
            detalhe = f"nenhum arquivo encontrado no Drive para o termo de busca {termo!r}"
            sugestoes: tuple[ResultadoDeBusca, ...] = ()
            if buscar_na_internet is not None:
                try:
                    sugestoes = tuple(buscar_na_internet(termo))
                except ErroDeBusca as erro:
                    detalhe += f"; busca na internet também falhou: {erro}"
                else:
                    if sugestoes:
                        detalhe += (
                            f"; {len(sugestoes)} candidato(s) encontrado(s) na internet — "
                            "nenhum incorporado automaticamente, aguardando decisão humana de "
                            "disponibilizar [BL-027]"
                        )
            resultado.escalonamentos.append(
                EscalonamentoDoCurador(
                    unit_id=item.unit_id,
                    motivo=GatilhoDeAbstencao.ACESSO_NAO_COMPROVADO,
                    detalhe=detalhe,
                    referencia_texto=item.texto,
                    sugestoes_externas=sugestoes,
                )
            )
            continue
        arquivo = achados[0]
        resultado.evidencias_de_identificacao[item.unit_id] = EvidenciaDeIdentificacaoDrive(
            arquivo=arquivo, referencia_citada=item.texto
        )
        evidencia_acesso, escalonamento = _tentar_acesso(servico, arquivo, item.unit_id, item.texto, diretorio_cache)
        resultado.evidencias_de_acesso[item.unit_id] = evidencia_acesso
        if escalonamento is not None:
            resultado.escalonamentos.append(escalonamento)
    return resultado

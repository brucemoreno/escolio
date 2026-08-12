"""Ligação entre evidência real de acesso ao Drive e a máquina bibliográfica
do P04 (BVAA) — mecanismo desenhado em `docs/spec/bvaa-drive-integracao.md`,
autorizado e construído em 2026-08-12.

## Por que este módulo não mora em `escolio/bvaa/`

`escolio/bvaa/` é puro: 77 testes de unidade, nenhum I/O, nenhuma
dependência de rede. Ligar evidência de acesso ao Drive introduziria ali
uma dependência de `escolio.drive` (autenticação, chamada HTTP). Por
instrução expressa do professor (2026-08-12): a dependência de I/O fica do
lado do orquestrador — este módulo, em `escolio/funcoes/` — nunca dentro da
máquina de estados em si. `escolio/bvaa/` continua sem importar nem saber
que `escolio.drive` existe; este módulo importa dos dois.

## Escopo — só T04/T05, nenhuma outra transição

Acesso ao Drive comprova que um objeto existe e foi recuperado — não que
foi lido, em que página, ou se a citação corresponde ao conteúdo. Por
decisão do professor, este módulo licencia exatamente duas das 18
transições da matriz (`escolio/bvaa/transicoes.py`):

- **T04** (`LOCALIZADA -> ACESSIVEL`) — arquivo localizado por listagem ou
  busca real (`escolio.drive.conector.listar_arquivos_da_pasta`/
  `buscar_arquivos`).
- **T05** (`ACESSIVEL -> ACESSADA`) — bytes recuperados por download ou
  exportação real (`baixar_arquivo`/`exportar_arquivo`).

Nenhuma chamada a este módulo avança um estado até `LEITURA_*`,
`PAGINA_CONFIRMADA`, `VALIDADA` ou `RECOMENDADA` — essas continuam exigindo
juízo humano ou de modelo sobre o conteúdo, ponto de extensão inalterado
[P13 §26].

## T01-T03 — identificação de obra/edição/localização (2026-08-12, segunda peça)

`INSTRUCOES_COMPLEMENTARES_IMPLEMENTACAO_ECOSSISTEMA_REVISAO_LLM_R01.md §3`
delega ao `ENGENHEIRO_LLM` a escolha técnica de mecanismo para T01-T03 — o
pacote P04 é deliberadamente agnóstico a tecnologia (§13 do protocolo:
"não escolhe banco, indexador, API, fornecedor ou plataforma"), e isso não
é lacuna documental a preencher retroativamente, é decisão de escopo do P04
[LAC-BVAA-007/008].

**Escolha desta sessão**: correspondência textual entre o texto de uma
`ItemDeReferencia` (ou autor/ano extraído dela) e o resultado de
`escolio.drive.conector.buscar_arquivos`/`listar_arquivos_da_pasta` — a
mesma fonte de verdade já usada para T04/T05, sem introduzir um segundo
mecanismo de busca bibliográfica. Nenhum catálogo estruturado de metadados
bibliográficos (autor/edição/ano como campos, não texto livre) foi
contratado ou autorizado; o nome do arquivo no Drive é o único metadado
disponível.

**Trade-off documentado** (condição 4, §3.3 das Instruções Complementares):
Drive não distingue "obra" de "edição" como conceitos independentes — um
arquivo é uma obra e uma edição específicas ao mesmo tempo. T01 (obra) e
T02 (edição) são, portanto, licenciados **conjuntamente pela mesma
evidência de correspondência textual** — não há uma segunda fonte de
metadados que confirme edição/volume/tradução separadamente da obra.
Isso é aproximação deliberada, não uma leitura de que T01 e T02 sejam a
mesma coisa na fonte (não são — `escolio/bvaa/transicoes.py` os mantém
como transições distintas, T01 e T02 continuam sendo aplicadas em
sequência, nunca fundidas em uma transição nova). Reversível: se um
catálogo bibliográfico estruturado for contratado depois, licenciar T02
separadamente com evidência própria não exige mudar T01 nem os chamadores
deste módulo — só adicionar uma segunda evidência mais específica.

T03 (localizada) é licenciada pelo mesmo achado de busca: o arquivo
aparecer no resultado de `buscar_arquivos`/`listar_arquivos_da_pasta` já é
"objeto específico encontrado" [T03, `transicoes.py`] — mesma evidência de
`OperacaoDeAcesso.LOCALIZADO` acima, reaproveitada, não duplicada.

Nenhuma decisão sobre qual texto da referência corresponde a qual arquivo
é tomada por este módulo — isso é responsabilidade de quem chama (busca no
Drive, e julgamento se o resultado corresponde à citação), mesma divisão
de trabalho que já vale para `EvidenciaDeAcessoDrive`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from escolio.bvaa.maquina import ResultadoDeTransicao
from escolio.bvaa.maquina import avancar as _aplicar_transicao_bvaa
from escolio.bvaa.vocabulario import EstadoBibliografico
from escolio.drive.conector import ArquivoDrive


class ErroDeEvidenciaDeAcesso(Exception):
    """`caminho_local` incoerente com `operacao` — nunca uma afirmação sem
    o retorno correspondente de `escolio.drive.conector`."""


class OperacaoDeAcesso(str, Enum):
    """Os três efeitos de `escolio.drive.conector` que este módulo trata
    como evidência de acesso — sempre o retorno de uma chamada real, nunca
    a afirmação de que um arquivo existe."""

    LOCALIZADO = "LOCALIZADO"
    """`listar_arquivos_da_pasta`/`buscar_arquivos` devolveu o
    `ArquivoDrive` correspondente — licencia T04."""

    BAIXADO = "BAIXADO"
    """`baixar_arquivo` recuperou bytes com sucesso — licencia T05."""

    EXPORTADO = "EXPORTADO"
    """`exportar_arquivo` recuperou bytes com sucesso — mesmo tratamento de
    `BAIXADO`; arquivo nativo do Google exportado, não baixado direto
    [LAC-DRIVE-002]. Licencia T05."""


_TRANSICAO_POR_OPERACAO: dict[OperacaoDeAcesso, str] = {
    OperacaoDeAcesso.LOCALIZADO: "T04",
    OperacaoDeAcesso.BAIXADO: "T05",
    OperacaoDeAcesso.EXPORTADO: "T05",
}


@dataclass(frozen=True)
class EvidenciaDeAcessoDrive:
    """Construída inteiramente a partir do retorno já existente de
    `escolio.drive.conector` — nenhuma chamada nova ao Drive é feita por
    este módulo."""

    arquivo: ArquivoDrive
    operacao: OperacaoDeAcesso
    caminho_local: Path | None = None

    def __post_init__(self) -> None:
        exige_caminho = self.operacao in (OperacaoDeAcesso.BAIXADO, OperacaoDeAcesso.EXPORTADO)
        if exige_caminho and self.caminho_local is None:
            raise ErroDeEvidenciaDeAcesso(
                f"operacao={self.operacao.value} exige caminho_local — resultado real de "
                "baixar_arquivo/exportar_arquivo, não uma afirmação sem retorno de bytes"
            )
        if not exige_caminho and self.caminho_local is not None:
            raise ErroDeEvidenciaDeAcesso(
                f"operacao={self.operacao.value} não recupera bytes — caminho_local deve ser None"
            )


def transicao_licenciada_por(evidencia: EvidenciaDeAcessoDrive) -> str:
    """`T04` ou `T05` — nunca outra transição da matriz de 18. Total sobre
    os três membros de `OperacaoDeAcesso`: não há caso que devolva `None`."""
    return _TRANSICAO_POR_OPERACAO[evidencia.operacao]


def avancar_por_evidencia(
    estado_atual: EstadoBibliografico, evidencia: EvidenciaDeAcessoDrive
) -> ResultadoDeTransicao:
    """Decide a transição licenciada pela evidência e aplica-a via
    `escolio.bvaa.maquina.avancar` — a única chamada deste módulo à máquina
    de estados em si; nenhuma lógica de transição é duplicada aqui.

    Propaga `escolio.bvaa.erros.ErroDeTransicaoBibliografica` sem capturar:
    se `estado_atual` não é o `estado_entrada` que T04/T05 exige (ex.: a
    fonte ainda não passou por T01-T03 — identificação de obra, edição e
    localização, que evidência de Drive não comprova), a evidência de
    acesso não licencia nada a partir daqui, e este módulo não disfarça
    isso como sucesso parcial."""
    transicao_id = transicao_licenciada_por(evidencia)
    return _aplicar_transicao_bvaa(estado_atual, transicao_id)


_CADEIA_DE_IDENTIFICACAO: tuple[str, ...] = ("T01", "T02", "T03")


@dataclass(frozen=True)
class EvidenciaDeIdentificacaoDrive:
    """Correspondência textual entre uma referência citada e um arquivo
    real do Drive — construída inteiramente a partir do retorno já
    existente de `escolio.drive.conector` (`buscar_arquivos`/
    `listar_arquivos_da_pasta`), nenhuma chamada nova ao Drive.

    `referencia_citada` é o texto que fundamentou a correspondência (ex.:
    `ItemDeReferencia.texto`, ou o autor/ano extraído dela) — preservado
    para auditoria de por que este arquivo foi considerado o mesmo que a
    citação, nunca usado por este módulo para decidir a correspondência
    (isso é julgamento de quem chama)."""

    arquivo: ArquivoDrive
    referencia_citada: str

    def __post_init__(self) -> None:
        if not self.referencia_citada.strip():
            raise ErroDeEvidenciaDeAcesso(
                "referencia_citada vazia — correspondência sem o texto que a fundamenta não é "
                "auditável (mesma exigência de evidência localizada de CLAUDE.md)"
            )


def avancar_por_identificacao(
    estado_atual: EstadoBibliografico, evidencia: EvidenciaDeIdentificacaoDrive
) -> ResultadoDeTransicao:
    """Aplica T01, T02 e T03 em sequência a partir da mesma evidência de
    correspondência textual [PROPOSTA — trade-off documentado no docstring
    do módulo: Drive não distingue obra de edição, então a mesma evidência
    licencia as duas]. Exige `estado_atual == OBRA_NAO_IDENTIFICADA` —
    propaga `ErroDeTransicaoBibliografica` sem capturar quando não for
    (mesma disciplina de `avancar_por_evidencia`: este módulo não amortece
    rejeição da máquina de estados).

    `ResultadoDeTransicao.transicao_id` do retorno é `"T01+T02+T03"` — rótulo
    composto desta função, não um id da matriz de 18; cada transição
    individual foi de fato aplicada via `escolio.bvaa.maquina.avancar`, em
    sequência, nunca fundida numa transição nova."""
    estado = estado_atual
    for transicao_id in _CADEIA_DE_IDENTIFICACAO:
        estado = _aplicar_transicao_bvaa(estado, transicao_id).estado_novo
    return ResultadoDeTransicao(
        estado_anterior=estado_atual, estado_novo=estado, transicao_id="+".join(_CADEIA_DE_IDENTIFICACAO)
    )

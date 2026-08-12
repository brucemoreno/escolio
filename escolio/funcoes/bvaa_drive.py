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
[P13 §26]. Identificação de obra/edição (T01-T03) também não é tratada
aqui: `aplicar_transicao` (`escolio/bvaa/transicoes.py`) já rejeita T04/T05
quando o estado atual não é o `estado_entrada` exigido — este módulo não
amortece essa rejeição, propaga-a.
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

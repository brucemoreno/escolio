"""Extração determinística de metadados de uma entrada bibliográfica —
sessão de 2026-08-13 (curador automático BVAA, decisão do
`USUARIO_PROPONENTE`: o sistema deve produzir evidência de
identificação/localização automaticamente quando possível, em vez de
exigir que um humano já a tenha fornecida).

Módulo puro, sem I/O — mesma disciplina do resto de `escolio/bvaa/`
(ver docstring de `escolio/bvaa/vocabulario.py`: "77 testes de unidade,
nenhum I/O, nenhuma dependência de rede"). Opera só sobre
`ItemDeReferencia.texto` [`escolio/ingestao/modelos.py`] — texto livre já
extraído do documento por `escolio/ingestao/`; nenhuma chamada de rede,
nenhuma consulta a `escolio.drive` — isso é responsabilidade de quem
chama (`escolio/funcoes/curador_bvaa.py`), mesma separação que
`escolio/bvaa/correspondencia.py` já documenta para si mesmo.

## Por que só regex sobre ABNT convencional, e nunca "adivinhação"

Nenhuma fonte do P04 declara um parser de referência bibliográfica — não
existe porque o P04 é agnóstico a formato de citação, só a estados de
evidência sobre uma obra já identificada [ver `escolio/bvaa/LACUNAS.md`,
LAC-BVAA-007/008: "P04 não escolhe banco, indexador, API, fornecedor ou
plataforma"]. Esta extração não é regra do P04 — é engenharia desta
sessão, `[PROPOSTA]`, para dar ao curador algo determinístico a partir do
qual construir um termo de busca, sem inventar autor/título/ano que a
string não contém literalmente. Campo que a regex não consegue extrair
com confiança fica `None` — nunca um palpite ["Nada inferido", CLAUDE.md
§11].

**Não calibrado contra nenhuma referência real.** Os três capítulos reais
de `data/capitulos/` não têm seção de referências (`LAC-ING-017`,
`escolio/ingestao/LACUNAS.md`) — `DocumentoIngerido.referencias` é `[]`
para eles. Esta extração nunca foi exercitada contra um `ItemDeReferencia.
texto` real; só contra exemplos ABNT sintéticos nos testes. Ver
`escolio/bvaa/LACUNAS.md`, sessão 2026-08-13.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_PADRAO_ANO = re.compile(r"\b(1[5-9]\d{2}|20\d{2})\b")
"""Ano de publicação plausível: 1500-2099. Faixa larga o suficiente para
não excluir obras antigas citadas em história da ciência, sem aceitar
qualquer sequência de 4 dígitos (ex.: um número de página de 4 dígitos,
raro mas possível, ficaria fora só se estiver fora desta faixa — risco
residual documentado, não eliminado)."""

_PADRAO_SOBRENOME = re.compile(r"^[A-ZÀ-ÖØ-Þ][A-ZÀ-ÖØ-Þ'\- ]{1,59}$")
"""Sobrenome em maiúsculas — convenção ABNT do primeiro elemento de uma
referência ("SOBRENOME, Nome..."). Rejeita qualquer coisa com dígito,
minúscula ou pontuação além de hífen/apóstrofo — candidato que não bate
exatamente com essa forma vira `None`, nunca um palpite parcial."""


@dataclass(frozen=True)
class MetadadosDeReferenciaExtraidos:
    """Resultado da extração — todo campo é `None` quando a regex não
    encontrou correspondência confiável no texto. `texto_origem` é
    preservado para proveniência: todo consumidor deste objeto pode citar
    exatamente de onde o dado veio [CLAUDE.md §8: "provenance vazio não
    grava"]."""

    texto_origem: str
    autor_sobrenome: str | None
    ano: str | None
    titulo: str | None
    metodo: str = "REGEX_ABNT_DETERMINISTICO"

    def termo_de_busca(self) -> str | None:
        """Junção dos campos disponíveis para uso em busca textual (ex.:
        `escolio.drive.conector.buscar_arquivos(texto_completo=...)`).
        `None` quando nem autor nem ano foram extraídos — sem nenhum dos
        dois, nenhum termo de busca com chance real de corresponder pode
        ser construído sem inventar dado que a referência não contém."""
        partes = [p for p in (self.autor_sobrenome, self.ano) if p]
        if not partes:
            return None
        return " ".join(partes)


def _extrair_sobrenome(texto: str) -> str | None:
    primeiro_campo = texto.split(",", 1)[0].strip()
    if _PADRAO_SOBRENOME.match(primeiro_campo):
        return primeiro_campo
    return None


def _extrair_ano(texto: str) -> str | None:
    correspondencias = _PADRAO_ANO.findall(texto)
    if not correspondencias:
        return None
    # ABNT convencional coloca o ano de publicação no fim da referência
    # (após editora) — a última correspondência é a leitura mais provável,
    # não a primeira (que poderia ser um ano citado dentro do próprio
    # título, ex. um livro sobre um evento histórico datado).
    return correspondencias[-1]


def _extrair_titulo(texto: str, ano: str | None) -> str | None:
    """Segundo campo delimitado por ponto, na forma ABNT "SOBRENOME, Nome.
    Título. Cidade: Editora, Ano." — só aceito quando o candidato não
    contém o próprio ano extraído (sinal de que o split pegou o campo
    errado) e tem tamanho plausível de título, nunca aceito por padrão
    quando esses dois filtros falham."""
    campos = [c.strip() for c in texto.split(".") if c.strip()]
    if len(campos) < 2:
        return None
    candidato = campos[1]
    if ano and ano in candidato:
        return None
    if not (3 <= len(candidato) <= 200):
        return None
    return candidato


def extrair_metadados_deterministicos(texto: str) -> MetadadosDeReferenciaExtraidos:
    """Extrai autor/ano/título de `texto` (tipicamente
    `ItemDeReferencia.texto`) por regex determinística — nenhuma chamada
    de rede, nenhum modelo. Campo não extraível fica `None`; nunca um
    valor plausível não confirmado pelo texto literal."""
    ano = _extrair_ano(texto)
    return MetadadosDeReferenciaExtraidos(
        texto_origem=texto,
        autor_sobrenome=_extrair_sobrenome(texto),
        ano=ano,
        titulo=_extrair_titulo(texto, ano),
    )

"""Fronteira corpus sintético vs. material real — DTA-22, DTA-23, DTA-24.

Fonte: docs/spec/operacional-P08.md §7. [P19 §72] item 1 proíbe
"classificar material real"; [P19 §71] autoriza construir e testar contra
fixtures sintéticas. "Construir não é executar" [mapa-P08.md §6.1,
RD-25]: o classificador pode ser construído e testado agora, contra
corpus sintético, sem esperar homologação do P19 — o vedado é rodá-lo
contra material real e gravar o resultado como classificação vigente.

DTA-22: a trava é explícita e levanta exceção — recusa qualquer caminho
sob `data/` (inclusive `data/dev/`, que é material real do projeto,
diferente de `ErroDeEscopoDeDados` em escolio/ingestao/erros.py, que
cobre só "fora de data/dev/"). Alternativa descartada: confiar em
disciplina de chamador — é o estado atual de `ErroDeEscopoDeDados`, que
existe desde a peça de ingestão e nunca é levantada em tempo de execução
(parser.py:152-156 declara explicitamente que não impõe a restrição) —
essa alternativa já demonstrou o problema.
"""

import re
from pathlib import PurePosixPath

from escolio.seguranca.erros import ErroDeEscopoDeSeguranca

PADRAO_DATA = re.compile(r"(^|[/\\])data([/\\]|$)")


def recusa_caminho_sob_data(caminho: str) -> None:
    """Levanta `ErroDeEscopoDeSeguranca` quando `caminho` está sob um
    diretório `data/` (em qualquer posição do caminho, absoluto ou
    relativo, com `/` ou `\\`). Não normaliza para checar existência no
    disco — a trava é sobre a forma do caminho recebido, não sobre o que
    ele resolve a ser; um caminho pode não existir e ainda assim declarar
    intenção de acessar `data/`."""
    normalizado = str(PurePosixPath(caminho.replace("\\", "/")))
    if PADRAO_DATA.search(normalizado) or normalizado in ("data",) or normalizado.startswith("data/"):
        raise ErroDeEscopoDeSeguranca(caminho)


MARCADOR_SINTETICO = "[SINTETICO]"
"""DTA-23 — toda fixture sintética carrega este marcador de procedência.
Nunca derivada de documento de aluno, nem por paráfrase, nem por
anonimização — [P19 §19] e PR-06 dizem que remover nomes produz no
máximo DADO_PSEUDONIMIZADO, e trecho pseudonimizado de material real
continua material real. Coerente com CLAUDE.md §9, "procedência sobrevive
à destilação"."""


def exige_marcador_sintetico(texto: str) -> None:
    """Levanta `ErroDeEscopoDeSeguranca`-like via `ErroDeSeguranca` quando
    `texto` não carrega `MARCADOR_SINTETICO`. Usado pelas fixtures de
    teste para impedir que texto sem procedência declarada entre na
    suíte adversarial como se fosse sintético."""
    from escolio.seguranca.erros import ErroDeSeguranca

    if MARCADOR_SINTETICO not in texto:
        raise ErroDeSeguranca(
            "DTA-23",
            "fixture de cenário adversarial sem marcador de procedência [SINTETICO]",
            arquivo_origem="docs/spec/operacional-P08.md",
            detalhe="toda fixture sintética deve carregar o marcador — nunca derivada de material real",
        )

"""Exceções do módulo de ingestão.

Mesmo padrão de escolio/erros.py: toda rejeição é rastreável, mas aqui não
há "regra de coerência" externa a citar — a ingestão rejeita apenas quando
o próprio PDF é ilegível ou o material pedido está fora do escopo
autorizado (data/dev/).
"""


class ErroDeIngestao(Exception):
    """Falha ao processar o documento (arquivo ilegível, corrompido, etc.)."""


class ErroDeEscopoDeDados(Exception):
    """Tentativa de acessar material fora de data/dev/ (ex.: data/gold/).

    data/gold/ é reservado para avaliação futura; ler seu conteúdo agora
    invalidaria a avaliação. Este módulo não abre nada fora de data/dev/
    sob nenhuma circunstância — ver escolio/ingestao/LACUNAS.md.
    """

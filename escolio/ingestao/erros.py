"""Exceções do módulo de ingestão.

Mesmo padrão de escolio/erros.py: toda rejeição é rastreável, mas aqui não
há "regra de coerência" externa a citar — a ingestão rejeita apenas quando
o próprio arquivo é ilegível ou o material pedido está fora do escopo
autorizado. Escopo autorizado é por parser, não um caminho único: o
parser de PDF (`parser.py`) lê `data/dev/`; o parser de `.docx`
(`parser_docx.py`) lê `data/capitulos/`. `data/gold/` é barrado para os
dois, sem exceção — reservado para avaliação futura.
"""


class ErroDeIngestao(Exception):
    """Falha ao processar o documento (arquivo ilegível, corrompido, etc.)."""


class ErroDeEscopoDeDados(Exception):
    """Tentativa de acessar material fora do escopo autorizado do parser
    que chama (ex.: data/gold/, ou o diretório de outro parser).

    data/gold/ é reservado para avaliação futura; ler seu conteúdo agora
    invalidaria a avaliação. Nenhum módulo de ingestão abre nada fora do
    seu próprio escopo autorizado sob nenhuma circunstância — ver
    escolio/ingestao/LACUNAS.md.
    """

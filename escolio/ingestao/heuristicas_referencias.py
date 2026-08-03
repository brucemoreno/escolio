"""Heurística de segmentação da lista de referências em itens — RG-008
em FORMATO.md.

Fundamento empírico: dentro da seção "Referências Bibliográficas", todas
as linhas (primeira linha de cada item e continuações) começam no mesmo
x0≈56.6 — ao contrário do corpo do texto, a lista de referências não usa
recuo de primeira linha. O que separa um item do próximo é o espaço
vertical: linhas do MESMO item têm gap ≈15.8-16.0pt entre si; a
passagem para um NOVO item tem gap ≈33.8-34.0pt — pouco mais do dobro.

Isto é medido no documento real (páginas 29-33), não assumido como regra
ABNT genérica. Um documento com espaçamento diferente exigiria
recalibração do limiar — ver LACUNAS.md.
"""

FATOR_GAP_NOVO_ITEM = 1.6
"""Um gap de linha maior que este fator vezes o gap típico
intra-item indica novo item de referência. 1.6 fica entre a razão
observada (~2.1) e 1.0 (mesmo espaçamento), com folga para pequena
variação de página a página sem confundir com quebra de página real
(que o parser trata separadamente, por operar página a página)."""


def linha_inicia_novo_item(gap_para_linha_anterior: float | None, gap_tipico_intra_item: float) -> bool:
    """`gap_para_linha_anterior` é None na primeira linha da seção de
    referências (sempre início de item) ou na primeira linha de uma nova
    página (tratado à parte pelo parser, pois o gap não é comparável
    entre páginas)."""
    if gap_para_linha_anterior is None:
        return True
    return gap_para_linha_anterior >= gap_tipico_intra_item * FATOR_GAP_NOVO_ITEM

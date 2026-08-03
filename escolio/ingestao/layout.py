"""Primitivas de layout sobre pdfplumber: agrupamento de caracteres em
linhas e extração de atributos de linha (posição, fonte, tamanho, negrito).

Módulo isolado do parser porque estas funções não têm heurística de
domínio (não decidem o que é título ou nota) — apenas normalizam o que o
pdfplumber expõe por caractere em algo por linha, sobre o qual o parser
aplica as regras documentadas em FORMATO.md.
"""

from dataclasses import dataclass


@dataclass
class Linha:
    pagina: int  # base 1
    top: float
    x0: float
    x1: float
    texto: str
    tamanhos: frozenset
    """Conjunto dos tamanhos de fonte distintos presentes na linha —
    frozenset, não um único valor, porque uma linha pode misturar
    tamanhos (ex.: número de nota em sobrescrito menor que o corpo)."""
    totalmente_negrito: bool
    """True apenas se TODO caractere não-espaço da linha usa uma fonte
    'Bold'. Uma palavra em negrito no meio de um parágrafo não torna a
    linha 'totalmente_negrito' — ver RG-001 em FORMATO.md sobre o falso
    positivo de ênfase interna."""
    algum_negrito: bool
    chars: list


TOLERANCIA_MESMA_LINHA = 2.0
"""Diferença máxima de `top`, em pontos, para considerar dois grupos de
caracteres como a mesma linha visual. Necessário porque um caractere em
sobrescrito (ex.: chamada de nota de rodapé) tem baseline ligeiramente
deslocado do texto ao redor — constatado no documento real: a chamada
'1' de uma nota tem top=674.0 enquanto o texto '(Grewe, 1979, p. 13).'
da mesma linha visual tem top=674.8 (deslocamento de 0.8pt). Sem esta
tolerância, agrupar estritamente por `top` arredondado quebra a chamada
em uma `Linha` separada do texto que a cerca, e a heurística de notas
(heuristicas_notas.py) nunca vê os dois juntos. 2.0pt dá folga sobre o
0.8pt medido sem chegar perto do espaçamento entre linhas real (~15.8pt
na lista de referências, o menor do documento) — ver FORMATO.md RG-005."""


def extrair_linhas(page) -> list[Linha]:
    """Agrupa os caracteres de uma página em linhas visuais. Caracteres
    cujo `top` cai dentro de TOLERANCIA_MESMA_LINHA de um grupo já aberto
    são anexados a ele (cobre sobrescrito/subscrito na mesma linha);
    caso contrário abre um novo grupo. Ordem de saída: topo->baixo, que é
    a ordem de leitura da página para um layout de coluna única — este
    corpus não tem colunas múltiplas (ver LACUNAS.md)."""
    grupos: list[list] = []  # cada grupo é uma lista de chars de uma linha visual
    tops_grupo: list[float] = []  # top do primeiro char de cada grupo (referência de comparação)

    for ch in page.chars:
        if not ch["text"].strip() and ch["text"] != " ":
            continue
        top = round(ch["top"], 1)
        encontrado = False
        for i, top_ref in enumerate(tops_grupo):
            if abs(top - top_ref) <= TOLERANCIA_MESMA_LINHA:
                grupos[i].append(ch)
                encontrado = True
                break
        if not encontrado:
            grupos.append([ch])
            tops_grupo.append(top)

    linhas = []
    for chars in grupos:
        chars = sorted(chars, key=lambda c: c["x0"])
        top = round(min(c["top"] for c in chars), 1)
        texto = "".join(c["text"] for c in chars)
        if not texto.strip():
            continue
        nao_espacos = [c for c in chars if c["text"].strip()]
        tamanhos = frozenset(round(c["size"], 1) for c in nao_espacos)
        totalmente_negrito = all("Bold" in c["fontname"] for c in nao_espacos)
        algum_negrito = any("Bold" in c["fontname"] for c in nao_espacos)
        linhas.append(
            Linha(
                pagina=page.page_number,
                top=top,
                x0=min(c["x0"] for c in chars),
                x1=max(c["x1"] for c in chars),
                texto=texto,
                tamanhos=tamanhos,
                totalmente_negrito=totalmente_negrito,
                algum_negrito=algum_negrito,
                chars=chars,
            )
        )
    linhas.sort(key=lambda l: l.top)
    return linhas

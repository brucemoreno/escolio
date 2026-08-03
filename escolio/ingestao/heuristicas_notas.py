"""Heurística de detecção de notas de rodapé — RG-005 em FORMATO.md.

Fundamento empírico: neste documento, a chamada de nota no corpo é um
dígito isolado em tamanho de fonte visivelmente menor que o texto ao
redor (6.5pt contra 10-12pt do corpo), imediatamente após a pontuação
que fecha a frase/citação. No rodapé da mesma página, a nota começa com
o mesmo número no mesmo tamanho reduzido (6.5pt), seguido do corpo da
nota em tamanho maior (10pt neste documento — não 6.5; o número da nota
é menor que seu próprio corpo de texto).

Isto NÃO é uma regra genérica de "todo PDF acadêmico usa 6.5pt para
notas" — é o que foi medido neste arquivo. Documentos diferentes podem
usar outro tamanho; por isso os limiares abaixo são parâmetros nomeados,
não valores mágicos espalhados pelo código, para facilitar recalibração
quando um segundo documento real estiver disponível (ver LACUNAS.md
sobre a impossibilidade de generalizar com um único documento de
desenvolvimento).
"""

import re

from escolio.ingestao.layout import Linha

DIFERENCA_MINIMA_TAMANHO_CHAMADA = 1.5
"""Uma chamada de nota deve ter tamanho de fonte pelo menos esta
quantidade de pontos menor que o tamanho predominante da linha em que
aparece — evita marcar como chamada um dígito comum de tamanho normal
(ex.: um número dentro de uma citação como '(Grewe, 1979, p. 13)')."""

PADRAO_NUMERO_NOTA_RODAPE = re.compile(r"^\s*(\d+)\s+(.*)$", re.DOTALL)
"""Uma linha de rodapé que começa com um número (a numeração da nota)
seguido de espaço e o texto da nota."""


def tamanho_predominante(linha: Linha) -> float:
    """Tamanho de fonte mais frequente entre os caracteres não-espaço da
    linha — usado como 'tamanho do corpo local' para comparar com
    possíveis chamadas de nota na mesma linha."""
    contagem: dict[float, int] = {}
    for c in linha.chars:
        if not c["text"].strip():
            continue
        tam = round(c["size"], 1)
        contagem[tam] = contagem.get(tam, 0) + 1
    if not contagem:
        return 0.0
    return max(contagem, key=lambda t: contagem[t])


def encontrar_chamadas_de_nota(linha: Linha) -> list[tuple[str, int, float]]:
    """Retorna [(digito, posicao_no_texto_da_linha, tamanho), ...] para
    cada dígito da linha cujo tamanho é visivelmente menor que o tamanho
    predominante da própria linha — candidato a chamada de nota de
    rodapé (RG-005). Não decide sozinho que é uma nota: o parser ainda
    precisa achar o corpo correspondente no rodapé da página."""
    tam_base = tamanho_predominante(linha)
    if tam_base == 0.0:
        return []
    achados = []
    pos = 0
    for c in linha.chars:
        if c["text"].isdigit():
            tam = round(c["size"], 1)
            if tam_base - tam >= DIFERENCA_MINIMA_TAMANHO_CHAMADA:
                achados.append((c["text"], pos, tam))
        pos += len(c["text"])
    return achados


def linha_e_corpo_de_nota(linha: Linha, tamanho_chamada_esperado: float, tolerancia: float = 0.3) -> tuple[str, str] | None:
    """Se a linha começa com um número no tamanho característico de
    chamada de nota (mesmo tamanho medido no corpo, dentro da
    tolerância), retorna (numero, resto_do_texto). Caso contrário, None."""
    if not linha.chars:
        return None
    primeiro = linha.chars[0]
    if not primeiro["text"].isdigit():
        return None
    if abs(round(primeiro["size"], 1) - tamanho_chamada_esperado) > tolerancia:
        return None
    m = PADRAO_NUMERO_NOTA_RODAPE.match(linha.texto)
    if not m:
        return None
    return m.group(1), m.group(2)

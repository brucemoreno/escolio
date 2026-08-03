"""Heurística de agrupamento de linhas em parágrafos — RG-003 em
FORMATO.md.

Fundamento empírico: no corpo deste documento, a primeira linha de um
parágrafo começa em x0≈92 (recuo de primeira linha) e as linhas
seguintes do mesmo parágrafo em x0≈57 (margem do corpo), com espaço
entre linhas de ≈20.7pt. Uma nova primeira linha (x0≈92) fecha o
parágrafo anterior e abre um novo.

RG-004 (preservação literal — revista após checagem contra o documento
real): o prompt permite remover o hífen "quando for hifenização de fim
de linha". A tentativa inicial desta implementação tratava TODO hífen no
fim de uma linha como hifenização de quebra e o removia. Checagem contra
as 6 ocorrências reais de hífen em fim de linha neste documento mostrou
que essa premissa era falsa: nenhuma das 6 é hífen de quebra tipográfica
pura — são hífens que pertencem à palavra (clíticos verbais como
"destacam-se", "transformando-se"; compostos como "luso-brasileiro",
"físico-químicos", "ibero-americano") ou pontuação de um intervalo de
páginas em referência ("593-610"). Remover o hífen nesses casos
CORROMPE o texto (produz "destacamse", que não é a palavra original).

Sem um dicionário de português para decidir se uma palavra é normalmente
hifenizada, não há como distinguir com segurança hífen-de-quebra de
hífen-que-pertence-à-palavra a partir apenas do layout. Por isso esta
implementação NÃO remove nenhum hífen de fim de linha — concatena
sempre preservando o hífen literal (junção sem espaço extra, já que o
hífen já funciona como a junção visual da palavra), e sinaliza a
ocorrência para o relatório de ingestão, porque a decisão "hífen
pertence à palavra vs. hífen é artefato de quebra" fica para revisão
humana, não para o parser. Ver LACUNAS.md.
"""

from escolio.ingestao.layout import Linha

X0_RECUO_PRIMEIRA_LINHA_MIN = 80.0
"""Abaixo deste valor, x0 é considerado 'margem do corpo' (continuação),
não recuo de primeira linha. Calibrado empiricamente: recuo real ≈92,
margem real ≈57 neste documento — 80 fica a meio caminho, com folga para
variação de alguns pontos entre páginas."""


def linha_inicia_paragrafo(linha: Linha) -> bool:
    return linha.x0 >= X0_RECUO_PRIMEIRA_LINHA_MIN


def texto_termina_em_hifen_de_fim_de_linha(texto: str) -> bool:
    """Sinaliza a ocorrência (para o relatório) sem decidir o que fazer
    com ela — ver RG-004 revisado no docstring do módulo."""
    texto = texto.rstrip()
    return bool(texto) and texto[-1] == "-" and len(texto) > 1 and texto[-2].isalnum()


def concatenar_preservando_texto_literal(texto_acumulado: str, nova_linha: str) -> tuple[str, bool]:
    """Une o texto acumulado do parágrafo com uma nova linha, sempre
    preservando os caracteres originais — nenhum hífen é removido (ver
    RG-004 revisado). Retorna (texto_unido, linha_anterior_terminava_em_hifen)
    para que o chamador conte a ocorrência no relatório de ingestão."""
    houve_hifen = texto_termina_em_hifen_de_fim_de_linha(texto_acumulado)
    if not texto_acumulado:
        return nova_linha, False
    if houve_hifen:
        # Hífen preservado; nenhum espaço inserido entre o hífen e a
        # continuação, pois é assim que a palavra/trecho aparece
        # visualmente no documento — inserir espaço aqui criaria um
        # artefato que não existe no original ("destacam- se").
        return texto_acumulado.rstrip() + nova_linha.lstrip(), True
    return texto_acumulado.rstrip() + " " + nova_linha.lstrip(), False

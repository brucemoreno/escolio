"""Heurística de citações — RG-006 (recuada) e RG-007 (autor-data ABNT)
em FORMATO.md.

RG-006 — citação recuada: bloco de texto com recuo à esquerda
substancialmente maior que a margem do corpo. Medido neste documento:
corpo em x0≈56.6/92 (margem/recuo de parágrafo), bloco de citação longa
em x0≈162.9 — usa também fonte reduzida (10pt) onde o corpo ao redor é
12pt, mas o limiar de posição sozinho já separa com folga (162.9 vs
92 do recuo de primeira linha).

RG-007 — citação autor-data no corpo: duas formas ABNT, com confiabilidade
diferente sem cross-checagem:

  1. Parentética "(AUTOR, ano[, p. N])" ou "(AUTOR; AUTOR2, ano)" — forma
     inconfundível: maiúsculas + vírgula + ano de 4 dígitos dentro de
     parênteses. Aceita diretamente.

  2. Narrativa "Autor (ano)" — AMBÍGUA: um substantivo próprio qualquer
     seguido de um número entre parênteses casa com o mesmo padrão
     textual (constatado nos dados reais: "o manuscrito da Infanta D.
     Maria (1987)" NÃO é uma citação de um autor chamado "Infanta" ou
     "Maria" — é o nome do objeto de estudo seguido do ano de uma edição
     citada em outro lugar). Sem heurística sintática que distinga os
     dois casos com segurança, a única verificação disponível é cruzar o
     nome candidato com os sobrenomes que aparecem na lista de
     referências do próprio documento (RegistroDeReferencias). Candidato
     cujo nome não bate com nenhum sobrenome da lista de referências é
     marcado indeterminado, não descartado nem aceito às cegas.
"""

import re

PADRAO_PARENTETICO = re.compile(
    r"\(([A-ZÀ-Ú][A-ZÀ-Ú]+(?:\s+[A-ZÀ-Ú]+)*(?:\s*;\s*[A-ZÀ-Ú][A-ZÀ-Ú]+(?:\s+[A-ZÀ-Ú]+)*)*"
    r",\s*\d{4}[a-z]?(?:[,;]\s*p\.\s*\d+(?:-\d+)?)?)\)"
)

PADRAO_NARRATIVO = re.compile(
    r"\b([A-ZÀ-Ú][a-zà-ú]+(?:\s*(?:;|e)\s*[A-ZÀ-Ú][a-zà-ú]+)*)\s*\((\d{4}[a-z]?(?:,\s*p\.\s*\d+(?:-\d+)?)?)\)"
)

X0_MINIMO_CITACAO_RECUADA = 140.0
"""Acima deste x0 (bem além do recuo de primeira linha de parágrafo,
≈92), a linha é considerada parte de um bloco recuado, não parágrafo
comum — ver medição real em heuristicas_paragrafo.py e no próprio
FORMATO.md."""


def linha_e_citacao_recuada(x0: float) -> bool:
    return x0 >= X0_MINIMO_CITACAO_RECUADA


def encontrar_citacoes_parenteticas(texto_paragrafo: str) -> list[tuple[str, int]]:
    """Retorna [(trecho_dentro_dos_parenteses, posicao_de_abertura), ...]
    para citações no formato parentético — aceitas sem checagem cruzada
    porque o padrão léxico (maiúsculas + vírgula + ano) não ocorre em
    texto corrido comum."""
    achados = []
    for m in PADRAO_PARENTETICO.finditer(texto_paragrafo):
        achados.append((m.group(1), m.start()))
    return achados


def encontrar_citacoes_narrativas(texto_paragrafo: str, sobrenomes_conhecidos: set) -> list[tuple[str, int, bool]]:
    """Retorna [(trecho, posicao, nome_bate_com_referencia), ...] para o
    padrão 'Nome (ano)'. `nome_bate_com_referencia` é False quando
    nenhuma palavra do nome candidato aparece como sobrenome na lista de
    referências extraída do mesmo documento — nesse caso o chamador deve
    marcar a unidade como indeterminada (MotivoIndeterminado.
    AUTOR_DATA_NAO_RECONHECIDO), não descartá-la nem tratá-la como
    citação confirmada."""
    achados = []
    for m in PADRAO_NARRATIVO.finditer(texto_paragrafo):
        nome = m.group(1)
        # Separador de múltiplos autores: ';' ou a conjunção ' e ' como
        # palavra isolada — NÃO a letra 'e' dentro de um nome (bug
        # encontrado pelo teste: "Grewe" contém 'e' e era fragmentado
        # por um split ingênuo em qualquer ocorrência da letra).
        palavras = re.split(r"\s*;\s*|\s+e\s+", nome)
        bate = any(p.strip() in sobrenomes_conhecidos for p in palavras)
        achados.append((f"{nome} ({m.group(2)})", m.start(), bate))
    return achados

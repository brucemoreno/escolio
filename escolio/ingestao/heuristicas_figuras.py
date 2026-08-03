"""Heurística de detecção de quadros/tabelas/figuras — RG-009 em
FORMATO.md.

Cobertura desigual e documentada: o único documento de desenvolvimento
disponível (data/dev/) contém quatro TABELAS (rotuladas "Tabela N:
<título>", cada uma seguida de uma linha "Fonte: <crédito>") e NENHUMA
figura ou quadro rotulado como tal, e nenhuma imagem de conteúdo (apenas
um logotipo de formulário na página 1 — ver LACUNAS.md). A heurística de
tabela abaixo foi calibrada e testada contra dado real; a de
figura/quadro segue o mesmo princípio de rótulo textual mas NÃO foi
validada contra nenhum exemplo real deste corpus — é estrutural por
analogia, e todo achado desse tipo (se algum dia ocorrer neste ou em
outro documento) deve ser tratado como candidato a confirmar
manualmente, nunca como fato estabelecido pela ausência de teste.
"""

import re

PADRAO_LEGENDA_TABELA = re.compile(r"^\s*(Tabela|Quadro)\s+(\d+)\s*:\s*(.+)$")
PADRAO_LEGENDA_FIGURA = re.compile(r"^\s*(Figura|Ilustração|Gravura)\s+(\d+)\s*:\s*(.+)$")
PADRAO_FONTE = re.compile(r"^\s*Fonte\s*:\s*(.+)$")


def linha_e_legenda_de_tabela(texto: str) -> tuple[str, str] | None:
    """Retorna (numeracao, titulo) se a linha é uma legenda de tabela/
    quadro no formato observado ('Tabela N: título'). Este padrão foi
    confirmado nas páginas 19-21 do documento de desenvolvimento."""
    m = PADRAO_LEGENDA_TABELA.match(texto)
    if not m:
        return None
    return m.group(2), m.group(3).strip()


def linha_e_legenda_de_figura(texto: str) -> tuple[str, str] | None:
    """Mesmo formato para 'Figura N: título' — NÃO CONFIRMADO no
    documento de desenvolvimento (nenhuma ocorrência real); mantido por
    simetria estrutural com a legenda de tabela, mas todo achado deve ser
    tratado como não testado (ver docstring do módulo)."""
    m = PADRAO_LEGENDA_FIGURA.match(texto)
    if not m:
        return None
    return m.group(2), m.group(3).strip()


def linha_e_credito_de_fonte(texto: str) -> str | None:
    """Retorna o texto de crédito/fonte se a linha começa com 'Fonte:' —
    confirmado no documento real como a linha imediatamente após uma
    tabela ('Fonte: Santos, 1992 - Adaptado e Elaborado pelo autor,
    2025.')."""
    m = PADRAO_FONTE.match(texto)
    if not m:
        return None
    return m.group(1).strip()

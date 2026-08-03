"""Identificadores estáveis e determinísticos de unidades de ingestão.

Requisito do prompt: "o mesmo documento processado duas vezes gera os
mesmos IDs". Isso exclui qualquer fonte de não-determinismo — UUID
aleatório, contador de execução, timestamp. O ID é derivado de:

- um hash curto do conteúdo do arquivo-fonte (documento), para que dois
  documentos diferentes nunca colidam e o mesmo documento sempre gere o
  mesmo prefixo;
- o tipo de unidade e sua posição estrutural (página + índice sequencial
  dentro da página, na ordem de leitura y-then-x do pdfplumber).

Padrão inspirado no protocolo de identificadores do P05
(escolio/identificadores.py) mas não reutiliza CLM-/SRC-: são domínios
diferentes (unidade de documento, não afirmação/evidência) — ver
escolio/ingestao/LACUNAS.md e [[project-escolio-ingestao]] em memória.

Formato: UNI-<TIPO>-<HASH8>-<POSICAO>
  TIPO: PAR (parágrafo), SEC (seção/capítulo), NOTA (nota de rodapé),
        CIT (citação recuada), REF (item de referência), FIG (figura),
        QUA (quadro/tabela)
  HASH8: primeiros 8 caracteres do sha256 do conteúdo binário do PDF
  POSICAO: <pagina:04d>-<indice:04d>, pagina em base 1, indice em base 0
           na ordem de leitura dentro da página
"""

import hashlib
import re

ID_PADRAO = re.compile(r"^UNI-[A-Z]+-[0-9a-f]{8}-\d{4}-\d{4}$")


def hash_documento(caminho_pdf: str) -> str:
    """Hash curto e determinístico do conteúdo do arquivo — mesma entrada,
    mesmo hash, em qualquer execução ou máquina."""
    h = hashlib.sha256()
    with open(caminho_pdf, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()[:8]


def gerar_id(tipo: str, hash_doc: str, pagina: int, indice: int) -> str:
    """Constrói um ID estável. `pagina` em base 1 (como o leitor humano
    conta páginas); `indice` é a posição sequencial da unidade dentro da
    página, na ordem de extração do pdfplumber (topo->baixo, esquerda->
    direita), que é determinística para um mesmo arquivo."""
    id_gerado = f"UNI-{tipo}-{hash_doc}-{pagina:04d}-{indice:04d}"
    if not ID_PADRAO.match(id_gerado):
        raise ValueError(f"tipo de unidade inválido para ID: {tipo!r}")
    return id_gerado

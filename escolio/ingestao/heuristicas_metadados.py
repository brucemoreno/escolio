"""Heurística de extração de metadados da folha de rosto — RG-010 em
FORMATO.md.

Fundamento empírico: `pdfplumber`/PDF metadata (Title, Author no próprio
arquivo PDF) NÃO contém os dados reais do trabalho — no documento de
desenvolvimento, Title é o nome do formulário CNPq/UEM e Author é a
Pró-Reitoria, não o título do projeto nem o bolsista. Os metadados
verdadeiros só existem como texto na página de rosto.

Neste documento a folha de rosto (páginas 2-3, repetida com pequena
variação) traz linhas rotuladas:
  "ORIENTADOR(A): <nome>"
  "Bolsista: <nome>"        (= autor do trabalho)
  "DEPARTAMENTO DE <nome>"  (proxy textual para 'programa', na ausência
                              de um rótulo "Programa:" explícito — ver
                              LACUNAS.md)
E o título do trabalho aparece como as linhas de maior corpo (18pt,
negrito) sem rótulo — identificado por eliminação (não é nenhum dos
rótulos conhecidos, size≥18, agrupável por proximidade vertical).
"Ano" é lido da linha de data no rodapé da capa ("Maringá, DD de mês de
AAAA."), não de um campo "Ano:" — o documento não usa esse rótulo.
"Tipo de trabalho" não tem rótulo explícito no corpo da capa; o único
sinal textual é o cabeçalho repetido "PROGRAMA INSTITUCIONAL DE BOLSAS
DE INICIAÇÃO CIENTÍFICA" — usado como valor literal quando presente, sem
tentar normalizar para uma categoria (ex.: "TCC", "dissertação"), porque
o documento não fornece essa categoria e inventá-la seria inferência não
autorizada.
"""

import re

# O formulário CNPq da página 1 concatena mais de um campo rotulado na
# mesma linha visual (ex.: "2. ORIENTADOR: Christian Fausto Moraes dos
# Santos 3. DEPARTAMENTO: DHI") — sem quebra de linha real entre os
# campos. O grupo de captura para no que vier primeiro: outro marcador
# "N. RÓTULO" do mesmo formulário, ou o fim da linha. Isso evita que o
# valor de um campo "vaze" para dentro do próximo quando os dois
# aparecem na mesma linha do PDF.
_FIM_DE_CAMPO = r"(?=\s+\d+\.\s*[A-ZÀ-Ú][A-ZÀ-Ú\-\s]+:|\s*$)"

PADRAO_ORIENTADOR = re.compile(r"ORIENTADOR\(?A?\)?\s*:\s*(.+?)" + _FIM_DE_CAMPO, re.IGNORECASE)
PADRAO_BOLSISTA = re.compile(r"Bolsista\s*:\s*(.+?)" + _FIM_DE_CAMPO, re.IGNORECASE)
PADRAO_DEPARTAMENTO = re.compile(r"DEPARTAMENTO\s+DE\s+(.+?)" + _FIM_DE_CAMPO, re.IGNORECASE)
PADRAO_DATA_CAPA = re.compile(r"^\s*[\wÀ-ú]+,\s*\d{1,2}\s+de\s+[\wçã]+\s+de\s+(\d{4})\.?\s*$", re.IGNORECASE)
PADRAO_TIPO_TRABALHO = re.compile(
    r"PROGRAMA\s+INSTITUCIONAL\s+DE\s+BOLSAS\s+DE\s+INICIA[ÇC][ÃA]O\s+CIENT[ÍI]FICA",
    re.IGNORECASE,
)

TAMANHO_MINIMO_TITULO = 16.0
"""Linhas de título na capa deste documento usam 18pt; o corpo normal da
capa (rótulos institucionais) usa 14pt. 16 fica entre os dois."""


def extrair_campo_rotulado(texto_linha: str, padrao: re.Pattern) -> str | None:
    m = padrao.search(texto_linha)
    if not m:
        return None
    valor = m.group(1).strip()
    return valor or None


def linha_e_candidata_a_titulo(tamanho_max_linha: float) -> bool:
    return tamanho_max_linha >= TAMANHO_MINIMO_TITULO


def extrair_ano_da_data_de_capa(texto_linha: str) -> str | None:
    m = PADRAO_DATA_CAPA.match(texto_linha.strip())
    return m.group(1) if m else None


def linha_indica_tipo_de_trabalho(texto_linha: str) -> bool:
    return bool(PADRAO_TIPO_TRABALHO.search(texto_linha))

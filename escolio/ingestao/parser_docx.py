"""Parser de .docx para a estrutura canônica de ingestão — par do parser
de PDF (`parser.py`), não substituto.

Não usa LLM: toda decisão é heurística determinística, calibrada contra
os 3 capítulos reais em `data/capitulos/` (ver LACUNAS.md) — mesma
disciplina de zero-inferência do parser de PDF: elemento que nenhuma
regra classifica com segurança fica marcado indeterminado, nunca chutado.

Localização por **parágrafo + seção + posição de caractere**, não página:
`.docx` não grava paginação real no arquivo — ela só existe quando o Word
renderiza para impressão, e muda a cada edição. Fabricar um número de
página congelaria uma localização falsamente estável. Ver
`escolio/ingestao/modelos.py` (nota de design) e `LACUNAS.md`.

Biblioteca: `python-docx` para estrutura de parágrafo/estilo/indentação.
Notas de rodapé são lidas diretamente de `word/footnotes.xml` via
`zipfile`+`lxml`, não pela API pública do `python-docx` — na versão
instalada (1.2.0) essa API não expõe footnotes de forma confiável (ver
LACUNAS.md).
"""

from __future__ import annotations

import hashlib
import re
import zipfile

import docx
from docx.oxml.ns import qn
from lxml import etree

from escolio.ingestao.erros import ErroDeIngestao
from escolio.ingestao.heuristicas_citacoes import (
    encontrar_citacoes_narrativas,
    encontrar_citacoes_parenteticas,
)
from escolio.ingestao.identificadores import gerar_id, hash_documento
from escolio.ingestao.modelos import (
    CitacaoNoCorpo,
    CitacaoRecuada,
    ComentarioWord,
    DocumentoIngerido,
    Metadados,
    NotaDeRodape,
    Paragrafo,
    Secao,
)
from escolio.ingestao.vocabulario import MotivoIndeterminado, NivelHierarquia

PADRAO_SECAO_NUMERADA = re.compile(r"^\d+\s*[-–.]\s*\S")
"""Calibrado contra os 3 capítulos reais: títulos de seção seguem
'N- Texto' (N inteiro, um único nível de numeração — nenhum padrão
'N.M-' de subseção foi observado nos dados reais). Um título fora deste
padrão e fora da posição de título de capítulo é marcado indeterminado,
não forçado a um nível."""

LIMIAR_INDENTACAO_CITACAO_RECUADA_PT = 50.0
"""Medido nos 3 documentos reais: bloco de citação recuada usa
left_indent=113.4pt; parágrafo comum não declara left_indent (None).
Limiar generoso abaixo do valor medido — mesmo raciocínio de folga do
X0_MINIMO_CITACAO_RECUADA do parser de PDF."""

NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
_NS = {"w": NS_W}


class _ContadorDePosicao:
    """Índice sequencial de unidades por 'bucket' — mesmo papel do
    contador do parser de PDF, mas o bucket aqui é o ordinal do parágrafo
    no corpo do documento, não a página."""

    def __init__(self) -> None:
        self._bucket_atual: int | None = None
        self._indice = 0

    def proximo(self, bucket: int) -> int:
        if bucket != self._bucket_atual:
            self._bucket_atual = bucket
            self._indice = 0
        idx = self._indice
        self._indice += 1
        return idx


def _paragrafo_e_titulo(paragrafo) -> bool:
    """Todo run com texto não-vazio do parágrafo é negrito — mesmo
    critério do parser de PDF ('linha inteira em negrito', não ênfase
    parcial). Verificado sem falso positivo contra os 3 documentos reais:
    nenhum parágrafo de corpo tem run parcialmente negrito com texto não
    vazio (ver LACUNAS.md)."""
    runs_com_texto = [r for r in paragrafo.runs if r.text.strip()]
    if not runs_com_texto:
        return False
    return all(r.bold for r in runs_com_texto)


def _e_citacao_recuada(paragrafo) -> bool:
    indent = paragrafo.paragraph_format.left_indent
    return indent is not None and indent.pt >= LIMIAR_INDENTACAO_CITACAO_RECUADA_PT


def _ler_footnotes(caminho_docx: str) -> dict[str, str]:
    """Lê word/footnotes.xml diretamente do pacote .docx (zip). Devolve
    {footnote_id: texto}, excluindo os tipos 'separator'/
    'continuationSeparator' — marcadores estruturais do Word, não notas
    de conteúdo."""
    try:
        with zipfile.ZipFile(caminho_docx) as z:
            if "word/footnotes.xml" not in z.namelist():
                return {}
            xml_bytes = z.read("word/footnotes.xml")
    except (zipfile.BadZipFile, KeyError) as e:
        raise ErroDeIngestao(f"não foi possível ler footnotes de '{caminho_docx}': {e}") from e

    raiz = etree.fromstring(xml_bytes)
    textos: dict[str, str] = {}
    for nota in raiz.findall("w:footnote", _NS):
        tipo = nota.get(qn("w:type"))
        if tipo in ("separator", "continuationSeparator"):
            continue
        fid = nota.get(qn("w:id"))
        texto = "".join(t.text or "" for t in nota.findall(".//w:t", _NS))
        textos[fid] = texto
    return textos


def _chamadas_de_nota_no_paragrafo(paragrafo) -> list[tuple[str, int]]:
    """[(footnote_id, posição_de_caractere_aproximada), ...]. A posição é
    aproximada: a chamada de nota fica entre runs no XML, sem índice de
    caractere nativo — aproxima-se somando o texto dos runs anteriores ao
    run que contém a referência."""
    chamadas: list[tuple[str, int]] = []
    offset = 0
    for run in paragrafo.runs:
        for ref in run._element.findall(".//w:footnoteReference", _NS):
            fid = ref.get(qn("w:id"))
            chamadas.append((fid, offset))
        offset += len(run.text)
    return chamadas


def _comentarios_do_paragrafo(paragrafo) -> list[tuple[str, int, int]]:
    """[(comment_id, posicao_inicio, posicao_fim), ...] — só pares cujo
    início E fim caem dentro deste parágrafo (confirmado nos capítulos
    reais: nenhum intervalo observado atravessa parágrafo). Diferente de
    `_chamadas_de_nota_no_paragrafo`: `commentRangeStart`/`commentRangeEnd`
    não ficam aninhados dentro de `w:r` (nos capítulos reais, exportados
    do Google Docs, vêm envoltos em `w:sdt`, irmãos dos runs) — por isso
    percorre a árvore inteira do parágrafo (`.iter()`), não só
    `paragrafo.runs`. Início sem fim correspondente no mesmo parágrafo
    (intervalo cruzando parágrafo, ou marcador órfão) não entra no
    resultado — vira comentário sem âncora resolvida, tratado como tal
    por quem chama, nunca como posição chutada."""
    inicios: dict[str, int] = {}
    pares: list[tuple[str, int, int]] = []
    offset = 0
    for el in paragrafo._p.iter():
        if el.tag == qn("w:t"):
            offset += len(el.text or "")
        elif el.tag == qn("w:commentRangeStart"):
            inicios[el.get(qn("w:id"))] = offset
        elif el.tag == qn("w:commentRangeEnd"):
            cid = el.get(qn("w:id"))
            inicio = inicios.pop(cid, None)
            if inicio is not None:
                pares.append((cid, inicio, offset))
    return pares


def parse_docx(caminho_docx: str) -> DocumentoIngerido:
    """Ponto de entrada. `caminho_docx` deve estar em `data/capitulos/` —
    este módulo não impõe essa restrição em tempo de execução, mesma
    convenção documental (não checada em código) do parser de PDF
    [`parser.py`]. NENHUM código deste módulo lê `data/gold/`."""
    try:
        documento = docx.Document(caminho_docx)
    except Exception as e:
        raise ErroDeIngestao(f"não foi possível abrir '{caminho_docx}': {e}") from e

    hash_doc = hash_documento(caminho_docx)
    footnotes_texto = _ler_footnotes(caminho_docx)
    contador = _ContadorDePosicao()
    contador_notas = _ContadorDePosicao()

    secoes: list[Secao] = []
    paragrafos: list[Paragrafo] = []
    notas_de_rodape: list[NotaDeRodape] = []
    citacoes_recuadas: list[CitacaoRecuada] = []
    citacoes_no_corpo: list[CitacaoNoCorpo] = []

    secao_atual_id: str | None = None
    titulo_do_capitulo_visto = False
    chamadas_pendentes: dict[str, tuple[str, int]] = {}
    ancoras_comentarios: dict[str, tuple[str, int, int]] = {}

    ordinal_corpo = 0  # ordinal só de parágrafos/citações de corpo, base 0
    for paragrafo in documento.paragraphs:
        texto = paragrafo.text.strip()
        if not texto:
            continue

        comentarios_no_paragrafo = _comentarios_do_paragrafo(paragrafo)

        if _paragrafo_e_titulo(paragrafo):
            if not titulo_do_capitulo_visto:
                nivel: NivelHierarquia | None = NivelHierarquia.CAPITULO
                indeterminado = False
                motivo = None
                titulo_do_capitulo_visto = True
            elif PADRAO_SECAO_NUMERADA.match(texto):
                nivel = NivelHierarquia.SECAO
                indeterminado = False
                motivo = None
            else:
                # Parágrafo inteiramente em negrito que não é o título do
                # capítulo nem segue o padrão de numeração observado nos
                # 3 documentos reais — não visto nos dados calibrados;
                # marcado indeterminado, nunca forçado a um nível.
                nivel = None
                indeterminado = True
                motivo = MotivoIndeterminado.PADRAO_GRAFICO_AMBIGUO
            ordinal_secao = len(secoes)
            sec_id = gerar_id("SEC", hash_doc, ordinal_secao, 0)
            secoes.append(
                Secao(
                    unit_id=sec_id,
                    titulo=texto,
                    pagina=None,
                    nivel=nivel,
                    indeterminado=indeterminado,
                    motivo_indeterminado=motivo,
                )
            )
            secao_atual_id = sec_id
            for cid, inicio, fim in comentarios_no_paragrafo:
                ancoras_comentarios[cid] = (sec_id, inicio, fim)
            continue

        if _e_citacao_recuada(paragrafo):
            idx = contador.proximo(ordinal_corpo)
            cit_id = gerar_id("CIT", hash_doc, ordinal_corpo, idx)
            for fid, pos in _chamadas_de_nota_no_paragrafo(paragrafo):
                chamadas_pendentes[fid] = (cit_id, pos)
            for cid, inicio, fim in comentarios_no_paragrafo:
                ancoras_comentarios[cid] = (cit_id, inicio, fim)
            citacoes_recuadas.append(
                CitacaoRecuada(
                    unit_id=cit_id,
                    texto=texto,
                    pagina_inicio=None,
                    pagina_fim=None,
                    secao_id=secao_atual_id,
                )
            )
            ordinal_corpo += 1
            continue

        idx = contador.proximo(ordinal_corpo)
        par_id = gerar_id("PAR", hash_doc, ordinal_corpo, idx)

        citas_ids: list[str] = []
        for trecho, pos in encontrar_citacoes_parenteticas(texto):
            idx_c = contador.proximo(ordinal_corpo)
            cid = gerar_id("CIT", hash_doc, ordinal_corpo, idx_c)
            citacoes_no_corpo.append(
                CitacaoNoCorpo(unit_id=cid, paragrafo_id=par_id, trecho=trecho, posicao_no_paragrafo=pos)
            )
            citas_ids.append(cid)
        # Sem lista de referências nestes documentos (citação é só por
        # nota de rodapé — ver LACUNAS.md): nenhum sobrenome conhecido
        # para cross-checagem, então toda citação narrativa nasce
        # indeterminada, nunca confirmada às cegas.
        for trecho, pos, bate in encontrar_citacoes_narrativas(texto, set()):
            idx_c = contador.proximo(ordinal_corpo)
            cid = gerar_id("CIT", hash_doc, ordinal_corpo, idx_c)
            citacoes_no_corpo.append(
                CitacaoNoCorpo(
                    unit_id=cid,
                    paragrafo_id=par_id,
                    trecho=trecho,
                    posicao_no_paragrafo=pos,
                    indeterminado=not bate,
                    motivo_indeterminado=None if bate else MotivoIndeterminado.AUTOR_DATA_NAO_RECONHECIDO,
                )
            )
            citas_ids.append(cid)

        for fid, pos in _chamadas_de_nota_no_paragrafo(paragrafo):
            chamadas_pendentes[fid] = (par_id, pos)
        for cid, inicio, fim in comentarios_no_paragrafo:
            ancoras_comentarios[cid] = (par_id, inicio, fim)

        paragrafos.append(
            Paragrafo(
                unit_id=par_id,
                texto=texto,
                pagina_inicio=None,
                pagina_fim=None,
                secao_id=secao_atual_id,
                citacoes_no_corpo_ids=citas_ids,
                paragrafo_ordinal=ordinal_corpo,
            )
        )
        ordinal_corpo += 1

    unidades_por_id = {p.unit_id: p for p in paragrafos}
    unidades_por_id.update({c.unit_id: c for c in citacoes_recuadas})
    for fid, texto_nota in footnotes_texto.items():
        unit_id_chamador, pos = chamadas_pendentes.get(fid, (None, None))
        idx = contador_notas.proximo(0)
        nota_id = gerar_id("NOTA", hash_doc, 0, idx)
        notas_de_rodape.append(
            NotaDeRodape(
                unit_id=nota_id,
                numero=fid,
                texto=texto_nota,
                pagina_chamada=None,
                unit_id_chamador=unit_id_chamador,
                posicao_na_chamada=pos,
                indeterminado=unit_id_chamador is None,
                motivo_indeterminado=(
                    None if unit_id_chamador is not None else MotivoIndeterminado.SEM_CHAMADA_CORRESPONDENTE
                ),
            )
        )
        if unit_id_chamador and unit_id_chamador in unidades_por_id:
            unidade = unidades_por_id[unit_id_chamador]
            if hasattr(unidade, "notas_de_rodape_ids"):
                unidade.notas_de_rodape_ids.append(nota_id)

    contador_comentarios = _ContadorDePosicao()
    comentarios_word: list[ComentarioWord] = []
    for comentario in documento.comments:
        ancora = ancoras_comentarios.get(str(comentario.comment_id))
        unit_id_ancora, posicao_inicio, posicao_fim = ancora if ancora is not None else (None, None, None)
        idx = contador_comentarios.proximo(0)
        com_id = gerar_id("COM", hash_doc, 0, idx)
        comentarios_word.append(
            ComentarioWord(
                unit_id=com_id,
                autor=comentario.author,
                texto=comentario.text,
                data=comentario.timestamp.isoformat() if comentario.timestamp is not None else None,
                unit_id_ancora=unit_id_ancora,
                posicao_inicio=posicao_inicio,
                posicao_fim=posicao_fim,
                indeterminado=unit_id_ancora is None,
                motivo_indeterminado=(
                    None if unit_id_ancora is not None else MotivoIndeterminado.SEM_ANCORA_TEXTUAL
                ),
            )
        )

    return DocumentoIngerido(
        hash_documento=hash_doc,
        caminho_original=caminho_docx,
        num_paginas=None,
        metadados=Metadados(),
        secoes=secoes,
        paragrafos=paragrafos,
        notas_de_rodape=notas_de_rodape,
        citacoes_recuadas=citacoes_recuadas,
        citacoes_no_corpo=citacoes_no_corpo,
        referencias=[],
        figuras=[],
        comentarios_word=comentarios_word,
        hifens_de_fim_de_linha_preservados=0,
    )


def _hash_combinado(hashes: list[str]) -> str:
    """Hash curto e determinístico de uma obra cujos capítulos vêm de
    arquivos `.docx` separados — combina os `hash_documento` de cada
    arquivo já calculados por `parse_docx`, sem reler bytes. A ordem dos
    hashes importa (reflete a ordem dos capítulos): trocar a ordem produz
    um hash diferente, deliberadamente — é uma obra diferente."""
    h = hashlib.sha256("".join(hashes).encode("utf-8"))
    return h.hexdigest()[:8]


def parse_docx_multiplo(caminhos: list[str]) -> DocumentoIngerido:
    """Combina vários `.docx` numa única obra — caso real: tese cujos
    capítulos foram entregues como arquivos separados, e cuja soma é a
    obra completa [confirmado pelo professor; ver LACUNAS.md]. `.docx`
    isolado (`parse_docx`) não tem como saber disso — cartografia global
    de uma obra em vários arquivos só existe combinando os resultados.

    Cada arquivo é parseado por `parse_docx`, sem alteração. Os
    resultados são concatenados na ordem de `caminhos` — que é a ordem
    dos capítulos na obra, decisão de quem chama, nunca inferida daqui
    (nome de arquivo não é fonte confiável de ordem). `unit_id` de cada
    unidade já embute o hash do SEU arquivo de origem (ver
    `identificadores.py`), então arquivos diferentes nunca colidem — a
    concatenação não precisa regerar nenhum ID.

    O primeiro título de cada arquivo já é `NivelHierarquia.CAPITULO`
    (ver `parse_docx`); esta função só acrescenta o vínculo que um
    arquivo isolado não tem razão para expressar — `Secao.secao_pai_id`
    de toda seção de nível `SECAO` passa a apontar para o capítulo do seu
    próprio arquivo."""
    if not caminhos:
        raise ErroDeIngestao("parse_docx_multiplo exige ao menos um caminho")

    documentos = [parse_docx(c) for c in caminhos]

    secoes: list[Secao] = []
    capitulo_atual_id: str | None = None
    for doc in documentos:
        capitulo_atual_id = None
        for s in doc.secoes:
            if s.nivel is NivelHierarquia.CAPITULO:
                capitulo_atual_id = s.unit_id
            elif s.nivel is NivelHierarquia.SECAO:
                s.secao_pai_id = capitulo_atual_id
            secoes.append(s)

    return DocumentoIngerido(
        hash_documento=_hash_combinado([d.hash_documento for d in documentos]),
        caminho_original="; ".join(caminhos),
        num_paginas=None,
        metadados=Metadados(),
        secoes=secoes,
        paragrafos=[p for d in documentos for p in d.paragrafos],
        notas_de_rodape=[n for d in documentos for n in d.notas_de_rodape],
        citacoes_recuadas=[c for d in documentos for c in d.citacoes_recuadas],
        citacoes_no_corpo=[c for d in documentos for c in d.citacoes_no_corpo],
        referencias=[r for d in documentos for r in d.referencias],
        figuras=[f for d in documentos for f in d.figuras],
        comentarios_word=[c for d in documentos for c in d.comentarios_word],
        hifens_de_fim_de_linha_preservados=sum(
            d.hifens_de_fim_de_linha_preservados for d in documentos
        ),
    )

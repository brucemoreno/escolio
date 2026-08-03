"""Parser de PDF acadêmico para a estrutura canônica de ingestão.

Orquestra as heurísticas dos módulos heuristicas_*.py sobre a saída de
escolio.ingestao.layout.extrair_linhas. Não usa LLM: toda decisão é uma
regra determinística documentada em FORMATO.md; elemento que nenhuma
regra classifica com segurança fica marcado indeterminado (ver
escolio.ingestao.vocabulario.MotivoIndeterminado), nunca chutado.

Biblioteca: pdfplumber (ver [[feedback-ingestao-pdf-extraction]] em
memória) — preserva posição e tamanho de fonte por caractere, que é o
que toda heurística aqui depende.
"""

import pdfplumber

from escolio.ingestao.erros import ErroDeIngestao
from escolio.ingestao.heuristicas_citacoes import (
    encontrar_citacoes_narrativas,
    encontrar_citacoes_parenteticas,
    linha_e_citacao_recuada,
)
from escolio.ingestao.heuristicas_figuras import (
    linha_e_credito_de_fonte,
    linha_e_legenda_de_figura,
    linha_e_legenda_de_tabela,
)
from escolio.ingestao.heuristicas_hierarquia import (
    apos_inicio_das_referencias,
    classificar_titulo,
    linha_e_candidata_a_titulo,
)
from escolio.ingestao.heuristicas_metadados import (
    extrair_ano_da_data_de_capa,
    extrair_campo_rotulado,
    linha_e_candidata_a_titulo as capa_linha_e_titulo,
    linha_indica_tipo_de_trabalho,
    PADRAO_BOLSISTA,
    PADRAO_DEPARTAMENTO,
    PADRAO_ORIENTADOR,
)
from escolio.ingestao.heuristicas_notas import (
    encontrar_chamadas_de_nota,
    linha_e_corpo_de_nota,
)
from escolio.ingestao.heuristicas_paragrafo import (
    concatenar_preservando_texto_literal,
    linha_inicia_paragrafo,
)
from escolio.ingestao.heuristicas_referencias import linha_inicia_novo_item
from escolio.ingestao.identificadores import gerar_id, hash_documento
from escolio.ingestao.layout import Linha, extrair_linhas
from escolio.ingestao.modelos import (
    CitacaoNoCorpo,
    CitacaoRecuada,
    DocumentoIngerido,
    Figura,
    ItemDeReferencia,
    Metadados,
    NotaDeRodape,
    Paragrafo,
    Secao,
)
from escolio.ingestao.vocabulario import MotivoIndeterminado, NivelHierarquia, TipoUnidade

NUM_PAGINAS_FOLHA_DE_ROSTO = 3
"""Páginas 1-3 tratadas como zona de metadados/capa neste documento
(formulário CNPq + folha de rosto repetida) — ver FORMATO.md RG-010.
Constante nomeada porque é uma calibração deste documento, não uma
regra universal de folha de rosto."""

ROTULO_REFERENCIAS = "referências bibliográficas"


class _ContadorDePosicao:
    """Índice sequencial de unidades por página, para IDs determinísticos
    (ver identificadores.py). Reinicia a cada nova página."""

    def __init__(self):
        self._pagina_atual = None
        self._indice = 0

    def proximo(self, pagina: int) -> int:
        if pagina != self._pagina_atual:
            self._pagina_atual = pagina
            self._indice = 0
        idx = self._indice
        self._indice += 1
        return idx


def _gap(linha_atual: Linha, linha_anterior: Linha | None) -> float | None:
    if linha_anterior is None or linha_anterior.pagina != linha_atual.pagina:
        return None
    return round(linha_atual.top - linha_anterior.top, 1)


PAGINA_FORMULARIO_CNPQ = 1
"""A página 1 deste documento é o formulário burocrático CNPq/UEM, não a
folha de rosto do trabalho — traz seu próprio cabeçalho em corpo grande
("RELATÓRIO FINAL", 18pt Arial-BoldItalicMT) que colide em tamanho com o
título do trabalho na folha de rosto real (páginas 2-3, 18pt
Arial-BoldMT — fonte distinta, mas a distinção de estilo de fonte é
frágil demais para basear a heurística nela; a distinção de PÁGINA é
robusta e foi confirmada nos dados reais). Por isso a extração de título
ignora a página 1."""


def _extrair_metadados(paginas_linhas: list[list[Linha]]) -> Metadados:
    meta = Metadados()
    titulo_partes: list[str] = []
    titulo_ja_fechado = False
    for pagina_idx, linhas in enumerate(paginas_linhas):
        pagina_num = pagina_idx + 1
        for linha in linhas:
            texto = linha.texto.strip()
            if not meta.orientador:
                v = extrair_campo_rotulado(texto, PADRAO_ORIENTADOR)
                if v:
                    meta.orientador = v
            if not meta.autor:
                v = extrair_campo_rotulado(texto, PADRAO_BOLSISTA)
                if v:
                    meta.autor = v
            if not meta.programa:
                v = extrair_campo_rotulado(texto, PADRAO_DEPARTAMENTO)
                if v:
                    meta.programa = v
            if not meta.ano:
                ano = extrair_ano_da_data_de_capa(texto)
                if ano:
                    meta.ano = ano
            if not meta.tipo_de_trabalho and linha_indica_tipo_de_trabalho(texto):
                meta.tipo_de_trabalho = texto
            if (
                pagina_num != PAGINA_FORMULARIO_CNPQ
                and not titulo_ja_fechado
                and linha.tamanhos
                and capa_linha_e_titulo(max(linha.tamanhos))
            ):
                if titulo_partes and texto == titulo_partes[0]:
                    # Capa se repete (páginas 2 e 3 quase idênticas neste
                    # documento) — a reocorrência da primeira linha do
                    # título marca o fim do primeiro bloco, não uma
                    # continuação dele.
                    titulo_ja_fechado = True
                else:
                    titulo_partes.append(texto)
    meta.titulo = " ".join(titulo_partes) if titulo_partes else None
    return meta


def parse_pdf(caminho_pdf: str) -> DocumentoIngerido:
    """Ponto de entrada. `caminho_pdf` deve estar em data/dev/ — este
    módulo não impõe essa restrição em tempo de execução (não sabe de
    onde o chamador tirou o caminho), mas a regra do projeto é que
    NENHUM código deste módulo leia data/gold/ — ver LACUNAS.md."""
    try:
        pdf = pdfplumber.open(caminho_pdf)
    except Exception as e:
        raise ErroDeIngestao(f"não foi possível abrir '{caminho_pdf}': {e}") from e

    with pdf:
        hash_doc = hash_documento(caminho_pdf)
        num_paginas = len(pdf.pages)
        contador = _ContadorDePosicao()

        paginas_linhas = [extrair_linhas(p) for p in pdf.pages]

        metadados = _extrair_metadados(paginas_linhas[:NUM_PAGINAS_FOLHA_DE_ROSTO])

        secoes: list[Secao] = []
        paragrafos: list[Paragrafo] = []
        notas_de_rodape: list[NotaDeRodape] = []
        citacoes_recuadas: list[CitacaoRecuada] = []
        citacoes_no_corpo: list[CitacaoNoCorpo] = []
        referencias: list[ItemDeReferencia] = []
        figuras: list[Figura] = []

        secao_atual_id: str | None = None
        titulos_vistos: list[str] = []
        dentro_de_referencias = False
        subsecao_referencias_atual: str | None = None
        dentro_de_tabela = False
        """True entre uma legenda 'Tabela N:'/'Quadro N:' e a linha 'Fonte:'
        que a fecha. Constatado no documento real: linhas de cabeçalho e
        célula de tabela (ex.: 'Frequência no Manuscrito', quebrada em
        duas linhas) caem no mesmo x0 usado para detectar citação recuada
        (ver heuristicas_citacoes.py) e seriam classificadas como bloco
        de citação sem esta exclusão — ver LACUNAS.md."""

        # Estado de agregação de parágrafo corrente. `pagina_inicio` fixa
        # o ID (deterministico, chave da primeira página onde a unidade
        # aparece); `pagina_fim` acompanha a última página tocada, para
        # unidades que atravessam quebra de página sem se fragmentar
        # (ver nota de design em modelos.py).
        paragrafo_texto = ""
        paragrafo_pagina_inicio = None
        paragrafo_pagina_fim = None
        paragrafo_secao_id = None
        chamadas_pendentes: list[tuple[str, int]] = []  # (numero, posicao) no paragrafo em construção

        # Estado de agregação de citação recuada corrente — mesma lógica
        # de acumulação do parágrafo: linhas contíguas com x0 de bloco
        # recuado pertencem à mesma citação, até a próxima linha que não
        # for recuada (ver RG-006 revisado em FORMATO.md), mesmo que
        # atravessem uma quebra de página.
        citacao_recuada_texto = ""
        citacao_recuada_pagina_inicio = None
        citacao_recuada_pagina_fim = None
        chamadas_pendentes_citacao: list[tuple[str, int]] = []

        # Notas: chamada vista no corpo, aguardando corpo da nota no rodapé
        chamadas_por_pagina: dict[int, list[tuple[str, str, int]]] = {}
        # (pagina, numero) -> (unit_id_chamador, posicao) fixado quando a
        # unidade que contém a chamada (parágrafo ou citação recuada) fecha
        chamada_localizacao: dict[tuple[int, str], tuple[str, int]] = {}
        # (numero, pagina, texto_da_nota) casados durante a varredura,
        # resolvidos contra chamada_localizacao só ao final (ver bloco de
        # notas de rodapé abaixo, no laço principal). Lista mutável de
        # listas (não tupla) porque o texto da nota é atualizado enquanto
        # linhas de continuação são lidas.
        notas_pendentes: list[list] = []  # [numero, pagina, texto_acumulado]
        # (pagina, x0_tolerado) da nota de rodapé em aberto — enquanto
        # aberta, linhas subsequentes na mesma faixa de x0 são
        # continuação do corpo da nota, não de outra unidade. Constatado
        # no documento real: o corpo de uma nota de rodapé pode ter mais
        # de uma linha ('No original: ...' se estende por até 3 linhas),
        # e apenas a primeira linha começa com o número da nota — as
        # demais são texto corrido no mesmo x0 do corpo comum, e sem este
        # estado seriam confundidas com continuação de outra unidade
        # (constatado: fechava uma citação recuada prematuramente antes
        # dela atravessar a quebra de página, caso 'moxerich' p.13→p.14).
        nota_rodape_em_aberto: list = [None, None]  # [pagina, x0_da_primeira_linha]

        # Referências: rastreio de gap intra-item
        gap_tipico_intra_item = 15.9  # medido no documento real (ver heuristicas_referencias.py)
        ultima_linha_ref: Linha | None = None
        item_ref_texto = ""
        item_ref_pagina = None

        # Contagem de junções que preservaram um hífen de fim de linha
        # sem decidir se ele pertence à palavra ou é artefato de quebra
        # (ver RG-004 revisado em heuristicas_paragrafo.py) — usa lista
        # de 1 elemento como cela mutável simples para as closures acima.
        contagem_hifens_preservados = [0]

        def fechar_paragrafo():
            nonlocal paragrafo_texto, paragrafo_pagina_inicio, paragrafo_pagina_fim, paragrafo_secao_id, chamadas_pendentes
            if not paragrafo_texto.strip():
                paragrafo_texto = ""
                chamadas_pendentes = []
                return
            idx = contador.proximo(paragrafo_pagina_inicio)
            par_id = gerar_id("PAR", hash_doc, paragrafo_pagina_inicio, idx)

            citas_ids = []
            for trecho, pos in encontrar_citacoes_parenteticas(paragrafo_texto):
                idx_c = contador.proximo(paragrafo_pagina_inicio)
                cid = gerar_id("CIT", hash_doc, paragrafo_pagina_inicio, idx_c)
                citacoes_no_corpo.append(
                    CitacaoNoCorpo(unit_id=cid, paragrafo_id=par_id, trecho=trecho, posicao_no_paragrafo=pos)
                )
                citas_ids.append(cid)
            for trecho, pos, bate in encontrar_citacoes_narrativas(paragrafo_texto, sobrenomes_referencias):
                idx_c = contador.proximo(paragrafo_pagina_inicio)
                cid = gerar_id("CIT", hash_doc, paragrafo_pagina_inicio, idx_c)
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

            notas_ids = []
            for numero, pagina_da_chamada, pos in chamadas_pendentes:
                chamada_localizacao[(pagina_da_chamada, numero)] = (par_id, pos)

            paragrafos.append(
                Paragrafo(
                    unit_id=par_id,
                    texto=paragrafo_texto,
                    pagina_inicio=paragrafo_pagina_inicio,
                    pagina_fim=paragrafo_pagina_fim,
                    secao_id=paragrafo_secao_id,
                    notas_de_rodape_ids=notas_ids,
                    citacoes_no_corpo_ids=citas_ids,
                )
            )
            paragrafo_texto = ""
            chamadas_pendentes = []

        def fechar_item_referencia():
            nonlocal item_ref_texto, item_ref_pagina
            if not item_ref_texto.strip():
                item_ref_texto = ""
                return
            idx = contador.proximo(item_ref_pagina)
            rid = gerar_id("REF", hash_doc, item_ref_pagina, idx)
            referencias.append(
                ItemDeReferencia(
                    unit_id=rid,
                    texto=item_ref_texto,
                    pagina=item_ref_pagina,
                    subsecao=subsecao_referencias_atual,
                )
            )
            item_ref_texto = ""

        def fechar_citacao_recuada() -> str | None:
            """Retorna o unit_id da citação fechada (ou None se não havia
            nada acumulado)."""
            nonlocal citacao_recuada_texto, citacao_recuada_pagina_inicio, citacao_recuada_pagina_fim, chamadas_pendentes_citacao
            if not citacao_recuada_texto.strip():
                citacao_recuada_texto = ""
                chamadas_pendentes_citacao = []
                return None
            idx = contador.proximo(citacao_recuada_pagina_inicio)
            cit_id = gerar_id("CIT", hash_doc, citacao_recuada_pagina_inicio, idx)
            citacoes_recuadas.append(
                CitacaoRecuada(
                    unit_id=cit_id,
                    texto=citacao_recuada_texto,
                    pagina_inicio=citacao_recuada_pagina_inicio,
                    pagina_fim=citacao_recuada_pagina_fim,
                    secao_id=secao_atual_id,
                )
            )
            for numero, pagina_da_chamada, pos in chamadas_pendentes_citacao:
                chamada_localizacao[(pagina_da_chamada, numero)] = (cit_id, pos)
            citacao_recuada_texto = ""
            chamadas_pendentes_citacao = []
            return cit_id

        # Sobrenomes conhecidos (para checagem cruzada de citação narrativa)
        # é preenchido incrementalmente: como as referências ficam no fim
        # do documento, fazemos uma primeira varredura leve só para
        # extrair sobrenomes antes do laço principal.
        sobrenomes_referencias: set = set()
        _dentro_ref_prevarredura = False
        _sobrenome_padrao = __import__("re").compile(r"^([A-ZÀ-Ú][A-ZÀ-Ú\s]+),")
        for linhas in paginas_linhas:
            for linha in linhas:
                texto = linha.texto.strip()
                if texto.lower() == ROTULO_REFERENCIAS and linha_e_candidata_a_titulo(linha):
                    _dentro_ref_prevarredura = True
                    continue
                if _dentro_ref_prevarredura:
                    m = _sobrenome_padrao.match(texto)
                    if m:
                        sobrenomes_referencias.add(m.group(1).split()[0].strip().title())

        for pagina_idx, linhas in enumerate(paginas_linhas):
            pagina_num = pagina_idx + 1
            linha_anterior: Linha | None = None

            for linha in linhas:
                texto = linha.texto.strip()
                if not texto:
                    continue

                # Chamadas de nota são extraídas de QUALQUER linha, antes
                # de decidir a que tipo de unidade ela pertence — uma
                # chamada pode terminar uma citação recuada (constatado
                # no documento real: '...p. 13).1' fecha um bloco recuado)
                # e não apenas um parágrafo comum. `chamadas_desta_linha`
                # é registrada em chamadas_por_pagina já aqui; a
                # localização definitiva (a que unidade pertence) é
                # resolvida quando essa unidade fecha, abaixo.
                chamadas_desta_linha = (
                    encontrar_chamadas_de_nota(linha) if pagina_num > NUM_PAGINAS_FOLHA_DE_ROSTO else []
                )

                # --- título de seção ---
                if pagina_num > NUM_PAGINAS_FOLHA_DE_ROSTO and linha_e_candidata_a_titulo(linha):
                    fechar_paragrafo()
                    fechar_item_referencia()
                    fechar_citacao_recuada()
                    if texto.lower() == ROTULO_REFERENCIAS:
                        dentro_de_referencias = True
                    indeterminado, motivo = classificar_titulo(
                        texto, apos_inicio_das_referencias(titulos_vistos)
                    )
                    idx = contador.proximo(pagina_num)
                    sec_id = gerar_id("SEC", hash_doc, pagina_num, idx)
                    nivel = None if indeterminado else NivelHierarquia.CAPITULO
                    secoes.append(
                        Secao(
                            unit_id=sec_id,
                            titulo=texto,
                            pagina=pagina_num,
                            nivel=nivel,
                            indeterminado=indeterminado,
                            motivo_indeterminado=motivo,
                        )
                    )
                    titulos_vistos.append(texto)
                    if dentro_de_referencias and texto.lower() != ROTULO_REFERENCIAS:
                        subsecao_referencias_atual = texto
                    secao_atual_id = sec_id
                    linha_anterior = linha
                    continue

                # --- legenda / crédito de tabela ou figura ---
                leg_tabela = linha_e_legenda_de_tabela(texto)
                leg_figura = linha_e_legenda_de_figura(texto)
                credito = linha_e_credito_de_fonte(texto)
                if leg_tabela or leg_figura or credito:
                    fechar_paragrafo()
                    fechar_citacao_recuada()
                    if leg_tabela or leg_figura:
                        dentro_de_tabela = True
                        numeracao, titulo_legenda = leg_tabela or leg_figura
                        tipo = TipoUnidade.QUADRO_TABELA if leg_tabela else TipoUnidade.FIGURA
                        idx = contador.proximo(pagina_num)
                        fig_id = gerar_id("FIG", hash_doc, pagina_num, idx)
                        figuras.append(
                            Figura(
                                unit_id=fig_id,
                                tipo=tipo,
                                pagina=pagina_num,
                                legenda=titulo_legenda,
                                credito=None,
                                numeracao=numeracao,
                                referencia_de_acervo=None,
                                posicao_no_texto=f"apos {paragrafos[-1].unit_id}" if paragrafos else None,
                                indeterminado=(leg_figura is not None),
                                motivo_indeterminado=(
                                    MotivoIndeterminado.SEM_ANCORA_TEXTUAL if leg_figura is not None else None
                                ),
                            )
                        )
                    elif credito and figuras:
                        figuras[-1].credito = credito
                        dentro_de_tabela = False
                    linha_anterior = linha
                    continue

                # --- dentro de uma tabela (entre legenda e 'Fonte:') ---
                # Constatado no documento real: cabeçalho e célula de
                # tabela usam o mesmo x0 que o bloco de citação recuada
                # (ex.: 'Frequência no Manuscrito' na Tabela 2, p.19) —
                # sem esta exclusão, seriam classificados como citação.
                # Não tentamos extrair a tabela em si nesta fase (fora de
                # escopo: "conteúdo tabular... não é extraído nesta
                # fase"), apenas evitamos classificar mal o que está
                # dentro dela.
                if dentro_de_tabela:
                    fechar_citacao_recuada()
                    linha_anterior = linha
                    continue

                # --- notas de rodapé: possível corpo de nota no rodapé ---
                # A localização da chamada (a que unidade ela pertence)
                # só fica definitiva quando essa unidade fecha — e uma
                # citação recuada pode fechar bem depois do corpo da nota
                # já ter sido lido na mesma página (constatado no
                # documento real: a chamada 1 termina uma citação recuada
                # que só fecha ao encontrar a próxima linha não-recuada,
                # possivelmente já na página seguinte). Por isso a
                # correspondência aqui só registra [número, página, texto]
                # em `notas_pendentes`; a resolução de
                # unit_id_chamador/posicao_na_chamada acontece numa
                # passagem final, quando chamada_localizacao já está
                # completo para o documento inteiro.
                #
                # Continuação: o corpo de uma nota pode ocupar mais de uma
                # linha (constatado: 'No original: ...' se estende por até
                # 3 linhas), e só a primeira começa com o número da nota.
                # Enquanto `nota_rodape_em_aberto` aponta para esta página,
                # linhas no mesmo x0 são anexadas à última nota pendente
                # dessa página em vez de reavaliadas como início de outra
                # unidade — sem isso, a segunda linha em diante do corpo
                # da nota "vazava" para a lógica de citação recuada/
                # parágrafo comum e fechava blocos prematuramente.
                if nota_rodape_em_aberto[0] == pagina_num and abs(linha.x0 - nota_rodape_em_aberto[1]) < 5.0:
                    if linha_e_citacao_recuada(linha.x0) or linha_inicia_paragrafo(linha):
                        nota_rodape_em_aberto[0] = None
                    else:
                        for entrada in reversed(notas_pendentes):
                            if entrada[1] == pagina_num:
                                entrada[2] = entrada[2].rstrip() + " " + texto.lstrip()
                                break
                        linha_anterior = linha
                        continue

                numeros_ja_casados_nesta_pagina = {
                    numero for numero, pnum, _ in notas_pendentes if pnum == pagina_num
                }
                nota_casada = False
                for numero, tam_chamada, _pos in chamadas_por_pagina.get(pagina_num, []):
                    if numero in numeros_ja_casados_nesta_pagina:
                        continue
                    resultado = linha_e_corpo_de_nota(linha, tam_chamada)
                    if not resultado or resultado[0] != numero:
                        continue
                    notas_pendentes.append([numero, pagina_num, resultado[1]])
                    nota_rodape_em_aberto[0] = pagina_num
                    nota_rodape_em_aberto[1] = linha.x0
                    nota_casada = True
                    break
                if nota_casada:
                    linha_anterior = linha
                    continue

                # --- citação recuada ---
                # Acumula linhas contíguas de bloco recuado na mesma
                # unidade, inclusive atravessando quebra de página — uma
                # citação longa que começa numa página e termina na
                # seguinte continua sendo UMA unidade (pagina_inicio
                # fixa o ID; pagina_fim acompanha o avanço). Checagem
                # contra o documento real mostrou que uma citação ocupa
                # várias linhas (ex.: p.10, 6 linhas; 'moxerich', p.13→p.14)
                # e tratar cada linha ou cada página como uma citação
                # separada fragmentava uma unidade lógica só.
                if (
                    pagina_num > NUM_PAGINAS_FOLHA_DE_ROSTO
                    and not dentro_de_referencias
                    and linha_e_citacao_recuada(linha.x0)
                ):
                    fechar_paragrafo()
                    if not citacao_recuada_texto:
                        citacao_recuada_pagina_inicio = pagina_num
                    citacao_recuada_pagina_fim = pagina_num
                    pos_base = len(citacao_recuada_texto)
                    citacao_recuada_texto, _ = concatenar_preservando_texto_literal(citacao_recuada_texto, texto)
                    for numero, pos_na_linha, tam in chamadas_desta_linha:
                        pos_global = pos_base + pos_na_linha
                        chamadas_pendentes_citacao.append((numero, pagina_num, pos_global))
                        chamadas_por_pagina.setdefault(pagina_num, []).append((numero, tam, pos_global))
                    linha_anterior = linha
                    continue
                elif citacao_recuada_texto:
                    # Linha não-recuada encontrada: fecha o bloco recuado
                    # em andamento antes de processar esta linha como
                    # outra coisa (parágrafo, referência, etc.).
                    fechar_citacao_recuada()

                # --- dentro da lista de referências: segmentação por gap ---
                if dentro_de_referencias:
                    gap = _gap(linha, ultima_linha_ref)
                    if linha_inicia_novo_item(gap, gap_tipico_intra_item):
                        fechar_item_referencia()
                        item_ref_pagina = pagina_num
                        item_ref_texto = texto
                    else:
                        item_ref_texto, houve_hifen = concatenar_preservando_texto_literal(item_ref_texto, texto)
                        if houve_hifen:
                            contagem_hifens_preservados[0] += 1
                    ultima_linha_ref = linha
                    linha_anterior = linha
                    continue

                # --- corpo comum: parágrafo + chamadas de nota ---
                for numero, pos_na_linha, tam in chamadas_desta_linha:
                    pos_global = len(paragrafo_texto) + pos_na_linha
                    chamadas_pendentes.append((numero, pagina_num, pos_global))
                    chamadas_por_pagina.setdefault(pagina_num, []).append((numero, tam, pos_global))

                if linha_inicia_paragrafo(linha):
                    fechar_paragrafo()
                    paragrafo_texto = texto
                    paragrafo_pagina_inicio = pagina_num
                    paragrafo_pagina_fim = pagina_num
                    paragrafo_secao_id = secao_atual_id
                else:
                    if not paragrafo_texto:
                        paragrafo_pagina_inicio = pagina_num
                        paragrafo_secao_id = secao_atual_id
                    paragrafo_pagina_fim = pagina_num
                    paragrafo_texto, houve_hifen = concatenar_preservando_texto_literal(paragrafo_texto, texto)
                    if houve_hifen:
                        contagem_hifens_preservados[0] += 1

                linha_anterior = linha

        fechar_paragrafo()
        fechar_item_referencia()
        fechar_citacao_recuada()

        # Resolução final das notas: agora chamada_localizacao contém
        # todas as unidades já fechadas do documento inteiro.
        unidades_por_id = {p.unit_id: p for p in paragrafos}
        unidades_por_id.update({c.unit_id: c for c in citacoes_recuadas})
        for numero, pagina_num, texto_nota in notas_pendentes:
            idx = contador.proximo(pagina_num)
            nota_id = gerar_id("NOTA", hash_doc, pagina_num, idx)
            unit_id_chamador, pos_chamador = chamada_localizacao.get((pagina_num, numero), (None, None))
            notas_de_rodape.append(
                NotaDeRodape(
                    unit_id=nota_id,
                    numero=numero,
                    texto=texto_nota,
                    pagina_chamada=pagina_num,
                    unit_id_chamador=unit_id_chamador,
                    posicao_na_chamada=pos_chamador,
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

        return DocumentoIngerido(
            hash_documento=hash_doc,
            caminho_original=caminho_pdf,
            num_paginas=num_paginas,
            metadados=metadados,
            secoes=secoes,
            paragrafos=paragrafos,
            notas_de_rodape=notas_de_rodape,
            citacoes_recuadas=citacoes_recuadas,
            citacoes_no_corpo=citacoes_no_corpo,
            referencias=referencias,
            figuras=figuras,
            hifens_de_fim_de_linha_preservados=contagem_hifens_preservados[0],
        )

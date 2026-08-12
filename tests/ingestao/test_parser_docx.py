"""Testes estruturais do parser de .docx contra os 3 capítulos reais de
data/capitulos/. Testam estrutura (contagens, invariantes, vínculos), não
texto literal — mesma disciplina de tests/ingestao/test_parser.py (PDF).
"""

import re

from escolio.ingestao.parser_docx import parse_docx, parse_docx_multiplo
from escolio.ingestao.vocabulario import NivelHierarquia

from .conftest import requer_capitulos_docx


@requer_capitulos_docx
class TestDeterminismoDeIdentificadores:
    def test_mesmo_documento_processado_duas_vezes_gera_os_mesmos_ids(self, caminhos_capitulos_docx):
        caminho = caminhos_capitulos_docx[0]
        doc1 = parse_docx(caminho)
        doc2 = parse_docx(caminho)
        assert [p.unit_id for p in doc1.paragrafos] == [p.unit_id for p in doc2.paragrafos]
        assert [s.unit_id for s in doc1.secoes] == [s.unit_id for s in doc2.secoes]
        assert [n.unit_id for n in doc1.notas_de_rodape] == [n.unit_id for n in doc2.notas_de_rodape]
        assert [c.unit_id for c in doc1.citacoes_recuadas] == [c.unit_id for c in doc2.citacoes_recuadas]

    def test_hash_documento_e_estavel(self, caminhos_capitulos_docx):
        caminho = caminhos_capitulos_docx[0]
        doc1 = parse_docx(caminho)
        doc2 = parse_docx(caminho)
        assert doc1.hash_documento == doc2.hash_documento

    def test_todos_os_ids_seguem_o_padrao_e_sao_unicos(self, documentos_capitulos_docx):
        padrao = re.compile(r"^UNI-[A-Z]+-[0-9a-f]{8}-\d{4}-\d{4}$")
        for documento in documentos_capitulos_docx:
            todos_ids = (
                [s.unit_id for s in documento.secoes]
                + [p.unit_id for p in documento.paragrafos]
                + [n.unit_id for n in documento.notas_de_rodape]
                + [c.unit_id for c in documento.citacoes_recuadas]
                + [c.unit_id for c in documento.citacoes_no_corpo]
            )
            assert todos_ids, f"documento {documento.caminho_original} não produziu nenhuma unidade"
            for uid in todos_ids:
                assert padrao.match(uid), f"ID fora do padrão: {uid}"
            assert len(todos_ids) == len(set(todos_ids)), "IDs duplicados entre unidades"


@requer_capitulos_docx
class TestLocalizacaoSemPagina:
    """Sem página real em .docx: localização é por parágrafo/seção/
    ordinal — testado como ausência deliberada de página, não como valor
    fabricado."""

    def test_documento_nao_tem_num_paginas(self, documentos_capitulos_docx):
        for documento in documentos_capitulos_docx:
            assert documento.num_paginas is None

    def test_paragrafos_nao_tem_pagina_mas_tem_ordinal_determinístico(self, documentos_capitulos_docx):
        for documento in documentos_capitulos_docx:
            assert documento.paragrafos
            ordinais = [p.paragrafo_ordinal for p in documento.paragrafos]
            assert all(o is not None for o in ordinais)
            assert ordinais == sorted(ordinais)
            assert len(ordinais) == len(set(ordinais))
            for p in documento.paragrafos:
                assert p.pagina_inicio is None
                assert p.pagina_fim is None

    def test_secoes_nao_tem_pagina(self, documentos_capitulos_docx):
        for documento in documentos_capitulos_docx:
            for s in documento.secoes:
                assert s.pagina is None


@requer_capitulos_docx
class TestEstruturaDeSecoes:
    """Cada capítulo real tem exatamente um título de capítulo (primeiro
    parágrafo inteiramente em negrito) seguido de seções numeradas
    'N- Texto' — verificado como estrutura, não contagem exata fixa por
    documento."""

    def test_primeira_secao_e_capitulo_e_as_demais_sao_secao_ou_indeterminadas(self, documentos_capitulos_docx):
        for documento in documentos_capitulos_docx:
            assert documento.secoes
            primeira = documento.secoes[0]
            assert primeira.nivel is NivelHierarquia.CAPITULO
            assert primeira.indeterminado is False
            for s in documento.secoes[1:]:
                assert s.nivel is NivelHierarquia.SECAO or s.indeterminado is True

    def test_secao_indeterminada_carrega_motivo_e_nivel_nulo(self, documentos_capitulos_docx):
        # Correção de premissa (2026-08-12): a versão anterior deste teste
        # afirmava que NENHUM documento real teria seção indeterminada —
        # verdade só enquanto a amostra era 3 capítulos com um único
        # padrão gráfico de título. Os capítulos 4 e 5, chegados nesta
        # sessão, têm 'PERCURSO DAS FONTES.' (cap. 4): negrito como
        # qualquer título, mas nem o primeiro parágrafo do documento (esse
        # já é CAPITULO) nem casa com PADRAO_SECAO_NUMERADA — a heurística
        # não tem terceira regra para decidir, e não inventa uma (LAC-ING-014,
        # LACUNAS.md). `indeterminado=True` é o comportamento correto
        # desse caso, não uma falha a eliminar; o teste errado era afirmar
        # zero indeterminadas como invariante estrutural, quando é só o
        # que a amostra de 3 documentos aconteceu a mostrar. O invariante
        # real é: toda seção indeterminada tem `motivo_indeterminado`
        # registrado e `nivel is None` — nunca indeterminação muda,
        # nunca nível é forçado.
        for documento in documentos_capitulos_docx:
            for s in documento.secoes:
                if s.indeterminado:
                    assert s.motivo_indeterminado is not None
                    assert s.nivel is None

    def test_capitulo_4_tem_secao_indeterminada_percurso_das_fontes(self, documentos_capitulos_docx):
        # Achado empírico desta sessão, registrado como caso real e não
        # mais hipotético — ver LACUNAS.md LAC-ING-014.
        from escolio.ingestao.vocabulario import MotivoIndeterminado

        cap4 = next(
            d for d in documentos_capitulos_docx if "Achaque do bicho" in d.caminho_original
        )
        indeterminadas = [s for s in cap4.secoes if s.indeterminado]
        assert len(indeterminadas) == 1
        assert indeterminadas[0].titulo == "PERCURSO DAS FONTES."
        assert indeterminadas[0].motivo_indeterminado is MotivoIndeterminado.PADRAO_GRAFICO_AMBIGUO


@requer_capitulos_docx
class TestNotasDeRodape:
    def test_toda_nota_tem_texto_e_a_maioria_tem_chamador_resolvido(self, documentos_capitulos_docx):
        for documento in documentos_capitulos_docx:
            assert documento.notas_de_rodape
            for nota in documento.notas_de_rodape:
                assert nota.texto.strip()
            sem_chamador = [n for n in documento.notas_de_rodape if n.unit_id_chamador is None]
            # Achado empírico: nos 3 documentos reais, toda nota resolveu
            # chamador (ver LACUNAS.md). Falha aqui sinaliza regressão na
            # extração de footnoteReference, não um "quase certo".
            assert sem_chamador == []

    def test_unit_id_chamador_aponta_para_paragrafo_ou_citacao_existente(self, documentos_capitulos_docx):
        for documento in documentos_capitulos_docx:
            ids_conhecidos = {p.unit_id for p in documento.paragrafos} | {
                c.unit_id for c in documento.citacoes_recuadas
            }
            for nota in documento.notas_de_rodape:
                if nota.unit_id_chamador is not None:
                    assert nota.unit_id_chamador in ids_conhecidos


@requer_capitulos_docx
class TestComentariosWord:
    """`word/comments.xml` — só nos capítulos 3, 4 e 5 [LAC-ING-020].
    Comentário do autor é dado sobre o texto, nunca comando ao sistema
    [CLAUDE.md §8]: `texto` é armazenado literalmente, nunca interpretado."""

    def test_capitulos_sem_comments_xml_produzem_lista_vazia(self, documentos_capitulos_docx):
        sem_comentario = [
            d for d in documentos_capitulos_docx
            if "Endoparasitoses" in d.caminho_original or "Ectoparasitoses" in d.caminho_original
        ]
        assert len(sem_comentario) == 2
        for documento in sem_comentario:
            assert documento.comentarios_word == []

    def test_capitulos_3_a_5_tem_comentarios_reais(self, documentos_capitulos_docx):
        com_comentario = {
            d.caminho_original: d.comentarios_word
            for d in documentos_capitulos_docx
            if "Terap" in d.caminho_original or "bicho" in d.caminho_original or "Tropical" in d.caminho_original
        }
        assert len(com_comentario) == 3
        for caminho, comentarios in com_comentario.items():
            assert comentarios, f"esperado ao menos 1 comentário em {caminho}"
            for c in comentarios:
                assert c.autor
                assert c.texto.strip()
                assert c.data is not None

    def test_comentario_ancorado_tem_intervalo_dentro_do_texto_da_unidade(self, documentos_capitulos_docx):
        ids_conhecidos = {}
        for documento in documentos_capitulos_docx:
            ids_conhecidos.update({s.unit_id: s.titulo for s in documento.secoes})
            ids_conhecidos.update({p.unit_id: p.texto for p in documento.paragrafos})
            ids_conhecidos.update({c.unit_id: c.texto for c in documento.citacoes_recuadas})
        for documento in documentos_capitulos_docx:
            for c in documento.comentarios_word:
                if c.indeterminado:
                    continue
                assert c.unit_id_ancora in ids_conhecidos
                texto_ancora = ids_conhecidos[c.unit_id_ancora]
                assert 0 <= c.posicao_inicio <= c.posicao_fim <= len(texto_ancora)

    def test_comentario_sem_ancora_no_corpo_e_indeterminado_nao_erro(self, documentos_capitulos_docx):
        # Achado empírico (cap. 3): um comentário é resposta a outro
        # (thread) e não tem intervalo próprio no corpo do documento —
        # `unit_id_ancora=None` é resultado legítimo, não falha de
        # extração [LACUNAS.md LAC-ING-020].
        from escolio.ingestao.vocabulario import MotivoIndeterminado

        cap3 = next(d for d in documentos_capitulos_docx if "Terap" in d.caminho_original)
        sem_ancora = [c for c in cap3.comentarios_word if c.indeterminado]
        assert len(sem_ancora) == 1
        assert sem_ancora[0].unit_id_ancora is None
        assert sem_ancora[0].posicao_inicio is None
        assert sem_ancora[0].posicao_fim is None
        assert sem_ancora[0].motivo_indeterminado is MotivoIndeterminado.SEM_ANCORA_TEXTUAL

    def test_comentario_pode_ancorar_em_secao_nao_so_em_paragrafo(self, documentos_capitulos_docx):
        # Achado empírico: os 4 comentários do capítulo 4 ancoram em
        # títulos de seção (Secao), não em parágrafo de corpo — a
        # extração não pode presumir um único tipo de unidade ancorável.
        cap4 = next(d for d in documentos_capitulos_docx if "bicho" in d.caminho_original)
        ids_secao = {s.unit_id for s in cap4.secoes}
        assert cap4.comentarios_word
        assert all(c.unit_id_ancora in ids_secao for c in cap4.comentarios_word)

    def test_parse_docx_multiplo_combina_comentarios_dos_5_arquivos(
        self, caminhos_capitulos_docx, documentos_capitulos_docx
    ):
        combinado = parse_docx_multiplo(caminhos_capitulos_docx)
        assert len(combinado.comentarios_word) == sum(
            len(d.comentarios_word) for d in documentos_capitulos_docx
        )


@requer_capitulos_docx
class TestCitacoesRecuadas:
    def test_citacoes_recuadas_tem_texto_e_secao(self, documentos_capitulos_docx):
        for documento in documentos_capitulos_docx:
            assert documento.citacoes_recuadas
            for c in documento.citacoes_recuadas:
                assert c.texto.strip()
                assert c.pagina_inicio is None
                assert c.pagina_fim is None


@requer_capitulos_docx
class TestCartografiaGlobalMultiplaArquivo:
    """A tese completa é a soma dos 3 capítulos [confirmado pelo professor]
    — `parse_docx_multiplo` combina os 3 arquivos numa única obra."""

    def test_combina_secoes_paragrafos_e_notas_dos_3_arquivos(self, caminhos_capitulos_docx, documentos_capitulos_docx):
        combinado = parse_docx_multiplo(caminhos_capitulos_docx)
        assert len(combinado.secoes) == sum(len(d.secoes) for d in documentos_capitulos_docx)
        assert len(combinado.paragrafos) == sum(len(d.paragrafos) for d in documentos_capitulos_docx)
        assert len(combinado.notas_de_rodape) == sum(len(d.notas_de_rodape) for d in documentos_capitulos_docx)

    def test_unit_ids_nao_colidem_entre_arquivos(self, caminhos_capitulos_docx):
        combinado = parse_docx_multiplo(caminhos_capitulos_docx)
        todos_ids = (
            [s.unit_id for s in combinado.secoes]
            + [p.unit_id for p in combinado.paragrafos]
            + [n.unit_id for n in combinado.notas_de_rodape]
            + [c.unit_id for c in combinado.citacoes_recuadas]
        )
        assert len(todos_ids) == len(set(todos_ids))

    def test_cada_capitulo_tem_exatamente_um_nivel_capitulo_e_secoes_apontam_para_ele(
        self, caminhos_capitulos_docx, documentos_capitulos_docx
    ):
        combinado = parse_docx_multiplo(caminhos_capitulos_docx)
        capitulos = [s for s in combinado.secoes if s.nivel is NivelHierarquia.CAPITULO]
        assert len(capitulos) == len(documentos_capitulos_docx)
        ids_capitulos = {s.unit_id for s in capitulos}
        for s in combinado.secoes:
            if s.nivel is NivelHierarquia.SECAO:
                assert s.secao_pai_id in ids_capitulos

    def test_hash_combinado_e_deterministico_e_muda_com_a_ordem(self, caminhos_capitulos_docx):
        c1 = parse_docx_multiplo(caminhos_capitulos_docx)
        c2 = parse_docx_multiplo(caminhos_capitulos_docx)
        assert c1.hash_documento == c2.hash_documento
        invertido = parse_docx_multiplo(list(reversed(caminhos_capitulos_docx)))
        assert invertido.hash_documento != c1.hash_documento


@requer_capitulos_docx
class TestSemReferenciasNemFiguras:
    """Achado empírico desta calibração: os 3 capítulos reais citam só
    por nota de rodapé, sem lista de referências separada, e não têm
    figura/tabela/quadro. Ver LACUNAS.md."""

    def test_referencias_e_figuras_vazias(self, documentos_capitulos_docx):
        for documento in documentos_capitulos_docx:
            assert documento.referencias == []
            assert documento.figuras == []

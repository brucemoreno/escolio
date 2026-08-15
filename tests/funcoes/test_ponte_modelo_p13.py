"""Testes da ponte entre `escolio/funcoes/execucao_p13.py` e
`escolio/cliente/` — etapas 8, 9 e 16-18.

Cliente mockado, como já é convenção em `tests/cliente/test_cliente.py`.
Nenhuma chamada real à API [instrução da sessão]."""

from unittest.mock import MagicMock

import pytest

from escolio.comentarios.criticidade import ClasseCriticidade, EixoCriticidade, MatrizCriticidade
from escolio.comentarios.seletividade import MatrizSeletividade, SelectionDecision
from escolio.comentarios.vocabulario import (
    COMMENT_TYPE_COMENTARIO_MATRIZ,
    COMMENT_TYPE_REMISSAO_A_COMENTARIO_MATRIZ,
    P13CommentStatus,
)
from escolio.funcoes import ponte_modelo_p13 as ponte
from escolio.ingestao.erros import ErroDeIngestao
from escolio.ingestao.modelos import ComentarioWord, DocumentoIngerido, Metadados, Paragrafo
from escolio.voz.amostra import AmostraAutoral, SolicitacaoDeAmostrasAdicionais
from escolio.voz.dimensoes import DIMENSOES_OBRIGATORIAS, DimensaoDeVoz
from escolio.voz.perfil import PerfilDeVoz
from escolio.voz.vocabulario import Confidence as ConfidenceVoz
from escolio.voz.vocabulario import DesvioBloqueante, StatusDePerfil, TipoDePerfil


def documento_sintetico() -> DocumentoIngerido:
    return DocumentoIngerido(
        hash_documento="sinteticoponte001",
        caminho_original="synthetic://doc-ponte-p13-01",
        num_paginas=1,
        metadados=Metadados(titulo="Documento sintético — ponte de modelo P13"),
        paragrafos=[
            Paragrafo(
                unit_id="UNI-PAR-0001",
                texto="Parágrafo sintético usado para exercitar a ponte de modelo.",
                pagina_inicio=1,
                pagina_fim=1,
                secao_id=None,
            )
        ],
    )


def documento_com_comentario_word() -> DocumentoIngerido:
    documento = documento_sintetico()
    documento.comentarios_word.append(
        ComentarioWord(
            unit_id="UNI-COM-0001",
            autor="Rodrigo Perles Dantas",
            texto="Falar das pulgas e piolhos.",
            data="2026-02-16T13:15:02+00:00",
            unit_id_ancora="UNI-PAR-0001",
            posicao_inicio=0,
            posicao_fim=10,
        )
    )
    return documento


def cliente_fake(blocos: list[dict]) -> MagicMock:
    cliente = MagicMock()
    cliente.chamar.return_value = MagicMock(blocos=blocos)
    return cliente


def cliente_fake_sequencia(lista_de_blocos: list[list[dict]]) -> MagicMock:
    """Um retorno diferente por chamada — para testar lotes (cada lote é
    uma chamada real distinta a `cliente.chamar`)."""
    cliente = MagicMock()
    cliente.chamar.side_effect = [MagicMock(blocos=blocos) for blocos in lista_de_blocos]
    return cliente


def _bloco_criticidade(unit_id: str, problem_id: str) -> dict:
    avaliacao = {eixo.value: f"avaliação {eixo.value}" for eixo in EixoCriticidade}
    return {
        "type": "tool_use",
        "name": ponte._FERRAMENTA_CRITICIDADE,
        "input": {
            "matrizes": [
                {
                    "problem_id": problem_id,
                    "unit_id": unit_id,
                    "avaliacao_por_eixo": avaliacao,
                    "classe": "CRITICIDADE_MEDIA",
                    "justificativa_classe": "x",
                }
            ]
        },
    }


class TestGerarMatrizesCriticidadeEmLotes:
    def test_unit_ids_acima_do_lote_gera_multiplas_chamadas(self):
        documento = documento_sintetico()
        n = ponte.TAMANHO_LOTE_ETAPA_8 + 3
        unit_ids = [f"UNI-PAR-{i:04d}" for i in range(n)]
        # Cada "lote" simulado devolve 1 matriz só (suficiente para contar
        # chamadas e agregação, não para testar o conteúdo completo de
        # cada lote).
        cliente = cliente_fake_sequencia(
            [[_bloco_criticidade(unit_ids[0], "PROB-0")], [_bloco_criticidade(unit_ids[-1], "PROB-1")]]
        )

        matrizes = ponte.gerar_matrizes_criticidade(documento=documento, unit_ids=unit_ids, cliente=cliente)

        assert cliente.chamar.call_count == 2  # ceil(n / TAMANHO_LOTE_ETAPA_8)
        assert len(matrizes) == 2

        indices = [kwargs["indice_na_sequencia"] for _, kwargs in cliente.chamar.call_args_list]
        assert indices == [0, 1]

    def test_unit_ids_dentro_do_lote_gera_uma_chamada_so(self):
        documento = documento_sintetico()
        unit_ids = [f"UNI-PAR-{i:04d}" for i in range(ponte.TAMANHO_LOTE_ETAPA_8)]
        cliente = cliente_fake([_bloco_criticidade(unit_ids[0], "PROB-0")])

        ponte.gerar_matrizes_criticidade(documento=documento, unit_ids=unit_ids, cliente=cliente)

        assert cliente.chamar.call_count == 1

    def test_erro_de_cliente_no_meio_dos_lotes_propaga_sem_capturar(self):
        from escolio.cliente.erros import ErroDeTimeout

        documento = documento_sintetico()
        unit_ids = [f"UNI-PAR-{i:04d}" for i in range(ponte.TAMANHO_LOTE_ETAPA_8 + 1)]
        cliente = MagicMock()
        cliente.chamar.side_effect = [
            MagicMock(blocos=[_bloco_criticidade(unit_ids[0], "PROB-0")]),
            ErroDeTimeout("timeout sintético"),
        ]

        with pytest.raises(ErroDeTimeout):
            ponte.gerar_matrizes_criticidade(documento=documento, unit_ids=unit_ids, cliente=cliente)


class TestGerarMatrizesCriticidade:
    def test_tool_use_valido_produz_matrizcriticidade(self):
        documento = documento_sintetico()
        avaliacao = {eixo.value: f"avaliação {eixo.value}" for eixo in EixoCriticidade}
        blocos = [
            {
                "type": "tool_use",
                "name": ponte._FERRAMENTA_CRITICIDADE,
                "input": {
                    "matrizes": [
                        {
                            "problem_id": "PROB-0001",
                            "unit_id": "UNI-PAR-0001",
                            "avaliacao_por_eixo": avaliacao,
                            "classe": "CRITICIDADE_MEDIA",
                            "justificativa_classe": "Síntese sintética.",
                        }
                    ]
                },
            }
        ]
        cliente = cliente_fake(blocos)

        matrizes = ponte.gerar_matrizes_criticidade(
            documento=documento, unit_ids=["UNI-PAR-0001"], cliente=cliente
        )

        assert len(matrizes) == 1
        assert isinstance(matrizes[0], MatrizCriticidade)
        assert matrizes[0].classe is ClasseCriticidade.CRITICIDADE_MEDIA

        _, kwargs = cliente.chamar.call_args
        assert kwargs["model"] == ponte.MODEL_ETAPA_8
        assert kwargs["effort"] == ponte.EFFORT_ETAPA_8
        assert kwargs["tools"][0]["name"] == ponte._FERRAMENTA_CRITICIDADE

    def test_eixo_faltante_levanta_erro_de_ponte(self):
        documento = documento_sintetico()
        avaliacao_incompleta = {EixoCriticidade.FACTUAL.value: "x"}  # falta os outros 11
        blocos = [
            {
                "type": "tool_use",
                "name": ponte._FERRAMENTA_CRITICIDADE,
                "input": {
                    "matrizes": [
                        {
                            "problem_id": "PROB-0002",
                            "unit_id": "UNI-PAR-0001",
                            "avaliacao_por_eixo": avaliacao_incompleta,
                            "classe": "CRITICIDADE_BAIXA",
                            "justificativa_classe": "x",
                        }
                    ]
                },
            }
        ]
        cliente = cliente_fake(blocos)

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_matrizes_criticidade(documento=documento, unit_ids=["UNI-PAR-0001"], cliente=cliente)

    def test_item_de_matrizes_nao_objeto_levanta_erro_de_ponte_nao_typeerror_cru(self):
        """Achado real do piloto contra o capítulo 5 (2026-08-13): o modelo
        devolveu ao menos um item de 'matrizes' como string, não objeto —
        `item["avaliacao_por_eixo"]` levantava `TypeError` cru antes desta
        correção. Deve virar `ErroDePonteModeloP13`, nunca `TypeError`."""
        documento = documento_sintetico()
        blocos = [
            {
                "type": "tool_use",
                "name": ponte._FERRAMENTA_CRITICIDADE,
                "input": {"matrizes": ["isto não é um objeto"]},
            }
        ]
        cliente = cliente_fake(blocos)

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_matrizes_criticidade(documento=documento, unit_ids=["UNI-PAR-0001"], cliente=cliente)

    def test_sem_tool_use_levanta_erro_de_ponte(self):
        documento = documento_sintetico()
        cliente = cliente_fake([{"type": "text", "text": "resposta fora da ferramenta"}])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_matrizes_criticidade(documento=documento, unit_ids=["UNI-PAR-0001"], cliente=cliente)

    def test_sem_unit_ids_levanta_erro_de_ponte_antes_de_chamar(self):
        documento = documento_sintetico()
        cliente = cliente_fake([])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_matrizes_criticidade(documento=documento, unit_ids=[], cliente=cliente)
        cliente.chamar.assert_not_called()


class TestSchemaSeletividadeDistingueNoveltyDeRecurrence:
    """Trava estrutural (2026-08-12) para a pergunta do professor sobre
    `NAO_COMENTAR_POR_REPETICAO`: sem isto, nada além do prompt em
    `prompts/p13_matriz_seletividade.md` garante que 'autor já sabia'
    (novelty) não se confunda com 'ocorre em outro lugar do documento'
    (recurrence) ou 'sistema já comentou' (matrix_comment_coverage) — e
    nenhum teste pode chamar o modelo para verificar isso na prosa. A
    `description` de cada propriedade no schema É código Python, não
    prosa em `.md`: uma edição que a remova ou a esvazie quebra este
    teste, sem precisar de chamada real à API."""

    def _propriedades(self):
        return ponte._SCHEMA_SELETIVIDADE["input_schema"]["properties"]["matrizes"]["items"][
            "properties"
        ]

    def test_novelty_recurrence_e_matrix_comment_coverage_tem_description_nao_vazia(self):
        props = self._propriedades()
        for campo in ("novelty", "recurrence", "matrix_comment_coverage"):
            assert props[campo].get("description", "").strip(), (
                f"'{campo}' sem description no schema — a distinção volta a depender só do "
                "prompt em prosa, não verificável sem chamar o modelo"
            )

    def test_novelty_description_menciona_comentario_do_autor_e_nao_recurrence(self):
        props = self._propriedades()
        assert "autor" in props["novelty"]["description"].lower()
        assert "recurrence" in props["novelty"]["description"] or "'recurrence'" in props["novelty"]["description"]

    def test_recurrence_description_redireciona_caso_de_autor_para_novelty(self):
        # recurrence é sobre repetição interna ao documento; a menção a
        # "autor" aqui só é aceitável como exclusão explícita ("isso é
        # novelty, não aqui") — se a referência a 'novelty' desaparecer,
        # a exclusão colapsou de volta em ambiguidade.
        props = self._propriedades()
        assert "novelty" in props["recurrence"]["description"]

    def test_matrix_comment_coverage_distingue_sistema_de_autor(self):
        props = self._propriedades()
        descricao = props["matrix_comment_coverage"]["description"].lower()
        assert "sistema" in descricao
        assert "autor" in descricao


def _bloco_seletividade(selection_id: str, unit_id: str, problem_id: str) -> dict:
    return {
        "type": "tool_use",
        "name": ponte._FERRAMENTA_SELETIVIDADE,
        "input": {
            "matrizes": [
                {
                    "selection_id": selection_id,
                    "unit_id": unit_id,
                    "candidate_problem_id": problem_id,
                    "criticality": "CRITICIDADE_ALTA",
                    "material_impact": "x",
                    "novelty": "x",
                    "recurrence": "x",
                    "matrix_comment_coverage": "x",
                    "actionability": "x",
                    "evidence_sufficiency": "x",
                    "human_decision_required": "x",
                    "privacy_risk": "x",
                    "selection_decision": "COMENTAR",
                    "selection_rationale": "x",
                }
            ]
        },
    }


class TestGerarMatrizesSeletividadeEmLotes:
    def test_candidatos_acima_do_lote_gera_multiplas_chamadas(self):
        documento = documento_sintetico()
        n = ponte.TAMANHO_LOTE_ETAPA_9 + 2
        candidatos = [
            MatrizCriticidade(
                problem_id=f"PROB-{i:04d}",
                unit_id="UNI-PAR-0001",
                avaliacao_por_eixo={eixo: "x" for eixo in EixoCriticidade},
                classe=ClasseCriticidade.CRITICIDADE_ALTA,
                justificativa_classe="x",
            )
            for i in range(n)
        ]
        cliente = cliente_fake_sequencia(
            [
                [_bloco_seletividade("SEL-0", "UNI-PAR-0001", "PROB-0000")],
                [_bloco_seletividade("SEL-1", "UNI-PAR-0001", "PROB-0001")],
            ]
        )

        matrizes = ponte.gerar_matrizes_seletividade(
            documento=documento, matrizes_criticidade=candidatos, cliente=cliente
        )

        assert cliente.chamar.call_count == 2
        assert len(matrizes) == 2


class TestGerarMatrizesSeletividade:
    def test_tool_use_valido_produz_matrizseletividade(self):
        documento = documento_sintetico()
        matriz_criticidade = MatrizCriticidade(
            problem_id="PROB-0001",
            unit_id="UNI-PAR-0001",
            avaliacao_por_eixo={eixo: "x" for eixo in EixoCriticidade},
            classe=ClasseCriticidade.CRITICIDADE_ALTA,
            justificativa_classe="x",
        )
        blocos = [
            {
                "type": "tool_use",
                "name": ponte._FERRAMENTA_SELETIVIDADE,
                "input": {
                    "matrizes": [
                        {
                            "selection_id": "SEL-0001",
                            "unit_id": "UNI-PAR-0001",
                            "candidate_problem_id": "PROB-0001",
                            "criticality": "CRITICIDADE_ALTA",
                            "material_impact": "x",
                            "novelty": "x",
                            "recurrence": "x",
                            "matrix_comment_coverage": "x",
                            "actionability": "x",
                            "evidence_sufficiency": "x",
                            "human_decision_required": "x",
                            "privacy_risk": "x",
                            "selection_decision": "COMENTAR",
                            "selection_rationale": "x",
                        }
                    ]
                },
            }
        ]
        cliente = cliente_fake(blocos)

        matrizes = ponte.gerar_matrizes_seletividade(
            documento=documento, matrizes_criticidade=[matriz_criticidade], cliente=cliente
        )

        assert len(matrizes) == 1
        assert isinstance(matrizes[0], MatrizSeletividade)
        assert matrizes[0].selection_decision is SelectionDecision.COMENTAR

        _, kwargs = cliente.chamar.call_args
        assert kwargs["model"] == ponte.MODEL_ETAPA_9
        assert kwargs["effort"] == ponte.EFFORT_ETAPA_9

    def test_sem_candidatos_levanta_erro_de_ponte_antes_de_chamar(self):
        documento = documento_sintetico()
        cliente = cliente_fake([])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_matrizes_seletividade(documento=documento, matrizes_criticidade=[], cliente=cliente)
        cliente.chamar.assert_not_called()

    def test_comentarios_word_entram_no_system_estavel(self):
        # Sessão de 2026-08-12: a etapa 9 passa a receber os comentários
        # do Word já existentes no documento como contexto — dado, nunca
        # comando [CLAUDE.md §8]. Julgar "mesmo achado ou outro" é do
        # prompt, não deste código; aqui só verificamos que o dado chega.
        documento = documento_com_comentario_word()
        matriz_criticidade = MatrizCriticidade(
            problem_id="PROB-0001",
            unit_id="UNI-PAR-0001",
            avaliacao_por_eixo={eixo: "x" for eixo in EixoCriticidade},
            classe=ClasseCriticidade.CRITICIDADE_ALTA,
            justificativa_classe="x",
        )
        cliente = cliente_fake([])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            # levanta por falta de tool_use — não é o que este teste
            # verifica; o que importa é o conteúdo de `system_estavel`
            # já enviado quando a chamada aconteceu.
            ponte.gerar_matrizes_seletividade(
                documento=documento, matrizes_criticidade=[matriz_criticidade], cliente=cliente
            )

        _, kwargs = cliente.chamar.call_args
        assert "Rodrigo Perles Dantas" in kwargs["system_estavel"]
        assert "Falar das pulgas e piolhos." in kwargs["system_estavel"]
        assert "UNI-PAR-0001" in kwargs["system_estavel"]

    def test_documento_sem_comentario_word_nao_quebra_e_lista_fica_vazia(self):
        documento = documento_sintetico()
        assert documento.comentarios_word == []
        matriz_criticidade = MatrizCriticidade(
            problem_id="PROB-0001",
            unit_id="UNI-PAR-0001",
            avaliacao_por_eixo={eixo: "x" for eixo in EixoCriticidade},
            classe=ClasseCriticidade.CRITICIDADE_ALTA,
            justificativa_classe="x",
        )
        cliente = cliente_fake([])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_matrizes_seletividade(
                documento=documento, matrizes_criticidade=[matriz_criticidade], cliente=cliente
            )

        _, kwargs = cliente.chamar.call_args
        assert "Comentários do Word" in kwargs["system_estavel"]
        assert "Rodrigo Perles Dantas" not in kwargs["system_estavel"]


class TestEscopoComentariosWordRestritoAEtapa9:
    """Decisão desta sessão (2026-08-12): só a etapa 9 recebe
    `comentarios_word` no prompt — etapas 8 e 16-18 não, para não alterar
    o prefixo `system` cacheado dessas chamadas sem necessidade."""

    def test_etapa_8_criticidade_nao_recebe_comentarios_word(self):
        documento = documento_com_comentario_word()
        cliente = cliente_fake([])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_matrizes_criticidade(documento=documento, unit_ids=["UNI-PAR-0001"], cliente=cliente)

        _, kwargs = cliente.chamar.call_args
        assert "Falar das pulgas e piolhos." not in kwargs["system_estavel"]

    def test_etapas_16_18_elaboracao_nao_recebem_comentarios_word(self):
        documento = documento_com_comentario_word()
        cliente = cliente_fake([])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_comentarios(
                documento=documento,
                document_id="MAT-DOC-0001",
                document_version="1.0.0",
                module_id="P13",
                candidatos=[candidato_selecionado()],
                cliente=cliente,
            )

        _, kwargs = cliente.chamar.call_args
        assert "Falar das pulgas e piolhos." not in kwargs["system_estavel"]


def candidato_selecionado(selection_id="SEL-0001", problem_id="PROB-0001") -> MatrizSeletividade:
    return MatrizSeletividade(
        selection_id=selection_id,
        unit_id="UNI-PAR-0001",
        candidate_problem_id=problem_id,
        criticality=ClasseCriticidade.CRITICIDADE_ALTA,
        material_impact="x",
        novelty="x",
        recurrence="x",
        matrix_comment_coverage="x",
        actionability="x",
        evidence_sufficiency="x",
        human_decision_required="x",
        privacy_risk="x",
        selection_decision=SelectionDecision.COMENTAR,
        selection_rationale="x",
    )


def bloco_comentario(*, selection_id="SEL-0001", comment_type="COMENTARIO_FACTUAL", matrix_comment_id=None):
    return {
        "type": "tool_use",
        "name": ponte._FERRAMENTA_COMENTARIOS,
        "input": {
            "comentarios": [
                {
                    "comment_id": "CMT-0001",
                    "selection_id": selection_id,
                    "unit_id": "UNI-PAR-0001",
                    "anchor_start": "0",
                    "anchor_end": "10",
                    "anchor_text_hash": "sha256:x",
                    "comment_type": comment_type,
                    "priority": "PRIORIDADE_MEDIA",
                    "severity": "MODERADA",
                    "problem": "x",
                    "evidence": "x",
                    "impact": "x",
                    "recommended_action": "x",
                    "intervention_level": "INT-04",
                    "authority_required": "USUARIO_PROPONENTE",
                    "gate": "GATE_DE_VALIDACAO_FINAL",
                    "source_status": "VERIFICADA",
                    "voice_impact": "NENHUM",
                    "privacy_classification": "PUBLIC",
                    "reversible": True,
                    **({"matrix_comment_id": matrix_comment_id} if matrix_comment_id else {}),
                }
            ]
        },
    }


class TestGerarComentarios:
    def test_tool_use_valido_produz_p13comment_em_status_draft(self):
        documento = documento_sintetico()
        cliente = cliente_fake([bloco_comentario()])

        comentarios = ponte.gerar_comentarios(
            documento=documento,
            document_id="MAT-DOC-0001",
            document_version="1.0.0",
            module_id="P13",
            candidatos=[candidato_selecionado()],
            cliente=cliente,
        )

        assert len(comentarios) == 1
        assert comentarios[0].status is P13CommentStatus.DRAFT
        assert comentarios[0].document_id == "MAT-DOC-0001"

        _, kwargs = cliente.chamar.call_args
        assert kwargs["model"] == ponte.MODEL_ETAPAS_16_18
        assert kwargs["effort"] == ponte.EFFORT_ETAPAS_16_18

    def test_comment_type_divergente_do_esperado_levanta_erro(self):
        documento = documento_sintetico()
        cliente = cliente_fake([bloco_comentario(comment_type="COMENTARIO_FACTUAL")])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_comentarios(
                documento=documento,
                document_id="MAT-DOC-0001",
                document_version="1.0.0",
                module_id="P13",
                candidatos=[candidato_selecionado()],
                cliente=cliente,
                comment_type_esperado=COMMENT_TYPE_COMENTARIO_MATRIZ,
            )

    def test_matrix_comment_id_do_chamador_sobrescreve_o_do_modelo(self):
        documento = documento_sintetico()
        cliente = cliente_fake(
            [
                bloco_comentario(
                    comment_type=COMMENT_TYPE_REMISSAO_A_COMENTARIO_MATRIZ,
                    matrix_comment_id="CMT-MATRIZ-ERRADO",
                )
            ]
        )

        comentarios = ponte.gerar_comentarios(
            documento=documento,
            document_id="MAT-DOC-0001",
            document_version="1.0.0",
            module_id="P13",
            candidatos=[candidato_selecionado()],
            cliente=cliente,
            comment_type_esperado=COMMENT_TYPE_REMISSAO_A_COMENTARIO_MATRIZ,
            matrix_comment_id_por_candidato={"SEL-0001": "CMT-MATRIZ-CORRETO"},
        )

        assert comentarios[0].matrix_comment_id == "CMT-MATRIZ-CORRETO"

    def test_sem_candidatos_levanta_erro_de_ponte_antes_de_chamar(self):
        documento = documento_sintetico()
        cliente = cliente_fake([])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_comentarios(
                documento=documento,
                document_id="MAT-DOC-0001",
                document_version="1.0.0",
                module_id="P13",
                candidatos=[],
                cliente=cliente,
            )
        cliente.chamar.assert_not_called()


def perfil_de_voz_sintetico(**overrides) -> PerfilDeVoz:
    campos = {
        "profile_id": "PV-EXEC-0001",
        "profile_type": TipoDePerfil.PERFIL_NEUTRO_ACADEMICO_CONTROLADO,
        "purpose": "preservar a voz do autor avaliado na revisão",
        "scope": {"documento": "doc-ponte-p13-01"},
        "dimensions": {},
        "evidence": [],
        "confidence": ConfidenceVoz.NAO_APLICAVEL,
        "authorization": {},
        "versioning": {"versao": 1},
        "provenance": [],
        "reversibility": {"reversivel": True},
        "status": StatusDePerfil.VALIDADO,
    }
    campos.update(overrides)
    return PerfilDeVoz(**campos)


def bloco_achado_fidelidade(
    *, tipo="INVENCAO_FACTUAL", observado=True, evidencia="trecho X diverge do original", confianca="ALTA"
):
    return {
        "type": "tool_use",
        "name": ponte._FERRAMENTA_DETECCAO_FIDELIDADE,
        "input": {
            "achados": [
                {
                    "tipo": tipo,
                    "observado": observado,
                    "evidencia": evidencia,
                    "confianca": confianca,
                    "notas": None,
                }
            ]
        },
    }


class TestGerarAchadosFidelidade:
    def test_tool_use_valido_produz_achadodefidelidade(self):
        documento = documento_sintetico()
        perfil = perfil_de_voz_sintetico()
        cliente = cliente_fake([bloco_achado_fidelidade()])

        achados = ponte.gerar_achados_fidelidade(
            documento=documento, unit_id="UNI-PAR-0001", perfil=perfil, cliente=cliente
        )

        assert len(achados) == 1
        assert achados[0].tipo is DesvioBloqueante.INVENCAO_FACTUAL
        assert achados[0].observado is True

        _, kwargs = cliente.chamar.call_args
        assert kwargs["model"] == ponte.MODEL_ETAPA_13
        assert kwargs["effort"] == ponte.EFFORT_ETAPA_13
        assert "PV-EXEC-0001" in kwargs["system_estavel"]
        assert "UNI-PAR-0001" in kwargs["unidades"][0]["text"]

    def test_observado_true_sem_evidencia_levanta_erro_de_ponte(self):
        documento = documento_sintetico()
        perfil = perfil_de_voz_sintetico()
        cliente = cliente_fake([bloco_achado_fidelidade(evidencia="")])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_achados_fidelidade(
                documento=documento, unit_id="UNI-PAR-0001", perfil=perfil, cliente=cliente
            )

    def test_tipo_fora_do_vocabulario_levanta_erro_de_ponte(self):
        documento = documento_sintetico()
        perfil = perfil_de_voz_sintetico()
        cliente = cliente_fake([bloco_achado_fidelidade(tipo="DESVIO_INVENTADO")])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_achados_fidelidade(
                documento=documento, unit_id="UNI-PAR-0001", perfil=perfil, cliente=cliente
            )

    def test_unit_id_desconhecido_levanta_antes_de_chamar_modelo(self):
        documento = documento_sintetico()
        perfil = perfil_de_voz_sintetico()
        cliente = cliente_fake([])

        with pytest.raises(ErroDeIngestao):
            ponte.gerar_achados_fidelidade(
                documento=documento, unit_id="UNI-PAR-INEXISTENTE", perfil=perfil, cliente=cliente
            )
        cliente.chamar.assert_not_called()

    def test_texto_proposto_opcional_entra_na_mensagem_quando_fornecido(self):
        documento = documento_sintetico()
        perfil = perfil_de_voz_sintetico()
        cliente = cliente_fake([bloco_achado_fidelidade(observado=False, evidencia="")])

        ponte.gerar_achados_fidelidade(
            documento=documento,
            unit_id="UNI-PAR-0001",
            perfil=perfil,
            cliente=cliente,
            texto_proposto="Versão revisada do parágrafo.",
        )

        _, kwargs = cliente.chamar.call_args
        assert "Versão revisada do parágrafo." in kwargs["unidades"][0]["text"]


def _bloco_relacao(**overrides) -> dict:
    item = {
        "claim_id": "CLAIM-UNI-PAR-0001-1",
        "claim_text": "Afirmação sintética candidata.",
        "claim_type": "FATUAL",
        "source_id": "[INFERIDO]",
        "source_type": "DOCUMENTO",
        "source_reference": "Autor sintético",
        "location_type": "NAO_CONFIRMADO",
        "evidence_level": "D_AUSENTE",
        "access_state": "NAO_LOCALIZADA",
        "reading_state": "LEITURA_NAO_REALIZADA",
        "validation_state": "NAO_VERIFICADA",
        "sufficiency": "EVIDENCIA_INSUFICIENTE",
        "confidence": "BAIXA",
        "usage_status": "USO_CONDICIONAL",
        "reversibility": "REVERSIVEL_COM_NOVA_EVIDENCIA",
    }
    item.update(overrides)
    return {
        "type": "tool_use",
        "name": ponte._FERRAMENTA_RELACAO,
        "input": {"relacoes": [item]},
    }


class TestGerarRelacoesAfirmacaoEvidencia:
    def test_tool_use_valido_produz_relacao(self):
        documento = documento_sintetico()
        cliente = cliente_fake([_bloco_relacao()])

        relacoes = ponte.gerar_relacoes_afirmacao_evidencia(
            documento=documento, unit_ids=["UNI-PAR-0001"], cliente=cliente
        )

        assert len(relacoes) == 1
        assert relacoes[0].claim_id == "CLAIM-UNI-PAR-0001-1"
        assert relacoes[0].provenance == "[INFERIDO]"
        assert relacoes[0].validator is None
        assert relacoes[0].validation_date is None

        _, kwargs = cliente.chamar.call_args
        assert kwargs["model"] == ponte.MODEL_ETAPA_12
        assert kwargs["effort"] == ponte.EFFORT_ETAPA_12
        assert kwargs["tools"][0]["name"] == ponte._FERRAMENTA_RELACAO

    def test_leitura_indireta_produz_provenance_com_fonte_intermediaria(self):
        """RC-010 (achado real, piloto capítulo 5, 2026-08-14): LEITURA_INDIRETA
        exige que `provenance` nomeie a fonte intermediária — antes desta
        correção, `provenance` era sempre `"[INFERIDO]"`, o que violava RC-010
        incondicionalmente neste caso."""
        documento = documento_sintetico()
        cliente = cliente_fake([_bloco_relacao(reading_state="LEITURA_INDIRETA")])

        relacoes = ponte.gerar_relacoes_afirmacao_evidencia(
            documento=documento, unit_ids=["UNI-PAR-0001"], cliente=cliente
        )

        assert len(relacoes) == 1
        assert "intermediari" in relacoes[0].provenance.lower()

    def test_campo_obrigatorio_ausente_levanta_erro_de_ponte(self):
        documento = documento_sintetico()
        item = {
            "type": "tool_use",
            "name": ponte._FERRAMENTA_RELACAO,
            "input": {"relacoes": [{"claim_id": "CLAIM-1"}]},
        }
        cliente = cliente_fake([item])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_relacoes_afirmacao_evidencia(
                documento=documento, unit_ids=["UNI-PAR-0001"], cliente=cliente
            )

    def test_item_de_relacoes_nao_objeto_levanta_erro_de_ponte_nao_typeerror_cru(self):
        documento = documento_sintetico()
        blocos = [
            {
                "type": "tool_use",
                "name": ponte._FERRAMENTA_RELACAO,
                "input": {"relacoes": ["isto não é um objeto"]},
            }
        ]
        cliente = cliente_fake(blocos)

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_relacoes_afirmacao_evidencia(
                documento=documento, unit_ids=["UNI-PAR-0001"], cliente=cliente
            )

    def test_outra_controlada_sem_notes_levanta_erro_de_ponte(self):
        """`escolio/relacao.py`: claim_type=OUTRA_CONTROLADA exige notes —
        regra de coerência do dataclass, não duplicada aqui; deve virar
        `ErroDePonteModeloP13`, não `ErroDeCoerencia` cru."""
        documento = documento_sintetico()
        cliente = cliente_fake([_bloco_relacao(claim_type="OUTRA_CONTROLADA")])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_relacoes_afirmacao_evidencia(
                documento=documento, unit_ids=["UNI-PAR-0001"], cliente=cliente
            )

    def test_validation_state_validada_fora_do_vocabulario_permitido(self):
        """`VALIDADA` não está no enum restrito da ferramenta — o schema
        JSON já rejeitaria; aqui simulamos o modelo devolvendo o valor
        mesmo assim para confirmar que a construção também recusa."""
        documento = documento_sintetico()
        cliente = cliente_fake([_bloco_relacao(validation_state="VALIDADA")])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_relacoes_afirmacao_evidencia(
                documento=documento, unit_ids=["UNI-PAR-0001"], cliente=cliente
            )

    def test_sem_unit_ids_levanta_erro_de_ponte_antes_de_chamar(self):
        documento = documento_sintetico()
        cliente = cliente_fake([])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_relacoes_afirmacao_evidencia(documento=documento, unit_ids=[], cliente=cliente)
        cliente.chamar.assert_not_called()


def amostras_sinteticas() -> list[AmostraAutoral]:
    return [
        AmostraAutoral(amostra_id="AM-1", texto="Texto da amostra 1.", provenance="[acervo:cap1]"),
        AmostraAutoral(amostra_id="AM-2", texto="Texto da amostra 2.", provenance="[acervo:cap2]"),
    ]


def _todas_as_dimensoes_com_evidencia(excluir: set | None = None) -> list[dict]:
    excluir = excluir or set()
    return [
        {
            "dimension_id": d.value,
            "valor": f"valor sintético para {d.value}",
            "evidencia": [{"amostra_id": "AM-1", "trecho": "trecho sintético"}],
            "confianca": "MEDIA",
        }
        for d in DimensaoDeVoz
        if d.value not in excluir
    ]


def bloco_derivacao_perfil(com_evidencia: list[dict], sem_evidencia: list[dict] | None = None) -> dict:
    return {
        "type": "tool_use",
        "name": ponte._FERRAMENTA_DERIVACAO_PERFIL,
        "input": {
            "dimensoes_com_evidencia": com_evidencia,
            "dimensoes_sem_evidencia_suficiente": sem_evidencia or [],
        },
    }


class TestGerarPerfilDeVozCandidato:
    def test_cobertura_completa_produz_perfilfedevoz_candidato(self):
        cliente = cliente_fake([bloco_derivacao_perfil(_todas_as_dimensoes_com_evidencia())])

        resultado = ponte.gerar_perfil_de_voz_candidato(
            amostras=amostras_sinteticas(),
            cliente=cliente,
            profile_id="PV-CAND-0001",
            purpose="preservar a voz do autor avaliado",
            scope={"documento": "cap5"},
        )

        assert isinstance(resultado, PerfilDeVoz)
        assert resultado.profile_type is TipoDePerfil.PERFIL_AUTORAL_DERIVADO_DE_AMOSTRAS
        assert resultado.status is StatusDePerfil.VALIDACAO_PENDENTE
        assert len(resultado.dimensions) == len(list(DimensaoDeVoz))
        assert resultado.confidence == ConfidenceVoz.MEDIA
        assert len(resultado.provenance) == 2

        _, kwargs = cliente.chamar.call_args
        assert kwargs["model"] == ponte.MODEL_ETAPA_13_DERIVACAO_PERFIL
        assert kwargs["tools"][0]["name"] == ponte._FERRAMENTA_DERIVACAO_PERFIL

    def test_menos_de_duas_amostras_nao_chama_modelo(self):
        cliente = cliente_fake([])

        resultado = ponte.gerar_perfil_de_voz_candidato(
            amostras=[amostras_sinteticas()[0]],
            cliente=cliente,
            profile_id="PV-CAND-0001",
            purpose="preservar a voz do autor avaliado",
            scope={"documento": "cap5"},
        )

        assert isinstance(resultado, SolicitacaoDeAmostrasAdicionais)
        assert resultado.amostras_recebidas == 1
        assert set(resultado.dimensoes_sem_evidencia) == DIMENSOES_OBRIGATORIAS
        cliente.chamar.assert_not_called()

    def test_dimensao_obrigatoria_sem_evidencia_produz_solicitacao_de_amostras(self):
        com_evidencia = _todas_as_dimensoes_com_evidencia(excluir={DimensaoDeVoz.VOZ_D01.value})
        sem_evidencia = [{"dimension_id": "VOZ-D01", "motivo": "amostras não trazem material suficiente"}]
        cliente = cliente_fake([bloco_derivacao_perfil(com_evidencia, sem_evidencia)])

        resultado = ponte.gerar_perfil_de_voz_candidato(
            amostras=amostras_sinteticas(),
            cliente=cliente,
            profile_id="PV-CAND-0001",
            purpose="preservar a voz do autor avaliado",
            scope={"documento": "cap5"},
        )

        assert isinstance(resultado, SolicitacaoDeAmostrasAdicionais)
        assert DimensaoDeVoz.VOZ_D01 in resultado.dimensoes_sem_evidencia
        assert "VOZ-D01" in resultado.motivos

    def test_dimensao_opcional_sem_evidencia_nao_bloqueia(self):
        com_evidencia = _todas_as_dimensoes_com_evidencia(excluir={DimensaoDeVoz.VOZ_D16.value})
        sem_evidencia = [{"dimension_id": "VOZ-D16", "motivo": "amostras não trazem preferências lexicais"}]
        cliente = cliente_fake([bloco_derivacao_perfil(com_evidencia, sem_evidencia)])

        resultado = ponte.gerar_perfil_de_voz_candidato(
            amostras=amostras_sinteticas(),
            cliente=cliente,
            profile_id="PV-CAND-0001",
            purpose="preservar a voz do autor avaliado",
            scope={"documento": "cap5"},
        )

        assert isinstance(resultado, PerfilDeVoz)
        assert "VOZ-D16" not in resultado.dimensions

    def test_dimensao_ausente_das_duas_listas_levanta_erro_de_ponte(self):
        com_evidencia = _todas_as_dimensoes_com_evidencia(excluir={DimensaoDeVoz.VOZ_D01.value})
        cliente = cliente_fake([bloco_derivacao_perfil(com_evidencia, [])])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_perfil_de_voz_candidato(
                amostras=amostras_sinteticas(),
                cliente=cliente,
                profile_id="PV-CAND-0001",
                purpose="preservar a voz do autor avaliado",
                scope={"documento": "cap5"},
            )

    def test_dimensao_duplicada_nas_duas_listas_levanta_erro_de_ponte(self):
        com_evidencia = _todas_as_dimensoes_com_evidencia()
        sem_evidencia = [{"dimension_id": "VOZ-D01", "motivo": "duplicado de propósito"}]
        cliente = cliente_fake([bloco_derivacao_perfil(com_evidencia, sem_evidencia)])

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_perfil_de_voz_candidato(
                amostras=amostras_sinteticas(),
                cliente=cliente,
                profile_id="PV-CAND-0001",
                purpose="preservar a voz do autor avaliado",
                scope={"documento": "cap5"},
            )

    def test_item_nao_objeto_levanta_erro_de_ponte(self):
        cliente = cliente_fake(
            [bloco_derivacao_perfil(["isto não é um objeto"], [])]
        )

        with pytest.raises(ponte.ErroDePonteModeloP13):
            ponte.gerar_perfil_de_voz_candidato(
                amostras=amostras_sinteticas(),
                cliente=cliente,
                profile_id="PV-CAND-0001",
                purpose="preservar a voz do autor avaliado",
                scope={"documento": "cap5"},
            )

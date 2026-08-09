"""Sessão 7 do plano P13 — auditoria final interna (§25, §44).

Testes TA13-17 (rastreabilidade), TA13-18 (reversibilidade), TA13-19
(envelopes P09) [§46], mais cobertura do checklist de 25 itens e da
proibição simétrica de §25 (zero comentários legítimo / silêncio diante de
risco material ilegítimo).
"""

import pytest

from escolio.comentarios.auditoria import (
    ItemChecklist,
    LoteDeAuditoria,
    VeredictoChecklist,
    VeredictoFinal,
    VerificacaoEnvelope,
    auditar_lote,
    verifica_consistencia_envelope_p09,
)
from escolio.comentarios.criticidade import ClasseCriticidade
from escolio.comentarios.erros import ErroDeComentario
from escolio.comentarios.seletividade import SelectionDecision
from escolio.comentarios.tipos import CommentType
from escolio.comentarios.vocabulario import P13CommentResolution, P13CommentStatus
from escolio.contrato.payloads import AbstentionPayload
from escolio.contrato.vocabulario import AbstentionCategory, ResponseStatus
from escolio.intervencao.niveis import NivelIntervencao
from tests.comentarios.fixtures import (
    comentario_base,
    matriz_criticidade_base,
    matriz_seletividade_base,
)


class TestChecklistCompletude:
    """RelatorioAuditoriaFinal exige exatamente os 25 itens de §44, nesta ordem."""

    def test_lote_vazio_produz_25_itens_na_ordem_de_44(self):
        relatorio = auditar_lote(LoteDeAuditoria(comentarios=[]), lote_id="LOTE-VAZIO")
        assert [r.item for r in relatorio.resultados] == list(ItemChecklist)
        assert len(relatorio.resultados) == 25

    def test_item_15_privacidade_e_sempre_na_explicito(self):
        relatorio = auditar_lote(LoteDeAuditoria(comentarios=[]), lote_id="LOTE-VAZIO")
        resultado = relatorio.resultado_do_item(ItemChecklist.PRIVACIDADE_P08)
        assert resultado.veredito == VeredictoChecklist.NAO_APLICAVEL

    def test_relatorio_rejeita_item_faltante_ou_duplicado(self):
        relatorio_ok = auditar_lote(LoteDeAuditoria(comentarios=[]), lote_id="LOTE-1")
        resultados_incompletos = relatorio_ok.resultados[:-1]
        with pytest.raises(ErroDeComentario):
            from escolio.comentarios.auditoria import RelatorioAuditoriaFinal

            RelatorioAuditoriaFinal(lote_id="LOTE-1", resultados=resultados_incompletos)

    def test_lote_totalmente_vazio_e_indeterminado_nao_aprovado_silenciosamente(self):
        """Itens sem dado suficiente viram NAO_VERIFICAVEL_NESTA_SESSAO, não
        aprovação silenciosa — 'indeterminado em vez de chute' [CLAUDE.md §11]."""
        relatorio = auditar_lote(LoteDeAuditoria(comentarios=[]), lote_id="LOTE-VAZIO")
        assert relatorio.veredicto_final == VeredictoFinal.AUDITORIA_INDETERMINADA


class TestTA13_17_Rastreabilidade:
    """[§46] Comentário sem unidade ou hash deve impedir consolidação."""

    def test_comentario_completo_aprova_ancoragem_e_rastreabilidade(self):
        lote = LoteDeAuditoria(comentarios=[comentario_base()])
        relatorio = auditar_lote(lote, lote_id="LOTE-OK")
        assert relatorio.resultado_do_item(ItemChecklist.ANCORAGEM).veredito == VeredictoChecklist.APROVADO
        assert relatorio.resultado_do_item(ItemChecklist.RASTREABILIDADE).veredito == VeredictoChecklist.APROVADO

    def test_comentario_sem_unidade_reprova_rastreabilidade(self):
        comentario = comentario_base()
        comentario.unit_id = ""  # simula registro corrompido após a construção válida
        lote = LoteDeAuditoria(comentarios=[comentario])
        relatorio = auditar_lote(lote, lote_id="LOTE-ORFAO")
        resultado = relatorio.resultado_do_item(ItemChecklist.RASTREABILIDADE)
        assert resultado.veredito == VeredictoChecklist.REPROVADO
        assert comentario.comment_id in resultado.justificativa

    def test_comentario_sem_hash_reprova_ancoragem(self):
        comentario = comentario_base()
        comentario.anchor_text_hash = ""
        lote = LoteDeAuditoria(comentarios=[comentario])
        relatorio = auditar_lote(lote, lote_id="LOTE-SEM-HASH")
        resultado = relatorio.resultado_do_item(ItemChecklist.ANCORAGEM)
        assert resultado.veredito == VeredictoChecklist.REPROVADO
        assert comentario.comment_id in resultado.justificativa
        # Rastreabilidade não avalia hash — permanece aprovada isoladamente.
        assert relatorio.resultado_do_item(ItemChecklist.RASTREABILIDADE).veredito == VeredictoChecklist.APROVADO


class TestTA13_18_Reversibilidade:
    """[§46] Comentário aceito ou recusado deve preservar histórico e
    original; apagamento da proveniência reprova o item."""

    def test_resolucao_presente_em_status_terminal_aprova(self):
        comentario = comentario_base(status=P13CommentStatus.RESOLVED, resolution=P13CommentResolution.ACEITO)
        lote = LoteDeAuditoria(comentarios=[comentario])
        relatorio = auditar_lote(lote, lote_id="LOTE-RESOLVIDO")
        assert relatorio.resultado_do_item(ItemChecklist.REVERSIBILIDADE).veredito == VeredictoChecklist.APROVADO

    def test_resolucao_apagada_apos_status_terminal_reprova(self):
        comentario = comentario_base(status=P13CommentStatus.RESOLVED, resolution=P13CommentResolution.ACEITO)
        comentario.resolution = None  # simula apagamento de proveniência após a construção válida
        lote = LoteDeAuditoria(comentarios=[comentario])
        relatorio = auditar_lote(lote, lote_id="LOTE-APAGADO")
        resultado = relatorio.resultado_do_item(ItemChecklist.REVERSIBILIDADE)
        assert resultado.veredito == VeredictoChecklist.REPROVADO
        assert comentario.comment_id in resultado.justificativa

    def test_acao_irreversivel_sem_gate_nomeado_reprova(self):
        comentario = comentario_base(reversible=False, gate="NENHUM")
        lote = LoteDeAuditoria(comentarios=[comentario])
        relatorio = auditar_lote(lote, lote_id="LOTE-IRREVERSIVEL")
        resultado = relatorio.resultado_do_item(ItemChecklist.REVERSIBILIDADE)
        assert resultado.veredito == VeredictoChecklist.REPROVADO

    def test_acao_irreversivel_com_gate_nomeado_nao_reprova_por_este_motivo(self):
        comentario = comentario_base(reversible=False, gate="GATE_DE_ALTERACAO_DE_CONCLUSAO")
        lote = LoteDeAuditoria(comentarios=[comentario])
        relatorio = auditar_lote(lote, lote_id="LOTE-IRREVERSIVEL-COM-GATE")
        resultado = relatorio.resultado_do_item(ItemChecklist.REVERSIBILIDADE)
        assert resultado.veredito == VeredictoChecklist.APROVADO


class TestTA13_19_EnvelopesP09:
    """[§46] status/payload: ABSTAINED com safe_result.available=true deve
    ser resposta inválida; trabalho seguro nos campos do AbstentionPayload,
    nunca payload concorrente."""

    def _abstention_valida(self):
        return AbstentionPayload(
            abstention_id="ABST-01",
            request_id="AUD-ENVELOPE-CHECK",
            category=AbstentionCategory.INSUFFICIENT_EVIDENCE,
            reason="Página não confirmada.",
        )

    def test_abstained_com_safe_result_available_e_invalido(self):
        verificacao = VerificacaoEnvelope(
            status=ResponseStatus.ABSTAINED, safe_result_available=True, abstention=self._abstention_valida()
        )
        assert verifica_consistencia_envelope_p09(verificacao) is False

    def test_abstained_com_safe_result_indisponivel_e_valido(self):
        verificacao = VerificacaoEnvelope(
            status=ResponseStatus.ABSTAINED, safe_result_available=False, abstention=self._abstention_valida()
        )
        assert verifica_consistencia_envelope_p09(verificacao) is True

    def test_item_envelopes_reprova_lote_com_envelope_inconsistente(self):
        lote = LoteDeAuditoria(
            comentarios=[],
            verificacoes_envelope=[
                VerificacaoEnvelope(
                    status=ResponseStatus.ABSTAINED, safe_result_available=True, abstention=self._abstention_valida()
                )
            ],
        )
        relatorio = auditar_lote(lote, lote_id="LOTE-ENVELOPE-RUIM")
        resultado = relatorio.resultado_do_item(ItemChecklist.ENVELOPES_P09)
        assert resultado.veredito == VeredictoChecklist.REPROVADO
        assert "0" in resultado.justificativa

    def test_item_envelopes_aprova_lote_com_envelope_consistente(self):
        lote = LoteDeAuditoria(
            comentarios=[],
            verificacoes_envelope=[
                VerificacaoEnvelope(
                    status=ResponseStatus.ABSTAINED, safe_result_available=False, abstention=self._abstention_valida()
                )
            ],
        )
        relatorio = auditar_lote(lote, lote_id="LOTE-ENVELOPE-BOM")
        assert relatorio.resultado_do_item(ItemChecklist.ENVELOPES_P09).veredito == VeredictoChecklist.APROVADO

    def test_sem_envelope_informado_e_nao_verificavel(self):
        relatorio = auditar_lote(LoteDeAuditoria(comentarios=[]), lote_id="LOTE-SEM-ENVELOPE")
        resultado = relatorio.resultado_do_item(ItemChecklist.ENVELOPES_P09)
        assert resultado.veredito == VeredictoChecklist.NAO_VERIFICAVEL_NESTA_SESSAO


class TestProibicaoSimetricaDeDensidade:
    """[§25] "zero comentários" é legítimo; "silêncio diante de risco
    material" é ilegítimo — as duas pontas verificadas separadamente."""

    def test_zero_comentarios_com_decisoes_consistentes_e_legitimo(self):
        matriz_criticidade = matriz_criticidade_base(classe=ClasseCriticidade.SEM_CRITICIDADE_MATERIAL)
        matriz_selecao = matriz_seletividade_base(
            criticality=ClasseCriticidade.SEM_CRITICIDADE_MATERIAL,
            selection_decision=SelectionDecision.NAO_COMENTAR_SEM_PROBLEMA_MATERIAL,
        )
        lote = LoteDeAuditoria(
            comentarios=[], matrizes_criticidade=[matriz_criticidade], matrizes_seletividade=[matriz_selecao]
        )
        relatorio = auditar_lote(lote, lote_id="LOTE-ZERO-LEGITIMO")
        assert relatorio.resultado_do_item(ItemChecklist.AUSENCIA_LEGITIMA_DE_COMENTARIOS).veredito == (
            VeredictoChecklist.APROVADO
        )
        assert relatorio.resultado_do_item(ItemChecklist.PROBLEMAS_MATERIAIS_NAO_SILENCIADOS).veredito == (
            VeredictoChecklist.APROVADO
        )

    def test_silencio_diante_de_risco_material_e_ilegitimo(self):
        matriz_criticidade = matriz_criticidade_base(classe=ClasseCriticidade.CRITICIDADE_ALTA)
        matriz_selecao = matriz_seletividade_base(
            criticality=ClasseCriticidade.CRITICIDADE_ALTA,
            selection_decision=SelectionDecision.NAO_COMENTAR_SEM_PROBLEMA_MATERIAL,
        )
        lote = LoteDeAuditoria(
            comentarios=[], matrizes_criticidade=[matriz_criticidade], matrizes_seletividade=[matriz_selecao]
        )
        relatorio = auditar_lote(lote, lote_id="LOTE-SILENCIO-ILEGITIMO")
        resultado = relatorio.resultado_do_item(ItemChecklist.PROBLEMAS_MATERIAIS_NAO_SILENCIADOS)
        assert resultado.veredito == VeredictoChecklist.REPROVADO
        # A contradição também derruba a densidade justificada [§25].
        assert relatorio.resultado_do_item(ItemChecklist.DENSIDADE_JUSTIFICADA).veredito == VeredictoChecklist.REPROVADO

    def test_quota_declarada_reprova_quota_e_densidade(self):
        lote = LoteDeAuditoria(comentarios=[], quota_declarada=True)
        relatorio = auditar_lote(lote, lote_id="LOTE-QUOTA")
        assert relatorio.resultado_do_item(ItemChecklist.AUSENCIA_DE_QUOTA).veredito == VeredictoChecklist.REPROVADO
        assert relatorio.resultado_do_item(ItemChecklist.DENSIDADE_JUSTIFICADA).veredito == VeredictoChecklist.REPROVADO


class TestItensDependentesDeComentario:
    def test_comentario_matriz_bem_formado_aprova_matriz_e_remissoes(self):
        matriz = comentario_base(comment_id="CMT-MATRIZ-AUD", comment_type=CommentType.COMENTARIO_MATRIZ.value)
        remissao = comentario_base(
            comment_id="CMT-REM-AUD",
            unit_id="UNIT-02",
            comment_type=CommentType.REMISSAO_A_COMENTARIO_MATRIZ.value,
            matrix_comment_id="CMT-MATRIZ-AUD",
        )
        lote = LoteDeAuditoria(comentarios=[matriz, remissao])
        relatorio = auditar_lote(lote, lote_id="LOTE-MATRIZ")
        assert relatorio.resultado_do_item(ItemChecklist.COMENTARIOS_MATRIZ).veredito == VeredictoChecklist.APROVADO
        assert relatorio.resultado_do_item(ItemChecklist.REMISSOES).veredito == VeredictoChecklist.APROVADO

    def test_remissao_orfa_reprova_remissoes(self):
        remissao_orfa = comentario_base(
            comment_id="CMT-REM-ORFA",
            comment_type=CommentType.REMISSAO_A_COMENTARIO_MATRIZ.value,
            matrix_comment_id="CMT-MATRIZ-INEXISTENTE",
        )
        lote = LoteDeAuditoria(comentarios=[remissao_orfa])
        relatorio = auditar_lote(lote, lote_id="LOTE-REMISSAO-ORFA")
        assert relatorio.resultado_do_item(ItemChecklist.REMISSOES).veredito == VeredictoChecklist.REPROVADO

    def test_priority_sem_prioridade_reprova_relevancia(self):
        comentario = comentario_base(priority="SEM_PRIORIDADE_DE_COMENTARIO")
        lote = LoteDeAuditoria(comentarios=[comentario])
        relatorio = auditar_lote(lote, lote_id="LOTE-SEM-PRIORIDADE")
        assert relatorio.resultado_do_item(ItemChecklist.RELEVANCIA).veredito == VeredictoChecklist.REPROVADO

    def test_status_inserted_reprova_ausencia_de_implementacao_word(self):
        comentario = comentario_base(status=P13CommentStatus.INSERTED)
        lote = LoteDeAuditoria(comentarios=[comentario])
        relatorio = auditar_lote(lote, lote_id="LOTE-INSERIDO")
        resultado = relatorio.resultado_do_item(ItemChecklist.AUSENCIA_DE_IMPLEMENTACAO_WORD)
        assert resultado.veredito == VeredictoChecklist.REPROVADO

    def test_intervention_level_reescrita_reprova_nivel_e_ausencia_de_reescrita(self):
        comentario = comentario_base(intervention_level=NivelIntervencao.REESCRITA.value)
        lote = LoteDeAuditoria(comentarios=[comentario])
        relatorio = auditar_lote(lote, lote_id="LOTE-REESCRITA")
        assert relatorio.resultado_do_item(ItemChecklist.NIVEL_P06).veredito == VeredictoChecklist.REPROVADO
        assert (
            relatorio.resultado_do_item(ItemChecklist.AUSENCIA_DE_REESCRITA_SUBSTITUTIVA).veredito
            == VeredictoChecklist.REPROVADO
        )

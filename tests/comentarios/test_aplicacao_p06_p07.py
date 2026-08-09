"""Sessão 5 do plano P13 — integração P06 (níveis de intervenção)/P07
(voz autoral) no comentário.

Testes PS13-07, PS13-08 [§45] e TA13-12, TA13-20 [§46], mais cobertura de
regra de §4.4/§4.5/§28/§29/§32 que os quatro cenários narrativos exercitam.
"""

import pytest

from escolio.comentarios.aplicacao_p06_p07 import (
    AplicacaoP06P07DoComentario,
    GateCatalogoP13,
    NIVEIS_PERMITIDOS_P13,
    aplicar_intervencao_e_voz,
    perfil_insuficiente,
    valida_alerta_de_voz_quando_bloqueado,
    valida_correcao_local_nao_autoriza_reescrita_forte,
    valida_gate,
    valida_gate_humano_tem_gate_nomeado,
    valida_intervention_level_permitido,
    valida_voice_impact_registrado,
)
from escolio.comentarios.erros import ErroDeComentario
from escolio.comentarios.tipos import CommentType
from escolio.intervencao.niveis import NivelIntervencao
from escolio.voz.fidelidade import avaliar
from escolio.voz.vocabulario import (
    Confidence,
    DesvioBloqueante,
    ResultadoDeFidelidade,
    StatusDePerfil,
    TipoDePerfil,
)
from escolio.voz.perfil import PerfilDeVoz
from tests.comentarios.fixtures import comentario_base

NI = NivelIntervencao


def avaliacao_conforme():
    return avaliar(
        desvios_encontrados=[],
        amostra_unica=False,
        amostras_conflitantes=False,
        proveniencia_ausente=False,
        autorizacao_ausente=False,
        perfil_declarado_sem_amostras=False,
        exigencia_institucional_em_conflito=False,
    )


def avaliacao_bloqueada(desvio: DesvioBloqueante):
    return avaliar(
        desvios_encontrados=[desvio],
        amostra_unica=False,
        amostras_conflitantes=False,
        proveniencia_ausente=False,
        autorizacao_ausente=False,
        perfil_declarado_sem_amostras=False,
        exigencia_institucional_em_conflito=False,
        justificativa="reescrita substitutiva identificada",
    )


class TestValidaInterventionLevelPermitido:
    """§4.4 — o comentário só pode exercer os cinco níveis nomeados como
    "pode"; os demais, nomeados ou não em "não pode", são recusados."""

    @pytest.mark.parametrize(
        "nivel",
        [NI.OBSERVACAO, NI.DIAGNOSTICO, NI.SINALIZACAO, NI.RECOMENDACAO, NI.PROPOSTA],
    )
    def test_niveis_permitidos_nao_levantam(self, nivel):
        valida_intervention_level_permitido(nivel)
        assert nivel in NIVEIS_PERMITIDOS_P13

    @pytest.mark.parametrize(
        "nivel",
        [
            NI.SIMULACAO,
            NI.EDICAO_LOCAL,
            NI.REESCRITA,
            NI.REORGANIZACAO,
            NI.FUSAO,
            NI.CORTE,
            NI.SUBSTITUICAO,
            NI.VALIDACAO,
            NI.HOMOLOGACAO,
            NI.ABSTENCAO,
        ],
    )
    def test_niveis_fora_da_lista_pode_sao_recusados(self, nivel):
        with pytest.raises(ErroDeComentario):
            valida_intervention_level_permitido(nivel)

    def test_valor_invalido_rejeitado(self):
        with pytest.raises(ErroDeComentario):
            valida_intervention_level_permitido("INT-04")


class TestGateCatalogoP13:
    """§32 — 17 gates nomeados mais NENHUM [§45]."""

    def test_gate_valido_nao_levanta(self):
        valida_gate(GateCatalogoP13.GATE_DE_ALTERACAO_DE_CONCLUSAO)
        valida_gate(GateCatalogoP13.NENHUM)

    def test_gate_invalido_rejeitado(self):
        with pytest.raises(ErroDeComentario):
            valida_gate("GATE_INVENTADO")

    def test_correcao_local_nao_autoriza_reescrita_forte(self):
        with pytest.raises(ErroDeComentario):
            valida_correcao_local_nao_autoriza_reescrita_forte(
                CommentType.CORRECAO_LOCAL.value, GateCatalogoP13.GATE_DE_REESCRITA_FORTE
            )

    def test_correcao_local_com_outro_gate_e_aceito(self):
        valida_correcao_local_nao_autoriza_reescrita_forte(
            CommentType.CORRECAO_LOCAL.value, GateCatalogoP13.NENHUM
        )

    def test_gate_humano_exige_gate_nomeado(self):
        with pytest.raises(ErroDeComentario):
            valida_gate_humano_tem_gate_nomeado(CommentType.GATE_HUMANO.value, GateCatalogoP13.NENHUM)
        valida_gate_humano_tem_gate_nomeado(
            CommentType.GATE_HUMANO.value, GateCatalogoP13.GATE_DE_ALTERACAO_DE_CONCLUSAO
        )


class TestVoiceImpact:
    """§4.5, §29 — voice_impact reusa ResultadoDeFidelidade (P07)."""

    def test_resultado_valido_nao_levanta(self):
        valida_voice_impact_registrado(ResultadoDeFidelidade.CONFORME)

    def test_valor_invalido_rejeitado(self):
        with pytest.raises(ErroDeComentario):
            valida_voice_impact_registrado("CONFORME")

    def test_bloqueio_exige_alerta_de_voz(self):
        with pytest.raises(ErroDeComentario):
            valida_alerta_de_voz_quando_bloqueado(
                CommentType.DIAGNOSTICO.value, ResultadoDeFidelidade.BLOQUEAR
            )
        valida_alerta_de_voz_quando_bloqueado(
            CommentType.ALERTA_DE_VOZ.value, ResultadoDeFidelidade.BLOQUEAR
        )

    def test_conforme_nao_exige_alerta_de_voz(self):
        valida_alerta_de_voz_quando_bloqueado(CommentType.DIAGNOSTICO.value, ResultadoDeFidelidade.CONFORME)


class TestPerfilInsuficiente:
    """§29 — "quando o perfil for insuficiente"."""

    def test_perfil_abstencao_e_insuficiente(self):
        perfil = PerfilDeVoz(
            profile_id="PERF-0001",
            profile_type=TipoDePerfil.PERFIL_INSUFICIENTE_OU_CONFLITANTE,
            purpose="Preservar voz do autor avaliado.",
            scope={"secao": "todas"},
            dimensions={},
            evidence=[],
            confidence=Confidence.BAIXA,
            authorization={},
            versioning={},
            provenance=[],
            reversibility={},
            status=StatusDePerfil.ABSTENCAO,
            abstention_reason="amostra única, insuficiente para perfil derivado",
        )
        assert perfil_insuficiente(perfil) is True

    def test_perfil_homologado_nao_e_insuficiente(self):
        perfil = PerfilDeVoz(
            profile_id="PERF-0002",
            profile_type=TipoDePerfil.PERFIL_NEUTRO_ACADEMICO_CONTROLADO,
            purpose="Preservar voz do autor avaliado.",
            scope={"secao": "todas"},
            dimensions={},
            evidence=[],
            confidence=Confidence.ALTA,
            authorization={},
            versioning={},
            provenance=[],
            reversibility={},
            status=StatusDePerfil.HOMOLOGADO,
        )
        assert perfil_insuficiente(perfil) is False


class TestAplicarIntervencaoEVoz:
    """Adaptador de sessão 5: popula intervention_level/gate/voice_impact
    preservando os demais campos; nada é gravado se alguma validação
    falhar."""

    def test_atualiza_campos_preservando_demais(self):
        comentario = comentario_base(comment_type=CommentType.DIAGNOSTICO.value)
        atualizado, aplicacao = aplicar_intervencao_e_voz(
            comentario,
            intervention_level=NI.SINALIZACAO,
            gate=GateCatalogoP13.NENHUM,
            avaliacao_de_voz=avaliacao_conforme(),
        )
        assert atualizado.intervention_level == NI.SINALIZACAO.value
        assert atualizado.gate == GateCatalogoP13.NENHUM.value
        assert atualizado.voice_impact == ResultadoDeFidelidade.CONFORME.value
        assert atualizado.comment_id == comentario.comment_id
        assert isinstance(aplicacao, AplicacaoP06P07DoComentario)

    def test_nao_grava_quando_nivel_excede_permitido(self):
        comentario = comentario_base(comment_type=CommentType.DIAGNOSTICO.value)
        with pytest.raises(ErroDeComentario):
            aplicar_intervencao_e_voz(
                comentario,
                intervention_level=NI.SUBSTITUICAO,
                gate=GateCatalogoP13.NENHUM,
                avaliacao_de_voz=avaliacao_conforme(),
            )
        assert comentario.intervention_level != NI.SUBSTITUICAO.value


class TestPS13_07_ComentarioSugereReescritaForteDeConclusao:
    """[§45] Comentário indica GATE_DE_ALTERACAO_DE_CONCLUSAO; a alteração
    em si não é aplicada por este módulo — não existe caminho de código
    aqui que produza a mudança de conclusão."""

    def test_gate_humano_indica_gate_sem_aplicar_alteracao(self):
        comentario = comentario_base(comment_type=CommentType.GATE_HUMANO.value)
        atualizado, aplicacao = aplicar_intervencao_e_voz(
            comentario,
            intervention_level=NI.SINALIZACAO,
            gate=GateCatalogoP13.GATE_DE_ALTERACAO_DE_CONCLUSAO,
            avaliacao_de_voz=avaliacao_conforme(),
        )
        assert atualizado.gate == GateCatalogoP13.GATE_DE_ALTERACAO_DE_CONCLUSAO.value
        assert aplicacao.intervention_level in NIVEIS_PERMITIDOS_P13

    def test_gate_humano_sem_gate_nomeado_e_rejeitado(self):
        comentario = comentario_base(comment_type=CommentType.GATE_HUMANO.value)
        with pytest.raises(ErroDeComentario):
            aplicar_intervencao_e_voz(
                comentario,
                intervention_level=NI.SINALIZACAO,
                gate=GateCatalogoP13.NENHUM,
                avaliacao_de_voz=avaliacao_conforme(),
            )


class TestPS13_08_SugestaoApagaVoz:
    """[§45] Sugestão melhora fluidez, mas apaga voz — produz
    ALERTA_DE_VOZ, nunca a reescrita substitutiva em si."""

    def test_alerta_de_voz_e_aceito(self):
        comentario = comentario_base(comment_type=CommentType.ALERTA_DE_VOZ.value)
        atualizado, aplicacao = aplicar_intervencao_e_voz(
            comentario,
            intervention_level=NI.RECOMENDACAO,
            gate=GateCatalogoP13.GATE_DE_REESCRITA_FORTE,
            avaliacao_de_voz=avaliacao_bloqueada(DesvioBloqueante.ALTERACAO_FORTE_SEM_GATE),
        )
        assert atualizado.voice_impact == ResultadoDeFidelidade.BLOQUEAR.value

    def test_reescrita_substitutiva_como_diagnostico_e_rejeitada(self):
        comentario = comentario_base(comment_type=CommentType.DIAGNOSTICO.value)
        with pytest.raises(ErroDeComentario):
            aplicar_intervencao_e_voz(
                comentario,
                intervention_level=NI.RECOMENDACAO,
                gate=GateCatalogoP13.GATE_DE_REESCRITA_FORTE,
                avaliacao_de_voz=avaliacao_bloqueada(DesvioBloqueante.ALTERACAO_FORTE_SEM_GATE),
            )


class TestTA13_12_Voz:
    """[§46] Objeto: preservação autoral. Entrada: reescrita substitutiva.
    Resultado esperado: recusa e alerta de voz. Critério de falha:
    comentário escrito como versão final do orientador."""

    def test_reescrita_substitutiva_produz_alerta_de_voz(self):
        comentario = comentario_base(comment_type=CommentType.ALERTA_DE_VOZ.value)
        atualizado, _ = aplicar_intervencao_e_voz(
            comentario,
            intervention_level=NI.SINALIZACAO,
            gate=GateCatalogoP13.NENHUM,
            avaliacao_de_voz=avaliacao_bloqueada(DesvioBloqueante.COPIA_OU_IMITACAO),
        )
        assert atualizado.voice_impact == ResultadoDeFidelidade.BLOQUEAR.value
        assert atualizado.comment_type == CommentType.ALERTA_DE_VOZ.value

    def test_versao_final_do_orientador_como_correcao_local_e_recusada(self):
        # "Comentário escrito como versão final do orientador" é
        # exatamente o critério de falha — aqui modelado como tentativa de
        # gravar o bloqueio sob um comment_type que não é ALERTA_DE_VOZ.
        comentario = comentario_base(comment_type=CommentType.CORRECAO_LOCAL.value)
        with pytest.raises(ErroDeComentario):
            aplicar_intervencao_e_voz(
                comentario,
                intervention_level=NI.SINALIZACAO,
                gate=GateCatalogoP13.NENHUM,
                avaliacao_de_voz=avaliacao_bloqueada(DesvioBloqueante.COPIA_OU_IMITACAO),
            )


class TestTA13_20_SoberaniaHumana:
    """[§46] Objeto: comentário com alteração forte. Entrada: sugestão de
    mudar conclusão. Resultado esperado: gate humano sem execução.
    Critério de falha: decisão executada autonomamente."""

    def test_mudanca_de_conclusao_fica_em_gate_humano_sem_executar(self):
        comentario = comentario_base(comment_type=CommentType.GATE_HUMANO.value)
        atualizado, _ = aplicar_intervencao_e_voz(
            comentario,
            intervention_level=NI.RECOMENDACAO,
            gate=GateCatalogoP13.GATE_DE_ALTERACAO_DE_CONCLUSAO,
            avaliacao_de_voz=avaliacao_conforme(),
        )
        # O texto original não é alterado: nenhum campo de conteúdo do
        # documento é tocado por este adaptador, só os quatro campos de
        # controle do comentário.
        assert atualizado.gate == GateCatalogoP13.GATE_DE_ALTERACAO_DE_CONCLUSAO.value

    def test_execucao_autonoma_da_mudanca_nao_tem_caminho_de_codigo(self):
        # "Decisão executada autonomamente" exigiria um nível de execução
        # (SUBSTITUICAO, por exemplo) — recusado por
        # valida_intervention_level_permitido, nunca alcançável a partir
        # deste módulo.
        comentario = comentario_base(comment_type=CommentType.GATE_HUMANO.value)
        with pytest.raises(ErroDeComentario):
            aplicar_intervencao_e_voz(
                comentario,
                intervention_level=NI.SUBSTITUICAO,
                gate=GateCatalogoP13.GATE_DE_ALTERACAO_DE_CONCLUSAO,
                avaliacao_de_voz=avaliacao_conforme(),
            )

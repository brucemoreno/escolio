import pytest

from escolio.comentarios.erros import ErroDeComentario
from escolio.comentarios.tipos import (
    AcaoMetodologica,
    CommentType,
    CondicaoMetodologica,
    TemplateAlertaArgumentativo,
    TemplateAlertaEstrutural,
    TemplateAlertaMetodologico,
    TemplateComentarioLinguistico,
    valida_template_por_tipo,
)


def test_catalogo_tem_os_15_tipos():
    assert len(list(CommentType)) == 15


def test_comentario_matriz_reusa_literal_de_vocabulario():
    from escolio.comentarios.vocabulario import (
        COMMENT_TYPE_COMENTARIO_MATRIZ,
        COMMENT_TYPE_REMISSAO_A_COMENTARIO_MATRIZ,
    )

    assert CommentType.COMENTARIO_MATRIZ.value == COMMENT_TYPE_COMENTARIO_MATRIZ
    assert CommentType.REMISSAO_A_COMENTARIO_MATRIZ.value == COMMENT_TYPE_REMISSAO_A_COMENTARIO_MATRIZ


# --- TA13-06 — Comentário linguístico ---------------------------------


def test_ta13_06_ambiguidade_material_e_aceita():
    t = TemplateComentarioLinguistico(
        problem="A construção permite duas leituras incompatíveis.",
        evidence="O pronome pode retomar dois sujeitos anteriores.",
        impact="Não é possível determinar quem executou a ação descrita.",
        recommended_action="Explicitar o sujeito sem alterar o conteúdo factual.",
        efeito="AMBIGUIDADE_MATERIAL",
    )
    assert t.efeito == "AMBIGUIDADE_MATERIAL"


def test_ta13_06_preferencia_estilistica_generica_rejeita():
    with pytest.raises(ErroDeComentario):
        TemplateComentarioLinguistico(
            problem="Troca de sinônimo.",
            evidence="Palavra repetida no parágrafo.",
            impact="Nenhum.",
            recommended_action="Trocar por sinônimo.",
            efeito="PREFERENCIA_ESTILISTICA",
        )


def test_ta13_06_efeito_nao_reconhecido_rejeita():
    with pytest.raises(ErroDeComentario):
        TemplateComentarioLinguistico(
            problem="p", evidence="e", impact="i", recommended_action="a",
            efeito="EFEITO_INVENTADO",
        )


def test_ta13_06_campo_vazio_rejeita():
    with pytest.raises(ErroDeComentario):
        TemplateComentarioLinguistico(
            problem="", evidence="e", impact="i", recommended_action="a",
            efeito="SENTIDO",
        )


# --- TA13-07 — Comentário estrutural -----------------------------------


def _estrutural_base(**overrides):
    campos = dict(
        funcao_esperada="Transição entre método e resultados.",
        posicao_atual="Seção aparece antes da introdução do problema.",
        impacto="Compromete a progressão argumentativa.",
        alternativa_possivel="Mover a seção para depois da metodologia.",
        nivel_de_intervencao="INT-04",
        gate_aplicavel="GATE_DE_REESCRITA_FORTE",
    )
    campos.update(overrides)
    return TemplateAlertaEstrutural(**campos)


def test_ta13_07_diagnostica_sem_realocar():
    t = _estrutural_base()
    assert t.realocacao_executada is False


def test_ta13_07_realocacao_executada_rejeita():
    with pytest.raises(ErroDeComentario):
        _estrutural_base(realocacao_executada=True)


def test_ta13_07_campo_vazio_rejeita():
    with pytest.raises(ErroDeComentario):
        _estrutural_base(posicao_atual="")


# --- TA13-08 — Comentário argumentativo --------------------------------


def _argumentativo_base(**overrides):
    campos = dict(
        afirmacao="A hipótese é confirmada pelos dados coletados.",
        evidencia="Os dados cobrem apenas um subconjunto do período estudado.",
        inferencia="A conclusão generaliza além do subconjunto observado.",
        limitacao="Amostra não representa o período integral.",
        impacto="Conclusão pode não se sustentar para o período total.",
        acao_possivel="Restringir a conclusão ao período efetivamente coberto.",
    )
    campos.update(overrides)
    return TemplateAlertaArgumentativo(**campos)


def test_ta13_08_grau_de_certeza_problematizado():
    t = _argumentativo_base()
    assert t.solucao_factual_inventada is False


def test_ta13_08_solucao_factual_inventada_rejeita():
    with pytest.raises(ErroDeComentario):
        _argumentativo_base(solucao_factual_inventada=True)


def test_ta13_08_campo_vazio_rejeita():
    with pytest.raises(ErroDeComentario):
        _argumentativo_base(limitacao="")


# --- TA13-09 — Comentário metodológico ----------------------------------


def test_ta13_09_pede_decisao_ou_explicitacao():
    t = TemplateAlertaMetodologico(
        condicao=CondicaoMetodologica.PROCEDIMENTO_INCOMPATIVEL_COM_OBJETIVO,
        acao=AcaoMetodologica.SOLICITAR_EXPLICITACAO,
    )
    assert t.metodo_substitutivo_proposto is None


def test_ta13_09_metodo_substitutivo_inventado_rejeita():
    with pytest.raises(ErroDeComentario):
        TemplateAlertaMetodologico(
            condicao=CondicaoMetodologica.METODO_NAO_EXPLICITADO,
            acao=AcaoMetodologica.DECISAO_NECESSARIA,
            metodo_substitutivo_proposto="Usar análise de conteúdo em vez do método descrito.",
        )


def test_ta13_09_condicao_fora_do_enum_rejeita():
    with pytest.raises(ErroDeComentario):
        TemplateAlertaMetodologico(
            condicao="CONDICAO_INVENTADA", acao=AcaoMetodologica.DECISAO_NECESSARIA
        )


# --- Validador por comment_type -----------------------------------------


def test_valida_template_por_tipo_aceita_par_correto():
    valida_template_por_tipo(CommentType.ALERTA_ESTRUTURAL, _estrutural_base())
    valida_template_por_tipo(CommentType.ALERTA_ARGUMENTATIVO, _argumentativo_base())
    valida_template_por_tipo(
        CommentType.ALERTA_METODOLOGICO,
        TemplateAlertaMetodologico(
            condicao=CondicaoMetodologica.INFERENCIA_EXCEDE_A_OPERACAO,
            acao=AcaoMetodologica.DECISAO_NECESSARIA,
        ),
    )


def test_valida_template_por_tipo_rejeita_par_trocado():
    with pytest.raises(ErroDeComentario):
        valida_template_por_tipo(CommentType.ALERTA_ESTRUTURAL, _argumentativo_base())


def test_valida_template_por_tipo_sem_template_nesta_sessao():
    with pytest.raises(ErroDeComentario):
        valida_template_por_tipo(CommentType.DIAGNOSTICO, _estrutural_base())


def test_valida_template_por_tipo_comment_type_invalido():
    with pytest.raises(ErroDeComentario):
        valida_template_por_tipo("ALERTA_ESTRUTURAL", _estrutural_base())

import pytest

from escolio.comentarios.criticidade import ClasseCriticidade, EixoCriticidade
from escolio.comentarios.erros import ErroDeComentario
from tests.comentarios.fixtures import matriz_criticidade_base


def test_matriz_valida_com_12_eixos():
    m = matriz_criticidade_base()
    assert len(m.avaliacao_por_eixo) == 12
    assert m.classe == ClasseCriticidade.CRITICIDADE_MEDIA


def test_eixo_faltante_rejeita():
    avaliacao = matriz_criticidade_base().avaliacao_por_eixo.copy()
    del avaliacao[EixoCriticidade.PRIVACIDADE]
    with pytest.raises(ErroDeComentario):
        matriz_criticidade_base(avaliacao_por_eixo=avaliacao)


def test_eixo_desconhecido_rejeita():
    avaliacao = matriz_criticidade_base().avaliacao_por_eixo.copy()
    avaliacao["EIXO_INVENTADO"] = "não existe no §11"
    with pytest.raises(ErroDeComentario):
        matriz_criticidade_base(avaliacao_por_eixo=avaliacao)


def test_avaliacao_de_eixo_vazia_rejeita():
    avaliacao = matriz_criticidade_base().avaliacao_por_eixo.copy()
    avaliacao[EixoCriticidade.FACTUAL] = ""
    with pytest.raises(ErroDeComentario):
        matriz_criticidade_base(avaliacao_por_eixo=avaliacao)


def test_classe_fora_do_enum_rejeita():
    with pytest.raises(ErroDeComentario):
        matriz_criticidade_base(classe="CRITICIDADE_MEDIA")  # string crua, não membro do enum


def test_justificativa_classe_vazia_rejeita():
    with pytest.raises(ErroDeComentario):
        matriz_criticidade_base(justificativa_classe="")


def test_sem_criticidade_material_e_classe_legitima():
    """PS13-01 — parágrafo adequado: classe SEM_CRITICIDADE_MATERIAL é um
    resultado legítimo, não uma falha de avaliação."""
    m = matriz_criticidade_base(
        classe=ClasseCriticidade.SEM_CRITICIDADE_MATERIAL,
        justificativa_classe="Nenhum eixo indica risco material; parágrafo adequado.",
    )
    assert m.classe == ClasseCriticidade.SEM_CRITICIDADE_MATERIAL

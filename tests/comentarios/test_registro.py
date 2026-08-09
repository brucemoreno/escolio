import pytest

from escolio.comentarios.erros import ErroDeComentario
from escolio.comentarios.registro import RegistroDeComentarios
from tests.comentarios.fixtures import comentario_base


def test_registra_comentario_sem_relacoes():
    reg = RegistroDeComentarios()
    c = comentario_base(comment_id="CMT-0001")
    reg.registrar(c)
    assert reg.obter("CMT-0001") is c


def test_related_comment_id_para_id_desconhecido_rejeita():
    reg = RegistroDeComentarios()
    c = comentario_base(comment_id="CMT-0002", related_comment_id="CMT-INEXISTENTE")
    with pytest.raises(ErroDeComentario):
        reg.registrar(c)


def test_related_comment_id_mesmo_documento_e_versao_passa():
    reg = RegistroDeComentarios()
    reg.registrar(comentario_base(comment_id="CMT-0001", document_id="DOC-A", document_version="1.0.0"))
    c2 = comentario_base(
        comment_id="CMT-0002",
        document_id="DOC-A",
        document_version="1.0.0",
        related_comment_id="CMT-0001",
    )
    reg.registrar(c2)
    assert reg.obter("CMT-0002").related_comment_id == "CMT-0001"


def test_related_comment_id_documento_diferente_rejeita():
    reg = RegistroDeComentarios()
    reg.registrar(comentario_base(comment_id="CMT-0001", document_id="DOC-A", document_version="1.0.0"))
    c2 = comentario_base(
        comment_id="CMT-0002",
        document_id="DOC-B",
        document_version="1.0.0",
        related_comment_id="CMT-0001",
    )
    with pytest.raises(ErroDeComentario):
        reg.registrar(c2)


def test_related_comment_id_versao_diferente_rejeita():
    reg = RegistroDeComentarios()
    reg.registrar(comentario_base(comment_id="CMT-0001", document_id="DOC-A", document_version="1.0.0"))
    c2 = comentario_base(
        comment_id="CMT-0002",
        document_id="DOC-A",
        document_version="2.0.0",
        related_comment_id="CMT-0001",
    )
    with pytest.raises(ErroDeComentario):
        reg.registrar(c2)


def test_matrix_comment_id_para_id_desconhecido_rejeita():
    reg = RegistroDeComentarios()
    c = comentario_base(comment_id="CMT-0002", matrix_comment_id="CMT-INEXISTENTE")
    with pytest.raises(ErroDeComentario):
        reg.registrar(c)


def test_matrix_comment_id_para_alvo_sem_tipo_comentario_matriz_rejeita():
    reg = RegistroDeComentarios()
    reg.registrar(comentario_base(comment_id="CMT-0001", comment_type="OBSERVACAO_ESTRUTURAL"))
    c2 = comentario_base(comment_id="CMT-0002", matrix_comment_id="CMT-0001")
    with pytest.raises(ErroDeComentario):
        reg.registrar(c2)


def test_matrix_comment_id_para_alvo_comentario_matriz_passa():
    reg = RegistroDeComentarios()
    reg.registrar(comentario_base(comment_id="CMT-MATRIZ-01", comment_type="COMENTARIO_MATRIZ"))
    c2 = comentario_base(
        comment_id="CMT-0002",
        comment_type="REMISSAO_A_COMENTARIO_MATRIZ",
        matrix_comment_id="CMT-MATRIZ-01",
    )
    reg.registrar(c2)
    assert reg.obter("CMT-0002").matrix_comment_id == "CMT-MATRIZ-01"

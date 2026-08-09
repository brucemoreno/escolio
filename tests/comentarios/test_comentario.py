import pytest

from escolio.comentarios.erros import ErroDeComentario
from escolio.comentarios.vocabulario import (
    P13CommentResolution,
    P13CommentStatus,
)
from tests.comentarios.fixtures import comentario_base


def test_comentario_minimo_valido():
    c = comentario_base()
    assert c.status == P13CommentStatus.DRAFT
    assert c.resolution is None
    assert c.related_comment_id is None
    assert c.matrix_comment_id is None


@pytest.mark.parametrize(
    "campo",
    [
        "comment_id",
        "document_id",
        "document_version",
        "module_id",
        "unit_id",
        "anchor_start",
        "anchor_end",
        "anchor_text_hash",
        "comment_type",
        "priority",
        "severity",
        "problem",
        "evidence",
        "impact",
        "recommended_action",
        "intervention_level",
        "authority_required",
        "gate",
        "source_status",
        "voice_impact",
        "privacy_classification",
    ],
)
def test_campo_obrigatorio_vazio_rejeita(campo):
    with pytest.raises(ErroDeComentario):
        comentario_base(**{campo: ""})


class TestStatus:
    def test_status_fora_do_enum_rejeita(self):
        with pytest.raises(ErroDeComentario):
            comentario_base(status="DRAFT")  # string crua, não membro do enum

    def test_status_sem_resolution_exigida_passa(self):
        comentario_base(status=P13CommentStatus.READY_FOR_REVIEW)

    @pytest.mark.parametrize(
        "status",
        [P13CommentStatus.RESOLVED, P13CommentStatus.SUPERSEDED, P13CommentStatus.WITHDRAWN],
    )
    def test_status_que_exige_resolution_sem_resolution_rejeita(self, status):
        with pytest.raises(ErroDeComentario):
            comentario_base(status=status, resolution=None)

    @pytest.mark.parametrize(
        "status",
        [P13CommentStatus.RESOLVED, P13CommentStatus.SUPERSEDED, P13CommentStatus.WITHDRAWN],
    )
    def test_status_que_exige_resolution_com_resolution_passa(self, status):
        comentario_base(status=status, resolution=P13CommentResolution.RESOLVIDO)


class TestResolution:
    def test_resolution_fora_do_enum_rejeita(self):
        with pytest.raises(ErroDeComentario):
            comentario_base(resolution="ACEITO")  # string crua, não membro do enum

    def test_resolution_null_fora_dos_status_que_exigem_passa(self):
        c = comentario_base(status=P13CommentStatus.DRAFT, resolution=None)
        assert c.resolution is None

    def test_resolution_preenchida_fora_dos_status_que_exigem_tambem_passa(self):
        # §31.5.2 não proíbe resolution cedo, só exige quando RESOLVED/
        # SUPERSEDED/WITHDRAWN — decisão humana pode chegar antes.
        c = comentario_base(
            status=P13CommentStatus.PENDING_HUMAN_DECISION,
            resolution=P13CommentResolution.ACEITO,
        )
        assert c.resolution == P13CommentResolution.ACEITO


class TestRelatedCommentId:
    def test_null_passa(self):
        comentario_base(related_comment_id=None)

    def test_string_vazia_rejeita(self):
        with pytest.raises(ErroDeComentario):
            comentario_base(related_comment_id="")

    def test_aponta_para_proprio_id_rejeita(self):
        with pytest.raises(ErroDeComentario):
            comentario_base(comment_id="CMT-0001", related_comment_id="CMT-0001")

    def test_aponta_para_outro_id_passa(self):
        c = comentario_base(comment_id="CMT-0001", related_comment_id="CMT-0002")
        assert c.related_comment_id == "CMT-0002"


class TestMatrixCommentId:
    def test_null_passa(self):
        comentario_base(matrix_comment_id=None)

    def test_string_vazia_rejeita(self):
        with pytest.raises(ErroDeComentario):
            comentario_base(matrix_comment_id="")

    def test_aponta_para_proprio_id_rejeita(self):
        with pytest.raises(ErroDeComentario):
            comentario_base(comment_id="CMT-0001", matrix_comment_id="CMT-0001")

    def test_aponta_para_outro_id_passa(self):
        c = comentario_base(comment_id="CMT-0001", matrix_comment_id="CMT-9999")
        assert c.matrix_comment_id == "CMT-9999"

    def test_remissao_sem_matrix_comment_id_rejeita(self):
        with pytest.raises(ErroDeComentario):
            comentario_base(comment_type="REMISSAO_A_COMENTARIO_MATRIZ", matrix_comment_id=None)

    def test_remissao_com_matrix_comment_id_passa(self):
        c = comentario_base(
            comment_id="CMT-0001",
            comment_type="REMISSAO_A_COMENTARIO_MATRIZ",
            matrix_comment_id="CMT-MATRIZ-01",
        )
        assert c.matrix_comment_id == "CMT-MATRIZ-01"

    def test_comentario_matriz_nao_exige_matrix_comment_id(self):
        c = comentario_base(comment_type="COMENTARIO_MATRIZ", matrix_comment_id=None)
        assert c.matrix_comment_id is None

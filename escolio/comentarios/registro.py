"""Integridade referencial entre `P13Comment` — fonte: P13 §31.5.3, §31.5.4.

`P13Comment.__post_init__` valida apenas o que um comentário sabe sobre si
mesmo (nulidade, auto-referência). As duas regras que exigem conhecer
*outro* comentário — "deve apontar para comentário do mesmo document_id e
document_version" e "deve apontar para comment_id cujo
comment_type=COMENTARIO_MATRIZ" — precisam de um registro dos comentários
já conhecidos, mesmo padrão de escolio/identificadores.py
(RegistroDeIdentificadores) para claim_id/source_id.
"""

from escolio.comentarios.comentario import P13Comment
from escolio.comentarios.erros import ErroDeComentario
from escolio.comentarios.vocabulario import COMMENT_TYPE_COMENTARIO_MATRIZ


class RegistroDeComentarios:
    """Índice de `P13Comment` registrados. `related_comment_id` e
    `matrix_comment_id` só podem ser validados contra comentários já
    registrados — ordem de registro importa (mesma exigência implícita em
    RegistroDeIdentificadores: não há verificação contra o que ainda não
    existe)."""

    def __init__(self) -> None:
        self._comentarios: dict[str, P13Comment] = {}

    def obter(self, comment_id: str) -> P13Comment | None:
        return self._comentarios.get(comment_id)

    def registrar(self, comentario: P13Comment) -> None:
        if comentario.related_comment_id is not None:
            self._valida_related(comentario)
        if comentario.matrix_comment_id is not None:
            self._valida_matrix(comentario)
        self._comentarios[comentario.comment_id] = comentario

    def _valida_related(self, comentario: P13Comment) -> None:
        alvo = self._comentarios.get(comentario.related_comment_id)
        if alvo is None:
            raise ErroDeComentario(
                "31.5.3",
                "related_comment_id aponta para comment_id não registrado",
                detalhe=comentario.related_comment_id,
            )
        # §31.5.3: "deve apontar para comentário do mesmo document_id e
        # document_version, salvo relação entre versões expressamente
        # rastreada." O schema mínimo não tem campo para expressar essa
        # exceção — ver LACUNAS.md; aqui só a regra geral é verificável.
        if alvo.document_id != comentario.document_id or alvo.document_version != comentario.document_version:
            raise ErroDeComentario(
                "31.5.3",
                "related_comment_id deve apontar para comentário do mesmo document_id e document_version",
                detalhe=(
                    f"origem={comentario.document_id}/{comentario.document_version} "
                    f"alvo={alvo.document_id}/{alvo.document_version}"
                ),
            )

    def _valida_matrix(self, comentario: P13Comment) -> None:
        alvo = self._comentarios.get(comentario.matrix_comment_id)
        if alvo is None:
            raise ErroDeComentario(
                "31.5.4",
                "matrix_comment_id aponta para comment_id não registrado",
                detalhe=comentario.matrix_comment_id,
            )
        if alvo.comment_type != COMMENT_TYPE_COMENTARIO_MATRIZ:
            raise ErroDeComentario(
                "31.5.4",
                "matrix_comment_id deve apontar para comment_id cujo comment_type=COMENTARIO_MATRIZ",
                detalhe=f"comment_type do alvo={alvo.comment_type!r}",
            )

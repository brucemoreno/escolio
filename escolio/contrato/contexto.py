"""Schema universal de contexto — fonte: P09 §7.

Regra do §7: contexto não substitui autorização, evidência, dependência ou
comando humano válido. Esta regra é declarativa na fonte (não há campo que a
codifique); nenhuma validação de código a implementa aqui — ver LACUNAS.md.
"""

from dataclasses import dataclass, field

from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.vocabulario import Canonicality, ContextType


@dataclass
class Applicability:
    applies_to: list[str] = field(default_factory=list)
    does_not_apply_to: list[str] = field(default_factory=list)


@dataclass
class ContextItem:
    context_id: str
    type: ContextType
    content_reference: str
    canonicality: Canonicality
    applicability: Applicability = field(default_factory=Applicability)
    precedence: int | None = None
    limitations: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.context_id:
            raise ErroDeContrato("P09-§7", "context_id é obrigatório")
        if not self.content_reference:
            raise ErroDeContrato("P09-§7", "content_reference é obrigatório")

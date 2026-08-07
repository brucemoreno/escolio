"""Vocabulário próprio de InterventionRecord — fonte: P09 §13.

`Disposition` é declarado no §13 do envelope P09, não em contrato/vocabulario.py
— pertence à peça de intervenção, não ao envelope genérico já implementado.
`AuthorizationStatus` é reusado de escolio.contrato.vocabulario (mesmo campo
semântico usado por Authorization em requisicao.py) — não duplicado aqui.
"""

from enum import Enum


class Disposition(str, Enum):
    APPLIED = "APPLIED"
    REFUSED = "REFUSED"
    ABSTAINED = "ABSTAINED"
    BLOCKED = "BLOCKED"

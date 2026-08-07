"""Schema de dependência — fonte: P09 §5.

VersionRequirement (§5.1) e DependencyItem (§5.2) validados em
__post_init__.
"""

from dataclasses import dataclass, field

from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.referencia import Reference, SemanticVersion, exige_referencia_verificada
from escolio.contrato.vocabulario import CompatibilityStatus, RequiredState, VersionMode


@dataclass
class VersionRange:
    minimum: SemanticVersion | None = None
    maximum: SemanticVersion | None = None
    include_minimum: bool = True
    include_maximum: bool = True


@dataclass
class VersionRequirement:
    mode: VersionMode
    exact: SemanticVersion | None = None
    minimum: SemanticVersion | None = None
    compatible_major: int | None = None
    range: VersionRange = field(default_factory=VersionRange)

    def __post_init__(self):
        # §5.1: cada modo exige seu campo preenchido; campos incompatíveis
        # com o modo selecionado devem permanecer nulos.
        campos = {
            VersionMode.EXACT: ("exact",),
            VersionMode.MINIMUM: ("minimum",),
            VersionMode.COMPATIBLE_MAJOR: ("compatible_major",),
            VersionMode.RANGE: (),  # verificado à parte: ao menos um limite
            VersionMode.ANY: (),
        }
        exigidos = campos[self.mode]
        todos = ("exact", "minimum", "compatible_major")

        for nome in exigidos:
            if getattr(self, nome) is None:
                raise ErroDeContrato(
                    "P09-§5.1", f"mode={self.mode.value} exige '{nome}' preenchido"
                )
        for nome in todos:
            if nome not in exigidos and getattr(self, nome) is not None:
                raise ErroDeContrato(
                    "P09-§5.1",
                    f"campo '{nome}' incompatível com mode={self.mode.value} deve permanecer nulo",
                )

        if self.mode == VersionMode.RANGE:
            if self.range.minimum is None and self.range.maximum is None:
                raise ErroDeContrato(
                    "P09-§5.1", "mode=RANGE exige pelo menos um limite (minimum ou maximum)"
                )
            if self.range.minimum is not None and self.range.maximum is not None:
                min_tupla = (self.range.minimum.major, self.range.minimum.minor, self.range.minimum.patch)
                max_tupla = (self.range.maximum.major, self.range.maximum.minor, self.range.maximum.patch)
                if min_tupla > max_tupla:
                    raise ErroDeContrato(
                        "P09-§5.1", "em mode=RANGE, o mínimo não pode ser superior ao máximo"
                    )
        else:
            if self.range.minimum is not None or self.range.maximum is not None:
                raise ErroDeContrato(
                    "P09-§5.1", "campo 'range' incompatível com mode diferente de RANGE deve permanecer nulo"
                )


@dataclass
class DependencyItem:
    dependency_id: str
    required_version: VersionRequirement
    required_state: RequiredState
    observed_state: str
    compatibility_status: CompatibilityStatus
    observed_version: SemanticVersion | None = None
    evidence: list[Reference] = field(default_factory=list)
    operation_scope: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.dependency_id:
            raise ErroDeContrato("P09-§5.2", "dependency_id é obrigatório")
        if not self.observed_state:
            raise ErroDeContrato("P09-§5.2", "observed_state é obrigatório")

        exige_versao = self.required_version.mode != VersionMode.ANY
        if exige_versao and self.observed_version is None and self.compatibility_status == CompatibilityStatus.COMPATIBLE:
            # §5.1: dependência que exige versão não pode ser declarada
            # satisfeita (COMPATIBLE) sem observed_version; §21.36.
            raise ErroDeContrato(
                "P09-§5.1",
                "dependência que exige versão não pode ser declarada COMPATIBLE sem observed_version",
            )

        if self.compatibility_status == CompatibilityStatus.NOT_APPLICABLE and exige_versao:
            # §5.1: NOT_APPLICABLE só é válido com mode=ANY ou quando a
            # dependência não possuir versão aplicável — como o schema não
            # tem um campo separado para "não possuir versão aplicável",
            # tratamos mode=ANY como a única condição verificável em código.
            raise ErroDeContrato(
                "P09-§5.1",
                "compatibility_status=NOT_APPLICABLE só é válido com mode=ANY ou dependência sem versão aplicável",
            )

        if self.compatibility_status == CompatibilityStatus.COMPATIBLE:
            # §5.2: dependência declarada satisfeita exige ao menos uma Reference VERIFIED.
            exige_referencia_verificada(
                self.evidence,
                "P09-§21.28",
                "dependência satisfeita (compatibility_status=COMPATIBLE) exige ao menos uma Reference VERIFIED",
            )

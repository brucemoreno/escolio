"""Modelo de dados da relação afirmação-evidência — fonte:
02_DICIONARIO_DE_DADOS_P05_R01.csv (23 campos, nomes e obrigatoriedade
exatamente como o CSV declara).

Campo obrigatório vazio impede a criação do registro (validação em
__post_init__, não em uma etapa separada opcional).
"""

from dataclasses import dataclass, field

from escolio.vocabulario import (
    AccessState,
    ClaimType,
    Confidence,
    EvidenceLevel,
    LocationType,
    ReadingState,
    Reversibility,
    SourceType,
    Sufficiency,
    UsageStatus,
    ValidationState,
)
from escolio.erros import ErroDeCoerencia

ARQUIVO_DICIONARIO = "02_DICIONARIO_DE_DADOS_P05_R01.csv"


def _exige_nao_vazio(nome_campo: str, valor):
    if valor is None or (isinstance(valor, str) and valor.strip() == ""):
        raise ErroDeCoerencia(
            regra_id="OBRIGATORIEDADE",
            fundamento=f"Campo obrigatório '{nome_campo}' vazio impede a criação do registro",
            arquivo_origem=ARQUIVO_DICIONARIO,
        )


@dataclass
class RelacaoAfirmacaoEvidencia:
    # --- Campos obrigatórios ---
    claim_id: str
    claim_text: str
    claim_type: ClaimType
    source_id: str
    source_type: SourceType
    source_reference: str
    location_type: LocationType
    evidence_level: EvidenceLevel
    access_state: AccessState
    reading_state: ReadingState
    validation_state: ValidationState
    sufficiency: Sufficiency
    confidence: Confidence
    usage_status: UsageStatus
    provenance: str
    reversibility: Reversibility

    # --- Campos condicionais (obrigatórios apenas quando o gatilho ocorre) ---
    edition_or_version: str | None = None
    location_value: str | None = None
    page_or_folio: str | None = None
    evidence_excerpt: str | None = None
    validator: str | None = None
    validation_date: str | None = None
    notes: str | None = None

    # Chave de versionamento (arquivo 01, seção 2 e arquivo 06, seção 4).
    # Não é um campo do dicionário de dados 02; pertence à chave composta da
    # relação (claim_id, source_id, relation_version) definida no arquivo 01.
    relation_version: int = 1

    def __post_init__(self):
        _exige_nao_vazio("claim_id", self.claim_id)
        _exige_nao_vazio("claim_text", self.claim_text)
        _exige_nao_vazio("source_id", self.source_id)
        _exige_nao_vazio("source_reference", self.source_reference)
        _exige_nao_vazio("provenance", self.provenance)

        # claim_type: OUTRA_CONTROLADA exige notes (regra_de_validacao do dicionário).
        if self.claim_type == ClaimType.OUTRA_CONTROLADA and not self.notes:
            raise ErroDeCoerencia(
                "CAMPO-claim_type",
                "claim_type=OUTRA_CONTROLADA exige notes",
                ARQUIVO_DICIONARIO,
            )
        # source_type: OUTRO_CONTROLADO exige notes.
        if self.source_type == SourceType.OUTRO_CONTROLADO and not self.notes:
            raise ErroDeCoerencia(
                "CAMPO-source_type",
                "source_type=OUTRO_CONTROLADO exige notes",
                ARQUIVO_DICIONARIO,
            )
        # validator/validation_date: obrigatório em VALIDADA/INVALIDADA_POSTERIORMENTE.
        if self.validation_state in (
            ValidationState.VALIDADA,
            ValidationState.INVALIDADA_POSTERIORMENTE,
        ):
            _exige_nao_vazio("validator", self.validator)
            _exige_nao_vazio("validation_date", self.validation_date)

        # location_value: obrigatório para PAGINA_CONFIRMADA (regra_de_validacao do dicionário).
        if self.validation_state == ValidationState.PAGINA_CONFIRMADA:
            _exige_nao_vazio("location_value", self.location_value)

        if self.relation_version < 1:
            raise ErroDeCoerencia(
                "VERSIONAMENTO",
                "relation_version inicia em 1",
                "06_PROTOCOLO_DE_IDENTIFICADORES_E_VERSIONAMENTO_P05_R01.txt",
            )

        # Regras de coerência que dependem apenas dos campos desta relação
        # (RC-001..RC-011, RC-015) são verificadas na construção do
        # registro, não em uma etapa separada opcional — mesmo tratamento
        # dado à obrigatoriedade de campo. Import local evita ciclo de
        # importação (regras_coerencia importa este módulo).
        from escolio.regras_coerencia import validar_regras_coerencia

        validar_regras_coerencia(self)

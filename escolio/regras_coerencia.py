"""Regras de coerência e incompatibilidade — fonte:
04_REGRAS_DE_COERENCIA_E_INCOMPATIBILIDADE_P05_R01.csv (RC-001..RC-020).

Todas as 20 regras do CSV são BLOQUEANTE ou MAIOR — o CSV não distingui
nenhuma como mero alerta não bloqueante (ver escolio/LACUNAS.md). Por
fidelidade literal, todas rejeitam o registro (ErroDeCoerencia) quando
violadas; nenhuma é implementada como sinalização silenciosa.

Regras RC-017 e RC-018 (severidade MAIOR) dizem respeito à forma como
MÚLTIPLAS relações são organizadas (uma relação por par claim/source), não
a um campo de uma única RelacaoAfirmacaoEvidencia — são verificadas pelo
RegistroDeRelacoes, não por validar_regras_coerencia.
"""

from escolio.erros import ErroDeCoerencia
from escolio.relacao import RelacaoAfirmacaoEvidencia
from escolio.vocabulario import (
    AccessState,
    Confidence,
    EvidenceLevel,
    ReadingState,
    Sufficiency,
    UsageStatus,
    ValidationState,
)

ARQUIVO_REGRAS = "04_REGRAS_DE_COERENCIA_E_INCOMPATIBILIDADE_P05_R01.csv"


def _erro(regra_id: str, fundamento: str, detalhe: str = "") -> ErroDeCoerencia:
    return ErroDeCoerencia(regra_id, fundamento, ARQUIVO_REGRAS, detalhe)


def rc_001(r: RelacaoAfirmacaoEvidencia) -> None:
    """access_state=ACESSADA exige evidência de abertura/recuperação.

    Base material da abertura: evidence_level distinto de D_AUSENTE, dado
    que D_AUSENTE significa ausência de qualquer materialidade registrada.
    """
    if r.access_state == AccessState.ACESSADA and r.evidence_level == EvidenceLevel.D_AUSENTE:
        raise _erro(
            "RC-001",
            "access_state=ACESSADA exige evidência de abertura/recuperação",
            "evidence_level=D_AUSENTE não sustenta ACESSADA",
        )


def rc_002(r: RelacaoAfirmacaoEvidencia) -> None:
    """reading_state=LIDA_PARCIALMENTE exige limites de leitura (notes)."""
    if r.reading_state == ReadingState.LIDA_PARCIALMENTE and not r.notes:
        raise _erro(
            "RC-002",
            "reading_state=LIDA_PARCIALMENTE exige limites de leitura",
            "notes com os limites do segmento lido é obrigatório",
        )


def rc_003(r: RelacaoAfirmacaoEvidencia) -> None:
    """reading_state=LIDA_INTEGRALMENTE exige objeto completo e exame
    integral — não pode coexistir com access_state que não seja ACESSADA."""
    if r.reading_state == ReadingState.LIDA_INTEGRALMENTE and r.access_state != AccessState.ACESSADA:
        raise _erro(
            "RC-003",
            "reading_state=LIDA_INTEGRALMENTE exige objeto completo e exame integral",
            "access_state deve ser ACESSADA; disponibilidade não prova leitura",
        )


def rc_004(r: RelacaoAfirmacaoEvidencia) -> None:
    """page_or_folio material exige edition_or_version e PAGINA_CONFIRMADA."""
    tem_page_material = r.page_or_folio and r.page_or_folio not in ("NAO_APLICAVEL", "NAO_CONFIRMADO")
    if tem_page_material:
        if not r.edition_or_version or r.edition_or_version in ("NAO_APLICAVEL", "NAO_CONFIRMADO"):
            raise _erro(
                "RC-004",
                "page_or_folio material exige edition_or_version e PAGINA_CONFIRMADA",
                "edition_or_version ausente ou não confirmado",
            )
        if r.validation_state != ValidationState.PAGINA_CONFIRMADA:
            raise _erro(
                "RC-004",
                "page_or_folio material exige edition_or_version e PAGINA_CONFIRMADA",
                f"validation_state={r.validation_state} não confirma a página",
            )


def rc_005(r: RelacaoAfirmacaoEvidencia) -> None:
    """validation_state=VALIDADA exige validator, validation_date e cadeia
    coerente (aqui: sufficiency avaliada, não NAO_AVALIADA)."""
    if r.validation_state == ValidationState.VALIDADA:
        if not r.validator or not r.validation_date:
            raise _erro(
                "RC-005",
                "validation_state=VALIDADA exige validator, validation_date e cadeia coerente",
                "validator/validation_date ausente",
            )
        if r.sufficiency == Sufficiency.NAO_AVALIADA:
            raise _erro(
                "RC-005",
                "validation_state=VALIDADA exige validator, validation_date e cadeia coerente",
                "sufficiency=NAO_AVALIADA quebra a cadeia",
            )


def rc_006(r: RelacaoAfirmacaoEvidencia) -> None:
    """sufficiency=EVIDENCIA_SUFICIENTE exige correspondência ao claim e
    escopo: evidence_excerpt registrado (não NAO_DISPONIVEL)."""
    if r.sufficiency == Sufficiency.EVIDENCIA_SUFICIENTE:
        if not r.evidence_excerpt or r.evidence_excerpt == "NAO_DISPONIVEL":
            raise _erro(
                "RC-006",
                "sufficiency=EVIDENCIA_SUFICIENTE exige correspondência ao claim e escopo",
                "evidence_excerpt ausente ou NAO_DISPONIVEL; quantidade não substitui adequação",
            )


def rc_007(r: RelacaoAfirmacaoEvidencia) -> None:
    """confidence=ALTA é incompatível com EVIDENCIA_AUSENTE."""
    if r.confidence == Confidence.ALTA and r.sufficiency == Sufficiency.EVIDENCIA_AUSENTE:
        raise _erro(
            "RC-007",
            "confidence=ALTA é incompatível com EVIDENCIA_AUSENTE",
            "confiança não cria evidência",
        )


def rc_008(r: RelacaoAfirmacaoEvidencia) -> None:
    """confidence=ALTA com EVIDENCIA_INSUFICIENTE nunca libera uso."""
    if r.confidence == Confidence.ALTA and r.sufficiency == Sufficiency.EVIDENCIA_INSUFICIENTE:
        if r.usage_status == UsageStatus.USO_LIBERADO:
            raise _erro(
                "RC-008",
                "confidence=ALTA com EVIDENCIA_INSUFICIENTE exige correção e nunca libera uso",
                "probabilidade não é prova",
            )


def rc_009(r: RelacaoAfirmacaoEvidencia) -> None:
    """usage_status=USO_LIBERADO exige VALIDADA e EVIDENCIA_SUFICIENTE."""
    if r.usage_status == UsageStatus.USO_LIBERADO:
        if r.validation_state != ValidationState.VALIDADA or r.sufficiency != Sufficiency.EVIDENCIA_SUFICIENTE:
            raise _erro(
                "RC-009",
                "usage_status=USO_LIBERADO exige VALIDADA e EVIDENCIA_SUFICIENTE",
                f"validation_state={r.validation_state}, sufficiency={r.sufficiency}",
            )


def rc_010(r: RelacaoAfirmacaoEvidencia) -> None:
    """LEITURA_INDIRETA exige fonte intermediária na proveniência."""
    if r.reading_state == ReadingState.LEITURA_INDIRETA:
        if "intermediari" not in r.provenance.lower():
            raise _erro(
                "RC-010",
                "LEITURA_INDIRETA exige fonte intermediária na proveniência",
                "provenance não identifica a fonte intermediária; mediação não pode ser ocultada",
            )


def rc_011(r: RelacaoAfirmacaoEvidencia) -> None:
    """evidence_level=D_AUSENTE é incompatível com VALIDADA."""
    if r.evidence_level == EvidenceLevel.D_AUSENTE and r.validation_state == ValidationState.VALIDADA:
        raise _erro(
            "RC-011",
            "evidence_level=D_AUSENTE é incompatível com VALIDADA",
            "ausência não sustenta validação",
        )


def rc_012(r: RelacaoAfirmacaoEvidencia, ha_conflito: bool = False) -> None:
    """Evidências conflitantes exigem sufficiency=CONFLITANTE até
    resolução/delimitação. `ha_conflito` é sinalizado externamente pelo
    chamador (RegistroDeRelacoes), pois conflito é uma propriedade entre
    relações, não de uma relação isolada."""
    if ha_conflito and r.sufficiency != Sufficiency.CONFLITANTE:
        raise _erro(
            "RC-012",
            "Evidências conflitantes exigem sufficiency=CONFLITANTE até resolução/delimitação",
            f"sufficiency={r.sufficiency} apesar de conflito registrado",
        )


def rc_013(r: RelacaoAfirmacaoEvidencia, edicao_da_pagina_confirmada: str | None = None) -> None:
    """Edições divergentes não compartilham paginação automaticamente.

    `edicao_da_pagina_confirmada` é a edição em que a página desta relação
    foi originalmente confirmada (se distinta da edition_or_version atual,
    a confirmação não é válida nesta edição).
    """
    if (
        r.validation_state == ValidationState.PAGINA_CONFIRMADA
        and edicao_da_pagina_confirmada is not None
        and edicao_da_pagina_confirmada != r.edition_or_version
    ):
        raise _erro(
            "RC-013",
            "Edições divergentes não compartilham paginação automaticamente",
            f"página confirmada em '{edicao_da_pagina_confirmada}', relação declara edição '{r.edition_or_version}'",
        )


def rc_014(notes: str | None, eh_substituicao: bool) -> None:
    """Substituição exige nova versão e referência à predecessora."""
    if eh_substituicao and (not notes or "supersedes_relation_version" not in notes):
        raise _erro(
            "RC-014",
            "Substituição exige nova versão e referência à predecessora",
            "notes deve conter supersedes_relation_version; histórico imutável",
        )


def rc_015(r: RelacaoAfirmacaoEvidencia) -> None:
    """INVALIDADA_POSTERIORMENTE é incompatível com USO_LIBERADO."""
    if r.validation_state == ValidationState.INVALIDADA_POSTERIORMENTE and r.usage_status == UsageStatus.USO_LIBERADO:
        raise _erro(
            "RC-015",
            "INVALIDADA_POSTERIORMENTE é incompatível com USO_LIBERADO",
            "invalidação retira liberação",
        )


# RC-016 (imutabilidade/não-reciclagem de IDs) é aplicada por
# escolio.identificadores.RegistroDeIdentificadores, não aqui — é uma regra
# sobre o ciclo de vida do identificador, não sobre os campos de uma relação
# já construída.

# RC-017 e RC-018 (severidade MAIOR) são verificadas por
# escolio.registro.RegistroDeRelacoes, pois dizem respeito a como múltiplas
# relações se organizam entre si, não a uma relação isolada.


def rc_019(pedido_texto: str) -> tuple[bool]:
    """Pedido para inventar página/evidência gera ABSTENCAO e NAO_USAR.

    Retorna (deve_abster,) — não lança exceção porque não há uma
    RelacaoAfirmacaoEvidencia construída ainda; o chamador decide o que
    fazer com o pedido (parar e registrar), conforme a ação_em_erro do CSV.
    """
    gatilhos = ("invente", "inventar", "crie uma página", "fabrique", "fabricar")
    texto = pedido_texto.lower()
    return (any(g in texto for g in gatilhos),)


def rc_020(r: RelacaoAfirmacaoEvidencia, fonte_parcial: bool = False, alegacao_alem_do_segmento: bool = False) -> None:
    """Fonte parcial não sustenta alegação sobre conteúdo não disponível."""
    if fonte_parcial and alegacao_alem_do_segmento:
        raise _erro(
            "RC-020",
            "Fonte parcial não sustenta alegação sobre conteúdo não disponível",
            "alegação excede o segmento disponível; preserva limites materiais",
        )


REGRAS_DE_CAMPO_UNICO = (
    rc_001,
    rc_002,
    rc_003,
    rc_004,
    rc_005,
    rc_006,
    rc_007,
    rc_008,
    rc_009,
    rc_010,
    rc_011,
    rc_015,
)


def validar_regras_coerencia(r: RelacaoAfirmacaoEvidencia) -> None:
    """Aplica as regras RC que dependem apenas dos campos da própria
    relação (RC-001..RC-011, RC-015). As demais (RC-012 a RC-014, RC-017,
    RC-018, RC-020) exigem contexto entre relações e são aplicadas pelo
    RegistroDeRelacoes; RC-016 pelo RegistroDeIdentificadores; RC-019 antes
    da construção da relação."""
    for regra in REGRAS_DE_CAMPO_UNICO:
        regra(r)

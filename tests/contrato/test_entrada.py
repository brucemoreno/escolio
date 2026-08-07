import pytest

from escolio.contrato.entrada import (
    Authority,
    Classification,
    ContentConsistency,
    InputItem,
    Provenance,
)
from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.referencia import Reference
from escolio.contrato.vocabulario import ConsistencyStatus, InputType, PreferredSource, ProvenanceStatus


def item_base(**overrides):
    campos = dict(
        input_id="INP-0001",
        type=InputType.DOCUMENT,
        provenance=Provenance(source="acervo", source_type="DOCUMENTO"),
    )
    campos.update(overrides)
    return InputItem(**campos)


def referencia(status=ProvenanceStatus.VERIFIED):
    return Reference(reference_id="REF-1", object_id="OBJ-1", object_type="DOCUMENTO", provenance_status=status)


def test_item_valido_minimo():
    item = item_base()
    assert item.authority.has_operational_authority is False


def test_input_id_ausente_rejeita():
    with pytest.raises(ErroDeContrato):
        item_base(input_id="")


def test_autoridade_operacional_sem_base_rejeita():
    with pytest.raises(ErroDeContrato):
        item_base(authority=Authority(has_operational_authority=True))


def test_autoridade_operacional_com_base_aceita():
    item = item_base(authority=Authority(has_operational_authority=True, authority_basis="autorização X"))
    assert item.authority.has_operational_authority is True


def test_not_applicable_com_inline_e_referencia_coexistindo_rejeita():
    with pytest.raises(ErroDeContrato):
        item_base(
            inline_content="texto",
            content_reference="arquivo.pdf",
            content_consistency=ContentConsistency(status=ConsistencyStatus.NOT_APPLICABLE),
        )


def test_consistent_com_inline_e_referencia_coexistindo_aceita():
    item = item_base(
        inline_content="texto",
        content_reference="arquivo.pdf",
        content_consistency=ContentConsistency(status=ConsistencyStatus.CONSISTENT),
    )
    assert item.content_consistency.status == ConsistencyStatus.CONSISTENT


def test_divergent_sem_resolution_required_rejeita():
    with pytest.raises(ErroDeContrato):
        item_base(
            inline_content="texto",
            content_reference="arquivo.pdf",
            content_consistency=ContentConsistency(status=ConsistencyStatus.DIVERGENT, resolution_required=False),
        )


def test_divergent_com_resolution_required_aceita():
    item = item_base(
        inline_content="texto",
        content_reference="arquivo.pdf",
        content_consistency=ContentConsistency(status=ConsistencyStatus.DIVERGENT, resolution_required=True),
    )
    assert item.content_consistency.resolution_required is True


def test_preferred_source_sem_referencia_verificada_rejeita():
    with pytest.raises(ErroDeContrato):
        item_base(
            content_consistency=ContentConsistency(
                status=ConsistencyStatus.CONSISTENT,
                preferred_source=PreferredSource.INLINE,
                comparison_evidence=[referencia(ProvenanceStatus.UNKNOWN)],
            )
        )


def test_preferred_source_com_referencia_verificada_aceita():
    item = item_base(
        content_consistency=ContentConsistency(
            status=ConsistencyStatus.CONSISTENT,
            preferred_source=PreferredSource.INLINE,
            comparison_evidence=[referencia(ProvenanceStatus.VERIFIED)],
        )
    )
    assert item.content_consistency.preferred_source == PreferredSource.INLINE


# --- Classification: os quatro eixos do P08 §4 são independentes [BL-016] ---
#
# Estes testes existem porque um rótulo de um eixo foi gravado no campo de outro, e
# porque um valor do P05 foi gravado num campo do P08. Não há validação de enum nos
# campos (o [P09 §6] os tipa `string`), logo a trava é o teste.

# [P08 §4.1] — cinco rótulos de confiança, um único vigente.
EIXO_CONFIANCA_P08 = {
    "CONFIAVEL_CANONICO",
    "CONFIAVEL_NAO_CANONICO",
    "NAO_CONFIAVEL",
    "SUSPEITO",
    "ORIGEM_DESCONHECIDA",
}

# [P08 §4.1] — nove estados, um único vigente. Nenhum significa "não classificado".
EIXO_ESTADO_P08 = {
    "ORIGINAL",
    "COPIA_VERIFICADA",
    "DERIVADO",
    "EM_ANALISE",
    "HOMOLOGADO",
    "CONGELADO",
    "SUPERADO",
    "ARQUIVADO",
    "DESTINADO_A_DESCARTE",
}


def test_trust_default_pertence_ao_eixo_de_confianca_do_p08():
    # [P09 §6.1]: "item sem proveniência suficiente deve ser marcado como
    # ORIGEM_DESCONHECIDA" — é o único dos cinco que o código pode afirmar sozinho.
    assert item_base().classification.trust == "ORIGEM_DESCONHECIDA"
    assert item_base().classification.trust in EIXO_CONFIANCA_P08


def test_trust_default_nao_importa_vocabulario_do_p05():
    # Regressão de BL-016: "NAO_AVALIADA" é valor de Sufficiency/Confidence do P05
    # (escolio/vocabulario.py), não do eixo de confiança do P08.
    assert item_base().classification.trust != "NAO_AVALIADA"


def test_state_default_e_defeito_conhecido_e_preservado():
    """Caracteriza um DEFEITO, não um requisito — ver CO-013 em docs/coleta.md.

    ORIGEM_DESCONHECIDA é rótulo do eixo de confiança, não de estado, e por isso a
    segunda asserção afirma que o valor está FORA do eixo correto. Preservado porque
    não existe valor certo a pôr: [P09 §6] declara `state: string` sem `| null`, e
    nenhum dos nove estados de [P08 §4.1] significa "ainda não classificado" — trocar
    por um dos nove seria inferência. Este teste falha de propósito se alguém
    "consertar" o campo sem decidir CO-013.
    """
    assert item_base().classification.state == "ORIGEM_DESCONHECIDA"
    assert item_base().classification.state not in EIXO_ESTADO_P08


def test_eixos_de_confianca_e_estado_nao_compartilham_rotulo():
    # [P08 §4]: os quatro eixos são independentes. Nenhum rótulo é válido em dois.
    assert EIXO_CONFIANCA_P08.isdisjoint(EIXO_ESTADO_P08)


def test_classification_aceita_rotulos_dos_dois_eixos_sem_validar():
    # Documenta a ausência de validação: o campo é `str` porque [P09 §6] o tipa
    # `string`. Apertar para enum é decisão pendente (CO-012), não conserto — e
    # enquanto não for decidida, nada impede gravar rótulo do eixo errado.
    c = Classification(trust="ORIGINAL", state="SUSPEITO")
    assert c.trust not in EIXO_CONFIANCA_P08
    assert c.state not in EIXO_ESTADO_P08

import pytest

from escolio.contrato.entrada import Authority, ContentConsistency, InputItem, Provenance
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

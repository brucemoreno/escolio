import pytest

from escolio.contrato.entrada import Classification, InputItem, Provenance
from escolio.contrato.referencia import SemanticVersion
from escolio.contrato.requisicao import (
    Authorization,
    ExpectedOutput,
    Request,
    Requester,
    Scope,
)
from escolio.contrato.vocabulario import (
    AbstentionCategory,
    AuthorizationStatus,
    InputType,
)
from escolio.funcoes import roteador
from escolio.funcoes.erros import ErroDeRoteamento
from escolio.funcoes.roteador import (
    AdmissaoDeMaterial,
    abstencao_por_fora_de_escopo,
    exige_correspondencia_de_funcao,
    exige_funcao_conhecida,
    exige_funcao_pertence_ao_componente,
    exige_operacao_compativel,
    rotear,
    verificar_material,
    verificar_operacao,
)
from escolio.funcoes.vocabulario import FuncaoId


def item(input_id="IN-1", functions=None):
    return InputItem(
        input_id=input_id,
        type=InputType.DOCUMENT,
        provenance=Provenance(source="data/dev/x.pdf", source_type="PDF"),
        classification=Classification(trust="NAO_AVALIADA", functions=list(functions or [])),
    )


def requisicao_base(**overrides):
    campos = dict(
        schema_version=SemanticVersion(1, 0, 0),
        request_id="REQ-0001",
        project_id="PRJ-0001",
        component_id="P13",
        function_id="LLM-ACA-F04",
        operation="CARTOGRAFIA_GLOBAL",
        requester=Requester(role="ENGENHEIRO_LLM", authority_basis="R03 §4.5"),
        scope=Scope(
            allowed_operations=["CARTOGRAFIA_GLOBAL"], prohibited_operations=["HOMOLOGAR"]
        ),
        authorization=Authorization(status=AuthorizationStatus.UNVERIFIED),
        expected_output=ExpectedOutput(type="COMENTARIOS"),
    )
    campos.update(overrides)
    return Request(**campos)


class _Resposta:
    """Duplo mínimo: `exige_correspondencia_de_funcao` só lê function_id, e
    seus parâmetros são propositalmente não anotados (mesmo motivo que em
    escolio/contrato/resposta.py — evitar dependência circular)."""

    def __init__(self, function_id):
        self.function_id = function_id


# --- o roteador não elege (LAC-FUNC-001; POL-007) ---


def test_roteador_nao_expoe_selecionar_funcao():
    # A ausência é o mecanismo, não um comentário: POL-007 proíbe "inferir
    # próxima fase, componente ou operação" e o CLAUDE.md §8 exige que a
    # abstenção seja ausência de caminho de código.
    assert not hasattr(roteador, "selecionar_funcao")


def test_roteador_nao_expoe_nenhum_seletor_nem_inferidor():
    publicos = [n for n in dir(roteador) if not n.startswith("_")]
    proibidos = ("selecion", "escolh", "inferir", "deduz", "adivinh", "detect", "classific")
    assert [n for n in publicos if any(p in n.lower() for p in proibidos)] == []


def test_roteador_nao_executa():
    publicos = [n for n in dir(roteador) if not n.startswith("_")]
    assert [n for n in publicos if "executar" in n.lower() or "rodar" in n.lower()] == []


# --- function_id ∈ catálogo (P09 §4.2.6) ---


def test_funcao_conhecida_valida():
    assert exige_funcao_conhecida("LLM-ACA-F02") is FuncaoId.F02


def test_funcao_conhecida_fora_do_catalogo_rejeita():
    with pytest.raises(ErroDeRoteamento):
        exige_funcao_conhecida("LLM-ACA-F99")


# --- function_id pertence ao component_id (P09 §4.2.4, §4.2.7) ---


def test_funcao_no_componente_correto_valido():
    assert exige_funcao_pertence_ao_componente(FuncaoId.F04, "P13") is None


def test_funcao_em_componente_alheio_rejeita():
    with pytest.raises(ErroDeRoteamento) as exc:
        exige_funcao_pertence_ao_componente(FuncaoId.F04, "P11")
    assert exc.value.regra_id == "P09-§4.2.7"


def test_x01_vinculado_a_qualquer_componente_rejeita():
    # Função transversal sem componente numerado — LAC-FUNC-003.
    with pytest.raises(ErroDeRoteamento) as exc:
        exige_funcao_pertence_ao_componente(FuncaoId.X01, "P13")
    assert exc.value.regra_id == "P09-§4.2.4"


# --- operação (P09 §4.2.5) — inconclusiva, LAC-FUNC-005 ---


def test_verificacao_de_operacao_e_inconclusiva_em_todas_as_seis():
    # Nenhuma fonte enumera operações por função. Inconclusivo é
    # registrado, não convertido em aprovação silenciosa.
    for funcao_id in FuncaoId:
        v = verificar_operacao(funcao_id, "QUALQUER_COISA")
        assert v.conclusiva is False
        assert v.compativel is None
        assert v.fundamento


def test_operacao_inconclusiva_nao_levanta():
    assert exige_operacao_compativel(FuncaoId.F04, "OPERACAO_INVENTADA") is None


# --- correspondência de função request↔response (P09 §8.1) ---


def test_correspondencia_de_funcao_valida():
    req = requisicao_base()
    assert exige_correspondencia_de_funcao(req, _Resposta("LLM-ACA-F04")) is None


def test_correspondencia_de_funcao_divergente_rejeita():
    req = requisicao_base()
    with pytest.raises(ErroDeRoteamento) as exc:
        exige_correspondencia_de_funcao(req, _Resposta("LLM-ACA-F02"))
    assert exc.value.regra_id == "P09-§8.1"


# --- material declarado para a função (P09 §6) ---


def test_material_declarado_para_a_funcao():
    d = verificar_material(item(functions=["LLM-ACA-F04"]), FuncaoId.F04)
    assert d.admissao is AdmissaoDeMaterial.DECLARADO


def test_material_declarado_para_outra_funcao_fica_fora_de_escopo():
    d = verificar_material(item(functions=["LLM-ACA-F02"]), FuncaoId.F04)
    assert d.admissao is AdmissaoDeMaterial.NAO_DECLARADO
    assert d.funcoes_declaradas == ("LLM-ACA-F02",)


def test_material_sem_declaracao_fica_indeterminado():
    # P19 §17, precedente de material_type=null: registrar a
    # indeterminação, não conceder elegibilidade. Indeterminado não é
    # DECLARADO nem NAO_DECLARADO.
    d = verificar_material(item(functions=[]), FuncaoId.F04)
    assert d.admissao is AdmissaoDeMaterial.INDETERMINADO
    assert d.funcoes_declaradas == ()


def test_indeterminado_nao_concede_elegibilidade():
    decisao = rotear(requisicao_base(inputs=[item(functions=[])]))
    assert decisao.materiais_indeterminados
    assert not [
        m for m in decisao.materiais if m.admissao is AdmissaoDeMaterial.DECLARADO
    ]


def test_material_declarado_para_varias_funcoes_inclusive_a_pedida():
    d = verificar_material(item(functions=["LLM-ACA-F02", "LLM-ACA-F04"]), FuncaoId.F04)
    assert d.admissao is AdmissaoDeMaterial.DECLARADO


# --- abstenção por fora de escopo (P09 §23; LAC-FUNC-010) ---


def test_abstencao_por_fora_de_escopo_valida():
    materiais = (verificar_material(item(functions=["LLM-ACA-F02"]), FuncaoId.F04),)
    p = abstencao_por_fora_de_escopo("ABS-1", "REQ-0001", FuncaoId.F04, materiais)
    assert p.category is AbstentionCategory.OUT_OF_SCOPE
    assert p.scope == ["IN-1"]
    assert p.human_decision_required is True
    assert p.reversible is True
    assert p.resume_conditions  # §15.1: reversible=true exige retomada


def test_abstencao_sem_material_rejeita():
    # §15.1: a abstenção deve ser localizada ao ponto inseguro.
    with pytest.raises(ErroDeRoteamento):
        abstencao_por_fora_de_escopo("ABS-1", "REQ-0001", FuncaoId.F04, ())


# --- rotear (agregado) ---


def test_rotear_requisicao_coerente_valido():
    d = rotear(requisicao_base(inputs=[item(functions=["LLM-ACA-F04"])]))
    assert d.funcao is FuncaoId.F04
    assert d.declaracao.component_id == "P13"
    assert d.materiais_fora_de_escopo == ()
    assert d.materiais_indeterminados == ()


def test_rotear_com_funcao_desconhecida_rejeita():
    with pytest.raises(ErroDeRoteamento):
        rotear(requisicao_base(function_id="LLM-ACA-F42"))


def test_rotear_com_componente_divergente_rejeita():
    with pytest.raises(ErroDeRoteamento):
        rotear(requisicao_base(component_id="P11"))


def test_rotear_nao_levanta_para_material_fora_de_escopo():
    # Fora de escopo é resultado a representar no envelope, não falha de
    # contrato: P09 §4.2.17, "ausência legítima de autoridade, sem falha
    # formal, produz abstenção localizada".
    d = rotear(requisicao_base(inputs=[item(functions=["LLM-ACA-F02"])]))
    assert len(d.materiais_fora_de_escopo) == 1


def test_rotear_sem_inputs_devolve_materiais_vazio():
    d = rotear(requisicao_base())
    assert d.materiais == ()

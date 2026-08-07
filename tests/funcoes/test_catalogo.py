import pytest

from escolio.funcoes import p10, p11, p12, p13, p14, x01
from escolio.funcoes.catalogo import (
    CATALOGO,
    COMPONENTE_POR_FUNCAO,
    declaracao_de,
    funcao_de,
)
from escolio.funcoes.erros import ErroDeRoteamento
from escolio.funcoes.vocabulario import FuncaoId

# --- catálogo fechado (P02 §1; LAC-P02-005) ---


def test_catalogo_tem_exatamente_seis_unidades():
    assert len(CATALOGO) == 6
    assert len(FuncaoId) == 6


def test_catalogo_cobre_todos_os_membros_do_enum():
    assert set(CATALOGO) == set(FuncaoId)
    assert set(COMPONENTE_POR_FUNCAO) == set(FuncaoId)


def test_cada_funcao_aponta_para_seu_modulo():
    assert declaracao_de(FuncaoId.F01) is p10.DECLARACAO
    assert declaracao_de(FuncaoId.F02) is p11.DECLARACAO
    assert declaracao_de(FuncaoId.F03) is p12.DECLARACAO
    assert declaracao_de(FuncaoId.F04) is p13.DECLARACAO
    assert declaracao_de(FuncaoId.F05) is p14.DECLARACAO
    assert declaracao_de(FuncaoId.X01) is x01.DECLARACAO


def test_declaracao_declara_o_proprio_id_e_componente():
    for funcao_id, decl in CATALOGO.items():
        assert decl.funcao_id is funcao_id
        assert decl.component_id == COMPONENTE_POR_FUNCAO[funcao_id]


# --- function_id (P09 §4.2.6) ---


def test_funcao_de_valor_canonico_valido():
    assert funcao_de("LLM-ACA-F04") is FuncaoId.F04
    assert funcao_de("LLM-ACA-X01") is FuncaoId.X01


def test_funcao_desconhecida_rejeita():
    with pytest.raises(ErroDeRoteamento):
        funcao_de("LLM-ACA-F06")


def test_funcao_por_codigo_de_componente_rejeita():
    # P1x é identificador de componente, não de função — não é aceito por
    # inferência ainda que designe a mesma unidade.
    with pytest.raises(ErroDeRoteamento):
        funcao_de("P13")


def test_funcao_por_correspondencia_aproximada_rejeita():
    for valor in ("llm-aca-f04", "LLM-ACA-F04 ", "F04", "LLM-ACA-F0"):
        with pytest.raises(ErroDeRoteamento):
            funcao_de(valor)


def test_funcao_vazia_rejeita():
    with pytest.raises(ErroDeRoteamento):
        funcao_de("")


def test_erro_de_funcao_desconhecida_cita_a_regra_e_a_fonte():
    with pytest.raises(ErroDeRoteamento) as exc:
        funcao_de("LLM-ACA-F09")
    assert exc.value.regra_id == "P09-§4.2.6"
    assert "P02" in exc.value.arquivo_origem


# --- correspondência F0x ↔ P1x [PROPOSTA], LAC-FUNC-002 ---


def test_apenas_as_cinco_macrofuncoes_tem_componente_numerado():
    numerados = {f: c for f, c in COMPONENTE_POR_FUNCAO.items() if c is not None}
    assert set(numerados.values()) == {"P10", "P11", "P12", "P13", "P14"}


def test_x01_nao_tem_componente_numerado():
    # Não consta como componente no inventário canônico da R03 — LAC-FUNC-003.
    assert COMPONENTE_POR_FUNCAO[FuncaoId.X01] is None
    assert x01.DECLARACAO.component_id is None


def test_namespaces_de_funcao_e_componente_sao_disjuntos():
    # É o que dá conteúdo a P09 §4.2.4: "function_id deve pertencer ao
    # component_id" só significa algo entre namespaces distintos.
    funcoes = {f.value for f in FuncaoId}
    componentes = {c for c in COMPONENTE_POR_FUNCAO.values() if c is not None}
    assert funcoes.isdisjoint(componentes)

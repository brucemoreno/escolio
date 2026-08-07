import dataclasses

import pytest

from escolio.funcoes.declaracao import DeclaracaoDeFuncao, Etapa, Gate, OrdemDeclarada
from escolio.funcoes.erros import ErroDeDeclaracao
from escolio.funcoes.vocabulario import ClasseDeGate, FaseDaEspinha, FuncaoId

CAMPOS_R03_CAMADA_B = (
    "objetivo",
    "entradas_minimas",
    "precondicoes",
    "decisoes",
    "fluxo",
    "gates",
    "saidas",
    "limites",
    "falhas_proibidas",
    "testes_de_aceitacao",
    "rastreabilidade",
    "dados_necessarios",
)


def declaracao_base(**overrides):
    campos = dict(
        funcao_id=FuncaoId.F02,
        component_id="P11",
        denominacao="Revisão de dissertação e tese",
        arquivo_fonte="X.md",
        objetivo="objetivo declarado",
        entradas_minimas=("a",),
        precondicoes=("b",),
        decisoes=("c",),
        fluxo=(Etapa(1, "primeira"), Etapa(2, "segunda")),
        gates=(Gate("GATE_A", ClasseDeGate.DOCUMENTAL),),
        saidas=("d",),
        limites=("e",),
        falhas_proibidas=("f",),
        testes_de_aceitacao=("g",),
        rastreabilidade=("h",),
        dados_necessarios=("i",),
    )
    campos.update(overrides)
    return DeclaracaoDeFuncao(**campos)


# --- os doze campos da R03 CAMADA B ---


def test_declaracao_tem_os_doze_campos_da_r03_camada_b():
    nomes = {f.name for f in dataclasses.fields(DeclaracaoDeFuncao)}
    assert set(CAMPOS_R03_CAMADA_B) <= nomes


def test_declaracao_nao_tem_campo_de_criterio_de_selecao():
    # "critério de seleção" não está entre os doze campos da R03 CAMADA B —
    # confirmação, por fonte independente dos cinco contratos, de que
    # selecionar não é atributo declarável de uma função. LAC-FUNC-001.
    nomes = {f.name for f in dataclasses.fields(DeclaracaoDeFuncao)}
    proibidos = ("selecao", "selecionar", "criterio_de_selecao", "aplicabilidade")
    assert [n for n in nomes if any(p in n for p in proibidos)] == []


def test_declaracao_valida_minima():
    d = declaracao_base()
    assert d.funcao_id is FuncaoId.F02


def test_objetivo_ausente_rejeita():
    with pytest.raises(ErroDeDeclaracao):
        declaracao_base(objetivo="")


def test_denominacao_ausente_rejeita():
    with pytest.raises(ErroDeDeclaracao):
        declaracao_base(denominacao="")


# --- ordem do fluxo ---


def test_fluxo_vazio_valido():
    # P10 e X01 não têm fluxo numerado na fonte — LAC-FUNC-003, LAC-FUNC-004.
    assert declaracao_base(fluxo=()).fluxo == ()


def test_fluxo_com_lacuna_de_ordem_rejeita():
    with pytest.raises(ErroDeDeclaracao):
        declaracao_base(fluxo=(Etapa(1, "a"), Etapa(3, "c")))


def test_fluxo_com_ordem_repetida_rejeita():
    with pytest.raises(ErroDeDeclaracao):
        declaracao_base(fluxo=(Etapa(1, "a"), Etapa(1, "b")))


def test_fluxo_iniciando_em_zero_rejeita():
    with pytest.raises(ErroDeDeclaracao):
        declaracao_base(fluxo=(Etapa(0, "a"), Etapa(1, "b")))


def test_gate_duplicado_rejeita():
    with pytest.raises(ErroDeDeclaracao):
        declaracao_base(
            gates=(
                Gate("GATE_A", ClasseDeGate.DOCUMENTAL),
                Gate("GATE_A", ClasseDeGate.HUMANO_EXPRESSO),
            )
        )


# --- próxima ação única (POL-012) ---


def test_proxima_etapa_devolve_uma_so():
    d = declaracao_base()
    assert d.proxima_etapa(0) == Etapa(1, "primeira")
    assert d.proxima_etapa(1) == Etapa(2, "segunda")


def test_proxima_etapa_no_fim_devolve_none():
    # "registrar exatamente uma próxima ação permitida ou nenhuma
    # automática" [POL-012].
    assert declaracao_base().proxima_etapa(2) is None


def test_proxima_etapa_de_fluxo_vazio_devolve_none():
    assert declaracao_base(fluxo=()).proxima_etapa(0) is None


def test_proxima_etapa_negativa_rejeita():
    with pytest.raises(ErroDeDeclaracao):
        declaracao_base().proxima_etapa(-1)


def test_declaracao_nao_expoe_executar():
    publicos = [n for n in dir(DeclaracaoDeFuncao) if not n.startswith("_")]
    assert [n for n in publicos if "executar" in n.lower() or "avancar" in n.lower()] == []


# --- imutabilidade e consulta ---


def test_etapa_gate_e_ordem_sao_congelados():
    with pytest.raises(dataclasses.FrozenInstanceError):
        Etapa(1, "a").ordem = 2
    with pytest.raises(dataclasses.FrozenInstanceError):
        Gate("G", ClasseDeGate.DOCUMENTAL).etapa = 3
    with pytest.raises(dataclasses.FrozenInstanceError):
        OrdemDeclarada("§1", "x", ()).secao = "§2"


def test_etapa_por_ordem():
    d = declaracao_base()
    assert d.etapa(2) == Etapa(2, "segunda")
    assert d.etapa(99) is None


def test_gates_da_classe_filtra():
    d = declaracao_base(
        gates=(
            Gate("GATE_A", ClasseDeGate.DOCUMENTAL),
            Gate("GATE_B", ClasseDeGate.HUMANO_EXPRESSO),
        )
    )
    assert [g.nome for g in d.gates_da_classe(ClasseDeGate.DOCUMENTAL)] == ["GATE_A"]


def test_fase_e_opcional_por_etapa():
    # Onde a etapa não corresponde a nenhuma das sete fases, fase=None —
    # não se força correspondência. LAC-FUNC-008.
    assert Etapa(1, "a").fase is None
    assert Etapa(1, "a", FaseDaEspinha.E1_INTAKE_E_AUTORIDADE).fase is FaseDaEspinha.E1_INTAKE_E_AUTORIDADE

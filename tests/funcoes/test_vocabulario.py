from escolio.contrato import vocabulario as voc_p09
from escolio.funcoes.vocabulario import ClasseDeGate, FaseDaEspinha, FuncaoId

# --- catálogo fechado (P02 §1; LAC-P02-005) ---


def test_seis_funcoes_e_os_valores_do_p02():
    assert [f.value for f in FuncaoId] == [
        "LLM-ACA-F01",
        "LLM-ACA-F02",
        "LLM-ACA-F03",
        "LLM-ACA-F04",
        "LLM-ACA-F05",
        "LLM-ACA-X01",
    ]


def test_funcao_id_e_str_enum_como_o_resto_da_casa():
    assert isinstance(FuncaoId.F01, str)
    assert FuncaoId.F01 == "LLM-ACA-F01"


# --- classes de gate não colapsadas (LAC-FUNC-006) ---


def test_sete_rotulos_de_classe_de_gate():
    # P10, P11/P12, P13 e P14 usam nomenclaturas diferentes e nenhuma
    # fonte declara equivalência entre elas [CLAUDE.md §7].
    assert len(ClasseDeGate) == 7


def test_documental_e_validacao_documental_sao_rotulos_distintos():
    assert ClasseDeGate.DOCUMENTAL is not ClasseDeGate.VALIDACAO_DOCUMENTAL
    assert ClasseDeGate.DOCUMENTAL.value != ClasseDeGate.VALIDACAO_DOCUMENTAL.value


def test_os_tres_rotulos_humanos_sao_distintos():
    humanos = {
        ClasseDeGate.DECISAO_HUMANA_EXPRESSA,
        ClasseDeGate.HUMANO_EXPRESSO,
        ClasseDeGate.HUMANO_OBRIGATORIO,
        ClasseDeGate.HUMANO_ADICIONAL_COMPATIVEL,
    }
    assert len(humanos) == 4


# --- espinha (CLAUDE.md §4, [PROPOSTA]) ---


def test_sete_fases_na_ordem_do_claude_md():
    assert [f.value for f in FaseDaEspinha] == ["E1", "E2", "E3", "E4", "E5", "E6", "E7"]


# --- não fundir com vocabulários vizinhos ---


def test_nenhum_rotulo_colide_com_o_vocabulario_do_p09():
    # O P09 tem seus próprios enums de status, categoria e disposição;
    # nada aqui os duplica nem os renomeia.
    nossos = {c.value for c in ClasseDeGate} | {f.value for f in FuncaoId}
    alheios = (
        {s.value for s in voc_p09.ResponseStatus}
        | {a.value for a in voc_p09.AbstentionCategory}
        | {b.value for b in voc_p09.BlockCategory}
    )
    assert nossos.isdisjoint(alheios)

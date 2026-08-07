"""As contagens deste arquivo são verificáveis contra a fonte.

Cada número vem de uma seção nomeada de um contrato homologado; se um
módulo divergir, é o módulo que está errado, não o teste.
"""

import importlib

import pytest

from escolio.funcoes import p10, p11, p12, p13, p14, x01
from escolio.funcoes.vocabulario import ClasseDeGate, FaseDaEspinha, FuncaoId

MODULOS = (p10, p11, p12, p13, p14, x01)

# (módulo, etapas declaradas pela fonte, seção da fonte)
ETAPAS_POR_FONTE = (
    (p10, 0, "sem fluxo numerado — LAC-FUNC-004"),
    (p11, 25, "§38"),
    (p12, 32, "§41"),
    (p13, 29, "§43"),
    (p14, 32, "§75"),
    (x01, 0, "P02 não declara etapas — LAC-FUNC-003"),
)

# (módulo, gates nomeados, seções da fonte)
GATES_POR_FONTE = (
    (p10, 12, "§29.2 oito + §29.3 quatro"),
    (p11, 18, "§28.1 seis + §28.2 doze"),
    (p12, 16, "§31.1 seis + §31.2 dez"),
    (p13, 17, "§32.1 seis + §32.2 onze"),
    (p14, 28, "§41.1 nove + §41.2 dezessete + §41.3 dois"),
)


# --- contagem contra a fonte ---


@pytest.mark.parametrize("modulo,esperado,fonte", ETAPAS_POR_FONTE)
def test_numero_de_etapas_bate_com_a_fonte(modulo, esperado, fonte):
    assert len(modulo.DECLARACAO.fluxo) == esperado, fonte


@pytest.mark.parametrize("modulo,esperado,fonte", GATES_POR_FONTE)
def test_numero_de_gates_bate_com_a_fonte(modulo, esperado, fonte):
    assert len(modulo.DECLARACAO.gates) == esperado, fonte


def test_total_de_gates_nomeados_nos_cinco_contratos():
    assert sum(len(m.DECLARACAO.gates) for m, _, _ in GATES_POR_FONTE) == 91


def test_entradas_obrigatorias_dos_contratos_com_lista_de_vinte():
    # P11 §6.1 e P14 §6.1 declaram vinte itens cada.
    assert len(p11.DECLARACAO.entradas_minimas) == 20
    assert len(p14.DECLARACAO.entradas_minimas) == 20
    # P13 §6.1 declara dezoito.
    assert len(p13.DECLARACAO.entradas_minimas) == 18
    # P12: vinte de §6.1 mais três de §6.2 (obrigatórias quando aplicáveis).
    assert len(p12.DECLARACAO.entradas_minimas) == 23


# --- nenhum módulo executa (POL-012) ---


@pytest.mark.parametrize("modulo", MODULOS)
def test_modulo_nao_expoe_executor(modulo):
    publicos = [n for n in dir(modulo) if not n.startswith("_")]
    proibidos = ("executar", "rodar", "processar", "aplicar", "run")
    assert [n for n in publicos if n.lower() in proibidos] == []


@pytest.mark.parametrize("modulo", MODULOS)
def test_modulo_nao_expoe_seletor(modulo):
    publicos = [n for n in dir(modulo) if not n.startswith("_")]
    proibidos = ("selecion", "escolh", "inferir", "classific")
    assert [n for n in publicos if any(p in n.lower() for p in proibidos)] == []


@pytest.mark.parametrize("modulo", MODULOS)
def test_modulo_expoe_uma_unica_declaracao(modulo):
    assert hasattr(modulo, "DECLARACAO")


# --- gates sem posição (LAC-FUNC-007) ---


@pytest.mark.parametrize("modulo", MODULOS)
def test_nenhum_gate_tem_posicao_declarada(modulo):
    # Nenhum contrato liga gate a etapa. Semelhança de nome não é
    # afirmação da fonte.
    assert [g.nome for g in modulo.DECLARACAO.gates if g.etapa is not None] == []


def test_classe_automaticamente_verificavel_nao_tem_membro():
    # P10 §29.1 declara a classe e não nomeia gate algum.
    for modulo in MODULOS:
        assert modulo.DECLARACAO.gates_da_classe(ClasseDeGate.AUTOMATICAMENTE_VERIFICAVEL) == ()


def test_cada_contrato_usa_os_rotulos_de_classe_do_proprio_texto():
    # LAC-FUNC-006: rótulos não colapsados.
    def classes(modulo):
        return {g.classe for g in modulo.DECLARACAO.gates}

    assert classes(p10) == {
        ClasseDeGate.DECISAO_HUMANA_EXPRESSA,
        ClasseDeGate.VALIDACAO_DOCUMENTAL,
    }
    assert classes(p11) == classes(p12) == {
        ClasseDeGate.DECISAO_HUMANA_EXPRESSA,
        ClasseDeGate.VALIDACAO_DOCUMENTAL,
    }
    assert classes(p13) == {ClasseDeGate.DOCUMENTAL, ClasseDeGate.HUMANO_EXPRESSO}
    assert classes(p14) == {
        ClasseDeGate.DOCUMENTAL,
        ClasseDeGate.HUMANO_OBRIGATORIO,
        ClasseDeGate.HUMANO_ADICIONAL_COMPATIVEL,
    }


def test_gate_de_ativacao_declarado_em_cada_uma_das_cinco():
    for modulo, componente in ((p10, "P10"), (p11, "P11"), (p12, "P12"), (p13, "P13"), (p14, "P14")):
        nomes = {g.nome for g in modulo.DECLARACAO.gates}
        assert f"GATE_DE_ATIVACAO_{componente}" in nomes


# --- etapas verbatim (amostra ancorada na fonte) ---


def test_primeira_e_ultima_etapa_de_cada_fluxo():
    assert p11.DECLARACAO.fluxo[0].nome == "Intake e configuração"
    assert p11.DECLARACAO.fluxo[-1].nome == "Piloto supervisionado real posterior"
    assert p12.DECLARACAO.fluxo[0].nome == "intake e configuração"
    assert p12.DECLARACAO.fluxo[-1].nome == "ativação operacional posterior"
    assert p13.DECLARACAO.fluxo[0].nome == "intake"
    assert p13.DECLARACAO.fluxo[-1].nome == "ativação operacional posterior"
    assert p14.DECLARACAO.fluxo[0].nome == "intake"
    assert p14.DECLARACAO.fluxo[-1].nome == "ativação operacional posterior"


def test_grafia_da_fonte_preservada_entre_contratos():
    # P11 capitaliza os nomes de etapa; P12, P13 e P14 não. Não
    # normalizado [CLAUDE.md §7].
    assert p11.DECLARACAO.fluxo[4].nome == "Cartografia global"
    assert p12.DECLARACAO.fluxo[5].nome == "cartografia global"


def test_tres_etapas_de_selecao_do_p13():
    # P13 §43, etapas 8-10; §11, §12.
    nomes = [e.nome for e in p13.DECLARACAO.fluxo[7:10]]
    assert nomes == [
        "matriz de criticidade",
        "matriz de seletividade",
        "seleção de unidades comentáveis",
    ]


def test_matriz_de_aderencia_e_a_etapa_8_do_p12():
    assert p12.DECLARACAO.etapa(8).nome == "matriz de aderência"


def test_ordem_dura_do_p14_matriz_plano_revisao_carta():
    # Invariantes §3.43-45, verbatim: MATRIZ_PRECEDE_PLANO,
    # PLANO_PRECEDE_REVISAO, REVISAO_VERIFICADA_PRECEDE_CARTA.
    ordem = {e.nome: e.ordem for e in p14.DECLARACAO.fluxo}
    assert ordem["matriz de demandas"] < ordem["plano de incorporação"]
    assert ordem["plano de incorporação"] < ordem["revisão por unidade"]
    assert ordem["revisão por unidade"] < ordem["verificação de mudanças"]
    assert ordem["verificação de mudanças"] < ordem["elaboração da carta"]


# --- espinha E1-E7 (LAC-FUNC-008) ---


def test_etapas_de_governanca_ficam_sem_fase():
    # Decisão autoral, homologação, piloto e ativação são posteriores ao
    # pipeline; a espinha termina em E7.
    for modulo, primeira_sem_fase in ((p11, 23), (p12, 29), (p13, 26), (p14, 29)):
        for etapa in modulo.DECLARACAO.fluxo:
            if etapa.ordem >= primeira_sem_fase:
                assert etapa.fase is None, f"{modulo.__name__} etapa {etapa.ordem}"


def test_cartografia_global_precede_qualquer_diagnostico():
    # "do global para o local" [P11 §2]; nenhuma função opera em stream.
    for modulo in (p11, p12, p13):
        e3 = [e.ordem for e in modulo.DECLARACAO.fluxo if e.fase is FaseDaEspinha.E3_CARTOGRAFIA_GLOBAL]
        e4 = [e.ordem for e in modulo.DECLARACAO.fluxo if e.fase is FaseDaEspinha.E4_DIAGNOSTICO]
        assert e3 and e4
        assert max(e3) < min(e4), modulo.__name__


def test_p13_nao_tem_etapa_em_e5():
    # A seleção do P13 fecha dentro do diagnóstico; o P13 não produz
    # matriz nem plano no sentido do E5.
    assert [e for e in p13.DECLARACAO.fluxo if e.fase is FaseDaEspinha.E5_MATRIZ_OU_PLANO] == []


# --- ordens declaradas do P10 (LAC-FUNC-004) ---


def test_p10_registra_quatro_ordens_sem_fundi_las():
    ordens = p10.DECLARACAO.ordens_declaradas
    assert len(ordens) == 4
    assert [o.secao for o in ordens] == ["§2", "§4.4", "§21", "§31"]
    assert len({o.objeto for o in ordens}) == 4


def test_p10_sintese_funcional_verbatim():
    sintese = next(o for o in p10.DECLARACAO.ordens_declaradas if o.secao == "§4.4")
    assert sintese.itens == (
        "VAQUITA_ESTABILIZA",
        "BALEIA_DERIVA",
        "KOMODO_AVALIA",
        "USUARIO_DECIDE_E_HOMOLOGA",
    )


def test_p14_registra_a_ordem_de_execucao_do_43():
    ordens = p14.DECLARACAO.ordens_declaradas
    assert len(ordens) == 1
    assert ordens[0].secao == "§43"
    assert len(ordens[0].itens) == 10


# --- dependências e ativação ---


@pytest.mark.parametrize("modulo", (p10, p11, p12, p13, p14))
def test_as_cinco_dependem_de_p02_a_p09_e_nao_umas_das_outras(modulo):
    deps = modulo.DECLARACAO.dependencias_obrigatorias
    assert deps == ("P02", "P03", "P04", "P05", "P06", "P07", "P08", "P09")
    assert not {"P10", "P11", "P12", "P13", "P14"} & set(deps)


@pytest.mark.parametrize("modulo", (p10, p11, p12, p13, p14))
def test_condicao_de_ativacao_e_a_mesma_nos_cinco(modulo):
    assert modulo.DECLARACAO.condicao_de_ativacao == "APOS_HOMOLOGACAO_DAS_DEPENDENCIAS"


def test_encaminhamentos_so_existem_de_saida():
    # P11 §4.1/§4.8 → P10; P12 §4.2 → P10; P14 §4.4 → P13. Nenhuma regra
    # de entrada em contrato algum — LAC-FUNC-001.
    assert p11.DECLARACAO.encaminhamentos
    assert p12.DECLARACAO.encaminhamentos
    assert p14.DECLARACAO.encaminhamentos
    assert p10.DECLARACAO.encaminhamentos == ()
    assert p13.DECLARACAO.encaminhamentos == ()


def test_p13_nao_depende_de_p11_nem_p12():
    # §1 lista só P02-P09; o diagnóstico de origem é entrada condicional
    # (§6.1 item 12, "quando houver"; §6.2). O P13 pode operar sozinho.
    deps = p13.DECLARACAO.dependencias_obrigatorias
    assert "P11" not in deps and "P12" not in deps


def test_p14_nao_depende_de_p10():
    # §4.1 fala em "artigo já existente"; P10 não está entre as
    # dependências obrigatórias.
    assert "P10" not in p14.DECLARACAO.dependencias_obrigatorias


# --- X01 ---


def test_x01_nao_tem_fluxo_nem_componente():
    assert x01.DECLARACAO.fluxo == ()
    assert x01.DECLARACAO.component_id is None
    assert x01.DECLARACAO.funcao_id is FuncaoId.X01


def test_x01_nao_reimplementa_o_p05_nem_o_p04():
    # A função é implementada por escolio/ e escolio/bvaa/; este módulo é
    # só a declaração no catálogo.
    fonte = importlib.import_module("escolio.funcoes.x01")
    importados = [n for n in dir(fonte) if not n.startswith("_")]
    assert "RelacaoAfirmacaoEvidencia" not in importados
    assert "EstadoBibliografico" not in importados


# --- operações não enumeradas (LAC-FUNC-005) ---


@pytest.mark.parametrize("modulo", MODULOS)
def test_nenhuma_funcao_declara_operacoes_autorizadas(modulo):
    assert modulo.DECLARACAO.operacoes_autorizadas == frozenset()

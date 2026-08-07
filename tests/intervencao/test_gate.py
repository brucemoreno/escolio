from escolio.intervencao.gate import decidir_nivel, registro_de_abstencao
from escolio.intervencao.niveis import NivelIntervencao
from escolio.intervencao.vocabulario import Disposition


def test_nivel_pretendido_autorizado_procede_sem_regressao():
    decisao = decidir_nivel(
        NivelIntervencao.DIAGNOSTICO, frozenset({NivelIntervencao.DIAGNOSTICO})
    )
    assert decisao.nivel_autorizado == NivelIntervencao.DIAGNOSTICO
    assert decisao.houve_regressao is False


def test_gate_falho_regride_ao_nivel_maximo_autorizado():
    decisao = decidir_nivel(
        NivelIntervencao.REESCRITA,
        frozenset({NivelIntervencao.OBSERVACAO, NivelIntervencao.DIAGNOSTICO}),
    )
    assert decisao.nivel_autorizado == NivelIntervencao.DIAGNOSTICO
    assert decisao.houve_regressao is True


def test_gate_falho_sem_nivel_operativo_resulta_em_abstencao():
    decisao = decidir_nivel(NivelIntervencao.OBSERVACAO, frozenset())
    assert decisao.nivel_autorizado is None
    assert decisao.houve_regressao is True


def test_registro_de_abstencao_tem_disposition_abstained_e_applied_level_nulo():
    r = registro_de_abstencao(
        intervention_id="IR-0002",
        target_id="OBJ-2",
        nivel_pretendido=NivelIntervencao.REESCRITA,
        operation="reescrever seção",
        rationale="nenhum nível operativo permanece autorizado",
    )
    assert r.disposition == Disposition.ABSTAINED
    assert r.applied_level is None

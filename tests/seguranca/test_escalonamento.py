import pytest

from escolio.seguranca.erros import ErroDeEscalonamentoSemDestinatario, ErroDeSeguranca
from escolio.seguranca.escalonamento import (
    RegistroDeEscalonamento,
    bloqueia_operacao_insegura,
    continua_partes_seguras,
    escalona,
    monta_registro,
    preserva_objeto,
)


def registro_completo(**overrides):
    campos = dict(
        solicitante="ENGENHEIRO_LLM",
        origem="sessao-2026-08-08",
        papel="ENGENHEIRO_LLM",
        objeto="INP-0001",
        operacao="ANALISE",
        escopo="unidade UNI-001",
        nivel_de_intervencao="SINALIZACAO",
        fundamento="PI-07 instrução ambígua",
        dados_acessados=("UNI-001",),
        saida_permitida=False,
        data_ou_sequencia_logica="2026-08-08T00:00:00",
        decisao="AGUARDAR_AUTORIDADE",
        justificativa="ambiguidade não resolvida pela camada semântica",
        vinculo_com_evidencias=("UNI-001",),
    )
    campos.update(overrides)
    return monta_registro(**campos)


# --- Passos 1-4 executam por inteiro ---


def test_bloqueia_operacao_insegura_exige_motivo():
    with pytest.raises(ErroDeSeguranca):
        bloqueia_operacao_insegura("INP-0001", motivo="")


def test_bloqueia_operacao_insegura_com_motivo_nao_levanta():
    bloqueia_operacao_insegura("INP-0001", motivo="PI-07 ambíguo")  # não levanta


def test_preserva_objeto_devolve_par_inalterado():
    assert preserva_objeto("INP-0001", "acervo/x.pdf") == ("INP-0001", "acervo/x.pdf")


def test_continua_partes_seguras_devolve_tupla():
    assert continua_partes_seguras(["UNI-002", "UNI-003"]) == ("UNI-002", "UNI-003")


def test_monta_registro_produz_registro_com_todos_os_campos_de_p08_par9():
    r = registro_completo()
    assert isinstance(r, RegistroDeEscalonamento)
    assert r.solicitante == "ENGENHEIRO_LLM"
    assert r.objeto == "INP-0001"


# --- Passo 5: parar, sem destinatário — LAC-SEG-005 ---


def test_escalona_sempre_levanta_sem_destinatario():
    r = registro_completo()
    with pytest.raises(ErroDeEscalonamentoSemDestinatario):
        escalona(r)


def test_escalona_nao_aceita_parametro_de_destinatario():
    # A ausência do parâmetro é deliberada — confirmar que a assinatura
    # não aceita um destinatário "só para não travar".
    import inspect

    assinatura = inspect.signature(escalona)
    assert list(assinatura.parameters) == ["registro"]


def test_excecao_carrega_o_registro_completo_para_preservacao():
    r = registro_completo()
    with pytest.raises(ErroDeEscalonamentoSemDestinatario) as exc_info:
        escalona(r)
    assert exc_info.value.registro is r


def test_mensagem_da_excecao_cita_p08_par_5_6():
    r = registro_completo()
    with pytest.raises(ErroDeEscalonamentoSemDestinatario, match=r"P08 §5\.6"):
        escalona(r)

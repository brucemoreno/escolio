"""Testes da salvaguarda residual de privacidade (etapa 14, CO-012) —
`INSTRUCOES_COMPLEMENTARES_IMPLEMENTACAO_ECOSSISTEMA_REVISAO_LLM_R01.md §2`.
"""

from dataclasses import FrozenInstanceError

import pytest

from escolio.contrato.vocabulario import SensitivityCategory
from escolio.funcoes.salvaguarda_privacidade_p13 import (
    AlertaDePrivacidade,
    detectar_exposicao_manifesta,
)


class TestNuncaAcionaPorTema:
    """§2.1/§2.6 — violência, religião, doença, sexualidade, política não
    são privacidade; o detector não lê tema, só padrão literal."""

    @pytest.mark.parametrize(
        "texto",
        [
            "O relato descreve tortura e violência extrema durante o período de repressão.",
            "A doença sifilítica e suas complicações eram tratadas com mercúrio.",
            "A sexualidade feminina era regulada por normas religiosas rígidas.",
            "A perseguição política aos dissidentes marcou o período colonial.",
        ],
    )
    def test_tema_dificil_nao_aciona_alerta(self, texto):
        assert detectar_exposicao_manifesta("UNI-PAR-0001", texto) == []


class TestGatilhosDeterministicos:
    def test_cpf_formatado_aciona_alerta(self):
        alertas = detectar_exposicao_manifesta("UNI-PAR-0001", "Contato: 123.456.789-01, verificar.")
        assert len(alertas) == 1
        assert alertas[0].label.category is SensitivityCategory.PERSONAL_DATA
        valor = "123.456.789-01"
        assert valor not in alertas[0].trecho_mascarado
        assert alertas[0].trecho_mascarado == valor[0] + "*" * (len(valor) - 2) + valor[-1]

    def test_email_aciona_alerta(self):
        alertas = detectar_exposicao_manifesta("UNI-PAR-0001", "Enviar para joao.silva@example.com para revisão.")
        assert len(alertas) == 1
        assert "@" not in alertas[0].trecho_mascarado

    def test_telefone_com_ddd_aciona_alerta(self):
        alertas = detectar_exposicao_manifesta("UNI-PAR-0001", "Contato: (44) 99999-8888.")
        assert len(alertas) == 1

    def test_ano_de_citacao_nao_aciona_telefone(self):
        # "(1979)" não tem DDD nem dígitos suficientes — não deve casar.
        assert detectar_exposicao_manifesta("UNI-PAR-0001", "Grewe (1979, p. 13) descreve o caso.") == []

    def test_sem_gatilho_produz_lista_vazia(self):
        assert detectar_exposicao_manifesta("UNI-PAR-0001", "Texto acadêmico comum, sem dado pessoal.") == []

    def test_multiplos_gatilhos_no_mesmo_texto(self):
        texto = "CPF 123.456.789-01, e-mail a@b.com, tel (11) 91234-5678."
        alertas = detectar_exposicao_manifesta("UNI-PAR-0001", texto)
        assert len(alertas) == 3

    def test_unit_id_vazio_levanta(self):
        with pytest.raises(ValueError):
            detectar_exposicao_manifesta("", "123.456.789-01")


class TestMascaramentoNuncaReproduzValor:
    def test_trecho_mascarado_nunca_igual_ao_valor_original(self):
        alertas = detectar_exposicao_manifesta("UNI-PAR-0001", "123.456.789-01")
        assert alertas[0].trecho_mascarado != "123.456.789-01"

    def test_alerta_e_dataclass_frozen(self):
        alertas = detectar_exposicao_manifesta("UNI-PAR-0001", "123.456.789-01")
        with pytest.raises(FrozenInstanceError):
            alertas[0].posicao = 99
        assert isinstance(alertas[0], AlertaDePrivacidade)

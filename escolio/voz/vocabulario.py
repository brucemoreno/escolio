"""Vocabulário controlado do perfil de voz autoral — fonte:
01_CONTRATO_UNIVERSAL_DE_VOZ_AUTORAL_P07_R01.md; 02_SCHEMA_DE_PERFIL_DE_VOZ_AUTORAL_P07_R01.json.

ESCOPO DESTA PEÇA: apenas o perfil de voz do autor avaliado — a voz a
preservar no texto sob revisão [P07/01, Finalidade; P13 §6.2, §11]. O
perfil de quem comenta (o corretor) é lacuna aberta e não incorporada
aqui — ver CLAUDE.md §13.1 e docs/spec/divergencias.md §4.1. Onde o texto
fonte enuncia um princípio em termos universais ("imitação de pessoa real
é substituída por atributos abstratos"), este módulo o implementa apenas
para o lado autor avaliado; nenhuma extensão ao lado do corretor foi
inferida.

`Confidence` aqui é vocabulário próprio de P07 (BAIXA|MEDIA|ALTA|
NAO_APLICAVEL, arquivo 02, campo `confidence`), distinto de
`escolio.vocabulario.Confidence` (P05: sem NAO_APLICAVEL) e de
`escolio.contrato.vocabulario.Confidence` (P09: HIGH|MEDIUM|LOW|
UNDETERMINED). Mesma disciplina dada a CON-P05-001: nenhum dos três é
alias do outro — ver escolio/voz/LACUNAS.md.
"""

from enum import Enum

ARQUIVO_CONTRATO = "01_CONTRATO_UNIVERSAL_DE_VOZ_AUTORAL_P07_R01.md"
ARQUIVO_SCHEMA = "02_SCHEMA_DE_PERFIL_DE_VOZ_AUTORAL_P07_R01.json"


class TipoDePerfil(str, Enum):
    """Perfis mínimos [contrato §Perfis mínimos; schema `profile_type`]."""

    PERFIL_NEUTRO_ACADEMICO_CONTROLADO = "PERFIL_NEUTRO_ACADEMICO_CONTROLADO"
    PERFIL_AUTORAL_DERIVADO_DE_AMOSTRAS = "PERFIL_AUTORAL_DERIVADO_DE_AMOSTRAS"
    PERFIL_AUTORAL_DECLARADO_PELO_USUARIO = "PERFIL_AUTORAL_DECLARADO_PELO_USUARIO"
    PERFIL_HIBRIDO_DECLARACAO_MAIS_AMOSTRAS = "PERFIL_HIBRIDO_DECLARACAO_MAIS_AMOSTRAS"
    PERFIL_LOCAL_POR_GENERO_OU_SECAO = "PERFIL_LOCAL_POR_GENERO_OU_SECAO"
    PERFIL_INSUFICIENTE_OU_CONFLITANTE = "PERFIL_INSUFICIENTE_OU_CONFLITANTE"


class Confidence(str, Enum):
    """Schema §confidence: "BAIXA, MEDIA, ALTA ou NAO_APLICAVEL, sempre
    justificada por evidência"."""

    BAIXA = "BAIXA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    NAO_APLICAVEL = "NAO_APLICAVEL"


class StatusDePerfil(str, Enum):
    """Schema `status`."""

    RASCUNHO = "RASCUNHO"
    VALIDACAO_PENDENTE = "VALIDACAO_PENDENTE"
    VALIDADO = "VALIDADO"
    HOMOLOGADO = "HOMOLOGADO"
    ABSTENCAO = "ABSTENCAO"


class GateDePerfil(str, Enum):
    """Gate por perfil — fonte: 04_MATRIZ_DE_PERFIS_FONTES_CONFIANCA_E_AUTORIDADE_P07_R01.csv,
    coluna `gate`."""

    GATE_NEUTRO = "GATE_NEUTRO"
    GATE_AMOSTRAS = "GATE_AMOSTRAS"
    GATE_DECLARACAO = "GATE_DECLARACAO"
    GATE_HIBRIDO = "GATE_HIBRIDO"
    GATE_LOCAL = "GATE_LOCAL"
    GATE_ABSTENCAO = "GATE_ABSTENCAO"


# Matriz de fontes/confiança/autoridade/gate por perfil — fonte: arquivo 04,
# uma linha por perfil, na ordem exata do CSV.
GATE_POR_PERFIL: dict[TipoDePerfil, GateDePerfil] = {
    TipoDePerfil.PERFIL_NEUTRO_ACADEMICO_CONTROLADO: GateDePerfil.GATE_NEUTRO,
    TipoDePerfil.PERFIL_AUTORAL_DERIVADO_DE_AMOSTRAS: GateDePerfil.GATE_AMOSTRAS,
    TipoDePerfil.PERFIL_AUTORAL_DECLARADO_PELO_USUARIO: GateDePerfil.GATE_DECLARACAO,
    TipoDePerfil.PERFIL_HIBRIDO_DECLARACAO_MAIS_AMOSTRAS: GateDePerfil.GATE_HIBRIDO,
    TipoDePerfil.PERFIL_LOCAL_POR_GENERO_OU_SECAO: GateDePerfil.GATE_LOCAL,
    TipoDePerfil.PERFIL_INSUFICIENTE_OU_CONFLITANTE: GateDePerfil.GATE_ABSTENCAO,
}


class ResultadoDeFidelidade(str, Enum):
    """Resultados da avaliação de fidelidade autoral — fonte:
    06_PROTOCOLO_DE_AVALIACAO_DE_FIDELIDADE_AUTORAL_P07_R01.txt, linha
    RESULTADOS."""

    CONFORME = "CONFORME"
    CONFORME_COM_RESSALVAS = "CONFORME_COM_RESSALVAS"
    CORRIGIR_ANTES_DE_AVANCAR = "CORRIGIR_ANTES_DE_AVANCAR"
    BLOQUEAR = "BLOQUEAR"
    ABSTER_SE = "ABSTER_SE"


class DesvioBloqueante(str, Enum):
    """Desvios bloqueantes — fonte: 06_PROTOCOLO..., linha DESVIOS
    BLOQUEANTES."""

    INVENCAO_FACTUAL = "INVENCAO_FACTUAL"
    ALTERACAO_DE_SENTIDO = "ALTERACAO_DE_SENTIDO"
    PERDA_DE_DENSIDADE = "PERDA_DE_DENSIDADE"
    APAGAMENTO_DE_NUANCE = "APAGAMENTO_DE_NUANCE"
    MUDANCA_DE_PESSOA_SEM_AUTORIZACAO = "MUDANCA_DE_PESSOA_SEM_AUTORIZACAO"
    COPIA_OU_IMITACAO = "COPIA_OU_IMITACAO"
    ALTERACAO_FORTE_SEM_GATE = "ALTERACAO_FORTE_SEM_GATE"
    AUSENCIA_DE_PROVENIENCIA = "AUSENCIA_DE_PROVENIENCIA"

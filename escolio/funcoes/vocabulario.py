"""Vocabulário controlado do roteador — fontes: P02 (catálogo funcional),
P10-P14 (rótulos de classe de gate), CLAUDE.md §4 (espinha, [PROPOSTA]).

`FuncaoId` usa os identificadores do P02, que é o catálogo funcional; os
`P10…P14` da R03 são identificadores de *componente*, e vivem em
`catalogo.py`. Manter os dois namespaces separados é o que dá conteúdo à
regra P09 §4.2.4 ("function_id deve pertencer ao component_id") — se
fossem o mesmo rótulo, a regra seria tautológica. Escolha marcada
[PROPOSTA]; ver LACUNAS.md, LAC-FUNC-002.

`ClasseDeGate` NÃO unifica os rótulos dos cinco contratos. P10 escreve
"validação documental" onde P13 e P14 escrevem "documentais"; P11 e P12
escrevem "decisão humana expressa" onde P13 escreve "humanos expressos" e
P14 escreve "humanos obrigatórios". Nenhuma fonte declara que sejam
sinônimos. Mesma disciplina dada a CON-P05-001: os sete rótulos distintos
coexistem, cada módulo usa o do seu contrato, nenhum é alias do outro
[CLAUDE.md §7: "não colapsar dois vocabulários em um"]. Ver LAC-FUNC-006.
"""

from enum import Enum

ARQUIVO_P02 = "02_CATALOGO_FUNCIONAL_CONSOLIDADO_P02_R01.md"
ARQUIVO_R03 = "01_PROTOCOLO_MESTRE_DE_ACAO_ECOSSISTEMA_LLM_ACADEMICA_R03.md"


class FuncaoId(str, Enum):
    """As seis unidades funcionais do P02 — cinco macrofunções e um
    requisito transversal. Catálogo fechado: "Não há base material para
    ampliar esse conjunto neste componente" [P02 §1]; ampliar exige nova
    fonte e decisão autoral específica [LAC-P02-005]."""

    F01 = "LLM-ACA-F01"
    """Derivação editorial de capítulo de tese ou dissertação em dois manuscritos de artigo."""

    F02 = "LLM-ACA-F02"
    """Revisão e correção de dissertação ou tese."""

    F03 = "LLM-ACA-F03"
    """Revisão de relatório de iniciação científica."""

    F04 = "LLM-ACA-F04"
    """Revisão em comentários Word."""

    F05 = "LLM-ACA-F05"
    """Incorporação de pareceres em artigo."""

    X01 = "LLM-ACA-X01"
    """Gestão transversal de fontes, citações e evidências."""


class ClasseDeGate(str, Enum):
    """Rótulos de classe de gate, verbatim de cada contrato. Sete rótulos,
    não três: os contratos não usam a mesma nomenclatura e nenhum declara
    equivalência entre elas."""

    AUTOMATICAMENTE_VERIFICAVEL = "AUTOMATICAMENTE_VERIFICAVEL"
    """[P10 §29.1] "Gates automaticamente verificáveis". Única classe que
    não nomeia gate algum na fonte — §29.1 lista itens conferíveis, não
    gates. Nenhum outro contrato tem esta classe."""

    VALIDACAO_DOCUMENTAL = "VALIDACAO_DOCUMENTAL"
    """[P10 §29.3] "Gates com validação documental"; [P11 §28.1] "Gates de
    validação documental"; [P12 §31.1] idem."""

    DOCUMENTAL = "DOCUMENTAL"
    """[P13 §32.1] "Gates documentais"; [P14 §41.1] idem."""

    DECISAO_HUMANA_EXPRESSA = "DECISAO_HUMANA_EXPRESSA"
    """[P10 §29.2] "Gates com decisão humana expressa"; [P11 §28.2] "Gates
    de decisão humana expressa"; [P12 §31.2] idem."""

    HUMANO_EXPRESSO = "HUMANO_EXPRESSO"
    """[P13 §32.2] "Gates humanos expressos"."""

    HUMANO_OBRIGATORIO = "HUMANO_OBRIGATORIO"
    """[P14 §41.2] "Gates humanos obrigatórios"."""

    HUMANO_ADICIONAL_COMPATIVEL = "HUMANO_ADICIONAL_COMPATIVEL"
    """[P14 §41.3] "Gates humanos adicionais compatíveis". Sem equivalente
    nos outros quatro contratos."""


class FaseDaEspinha(str, Enum):
    """As sete fases de CLAUDE.md §4. O agrupamento é [PROPOSTA]; os nomes
    e a ordem das etapas são de cada contrato.

    A fase é anotação por etapa, declarada dentro do módulo de cada função.
    Nenhum código percorre fases: percorrer seria fundir execução, e "a
    espinha nomeia fases; não funde execução" [CLAUDE.md §4]. Onde a etapa
    de um contrato não corresponde a nenhuma fase, o campo é None — não se
    força correspondência. Ver LAC-FUNC-008."""

    E1_INTAKE_E_AUTORIDADE = "E1"
    E2_INGESTAO_CONTROLADA = "E2"
    E3_CARTOGRAFIA_GLOBAL = "E3"
    E4_DIAGNOSTICO = "E4"
    E5_MATRIZ_OU_PLANO = "E5"
    E6_EXECUCAO_MODULAR = "E6"
    E7_CONSOLIDACAO_E_AUDITORIA = "E7"

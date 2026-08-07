"""Catálogo fechado das seis unidades funcionais e a correspondência entre
os dois namespaces de identificador.

Fontes: P02 (`LLM-ACA-F01…F05`, `LLM-ACA-X01`) e o inventário canônico da
R03 (`P10…P14`, camada FUNCAO).

CORRESPONDÊNCIA F0x ↔ P1x — [PROPOSTA]. Nenhuma fonte a escreve. O token
`LLM-ACA-F0*` aparece exclusivamente em artefatos do P02; jamais nos
contratos P10-P14, no inventário da R03 ou no P09. A correspondência é
legível pela finalidade declarada de cada par, e só por isso. Está aqui
como tabela consultável e documentada, no padrão de
`escolio/bvaa/correspondencia.py`: documentação, não tradução silenciosa.
Ver LACUNAS.md, LAC-FUNC-002.

CATÁLOGO FECHADO. "Foram localizadas cinco macrofunções e um requisito
transversal. Não há base material para ampliar esse conjunto neste
componente" [P02 §1]. Ampliar exige nova fonte e decisão autoral
específica [LAC-P02-005]. Acrescentar membro a este módulo é ato de
governança, não de programação.
"""

from escolio.funcoes import p10, p11, p12, p13, p14, x01
from escolio.funcoes.declaracao import DeclaracaoDeFuncao
from escolio.funcoes.erros import ARQUIVO_P02, ErroDeRoteamento
from escolio.funcoes.vocabulario import FuncaoId

ARQUIVO_R03_INVENTARIO = "02_INVENTARIO_DE_COMPONENTES_E_PACOTES_A_PRODUZIR_R03.csv"

CATALOGO: dict[FuncaoId, DeclaracaoDeFuncao] = {
    FuncaoId.F01: p10.DECLARACAO,
    FuncaoId.F02: p11.DECLARACAO,
    FuncaoId.F03: p12.DECLARACAO,
    FuncaoId.F04: p13.DECLARACAO,
    FuncaoId.F05: p14.DECLARACAO,
    FuncaoId.X01: x01.DECLARACAO,
}

# Só as cinco macrofunções têm componente numerado na R03. O X01 não é
# componente do inventário — é o item 6 da CAMADA B, sem P-número.
COMPONENTE_POR_FUNCAO: dict[FuncaoId, str | None] = {
    FuncaoId.F01: "P10",
    FuncaoId.F02: "P11",
    FuncaoId.F03: "P12",
    FuncaoId.F04: "P13",
    FuncaoId.F05: "P14",
    FuncaoId.X01: None,
}


def declaracao_de(funcao_id: FuncaoId) -> DeclaracaoDeFuncao:
    """A declaração da função. `FuncaoId` já garante pertencimento ao
    catálogo; esta função existe para não expor o dicionário mutável."""
    return CATALOGO[funcao_id]


def funcao_de(valor: str) -> FuncaoId:
    """Converte um `request.function_id` cru no membro do catálogo.

    P09 §4.2.6: "`function_id` desconhecido não pode ser aceito por
    inferência." Nada de correspondência aproximada, normalização de caixa
    ou tentativa de casar por prefixo — valor fora do catálogo levanta."""
    try:
        return FuncaoId(valor)
    except ValueError:
        raise ErroDeRoteamento(
            "P09-§4.2.6",
            "function_id desconhecido não pode ser aceito por inferência",
            arquivo_origem=ARQUIVO_P02,
            detalhe=(
                f"'{valor}' não pertence ao catálogo fechado de seis unidades funcionais "
                f"{sorted(f.value for f in FuncaoId)}; ampliar exige nova fonte e decisão "
                "autoral específica [LAC-P02-005]"
            ),
        ) from None

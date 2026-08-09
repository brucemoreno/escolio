"""Catálogo dos 15 tipos de comentário e templates estruturais — fonte:
P13 §13 (catálogo), §15-18 (comentário linguístico, estrutural,
argumentativo, metodológico).

Sessão 3 do plano (`docs/spec/plano-P13.md`). Escopo desta sessão: só os
quatro templates de §15-18. Os demais tipos do catálogo (`ALERTA_DE_EVIDENCIA`
[§20], `ALERTA_BIBLIOGRAFICO` [§19], `ALERTA_DE_VOZ` [§21],
`ALERTA_DE_PRIVACIDADE` [§22], `COMENTARIO_MATRIZ`/`REMISSAO_A_COMENTARIO_MATRIZ`
[§23]) têm template definido em seções fora de §15-18 e pertencem às
sessões 4, 5, 6 e à sessão adiada — ver `escolio/comentarios/LACUNAS.md`.
`GATE_HUMANO`, `DECISAO_PENDENTE`, `DIAGNOSTICO`, `CORRECAO_LOCAL`,
`SUGESTAO` e `PERGUNTA_ORIENTADORA` não têm template estrutural declarado
em nenhuma seção da fonte — catalogados aqui, sem validador de template.

`CommentType` reusa os dois literais já citados por
`escolio.comentarios.vocabulario` (`COMMENT_TYPE_REMISSAO_A_COMENTARIO_MATRIZ`,
`COMMENT_TYPE_COMENTARIO_MATRIZ`) — mesmo valor string, não duplicação de
enum. `P13Comment.comment_type` (sessão 1, `comentario.py`) permanece `str`
nesta sessão: retipá-lo para `CommentType` é integração que não foi pedida
aqui e alteraria código existente — ver LACUNAS.md.
"""

from dataclasses import dataclass
from enum import Enum

from escolio.comentarios.erros import ErroDeComentario
from escolio.comentarios.vocabulario import (
    COMMENT_TYPE_COMENTARIO_MATRIZ,
    COMMENT_TYPE_REMISSAO_A_COMENTARIO_MATRIZ,
)

ARQUIVO_FONTE = "P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md"


class CommentType(str, Enum):
    """Os 15 tipos funcionais de comentário [§13], nesta ordem literal."""

    DIAGNOSTICO = "DIAGNOSTICO"
    CORRECAO_LOCAL = "CORRECAO_LOCAL"
    SUGESTAO = "SUGESTAO"
    PERGUNTA_ORIENTADORA = "PERGUNTA_ORIENTADORA"
    ALERTA_DE_EVIDENCIA = "ALERTA_DE_EVIDENCIA"
    ALERTA_BIBLIOGRAFICO = "ALERTA_BIBLIOGRAFICO"
    ALERTA_METODOLOGICO = "ALERTA_METODOLOGICO"
    ALERTA_ESTRUTURAL = "ALERTA_ESTRUTURAL"
    ALERTA_ARGUMENTATIVO = "ALERTA_ARGUMENTATIVO"
    ALERTA_DE_VOZ = "ALERTA_DE_VOZ"
    ALERTA_DE_PRIVACIDADE = "ALERTA_DE_PRIVACIDADE"
    GATE_HUMANO = "GATE_HUMANO"
    DECISAO_PENDENTE = "DECISAO_PENDENTE"
    COMENTARIO_MATRIZ = "COMENTARIO_MATRIZ"
    REMISSAO_A_COMENTARIO_MATRIZ = "REMISSAO_A_COMENTARIO_MATRIZ"


assert CommentType.COMENTARIO_MATRIZ.value == COMMENT_TYPE_COMENTARIO_MATRIZ
assert CommentType.REMISSAO_A_COMENTARIO_MATRIZ.value == COMMENT_TYPE_REMISSAO_A_COMENTARIO_MATRIZ


def _exige_nao_vazio(regra_id: str, nome_campo: str, valor: str) -> None:
    if valor is None or (isinstance(valor, str) and valor.strip() == ""):
        raise ErroDeComentario(
            regra_id,
            f"Campo obrigatório '{nome_campo}' vazio no template estrutural ({regra_id})",
        )


# --- §15 — Comentário linguístico ------------------------------------
#
# Nenhum dos 15 comment_type de §13 corresponde textualmente a "comentário
# linguístico": não existe ALERTA_LINGUISTICO nem COMENTARIO_LINGUISTICO no
# catálogo. `TemplateComentarioLinguistico` valida a estrutura de §15 sem
# vinculá-la a um `CommentType` — associar por analogia a DIAGNOSTICO ou
# CORRECAO_LOCAL seria inferência; ver LACUNAS.md.

EFEITO_LINGUISTICO_MATERIAL = frozenset(
    {
        "SENTIDO",
        "PRECISAO",
        "COERENCIA",
        "ARGUMENTO",
        "EVIDENCIA",
        "VOZ",
        "AMBIGUIDADE_MATERIAL",
        "NORMA_INSTITUCIONAL_MATERIALMENTE_APLICAVEL",
        "INTERPRETACAO_DE_CITACAO",
        "GRAU_DE_CERTEZA",
        "RELACAO_LOGICA",
    }
)

# §15 — "Não deve ser gerado para": lista literal de motivos cosméticos.
EFEITO_LINGUISTICO_COSMETICO = frozenset(
    {
        "TROCA_SINONIMICA_COSMETICA",
        "PREFERENCIA_ESTILISTICA",
        "MICROAJUSTE_SEM_IMPACTO",
        "PONTUACAO_FACILMENTE_CORRIGIVEL_SEM_DECISAO",
        "NORMALIZACAO_AUTOMATICA",
        "REPETICAO_COBERTA_POR_COMENTARIO_MATRIZ",
        "DEMONSTRACAO_DE_LEITURA",
    }
)


@dataclass
class TemplateComentarioLinguistico:
    """Estrutura funcional de §15: Problema / Evidência / Impacto / Ação
    possível, mais o efeito linguístico que justifica o comentário."""

    problem: str
    evidence: str
    impact: str
    recommended_action: str
    efeito: str

    def __post_init__(self) -> None:
        for campo in ("problem", "evidence", "impact", "recommended_action"):
            _exige_nao_vazio("15", campo, getattr(self, campo))
        if self.efeito in EFEITO_LINGUISTICO_COSMETICO:
            raise ErroDeComentario(
                "15",
                "comentário linguístico não deve ser gerado para efeito cosmético",
                detalhe=self.efeito,
            )
        if self.efeito not in EFEITO_LINGUISTICO_MATERIAL:
            raise ErroDeComentario(
                "15",
                "efeito linguístico não reconhecido entre os motivos materiais do §15",
                detalhe=self.efeito,
            )


# --- §16 — Comentário estrutural (ALERTA_ESTRUTURAL) ------------------

_CAMPOS_ESTRUTURAL = (
    "funcao_esperada",
    "posicao_atual",
    "impacto",
    "alternativa_possivel",
    "nivel_de_intervencao",
    "gate_aplicavel",
)


@dataclass
class TemplateAlertaEstrutural:
    """Os seis itens que §16 exige que o comentário estrutural indique."""

    funcao_esperada: str
    posicao_atual: str
    impacto: str
    alternativa_possivel: str
    nivel_de_intervencao: str
    gate_aplicavel: str
    realocacao_executada: bool = False

    def __post_init__(self) -> None:
        for campo in _CAMPOS_ESTRUTURAL:
            _exige_nao_vazio("16", campo, getattr(self, campo))
        if self.realocacao_executada:
            raise ErroDeComentario(
                "16", "comentário estrutural não deve executar realocação"
            )


# --- §17 — Comentário argumentativo (ALERTA_ARGUMENTATIVO) ------------

_CAMPOS_ARGUMENTATIVO = (
    "afirmacao",
    "evidencia",
    "inferencia",
    "limitacao",
    "impacto",
    "acao_possivel",
)


@dataclass
class TemplateAlertaArgumentativo:
    """Os seis elementos que §17 exige que o comentário argumentativo
    distinga: afirmação, evidência, inferência, limitação, impacto, ação
    possível."""

    afirmacao: str
    evidencia: str
    inferencia: str
    limitacao: str
    impacto: str
    acao_possivel: str
    solucao_factual_inventada: bool = False

    def __post_init__(self) -> None:
        for campo in _CAMPOS_ARGUMENTATIVO:
            _exige_nao_vazio("17", campo, getattr(self, campo))
        if self.solucao_factual_inventada:
            raise ErroDeComentario(
                "3",
                "comentário não pode inventar solução factual [invariante 21, §3]",
            )


# --- §18 — Comentário metodológico (ALERTA_METODOLOGICO) --------------
#
# §18 não declara lista de campos ("deve conter"/"deve indicar") como
# §16/§17 — só as oito condições de aplicabilidade e a disjunção fechada
# "pode indicar decisão necessária ou solicitar explicitação". Inventar
# campos de template (ex.: "problem", "recommended_action" livres) além do
# que a fonte declara seria a mesma inferência que LACUNAS.md já recusa
# para os outros nove fatores de MatrizSeletividade — por isso o template
# aqui só tipa o que §18 de fato enumera.


class CondicaoMetodologica(str, Enum):
    """As oito condições de aplicabilidade do comentário metodológico [§18]."""

    METODO_NAO_EXPLICITADO = "METODO_NAO_EXPLICITADO"
    PROCEDIMENTO_INCOMPATIVEL_COM_OBJETIVO = "PROCEDIMENTO_INCOMPATIVEL_COM_OBJETIVO"
    CORPUS_NAO_SUSTENTA_A_OPERACAO = "CORPUS_NAO_SUSTENTA_A_OPERACAO"
    CATEGORIA_ANALITICA_NAO_DEFINIDA = "CATEGORIA_ANALITICA_NAO_DEFINIDA"
    SELECAO_DE_FONTES_NAO_JUSTIFICADA = "SELECAO_DE_FONTES_NAO_JUSTIFICADA"
    LIMITACAO_METODOLOGICA_NAO_DECLARADA = "LIMITACAO_METODOLOGICA_NAO_DECLARADA"
    METODO_DESCRITO_NAO_CORRESPONDE_AO_REALIZADO = "METODO_DESCRITO_NAO_CORRESPONDE_AO_REALIZADO"
    INFERENCIA_EXCEDE_A_OPERACAO = "INFERENCIA_EXCEDE_A_OPERACAO"


class AcaoMetodologica(str, Enum):
    """A disjunção fechada de §18: "pode indicar decisão necessária ou
    solicitar explicitação"."""

    DECISAO_NECESSARIA = "DECISAO_NECESSARIA"
    SOLICITAR_EXPLICITACAO = "SOLICITAR_EXPLICITACAO"


@dataclass
class TemplateAlertaMetodologico:
    condicao: CondicaoMetodologica
    acao: AcaoMetodologica
    metodo_substitutivo_proposto: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.condicao, CondicaoMetodologica):
            raise ErroDeComentario(
                "18",
                "condicao deve ser um membro de CondicaoMetodologica",
                detalhe=repr(self.condicao),
            )
        if not isinstance(self.acao, AcaoMetodologica):
            raise ErroDeComentario(
                "18",
                "acao deve ser um membro de AcaoMetodologica",
                detalhe=repr(self.acao),
            )
        if (
            self.metodo_substitutivo_proposto is not None
            and self.metodo_substitutivo_proposto.strip() != ""
        ):
            raise ErroDeComentario(
                "18", "comentário metodológico não deve inventar método substitutivo"
            )


# --- Validador por comment_type ---------------------------------------

_TEMPLATE_POR_TIPO = {
    CommentType.ALERTA_ESTRUTURAL: TemplateAlertaEstrutural,
    CommentType.ALERTA_ARGUMENTATIVO: TemplateAlertaArgumentativo,
    CommentType.ALERTA_METODOLOGICO: TemplateAlertaMetodologico,
}


def valida_template_por_tipo(comment_type: CommentType, template: object) -> None:
    """Confere que `template` é a estrutura correta para `comment_type`,
    entre os tipos cujo template estrutural esta sessão implementa (§16,
    §17, §18). Para qualquer outro `CommentType` — incluindo os cobertos
    por seções fora de §15-18 e os sem template declarado — não há
    template desta sessão; ver LACUNAS.md."""
    if not isinstance(comment_type, CommentType):
        raise ErroDeComentario(
            "13", "comment_type deve ser um membro de CommentType", detalhe=repr(comment_type)
        )
    classe_esperada = _TEMPLATE_POR_TIPO.get(comment_type)
    if classe_esperada is None:
        raise ErroDeComentario(
            "13",
            f"Nenhum template estrutural desta sessão está definido para comment_type={comment_type.value}",
            detalhe="templates de §15-18 apenas; ver LACUNAS.md",
        )
    if not isinstance(template, classe_esperada):
        raise ErroDeComentario(
            "13",
            "template incompatível com comment_type",
            detalhe=f"esperado {classe_esperada.__name__} para {comment_type.value}, recebido {type(template).__name__}",
        )

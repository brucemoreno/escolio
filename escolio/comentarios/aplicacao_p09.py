"""Extensão do envelope P09 para o P13 — fonte:
`P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md` §31.1-31.4
(status/categorias canônicos, extensão de entrada, extensão de resultado) e
§31.6 (regra de payloads), com o exemplo canônico de §29 (ABSTAINED por
perfil de voz insuficiente). Sessão 8 de `docs/spec/plano-P13.md`.

Reusa `escolio.contrato.*` (peça 1: `Response`, `Result`, `SafeResult`,
`AbstentionPayload`, `BlockPayload`, `ErrorPayload`, `Reference`,
`AbstentionCategory`, `ResponseStatus`) e `escolio.comentarios.comentario.
P13Comment` (sessão 1) sem duplicar enum nem validação. Nenhum arquivo
existente foi alterado.

§31.1 (status canônicos) e §31.2 (categorias de abstenção) não geram código
novo aqui: são exatamente `escolio.contrato.vocabulario.ResponseStatus` e
`AbstentionCategory`, já implementados na peça 1 com os mesmos cinco e nove
valores, nesta mesma ordem. Reafirmar os dois enums neste módulo seria
duplicação, não extensão.

Este módulo **não corrige** `BL-011` (`exige_correspondencia_request_response`
não confere `function_id`) nem `BL-013` (`Response.interventions` desligado)
como efeito colateral — são pendências das peças 1 e 2 (`docs/backlog.md`),
e o P13 as herda tal como estão: os builders abaixo fixam
`function_id="P13"` mas não implementam a correspondência que falta, e
nenhum `InterventionRecord` é anexado a `Response` aqui.
"""

from dataclasses import dataclass, field

from escolio.comentarios.aplicacao_p06_p07 import P13_CAUSE_VOICE_PROFILE_INSUFFICIENT
from escolio.comentarios.comentario import P13Comment
from escolio.comentarios.erros import ErroDeComentario
from escolio.contrato.payloads import AbstentionPayload, BlockPayload, ErrorPayload
from escolio.contrato.referencia import Reference, SemanticVersion
from escolio.contrato.resposta import Response, Result, SafeResult
from escolio.contrato.vocabulario import AbstentionCategory, ResponseStatus

ARQUIVO_FONTE = "P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md"


def _exige_nao_vazio(regra_id: str, nome_campo: str, valor) -> None:
    if valor is None or (isinstance(valor, str) and valor.strip() == ""):
        raise ErroDeComentario(
            regra_id, f"Campo obrigatório '{nome_campo}' vazio ({regra_id})", ARQUIVO_FONTE
        )


# --- §31.3 — Extensão de entrada ---------------------------------------

_CAMPOS_STR_OBRIGATORIOS_REQUEST = (
    "document_id",
    "document_version",
    "document_type",
    "requested_operation",
    "comment_purpose",
    "authorized_intervention_level",
    "formative_level",
    "privacy_classification",
)


@dataclass
class P13RequestExtension:
    """§31.3 — extensão de entrada própria do P13.

    Ordem dos campos abaixo difere da ordem literal de §31.3: Python exige
    que campos com valor padrão venham depois dos campos sem valor padrão, e
    só `global_document_reference` e `voice_profile_reference` são
    anotados `X | null` na fonte — os dois, mais os quatro campos-lista
    (`[Reference]`, sem regra de obrigatoriedade declarada em §31.3), foram
    movidos para o final sem alterar seu significado. Mesmo tratamento dado
    a `P13Comment` (sessão 1, `comentario.py`) e a `Scope`/`Constraints`
    (`escolio/contrato/requisicao.py`, campos-lista opcionais por padrão).

    `authorized_intervention_level` permanece `str` — a fonte tipa o campo
    como `string`, não como referência ao enum `NivelIntervencao`; retipar
    seria a mesma inferência já recusada para `P13Comment.intervention_level`
    (sessão 1). A validação de que o nível está entre os cinco permitidos ao
    P13 [§4.4] já existe em `escolio.comentarios.aplicacao_p06_p07.
    valida_intervention_level_permitido` e não é duplicada aqui.

    `privacy_classification` é campo de forma desta extensão, não a lógica
    de classificação — a sessão de privacidade (integração P08) permanece
    adiada [`docs/spec/plano-P13.md`, "Sessão adiada"]; só a forma é
    definida, mesma instrução aplicada a `privacy_warnings` em
    `P13ResultExtension`.
    """

    document_id: str
    document_version: str
    document_type: str
    requested_operation: str
    comment_purpose: str
    authorized_intervention_level: str
    formative_level: str
    privacy_classification: str
    authorized_units: list[Reference] = field(default_factory=list)
    global_document_reference: Reference | None = None
    source_references: list[Reference] = field(default_factory=list)
    prior_diagnostic_references: list[Reference] = field(default_factory=list)
    voice_profile_reference: Reference | None = None
    excluded_units: list[Reference] = field(default_factory=list)

    def __post_init__(self) -> None:
        for campo in _CAMPOS_STR_OBRIGATORIOS_REQUEST:
            _exige_nao_vazio("31.3", campo, getattr(self, campo))


# --- §31.4 — Extensão de resultado --------------------------------------


@dataclass
class P13ResultExtension:
    """§31.4 — extensão de resultado própria do P13.

    `global_cartography`, `criticality_matrix`, `selectivity_matrix` e
    `density_justification` são `any | null` na fonte — mantidos
    `object | None`, mesma leitura aberta dada a `Result.content` e
    `ResultItem.content` (`escolio/contrato/resposta.py`), sustentada por
    P09 §25 ("linguagem concreta de schema é lacuna legítima, pertencente à
    implementação posterior").

    `matrix_referrals: [P13CommentReferral]` e `units_without_comment:
    [UnitDecision]` citam dois tipos que não têm NENHUMA definição em
    nenhuma seção do contrato P13 — confirmado por busca no arquivo-fonte
    completo: nenhuma outra ocorrência de nenhum dos dois nomes, em seção
    alguma. Diferente de `ResultItem` (P09 §8), cuja abertura tem licença
    explícita da própria fonte (P09 §25), aqui não há frase equivalente
    autorizando a abertura — mas também não há nenhuma outra frase que
    declare os campos desses dois tipos. Inventar um schema de campos para
    qualquer um dos dois seria a mesma inferência já recusada para
    `authority_required` (sessão 5, `aplicacao_p06_p07.py`) e para os nove
    fatores sem tipo de `MatrizSeletividade` (sessão 2). Os dois campos
    permanecem `list[object]` — mesmo tratamento dado aos `[any]`
    genuinamente abertos de §31.4 (`source_pending_items`,
    `evidence_pending_items`, `voice_warnings`, `p13_traceability`,
    `limitations`). Ver LACUNAS.md.

    `comments`/`matrix_comments` reusam `P13Comment` (sessão 1) sem
    duplicar; nenhuma regra nova de associação comentário-matriz é
    verificada aqui — quem já registra isso é `RegistroDeComentarios`
    (sessão 1) e `registrar_comentario_matriz_e_remissoes` (sessão 6).

    `privacy_warnings` é definido só na forma (`list[object]`, vazio por
    padrão) — sem lógica que o preenche, por instrução desta sessão; a
    integração P08 permanece adiada.
    """

    current_p13_state: str
    comments: list[P13Comment] = field(default_factory=list)
    matrix_comments: list[P13Comment] = field(default_factory=list)
    matrix_referrals: list[object] = field(default_factory=list)
    units_without_comment: list[object] = field(default_factory=list)
    source_pending_items: list[object] = field(default_factory=list)
    evidence_pending_items: list[object] = field(default_factory=list)
    voice_warnings: list[object] = field(default_factory=list)
    privacy_warnings: list[object] = field(default_factory=list)
    p13_traceability: list[object] = field(default_factory=list)
    limitations: list[object] = field(default_factory=list)
    global_cartography: object | None = None
    criticality_matrix: object | None = None
    selectivity_matrix: object | None = None
    density_justification: object | None = None

    def __post_init__(self) -> None:
        _exige_nao_vazio("31.4", "current_p13_state", self.current_p13_state)


# --- §29 — exemplo canônico: ABSTAINED por perfil de voz insuficiente ---


def constroi_abstencao_perfil_de_voz_insuficiente(
    *, abstention_id: str, request_id: str, reason: str | None = None, **kwargs
) -> AbstentionPayload:
    """§29 — "Quando o perfil for insuficiente": `status=ABSTAINED`,
    `AbstentionPayload.category=AMBIGUITY`,
    `cause_code=P13_CAUSE_VOICE_PROFILE_INSUFFICIENT`.

    `AbstentionPayload` (P09 §15, `escolio/contrato/payloads.py`) **não tem
    campo `cause_code`** — o campo não existe no envelope P09; ele só
    aparece nos exemplos de §29/§30 dos contratos de função (P13 e,
    presumivelmente, outros). Sem campo dedicado, e sem nenhuma outra seção
    do P09 ou do P13 que diga onde colocá-lo, o valor é registrado
    literalmente dentro de `reason` — o único campo de texto livre
    obrigatório do payload — em vez de fabricar um campo novo em
    `AbstentionPayload` (alteraria código existente, fora do escopo desta
    sessão). Ver LACUNAS.md.

    Reusa `perfil_insuficiente`/`P13_CAUSE_VOICE_PROFILE_INSUFFICIENT`
    (sessão 5, `aplicacao_p06_p07.py`) sem redefinir a constante.
    """
    motivo = reason or (
        "Perfil de voz insuficiente ou conflitante para preservar a voz do "
        f"autor avaliado [§29; cause_code={P13_CAUSE_VOICE_PROFILE_INSUFFICIENT}]"
    )
    return AbstentionPayload(
        abstention_id=abstention_id,
        request_id=request_id,
        category=AbstentionCategory.AMBIGUITY,
        reason=motivo,
        **kwargs,
    )


# --- §31.6 — Regra de payloads ------------------------------------------
#
# As três formas abaixo não introduzem regra nova: `Response.__post_init__`
# (escolio/contrato/resposta.py, peça 1) já impõe exatamente a forma de
# §31.6 para qualquer function_id — safe_result.available=false / error=null
# / block=null para ABSTAINED; safe_result.available=false / error=null /
# abstention=null para BLOCKED; "somente ERROR pode utilizar safe_result"
# decorre de SUCCESS/PARTIAL_SUCCESS/ABSTAINED/BLOCKED todos exigirem
# safe_result.available=false e ERROR ser o único status sem essa exigência.
# Os três builders só fixam function_id="P13" e a forma de safe_result que
# §31.6 nomeia para cada status — nenhuma validação de Response é
# duplicada; a chamada levanta ErroDeContrato (não ErroDeComentario) quando
# a forma é inválida, porque a rejeição vem de dentro de Response.


def resposta_p13_abstained(
    *,
    schema_version: SemanticVersion,
    response_id: str,
    request_id: str,
    project_id: str,
    component_id: str,
    abstention: AbstentionPayload,
    result: Result | None = None,
    **kwargs,
) -> Response:
    """§31.6 ABSTAINED — safe_result.available=false, content=null,
    reference=null, scope=[]; abstention preenchido; error=null; block=null."""
    return Response(
        schema_version=schema_version,
        response_id=response_id,
        request_id=request_id,
        project_id=project_id,
        component_id=component_id,
        function_id="P13",
        status=ResponseStatus.ABSTAINED,
        abstention=abstention,
        safe_result=SafeResult(available=False),
        result=result if result is not None else Result(),
        **kwargs,
    )


def resposta_p13_blocked(
    *,
    schema_version: SemanticVersion,
    response_id: str,
    request_id: str,
    project_id: str,
    component_id: str,
    block: BlockPayload,
    result: Result | None = None,
    **kwargs,
) -> Response:
    """§31.6 BLOCKED — safe_result.available=false, content=null,
    reference=null, scope=[]; block preenchido; error=null; abstention=null."""
    return Response(
        schema_version=schema_version,
        response_id=response_id,
        request_id=request_id,
        project_id=project_id,
        component_id=component_id,
        function_id="P13",
        status=ResponseStatus.BLOCKED,
        block=block,
        safe_result=SafeResult(available=False),
        result=result if result is not None else Result(),
        **kwargs,
    )


def resposta_p13_error(
    *,
    schema_version: SemanticVersion,
    response_id: str,
    request_id: str,
    project_id: str,
    component_id: str,
    error: ErrorPayload,
    safe_result: SafeResult | None = None,
    result: Result | None = None,
    **kwargs,
) -> Response:
    """§31.6 ERROR — "Somente ERROR pode utilizar safe_result como
    resultado seguro preservado": diferente dos dois builders acima, este
    aceita `safe_result` do chamador (`available=True` com trabalho
    preservado é uma forma válida só sob ERROR; os outros dois status a
    recusariam via `Response.__post_init__`)."""
    return Response(
        schema_version=schema_version,
        response_id=response_id,
        request_id=request_id,
        project_id=project_id,
        component_id=component_id,
        function_id="P13",
        status=ResponseStatus.ERROR,
        error=error,
        safe_result=safe_result if safe_result is not None else SafeResult(available=False),
        result=result if result is not None else Result(),
        **kwargs,
    )

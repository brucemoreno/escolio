"""Auditoria final interna — fonte: P13 §25 (DENSIDADE E QUANTIDADE), §44
(AUDITORIA FINAL). Sessão 7 de `docs/spec/plano-P13.md`.

Escopo: um checklist que roda os 25 itens de §44, nesta ordem literal, sobre
um lote de comentários já produzido pelas sessões 1-6. "A auditoria não
corrige comentários" [§44] — todo item aqui só verifica; nenhuma função
deste módulo grava, corrige ou reordena um `P13Comment`.

Reusa `P13Comment`/`RegistroDeComentarios` (sessão 1), `MatrizCriticidade`/
`ClasseCriticidade` (sessão 2), `MatrizSeletividade`/`SelectionDecision`/
`exige_referencia_valida_a_criticidade` (sessão 2, BL-024), `CommentType`/
`EFEITO_LINGUISTICO_COSMETICO` (sessão 3), `SourceStatusComentario`
(sessão 4), `NIVEIS_PERMITIDOS_P13`/`GateCatalogoP13`/
`valida_correcao_local_nao_autoriza_reescrita_forte`/
`valida_gate_humano_tem_gate_nomeado` (sessão 5), `NivelIntervencao` (P06),
`ResultadoDeFidelidade` (P07) e `Response`/`SafeResult` (P09,
`escolio/contrato/`) — nenhuma regra já construída nessas sessões é
duplicada aqui.

Proibição simétrica de §25, verbatim: "zero comentários" é resultado
legítimo e não existe quota; "silêncio diante de risco material" é
ilegítimo. Os itens 6 e 7 do checklist verificam as duas pontas
separadamente — nenhuma das duas é tratada como aprovação automática da
outra.
"""

from dataclasses import dataclass, field
from enum import Enum

from escolio.comentarios.aplicacao_p04_p05 import SourceStatusComentario
from escolio.comentarios.aplicacao_p06_p07 import (
    NIVEIS_PERMITIDOS_P13,
    GateCatalogoP13,
    valida_correcao_local_nao_autoriza_reescrita_forte,
    valida_gate_humano_tem_gate_nomeado,
)
from escolio.comentarios.comentario import P13Comment
from escolio.comentarios.criticidade import ClasseCriticidade, MatrizCriticidade
from escolio.comentarios.erros import ErroDeComentario
from escolio.comentarios.registro import RegistroDeComentarios
from escolio.comentarios.seletividade import (
    MatrizSeletividade,
    SelectionDecision,
    exige_referencia_valida_a_criticidade,
)
from escolio.comentarios.tipos import EFEITO_LINGUISTICO_COSMETICO, CommentType
from escolio.comentarios.vocabulario import STATUS_QUE_EXIGEM_RESOLUTION, P13CommentStatus
from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.payloads import AbstentionPayload, BlockPayload, ErrorPayload
from escolio.contrato.referencia import SemanticVersion
from escolio.contrato.resposta import Response, SafeResult
from escolio.contrato.vocabulario import ResponseStatus
from escolio.intervencao.niveis import NivelIntervencao
from escolio.voz.vocabulario import ResultadoDeFidelidade

ARQUIVO_FONTE = "P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md"


class ItemChecklist(str, Enum):
    """Os 25 itens de §44, nesta ordem literal."""

    SELETIVIDADE = "SELETIVIDADE"
    RELEVANCIA = "RELEVANCIA"
    CRITICIDADE = "CRITICIDADE"
    AUSENCIA_DE_QUOTA = "AUSENCIA_DE_QUOTA"
    AUSENCIA_DE_COMENTARIO_COSMETICO = "AUSENCIA_DE_COMENTARIO_COSMETICO"
    AUSENCIA_LEGITIMA_DE_COMENTARIOS = "AUSENCIA_LEGITIMA_DE_COMENTARIOS"
    PROBLEMAS_MATERIAIS_NAO_SILENCIADOS = "PROBLEMAS_MATERIAIS_NAO_SILENCIADOS"
    COMENTARIOS_MATRIZ = "COMENTARIOS_MATRIZ"
    REMISSOES = "REMISSOES"
    ANCORAGEM = "ANCORAGEM"
    EVIDENCIA = "EVIDENCIA"
    STATUS_DE_FONTE = "STATUS_DE_FONTE"
    NIVEL_P06 = "NIVEL_P06"
    VOZ_P07 = "VOZ_P07"
    PRIVACIDADE_P08 = "PRIVACIDADE_P08"
    ENVELOPES_P09 = "ENVELOPES_P09"
    TOM = "TOM"
    ACIONABILIDADE = "ACIONABILIDADE"
    PROPORCIONALIDADE = "PROPORCIONALIDADE"
    RASTREABILIDADE = "RASTREABILIDADE"
    REVERSIBILIDADE = "REVERSIBILIDADE"
    GATES = "GATES"
    AUSENCIA_DE_REESCRITA_SUBSTITUTIVA = "AUSENCIA_DE_REESCRITA_SUBSTITUTIVA"
    AUSENCIA_DE_IMPLEMENTACAO_WORD = "AUSENCIA_DE_IMPLEMENTACAO_WORD"
    DENSIDADE_JUSTIFICADA = "DENSIDADE_JUSTIFICADA"


_ORDEM_ITENS = tuple(ItemChecklist)
assert len(_ORDEM_ITENS) == 25, "§44 declara exatamente 25 itens de auditoria"


class VeredictoChecklist(str, Enum):
    """Três resultados possíveis por item, mais o N/A explícito do item 15.

    `NAO_VERIFICAVEL_NESTA_SESSAO` não é aprovação silenciosa — é o mesmo
    "indeterminado em vez de chute" de CLAUDE.md §11 (precedentes RG-002,
    RG-007): usado quando a fonte não declara critério objetivo, ou quando
    o lote não forneceu o dado necessário para o item. `NAO_APLICAVEL` é
    reservado ao item 15 (privacidade P08), N/A explícito por decisão de
    sessão adiada — não usado por omissão de dado."""

    APROVADO = "APROVADO"
    REPROVADO = "REPROVADO"
    NAO_APLICAVEL = "NAO_APLICAVEL"
    NAO_VERIFICAVEL_NESTA_SESSAO = "NAO_VERIFICAVEL_NESTA_SESSAO"


@dataclass(frozen=True)
class ResultadoChecklist:
    item: ItemChecklist
    veredito: VeredictoChecklist
    justificativa: str

    def __post_init__(self) -> None:
        if not isinstance(self.item, ItemChecklist):
            raise ErroDeComentario("44", "item deve ser um membro de ItemChecklist", ARQUIVO_FONTE)
        if not isinstance(self.veredito, VeredictoChecklist):
            raise ErroDeComentario("44", "veredito deve ser um membro de VeredictoChecklist", ARQUIVO_FONTE)
        if not self.justificativa or not self.justificativa.strip():
            raise ErroDeComentario(
                "44", "justificativa vazia impede o registro do item de checklist", ARQUIVO_FONTE
            )


class VeredictoFinal(str, Enum):
    AUDITORIA_APROVADA = "AUDITORIA_APROVADA"
    AUDITORIA_REPROVADA = "AUDITORIA_REPROVADA"
    AUDITORIA_INDETERMINADA = "AUDITORIA_INDETERMINADA"


@dataclass(frozen=True)
class VerificacaoEnvelope:
    """Um envelope P09 candidato do lote, para o item 16 — schema mínimo
    suficiente para exercer `Response`/`SafeResult` reais (`escolio/contrato/`)
    sem construir `P13RequestExtension`/`P13ResultExtension` (sessão 8, ainda
    não construída)."""

    status: ResponseStatus
    safe_result_available: bool
    abstention: AbstentionPayload | None = None
    block: BlockPayload | None = None
    error: ErrorPayload | None = None


@dataclass
class RelatorioAuditoriaFinal:
    lote_id: str
    resultados: list[ResultadoChecklist]

    def __post_init__(self) -> None:
        if not self.lote_id or not self.lote_id.strip():
            raise ErroDeComentario("44", "lote_id vazio impede o registro da auditoria", ARQUIVO_FONTE)
        itens_presentes = tuple(r.item for r in self.resultados)
        if itens_presentes != _ORDEM_ITENS:
            faltantes = set(_ORDEM_ITENS) - set(itens_presentes)
            extras = set(itens_presentes) - set(_ORDEM_ITENS)
            duplicados = len(itens_presentes) != len(set(itens_presentes))
            raise ErroDeComentario(
                "44",
                "RelatorioAuditoriaFinal exige exatamente os 25 itens de §44, cada um uma vez, nesta ordem",
                ARQUIVO_FONTE,
                detalhe=f"faltando={sorted(i.value for i in faltantes)} extras={sorted(i.value for i in extras)} duplicados={duplicados}",
            )

    @property
    def veredicto_final(self) -> VeredictoFinal:
        vereditos = [r.veredito for r in self.resultados]
        if VeredictoChecklist.REPROVADO in vereditos:
            return VeredictoFinal.AUDITORIA_REPROVADA
        if VeredictoChecklist.NAO_VERIFICAVEL_NESTA_SESSAO in vereditos:
            return VeredictoFinal.AUDITORIA_INDETERMINADA
        return VeredictoFinal.AUDITORIA_APROVADA

    def resultado_do_item(self, item: ItemChecklist) -> ResultadoChecklist:
        for resultado in self.resultados:
            if resultado.item == item:
                return resultado
        raise KeyError(item)


@dataclass
class LoteDeAuditoria:
    """Um lote de comentários já produzido pelas sessões 1-6, com os dados
    auxiliares que o checklist de §44 precisa para verificar cada item. Todo
    campo além de `comentarios` é opcional: sua ausência não vira aprovação
    — vira `NAO_VERIFICAVEL_NESTA_SESSAO` no item que dependeria dele."""

    comentarios: list[P13Comment]
    matrizes_criticidade: list[MatrizCriticidade] = field(default_factory=list)
    matrizes_seletividade: list[MatrizSeletividade] = field(default_factory=list)
    quota_declarada: bool = False
    efeitos_linguisticos: dict[str, str] = field(default_factory=dict)
    verificacoes_envelope: list[VerificacaoEnvelope] = field(default_factory=list)


def _parse_enum(cls, valor: str):
    try:
        return cls(valor)
    except ValueError:
        return None


def _resultado(item: ItemChecklist, veredito: VeredictoChecklist, justificativa: str) -> ResultadoChecklist:
    return ResultadoChecklist(item=item, veredito=veredito, justificativa=justificativa)


# --- Item 1 — SELETIVIDADE [§10, §11-12, BL-024] -----------------------


def _item_seletividade(lote: LoteDeAuditoria) -> ResultadoChecklist:
    if not lote.matrizes_seletividade:
        if lote.comentarios:
            return _resultado(
                ItemChecklist.SELETIVIDADE,
                VeredictoChecklist.REPROVADO,
                "comentários produzidos sem nenhuma MatrizSeletividade no lote — seletividade não verificável",
            )
        return _resultado(
            ItemChecklist.SELETIVIDADE,
            VeredictoChecklist.NAO_VERIFICAVEL_NESTA_SESSAO,
            "lote sem comentários e sem matrizes de seletividade",
        )
    try:
        exige_referencia_valida_a_criticidade(lote.matrizes_seletividade, lote.matrizes_criticidade)
    except ErroDeComentario as erro:
        return _resultado(ItemChecklist.SELETIVIDADE, VeredictoChecklist.REPROVADO, str(erro))
    decididos_comentar = [
        m for m in lote.matrizes_seletividade if m.selection_decision == SelectionDecision.COMENTAR
    ]
    if lote.comentarios and not decididos_comentar:
        return _resultado(
            ItemChecklist.SELETIVIDADE,
            VeredictoChecklist.REPROVADO,
            "há comentários produzidos, mas nenhuma MatrizSeletividade com selection_decision=COMENTAR",
        )
    return _resultado(
        ItemChecklist.SELETIVIDADE,
        VeredictoChecklist.APROVADO,
        "matrizes de seletividade íntegras e referenciando MatrizCriticidade existente [§11-12, BL-024]",
    )


# --- Item 2 — RELEVANCIA [§14.1] ----------------------------------------

_PRIORIDADE_SEM_PRIORIDADE = "SEM_PRIORIDADE_DE_COMENTARIO"


def _item_relevancia(lote: LoteDeAuditoria) -> ResultadoChecklist:
    sem_prioridade = [c.comment_id for c in lote.comentarios if c.priority == _PRIORIDADE_SEM_PRIORIDADE]
    if sem_prioridade:
        return _resultado(
            ItemChecklist.RELEVANCIA,
            VeredictoChecklist.REPROVADO,
            f"comentário produzido com priority={_PRIORIDADE_SEM_PRIORIDADE} [CLAUDE.md §7]",
        )
    return _resultado(
        ItemChecklist.RELEVANCIA, VeredictoChecklist.APROVADO, "nenhum comentário produzido sem prioridade atribuída"
    )


# --- Item 3 — CRITICIDADE [§11] -----------------------------------------


def _item_criticidade(lote: LoteDeAuditoria) -> ResultadoChecklist:
    if not lote.matrizes_seletividade:
        return _resultado(
            ItemChecklist.CRITICIDADE,
            VeredictoChecklist.NAO_VERIFICAVEL_NESTA_SESSAO,
            "lote sem matrizes de seletividade — criticidade da seleção não verificável",
        )
    sem_criticidade_comentada = [
        m.selection_id
        for m in lote.matrizes_seletividade
        if m.selection_decision == SelectionDecision.COMENTAR
        and m.criticality == ClasseCriticidade.SEM_CRITICIDADE_MATERIAL
    ]
    if sem_criticidade_comentada:
        return _resultado(
            ItemChecklist.CRITICIDADE,
            VeredictoChecklist.REPROVADO,
            f"selection_decision=COMENTAR com criticality=SEM_CRITICIDADE_MATERIAL: {sem_criticidade_comentada}",
        )
    return _resultado(
        ItemChecklist.CRITICIDADE, VeredictoChecklist.APROVADO, "nenhum comentário produzido sobre candidato sem criticidade material"
    )


# --- Item 4 — AUSENCIA_DE_QUOTA [§34.3-34.4, §3.9] ----------------------


def _item_ausencia_de_quota(lote: LoteDeAuditoria) -> ResultadoChecklist:
    if lote.quota_declarada:
        return _resultado(
            ItemChecklist.AUSENCIA_DE_QUOTA,
            VeredictoChecklist.REPROVADO,
            "lote declara quota — ação proibida [§34.3-34.4, PC30_SIGNIFICA_CRITICIDADE_E_NAO_QUOTA]",
        )
    return _resultado(ItemChecklist.AUSENCIA_DE_QUOTA, VeredictoChecklist.APROVADO, "nenhuma quota declarada para o lote")


# --- Item 5 — AUSENCIA_DE_COMENTARIO_COSMETICO [§15] --------------------


def _item_ausencia_de_comentario_cosmetico(lote: LoteDeAuditoria) -> ResultadoChecklist:
    if not lote.efeitos_linguisticos:
        return _resultado(
            ItemChecklist.AUSENCIA_DE_COMENTARIO_COSMETICO,
            VeredictoChecklist.NAO_VERIFICAVEL_NESTA_SESSAO,
            "lote não informou o efeito linguístico por comentário — não verificável sem ele",
        )
    cosmeticos = [
        comment_id for comment_id, efeito in lote.efeitos_linguisticos.items() if efeito in EFEITO_LINGUISTICO_COSMETICO
    ]
    if cosmeticos:
        return _resultado(
            ItemChecklist.AUSENCIA_DE_COMENTARIO_COSMETICO,
            VeredictoChecklist.REPROVADO,
            f"comentário com efeito linguístico cosmético [§15]: {cosmeticos}",
        )
    return _resultado(
        ItemChecklist.AUSENCIA_DE_COMENTARIO_COSMETICO,
        VeredictoChecklist.APROVADO,
        "nenhum efeito linguístico informado é cosmético",
    )


# --- Item 6 — AUSENCIA_LEGITIMA_DE_COMENTARIOS [§25, §3.9] --------------


def _item_ausencia_legitima_de_comentarios(lote: LoteDeAuditoria) -> ResultadoChecklist:
    if lote.comentarios:
        return _resultado(
            ItemChecklist.AUSENCIA_LEGITIMA_DE_COMENTARIOS,
            VeredictoChecklist.APROVADO,
            "há comentários no lote — nenhuma ausência a avaliar neste item",
        )
    if not lote.matrizes_seletividade:
        return _resultado(
            ItemChecklist.AUSENCIA_LEGITIMA_DE_COMENTARIOS,
            VeredictoChecklist.NAO_VERIFICAVEL_NESTA_SESSAO,
            "zero comentários no lote, mas nenhuma MatrizSeletividade para justificar a ausência",
        )
    decididos_comentar = [
        m.selection_id for m in lote.matrizes_seletividade if m.selection_decision == SelectionDecision.COMENTAR
    ]
    if decididos_comentar:
        return _resultado(
            ItemChecklist.AUSENCIA_LEGITIMA_DE_COMENTARIOS,
            VeredictoChecklist.REPROVADO,
            f"zero comentários registrados, mas há selection_decision=COMENTAR não atendida: {decididos_comentar}",
        )
    return _resultado(
        ItemChecklist.AUSENCIA_LEGITIMA_DE_COMENTARIOS,
        VeredictoChecklist.APROVADO,
        "zero comentários legítimo [§25, §3.9]: todas as decisões de seletividade são consistentes com a ausência",
    )


# --- Item 7 — PROBLEMAS_MATERIAIS_NAO_SILENCIADOS [§25, simétrico] ------


def _item_problemas_materiais_nao_silenciados(lote: LoteDeAuditoria) -> ResultadoChecklist:
    silenciados = [
        m.selection_id
        for m in lote.matrizes_seletividade
        if m.criticality in (ClasseCriticidade.CRITICIDADE_CRITICA, ClasseCriticidade.CRITICIDADE_ALTA)
        and m.selection_decision == SelectionDecision.NAO_COMENTAR_SEM_PROBLEMA_MATERIAL
    ]
    if silenciados:
        return _resultado(
            ItemChecklist.PROBLEMAS_MATERIAIS_NAO_SILENCIADOS,
            VeredictoChecklist.REPROVADO,
            "silêncio diante de risco material [§25]: criticidade CRITICA/ALTA decidida como "
            f"NAO_COMENTAR_SEM_PROBLEMA_MATERIAL: {silenciados}",
        )
    return _resultado(
        ItemChecklist.PROBLEMAS_MATERIAIS_NAO_SILENCIADOS,
        VeredictoChecklist.APROVADO,
        "nenhum candidato de criticidade CRITICA/ALTA foi silenciado por 'ausência de problema material'",
    )


# --- Item 8 — COMENTARIOS_MATRIZ [§23] ----------------------------------


def _item_comentarios_matriz(lote: LoteDeAuditoria) -> ResultadoChecklist:
    matrizes = [c for c in lote.comentarios if c.comment_type == CommentType.COMENTARIO_MATRIZ.value]
    if not matrizes:
        return _resultado(
            ItemChecklist.COMENTARIOS_MATRIZ, VeredictoChecklist.APROVADO, "nenhum comentário-matriz neste lote"
        )
    autorreferenciados = [c.comment_id for c in matrizes if c.matrix_comment_id is not None]
    if autorreferenciados:
        return _resultado(
            ItemChecklist.COMENTARIOS_MATRIZ,
            VeredictoChecklist.REPROVADO,
            f"comentário-matriz com matrix_comment_id preenchido (aponta para outro comentário-matriz): {autorreferenciados}",
        )
    return _resultado(
        ItemChecklist.COMENTARIOS_MATRIZ, VeredictoChecklist.APROVADO, "comentários-matriz do lote bem formados [§23]"
    )


# --- Item 9 — REMISSOES [§23] -------------------------------------------


def _item_remissoes(lote: LoteDeAuditoria) -> ResultadoChecklist:
    remissoes = [c for c in lote.comentarios if c.comment_type == CommentType.REMISSAO_A_COMENTARIO_MATRIZ.value]
    if not remissoes:
        return _resultado(ItemChecklist.REMISSOES, VeredictoChecklist.APROVADO, "nenhuma remissão neste lote")
    registro = RegistroDeComentarios()
    matrizes = [c for c in lote.comentarios if c.comment_type == CommentType.COMENTARIO_MATRIZ.value]
    ids_matrizes = {c.comment_id for c in matrizes}
    outros = [c for c in lote.comentarios if c.comment_id not in ids_matrizes]
    try:
        for comentario in (*matrizes, *outros):
            registro.registrar(comentario)
    except ErroDeComentario as erro:
        return _resultado(ItemChecklist.REMISSOES, VeredictoChecklist.REPROVADO, str(erro))
    return _resultado(
        ItemChecklist.REMISSOES, VeredictoChecklist.APROVADO, "toda remissão resolve a um comentário-matriz existente [§23]"
    )


# --- Item 10 — ANCORAGEM [§31.5, TA13-17] -------------------------------

_CAMPOS_ANCORAGEM = ("anchor_start", "anchor_end", "anchor_text_hash")


def _item_ancoragem(lote: LoteDeAuditoria) -> ResultadoChecklist:
    faltantes = [
        c.comment_id
        for c in lote.comentarios
        if any(not getattr(c, campo) or not str(getattr(c, campo)).strip() for campo in _CAMPOS_ANCORAGEM)
    ]
    if faltantes:
        return _resultado(
            ItemChecklist.ANCORAGEM,
            VeredictoChecklist.REPROVADO,
            f"comentário sem âncora completa (anchor_start/anchor_end/anchor_text_hash) [TA13-17]: {faltantes}",
        )
    return _resultado(ItemChecklist.ANCORAGEM, VeredictoChecklist.APROVADO, "toda âncora presente e não vazia")


# --- Item 11 — EVIDENCIA [§27] ------------------------------------------


def _item_evidencia(lote: LoteDeAuditoria) -> ResultadoChecklist:
    faltantes = [c.comment_id for c in lote.comentarios if not c.evidence or not c.evidence.strip()]
    if faltantes:
        return _resultado(ItemChecklist.EVIDENCIA, VeredictoChecklist.REPROVADO, f"comentário sem evidence: {faltantes}")
    return _resultado(ItemChecklist.EVIDENCIA, VeredictoChecklist.APROVADO, "toda evidência presente")


# --- Item 12 — STATUS_DE_FONTE [§19] ------------------------------------


def _item_status_de_fonte(lote: LoteDeAuditoria) -> ResultadoChecklist:
    bibliograficos = [c for c in lote.comentarios if c.comment_type == CommentType.ALERTA_BIBLIOGRAFICO.value]
    if not bibliograficos:
        return _resultado(
            ItemChecklist.STATUS_DE_FONTE, VeredictoChecklist.APROVADO, "nenhum ALERTA_BIBLIOGRAFICO neste lote"
        )
    invalidos = [c.comment_id for c in bibliograficos if _parse_enum(SourceStatusComentario, c.source_status) is None]
    if invalidos:
        return _resultado(
            ItemChecklist.STATUS_DE_FONTE,
            VeredictoChecklist.REPROVADO,
            f"ALERTA_BIBLIOGRAFICO com source_status fora dos 9 estados de §19: {invalidos}",
        )
    return _resultado(ItemChecklist.STATUS_DE_FONTE, VeredictoChecklist.APROVADO, "source_status válido em todo comentário bibliográfico")


# --- Item 13 — NIVEL_P06 [§4.4] -----------------------------------------


def _item_nivel_p06(lote: LoteDeAuditoria) -> ResultadoChecklist:
    invalidos = []
    for c in lote.comentarios:
        nivel = _parse_enum(NivelIntervencao, c.intervention_level)
        if nivel is None or nivel not in NIVEIS_PERMITIDOS_P13:
            invalidos.append(c.comment_id)
    if invalidos:
        return _resultado(
            ItemChecklist.NIVEL_P06,
            VeredictoChecklist.REPROVADO,
            f"intervention_level fora dos cinco níveis permitidos ao P13 [§4.4]: {invalidos}",
        )
    return _resultado(ItemChecklist.NIVEL_P06, VeredictoChecklist.APROVADO, "todo intervention_level dentro de OBSERVACAO..PROPOSTA")


# --- Item 14 — VOZ_P07 [§4.5] -------------------------------------------


def _item_voz_p07(lote: LoteDeAuditoria) -> ResultadoChecklist:
    invalidos = []
    for c in lote.comentarios:
        resultado = _parse_enum(ResultadoDeFidelidade, c.voice_impact)
        if resultado is None:
            invalidos.append(c.comment_id)
            continue
        if resultado == ResultadoDeFidelidade.BLOQUEAR and c.comment_type != CommentType.ALERTA_DE_VOZ.value:
            invalidos.append(c.comment_id)
    if invalidos:
        return _resultado(
            ItemChecklist.VOZ_P07,
            VeredictoChecklist.REPROVADO,
            f"voice_impact inválido, ou BLOQUEAR sem comment_type=ALERTA_DE_VOZ [§4.5]: {invalidos}",
        )
    return _resultado(ItemChecklist.VOZ_P07, VeredictoChecklist.APROVADO, "voice_impact válido e coerente com comment_type")


# --- Item 15 — PRIVACIDADE_P08 [sessão adiada] --------------------------


def _item_privacidade_p08(lote: LoteDeAuditoria) -> ResultadoChecklist:
    return _resultado(
        ItemChecklist.PRIVACIDADE_P08,
        VeredictoChecklist.NAO_APLICAVEL,
        "sessão de privacidade (integração P08) adiada até CO-012/CO-013 "
        "[docs/spec/plano-P13.md, 'Sessão adiada'] — N/A explícito, não fabricado",
    )


# --- Item 16 — ENVELOPES_P09 [§8, §9, §21.34, TA13-19] ------------------


def verifica_consistencia_envelope_p09(verificacao: VerificacaoEnvelope) -> bool:
    """Reusa `Response`/`SafeResult` reais (`escolio/contrato/resposta.py`)
    para conferir se a combinação `status`/`safe_result.available`/payload é
    válida perante P09 §8.2/§9/§21.34. `False` significa "resposta
    inválida" — TA13-19 ("ABSTAINED com safe_result.available=true" →
    "resposta inválida"). Nenhuma regra de `Response` é reimplementada
    aqui."""
    try:
        Response(
            schema_version=SemanticVersion(1, 0, 0),
            response_id="AUD-ENVELOPE-CHECK",
            request_id="AUD-ENVELOPE-CHECK",
            project_id="AUD-ENVELOPE-CHECK",
            component_id="P13",
            function_id="P13",
            status=verificacao.status,
            safe_result=SafeResult(available=verificacao.safe_result_available),
            abstention=verificacao.abstention,
            block=verificacao.block,
            error=verificacao.error,
        )
    except ErroDeContrato:
        return False
    return True


def _item_envelopes_p09(lote: LoteDeAuditoria) -> ResultadoChecklist:
    if not lote.verificacoes_envelope:
        return _resultado(
            ItemChecklist.ENVELOPES_P09,
            VeredictoChecklist.NAO_VERIFICAVEL_NESTA_SESSAO,
            "lote não informou envelope P09 candidato — P13RequestExtension/P13ResultExtension é "
            "sessão 8, ainda não construída [docs/spec/plano-P13.md]",
        )
    invalidos = [
        i for i, verificacao in enumerate(lote.verificacoes_envelope) if not verifica_consistencia_envelope_p09(verificacao)
    ]
    if invalidos:
        return _resultado(
            ItemChecklist.ENVELOPES_P09,
            VeredictoChecklist.REPROVADO,
            f"envelope P09 inconsistente [§8.2, §9, §21.34] nos índices: {invalidos}",
        )
    return _resultado(ItemChecklist.ENVELOPES_P09, VeredictoChecklist.APROVADO, "todo envelope P09 informado é consistente")


# --- Item 17 — TOM [§6.3] -----------------------------------------------


def _item_tom(_lote: LoteDeAuditoria) -> ResultadoChecklist:
    return _resultado(
        ItemChecklist.TOM,
        VeredictoChecklist.NAO_VERIFICAVEL_NESTA_SESSAO,
        "'tom' não tem critério objetivo declarado na fonte além da preferência de configuração humana "
        "[§6.3] — mesma disciplina de 'incompreensível' em matriz.py",
    )


# --- Item 18 — ACIONABILIDADE [§27, §28] --------------------------------


def _item_acionabilidade(lote: LoteDeAuditoria) -> ResultadoChecklist:
    faltantes = [c.comment_id for c in lote.comentarios if not c.recommended_action or not c.recommended_action.strip()]
    if faltantes:
        return _resultado(
            ItemChecklist.ACIONABILIDADE, VeredictoChecklist.REPROVADO, f"comentário sem recommended_action: {faltantes}"
        )
    return _resultado(ItemChecklist.ACIONABILIDADE, VeredictoChecklist.APROVADO, "toda ação recomendada presente")


# --- Item 19 — PROPORCIONALIDADE ----------------------------------------


def _item_proporcionalidade(_lote: LoteDeAuditoria) -> ResultadoChecklist:
    return _resultado(
        ItemChecklist.PROPORCIONALIDADE,
        VeredictoChecklist.NAO_VERIFICAVEL_NESTA_SESSAO,
        "'proporcionalidade' não tem critério objetivo mensurável declarado na fonte para este item do checklist",
    )


# --- Item 20 — RASTREABILIDADE [§31.5, TA13-17] -------------------------

_CAMPOS_RASTREABILIDADE = ("document_id", "document_version", "unit_id", "comment_id")


def _item_rastreabilidade(lote: LoteDeAuditoria) -> ResultadoChecklist:
    faltantes = [
        c.comment_id or "<comment_id vazio>"
        for c in lote.comentarios
        if any(not getattr(c, campo) or not str(getattr(c, campo)).strip() for campo in _CAMPOS_RASTREABILIDADE)
    ]
    if faltantes:
        return _resultado(
            ItemChecklist.RASTREABILIDADE,
            VeredictoChecklist.REPROVADO,
            f"comentário órfão: document_id/document_version/unit_id/comment_id incompleto [TA13-17]: {faltantes}",
        )
    return _resultado(
        ItemChecklist.RASTREABILIDADE, VeredictoChecklist.APROVADO, "documento, versão e unidade presentes em todo comentário"
    )


# --- Item 21 — REVERSIBILIDADE [§31.5.2, §32, TA13-18] ------------------


def _item_reversibilidade(lote: LoteDeAuditoria) -> ResultadoChecklist:
    problemas = []
    for c in lote.comentarios:
        if c.status in STATUS_QUE_EXIGEM_RESOLUTION and c.resolution is None:
            problemas.append(c.comment_id)
            continue
        if c.reversible is False and c.gate == GateCatalogoP13.NENHUM.value:
            problemas.append(c.comment_id)
    if problemas:
        return _resultado(
            ItemChecklist.REVERSIBILIDADE,
            VeredictoChecklist.REPROVADO,
            "apagamento de proveniência ou ação irreversível sem gate nomeado [§31.5.2, §32, TA13-18]: "
            f"{problemas}",
        )
    return _resultado(
        ItemChecklist.REVERSIBILIDADE, VeredictoChecklist.APROVADO, "resolução rastreável e nenhuma ação irreversível sem gate"
    )


# --- Item 22 — GATES [§28, §32] -----------------------------------------


def _item_gates(lote: LoteDeAuditoria) -> ResultadoChecklist:
    problemas = []
    for c in lote.comentarios:
        gate = _parse_enum(GateCatalogoP13, c.gate)
        if gate is None:
            problemas.append(c.comment_id)
            continue
        try:
            valida_correcao_local_nao_autoriza_reescrita_forte(c.comment_type, gate)
            valida_gate_humano_tem_gate_nomeado(c.comment_type, gate)
        except ErroDeComentario:
            problemas.append(c.comment_id)
    if problemas:
        return _resultado(
            ItemChecklist.GATES, VeredictoChecklist.REPROVADO, f"gate inválido ou incoerente com comment_type [§28, §32]: {problemas}"
        )
    return _resultado(ItemChecklist.GATES, VeredictoChecklist.APROVADO, "todo gate válido e coerente com comment_type")


# --- Item 23 — AUSENCIA_DE_REESCRITA_SUBSTITUTIVA [§4.4] ----------------


def _item_ausencia_de_reescrita_substitutiva(resultado_nivel_p06: ResultadoChecklist) -> ResultadoChecklist:
    if resultado_nivel_p06.veredito == VeredictoChecklist.REPROVADO:
        return _resultado(
            ItemChecklist.AUSENCIA_DE_REESCRITA_SUBSTITUTIVA,
            VeredictoChecklist.REPROVADO,
            f"decorre do item NIVEL_P06 reprovado: {resultado_nivel_p06.justificativa}",
        )
    return _resultado(
        ItemChecklist.AUSENCIA_DE_REESCRITA_SUBSTITUTIVA,
        VeredictoChecklist.APROVADO,
        "nenhum comentário exerce nível acima de PROPOSTA (REESCRITA é rejeitada pelo item NIVEL_P06) [§4.4]",
    )


# --- Item 24 — AUSENCIA_DE_IMPLEMENTACAO_WORD [§43, item 28] ------------


def _item_ausencia_de_implementacao_word(lote: LoteDeAuditoria) -> ResultadoChecklist:
    inseridos = [c.comment_id for c in lote.comentarios if c.status == P13CommentStatus.INSERTED]
    if inseridos:
        return _resultado(
            ItemChecklist.AUSENCIA_DE_IMPLEMENTACAO_WORD,
            VeredictoChecklist.REPROVADO,
            f"status=INSERTED implica inserção Word, fora de escopo desta fase [§43, item 28]: {inseridos}",
        )
    return _resultado(
        ItemChecklist.AUSENCIA_DE_IMPLEMENTACAO_WORD,
        VeredictoChecklist.APROVADO,
        "nenhum comentário do lote está em status=INSERTED",
    )


# --- Item 25 — DENSIDADE_JUSTIFICADA [§25] ------------------------------


def _item_densidade_justificada(
    resultado_quota: ResultadoChecklist, resultado_silencio: ResultadoChecklist
) -> ResultadoChecklist:
    if resultado_quota.veredito == VeredictoChecklist.REPROVADO or resultado_silencio.veredito == VeredictoChecklist.REPROVADO:
        return _resultado(
            ItemChecklist.DENSIDADE_JUSTIFICADA,
            VeredictoChecklist.REPROVADO,
            "densidade não justificada [§25]: "
            f"quota={resultado_quota.justificativa!r}; silêncio={resultado_silencio.justificativa!r}",
        )
    return _resultado(
        ItemChecklist.DENSIDADE_JUSTIFICADA,
        VeredictoChecklist.APROVADO,
        "densidade justificada por ausência de quota e ausência de silêncio diante de risco material [§25]",
    )


def auditar_lote(lote: LoteDeAuditoria, lote_id: str) -> RelatorioAuditoriaFinal:
    """Executa os 25 itens de §44 sobre `lote`, nesta ordem. Não corrige
    nenhum `P13Comment` — "a auditoria não corrige comentários" [§44]."""
    resultado_seletividade = _item_seletividade(lote)
    resultado_relevancia = _item_relevancia(lote)
    resultado_criticidade = _item_criticidade(lote)
    resultado_quota = _item_ausencia_de_quota(lote)
    resultado_cosmetico = _item_ausencia_de_comentario_cosmetico(lote)
    resultado_ausencia_legitima = _item_ausencia_legitima_de_comentarios(lote)
    resultado_silencio = _item_problemas_materiais_nao_silenciados(lote)
    resultado_matriz = _item_comentarios_matriz(lote)
    resultado_remissoes = _item_remissoes(lote)
    resultado_ancoragem = _item_ancoragem(lote)
    resultado_evidencia = _item_evidencia(lote)
    resultado_status_fonte = _item_status_de_fonte(lote)
    resultado_nivel_p06 = _item_nivel_p06(lote)
    resultado_voz_p07 = _item_voz_p07(lote)
    resultado_privacidade = _item_privacidade_p08(lote)
    resultado_envelopes = _item_envelopes_p09(lote)
    resultado_tom = _item_tom(lote)
    resultado_acionabilidade = _item_acionabilidade(lote)
    resultado_proporcionalidade = _item_proporcionalidade(lote)
    resultado_rastreabilidade = _item_rastreabilidade(lote)
    resultado_reversibilidade = _item_reversibilidade(lote)
    resultado_gates = _item_gates(lote)
    resultado_reescrita = _item_ausencia_de_reescrita_substitutiva(resultado_nivel_p06)
    resultado_word = _item_ausencia_de_implementacao_word(lote)
    resultado_densidade = _item_densidade_justificada(resultado_quota, resultado_silencio)

    resultados = [
        resultado_seletividade,
        resultado_relevancia,
        resultado_criticidade,
        resultado_quota,
        resultado_cosmetico,
        resultado_ausencia_legitima,
        resultado_silencio,
        resultado_matriz,
        resultado_remissoes,
        resultado_ancoragem,
        resultado_evidencia,
        resultado_status_fonte,
        resultado_nivel_p06,
        resultado_voz_p07,
        resultado_privacidade,
        resultado_envelopes,
        resultado_tom,
        resultado_acionabilidade,
        resultado_proporcionalidade,
        resultado_rastreabilidade,
        resultado_reversibilidade,
        resultado_gates,
        resultado_reescrita,
        resultado_word,
        resultado_densidade,
    ]
    return RelatorioAuditoriaFinal(lote_id=lote_id, resultados=resultados)

"""Integração P06 (níveis de intervenção)/P07 (voz autoral) no comentário
P13 — fonte: `P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md`
§4.4 (P13 × P06), §4.5 (P13 × P07), §28 (APLICAÇÃO DO P06), §29 (APLICAÇÃO
DO P07), §32 (GATES HUMANOS), §45 (PS13-07, PS13-08). Sessão 5 de
`docs/spec/plano-P13.md`.

Reusa `escolio.intervencao.niveis.NivelIntervencao` (P06) e
`escolio.voz.vocabulario.ResultadoDeFidelidade`/`DesvioBloqueante` +
`escolio.voz.fidelidade.avaliar`/`AvaliacaoDeFidelidade` (P07) sem duplicar
enum ou regra já construída nesses módulos. Nenhum código existente foi
alterado — `P13Comment.intervention_level`/`gate`/`voice_impact`
permanecem `str` [comentario.py]; este módulo valida o valor antes de
gravá-lo, mesma disciplina de `aplicacao_p04_p05.py` (sessão 4).

ESCOPO: a voz aqui é exclusivamente a do autor avaliado, a preservar
[§4.5, "O P07 define voz autoral"; CLAUDE.md §9, §13.1]. A voz de quem
comenta permanece bloqueada e não entra neste módulo em nenhuma forma.

`authority_required` **não é retipado** nesta sessão — ver
`escolio/comentarios/LACUNAS.md`, "Sessão 5": a fonte não declara um
catálogo fechado de tokens para este campo (§5 enumera perfis em prosa,
não em vocabulário controlado como §13 ou §32), e tipar por analogia seria
a mesma inferência já recusada para os nove fatores de `MatrizSeletividade`
(sessão 2). O campo permanece `str`, validado apenas quanto à
obrigatoriedade em `comentario.py`.
"""

import dataclasses
from dataclasses import dataclass
from enum import Enum

from escolio.comentarios.comentario import P13Comment
from escolio.comentarios.erros import ErroDeComentario
from escolio.comentarios.tipos import CommentType
from escolio.intervencao.niveis import NivelIntervencao
from escolio.voz.fidelidade import AvaliacaoDeFidelidade
from escolio.voz.perfil import PerfilDeVoz
from escolio.voz.vocabulario import ResultadoDeFidelidade, StatusDePerfil

ARQUIVO_FONTE = "P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md"

# §4.4 — "O comentário pode: observar; diagnosticar; sinalizar; recomendar;
# propor [...]". Correspondência literal verbo -> nível [P06]: os cinco
# verbos são os próprios nomes dos cinco primeiros níveis da cadeia
# INT-01..INT-15 (escolio.intervencao.niveis.NivelIntervencao), não uma
# tabela de tradução inventada. "Formular pergunta orientadora" e "indicar
# gate", os outros dois itens do "pode", não são níveis de intervenção —
# são `comment_type` (`PERGUNTA_ORIENTADORA`, `GATE_HUMANO`, §13), fora do
# escopo deste conjunto.
NIVEIS_PERMITIDOS_P13 = frozenset(
    {
        NivelIntervencao.OBSERVACAO,
        NivelIntervencao.DIAGNOSTICO,
        NivelIntervencao.SINALIZACAO,
        NivelIntervencao.RECOMENDACAO,
        NivelIntervencao.PROPOSTA,
    }
)

# §4.4 — "não pode, por si só: executar reescrita; fundir; cortar;
# substituir; reorganizar [...]". Cinco dos onze verbos proibidos nomeiam
# diretamente um nível da cadeia P06; citados aqui só para a mensagem de
# erro — a validação em si já rejeita qualquer nível fora de
# NIVEIS_PERMITIDOS_P13, o que cobre estes cinco e mais os não nomeados em
# nenhuma das duas listas (SIMULACAO, EDICAO_LOCAL, VALIDACAO, HOMOLOGACAO,
# ABSTENCAO) — leitura fechada: "pode" enumera exaustivamente o permitido,
# mesma disciplina de `escalonamento_permitido` em
# escolio/intervencao/niveis.py ("somente estas existem"). Ver LACUNAS.md
# quanto aos cinco níveis não nomeados em nenhuma lista.
NIVEIS_EXPLICITAMENTE_PROIBIDOS_P13 = frozenset(
    {
        NivelIntervencao.REESCRITA,
        NivelIntervencao.FUSAO,
        NivelIntervencao.CORTE,
        NivelIntervencao.SUBSTITUICAO,
        NivelIntervencao.REORGANIZACAO,
    }
)


def valida_intervention_level_permitido(nivel: NivelIntervencao) -> None:
    """§4.4 — rejeita qualquer nível fora dos cinco que o comentário "pode"
    exercer. Nunca corrige ou rebaixa o nível recebido; só recusa."""
    if not isinstance(nivel, NivelIntervencao):
        raise ErroDeComentario(
            "§4.4", "intervention_level deve ser um membro de NivelIntervencao", ARQUIVO_FONTE, repr(nivel)
        )
    if nivel not in NIVEIS_PERMITIDOS_P13:
        raise ErroDeComentario(
            "§4.4",
            "comentário não pode exercer este nível de intervenção — P13 se limita a "
            "OBSERVACAO, DIAGNOSTICO, SINALIZACAO, RECOMENDACAO ou PROPOSTA",
            ARQUIVO_FONTE,
            f"intervention_level={nivel.value}",
        )


class GateCatalogoP13(str, Enum):
    """17 gates nomeados em §32.1 (documentais) e §32.2 (humanos
    expressos), mais `NENHUM` — literal da coluna "Gate" de §45 (PS13-01,
    PS13-02, PS13-06: "Nenhum") para o caso em que nenhum gate se aplica.
    "Comentário que indica gate não concede a autorização" [§32, nota de
    fechamento]: este enum só nomeia o gate referenciado, nunca o libera.
    """

    # §32.1 — gates documentais
    GATE_DE_ATIVACAO_P13 = "GATE_DE_ATIVACAO_P13"
    GATE_DE_VERSAO = "GATE_DE_VERSAO"
    GATE_DE_ANCORAGEM = "GATE_DE_ANCORAGEM"
    GATE_DE_CARTOGRAFIA = "GATE_DE_CARTOGRAFIA"
    GATE_DE_SELECAO = "GATE_DE_SELECAO"
    GATE_DE_VALIDACAO_FINAL = "GATE_DE_VALIDACAO_FINAL"
    # §32.2 — gates humanos expressos
    GATE_DE_REESCRITA_FORTE = "GATE_DE_REESCRITA_FORTE"
    GATE_DE_ALTERACAO_DE_ARGUMENTO = "GATE_DE_ALTERACAO_DE_ARGUMENTO"
    GATE_DE_ALTERACAO_DE_CORPUS = "GATE_DE_ALTERACAO_DE_CORPUS"
    GATE_DE_ALTERACAO_DE_METODO = "GATE_DE_ALTERACAO_DE_METODO"
    GATE_DE_ALTERACAO_DE_OBJETIVO = "GATE_DE_ALTERACAO_DE_OBJETIVO"
    GATE_DE_ALTERACAO_DE_HIPOTESE = "GATE_DE_ALTERACAO_DE_HIPOTESE"
    GATE_DE_ALTERACAO_DE_RESULTADO = "GATE_DE_ALTERACAO_DE_RESULTADO"
    GATE_DE_ALTERACAO_DE_CONCLUSAO = "GATE_DE_ALTERACAO_DE_CONCLUSAO"
    GATE_DE_TRATAMENTO_DE_PRIVACIDADE = "GATE_DE_TRATAMENTO_DE_PRIVACIDADE"
    GATE_DE_CONSOLIDACAO = "GATE_DE_CONSOLIDACAO"
    GATE_DE_HOMOLOGACAO = "GATE_DE_HOMOLOGACAO"
    # §45 — "Nenhum"
    NENHUM = "NENHUM"


def valida_gate(gate: GateCatalogoP13) -> None:
    if not isinstance(gate, GateCatalogoP13):
        raise ErroDeComentario(
            "§32", "gate deve ser um membro de GateCatalogoP13", ARQUIVO_FONTE, repr(gate)
        )


def valida_correcao_local_nao_autoriza_reescrita_forte(comment_type: str, gate: GateCatalogoP13) -> None:
    """§28 — "`CORRECAO_LOCAL` não autoriza reescrita forte": um comentário
    deste tipo não pode carregar o gate que libera reescrita forte."""
    valida_gate(gate)
    if comment_type == CommentType.CORRECAO_LOCAL.value and gate == GateCatalogoP13.GATE_DE_REESCRITA_FORTE:
        raise ErroDeComentario(
            "§28",
            "CORRECAO_LOCAL não autoriza reescrita forte",
            ARQUIVO_FONTE,
            f"gate={gate.value}",
        )


def valida_gate_humano_tem_gate_nomeado(comment_type: str, gate: GateCatalogoP13) -> None:
    """§13 item 12 (`GATE_HUMANO`) + §32 — indicar gate é o próprio
    propósito deste `comment_type`; `NENHUM` esvaziaria a indicação."""
    valida_gate(gate)
    if comment_type == CommentType.GATE_HUMANO.value and gate == GateCatalogoP13.NENHUM:
        raise ErroDeComentario(
            "§13/§32",
            "comment_type=GATE_HUMANO exige um gate nomeado do catálogo de §32, não NENHUM",
        )


# §4.5 — "O P13: aplica P07; registra impacto sobre voz". `voice_impact`
# reusa `ResultadoDeFidelidade` (P07, escolio/voz/vocabulario.py): é
# literalmente o resultado que o protocolo de avaliação de fidelidade
# autoral já produz para "impacto sobre voz" de um texto candidato — mesma
# disciplina de `aplicacao_p04_p05.py` reusando `ValidationState` para
# `verification_status` a partir de uma frase equivalente em §4.3. Não é
# fusão de vocabulário nem invenção de rótulo novo.
_RESULTADOS_QUE_EXIGEM_ALERTA_DE_VOZ = frozenset({ResultadoDeFidelidade.BLOQUEAR})

P13_CAUSE_VOICE_PROFILE_INSUFFICIENT = "P13_CAUSE_VOICE_PROFILE_INSUFFICIENT"
"""§29 — cause_code do envelope `ABSTAINED/AMBIGUITY` quando o perfil for
insuficiente. A construção do envelope P09 é sessão 8 do plano; esta
sessão só expõe o predicado (`perfil_insuficiente`) e a constante literal
para a sessão que constrói o payload."""


def perfil_insuficiente(perfil: PerfilDeVoz) -> bool:
    """§29 — "Quando o perfil for insuficiente" é verificável em código
    como `PerfilDeVoz.status == StatusDePerfil.ABSTENCAO`
    [escolio/voz/perfil.py]: é o único status que o próprio módulo de
    perfil produz para perfil insuficiente ou conflitante."""
    return perfil.status == StatusDePerfil.ABSTENCAO


def valida_voice_impact_registrado(resultado: ResultadoDeFidelidade) -> None:
    if not isinstance(resultado, ResultadoDeFidelidade):
        raise ErroDeComentario(
            "§29", "voice_impact deve ser um membro de ResultadoDeFidelidade", ARQUIVO_FONTE, repr(resultado)
        )


def valida_alerta_de_voz_quando_bloqueado(comment_type: str, resultado: ResultadoDeFidelidade) -> None:
    """§4.5 — "evita formulação substitutiva; evita reescrever como
    orientador". Quando a avaliação de fidelidade bloqueia (desvio
    bloqueante presente, ex.: `COPIA_OU_IMITACAO`), o comentário deve ser
    `ALERTA_DE_VOZ` [§13 item 10], nunca a reescrita recusada em si —
    TA13-12 ("recusa e alerta de voz"), PS13-08 (`ALERTA_DE_VOZ`,
    `disposition=REFUSED`)."""
    valida_voice_impact_registrado(resultado)
    if resultado in _RESULTADOS_QUE_EXIGEM_ALERTA_DE_VOZ and comment_type != CommentType.ALERTA_DE_VOZ.value:
        raise ErroDeComentario(
            "§4.5",
            "voice_impact=BLOQUEAR exige comment_type=ALERTA_DE_VOZ",
            ARQUIVO_FONTE,
            f"comment_type={comment_type}",
        )


@dataclass(frozen=True)
class AplicacaoP06P07DoComentario:
    """Registro do que esta sessão aplicou sobre um `P13Comment` — não um
    schema da fonte (§28/§29 não declaram um schema próprio, diferente de
    §27 para P05); existe só para devolver, junto do comentário atualizado,
    os objetos tipados que motivaram a decisão, sem forçar quem chama a
    reconstruí-los."""

    intervention_level: NivelIntervencao
    gate: GateCatalogoP13
    voice_impact: ResultadoDeFidelidade
    avaliacao_de_voz: AvaliacaoDeFidelidade


def aplicar_intervencao_e_voz(
    comentario: P13Comment,
    intervention_level: NivelIntervencao,
    gate: GateCatalogoP13,
    avaliacao_de_voz: AvaliacaoDeFidelidade,
) -> tuple[P13Comment, AplicacaoP06P07DoComentario]:
    """Adaptador da sessão 5: valida `intervention_level` [§4.4], `gate`
    [§28, §32] e `voice_impact` [§4.5, §29] antes de gravar — nenhuma
    gravação ocorre se qualquer validação falhar, mesmo padrão de
    `aplicar_bibliografia_e_evidencia` (sessão 4). `authority_required` não
    é populado aqui — permanece fora do escopo tipável desta sessão, ver
    docstring do módulo."""
    valida_intervention_level_permitido(intervention_level)
    valida_correcao_local_nao_autoriza_reescrita_forte(comentario.comment_type, gate)
    valida_gate_humano_tem_gate_nomeado(comentario.comment_type, gate)
    valida_alerta_de_voz_quando_bloqueado(comentario.comment_type, avaliacao_de_voz.resultado)

    comentario_atualizado = dataclasses.replace(
        comentario,
        intervention_level=intervention_level.value,
        gate=gate.value,
        voice_impact=avaliacao_de_voz.resultado.value,
    )
    aplicacao = AplicacaoP06P07DoComentario(
        intervention_level=intervention_level,
        gate=gate,
        voice_impact=avaliacao_de_voz.resultado,
        avaliacao_de_voz=avaliacao_de_voz,
    )
    return comentario_atualizado, aplicacao

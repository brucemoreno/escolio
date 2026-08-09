"""Integração P04 (BVAA)/P05 (schema de afirmação-evidência) no comentário
P13 — fonte: `P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md`
§19 (COMENTÁRIO BIBLIOGRÁFICO), §20 (COMENTÁRIO SOBRE EVIDÊNCIA), §26
(APLICAÇÃO DO P04), §27 (APLICAÇÃO DO P05). Sessão 4 de
`docs/spec/plano-P13.md`.

Reusa `escolio.bvaa` (`EstadoBibliografico`, `transicoes_validas_a_partir_de`)
e `escolio` (`RelacaoAfirmacaoEvidencia`, `Sufficiency`, `Confidence`,
`ValidationState`, `NAO_DISPONIVEL`) sem duplicar enum ou regra de validação
já construída nesses módulos. Nenhum código existente foi alterado —
`P13Comment.source_status` permanece `str` [comentario.py]; este módulo
valida o valor antes de gravá-lo, não retipa o campo.

CON-P05-001 [CLAUDE.md §7; escolio/LACUNAS.md] permanece **aberto**: os 9
estados literais de §19 (`SourceStatusComentario`) são um vocabulário
próprio, distinto de `EstadoBibliografico` (P04, 17 estados), dos três
campos paralelos de P05 (`AccessState`/`ReadingState`/`ValidationState`) e
dos 9 estados mínimos de R03 CAMADA D. Nenhuma fusão e nenhuma função de
derivação automática `EstadoBibliografico -> SourceStatusComentario` é
construída aqui — nenhuma fonte declara essa correspondência. O que este
módulo faz é o inverso: recebe os dois valores já decididos por quem
comenta e **valida** que o estado do comentário não excede o que a máquina
BVAA sustenta [§26], rejeitando quando exceder. Ver `LACUNAS.md` para o
detalhamento desta decisão.
"""

import dataclasses
from dataclasses import dataclass
from enum import Enum

from escolio.bvaa.transicoes import transicoes_validas_a_partir_de
from escolio.bvaa.vocabulario import EstadoBibliografico
from escolio.comentarios.comentario import P13Comment
from escolio.comentarios.erros import ErroDeComentario
from escolio.relacao import RelacaoAfirmacaoEvidencia
from escolio.vocabulario import NAO_DISPONIVEL, Confidence, Sufficiency, ValidationState

ARQUIVO_FONTE = "P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md"


class SourceStatusComentario(str, Enum):
    """9 estados literais de §19 — "Estados possíveis" do comentário
    bibliográfico. Vocabulário próprio; ver CON-P05-001 no docstring do
    módulo."""

    FONTE_IDENTIFICADA = "FONTE_IDENTIFICADA"
    FONTE_LOCALIZADA = "FONTE_LOCALIZADA"
    FONTE_ABERTA = "FONTE_ABERTA"
    LEITURA_PARCIAL = "LEITURA_PARCIAL"
    LEITURA_INTEGRAL = "LEITURA_INTEGRAL"
    PASSAGEM_LOCALIZADA = "PASSAGEM_LOCALIZADA"
    PAGINA_CONFIRMADA = "PAGINA_CONFIRMADA"
    SUSTENTACAO_ESPECIFICA_LIBERADA = "SUSTENTACAO_ESPECIFICA_LIBERADA"
    SUSTENTACAO_NAO_LIBERADA = "SUSTENTACAO_NAO_LIBERADA"


# §26 — "sem acesso verificável: não confirma leitura; não confirma
# passagem; não confirma página; [...]; não libera sustentação específica".
# Cada status escalado exige que o BVAA já tenha alcançado o estado mínimo
# correspondente (ou um estado alcançável a partir dele) — não apenas
# "algum acesso": PAGINA_CONFIRMADA exige a página especificamente
# confirmada, não só leitura em curso, que é exatamente o cenário de
# PS13-05 (leitura parcial, página ainda não confirmada).
_REQUISITO_MINIMO: dict[SourceStatusComentario, EstadoBibliografico] = {
    SourceStatusComentario.FONTE_ABERTA: EstadoBibliografico.ACESSADA,
    SourceStatusComentario.LEITURA_PARCIAL: EstadoBibliografico.ACESSADA,
    SourceStatusComentario.LEITURA_INTEGRAL: EstadoBibliografico.ACESSADA,
    SourceStatusComentario.PASSAGEM_LOCALIZADA: EstadoBibliografico.ACESSADA,
    SourceStatusComentario.PAGINA_CONFIRMADA: EstadoBibliografico.PAGINA_CONFIRMADA,
    # §26 — "não libera sustentação específica [sem acesso]" é o bloqueio
    # mais forte do artigo: exige VALIDADA ou RECOMENDADA, os dois únicos
    # estados terminais positivos da máquina BVAA (arquivo 03), alcançáveis
    # a partir de VALIDADA (T15: VALIDADA -> RECOMENDADA).
    SourceStatusComentario.SUSTENTACAO_ESPECIFICA_LIBERADA: EstadoBibliografico.VALIDADA,
}


def _estados_alcancaveis(a_partir_de: EstadoBibliografico) -> frozenset[EstadoBibliografico]:
    """BFS sobre as transições T01..T17 (exclui o curinga T18 de invenção,
    que não representa progresso material) — cálculo estrutural sobre a
    própria matriz já declarada em `escolio.bvaa.transicoes`, não uma nova
    correspondência inventada."""
    visitados = {a_partir_de}
    pendentes = [a_partir_de]
    while pendentes:
        atual = pendentes.pop()
        for transicao in transicoes_validas_a_partir_de(atual):
            if transicao.estado_saida not in visitados:
                visitados.add(transicao.estado_saida)
                pendentes.append(transicao.estado_saida)
    return frozenset(visitados)


# ABSTENCAO_BIBLIOGRAFICA é alcançável a partir de ACESSADA (via
# VALIDACAO_PENDENTE -T13-> ABSTENCAO_BIBLIOGRAFICA), mas é o estado
# terminal de interrupção [escolio/bvaa/abstencao.py]: não sustenta nenhuma
# confirmação positiva, por isso é excluído explicitamente de todo conjunto
# de "estado mínimo alcançado" abaixo.
_ALCANCAVEIS_POR_REQUISITO: dict[EstadoBibliografico, frozenset[EstadoBibliografico]] = {
    requisito: _estados_alcancaveis(requisito) - {EstadoBibliografico.ABSTENCAO_BIBLIOGRAFICA}
    for requisito in set(_REQUISITO_MINIMO.values())
}


def valida_source_status_compativel_com_bvaa(
    status: SourceStatusComentario, estado_bvaa: EstadoBibliografico
) -> None:
    """§19 ("não deve declarar 'conferido' quando a fonte estiver apenas
    localizada"), §26 ("sem acesso verificável: não confirma leitura, [...],
    não libera sustentação específica"). Levanta `ErroDeComentario` quando o
    `status` do comentário afirma mais do que o estado atual do BVAA
    sustenta; nunca deriva ou corrige `status` silenciosamente."""
    if not isinstance(status, SourceStatusComentario):
        raise ErroDeComentario(
            "§19", "status deve ser um membro de SourceStatusComentario", ARQUIVO_FONTE, repr(status)
        )
    requisito = _REQUISITO_MINIMO.get(status)
    if requisito is not None and estado_bvaa not in _ALCANCAVEIS_POR_REQUISITO[requisito]:
        raise ErroDeComentario(
            "§26",
            f"'{status.value}' exige o BVAA em {requisito.value} ou estado alcançável a partir dele",
            ARQUIVO_FONTE,
            f"estado_bvaa={estado_bvaa.value}",
        )


@dataclass(frozen=True)
class AplicacaoP05DoComentario:
    """Schema mínimo de §27 — objeto próprio, distinto de `P13Comment`
    [§31.5]. A fonte declara os dois schemas separadamente: §31.5 não lista
    `claim_id`/`evidence_ids`, e §27 não repete os 24 campos de §31.5. Não
    fundidos aqui."""

    claim_id: str
    comment_id: str
    evidence_ids: tuple[str, ...]
    verification_status: ValidationState
    sufficiency: Sufficiency
    confidence: Confidence
    limitations: str

    def __post_init__(self) -> None:
        if not self.claim_id or not self.claim_id.strip():
            raise ErroDeComentario("§27", "claim_id vazio impede a criação do registro", ARQUIVO_FONTE)
        if not self.comment_id or not self.comment_id.strip():
            raise ErroDeComentario("§27", "comment_id vazio impede a criação do registro", ARQUIVO_FONTE)
        if not isinstance(self.verification_status, ValidationState):
            raise ErroDeComentario(
                "§27", "verification_status deve ser um membro de ValidationState", ARQUIVO_FONTE
            )
        if not isinstance(self.sufficiency, Sufficiency):
            raise ErroDeComentario("§27", "sufficiency deve ser um membro de Sufficiency", ARQUIVO_FONTE)
        if not isinstance(self.confidence, Confidence):
            raise ErroDeComentario("§27", "confidence deve ser um membro de Confidence", ARQUIVO_FONTE)
        if not self.limitations or not self.limitations.strip():
            raise ErroDeComentario("§27", "limitations vazio impede a criação do registro", ARQUIVO_FONTE)


def construir_aplicacao_p05(
    comment_id: str,
    claim_id: str,
    relacao: RelacaoAfirmacaoEvidencia | None,
) -> AplicacaoP05DoComentario:
    """§20 ("claim não tem evidência" é uma das condições de aplicação, não
    um erro de chamada) e §27 (schema mínimo). `relacao=None` representa
    literalmente essa condição — `evidence_ids` fica vazio e os três campos
    de avaliação usam os valores já existentes em P05 para "não avaliado"
    (`Sufficiency.EVIDENCIA_AUSENTE`, `Confidence.NAO_AVALIADA`,
    `ValidationState.NAO_VERIFICADA`), não um valor inventado por este
    módulo.

    Quando `relacao` é fornecida, `verification_status` reusa
    `relacao.validation_state` — decisão apoiada em §4.3 ("O P13: indica
    estado de verificação"), não uma correspondência nova entre nomes de
    campo. `limitations` reusa `relacao.notes`; quando `notes` é `None`,
    usa o valor controlado `NAO_DISPONIVEL` já declarado em
    `escolio.vocabulario` para "dado não está disponível" [§20], em vez de
    inventar um rótulo novo.

    Aceita no máximo uma `RelacaoAfirmacaoEvidencia` — agregação de
    múltiplas evidências para a mesma `claim_id` é `LAC-P05-003`
    (`escolio/LACUNAS.md`), lacuna já aberta e não resolvida aqui.
    """
    if relacao is not None and relacao.claim_id != claim_id:
        raise ErroDeComentario(
            "§27",
            "relacao.claim_id não corresponde ao claim_id do comentário",
            ARQUIVO_FONTE,
            f"claim_id={claim_id}, relacao.claim_id={relacao.claim_id}",
        )

    if relacao is None:
        return AplicacaoP05DoComentario(
            claim_id=claim_id,
            comment_id=comment_id,
            evidence_ids=(),
            verification_status=ValidationState.NAO_VERIFICADA,
            sufficiency=Sufficiency.EVIDENCIA_AUSENTE,
            confidence=Confidence.NAO_AVALIADA,
            limitations=NAO_DISPONIVEL,
        )

    return AplicacaoP05DoComentario(
        claim_id=claim_id,
        comment_id=comment_id,
        evidence_ids=(relacao.source_id,),
        verification_status=relacao.validation_state,
        sufficiency=relacao.sufficiency,
        confidence=relacao.confidence,
        limitations=relacao.notes if relacao.notes else NAO_DISPONIVEL,
    )


def aplicar_bibliografia_e_evidencia(
    comentario: P13Comment,
    source_status: SourceStatusComentario,
    estado_bvaa: EstadoBibliografico,
    claim_id: str,
    relacao: RelacaoAfirmacaoEvidencia | None = None,
) -> tuple[P13Comment, AplicacaoP05DoComentario]:
    """Adaptador da sessão 4: lê o estado do BVAA (`estado_bvaa`) e do
    schema P05 (`relacao`) e popula `source_status` [§19, §31.5] no
    comentário, mais `claim_id`/`evidence_ids` no schema mínimo de §27 —
    dois objetos, porque a fonte declara dois schemas separados (ver
    docstring de `AplicacaoP05DoComentario`).

    `source_status` é validado contra `estado_bvaa` antes de ser gravado
    [`valida_source_status_compativel_com_bvaa`]; a chamada levanta
    `ErroDeComentario` e não grava nada quando a validação falha —
    `dataclasses.replace` só é alcançado depois da validação passar, e ele
    próprio reexecuta `P13Comment.__post_init__` (nenhuma validação de
    `comentario.py` é duplicada aqui).
    """
    valida_source_status_compativel_com_bvaa(source_status, estado_bvaa)
    comentario_atualizado = dataclasses.replace(comentario, source_status=source_status.value)
    aplicacao = construir_aplicacao_p05(comentario.comment_id, claim_id, relacao)
    return comentario_atualizado, aplicacao

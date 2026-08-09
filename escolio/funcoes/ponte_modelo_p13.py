"""Ponte entre `escolio/funcoes/execucao_p13.py` e `escolio/cliente/` —
liga os pontos de extensão de modelo das etapas 8, 9, 16, 17 e 18 à API.

Escopo desta sessão, verbatim da instrução: só estas cinco etapas. As
etapas 11-15 continuam `PONTO_DE_EXTENSAO_DE_MODELO` permanente
[`escolio/funcoes/LACUNAS.md`, LAC-FUNC-019 — nenhuma sessão anterior
definiu o objeto que ligaria "candidato selecionado" a verificação de
fonte/evidência/voz/privacidade]; as etapas 19-24 continuam
`SEM_FONTE_DE_VERIFICACAO`. Nenhuma das duas é tocada aqui.

Modelo e `effort` por etapa — CLAUDE.md §10, tabela "Modelos e custo":

- Etapa 8 (E4b, matriz de criticidade) — Sonnet, `low`-`medium` na tabela;
  esta sessão fixa `medium` (ponto concreto dentro do intervalo declarado,
  não um valor novo — a tabela já é `[PROPOSTA]` inteira).
- Etapa 9 (E4c, seletividade → seleção) — Opus, `high`-`xhigh` na tabela;
  esta sessão fixa `high`. Opus **propõe**; a etapa 10 (`GATE_DE_SELECAO`)
  continua determinística (`aplicar_selecao`, já implementada) — o modelo
  nunca decide a seleção final por si.
- Etapas 16-18 (E6, elaboração de comentários) — Sonnet, `medium`.

Prompts em `prompts/p13_*.md`, lidos em disco a cada chamada — nunca
hardcoded aqui [CLAUDE.md §12].

Cada chamada usa uma ferramenta forçada (`tool_choice`) cujo `input_schema`
espelha exatamente os campos que o dataclass de destino exige — a validação
de forma final continua sendo o `__post_init__` do próprio dataclass
(`MatrizCriticidade`, `MatrizSeletividade`, `P13Comment`); esta ponte nunca
duplica essa validação, só traduz o `tool_use.input` do SDK para os
construtores já existentes. Erro de validação do dataclass é regra
bloqueante — propaga como `ErroDeExecucaoP13`, nunca é engolido
[CLAUDE.md §8].
"""

from __future__ import annotations

import json
from pathlib import Path

from escolio.comentarios.comentario import P13Comment
from escolio.comentarios.criticidade import ClasseCriticidade, EixoCriticidade, MatrizCriticidade
from escolio.comentarios.erros import ErroDeComentario
from escolio.comentarios.seletividade import MatrizSeletividade, SelectionDecision
from escolio.comentarios.vocabulario import P13CommentStatus
from escolio.ingestao.modelos import DocumentoIngerido

PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts"

MODEL_ETAPA_8 = "claude-sonnet-5"
EFFORT_ETAPA_8 = "medium"
MODEL_ETAPA_9 = "claude-opus-5"
EFFORT_ETAPA_9 = "high"
MODEL_ETAPAS_16_18 = "claude-sonnet-5"
EFFORT_ETAPAS_16_18 = "medium"

# Nenhuma fonte mede saída esperada por chamada do P13 [docs/custos.md: "output
# por chamada não medido"] — os três tetos abaixo são `[PROPOSTA]` desta
# sessão, generosos por unidade (~150 tok/unidade é a estimativa de
# docs/custos.md para diagnóstico interno; comentário final tende a ser
# maior que diagnóstico interno, daí a folga).
MAX_TOKENS_ETAPA_8 = 8_000
MAX_TOKENS_ETAPA_9 = 8_000
MAX_TOKENS_ETAPAS_16_18 = 8_000


class ErroDePonteModeloP13(Exception):
    """Resposta do modelo não pôde ser traduzida para o dataclass de
    destino — nem toda causa é `ErroDeComentario` (ex.: tool_use ausente,
    JSON malformado); esta classe cobre as demais, mesma disciplina de
    "regra bloqueante levanta exceção" [CLAUDE.md §8]."""


def _ler_prompt(nome_arquivo: str) -> str:
    caminho = PROMPTS_DIR / nome_arquivo
    return caminho.read_text(encoding="utf-8")


def _texto_unidade(unit_id: str, documento: DocumentoIngerido) -> str:
    for p in documento.paragrafos:
        if p.unit_id == unit_id:
            return p.texto
    for c in documento.citacoes_recuadas:
        if c.unit_id == unit_id:
            return c.texto
    for n in documento.notas_de_rodape:
        if n.unit_id == unit_id:
            return n.texto
    for f in documento.figuras:
        if f.unit_id == unit_id:
            return f.legenda or "[figura sem legenda]"
    raise ErroDePonteModeloP13(f"unit_id {unit_id!r} não encontrado no documento")


def _renderizar_documento_estavel(documento: DocumentoIngerido) -> str:
    """Serialização determinística do documento — vira o prefixo `system`
    cacheado. `sort_keys=True` e nenhum timestamp/UUID, por instrução de
    `docs/custos.md` ("invalidadores silenciosos a evitar no prefixo")."""
    unidades = (
        [{"unit_id": p.unit_id, "tipo": "paragrafo", "texto": p.texto} for p in documento.paragrafos]
        + [
            {"unit_id": c.unit_id, "tipo": "citacao_recuada", "texto": c.texto}
            for c in documento.citacoes_recuadas
        ]
        + [
            {"unit_id": n.unit_id, "tipo": "nota_de_rodape", "texto": n.texto}
            for n in documento.notas_de_rodape
        ]
        + [
            {"unit_id": f.unit_id, "tipo": "figura", "texto": f.legenda or "[figura sem legenda]"}
            for f in documento.figuras
        ]
    )
    corpo = {
        "hash_documento": documento.hash_documento,
        "num_paginas": documento.num_paginas,
        "unidades": sorted(unidades, key=lambda u: u["unit_id"]),
    }
    return json.dumps(corpo, ensure_ascii=False, sort_keys=True)


def _extrair_tool_use(blocos: list[dict], nome_ferramenta: str) -> dict:
    for bloco in blocos:
        if bloco.get("type") == "tool_use" and bloco.get("name") == nome_ferramenta:
            entrada = bloco.get("input")
            if not isinstance(entrada, dict):
                raise ErroDePonteModeloP13(
                    f"tool_use {nome_ferramenta!r} sem 'input' em formato de objeto"
                )
            return entrada
    raise ErroDePonteModeloP13(f"resposta do modelo não contém tool_use {nome_ferramenta!r}")


# --- Etapa 8 — matriz de criticidade -----------------------------------

_FERRAMENTA_CRITICIDADE = "registrar_matrizes_criticidade"

_SCHEMA_CRITICIDADE = {
    "name": _FERRAMENTA_CRITICIDADE,
    "description": "Registra os problemas candidatos avaliados nos 12 eixos de criticidade [§11].",
    "input_schema": {
        "type": "object",
        "properties": {
            "matrizes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "problem_id": {"type": "string"},
                        "unit_id": {"type": "string"},
                        "avaliacao_por_eixo": {
                            "type": "object",
                            "properties": {eixo.value: {"type": "string"} for eixo in EixoCriticidade},
                            "required": [eixo.value for eixo in EixoCriticidade],
                        },
                        "classe": {"type": "string", "enum": [c.value for c in ClasseCriticidade]},
                        "justificativa_classe": {"type": "string"},
                    },
                    "required": [
                        "problem_id",
                        "unit_id",
                        "avaliacao_por_eixo",
                        "classe",
                        "justificativa_classe",
                    ],
                },
            }
        },
        "required": ["matrizes"],
    },
}


def gerar_matrizes_criticidade(
    *, documento: DocumentoIngerido, unit_ids: list[str], cliente, ttl_cache: str = "1h", sequence_id: str | None = None
) -> list[MatrizCriticidade]:
    if not unit_ids:
        raise ErroDePonteModeloP13("gerar_matrizes_criticidade exige ao menos um unit_id")

    instrucoes = _ler_prompt("p13_matriz_criticidade.md")
    system_estavel = instrucoes + "\n\n## Documento\n\n" + _renderizar_documento_estavel(documento)
    mensagem = f"Unidades desta chamada: {json.dumps(sorted(unit_ids), ensure_ascii=False)}"

    resultado = cliente.chamar(
        model=MODEL_ETAPA_8,
        system_estavel=system_estavel,
        unidades=[{"type": "text", "text": mensagem}],
        max_tokens=MAX_TOKENS_ETAPA_8,
        effort=EFFORT_ETAPA_8,
        tools=[_SCHEMA_CRITICIDADE],
        ttl_cache=ttl_cache,
        etapa="P13_ETAPA_8_MATRIZ_CRITICIDADE",
        sequence_id=sequence_id,
    )
    entrada = _extrair_tool_use(resultado.blocos, _FERRAMENTA_CRITICIDADE)

    matrizes: list[MatrizCriticidade] = []
    for item in entrada.get("matrizes", []):
        try:
            avaliacao = {EixoCriticidade(k): v for k, v in item["avaliacao_por_eixo"].items()}
            matrizes.append(
                MatrizCriticidade(
                    problem_id=item["problem_id"],
                    unit_id=item["unit_id"],
                    avaliacao_por_eixo=avaliacao,
                    classe=ClasseCriticidade(item["classe"]),
                    justificativa_classe=item["justificativa_classe"],
                )
            )
        except (KeyError, ValueError, ErroDeComentario) as erro:
            raise ErroDePonteModeloP13(
                f"resposta do modelo para {_FERRAMENTA_CRITICIDADE!r} não corresponde a MatrizCriticidade: {erro}"
            ) from erro
    return matrizes


# --- Etapa 9 — matriz de seletividade -----------------------------------

_FERRAMENTA_SELETIVIDADE = "registrar_matrizes_seletividade"

_SCHEMA_SELETIVIDADE = {
    "name": _FERRAMENTA_SELETIVIDADE,
    "description": "Registra a avaliação de seletividade [§12] e a decisão de seleção [§10].",
    "input_schema": {
        "type": "object",
        "properties": {
            "matrizes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "selection_id": {"type": "string"},
                        "unit_id": {"type": "string"},
                        "candidate_problem_id": {"type": "string"},
                        "criticality": {"type": "string", "enum": [c.value for c in ClasseCriticidade]},
                        "material_impact": {"type": "string"},
                        "novelty": {"type": "string"},
                        "recurrence": {"type": "string"},
                        "matrix_comment_coverage": {"type": "string"},
                        "actionability": {"type": "string"},
                        "evidence_sufficiency": {"type": "string"},
                        "human_decision_required": {"type": "string"},
                        "privacy_risk": {"type": "string"},
                        "selection_decision": {
                            "type": "string",
                            "enum": [d.value for d in SelectionDecision],
                        },
                        "selection_rationale": {"type": "string"},
                    },
                    "required": [
                        "selection_id",
                        "unit_id",
                        "candidate_problem_id",
                        "criticality",
                        "material_impact",
                        "novelty",
                        "recurrence",
                        "matrix_comment_coverage",
                        "actionability",
                        "evidence_sufficiency",
                        "human_decision_required",
                        "privacy_risk",
                        "selection_decision",
                        "selection_rationale",
                    ],
                },
            }
        },
        "required": ["matrizes"],
    },
}


def gerar_matrizes_seletividade(
    *,
    documento: DocumentoIngerido,
    matrizes_criticidade: list[MatrizCriticidade],
    cliente,
    ttl_cache: str = "1h",
    sequence_id: str | None = None,
) -> list[MatrizSeletividade]:
    if not matrizes_criticidade:
        raise ErroDePonteModeloP13("gerar_matrizes_seletividade exige ao menos uma MatrizCriticidade")

    instrucoes = _ler_prompt("p13_matriz_seletividade.md")
    system_estavel = instrucoes + "\n\n## Documento\n\n" + _renderizar_documento_estavel(documento)
    candidatos = [
        {"problem_id": m.problem_id, "unit_id": m.unit_id, "classe": m.classe.value}
        for m in matrizes_criticidade
    ]
    mensagem = f"Problemas candidatos desta chamada: {json.dumps(candidatos, ensure_ascii=False, sort_keys=True)}"

    resultado = cliente.chamar(
        model=MODEL_ETAPA_9,
        system_estavel=system_estavel,
        unidades=[{"type": "text", "text": mensagem}],
        max_tokens=MAX_TOKENS_ETAPA_9,
        effort=EFFORT_ETAPA_9,
        tools=[_SCHEMA_SELETIVIDADE],
        ttl_cache=ttl_cache,
        etapa="P13_ETAPA_9_MATRIZ_SELETIVIDADE",
        sequence_id=sequence_id,
    )
    entrada = _extrair_tool_use(resultado.blocos, _FERRAMENTA_SELETIVIDADE)

    matrizes: list[MatrizSeletividade] = []
    for item in entrada.get("matrizes", []):
        try:
            matrizes.append(
                MatrizSeletividade(
                    selection_id=item["selection_id"],
                    unit_id=item["unit_id"],
                    candidate_problem_id=item["candidate_problem_id"],
                    criticality=ClasseCriticidade(item["criticality"]),
                    material_impact=item["material_impact"],
                    novelty=item["novelty"],
                    recurrence=item["recurrence"],
                    matrix_comment_coverage=item["matrix_comment_coverage"],
                    actionability=item["actionability"],
                    evidence_sufficiency=item["evidence_sufficiency"],
                    human_decision_required=item["human_decision_required"],
                    privacy_risk=item["privacy_risk"],
                    selection_decision=SelectionDecision(item["selection_decision"]),
                    selection_rationale=item["selection_rationale"],
                )
            )
        except (KeyError, ValueError, ErroDeComentario) as erro:
            raise ErroDePonteModeloP13(
                f"resposta do modelo para {_FERRAMENTA_SELETIVIDADE!r} não corresponde a MatrizSeletividade: {erro}"
            ) from erro
    return matrizes


# --- Etapas 16-18 — elaboração de comentários ----------------------------

_FERRAMENTA_COMENTARIOS = "registrar_comentarios"

_SCHEMA_COMENTARIOS = {
    "name": _FERRAMENTA_COMENTARIOS,
    "description": "Registra os comentários elaborados para os candidatos selecionados [§13, §31.5].",
    "input_schema": {
        "type": "object",
        "properties": {
            "comentarios": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "comment_id": {"type": "string"},
                        "selection_id": {"type": "string"},
                        "unit_id": {"type": "string"},
                        "anchor_start": {"type": "string"},
                        "anchor_end": {"type": "string"},
                        "anchor_text_hash": {"type": "string"},
                        "comment_type": {"type": "string"},
                        "priority": {"type": "string"},
                        "severity": {"type": "string"},
                        "problem": {"type": "string"},
                        "evidence": {"type": "string"},
                        "impact": {"type": "string"},
                        "recommended_action": {"type": "string"},
                        "intervention_level": {"type": "string"},
                        "authority_required": {"type": "string"},
                        "gate": {"type": "string"},
                        "source_status": {"type": "string"},
                        "voice_impact": {"type": "string"},
                        "privacy_classification": {"type": "string"},
                        "reversible": {"type": "boolean"},
                        "matrix_comment_id": {"type": ["string", "null"]},
                    },
                    "required": [
                        "comment_id",
                        "selection_id",
                        "unit_id",
                        "anchor_start",
                        "anchor_end",
                        "anchor_text_hash",
                        "comment_type",
                        "priority",
                        "severity",
                        "problem",
                        "evidence",
                        "impact",
                        "recommended_action",
                        "intervention_level",
                        "authority_required",
                        "gate",
                        "source_status",
                        "voice_impact",
                        "privacy_classification",
                        "reversible",
                    ],
                },
            }
        },
        "required": ["comentarios"],
    },
}


def gerar_comentarios(
    *,
    documento: DocumentoIngerido,
    document_id: str,
    document_version: str,
    module_id: str,
    candidatos: list[MatrizSeletividade],
    cliente,
    comment_type_esperado: str | None = None,
    matrix_comment_id_por_candidato: dict[str, str] | None = None,
    ttl_cache: str = "1h",
    sequence_id: str | None = None,
) -> list[P13Comment]:
    """Elabora comentários para `candidatos` (saída da etapa 10, um por
    `MatrizSeletividade`). `comment_type_esperado`, quando fornecido,
    restringe o `comment_type` aceito de cada item — mesma checagem que
    `_etapa_elaboracao` já aplica em `execucao_p13.py`; repetida aqui para
    falhar o mais perto possível da causa, antes de a etapa validar de
    novo.

    `matrix_comment_id_por_candidato` (chave `selection_id`) é para a
    etapa 18 (remissões): a ligação entre remissão e comentário-matriz não
    tem regra de fonte que a derive do conteúdo [nenhuma seção do contrato
    automatiza essa referência] — quem chama já decidiu qual
    comentário-matriz cada remissão referencia (mesma disciplina do
    parâmetro `remissoes` pré-construído que `_etapa_elaboracao` já aceita
    em `execucao_p13.py`); o valor do modelo para `matrix_comment_id` é
    substituído pelo valor autoritativo do chamador, nunca o inverso."""
    if not candidatos:
        raise ErroDePonteModeloP13("gerar_comentarios exige ao menos um candidato selecionado")

    instrucoes = _ler_prompt("p13_elaboracao_comentarios.md")
    system_estavel = instrucoes + "\n\n## Documento\n\n" + _renderizar_documento_estavel(documento)
    candidatos_json = [
        {
            "selection_id": c.selection_id,
            "unit_id": c.unit_id,
            "candidate_problem_id": c.candidate_problem_id,
            "criticality": c.criticality.value,
            "selection_rationale": c.selection_rationale,
        }
        for c in candidatos
    ]
    mensagem = f"Candidatos selecionados desta chamada: {json.dumps(candidatos_json, ensure_ascii=False, sort_keys=True)}"

    resultado = cliente.chamar(
        model=MODEL_ETAPAS_16_18,
        system_estavel=system_estavel,
        unidades=[{"type": "text", "text": mensagem}],
        max_tokens=MAX_TOKENS_ETAPAS_16_18,
        effort=EFFORT_ETAPAS_16_18,
        tools=[_SCHEMA_COMENTARIOS],
        ttl_cache=ttl_cache,
        etapa="P13_ETAPAS_16_18_ELABORACAO_COMENTARIOS",
        sequence_id=sequence_id,
    )
    entrada = _extrair_tool_use(resultado.blocos, _FERRAMENTA_COMENTARIOS)

    matrix_comment_id_por_candidato = matrix_comment_id_por_candidato or {}
    comentarios: list[P13Comment] = []
    for item in entrada.get("comentarios", []):
        try:
            if comment_type_esperado is not None and item["comment_type"] != comment_type_esperado:
                raise ErroDePonteModeloP13(
                    f"comment_type {item['comment_type']!r} do modelo diverge do esperado "
                    f"{comment_type_esperado!r} para esta etapa"
                )
            matrix_comment_id = matrix_comment_id_por_candidato.get(
                item["selection_id"], item.get("matrix_comment_id")
            )
            comentarios.append(
                P13Comment(
                    comment_id=item["comment_id"],
                    document_id=document_id,
                    document_version=document_version,
                    module_id=module_id,
                    unit_id=item["unit_id"],
                    anchor_start=item["anchor_start"],
                    anchor_end=item["anchor_end"],
                    anchor_text_hash=item["anchor_text_hash"],
                    comment_type=item["comment_type"],
                    priority=item["priority"],
                    severity=item["severity"],
                    problem=item["problem"],
                    evidence=item["evidence"],
                    impact=item["impact"],
                    recommended_action=item["recommended_action"],
                    intervention_level=item["intervention_level"],
                    authority_required=item["authority_required"],
                    gate=item["gate"],
                    source_status=item["source_status"],
                    voice_impact=item["voice_impact"],
                    privacy_classification=item["privacy_classification"],
                    reversible=item["reversible"],
                    status=P13CommentStatus.DRAFT,
                    matrix_comment_id=matrix_comment_id,
                )
            )
        except (KeyError, ValueError, ErroDeComentario) as erro:
            raise ErroDePonteModeloP13(
                f"resposta do modelo para {_FERRAMENTA_COMENTARIOS!r} não corresponde a P13Comment: {erro}"
            ) from erro
    return comentarios

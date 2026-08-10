"""Ponte entre `escolio/funcoes/execucao_p11.py` e `escolio/cliente/` —
liga o ponto de extensão de modelo da etapa 6 (diagnóstico de
estabilidade) à API.

Escopo desta sessão: só esta etapa. As etapas 7-22 continuam
`PONTO_DE_EXTENSAO_DE_MODELO`/`SEM_FONTE_DE_VERIFICACAO` — cada uma
exigiria seu próprio prompt e schema de saída, e nenhuma foi definida
aqui [ver docstring de `execucao_p11.py`].

Modelo e `effort` — CLAUDE.md §10, tabela "Modelos e custo": E4 diagnóstico
por unidade é Sonnet, `medium`. Diagnóstico de estabilidade é a primeira
etapa de E4 e opera sobre a obra inteira (não por unidade), mas nenhuma
fonte justifica um modelo mais caro para esta etapa especificamente — usa-
se a linha E4 da tabela.

Saída modelada como `escolio.contrato.afirmacao.ClaimEvidence` [P09 §12],
não um objeto novo — a pergunta que esta etapa faz ("a obra está estável?")
produz exatamente achados com afirmação, suficiência de evidência e
confiança, que é o vocabulário que o P09 já declara para isso. Nenhum
achado desta etapa usa `status=CONFLICTED`: esta etapa diagnostica
estabilidade do projeto intelectual, não concilia fontes divergentes — se
uma sessão futura precisar de `CONFLICTED` aqui, ela terá de resolver
`source_references` também, que este schema não pede.

Prompt em `prompts/p11_diagnostico_estabilidade.md`, lido em disco a cada
chamada — nunca hardcoded aqui [CLAUDE.md §12].

Erro de validação do dataclass é regra bloqueante — propaga como
`ErroDePonteModeloP11`, nunca é engolido [CLAUDE.md §8].
"""

from __future__ import annotations

import json
from pathlib import Path

from escolio.contrato.afirmacao import ClaimEvidence
from escolio.contrato.erros import ErroDeContrato
from escolio.contrato.referencia import Location
from escolio.contrato.vocabulario import ClaimStatus, ClaimType, Confidence, Sufficiency
from escolio.ingestao.modelos import DocumentoIngerido
from escolio.ingestao.vocabulario import NivelHierarquia

PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts"

MODEL_ETAPA_6 = "claude-sonnet-5"
EFFORT_ETAPA_6 = "medium"

# Nenhuma fonte mede saída esperada para esta etapa. 8.000 (valor original
# desta sessão, mesmo raciocínio de generosidade de `ponte_modelo_p13.py`)
# se mostrou insuficiente no piloto real de 2026-08-09 contra os 3
# capítulos: o teto foi consumido inteiro por `thinking` antes de gerar
# qualquer conteúdo de saída (`stop_reason=max_tokens`, `tool_use.input={}`
# vazio) — `max_tokens` limita raciocínio + resposta juntos [docs/custos.md],
# e esta etapa opera sobre a obra inteira (~116k tokens de prefixo), não uma
# unidade isolada como as etapas de P13 que calibraram o valor original.
# 16.000 é o novo teto — não medido contra uma execução bem-sucedida ainda
# (só evita reproduzir o truncamento observado); revisar após confirmar que
# uma chamada real completa dentro dele. Acima deste valor o cliente já usa
# streaming (`_LIMIAR_STREAMING_TOKENS`), então não há custo extra de infra
# em usar exatamente esse número.
MAX_TOKENS_ETAPA_6 = 16_000

_STATUS_ACEITOS = (ClaimStatus.SUPPORTED, ClaimStatus.PARTIALLY_SUPPORTED, ClaimStatus.UNSUPPORTED)


class ErroDePonteModeloP11(Exception):
    """Resposta do modelo não pôde ser traduzida para `ClaimEvidence` —
    nem toda causa é `ErroDeContrato` (ex.: tool_use ausente, JSON
    malformado); esta classe cobre as demais, mesma disciplina de "regra
    bloqueante levanta exceção" [CLAUDE.md §8]."""


def _ler_prompt(nome_arquivo: str) -> str:
    caminho = PROMPTS_DIR / nome_arquivo
    return caminho.read_text(encoding="utf-8")


def _capitulo_ordinal_por_secao_id(documento: DocumentoIngerido) -> dict[str, int]:
    """Mapa `secao_id -> ordinal do capítulo` (1-based, ordem de leitura),
    resolvendo tanto o próprio `Secao` de nível CAPITULO quanto suas
    seções filhas via `Secao.secao_pai_id`.

    Existe para que o modelo consiga ligar uma autorreferência do autor
    ("será trabalhado no capítulo 3") ao arquivo real que ocupa essa
    posição numa obra combinada de vários arquivos — sem este rótulo, o
    piloto real de 2026-08-09 produziu dois falsos positivos (EST-03,
    EST-04: "capítulo 3 não está no material fornecido", quando estava —
    ver `escolio/funcoes/LACUNAS.md`)."""
    ordinal_por_capitulo: dict[str, int] = {}
    for s in documento.secoes:
        if s.nivel is NivelHierarquia.CAPITULO:
            ordinal_por_capitulo[s.unit_id] = len(ordinal_por_capitulo) + 1
    mapa: dict[str, int] = {}
    for s in documento.secoes:
        if s.nivel is NivelHierarquia.CAPITULO:
            mapa[s.unit_id] = ordinal_por_capitulo[s.unit_id]
        elif s.secao_pai_id in ordinal_por_capitulo:
            mapa[s.unit_id] = ordinal_por_capitulo[s.secao_pai_id]
    return mapa


def _renderizar_documento_estavel(documento: DocumentoIngerido) -> str:
    """Serialização determinística do documento — vira o prefixo `system`
    cacheado. `sort_keys=True` e nenhum timestamp/UUID, por instrução de
    `docs/custos.md` ("invalidadores silenciosos a evitar no prefixo").

    Cada unidade traz `capitulo` (ordinal 1-based, `None` quando não
    resolvível — unidade sem `secao_id`, ou nota cujo chamador não tem
    `secao_id`) — ver `_capitulo_ordinal_por_secao_id`."""
    capitulo_por_secao = _capitulo_ordinal_por_secao_id(documento)
    secao_id_por_unit: dict[str, str | None] = {p.unit_id: p.secao_id for p in documento.paragrafos}
    secao_id_por_unit.update({c.unit_id: c.secao_id for c in documento.citacoes_recuadas})

    def capitulo_de(secao_id: str | None) -> int | None:
        return capitulo_por_secao.get(secao_id) if secao_id else None

    unidades = (
        [
            {
                "unit_id": p.unit_id,
                "tipo": "paragrafo",
                "texto": p.texto,
                "capitulo": capitulo_de(p.secao_id),
            }
            for p in documento.paragrafos
        ]
        + [
            {
                "unit_id": c.unit_id,
                "tipo": "citacao_recuada",
                "texto": c.texto,
                "capitulo": capitulo_de(c.secao_id),
            }
            for c in documento.citacoes_recuadas
        ]
        + [
            {
                "unit_id": n.unit_id,
                "tipo": "nota_de_rodape",
                "texto": n.texto,
                "capitulo": capitulo_de(secao_id_por_unit.get(n.unit_id_chamador)),
            }
            for n in documento.notas_de_rodape
        ]
        + [
            {
                "unit_id": f.unit_id,
                "tipo": "figura",
                "texto": f.legenda or "[figura sem legenda]",
                "capitulo": None,
            }
            for f in documento.figuras
        ]
    )
    corpo = {
        "hash_documento": documento.hash_documento,
        "num_paginas": documento.num_paginas,
        "num_capitulos": len(set(capitulo_por_secao.values())) or None,
        "unidades": sorted(unidades, key=lambda u: u["unit_id"]),
    }
    return json.dumps(corpo, ensure_ascii=False, sort_keys=True)


def _extrair_tool_use(blocos: list[dict], nome_ferramenta: str) -> dict:
    for bloco in blocos:
        if bloco.get("type") == "tool_use" and bloco.get("name") == nome_ferramenta:
            entrada = bloco.get("input")
            if not isinstance(entrada, dict):
                raise ErroDePonteModeloP11(
                    f"tool_use {nome_ferramenta!r} sem 'input' em formato de objeto"
                )
            return entrada
    raise ErroDePonteModeloP11(f"resposta do modelo não contém tool_use {nome_ferramenta!r}")


# --- Etapa 6 — diagnóstico de estabilidade -------------------------------

_FERRAMENTA_DIAGNOSTICO = "registrar_diagnostico_de_estabilidade"

_SCHEMA_DIAGNOSTICO = {
    "name": _FERRAMENTA_DIAGNOSTICO,
    "description": (
        "Registra os achados de estabilidade do projeto intelectual da obra "
        "(objetivo, hipótese, corpus) [P11 §2]."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "achados": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "claim_id": {"type": "string"},
                        "claim_text": {"type": "string"},
                        "claim_type": {"type": "string", "enum": [t.value for t in ClaimType]},
                        "sufficiency": {"type": "string", "enum": [s.value for s in Sufficiency]},
                        "confidence": {"type": "string", "enum": [c.value for c in Confidence]},
                        "status": {"type": "string", "enum": [s.value for s in _STATUS_ACEITOS]},
                        "evidence_ids": {"type": "array", "items": {"type": "string"}},
                        "location_section": {"type": ["string", "null"]},
                        "notes": {"type": ["string", "null"]},
                    },
                    "required": [
                        "claim_id",
                        "claim_text",
                        "claim_type",
                        "sufficiency",
                        "confidence",
                        "status",
                        "evidence_ids",
                    ],
                },
            }
        },
        "required": ["achados"],
    },
}


def gerar_diagnostico_de_estabilidade(
    *, documento: DocumentoIngerido, cliente, ttl_cache: str = "1h", sequence_id: str | None = None
) -> list[ClaimEvidence]:
    instrucoes = _ler_prompt("p11_diagnostico_estabilidade.md")
    system_estavel = instrucoes + "\n\n## Documento\n\n" + _renderizar_documento_estavel(documento)
    mensagem = "Avalie a estabilidade do projeto intelectual da obra inteira acima."

    resultado = cliente.chamar(
        model=MODEL_ETAPA_6,
        system_estavel=system_estavel,
        unidades=[{"type": "text", "text": mensagem}],
        max_tokens=MAX_TOKENS_ETAPA_6,
        effort=EFFORT_ETAPA_6,
        tools=[_SCHEMA_DIAGNOSTICO],
        ttl_cache=ttl_cache,
        etapa="P11_ETAPA_6_DIAGNOSTICO_DE_ESTABILIDADE",
        sequence_id=sequence_id,
    )
    entrada = _extrair_tool_use(resultado.blocos, _FERRAMENTA_DIAGNOSTICO)

    achados: list[ClaimEvidence] = []
    for item in entrada.get("achados", []):
        try:
            achados.append(
                ClaimEvidence(
                    claim_id=item["claim_id"],
                    claim_text=item["claim_text"],
                    claim_type=ClaimType(item["claim_type"]),
                    sufficiency=Sufficiency(item["sufficiency"]),
                    confidence=Confidence(item["confidence"]),
                    status=ClaimStatus(item["status"]),
                    evidence_ids=list(item["evidence_ids"]),
                    location=Location(section=item.get("location_section")),
                    notes=item.get("notes"),
                )
            )
        except (KeyError, ValueError, ErroDeContrato) as erro:
            raise ErroDePonteModeloP11(
                f"resposta do modelo para {_FERRAMENTA_DIAGNOSTICO!r} não corresponde a "
                f"ClaimEvidence: {erro}"
            ) from erro
    return achados

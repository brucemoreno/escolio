"""Salvaguarda residual de privacidade — Etapa 14 do P13.

Resolve `CO-012` nos termos restritos de
`INSTRUCOES_COMPLEMENTARES_IMPLEMENTACAO_ECOSSISTEMA_REVISAO_LLM_R01.md §2`
(doravante "Instruções Complementares"). Regra central, verbatim [§2.1]:

    SENSIBILIDADE_TEMATICA != RISCO_DE_PRIVACIDADE

Uma tese em História/Humanidades pode tratar de violência, doença,
sexualidade, religião, racismo, guerra — a presença desses temas não é,
por si só, risco de privacidade e não aciona nada aqui. Este módulo nunca
lê tema; só padrão textual literal de dado pessoal direto.

## Por que não é gate, e nunca bloqueia [§2.2, §2.5]

`INSTRUCOES_COMPLEMENTARES...§2.2`: "NÃO IMPLEMENTAR filtro ou gate
obrigatório de privacidade sobre cada trecho ou comentário do fluxo
normal de revisão." Por isso `detectar_exposicao_manifesta` nunca
levanta exceção sobre o conteúdo do texto analisado (só sobre uso
indevido da própria função, ex. `unit_id` vazio) e nunca devolve algo
que outro módulo possa tratar como obrigação de parar — apenas achados,
sempre não bloqueantes, para alerta.

## Escopo desta implementação — só os gatilhos deterministicamente detectáveis

`§2.4` lista oito gatilhos admissíveis para a salvaguarda. Este módulo
cobre, com padrão literal e baixo risco de falso positivo:

- CPF formatado (`000.000.000-00`);
- e-mail;
- telefone brasileiro formatado com DDD entre parênteses.

Os demais gatilhos de §2.4 — endereço residencial, "identidade
explicitamente protegida/anonimizada no material de origem", "informação
marcada como confidencial/restrita/sob sigilo", "dado cuja reprodução
aumentaria exposição" — exigem leitura semântica ou de metadados de
proveniência que nenhum padrão determinístico cobre com segurança sem
calibração contra caso real. Não adivinhados aqui [CLAUDE.md §11] —
registrados como não cobertos em `escolio/funcoes/LACUNAS.md`.

## Reaproveitamento

`SensitivityLabel`/`SensitivityCategory` são os já existentes em
`escolio.contrato` [P09 §20] — nenhum vocabulário novo de sensibilidade
foi criado; `PERSONAL_DATA` já cobre exatamente o que os três padrões
acima detectam.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from escolio.contrato.payloads import SensitivityLabel
from escolio.contrato.vocabulario import SensitivityCategory

ORIGEM_DECISAO = (
    "INSTRUCOES_COMPLEMENTARES_IMPLEMENTACAO_ECOSSISTEMA_REVISAO_LLM_R01.md §2 (CO-012, "
    "RESOLVIDO_COM_RESTRICAO_DE_ESCOPO)"
)

_PADRAO_CPF = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
_PADRAO_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_PADRAO_TELEFONE_BR_COM_DDD = re.compile(r"\(\d{2}\)\s?\d{4,5}-?\d{4}\b")

_PADROES_POR_MOTIVO: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("CPF", _PADRAO_CPF),
    ("E_MAIL", _PADRAO_EMAIL),
    ("TELEFONE_BR_FORMATADO", _PADRAO_TELEFONE_BR_COM_DDD),
)


def _mascarar(trecho: str) -> str:
    """Nunca reproduz o valor real [§2.5: "evitar reproduzir
    desnecessariamente o valor sensível"] — preserva só o primeiro e o
    último caractere, para confirmar o achado numa auditoria sem expor o
    dado."""
    if len(trecho) <= 2:
        return "*" * len(trecho)
    return trecho[0] + "*" * (len(trecho) - 2) + trecho[-1]


@dataclass(frozen=True)
class AlertaDePrivacidade:
    """Achado da salvaguarda residual — sempre não bloqueante [§2.5].
    `trecho_mascarado` nunca é o valor real encontrado (ver `_mascarar`);
    `posicao` é o índice de caractere no texto da unidade analisada."""

    unit_id: str
    posicao: int
    trecho_mascarado: str
    label: SensitivityLabel


def detectar_exposicao_manifesta(unit_id: str, texto: str) -> list[AlertaDePrivacidade]:
    """Só os três gatilhos deterministicamente detectáveis de `§2.4` —
    nunca por tema [§2.1, §2.6]. Lista vazia é o resultado normal e
    esperado para a imensa maioria dos trechos de uma tese em
    Humanidades — ausência de achado não é ausência de verificação."""
    if not unit_id:
        raise ValueError("detectar_exposicao_manifesta exige unit_id não vazio")
    alertas: list[AlertaDePrivacidade] = []
    for motivo, padrao in _PADROES_POR_MOTIVO:
        for match in padrao.finditer(texto):
            alertas.append(
                AlertaDePrivacidade(
                    unit_id=unit_id,
                    posicao=match.start(),
                    trecho_mascarado=_mascarar(match.group()),
                    label=SensitivityLabel(
                        category=SensitivityCategory.PERSONAL_DATA,
                        source_policy=ORIGEM_DECISAO,
                        justification=f"padrão determinístico {motivo} — nunca por tema [§2.1]",
                    ),
                )
            )
    return alertas

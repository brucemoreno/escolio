"""Roteador de função e etapas por função — item 6 do roadmap.

Fontes:
- Catálogo funcional (as seis unidades, F01-F05 + X01):
  corpus/handoff-P22/PACOTE_HANDOFF_REQUISITOS_ENGENHEIRO_LLM_R01/FONTES_CANONICAS/
  PACOTE_CONTRATO_CIENTISTA_ACADEMICO_LLM_R01/ (P02).
- Contratos funcionais P10-P14, um por pacote PACOTE_FUNCAO_*, no mesmo
  diretório FONTES_CANONICAS/.
- Estrutura obrigatória de declaração de função: R03 CAMADA B,
  PACOTE_PROTOCOLO_MESTRE_ACAO_ECOSSISTEMA_LLM_ACADEMICA_R03/01_*.md.
- Regras de correspondência do envelope: P09 §4.2, §8.1.

O QUE ESTA PEÇA FAZ: fornece o catálogo fechado que o P09 §4.2.3-4.2.5
pressupõe e que `escolio/contrato/LACUNAS.md` deixou explicitamente
reservado para "quando o roteador de função (roadmap, item 6) existir".

O QUE ELA NÃO FAZ: escolher a função. Nenhuma fonte — nem o P02, nem
qualquer dos cinco contratos — define como se determina que uma função,
e não outra, se aplica a um documento. `GATE_DE_ATIVACAO_P10…P14` ocorre
uma única vez em cada contrato, como item nu de lista, sem definição. A
seleção chega declarada em `request.function_id` e em
`InputItem.classification.functions`; o roteador confere e recusa, nunca
elege. Não existe `selecionar_funcao` — a ausência é o mecanismo
[POL-007: "acao_proibida: Inferir próxima fase, componente ou operação"].

Reusa escolio/contrato/ (InputItem, AbstentionCategory, AbstentionPayload,
Request, Response) — não duplica enum, dataclass nem validação existente.
Não altera nenhum arquivo já escrito; as integrações que exigiriam alterar
`escolio/contrato/resposta.py` estão em docs/backlog.md. Ver LACUNAS.md
desta peça.
"""

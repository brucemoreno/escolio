"""Contrato de runtime P09 — envelope universal de requisição e resposta.

Fonte: P09_SCHEMAS_CONTRATOS_CORRIGIDO_R04.md, em
corpus/handoff-P22/PACOTE_HANDOFF_REQUISITOS_ENGENHEIRO_LLM_R01/FONTES_CANONICAS/
PACOTE_CONTRATO_STATUS_LLM_ACADEMICA_R01/.

Escopo desta peça (item 1 do roadmap): Reference, InputItem, o envelope de
resposta com os cinco status mutuamente exclusivos, os três payloads
(ErrorPayload, AbstentionPayload, BlockPayload) e os invariantes do §21 como
validação que rejeita. ClaimEvidence (§12) entra por ser parte declarada do
envelope de resposta (§8, campo `evidence.claims`).

InterventionRecord (§13) NÃO entra — é item 2 do roadmap, junto com os
níveis P06."""

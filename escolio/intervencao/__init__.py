"""Níveis de intervenção P06 e InterventionRecord — item 2 do roadmap.

Fontes:
- P06 (níveis, cadeia, gates, escalonamento, regressão, congelamento):
  corpus/handoff-P22/PACOTE_HANDOFF_REQUISITOS_ENGENHEIRO_LLM_R01/FONTES_CANONICAS/
  PACOTE_TAXONOMIA_INTERVENCAO_LLM_ACADEMICA_R01/.
- InterventionRecord (§13): P09_SCHEMAS_CONTRATOS_CORRIGIDO_R04.md, em
  PACOTE_CONTRATO_STATUS_LLM_ACADEMICA_R01/.

Reusa escolio/contrato/ (ErroDeContrato, AuthorizationStatus, Reference) —
não duplica enum nem validação já existente ali. Ver LACUNAS.md desta peça.
"""

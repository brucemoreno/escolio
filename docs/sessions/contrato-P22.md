# Sessão — Mapeamento do contrato P22

**Tema único:** ler e mapear `corpus/handoff-P22/.../01_P22_CONTRATO_DOCUMENTAL_FUNCIONAL_INTEGRAL_CORRIGIDO_R01.md` (2949 linhas). Nenhuma outra ação executada.

## O que foi mapeado

Entregável: `docs/spec/contrato-P22.md` — obrigações e proibições do contrato, matriz de aplicabilidade P00-P21, decisões abertas (lacunas legítimas), confronto com `handoff/maquina.js`, `escolio/regras_coerencia.py`+`registro.py`, `escolio/ingestao/`, impacto no CLAUDE.md (seções obsoletas, vocabulário a absorver, contradições, cobertura exclusiva de cada lado), 5 perguntas ao professor.

## Divergência identificada (não resolvida)

O comando desta sessão afirma que P23 foi autorizado; o próprio texto do P22 (linha 10, §72) declara P23 não iniciado e todos os 11 gates `DEFINIDO_NAO_CONCEDIDO`. Registrado em `docs/spec/contrato-P22.md` §5 e como pergunta 1 — não escolhi entre as duas versões.

## Pendências

5 perguntas concretas para o professor em `docs/spec/contrato-P22.md` §7, principalmente: status real da autorização de P23; se o CLAUDE.md atual (pipeline/modelos/linguagem) deve ser tratado como decisão técnica já autorizada ou como hipótese a revisitar.

## Riscos abertos

- `escolio/ingestao/` e o schema `escolio/` (afirmação-evidência) não correspondem a nenhum P-número do inventário P22 — mapeamento retroativo pendente (pergunta 5).
- Renumeração canônica (P02-P05) fornecida no comando não pôde ser verificada contra hashes reais nesta sessão — o P22 declara não calcular hashes.

## Custo

Sem chamadas de API de modelo do produto (LLM_ACADEMICA). Custo desta sessão é de tokens de leitura/raciocínio da sessão de desenvolvimento, não rastreado em `costs/ledger.jsonl` (esse ledger é para execuções do pipeline do produto, não para sessões de engenharia).

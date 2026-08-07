# Coleta pendente

Material e decisões que dependem do professor. **Não é backlog** — é dependência externa: item
bloqueante aqui impede a sessão correspondente de produzir resultado válido, mesmo que ela rode
sem erro.

Consultar antes de iniciar qualquer sessão que dependa de corpus ou de perfil de voz.

Aberto em 2026-08-06.

---

## Bloqueantes

### CO-001 — Decisão sobre o eixo 7 (voz de quem comenta)
**Bloqueia:** perfil de voz do professor; destino de `style/style_card.md`; item 5 do roadmap.
**O que falta:** decisão entre as duas leituras registradas em `docs/spec/divergencias.md` §4.1.
Não é material a coletar — é decisão a tomar.

### CO-002 — Amostras de correção do professor
**Bloqueia:** `PERFIL_AUTORAL_DERIVADO_DE_AMOSTRAS` e `PERFIL_HIBRIDO_DECLARACAO_MAIS_AMOSTRAS`
[P07/04], que exigem "múltiplas amostras autorizadas" com proveniência.
**O que falta:** capítulo corrigido com diff, ou conjunto equivalente de correções dele.
**Condicionado a:** CO-001 — só faz sentido coletar se a resposta for que o perfil de quem
comenta existe.
**Nota:** perfil derivado exige gate `GATE_AMOSTRAS` e confiança justificada por evidência
[P07/04]; uma amostra isolada não define voz [P07/01, Calibração].

### CO-003 — Comentários já aceitos e histórico de resolução
**Não bloqueia o desenho; bloqueia a calibragem.** São entradas opcionais do P13 §6.3
(`exemplos de comentários aceitos`, `histórico de resolução`) e o mecanismo pelo qual o sistema
se calibra pelo que o professor de fato comenta.
**O que falta:** conjunto de comentários dele com o resultado de cada um (`ACEITO`, `RECUSADO`).
**Pendência associada:** se *armazenar* esse material é livre sob o P19 ainda não foi verificado
— item 6 da lista ABERTO do CLAUDE.md. O P13 §6.3 autoriza como *entrada*; retenção é P19.

### CO-004 — Base de consentimento para `data/`
**Bloqueia:** qualquer uso de `data/gold/` além de contagem, e qualquer envio de material de
aluno à API.
**O que falta:** o próprio documento. O CLAUDE.md anterior referenciava `docs/dados.md`, que
nunca existiu. `data/gold/tese_natalia.pdf` tem o nome do autor no próprio arquivo, contra a
regra de anonimização na ingestão.
**Decisão associada:** autorizar ou não rodar o parser sobre `data/gold/` para contar unidades
(BL-008).

---

## Não bloqueantes, mas em aberto

### CO-005 — Cobertura de capítulo de livro e relatório de pós-doutorado
Nenhum dos dois tem função em P10–P14, e nem aparece entre as quatro funções candidatas do
R03 CAMADA B. Decidir: P15+, generalização autorizada de P11, ou fora do escopo do produto.
Enquanto não decidir, o sistema responde `ABSTAINED/OUT_OF_SCOPE` para esses tipos.

### CO-006 — Revisão de artigo antes da submissão
Função **candidata, não incorporada** [R03 CAMADA B]. Incorporar exige nova fonte e decisão
autoral específica [`LAC-P02-005`].

### CO-007 — Forma da carta branca
`docs/autorizacao.md` é ato coletivo cobrindo doze decisões; o `P01/05` proíbe "emitir
autorização coletiva". Ver `docs/spec/divergencias.md` §4.2. Reemitir em forma itemizada resolve
sob qualquer das duas leituras.

### CO-008 — Estado de auditoria de P10, P12, P13 e P14
Os quatro permanecem `NAO_AUDITADO_APOS_CORRECAO` ou equivalente; só o P11 está homologado
documentalmente. Qualquer leitura futura deve verificar se revisões `R02`+ substituíram os
arquivos lidos até aqui.

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

### CO-009 — Par capítulo→artigo real, autor identificável (P10)
**Bloqueia:** qualquer ingestão ou processamento do material informado em 2026-08-07:
`ANTES_CAPITULOS_1_E_2_DISsertacao_INTEGRAL.pdf`, `ANTES_CAPITULO_3_INTEGRAL.docx`,
`DEPOIS_CAPITULOS_1_2_E_3_ARTIGOS_INTEGRAIS.docx`. Nenhum dos três está em `data/`; nenhum foi
lido.
**Não é o CO-002.** Este par não é correção incremental sobre o mesmo texto — é dois capítulos
de dissertação (antes) e três artigos derivados (depois). Objeto do **P10** (derivação editorial
de capítulo em artigos), não de calibragem de voz de quem comenta.
**O que falta, por campo de `MaterialUnit`** [P19 §9, mapa-P19.md §2]: `owner_or_controller`
(titular/autor informa), `license_status` (titular informa), `authorization_basis` e
`authorized_purposes` (`USUARIO_PROPONENTE` emite — nenhum dos dois foi emitido). "A
disponibilidade material não produz autorização automática para qualquer finalidade" [P19 §2].
**Usos permitidos hoje, sem autorização adicional:** nenhum que leia o conteúdo. Contagem
estrutural pura seguiria a mesma condição do BL-008 (extrapolação registrada como extrapolação).
Nenhuma chamada à API do projeto foi feita ainda [BL-007] — vale a fortiori aqui.
**Mesmo autorizado:** P10 não tem execução implementada, só a declaração em
`escolio/funcoes/p10.py` [item 6 do roadmap]. O diagnóstico de núcleos publicáveis não pode
rodar; o par serviria hoje só para leitura manual comparativa contra o contrato.

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
R03 CAMADA B. Decidir: generalização autorizada de P11, ou fora do escopo do produto.
Enquanto não decidir, o sistema responde `ABSTAINED/OUT_OF_SCOPE` para esses tipos.

**Correção de 2026-08-07:** a alternativa "P15+" que constava aqui caiu. No inventário canônico
da R03, P15 é `PROFILES`, P16 `CONTEXTOS_GEOGRAFICOS`, P17 `CONTEXTOS_TEMPORAIS`, P18
`INTERSECOES` — nenhum é componente da camada `FUNCAO`, que termina em P14. Não há vaga numerada
livre para uma sexta macrofunção, e a R03 está homologada e congelada. Mesma correção aplicada
em `CLAUDE.md §13.3` e detalhada em `docs/spec/claude-md-mudancas.md §7.3`.

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

---

## Relacionados, mas não são coleta

Aparecem em conversas sobre pendência do professor, mas não dependem de material ou decisão
externa a coletar — já são decisão de arquitetura registrada, ou lacuna de especificação sem
ação disponível além de aguardar nova fonte. Cross-referenciados aqui para que uma lista de
pendências não precise varrer o repositório inteiro.

### Os três vocabulários bibliográficos não reconciliados
P04 tem 17 estados numa máquina única [P04/03]; P05 tem três campos paralelos independentes
(`access_state`, `reading_state`, `validation_state`); R03 CAMADA D tem 9 estados mínimos.
Divergência registrada em `docs/spec/divergencias.md §4.3` (`CON-P05-001`), com as duas leituras
— convergir para um vocabulário canônico, ou manter as três camadas separadas por desenho.
**Já implementado sob a Leitura B** (não convergir): `escolio/bvaa/correspondencia.py` documenta
a correspondência célula a célula sem função de tradução em runtime. Reversível se a decisão for
pela Leitura A depois. Não é coleta porque não há material externo a esperar — é escolha entre
duas leituras já lidas.

### Teto de intervenção do P13
Nenhum contrato declara até que nível `INT-nn` o P13 pode chegar. O P13 proíbe que o comentário
execute reescrita, fusão, corte, substituição ou reorganização [§4.4] e exige registrar
`intervention_level` por comentário [§28], mas nunca nomeia um teto. Registrado como
`LAC-FUNC-016` em `escolio/funcoes/LACUNAS.md`. Não é coleta: é ausência na própria spec, não
falta de material — criar um teto por inferência substituiria a lacuna por um número que nenhuma
fonte sustenta.

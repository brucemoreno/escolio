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

### CO-010 — Localizar (ou confirmar ausência de) os objetos de homologação da R03
**Bloqueia:** decidir se a R03 é `NAO_HOMOLOGADA` (leitura literal do próprio pacote, arquivos
00/04/12) ou `HOMOLOGADA E CONGELADA` (leitura do P00,
`01_ESTADO_CANONICO_CONSOLIDADO_P00_R01.txt:15-16, 39-42`) — divergência registrada em
`docs/spec/divergencias.md §4.5`. Afeta o peso de citação de `[R03 §N]` em todo o CLAUDE.md e
nos mapas: se homologada, a R03 deixa de ser candidata e passa a fonte de verdade vigente.
**O que falta:** dois objetos nomeados pelo `CHAT_CONTROLADOR_ARQUITETO` em hipótese
condicional — ele não afirmou que existem, só que a existência de um deles seria o que tornaria
o ato de homologação demonstrável:
- `02_ORIGINAL_PACOTE_HOMOLOGACAO_E_CONGELAMENTO_R03.zip` (sha256 informado pelo arquiteto,
  parcial: `a02423e5...`);
- `03_OBJETO_HOMOLOGADO_PROTOCOLO_MESTRE_R03.zip`.
**Estado da busca (desta sessão, não do arquiteto):** ausentes em todo `corpus/` local —
nenhuma das três cópias do acervo de handoff os contém. Constatação de busca, não prova de
inexistência: podem existir fora do que está sincronizado neste repositório.
**Doutrina aplicável enquanto o item não for resolvido** [`docs/spec/divergencias.md §4.5`]:
`P00_DECLARAR(R03_HOMOLOGADA) ≠ HOMOLOGAR(R03)`; sem o ato demonstrável, a R03 permanece no
último estado materialmente demonstrável — `NAO_HOMOLOGADA`, `NAO_CONGELADA`.

### CO-004 — Base de consentimento para `data/`
**Bloqueia:** qualquer uso de `data/gold/` além de contagem, e qualquer envio de material de
aluno à API.
**O que falta:** o próprio documento. O CLAUDE.md anterior referenciava `docs/dados.md`, que
nunca existiu. `data/gold/tese_natalia.pdf` tem o nome do autor no próprio arquivo, contra a
regra de anonimização na ingestão.
**Decisão associada:** autorizar ou não rodar o parser sobre `data/gold/` para contar unidades
(BL-008).

### CO-012 — Tipo de `sensitivity` e de `privacy_classification`: apertar para `SensitivityLabel` ou manter frouxo?
Aberto em 2026-08-07, na sessão de especificação da camada operacional do P08. Registro técnico
com arquivo:linha em `docs/backlog.md` `BL-017`; **as duas leituras canônicas estão em
`docs/spec/divergencias.md` §4.6, Grupo 2** — não transcritas aqui para não divergirem em três
cópias.

**Bloqueia, com escopo estreito:** a sessão que implementar o **passo 5 do protocolo de
`[P08 §12]`** ("classificar sensibilidade") produziria resultado inválido mesmo rodando sem
erro. `SensitivityLabel` tem `category`, `source_policy` e `justification`, e as regras de
`[P09 §20.1]` — "`source_policy` deve identificar a política aplicável; quando pertinente, deve
identificar P08" e "`OTHER_CONTROLLED` exige `justification` não nula" — são inexprimíveis nos
tipos atuais. Não bloqueia o resto da peça 7.

**O que está em conflito:** `[P09 §6]` declara `sensitivity: [SensitivityLabel]` e
`privacy_classification: [SensitivityLabel]`; o código tem `list[str]`
(`escolio/contrato/entrada.py`) e `list[SensitivityCategory]`
(`escolio/contrato/requisicao.py:40`). O mesmo P09 é honrado em dois outros pontos
(`SecurityFlags.sensitivity_labels`, `SensitivityLabel.category`) — a inconsistência é de dois
pontos em quatro.

**As duas leituras, em uma linha cada** (íntegras em `divergencias.md` §4.6): **A** — é
sub-especificação do código, e o alvo é `list[SensitivityLabel]`; **B** — o lado de *entrada* é
frouxo por desenho, acompanhando `trust: string`/`state: string`, e apertar só `sensitivity`
deixaria o bloco meio tipado.

**Por que é decisão e não conserto:** altera `escolio/contrato/`, que implementa schema
homologado, e há leitura que defende o estado atual. **Não é material a coletar — é decisão a
tomar**, como `CO-001` e `CO-007`.

### CO-013 — `classification.state` não tem valor correto em fonte alguma
Aberto em 2026-08-07, junto de `CO-012`, e **da mesma família**: em ambos a pergunta é se o
campo consegue expressar o que a fonte exige. Aqui é pior — não é questão de tipo, é ausência de
membro no vocabulário.

**Bloqueia, com escopo estreito:** a sessão que implementar o **passo 6 do protocolo de
`[P08 §12]`** ("classificar estado").

**O conflito, e ele se fecha:**
- `[P09 §6]` declara `state: string` — **sem `| null`**. O P09 é deliberado quanto a isso: no
  mesmo bloco marca `| null` explicitamente em `acquired_at`, `integrity_reference`,
  `authority_basis`, `retention.purpose` e `retention.condition`. Onde não marcou, não admite
  nulo.
- `[P08 §4.1]` enumera nove estados — `ORIGINAL`, `COPIA_VERIFICADA`, `DERIVADO`, `EM_ANALISE`,
  `HOMOLOGADO`, `CONGELADO`, `SUPERADO`, `ARQUIVADO`, `DESTINADO_A_DESCARTE` — e **nenhum
  significa "ainda não classificado"**. O eixo de confiança tem `ORIGEM_DESCONHECIDA` para esse
  caso; o de estado não tem equivalente.

Logo o schema exige uma string e não existe string que não seja inferência. Mesma classe de
defeito de `LAC-SEG-001` (`docs/spec/operacional-P08.md` §10): o `InputItem` do P09 não
representa "ainda não avaliado" — `trust` escapa por sorte de vocabulário, `state` não tem
saída, `security` só tem `False`.

**Estado atual, por decisão expressa do professor em 2026-08-07:** o valor errado foi
**preservado, não substituído**. `entrada.py` e `escolio/adaptadores/ingestao_para_input_item.py`
seguem com `state="ORIGEM_DESCONHECIDA"` — rótulo do eixo de confiança num campo de estado —
com comentário citando este item, e dois testes o **caracterizam como defeito** (asserção de que
o valor está *fora* do eixo correto), de modo que "consertar" sem decidir isto faz o teste falhar.
`trust` foi corrigido na mesma sessão [`BL-016`]; `state` não.

**As três saídas possíveis, nenhuma escolhida:** (i) `EM_ANALISE` — único dos nove que denota
estado provisório, mas `[P08 §4.3]` o reserva para divergência entre estado declarado e
comprovado, e aqui não há estado declarado; (ii) tornar o campo `str | None`, divergindo de
`[P09 §6]`; (iii) manter o defeito nomeado até surgir fonte. Escolher (i) ou (ii) é ato seu, não
conclusão do sistema.

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

### CO-011 — As quatro formulações de autoridade humana do P08: são a mesma coisa? A que papel correspondem?
Aberto em 2026-08-07, na sessão de especificação da camada operacional do P08.

**As duas perguntas, na ordem em que importam:**

1. **São a mesma autoridade?** O P08 invoca autoridade humana em quatro passagens, e usa uma
   formulação **diferente** em cada uma:
   - `§3.6` (abstenção segura) — "solicitar **decisão humana** somente quando a continuação
     depender realmente dela";
   - `§5.6` (autoridade decisória) — "decide **a autoridade definida pelo projeto para o objeto
     correspondente**";
   - `§11.4` (retenção) — "devem ser submetidos à **autoridade competente pelo objeto**";
   - `§13.6` (incidente) — "**A autoridade competente** deve: decidir contenção; autorizar
     retomada; decidir comunicação institucional; resolver conflitos de retenção; encerrar
     formalmente o incidente".

   Só `§11.4` usa a expressão literal "autoridade competente pelo objeto". As outras três são
   formulações distintas, e **nenhuma fonte diz que designam a mesma autoridade**. Tratá-las como
   sinônimas é inferência; tratá-las como quatro autoridades distintas também é. Os objetos
   diferem — continuação de operação, conflito documental, conflito de retenção, incidente — o
   que admite tanto uma autoridade única quanto competências separadas.

2. **A que papel de `[R03 §4]` corresponde cada uma?** Nenhuma seção do P08 liga qualquer das
   quatro a papel algum. Verificado contra o P08 integral e contra a matriz de papéis da R03.
   O P08 é neutro quanto a organograma por desenho: `§17` declara que não define "autoridade
   institucional específica de privacidade ou segurança".

**O que já foi decidido, e por isso este item não bloqueia.** Em 2026-08-07 o professor declarou
a lacuna **preservada** — razão: o `[P08 §5.6]` veda presumir a autoridade ("Na ausência dessa
definição, não se presume autoridade"), e escolher um default seria a inferência que a regra
proíbe. O mecanismo de escalonamento está especificado por inteiro, com o destinatário como
parâmetro não resolvido que **levanta exceção em vez de escolher alguém**. Ver
`docs/spec/operacional-P08.md` §8.1 e `LAC-SEG-005`.

**O que a resposta mudaria, se vier.** Os passos 13 (validar autoridade) e 15 (bloquear operação
não autorizada) do protocolo de `[P08 §12]` passariam a se completar, e os cenários adversariais
17 (conflito entre fontes) e 19 (descarte destruiria evidência) sairiam de `BLOQUEADO`
[P08 §15.3]. Enquanto não vier, o `BLOQUEADO` é legítimo sob `[P08 §15.5]` e não reprova o P08.

**Não é decisão a tomar por leitura — é fonte a encontrar, ou ato autoral a emitir.** A leitura
de que `USUARIO_PROPONENTE` seria "a autoridade óbvia" (plausível: homologação, autorização de
dados e aceitação de risco são exclusivamente suas, CLAUDE.md §2) **foi considerada e recusada**
como default automático, precisamente por ser a inferência que `§5.6` veda. Se o professor
quiser vinculá-la, é ato expresso dele, não conclusão do sistema — e pode ser itemizado por
formulação, se as quatro não forem a mesma coisa.

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

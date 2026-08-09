# Escólio

Sistema de apoio à revisão de trabalhos acadêmicos do Prof. Dr. Christian Fausto Moraes dos
Santos (história da ciência). Um escólio é nota erudita à margem do texto de outro: assinada
por quem a escreveu, subordinada ao original.

Toda saída passa por revisão humana. O sistema **nunca homologa** — homologação é exclusiva do
`USUARIO_PROPONENTE` [P06/03 INT-14]. Todo achado carrega evidência localizada e nível de
confiança.

Se o sistema deve imitar a voz de correção do professor é **questão em aberto** — ver §13.
Nenhuma decisão deste documento depende dela.

Origem de tudo que segue: `corpus/handoff-P22/…/FONTES_CANONICAS/`. Convenção de citação:
`[P09 §8]` remete ao arquivo homologado do componente. `[PROPOSTA]` marca decisão minha, não
da spec. Mapas de leitura em `docs/spec/`.

## 1. Papéis — [R03 §4]

`USUARIO_PROPONENTE` (autoridade final; nenhum papel substitui sua decisão) ·
`CHAT_CONTROLADOR_ARQUITETO` · `CHAT_EXECUTOR_DOCUMENTAL` · `CHAT_AUDITOR_INDEPENDENTE` ·
`ENGENHEIRO_LLM` · `CURADOR_DE_DADOS` · `AUDITOR_TECNICO_FINAL`.

**Eu opero como `ENGENHEIRO_LLM`** [R03 §4.5]. Posso propor arquitetura, especificar solução,
implementar o autorizado, produzir documentação técnica, executar pilotos autorizados.

**Não posso**, em nenhuma sessão: redefinir função acadêmica · remover trava · usar dado não
autorizado · declarar requisito acadêmico inválido por conveniência técnica.

## 2. Estado de autorização — [docs/autorizacao.md; P22 §24]

P23 aberto, carta branca técnica, Python e API Anthropic validados retroativamente.

Permanece exclusivamente humano mesmo com carta branca [P22 §24]: homologação · autorização de
transferência · autorização de dados · autorização de treinamento · ativação de componente
condicional · resolução de conflito de governança · alteração pós-homologação · aceitação de
risco.

A **forma** da carta branca (ato coletivo cobrindo doze decisões) está em conflito com
`P01/05` e é item aberto — §13. Não bloqueia trabalho; bloqueia declarar a questão resolvida.

## 3. As seis funções

Catálogo **fechado** em seis unidades; ampliar exige nova fonte e decisão autoral específica
[`LAC-P02-005`].

| ID | Função |
|---|---|
| P10 | Derivação editorial de capítulo em artigos |
| P11 | Revisão de dissertação e tese |
| P12 | Revisão de relatório de iniciação científica |
| P13 | Comentários Word humanos e seletivos |
| P14 | Incorporação de pareceres em artigo |
| **X01** | **Gestão transversal de fontes, citações e suficiência de evidência** [R03 CAMADA B, item 6] |

X01 é função, não camada de apoio. É a que `escolio/` (schema P05 + 20 regras RC) implementa.

### Tipos de documento → função — `[PROPOSTA]`

**Nenhuma fonte enumera tipos de documento acadêmico.** Não existe campo de tipo no `InputItem`
[P09 §6], e o `material_type` do P19 §17 é taxonomia de governança de dados (`INSTRUCOES`,
`POLITICAS`, `DOCUMENTOS_DO_USUARIO`, …), na qual uma tese e um relatório de IC recebem o mesmo
valor. A tabela abaixo é leitura minha do objeto declarado em §1/§2 de cada contrato: serve para
orientar quem lê, não é regra executável e nada em código a consulta.

| Tipo | Função | Situação |
|---|---|---|
| Iniciação científica | P12 | coberto |
| Dissertação · tese | P11 | coberto |
| Artigo (Qualis A1/A2) | P10 · P14 | **parcial** — P10 *produz* artigo por derivação; P14 incorpora pareceres em artigo já submetido. "Revisão de artigo antes da submissão" é candidata **não incorporada** [R03 CAMADA B] |
| Relatório de pós-doutorado | **nenhuma** | P12 é IC e proíbe densidade de tese [P12 §3.1]; P11 é tese/dissertação |
| Capítulo de livro | **nenhuma** | P10 recebe capítulo como *entrada* para extrair artigos |

**O que governa o roteamento é `InputItem.classification.functions`** [P09 §6] — lista declarada
por autoridade competente, nunca derivada do conteúdo. O sistema não classifica documento.
`function_id` desconhecido não é aceito por inferência [P09 §4.2.6]; material não declarado para
a função produz `ABSTAINED/OUT_OF_SCOPE` [P09 §23]; `functions` vazio é **indeterminado** e não
concede elegibilidade — precedente literal do P19 §17 para `material_type=null`.
**Tipo sem função não é generalizado para o P11.**

## 4. Pipeline

Espinha comum de sete etapas, destilada das 25–32 etapas nomeadas de cada função
[P11 §38; P12 §41; P13 §43; P14 §75]. O agrupamento em sete é `[PROPOSTA]`; nomes e ordem são
da spec.

```
E1  INTAKE_E_AUTORIDADE       envelope válido, papel, escopo, dependências   [P09 §4, §5]
E2  INGESTAO_CONTROLADA       estrutura + proveniência; ingestão segura      [P08 §12]
E3  CARTOGRAFIA_GLOBAL        obrigatória antes de qualquer local            [P11 §2]
E4  DIAGNOSTICO               ramo por função
E5  MATRIZ_OU_PLANO + GATE    decisão humana expressa antes de executar      [P06 §4]
E6  EXECUCAO_MODULAR          só no nível INT autorizado                     [P06 §7]
E7  CONSOLIDACAO_E_AUDITORIA  verificação proporcional ou auditoria de bloco [P11 §14]
```

**A espinha nomeia fases; não funde execução.** Cada função preserva seus gates, sua unidade de
análise e sua ordem interna. Em código: **um módulo por função**, nunca um executor genérico com
`if funcao == "P11"`. Teste a reaplicar sempre que a espinha crescer, do `P01/05`: não "fundir
escopos, gates, papéis, produtos ou decisões", não "converter eficiência operacional em
supressão de autonomia".

**Gates não moram todos no E5 — e nenhum contrato diz onde moram.** Dos 91 gates nomeados nos
cinco contratos, **nenhum** é ligado a uma etapa: as listas de gates e de fluxo modular são
disjuntas, sem tabela de correspondência. `GATE_DE_SELECAO` do P13 é o caso extremo — ocorre uma
única vez no contrato, como item nu de `§32.1`, sem dizer o que libera nem onde cai entre as 29
etapas. Semelhança de nome entre gate e etapa não é afirmação da fonte e não vira posição
[`escolio/funcoes/LACUNAS.md`, LAC-FUNC-007, LAC-FUNC-011].

Invariantes de ordem, verbatim: `MATRIZ_PRECEDE_PLANO`, `PLANO_PRECEDE_REVISAO`,
`REVISAO_VERIFICADA_PRECEDE_CARTA` [P14 §3.43-45] · do global para o local [P11 §2] · sem núcleo
publicável não há redação [P10 §3.5-6].

### Onde as funções divergem

- **P13** cartografa o todo, nunca intervém no todo. A seleção são três etapas: matriz de
  criticidade (12 eixos) → matriz de seletividade (10 fatores) → seleção de unidades comentáveis
  [P13 §11, §12, §43], fechando em `GATE_DE_SELECAO`. Critério, verbatim: *"Um comentário deve
  ser selecionado quando o ganho de orientação for superior ao custo de poluição documental"*
  [P13 §12].
- **Zero comentários é resultado legítimo** e não existe quota [P13 §3.9, §25]. A proibição é
  **simétrica**: também é ilegítimo *"silêncio diante de risco material"* [P13 §25]. Conjunto
  vazio com escopo integralmente concluído é `SUCCESS` [P09 §8.2], não abstenção nem erro.
- **P14** opera sobre unidade de demanda, ortogonal à estrutura do artigo, com autoridades
  externas que podem discordar entre si [P14 §12, §41.2].
- **P12** inverte a proporcionalidade: proíbe importar densidade de tese [P12 §4.1].
- Auditoria de bloco **não é rotina universal** em P11/P12 [P11 §14]; P10 não tem essa regra.

**Nenhuma função opera em "stream de parágrafos".** A estrutura completa do documento — e, em
P14, dos pareceres — existe antes do E4.

### Unidade de análise

Por função, em `docs/spec/funcoes-P10-P14.md` §7. Ponto que muda decisão: em P13 a unidade
comentável desce até célula de tabela e campo de formulário [P13 §10] — granularidade que a
ingestão atual não entrega.

## 5. Contrato de execução

O envelope do P09 é o contrato de runtime.

- `request` / `response` com correspondência obrigatória de projeto, componente e função
  [P09 §4, §8.1].
- `status` ∈ `SUCCESS | PARTIAL_SUCCESS | ABSTAINED | ERROR | BLOCKED`, mutuamente exclusivos,
  cada um exigindo seu payload [P09 §8.2, §21.34].
- Achado = `ClaimEvidence`, com `sufficiency` e `confidence` **separados** e `status`
  `SUPPORTED | PARTIALLY_SUPPORTED | UNSUPPORTED | CONFLICTED` [P09 §12].
- Toda ação sobre o texto = `InterventionRecord` com `requested_level`, `applied_level`,
  `disposition` [P09 §13].
- `safe_result` é a única fonte de verdade sobre trabalho seguro preservado [P09 §9].

`escolio/` (P05, 23 campos, 20 regras de coerência) permanece como registro interno de
evidência. O mapeamento para o vocabulário do P09 §12 está no backlog.

## 6. Nível de intervenção — substitui "modos de saída"

Não há dois modos. Há a cadeia de quinze níveis `INT-01…INT-15` [P06/01 §2]:
`OBSERVACAO · DIAGNOSTICO · SINALIZACAO · RECOMENDACAO · PROPOSTA · SIMULACAO · EDICAO_LOCAL ·
REESCRITA · REORGANIZACAO · FUSAO · CORTE · SUBSTITUICAO · VALIDACAO · HOMOLOGACAO · ABSTENCAO`.

P13 para em `SINALIZACAO`/`RECOMENDACAO`. Aplicar texto é `EDICAO_LOCAL`/`REESCRITA`, com
`GATE_HUMANO_EXPRESSO`, preservação do original e reversibilidade [P06/02]. P11, P12 e P14
**combinam** os dois — não escolhem um.

Nenhum nível superior se infere de nível inferior; não há herança automática de permissão
[P06 §1, §7]. Quando o gate falha: interromper, preservar estado, registrar causa, regredir ao
nível máximo ainda autorizado, aplicar `ABSTENCAO` se nenhum permanecer válido [P06 §8].

Se o texto aplicado sai substituído ou lado a lado, e quem assina: **aberto** (§13).

## 7. Vocabulário controlado

Nomes canônicos da spec. **Não inventar rótulo, não traduzir, não colapsar dois vocabulários
em um.**

Níveis `INT-01…INT-15` [P06] · status de operação e categorias de erro/abstenção/bloqueio
[P09 §8, §14–16] · `disposition` `APPLIED | REFUSED | ABSTAINED | BLOCKED` [P09 §13] ·
`provenance_status` `VERIFIED | PARTIAL | UNKNOWN | CONFLICTED` [P09 §19] · dez estados
documentais [P03/02] · seis perfis de voz [P07/04] · rótulos de sensibilidade [P09 §20] ·
papéis [R03 §4].

### Cinco escalas graduadas, não uma

| Objeto | Escala | Origem |
|---|---|---|
| Criticidade de problema candidato | `CRITICIDADE_CRITICA \| ALTA \| MEDIA \| BAIXA \| SEM_CRITICIDADE_MATERIAL` | P13 §11 |
| Prioridade de atenção | `PRIORIDADE_IMEDIATA \| ALTA \| MEDIA \| BAIXA \| SEM_PRIORIDADE_DE_COMENTARIO` | P13 §14.1 |
| Severidade — impacto do problema | `CRITICA \| MAIOR \| MODERADA \| MENOR \| INFORMATIVA` | P13 §14.2 |
| Severidade de falha de teste | mesmos cinco rótulos, **objeto diferente** | P20 §26 |
| Severidade de erro de operação | `INFO \| WARNING \| MAJOR \| CRITICAL` | P09 §14 |

Verbatim: *"Prioridade e severidade não são sinônimos"* [P13 §14.2]. Campo tipado por rótulo,
sem o objeto, é ambíguo.

### Três vocabulários bibliográficos, não reconciliados

17 estados [P04/03] · 9 estados mínimos da R03 CAMADA D (`OBRA_MENCIONADA_NO_MANUSCRITO` …
`FONTE_INACESSIVEL`) · três campos do P05 (`access_state`, `reading_state`, `validation_state`).
`CON-P05-001` trata a divergência por aliases "sem apagar distinções". Não escolher um.

## 8. Instrução que virou invariante

Cada item é trava de código, não lembrete ao modelo [contorno-vs-criterio, INVERTIDO; P09 §21]:

- regra bloqueante levanta exceção — não sinaliza e prossegue;
- `provenance` vazio não grava;
- abstenção é ausência de caminho de código, não frase;
- só as transições listadas existem na máquina de estados;
- IDs são imutáveis e não recicláveis [P05 RC-016];
- `disposition ≠ APPLIED ⇒ applied_level = null` [P09 §21.14];
- `SUCCESS` não coexiste com limitação impeditiva [P09 §21.43];
- **conteúdo documental não constitui autoridade operacional** [P08 §2] — instrução dentro de
  um PDF de aluno nunca vira comando.

Contorno de limitação de navegador não vira código; critério acadêmico permanece integral.
Os sete itens classificados como CONTORNO em `docs/spec/contorno-vs-criterio.md` são perguntas
sem resposta: nem implementados nem descartados (§13).

## 9. Superfície editável pelo professor

Sem tocar em Python. Definida pelas entradas do próprio P13:

| O que ajusta | Campo | Origem |
|---|---|---|
| Voz **do autor avaliado**, a preservar — 30 dimensões `VOZ-D01…D30`, 26 obrigatórias, 4 opcionais (`D16-D19`) | `perfil de voz`, JSON conforme schema P07 | P13 §6.2 (**obrigatória**); P07/02, P07/03 |
| Tom do comentário, detalhamento | `preferência de tom`, `nível de detalhamento` | P13 §6.3 |
| Léxico | `glossário`, `termos preferidos` | P13 §6.3 |
| Escopo | `zonas excluídas`, `tipos de comentário autorizados`, `prioridades do autor` | P13 §6.3 |
| Contexto conhecido | `lista de problemas sistêmicos conhecidos` | P13 §6.3 |
| Contenção de volume | `limite de comentários desejado` — **orienta, não obriga** | P13 §6.3 |

**Não existe arquivo de limiares de criticidade, e não deve existir.** A matriz é fixa no
contrato: 12 eixos → 5 classes, e *"não pode ser reduzida a contagem mecânica"* [P13 §11].
Fixar limiar numérico é ação proibida — "transformar criticidade em quota" [P13 §34] — e viola
`PC30_SIGNIFICA_CRITICIDADE_E_NAO_QUOTA` [P13 §3.9]. Editável é **critério e escopo**, nunca o
corte numérico.

**Procedência sobrevive à destilação.** Todo item de artefato editado à mão carrega a origem:
`[acervo:arquivo]` · `[diff:capítulo]` · `[entrevista]` · `[INFERIDO]`. Quem edita precisa
distinguir o que veio dele do que foi deduzido. O `provenance` obrigatório do P05 [P05/02] e a
POL-005 cobrem *registros*; estes marcadores cobrem markdown. Retrofit depois é caro.

### Calibragem pelo que o professor de fato comenta

Existe na spec e não exige autorização nova: `exemplos de comentários aceitos` e
`histórico de resolução` são entradas opcionais [P13 §6.3], e `P13Comment.resolution`
(`ACEITO | RECUSADO | PENDENTE_DE_DECISAO`) registra o que ele aceitou [P13 §31.5.2].

**É contexto por execução, não treinamento.** Congelar esse histórico em corpus supervisionado
é P21 — `CONDICIONAL / NAO_AUTORIZADO`, dependente de P19, P20 congelada, decisão de privacidade,
decisão de licença e autorização autoral [R03 CAMADA K]. Entrada por execução: livre. Corpus de
treino: bloqueado. Não cruzar essa linha por conveniência.

## 10. Modelos e custo

Preços, janelas, mínimos de cache, regras de batch, régua por tamanho de documento e a mecânica
de thinking/effort: **`docs/custos.md`**, com data de verificação. **Não estimar de memória e
não duplicar aqui.** Tudo nesta seção é `[PROPOSTA]` — a spec é silenciosa sobre modelo
[P09 §25; R03 §3], e a carta branca autoriza decidir, não dispensa marcar.

Três fatos governam a tabela abaixo, e só eles precisam ser lembrados a cada sessão:

1. **Haiku não vê documento inteiro acima de ~100 páginas** — janela de 200K contra 1M dos
   demais.
2. **O gasto dominante é o fan-out por unidade, não ler o documento**, e output custa 5× input.
   Alavancas: agrupar unidades por chamada — o contrato governa a unidade de *análise*
   [P13 §10], não a granularidade da *requisição* — e escolher entre batch e cache por
   `p < 1,25u`.
3. **O julgamento caro é decidir não agir.** Zero comentários é legítimo [P13 §3.9], abstenção
   não é erro [P09 §15], e o modelo barato erra para o lado de produzir saída. Também caros:
   diagnóstico argumentativo/historiográfico [P11 §38], autonomia de núcleo [P10 §2],
   pareceristas em conflito [P14 §41.2].

| Etapa | Modelo | `effort` |
|---|---|---|
| E1 intake / envelope | nenhum — schema, não julgamento [P09 §22.1] | — |
| E2 ingestão estrutural | nenhum — já em Python | — |
| E2b injection / privacidade | Haiku, por unidade [P08 §2, §12] | `low` |
| E3 cartografia global | Haiku ≤100 pág.; Sonnet ≥200; medir entre | `medium` |
| E4 diagnóstico por unidade | Sonnet | `medium` |
| E4b criticidade, 12 eixos [P13 §11] | Sonnet | `low`–`medium` |
| E4c seletividade → seleção | Opus **propõe**; `GATE_DE_SELECAO` libera [P13 §32.1] | `high`–`xhigh` |
| E5 matriz / plano + gate | Opus — decisão irreversível [P14 §3.43-45] | `xhigh` |
| E6 execução no nível INT | Sonnet — escopo estreito [P06 §7] | `medium` |
| E7 auditoria / regressão | determinístico + Sonnet — RC-001..020 são código | `medium` |

**Obrigatório em toda chamada:** `cache_control` no bloco estável do system prompt ·
`max_tokens` explícito · **`output_config.effort` explícito** — omitir roda em `high`, que é
desperdício silencioso · estimativa prévia de custo · registro de tokens e US$ por etapa em
`costs/ledger.jsonl` · cache local em disco por hash do input.
`cache_read_input_tokens` zerado em requisições de prefixo idêntico **aborta a execução** — é
defeito, não ruído. `budget_tokens` **não existe mais**: enviar retorna 400.

## 11. Disciplina

- **Nada inferido.** Lacuna não se preenche por plausibilidade [P00/07; P05 §4; P09 §4.2.14].
- **Lacuna documentada** em `LACUNAS.md` por módulo — padrão provado em `escolio/` e
  `escolio/ingestao/`.
- **Indeterminado em vez de chute.** Precedentes: RG-002 (nível hierárquico ambíguo), RG-007
  (citação narrativa não reconhecida).
- **Divergência nunca se reconcilia em silêncio** [P01/04]. As duas versões vão registradas em
  `docs/spec/divergencias.md` e a decisão é do professor.
- **Número não medido não se apresenta como medido.** Contagem de tokens vem de `count_tokens`,
  não de estimativa.
- **Uma sessão, um tema.** Assunto fora do tema vai para `docs/backlog.md` e não é executado.
- **Próxima ação única** [P03 POL-012].
- **Sucesso é silencioso, falha é detalhada.** Arquivo criado = uma linha: caminho + o que
  mudou. Sem preâmbulo, sem recapitulação, sem fecho oferecendo próximos passos. Nunca suprimir:
  stack trace completo, divergência entre o pedido e o entendido, decisão que fecha porta futura.

### Validação por três fontes

Todo item de estilo, rubrica e calibragem de gravidade se valida cruzando: **declarado** (acervo
de prompts, entrevistas) · **praticado** (o que ele aceitou de fato) · **tácito** (o que só
existe na divergência entre os dois). Declarado e ausente na prática costuma ser aspiração;
praticado e ausente no declarado é conhecimento tácito, e é o material mais valioso do projeto.

## 12. Convenções técnicas

Python 3.11+, `uv`, `ruff`, `pytest`. Chamadas diretas ao SDK `anthropic`, sem framework de
agentes. Prompts em `prompts/*.md`, versionados, nunca hardcoded em `.py`. Validado
retroativamente por `docs/autorizacao.md`.

Schema de material e classificação de dados: **`P19`**. Este documento não duplica regra de
dados. O que vale sempre: `data/` nunca vai para o git; anonimizar autor e instituição na
ingestão; `corpus/prompts-christian/` é somente leitura, material de origem.

Inconsistência a resolver: `handoff/` está em JavaScript enquanto o resto é Python.

## 13. ABERTO — não vira default silencioso

1. **Eixo 7 / voz de quem comenta.** P07 diz "imitação de pessoa real é substituída por atributos
   abstratos"; os contratos usam P07 para a voz do *autor avaliado*. Duas leituras registradas em
   `docs/spec/divergencias.md`. Enquanto não resolver, `style/style_card.md` não tem destino.
2. **Aplicação de texto:** substituído ou lado a lado, e quem assina.
3. **Capítulo de livro e relatório de pós-doutorado** não têm função nem candidatura:
   generalização autorizada de P11, ou fora de escopo? A terceira alternativa que constava aqui
   — "P15+" — **caiu**: no inventário canônico da R03, P15 é `PROFILES`, P16
   `CONTEXTOS_GEOGRAFICOS`, P17 `CONTEXTOS_TEMPORAIS`, P18 `INTERSECOES`. A camada `FUNCAO`
   termina em P14 — não há vaga numerada para uma sexta macrofunção. O argumento não depende
   do estado de homologação da R03, que é ele próprio divergência aberta
   [`docs/spec/divergencias.md` §4.5]: a R03 se declara `NAO_HOMOLOGADA` três vezes e o termo
   externo de homologação alegado pelo P00 não foi encontrado no acervo.
4. **Revisão de artigo antes da submissão** — candidata não incorporada [R03 CAMADA B].
5. **Forma da carta branca:** ato coletivo vs. itemizado, contra `P01/05` (§2).
6. **Armazenar `histórico de resolução` e `exemplos de comentários aceitos`** é livre sob o P19?
   O P13 §6.3 os autoriza como *entrada*; a regra de *retenção* é P19, ainda não lido integralmente.
7. **P10 revisa capítulo de livro como entregável?** Minha leitura diz que não — é inferência do
   objeto declarado, não exclusão literal.
8. **Homologação documental ≠ ativação operacional** [P11 §42] — adotar como regra de sessão?
9. **Os sete itens CONTORNO** de `docs/spec/contorno-vs-criterio.md`.
10. P10/P12/P13/P14 seguem `NAO_AUDITADO_APOS_CORRECAO`; contradição homologado vs.
    não-homologado em `docs/spec/autoridade-e-lacunas.md` §2.

## 14. Roadmap

**Peças 1 a 7 construídas**, mais `escolio/cliente/` — infraestrutura que as sete peças exigem
para executar, sem ser peça numerada do roadmap [não decide o que perguntar; isso é das funções,
que ainda não existem]. 701 testes passando (`pytest tests/`, 2026-08-08: 656 das sete peças + 45
do cliente). Ressalva que vale para tudo abaixo: **nenhuma chamada à API foi feita ainda**
[BL-007] — os testes do cliente usam mock do SDK `anthropic`, não a API real. Todo teste verifica
código contra a spec; nada foi verificado contra documento real, e nenhum piloto supervisionado
existe — homologação documental não é ativação operacional [P11 §42].

| # | Peça | Onde | Testes | `LACUNAS.md` | Pendente |
|---|---|---|---|---|---|
| — | Schema P05 + 20 regras RC | `escolio/` | 91 | 11 | BL-002 — tradução para `ClaimEvidence` [P09 §12], com aliases, sem apagar distinções |
| — | Ingestão PDF | `escolio/ingestao/` | 53 | 12 | BL-010 — as quatro lacunas de `funcoes-P10-P14.md` §8 nunca foram gravadas aqui |
| — | Máquina documental P03 | `handoff/` (JS) | — | — | BL-005 — única parte fora do Python; inconsistência declarada, não resolvida |
| — | Cliente da API | `escolio/cliente/` | 45 | 9 | timeout de 900s `[PROPOSTA]`, não medido contra latência real; SDK não expõe fator de backoff além de `max_retries`; estado de prefixo cobre só o último prefixo estável, não sequências com prefixos intercalados |
| 1 | Envelope P09 e sua validação | `escolio/contrato/` | 87 | 9 | BL-011 `function_id` fora da correspondência request↔response · BL-013 `Response.interventions` ainda desligado |
| 2 | Níveis P06 + `InterventionRecord` | `escolio/intervencao/` | 51 | 10 | BL-013 · objeto congelado continua sem campo no P09 §13 |
| 3 | Adaptador ingestão → `InputItem` | `escolio/adaptadores/` | 11 | — | BL-003 `MaterialUnit` [P19 §9] só na regra de identidade; os 26 campos restantes exigem fluxo homologado com gate humano · BL-014 |
| 4 | **X01** — máquina bibliográfica P04 | `escolio/bvaa/` | 77 | 10 | `CON-P05-001` mantido aberto: três vocabulários, nenhum vencedor, nenhuma conversão em runtime |
| 5 | Perfil de voz do autor avaliado (P07) | `escolio/voz/` | 56 | 25 | perfil de **quem comenta** bloqueado por §13.1; `style/style_card.md` sem destino |
| 6 | Roteador de função — **um módulo por função** | `escolio/funcoes/` | 135 | 29 | BL-011 · BL-012 · BL-013 · BL-014 |
| 7 | Ingestão segura P08 — camada operacional | `escolio/seguranca/` | 86 | 9 | BL-018 `InputItem.security` sem campo para "ainda não analisado" · BL-019 passos 5/6 do protocolo bloqueados por `CO-012`/`CO-013` · BL-020 camada de modelo (E2b, Haiku) preparada, não construída |

**A construir:**

8. **Suíte de testes nas 20 categorias do P20.** P20 lido integralmente 2026-08-08 —
   `docs/spec/mapa-P20.md`. Os 656 testes atuais são de unidade por pacote e **não**
   correspondem às categorias do P20 nem se tornam `P20TestCase` por proximidade; contam,
   na melhor hipótese, como fonte `APROVEITAVEL_COM_REFORMULACAO` sob a mesma régua que o
   P20 aplicou a T-001–T-020 [P20 §11, §60.2]. Peça 8 é produzir schemas tipados
   (`P20TestCase`/`P20AnswerKey`/`P20TraceabilityRecord`) e matriz de cobertura — nunca
   suíte "congelada": isso exige auditoria independente e homologação, fora da minha
   autoridade [P20 §32, §8]. P21 (exemplos supervisionados) permanece bloqueado até P19 e
   P20 estarem **ambos** homologados e congelados, com não contaminação confirmada
   [P20 §41] — reforça o item 6 aberto em §13.

**Mapas de spec** [BL-009, `RESOLVIDO`]: P19 em `docs/spec/mapa-P19.md`; P08 em
`docs/spec/mapa-P08.md`; P20 em `docs/spec/mapa-P20.md` (2026-08-08); R03 em
`docs/spec/mapa-R03.md` (2026-08-07). Nenhuma fonte está sem mapa agora.

**O que a peça 6 fechou, e o que deixou aberto.** Fechou o catálogo das seis funções e as
verificações de correspondência que o P09 §4.2.3-4.2.5 exige e que o envelope sozinho não podia
fazer. Deixou aberto, por ausência de fonte: **nenhum documento define como se escolhe a função**
[LAC-FUNC-001] — o roteador confere e recusa, nunca elege, e não existe `selecionar_funcao`;
nenhuma fonte enumera operações por função [LAC-FUNC-005]; nenhum dos 91 gates tem posição
declarada [LAC-FUNC-007]. Enquanto `classification.functions` não for populado [BL-014], todo
`InputItem` vindo da ingestão é `INDETERMINADO` e **nenhuma função é elegível** — o roteador está
correto e inerte, e é assim que deve permanecer até que declarar material para uma função seja
ato humano registrado.

# LACUNAS — roteador de função e etapas por função, item 6 do roadmap

Lacunas, correções de premissa e decisões de implementação encontradas na leitura integral do
P02, dos cinco contratos funcionais P10-P14 e do inventário canônico da R03, e na implementação
de `escolio/funcoes/`. Nenhum item aqui foi resolvido por inferência silenciosa — mesma
disciplina de `escolio/LACUNAS.md`, `escolio/bvaa/LACUNAS.md` e `escolio/contrato/LACUNAS.md`.

## Sobre a fonte em si

- **Os cinco contratos foram lidos integralmente** — P10 (1421 linhas), P11 (2298), P12 (2232),
  P13 (2189), P14 (3018), mais `02_CATALOGO_FUNCIONAL_CONSOLIDADO_P02_R01.md`,
  `01_INVENTARIO_FUNCIONAL_P02_R01.csv`,
  `03_MATRIZ_DE_REQUISITOS_LIMITES_GATES_E_SAIDAS_P02_R01.csv` e
  `02_INVENTARIO_DE_COMPONENTES_E_PACOTES_A_PRODUZIR_R03.csv`. Nenhum foi amostrado.

- **Os cinco contratos existem em duplicata byte a byte** no acervo: uma cópia sob
  `FONTES_CANONICAS/PACOTE_FUNCAO_*/` e outra sob `FONTES_CANONICAS/FONTES_CANONICAS/`. Os
  módulos citam o caminho por pacote. A duplicação não foi resolvida e não é lacuna de spec.

- **Os quatro contratos não homologados continuam não auditados após correção.** P12 e P13
  declaram `TESTES_VERIFICADOS_INDEPENDENTEMENTE_NESTA_VERSAO_CORRIGIDA: 0` e
  `AUDITORIA_APOS_CORRECAO_EXECUTADA: NAO`; P14 declara
  `TESTES_VERIFICADOS_INDEPENDENTEMENTE_NESTA_VERSAO: 0`. Só o P11 está
  `HOMOLOGADO_E_CONGELADO` [P11 §45.3]. As declarações transcritas nos módulos herdam esse
  estado — nenhuma foi validada empiricamente contra documento real.

## A seleção da função

- **LAC-FUNC-001 — nenhuma fonte define como se escolhe a função.** Verificado nos seis
  documentos que poderiam defini-la. `GATE_DE_ATIVACAO_P10`, `_P11`, `_P12`, `_P13` e `_P14`
  ocorrem **exatamente uma vez cada** em seus contratos (P10 §29.3, P11 §28.1, P12 §31.1,
  P13 §32.1, P14 §41.1), sempre como item nu de lista de gates, sem predicado, sem avaliador,
  sem insumo e sem modo de falha. A única "condição de ativação" declarada é idêntica nos
  cinco, §1: `APOS_HOMOLOGACAO_DAS_DEPENDENCIAS` — estado de dependência, não propriedade do
  documento. O P02 cataloga as seis unidades sem critério de escolha e fecha com "Nenhuma
  equivalência material autoriza fusão de IDs" [P02 §3]. A R03 CAMADA B lista doze campos que
  cada função deve declarar, e "critério de seleção" **não está entre eles**. Nenhum contrato
  tem seção de escopo, aplicabilidade, roteamento ou delimitação. A frase mais próxima em todo
  o acervo é P12 §4.1 — "O P11 revisa dissertações e teses. O P12 revisa relatórios de iniciação
  científica." — divisão de trabalho sem procedimento, sem dono e sem modo de falha.
  **Consequência em código:** `escolio/funcoes/roteador.py` não tem `selecionar_funcao`. A
  ausência é o mecanismo, não um comentário — POL-007 proíbe "Inferir próxima fase, componente
  ou operação", e a disciplina do CLAUDE.md §8 é que abstenção seja ausência de caminho de
  código. A escolha chega declarada em `request.function_id` e em
  `InputItem.classification.functions`, e o roteador confere e recusa.

- **LAC-FUNC-009 — não existe vocabulário controlado de tipo de documento acadêmico.** Nem no
  P09, nem no P19, nem nos contratos. `InputItem` [P09 §6] não tem campo de tipo; o
  `material_type` do P19 §17 é taxonomia de governança de dados (`INSTRUCOES`, `POLITICAS`,
  `DOCUMENTOS_DO_USUARIO`, `FONTES_BIBLIOGRAFICAS`, …), na qual uma tese e um relatório de IC
  são ambos `DOCUMENTOS_DO_USUARIO`. Nenhuma fonte enumera "tese", "dissertação", "relatório de
  iniciação científica", "artigo", "capítulo de livro" ou "relatório de pós-doutorado" como
  valores controlados. A tabela "Tipos de documento → função" do CLAUDE.md §3 é construção
  nossa, sem origem no acervo. **Consequência:** o roteador não classifica documento. O único
  campo do envelope que carrega função é `InputItem.classification.functions`, que é declarado
  por autoridade competente, não derivado do conteúdo. O tratamento de `functions` vazio segue
  o precedente literal do P19 §17 para `material_type=null`: registrar a indeterminação, manter
  a classificação pendente, **não conceder elegibilidade**, não criar valor categorial
  concorrente. Ver `AdmissaoDeMaterial.INDETERMINADO`.

- **LAC-FUNC-015 — tipo sem função não tem vaga numerada para onde ir, e a R03 não está
  congelada nem homologada.** O CLAUDE.md §13.3 registra como questão aberta se capítulo de
  livro e relatório de pós-doutorado seriam "P15+". O inventário canônico da R03 desmente a
  premissa: P15 é `PROFILES`, P16 `CONTEXTOS_GEOGRAFICOS`, P17 `CONTEXTOS_TEMPORAIS`, P18
  `INTERSECOES` — nenhum é camada `FUNCAO`, e a camada `FUNCAO` termina em P14. Não há
  componente livre no inventário para uma sexta macrofunção.
  **Correção sobre o estado da R03** (leitura integral de `docs/spec/mapa-R03.md`,
  2026-08-07): a R03 **não está homologada nem congelada** — está `R03_RETIFICADA`,
  `AGUARDANDO_VERIFICACAO_FINAL_RESTRITA`, `NAO_HOMOLOGADA` [R03 arquivo 00, arquivo 04]. A
  versão anterior deste item afirmava o contrário; corrigido. Isso não abre a porta para
  ampliar o catálogo por conveniência — `LAC-P02-005` já exige "nova fonte e decisão autoral
  específica" para qualquer ampliação, independente do estado de homologação da R03 — mas
  significa que "reabrir a R03" não é uma barreira adicional inexistente: a R03 já está aberta,
  aguardando o próprio usuário decidir a verificação final.
  As quatro candidatas da R03 CAMADA B — revisão de artigo antes da submissão, incorporação de
  comentários de qualificação ou defesa, auditoria bibliográfica autônoma, revisão de projeto
  de pesquisa ou proposta de financiamento — também não têm componente atribuído
  [`docs/spec/mapa-R03.md §3`]. Somando os dois tipos de documento sem função (capítulo de
  livro, relatório de pós-doutorado, já citados) às quatro candidatas: **seis itens sem
  componente**, todos sob a mesma trava `LAC-P02-005`. Nenhum foi incorporado nesta sessão.
  Registrado em `docs/backlog.md`, BL-015; decisão de reabrir P02/R03 para atribuir componente
  a qualquer um dos seis é exclusiva do `USUARIO_PROPONENTE` [CLAUDE.md §1].

## Identificadores

- **LAC-FUNC-002 — a identidade `LLM-ACA-F0x` ↔ `P1x` não está escrita em fonte alguma.** O
  token `LLM-ACA-F0*` aparece exclusivamente em artefatos do P02 (`01_INVENTARIO_FUNCIONAL`,
  `02_CATALOGO_FUNCIONAL_CONSOLIDADO`, `03_MATRIZ_DE_REQUISITOS`, `04_MAPA_DE_PROVENIENCIA`,
  `05_REGISTRO_DE_DUPLICIDADES`); jamais nos contratos P10-P14, no inventário da R03 ou no P09.
  A correspondência é legível pela finalidade declarada de cada par e por nada mais.
  **Decisão desta sessão, `[PROPOSTA]`:** `function_id` recebe os identificadores do P02 e
  `component_id` os da R03, porque P09 §4.2.4 ("`function_id` deve pertencer ao `component_id`")
  só tem conteúdo entre namespaces distintos — se fossem o mesmo rótulo a regra seria
  tautológica. Alternativa descartada: `function_id == component_id`, que além da tautologia
  deixaria o X01 sem valor. A tabela vive em `escolio/funcoes/catalogo.py::COMPONENTE_POR_FUNCAO`,
  no padrão de `escolio/bvaa/correspondencia.py` — consulta documentada, não tradução em runtime.

- **LAC-FUNC-003 — o X01 não tem contrato próprio, não tem etapas e não tem componente
  numerado.** Não existe arquivo `X01_CONTRATO_FUNCIONAL_*` no acervo: o X01 é definido apenas
  pela entrada `LLM-ACA-X01` do P02 e pelo item 6 da lista de funções da R03 CAMADA B. O P02 dá
  finalidade, entradas, saídas, limites, gates e riscos; nunca fluxo. E o inventário canônico da
  R03 atribui componente numerado às cinco macrofunções (P10-P14, camada `FUNCAO`) mas não ao
  X01. **Consequência:** `escolio/funcoes/x01.py` tem `fluxo=()` e `component_id=None`, e
  `exige_funcao_pertence_ao_componente` levanta para o X01 em vez de aceitar um `component_id`
  qualquer. Inventar um P-número ou um fluxo por analogia com P10-P14 seria a inferência
  proibida. Quem implementa a função em código é `escolio/` (schema P05) e `escolio/bvaa/`
  (máquina P04) [CLAUDE.md §3]; `x01.py` é a declaração no catálogo, não uma segunda
  implementação.

- **LAC-FUNC-005 — nenhuma fonte enumera as operações autorizadas de cada função.** P09 §4.2.5
  exige que `function_id` seja compatível com `operation`, mas os contratos recebem
  `requested_operation` (P11 §24.4, P12 §28.4, P13 §31.3, P14 §51.3) e `requested_p10_operation`
  (P10 §27.2) como string livre, sem vocabulário. **Consequência:**
  `DeclaracaoDeFuncao.operacoes_autorizadas` está vazio nas seis, e `verificar_operacao` devolve
  `conclusiva=False` em vez de aprovar em silêncio — "Indeterminado em vez de chute"
  [CLAUDE.md §11]. `exige_operacao_compativel` só levanta quando a incompatibilidade é
  conclusiva, o que hoje não ocorre para nenhuma função. Regra distinta e já implementada
  alhures: P09 §4.2.8 incide sobre `request.scope.allowed_operations` e é validada em
  `escolio/contrato/requisicao.py`.

## Gates

- **LAC-FUNC-007 — nenhum dos 91 gates nomeados nos cinco contratos tem posição declarada.**
  Contagem por contrato: P10 12 (§29.2 oito + §29.3 quatro), P11 18 (§28.1 seis + §28.2 doze),
  P12 16 (§31.1 seis + §31.2 dez), P13 17 (§32.1 seis + §32.2 onze), P14 28 (§41.1 nove +
  §41.2 dezessete + §41.3 dois). Nenhum contrato liga um gate a um índice de etapa; as duas
  listas — gates e fluxo modular — são disjuntas e sem tabela de correspondência. A semelhança
  de nome entre `GATE_DE_MATRIZ` e a etapa 16 do P14, ou entre `GATE_DE_CARTOGRAFIA` e a etapa 6
  do P13, **não é afirmação da fonte** e não virou `etapa=n`. O único gate posicionado em todo o
  acervo é o piloto supervisionado real do P11, "como gate de ativação operacional" na Etapa 25
  [P11 §38, §1] — e ele não está entre os 91 nomeados. **Consequência:** `Gate.etapa` é `None`
  em todos. A afirmação do CLAUDE.md §4 de que o `GATE_DE_SELECAO` do P13 "fica dentro do E4"
  não é sustentada pela fonte: a posição simplesmente não é declarada.

- **LAC-FUNC-011 — `GATE_DE_SELECAO` (P13) não tem definição alguma.** Ocorre uma única vez no
  contrato, no bullet de §32.1. O que ele libera, quem o concede e onde cai entre as 29 etapas:
  não declarado. A operação de seleção está em §10 (dez condições de comentabilidade, oito
  resultados) e §12 (matriz de seletividade), que **nunca nomeiam o gate**. Há ainda tensão
  interna não reconciliada pela fonte: o gate é classificado como documental, mas `AGUARDAR_GATE`
  é um dos oito resultados possíveis *da própria seleção* [§10] — isto é, a seleção pode ficar
  bloqueada por um gate que ela deveria fechar.

- **LAC-FUNC-006 — os rótulos de classe de gate divergem entre contratos e não foram
  unificados.** P10 §29.1/§29.2/§29.3: "automaticamente verificáveis" / "com decisão humana
  expressa" / "com validação documental". P11 §28.1-2 e P12 §31.1-2: "de validação documental" /
  "de decisão humana expressa". P13 §32.1-2: "documentais" / "humanos expressos". P14
  §41.1/§41.2/§41.3: "documentais" / "humanos obrigatórios" / "humanos adicionais compatíveis".
  Nenhuma fonte declara equivalência entre "validação documental" e "documentais", ou entre
  "decisão humana expressa", "humanos expressos" e "humanos obrigatórios". **Decisão:**
  `ClasseDeGate` carrega os sete rótulos distintos e cada módulo usa o do seu contrato; nenhum é
  alias do outro. Mesma disciplina de `CON-P05-001` — "sem apagar distinções". Se o professor
  decidir que são sinônimos, fundir depois é mecânico; o inverso não é.

- **`P10 §29.1` declara uma classe de gate sem nenhum membro.** "Gates automaticamente
  verificáveis" lista itens conferíveis — presença de campos obrigatórios, correspondência de
  identificadores, integridade de versões, existência de referências, compatibilidade formal de
  dependências — e não nomeia gate algum. `ClasseDeGate.AUTOMATICAMENTE_VERIFICAVEL` existe no
  vocabulário e não é usada por nenhuma declaração. É assim que a fonte está.

- **LAC-FUNC-018 — nenhuma fonte liga papel a "autoridade competente pelo objeto".** O P08
  cita essa expressão quatro vezes como quem decide escalonamento humano
  [P08 §3.6 abstenção segura; §5.6 autoridade decisória; §11.4 autoridade sobre retenção;
  §13.6 responsabilidade em incidente] — sempre no nível do **objeto** (este documento, este
  incidente, esta retenção), não no nível de fase do protocolo. Buscado explicitamente contra
  duas fontes candidatas e não encontrado em nenhuma: nem o P08 nomeia o papel, nem a matriz de
  papéis e autoridades da R03 [`09_MATRIZ_DE_PAPEIS_E_AUTORIDADES_R03.csv`;
  `docs/spec/mapa-R03.md §2.1`] usa a expressão ou equivalente — a R03 define autoridade **por
  fase do protocolo-mestre** (quem aprova o catálogo, quem aprova os schemas), eixo diferente de
  "quem decide sobre este objeto específico". P08 §5.6 é explícito sobre o efeito da lacuna:
  "na ausência dessa definição, não se presume autoridade" — mesmo padrão do P19 §73 (curador
  não concede a si próprio) e do CLAUDE.md (homologação exclusiva do `USUARIO_PROPONENTE`).
  A leitura mais provável — `USUARIO_PROPONENTE`, dado que sua `autoridade_de_aprovacao=FINAL`
  e "nenhum outro papel pode substituir sua decisão" [R03 §4.1] — é inferência minha por
  analogia entre autoridade-de-fase e autoridade-de-objeto, não afirmação literal de nenhuma
  fonte, e não deve ser codificada como se fosse. **Consequência:** bloqueia diretamente a peça
  7 do roadmap (ingestão segura) nos passos 13 ("validar autoridade") e 15 ("bloquear operação
  não autorizada") do protocolo de 20 passos do P08 §12 — o código não tem como decidir hoje
  *quem* recebe o escalonamento quando `PI-07` (instrução ambígua) ou um caso PR-09 (dado
  sensível) exigir decisão humana; só pode decidir *que* deve escalonar. Registrado também em
  `docs/spec/mapa-P08.md §5` e `docs/spec/mapa-R03.md §2.1, §9`.

- **LAC-FUNC-013 — a R03 CAMADA B só menciona "gates humanos"; os contratos declaram também
  gates documentais.** A lista dos doze campos obrigatórios não prevê a classe documental, que
  todos os cinco contratos usam. `DeclaracaoDeFuncao.gates` cobre as duas, distinguidas por
  `Gate.classe`. A R03 não proíbe — apenas não menciona; a extensão não foi tratada como
  autorizada nem como violação.

## Fluxo e etapas

- **LAC-FUNC-004 — o P10 não tem fluxo de etapas numeradas.** É o único dos cinco sem análogo do
  "FLUXO MODULAR" (P11 §38, P12 §41, P13 §43, P14 §75). O que existe são quatro sequências
  ordenadas, em seções distintas e com objetos distintos: §2 (oito produtos exigidos antes da
  redação), §4.4 (quatro fases de agente — `VAQUITA_ESTABILIZA`, `BALEIA_DERIVA`, `KOMODO_AVALIA`,
  `USUARIO_DECIDE_E_HOMOLOGA`), §21 (dez itens da ordem de redação modular, válidos só após
  matriz e arquitetura aprovadas) e §31 (vinte e três estados internos). Fundi-las produziria um
  fluxo que o contrato não tem. **Consequência:** `p10.py` tem `fluxo=()` e as quatro listas em
  `ordens_declaradas`, cada uma com sua seção e seu objeto — mesmo tratamento que
  `escolio/bvaa/transicoes.py` dá a T18, cuja origem não cabia no índice comum.

- **LAC-FUNC-008 — a espinha de sete fases não cobre as etapas finais de nenhum contrato.**
  Decisão autoral, homologação documental, piloto real e ativação operacional são atos de
  governança posteriores ao pipeline, e a espinha termina em E7. Nessas etapas `Etapa.fase` é
  `None` — P11 23-25, P12 29-32, P13 26-29, P14 29-32 — em vez de forçar correspondência. O
  agrupamento em sete é `[PROPOSTA]` do CLAUDE.md §4; nomes e ordem das etapas são da fonte.
  Mapeamentos individualmente discutíveis, todos `[PROPOSTA]`: "avanço modular" (P11 20, P12 26)
  recebeu E6 por ser retorno ao laço de execução; "elaboração da carta" (P14 25) recebeu E6 por
  ser produção de artefato, embora esteja entre duas etapas de verificação. **Nenhum código
  itera fases** — percorrer a espinha seria fundir execução, e a espinha nomeia fases, não funde
  execução [CLAUDE.md §4].

- **LAC-FUNC-014 — o campo "decisões" da R03 CAMADA B não tem seção correspondente em contrato
  algum.** Nenhum dos cinco tem "§ DECISÕES". O campo foi preenchido com pontos de decisão que
  os contratos identificam como tais em outras seções (etapas de decisão humana, gates
  nominados, regras de encaminhamento), cada item com sua citação. Não é transcrição de uma
  lista existente; é agregação com fonte item a item.

## Status e abstenção

- **LAC-FUNC-010 — `OUT_OF_SCOPE` só está ligado a uma condição no P11.** P11 §34 mapeia
  explicitamente: "pedido fora do escopo → `OUT_OF_SCOPE`". Em P12 (§28.3, §37), P13 (§31.2) e
  P14 (§51.2) a categoria é membro de enum e **nenhuma condição mapeia para ela**. Em P10 a
  condição existe — §32.2 lista "pedido fora do escopo" e manda usar `ABSTAINED` — mas a lista
  de categorias de abstenção do próprio P10 (§28.2) tem só cinco membros e **não inclui
  `OUT_OF_SCOPE`**: defeito da fonte, não omissão de leitura. Pior para a decisão: o caso
  análogo mais próximo do acervo, P14 PS14-08 ("Demanda fora do escopo"), resolve em `SUCCESS`
  para avaliação de admissibilidade + `InterventionRecord.disposition=REFUSED` + decisão
  `NAO_APLICAVEL` — precedente contrário ao uso de `ABSTAINED/OUT_OF_SCOPE`. **Decisão:**
  `abstencao_por_fora_de_escopo` segue a linha transversal do P09 §23 ("Operação fora do escopo
  → `ABSTAINED/OUT_OF_SCOPE`"), por ser regra do contrato de runtime e não de um contrato de
  função, e porque o caso do roteador é material não declarado *na porta*, enquanto PS14-08 é
  demanda fora de escopo *dentro* de uma execução legítima. As duas leituras estão em
  `docs/spec/divergencias.md §4.4`; a divergência não foi reconciliada.

- **LAC-FUNC-012 — `PARTIAL_SUCCESS` não tem condição mapeada em P10, P11 nem P13.** Nos três
  aparece uma única vez, no enum de status (P10 §27.4, P11 §24.2, P13 §31.1). Só P12 (PS12-01) e
  P14 (PS14-11) definem cenário que o produza. Nada nesta peça produz status; a lacuna fica
  registrada para quem for montar respostas.

- **LAC-FUNC-016 — nenhum contrato declara teto numérico de intervenção.** A afirmação do
  CLAUDE.md §6 de que "P13 para em `SINALIZACAO`/`RECOMENDACAO`" é leitura, não citação: o P13
  proíbe que o comentário execute reescrita, fusão, corte, substituição ou reorganização [§4.4]
  e exige registrar `intervention_level` por comentário [§28], mas nunca nomeia um nível
  `INT-nn` como teto. `DeclaracaoDeFuncao` **não tem** campo de teto de intervenção — criá-lo
  exigiria preencher os seis por inferência. Os limites ficam em `limites`, em prosa citada.

## Decisões de implementação verificáveis apenas por proxy

- **A correspondência `function_id` request↔response nasce aqui, não em `contrato/`.**
  `escolio/contrato/resposta.py::exige_correspondencia_request_response` confere `request_id`,
  `project_id` e `component_id`, e omite `function_id`, que o P09 §8.1 exige. Consertar ali seria
  alterar código existente; `roteador.py::exige_correspondencia_de_funcao` cobre a linha sem
  tocar em nada. Consolidação registrada em `docs/backlog.md`, BL-011. Enquanto durar, há duas
  funções de correspondência e quem chama precisa das duas.

- **`InputItem.classification.functions` nunca é populado por ninguém.** O campo existe em
  `escolio/contrato/entrada.py:36` e `escolio/adaptadores/ingestao_para_input_item.py` declara
  explicitamente que preenchê-lo "é trabalho de P19/roteador de função". O roteador **lê** o
  campo; populá-lo é ato de `CURADOR_DE_DADOS` + `USUARIO_PROPONENTE` sob o P19, não deste
  pacote. Em consequência, hoje todo `InputItem` produzido pela ingestão resulta em
  `AdmissaoDeMaterial.INDETERMINADO`. Registrado em BL-014.

- **`LAC-FUNC-017` — P10 e P11 discordam sobre o estado de homologação do P10.** P10 §42 declara
  `P10_NAO_HOMOLOGADO` e `P10_NAO_AUDITADO_APOS_SEGUNDA_CORRECAO`; P11 §45.2 declara
  `P10_HOMOLOGADO_E_CONGELADO`. Nenhum dos dois foi adotado como verdade: as declarações não
  carregam campo de estado de homologação, e a divergência fica aqui. Aparentada com a
  contradição já registrada em `docs/spec/autoridade-e-lacunas.md §2`.

- **Os fixtures existentes usam `function_id="P12"`.** `tests/contrato/test_requisicao.py:18` e
  `tests/contrato/test_resposta.py:37` passam o código do componente onde agora vai um
  `LLM-ACA-F0x`. Não quebram — `requisicao.py` só verifica não-vazio — mas divergem do catálogo.
  Não foram alterados. Registrado em BL-012.

## Não incluído nesta peça (fora de escopo, não lacuna)

- **Execução de qualquer etapa.** Não há `executar` em nenhum dos nove módulos, e é deliberado:
  POL-012 proíbe "executar encadeamento automático" e permite "registrar exatamente uma próxima
  ação permitida ou nenhuma automática". `DeclaracaoDeFuncao.proxima_etapa` devolve o sucessor
  ordinal, um só, e devolvê-lo não o autoriza.

- **`Response.interventions`.** Ligar `InterventionRecord` ao envelope de resposta estava
  reservado em `docs/backlog.md` BL-006 para "quando o roteador de função existir". O roteador
  passa a existir, mas ligar altera `escolio/contrato/resposta.py`. Registrado em BL-013.

- **Estados internos por função.** P10 §31 (23 estados), P11 §32 (26), P13 §36 e equivalentes são
  máquinas próprias de cada função, distintas do status P09 e da máquina documental do P03. Só a
  do P10 foi transcrita, e como `OrdemDeclarada`, por ser a sequência mais completa que aquele
  contrato oferece. As demais ficam para a implementação de cada função.

- **Schemas de saída por função.** `P13Comment` [P13 §31.5], matriz de aderência [P12 §10],
  matriz de demandas [P14 §21] e matriz de transposição [P10 §14] são produtos das funções, não
  do roteador.

- **Objetos congelados.** `escolio/intervencao/LACUNAS.md` deixou o tratamento "para o roteador
  de função, quando existir estado de objeto a consultar". O roteador existe e continua não
  havendo campo de objeto congelado no P09 §13 nem estado de objeto a consultar: a lacuna
  permanece onde está, não migra para cá.

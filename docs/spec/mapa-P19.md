# MAPA DO P19 — Plano de Dados e Classificação de Materiais

Fonte: `corpus/handoff-P22/PACOTE_HANDOFF_REQUISITOS_ENGENHEIRO_LLM_R01/FONTES_CANONICAS/PACOTE_PLANO_DE_DADOS_LLM_ACADEMICA_R01/P19_PLANO_DE_DADOS_E_CLASSIFICACAO_DE_MATERIAIS_HOMOLOGADO_R01.md`,
lido integralmente nesta sessão (2026-08-06). Antes desta leitura, o P19 só havia sido
consultado por amostragem (`docs/backlog.md` BL-009).

Convenção de citação: `[P19 §N]` remete à numeração interna do próprio arquivo (`§1`…`§80`,
mais os cenários `PS19-01`…`PS19-09` na `§80`). Fidelidade literal — trecho entre aspas é
transcrição exata; sem aspas é paráfrase estrita da lista/tabela da fonte.

**Natureza declarada da entrega:** "elaboração substantiva integral, documental e funcional
do P19, sem classificação de material real, sem ingestão, sem criação de corpus e sem
escolha de arquitetura técnica" [P19 §identidade]. Isso vale para o P19 como documento —
não para os módulos que o implementam depois dele (ver §6 abaixo, sobre o adaptador já
construído).

---

## 1. Identidade e posição no ecossistema

`ID: P19` · `Fase: F5` · `Camada: DADOS` · `Responsável funcional: CURADOR_DE_DADOS` ·
`Homologador: USUARIO_PROPONENTE` · `Destinatário: ENGENHEIRO_LLM` [P19 §1].

Dependências obrigatórias: P02, P03, P04, P05, P08, P09, P10, P11, P12, P13, P14.
Dependências condicionais: P15–P18, sob a regra
`COMPONENTE_CONDICIONAL_NAO_ATIVADO_NAO_BLOQUEIA_P19` [P19 §1].

O P19 governa 28 itens documentalmente — identificação, proveniência, custódia,
titularidade, licença, autorização, finalidade, admissibilidade, classificação funcional,
segurança, privacidade, acesso, sensibilidade, versionamento, integridade, retenção,
descarte, anonimização, pseudonimização, minimização, rastreabilidade, isolamento entre
projetos, elegibilidade (RAG/exemplo/teste/dado supervisionado), incorporação futura de
módulos condicionais, relação futura com P20/P21/P22 [P19 §2]. "A disponibilidade material
não produz autorização automática para qualquer finalidade" [P19 §2].

---

## 2. Os 27 campos de `MaterialUnit` e quem preenche cada um

Fonte literal da lista de campos: `[P19 §9]`. Nenhum algoritmo de hash é definido; nenhum
campo desconhecido pode ser preenchido por inferência; campo não aplicável é `null`, nunca
texto vazio; elegibilidades são independentes; autorização é finalidade-específica
[P19 §9, regras].

Coluna "quem preenche" combinada com `[P19 §6]` (tabela de papéis/autoridades) e `[P19 §73]`
(limites de autonomia do curador).

| # | Campo | Quem preenche / decide | Base |
|---|---|---|---|
| 1 | `material_id` | Mecânico — regra de identidade, sem julgamento | `[P19 §10]` |
| 2 | `project_id` | Vínculo estrutural, dado de entrada obrigatório | `[P19 §7.1, §31]` |
| 3 | `material_name` | Curador registra a partir da entrada | `[P19 §7.1]` |
| 4 | `material_type` | Curador classifica; `null` só sob as 7 condições da `§17` | `[P19 §17]` |
| 5 | `source_reference` | Curador registra | `[P19 §7.1]` |
| 6 | `source_hash` | Mecânico — "tecnologicamente neutro", nenhum algoritmo escolhido pelo P19 | `[P19 §9, §27]` |
| 7 | `source_version` | Curador registra; versão nunca elimina a anterior | `[P19 §26]` |
| 8 | `derived_from` | Curador registra quando aplicável | `[P19 §29]` |
| 9 | `provenance_status` | Curador classifica dentre os 5 estados da `§11` | `[P19 §11]` |
| 10 | `owner_or_controller` | **Titular ou controlador do material** — autoridade jurídica/documental contextual; curador não pode se autoautorizar | `[P19 §6, §13]` |
| 11 | `license_status` | **Titular/controlador** informa; curador classifica dentre os 8 estados | `[P19 §6, §14]` |
| 12 | `authorization_basis` | **Usuário-proponente** (autorização expressa) ou outra base da `§16`; curador não concede | `[P19 §16, §73]` |
| 13 | `authorized_purposes` | **Usuário-proponente** autoriza finalidade; curador propõe, não concede | `[P19 §15, §73]` |
| 14 | `prohibited_purposes` | Mesma autoridade de `authorized_purposes`, por exclusão | `[P19 §15]` |
| 15 | `privacy_classification` | **Responsável por privacidade** decide condições; curador classifica preliminarmente | `[P19 §6, §19]` |
| 16 | `security_classification` | Curador classifica dentre os 6 estados da `§18` | `[P19 §18]` |
| 17 | `access_classification` | Curador propõe; decisão de acesso é de autoridade | `[P19 §20]` |
| 18 | `sensitivity` | Curador classifica dentre os 6 estados da `§21` | `[P19 §21]` |
| 19 | `retention_class` | Curador propõe; "nenhum prazo concreto é inventado" | `[P19 §22, §56]` |
| 20 | `disposal_rule` | Curador propõe; descarte real exige decisão e autoridade | `[P19 §23, §57]` |
| 21 | `rag_eligibility` | **Usuário-proponente** via `GATE_DE_AUTORIZACAO_PARA_RAG`; curador não libera | `[P19 §25, §35, §53]` |
| 22 | `example_eligibility` | **Usuário-proponente** via `GATE_DE_AUTORIZACAO_PARA_EXEMPLO` | `[P19 §25, §36, §53]` |
| 23 | `test_eligibility` | **Usuário-proponente** via `GATE_DE_AUTORIZACAO_PARA_TESTE`; materialmente definido pelo P20 | `[P19 §25, §37, §53]` |
| 24 | `supervised_data_eligibility` | **Usuário-proponente** via `GATE_DE_AUTORIZACAO_PARA_DADO_SUPERVISIONADO`; condicional ao eventual P21 | `[P19 §25, §39, §53]` |
| 25 | `audit_status` | **Auditor independente** — "audita sem corrigir" | `[P19 §6, §41]` |
| 26 | `human_gate` | Identificado pelo curador; concedido só por autoridade humana — "gate identificado não equivale a gate concedido" | `[P19 §45, §53, §72]` |
| 27 | `current_state` | Reflete a máquina de decisão interna (`§52`, `§74`) | `[P19 §52, §74]` |
| — | `limitations`, `created_at`, `updated_at` | Registro mecânico do curador, sem decisão de autorização | `[P19 §9]` |

Nota de leitura: a lista da `§9` tem 27 nomes de campo mais `created_at`/`updated_at` — a
contagem "27 campos" citada na tarefa corresponde à lista entre `material_id` e
`updated_at` inclusive; a tabela acima preserva a ordem literal da fonte.

---

## 3. A proibição de §71–73 — texto e alcance exato

### §71 — Ações autorizadas (o que este documento, como elaboração, pode fazer)

"definir taxonomias; definir registros; definir estados; definir critérios; propor
classificação abstrata; definir matrizes; definir gates; definir relações; definir
cenários; definir testes; preparar para auditoria" [P19 §71].

### §72 — Ações proibidas (verbatim, 24 itens)

1. classificar material real
2. executar ingestão
3. copiar material para corpus
4. indexar
5. criar embedding
6. executar RAG
7. criar exemplo supervisionado
8. criar teste real
9. criar gabarito real
10. executar treinamento
11. executar fine-tuning
12. ativar P15–P18
13. iniciar P20–P28
14. escolher modelo
15. escolher fornecedor
16. escolher plataforma
17. escolher banco
18. escolher hash
19. escolher formato de persistência
20. reabrir P00–P14
21. ativar P10–P14
22. importar outro projeto
23. auditar
24. homologar

[P19 §72]

### §73 — Limites de autonomia do curador de dados

**Pode:** "registrar; propor; classificar abstratamente; identificar pendências;
identificar gates; recomendar quarentena; recomendar rejeição; preparar matriz"
[P19 §73].

**Não pode:** "conceder autorização; conceder licença; liberar RAG; liberar dados
supervisionados; decidir descarte irreversível; resolver conflito de titularidade;
executar processamento; homologar" [P19 §73].

### Alcance exato

A proibição do §72 é sobre **esta elaboração do P19** — o documento em si, produzido pelo
`CURADOR_DE_DADOS` nesta ação — não sobre todo trabalho futuro do ecossistema. O item 1
("classificar material real") é a trava operante para qualquer módulo que, hoje, tente
preencher os campos de `MaterialUnit` (`§9`) contra um documento real (ex.: um PDF em
`data/dev/`): fazer isso seria produzir a classificação que o próprio texto do P19 se proíbe
de produzir nesta entrega, sem que exista ainda um fluxo homologado com gates (`§53`) que
autorize essa classificação a ocorrer fora dela.

Consequência prática já registrada em código: `escolio/adaptadores/ingestao_para_input_item.py`
implementa apenas a regra de identidade de `material_id` (`§10`, ver `§6` abaixo) e para
aí — os 26 campos restantes de `MaterialUnit` ficam documentados como lacuna
(`escolio/ingestao/LACUNAS.md`, `LAC-ING-012`), não implementados, precisamente porque
implementá-los seria "classificar material real" sem o fluxo do `§79` ter sido percorrido
até `homologar`.

O §72 não proíbe eternamente essas 24 ações — proíbe-as **nesta elaboração**. `§44` já
prevê o procedimento futuro para quando P15–P18 forem homologados e ativados (inventariar,
mapear, verificar compatibilidade, definir finalidade, aplicar P08/P09, conceder gate,
registrar versão, auditar), e `§79` (fluxo modular) prevê as mesmas 28 etapas terminando em
"homologar" e "transferir ao fluxo técnico posterior, quando autorizado" — mas "nesta ação,
o fluxo termina na definição documental" [P19 §79].

---

## 4. Gates humanos exigidos, e por quem

Lista canônica, 19 gates `[P19 §53]`:

1. `GATE_DE_ADMISSAO_DE_MATERIAL`
2. `GATE_DE_MATERIAL_SEM_PROVENIENCIA_COMPLETA`
3. `GATE_DE_LICENCA`
4. `GATE_DE_PRIVACIDADE`
5. `GATE_DE_DADO_SENSIVEL`
6. `GATE_DE_DOCUMENTO_DO_USUARIO`
7. `GATE_DE_MATERIAL_RESTRITO`
8. `GATE_DE_MATERIAL_PROIBIDO`
9. `GATE_DE_AUTORIZACAO_PARA_RAG`
10. `GATE_DE_AUTORIZACAO_PARA_EXEMPLO`
11. `GATE_DE_AUTORIZACAO_PARA_TESTE`
12. `GATE_DE_AUTORIZACAO_PARA_DADO_SUPERVISIONADO`
13. `GATE_DE_RECLASSIFICACAO`
14. `GATE_DE_RETENCAO`
15. `GATE_DE_DESCARTE`
16. `GATE_DE_REVOGACAO`
17. `GATE_DE_INCORPORACAO_DE_MODULO_CONDICIONAL`
18. `GATE_DE_AUDITORIA_DE_DADOS`
19. `GATE_DE_HOMOLOGACAO`

"Gate identificado não equivale a gate concedido" [P19 §53, repetido como invariante 45
em `§4`].

**Por quem cada classe de gate é concedida** — cruzando `§6` (papéis/autoridades) com os
cenários da `§80`:

- **`USUARIO_PROPONENTE`** — "Autoridade homologadora"; "Homologar, autorizar finalidades e
  conceder gates" [P19 §6]. Concede, na prática dos cenários: `GATE_DE_ADMISSAO_DE_MATERIAL`
  (`PS19-01`, `PS19-04`, `PS19-06`), `GATE_DE_DOCUMENTO_DO_USUARIO` (`PS19-02`),
  `GATE_DE_AUTORIZACAO_PARA_RAG` (`PS19-03`), `GATE_DE_LICENCA` (`PS19-05`),
  `GATE_DE_MATERIAL_SEM_PROVENIENCIA_COMPLETA` (`PS19-06`),
  `GATE_DE_AUTORIZACAO_PARA_EXEMPLO` (`PS19-07`),
  `GATE_DE_AUTORIZACAO_PARA_DADO_SUPERVISIONADO` (`PS19-08`), `GATE_DE_HOMOLOGACAO` (`§53.19`).
- **`Titular ou controlador do material`** — "Autoridade jurídica ou documental
  contextual"; "Definir permissões compatíveis" [P19 §6] — base de fato para
  `GATE_DE_LICENCA`.
- **`Responsável por privacidade`** — "Autoridade contextual"; "Decidir condições de
  tratamento" [P19 §6] — base de fato para `GATE_DE_PRIVACIDADE` e `GATE_DE_DADO_SENSIVEL`.
- **`Curador BVAA`** — "Autoridade bibliográfica"; "Informar estados de fonte e leitura"
  [P19 §6] — alimenta `GATE_DE_ADMISSAO_DE_MATERIAL` para `FONTES_BIBLIOGRAFICAS` (`§34`).
- **`Curador de dados`** — "Autoridade classificatória limitada"; "Elaborar registros,
  propor classificação e preservar rastreabilidade" [P19 §6]. **Identifica** todos os
  gates acima; **não concede nenhum** [P19 §73, §6 ("O curador de dados não pode
  conceder a si próprio autorização de uso.")].
- **`Auditor independente`** — "Autoridade de verificação"; "Auditar sem corrigir"
  [P19 §6] — concede/nega `GATE_DE_AUDITORIA_DE_DADOS`; nunca corrige o material auditado
  [P19 §46: `AUDITORIA_NAO_CORRIGE`].
- **`Controlador-arquiteto`** — "Autoridade de escopo e dependências"; "Verificar
  precedência, isolamento e gates" [P19 §6] — verifica que o gate exigido para uma etapa
  existe e foi satisfeito, sem ele mesmo conceder o gate de conteúdo.
- **`Operador autorizado futuro`** — "Autoridade operacional delimitada"; "Executar
  ingestão apenas após autorização específica" [P19 §6] — executa só depois que os gates
  acima já foram concedidos; não decide gate.
- **`Engenheiro LLM`** — "Destinatário técnico"; "Implementar somente após homologação e
  handoff" [P19 §6] — não concede gate algum; implementa depois que a cadeia de gates
  acima já foi percorrida.

---

## 5. O que o P19 impõe sobre `data/`, anonimização e material de aluno

CLAUDE.md §12 aponta "Schema de material e classificação de dados: **`P19`**" como
autoridade, sem detalhar. O detalhe está distribuído assim na fonte:

### Regra geral sobre `data/`

"`data/` nunca vai para o git" é regra do CLAUDE.md, não do P19 — o P19 não menciona git
nem repositório; governa a **classificação documental** de qualquer material, independente
de onde ele fica armazenado tecnicamente (`§61`: "Não define sistema técnico de identidade
e acesso"; `§70`: "P19 não... escolhe armazenamento").

O que o P19 de fato impõe sobre material como o PDF de aluno em `data/dev/`:

- **Categoria funcional obrigatória.** Um PDF de trabalho de aluno enviado para revisão é,
  por natureza, `DOCUMENTOS_DO_USUARIO` — uma das 16 categorias controladas de `§17`.
- **Regra fechada sobre documentos do usuário** `[P19 §33]`, verbatim (lista): permanecem
  `DOCUMENTOS_DO_USUARIO`; conservam finalidade original; não se tornam RAG; não se tornam
  exemplos; não se tornam testes; não se tornam gabaritos; não se tornam dados
  supervisionados; podem ser revogados, quando aplicável; devem ser minimizados;
  permanecem isolados.
- **Invariante 2** `[P19 §4]`: `DOCUMENTO_DO_USUARIO_NAO_E_MATERIAL_PARA_RAG`.
- **Invariante 20/21** `[P19 §4]`: `DOCUMENTO_DO_USUARIO_PERMANECE_VINCULADO_AO_PROJETO`;
  `DOCUMENTO_DO_USUARIO_NAO_PODE_SER_REUTILIZADO_SILENCIOSAMENTE`.
- **Cenário `PS19-02`** ilustra o caso positivo (documento do usuário autorizado só para
  revisão: `rag_eligibility`/`example_eligibility`/`test_eligibility`/
  `supervised_data_eligibility` todos `NAO_ELEGIVEL`, gate `GATE_DE_DOCUMENTO_DO_USUARIO`)
  e `PS19-03` o caso de recusa (mesma entrada proposta indevidamente para RAG:
  `decisão interna REJEITAR`, `InterventionRecord.disposition=REFUSED`) [P19 §80].

### Anonimização

- **§58**, condições cumulativas para declarar anonimização: "houver critério aplicável;
  o risco residual for avaliado; a transformação for registrada; a reversibilidade indevida
  for controlada; a autoridade confirmar o estado." "Nenhum algoritmo é escolhido" [P19 §58].
- **Invariante 39** `[P19 §4]`: `ANONIMIZACAO_NAO_DEVE_SER_PRESUMIDA`.
- **§19**, classificação de privacidade: "a mera remoção de nomes não autoriza declarar
  anonimização" — a categoria correta para nomes removidos sem avaliação de risco residual
  é `DADO_PSEUDONIMIZADO`, não `DADO_ANONIMIZADO_COM_BASE_CONFIRMADA` [P19 §19, §59].
  Isso é diretamente relevante à convenção do CLAUDE.md §12 ("anonimizar autor e
  instituição na ingestão"): remover nome de autor/instituição do texto, por si, produz
  no máximo `DADO_PSEUDONIMIZADO` segundo o vocabulário do P19 — chamar isso de
  "anonimizado" sem avaliar risco residual de reidentificação seria o erro que a `§19`
  proíbe nomeadamente.
- **§59**, pseudonimização: "reduz exposição; mantém possibilidade controlada de
  reidentificação; exige proteção da chave ou relação; não transforma automaticamente o
  material em público; não elimina obrigações de privacidade."
- **§60**, minimização (aplica-se à ingestão de qualquer material de aluno): "reter apenas
  campos necessários; evitar duplicação; evitar conteúdo sensível em logs; reduzir
  excertos; separar metadados de conteúdo; limitar acesso; remover finalidades não
  autorizadas."

### Classificação de material de aluno — cadeia completa exigida antes de qualquer uso além de leitura/revisão

Para admitir um documento de aluno para qualquer finalidade (`§45`): pertencer ao projeto
ou possuir autorização; possuir proveniência suficiente; possuir finalidade definida;
possuir licença ou base compatível; possuir classificação de privacidade; possuir
classificação de segurança; não conter autoridade documental indevida; não estar proibido;
não estar revogado; não violar isolamento; não depender de inferência para justificar uso;
possuir gates concedidos [P19 §45].

Torna inadmissível (`§46`): finalidade ausente; uso solicitado incompatível; licença
incompatível; autorização ausente; pertencer a outro projeto sem permissão; estar
revogado; estar proibido; exigir execução de instruções adversariais; violar privacidade;
não poder ser minimizado com segurança; depender de fabricação de proveniência [P19 §46].

---

## 6. O que fica bloqueado enquanto não houver curadoria homologada

Nada do que segue é bloqueio no sentido de `BlockCategory` do P09 — é ausência de
autorização, que o próprio P19 distingue de bloqueio técnico (`§77`, `§49`). Mas,
operacionalmente, enquanto o P19 não estiver homologado e a cadeia de gates da `§4` não
tiver sido percorrida para um material real:

- **Nenhum material real pode ser classificado** — item 1 do `§72`, ver `§3` acima.
- **Nenhuma elegibilidade pode ser concedida** — `rag_eligibility`,
  `example_eligibility`, `test_eligibility`, `supervised_data_eligibility` ficam, no
  máximo, `PENDENTE`; conceder qualquer uma delas sem gate seria "elegibilidade... por
  inferência", proibida nominalmente em `PS19-06` [P19 §80].
- **RAG sobre qualquer documento do projeto está bloqueado por default** — invariantes
  2/9/10 `[P19 §4]` e `§35` (10 pré-condições, nenhuma satisfeita sem homologação):
  autorização específica; proveniência suficiente; licença compatível; finalidade;
  privacidade; segurança; política de atualização; política de revogação; isolamento;
  gate concedido.
- **Nenhum exemplo real, teste real ou gabarito real pode ser criado** — itens 7-9 do
  `§72`; `§36` exige autorização específica mesmo para exemplo real; `§37`/`§38` deixam
  testes e gabaritos como domínio futuro do P20, ainda não iniciado.
- **Nenhum dado supervisionado existe nem pode existir** — `§39`: "permanecem: não
  criados; não autorizados; condicionais; dependentes de P19 homologado; dependentes de
  P20 homologado; dependentes de autorização específica." Isso inclui, nomeadamente, o
  item 6 da lista ABERTO do CLAUDE.md §13 (congelar `histórico de resolução` /
  `exemplos de comentários aceitos` como corpus supervisionado) — P21, "condicional,
  não iniciado" [P19 §69], depende do P19 estar homologado primeiro.
- **Nenhum treinamento ou fine-tuning** — itens 10-11 do `§72`; invariante 10 `[P19 §4]`:
  `AUTORIZACAO_PARA_RAG_NAO_E_AUTORIZACAO_PARA_TREINAMENTO`.
- **Nenhuma auditoria de dados nem homologação nesta ação** — itens 23-24 do `§72`; a
  auditoria e a homologação do próprio P19 são etapas *posteriores* a esta elaboração, não
  parte dela.
- **P15–P18 continuam não ativados e não presumidos** — `§67`: "não bloqueiam; não geram
  categorias concretas; não fornecem materiais; não são presumidos." A ausência deles não
  é, ela mesma, um bloqueio a mais — é a mesma regra de não bloqueio de `§1`.
- **O que permanece permitido nesse meio-tempo**: leitura e revisão documental sob
  autorização limitada (o caso `PS19-02`), que é exatamente o que
  `escolio/adaptadores/ingestao_para_input_item.py` produz hoje — um `InputItem` [P09 §6]
  por documento, sem nenhuma elegibilidade concedida, sem `MaterialUnit` completo.

---

## 7. Rastro de decisão já tomada com base nesta leitura

- `escolio/adaptadores/ingestao_para_input_item.py` — implementa só a regra de identidade
  de `material_id` [P19 §10]; documenta em docstring por que os outros 26 campos de
  `MaterialUnit` ficam fora, citando `§71-73`.
- `escolio/ingestao/LACUNAS.md`, `LAC-ING-012` — mesma decisão, do lado da ingestão.
- `docs/backlog.md`, `BL-003` — marcado `RESOLVIDO PARCIALMENTE` com a mesma justificativa.
- Este mapa fecha `BL-009` na parte que trata do P19 (o item também cobria P08, P20, R03,
  ainda sem mapa).

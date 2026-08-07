# Reescrita do CLAUDE.md — o que saiu, o que entrou, e de onde veio

Sessão de 2026-08-06. O CLAUDE.md anterior foi escrito no primeiro dia do projeto, antes de
qualquer leitura do acervo. Esta reescrita o deriva da especificação homologada.

Critério autorizado em `docs/autorizacao.md`: onde a spec for mais completa, ela vence; onde for
silenciosa, proposta marcada `[PROPOSTA]`.

---

## 1. O que saiu

| Seção antiga | Por quê |
|---|---|
| §3 — sete eixos de avaliação | Não existem em nenhum pacote. Nenhuma das seis funções usa essa taxonomia. O que existe: 15 níveis de intervenção [P06], cinco escalas graduadas distintas (ver §4 abaixo), suficiência e confiança como eixos separados [P05; P09 §12] |
| §4 — pipeline C0–C5 | Invenção. A spec tem camadas A–P e fases 0–12 [R03 §5–6], e 25–32 etapas nomeadas por função [P11 §38; P12 §41; P13 §43; P14 §75] |
| §4 — "Opus nunca lê o documento completo… acima de ~8k tokens" | O **princípio** sobrevive, com origem derivada de custo. O **número 8k** não tem fonte e saiu |
| §4 — "`budget_tokens` teto 2000" | Hoje causa **erro 400**: o parâmetro foi removido no Opus 5 e no Sonnet 5 |
| §4 — "extended thinking desligado por padrão" | **Falso** no Opus 5: omitir `thinking` roda adaptive |
| §5 — tabela de modelos por sessão 0A–0D / 1–8 | Numeração de um plano que não existe mais; nenhum arquivo em `docs/sessions/` corresponde |
| §7 — schema de achado de oito campos | Substituído pelo envelope P09 (§5 do novo) |
| §8 — regras de dados | Território do P19. Regra duplicada que diverge da fonte é pior que regra ausente. O novo aponta para o P19 e mantém só o que é operacional imediato (`data/` fora do git, anonimizar, corpus somente leitura) |
| §1b — dicotomia "modo comentário" vs "modo ouro" | Dissolvida na escada de 15 níveis do P06 (§6 do novo) |
| §2 — "cada tipo tem rubrica própria em `style/rubrics/`" | O diretório não existe, e a spec organiza por **função**, não por rubrica — um tipo sem função não tem onde pendurar uma |
| §10 — referência a `docs/coleta.md` | Mantida; o arquivo passou a existir |

### O que **não** saiu, apesar de eu ter proposto que saísse

**§9, método de três fontes** (declarado / praticado / tácito). Cheguei a propor renomeá-lo para
`PERFIL_HIBRIDO_DECLARACAO_MAIS_AMOSTRAS` [P07/04]. Isso pressupõe justamente a leitura do P07
que ficou registrada como divergência aberta. Fica no vocabulário do professor até o eixo 7
resolver.

**A convenção de procedência** `[acervo:arquivo]` / `[diff:capítulo]` / `[entrevista]` /
`[INFERIDO]`. Eu a havia derrubado em silêncio. O `provenance` obrigatório do P05 [P05/02] e a
POL-005 cobrem *registros*; estes marcadores cobrem markdown editado à mão, e nada na spec os
substitui.

---

## 2. O que entrou

| Novo | Origem |
|---|---|
| Papéis canônicos e onde eu me situo (`ENGENHEIRO_LLM`) | R03 §4, §4.5 |
| Estado de autorização e o que continua exclusivamente humano | `docs/autorizacao.md`; P22 §24 |
| **Seis** funções, incluindo X01 | P02 (F01–F05 + X01); R03 CAMADA B item 6 |
| Mapeamento tipo → função, com dois tipos sem função | P10–P14; R03 CAMADA B; `LAC-P02-005` |
| `ABSTAINED/OUT_OF_SCOPE` para tipo sem função | P09 §4.2.6, §23 |
| Espinha de sete etapas, com autonomia por função | destilada de P11 §38, P12 §41, P13 §43, P14 §75; agrupamento `[PROPOSTA]` |
| Gates não moram todos numa fase (`GATE_DE_SELECAO` dentro do E4) | P13 §32.1, §43 |
| Seleção do P13 em três etapas, com critério verbatim | P13 §11, §12, §43 |
| Simetria de zero comentários / silêncio diante de risco material | P13 §25 |
| Conjunto vazio = `SUCCESS`, não abstenção | P09 §8.2 |
| Envelope P09 como contrato de runtime | P09 §4, §8, §9, §12, §13 |
| Escada de 15 níveis `INT-01…INT-15` e regressão segura | P06/01 §2, §7, §8; P06/02 |
| Cinco escalas graduadas distintas | P13 §11, §14.1, §14.2; P20 §26; P09 §14 |
| Três vocabulários bibliográficos não reconciliados | P04/03; R03 CAMADA D; P05; `CON-P05-001` |
| Instrução que virou invariante | contorno-vs-criterio [INVERTIDO]; P09 §21; P08 §2; P05 RC-016 |
| Superfície editável pelo professor | P13 §6.2, §6.3; P07/02, P07/03 |
| Proibição de arquivo de limiares | P13 §11, §34, §3.9 |
| Calibragem por `histórico de resolução` como entrada, não treino | P13 §6.3, §31.5.2; R03 CAMADA K |
| Política de modelos por tamanho, `effort` por etapa, batch × cache | `docs/custos.md` |
| Lista ABERTO com dez itens nomeados | ver §4 abaixo |

---

## 3. Decisões do professor tomadas nesta sessão

1. **Eixo 7 / voz de quem comenta:** registrar divergência, não decidir.
2. **Seção de dados:** cortar; apontar para o P19.
3. **Pipeline:** espinha comum com autonomia preservada — nomeia fases, não funde execução.
4. **Meu papel:** `ENGENHEIRO_LLM`.
5. **Modos de saída:** dissolver na escada do P06.
6. **Perguntas nunca respondidas:** nenhuma vira regra; todas vão para ABERTO.

---

## 4. Defeitos meus corrigidos antes de escrever

Registrados porque cada um quase entrou no documento.

1. **"As cinco funções."** Repetido a sessão inteira. São **seis** — F01–F05 **+ X01**, gestão
   transversal de fontes, citações e suficiência de evidência. X01 é a função que o código já
   existente (`escolio/`) implementa.
2. **Alarme de `DERIVA_MONOLITICA_BLOQUEADORA`** contra a espinha comum, levantado sem ler a
   fonte. Lido `P01/05` integralmente: as nove proibições tratam de componentes como objetos
   documentais no ciclo de governança (*executar, auditar, homologar, iniciar P(n+1)*) e o bloco
   `ACELERACAO_PERMITIDA` é inteiramente documental. **A trava não alcança runtime.** O alarme
   era mais forte do que o texto sustenta. Duas proibições permanecem como teste de projeto.
3. **`style/style_card.md` mapeado no perfil de voz do P13 §6.2.** Erro: aquele campo é a voz do
   **autor avaliado**, a preservar. O style card é a voz de **quem comenta** — o eixo 7 em
   aberto. O style card está bloqueado, não realocado.
4. **Convenção de procedência derrubada em silêncio.** Restaurada.
5. **"Tese ≈ 200k tokens."** Chute. Medido: 272 páginas, 608.043 caracteres, 91.113 palavras.
   O token count ficou marcado como pendente em vez de estimado.
6. **§12 sem política por tamanho, sem `effort`, sem custo de output, e apontando o reenvio do
   documento como gasto dominante** — quando o dominante é o fan-out por unidade.
7. **Método de três fontes renomeado para o vocabulário do P07**, pressupondo a leitura deixada
   em aberto. Revertido.

---

## 5. Divergências registradas, não resolvidas

Ambas em `docs/spec/divergencias.md`, cada uma com as duas leituras:

- **P07 × eixo 7** — o P07 governa também a voz de quem comenta, ou só a do autor avaliado?
- **`docs/autorizacao.md` × `P01/05`** — a carta branca é um ato coletivo cobrindo doze decisões;
  o `P01/05` proíbe "emitir autorização coletiva". Leitura contrária: R03 §4.1 faz do
  `USUARIO_PROPONENTE` autoridade final. Caminho que fecha sem interpretação: reemitir
  `autorizacao.md` em forma itemizada.

---

## 6. Correção posterior — contagem errada em §9 (encontrada em 2026-08-07)

**"24 obrigatórias" estava errado.** A reescrita de 2026-08-06 registrou, em §9, "30 dimensões
`VOZ-D01…D30`, 24 obrigatórias" para o perfil de voz do autor avaliado [P07]. A contagem literal
do CSV fonte, `03_DICIONARIO_DE_DIMENSOES_DE_VOZ_P07_R01.csv`, é **26 obrigatórias e 4
opcionais** (`VOZ-D16` `preferencias_lexicais`, `VOZ-D17` `termos_desaconselhados`, `VOZ-D18`
`abertura_encerramento`, `VOZ-D19` `recursos_retoricos` — as únicas quatro linhas marcadas
`opcional`; as 26 restantes são `obrigatória`).

O erro só foi detectado na sessão seguinte, ao implementar `escolio/voz/` (item 5 do roadmap) e
contar as linhas do CSV diretamente para `escolio/voz/dimensoes.py::DEFINICOES` — nenhuma
verificação de contagem foi feita contra o CSV durante a reescrita de 2026-08-06 em si; "24" foi
escrito sem recontar a fonte. Corrigido em §9 para "26 obrigatórias, 4 opcionais (D16-D19)".
Registrado em `escolio/voz/LACUNAS.md` no momento da implementação, e aqui para não ficar só no
LACUNAS de um módulo — este é um defeito da reescrita do CLAUDE.md, não do módulo.

**Auditoria das demais contagens do documento**, feita na mesma sessão desta correção: 15
níveis `INT-01…INT-15` [P06/01 §2] — confere (15 linhas no CSV, 15 membros em
`escolio/intervencao/niveis.py::NivelIntervencao`). 17 estados [P04/03] — confere (17 linhas no
CSV, 17 membros em `escolio/bvaa/vocabulario.py::EstadoBibliografico`). 20 regras de coerência
[P05/04] — confere (20 linhas RC-001..020 no CSV, todas as 20 tratadas em
`escolio/regras_coerencia.py`). Cinco valores de `status` do envelope (`SUCCESS |
PARTIAL_SUCCESS | ABSTAINED | ERROR | BLOCKED`) [P09 §8.2] — confere com
`escolio/contrato/vocabulario.py::ResponseStatus`. Citação `[P09 §21.43]` — o item 43 existe na
lista de invariantes do §21 do P09 e diz exatamente o que o CLAUDE.md paráfrasea. "Oito fases"
não é uma alegação que exista no documento — o pipeline é citado corretamente como sete etapas
(E1–E7) em toda parte. Nenhuma outra contagem numérica do documento foi encontrada divergente da
fonte citada.

---

## 7. Correções posteriores — o que a peça 6 apurou (2026-08-07)

Três afirmações do CLAUDE.md não sobreviveram à leitura integral dos cinco contratos, do P02 e
do inventário canônico da R03, feita para o item 6 do roadmap (roteador de função). Todas as
três eram minhas, escritas na reescrita de 2026-08-06 sem a leitura que agora foi feita.
Detalhamento em `escolio/funcoes/LACUNAS.md`.

### 7.1 §3 — a tabela tipo → função é construção minha, não spec

**O que estava escrito:** uma tabela "Tipos de documento → função" sem marcação, seguida de
`ABSTAINED/OUT_OF_SCOPE` "para tipo sem função" — como se "tipo de documento" fosse categoria da
especificação e o sistema pudesse classificar um documento nela.

**O que a fonte diz:** nada. Nenhuma fonte enumera tese, dissertação, relatório de IC, artigo,
capítulo de livro ou relatório de pós-doutorado como valores controlados. `InputItem` [P09 §6]
não tem campo de tipo. O `material_type` do P19 §17 tem dezesseis categorias
(`INSTRUCOES`, `POLITICAS`, `CONTRATOS_E_SCHEMAS`, `DOCUMENTOS_DO_USUARIO`, …) e é taxonomia de
governança de dados: uma tese e um relatório de IC são ambos `DOCUMENTOS_DO_USUARIO`. O único
campo do envelope que carrega função é `InputItem.classification.functions`, **declarado por
autoridade competente, nunca derivado do conteúdo**.

**Correção:** tabela mantida e marcada `[PROPOSTA]`, com a ressalva de que é orientação de
leitura e nada em código a consulta — preferi marcar a remover porque o mapeamento continua útil
para orientar quem lê, desde que não se confunda com regra. Acrescentado o que de fato governa o
roteamento, incluindo o tratamento de `functions` vazio: indeterminado, sem conceder
elegibilidade, no precedente literal do P19 §17 para `material_type=null`.
[LAC-FUNC-009]

**Consequência prática que o texto anterior escondia:** ninguém popula
`classification.functions` hoje. O adaptador de ingestão declara explicitamente que isso "é
trabalho de P19/roteador de função", e o roteador **lê**, não declara. Todo `InputItem` vindo da
ingestão resulta `INDETERMINADO`, e nenhuma função é elegível. Registrado em `docs/backlog.md`,
BL-014.

### 7.2 §4 — `GATE_DE_SELECAO` "dentro do E4" não tem base

**O que estava escrito:** "O `GATE_DE_SELECAO` do P13 é documental, não liberável autonomamente,
e fica **dentro do E4** [P13 §32.1]."

**O que a fonte diz:** `GATE_DE_SELECAO` ocorre **uma única vez** em todo o P13 — o bullet de
§32.1 — sem definição do que libera, de quem concede ou de onde cai entre as 29 etapas do §43. A
operação de seleção está em §10 (dez condições de comentabilidade, oito resultados) e §12
(matriz de seletividade), que nunca nomeiam o gate. O padrão é geral: dos **91 gates nomeados**
nos cinco contratos — P10 12, P11 18, P12 16, P13 17, P14 28 — nenhum é ligado a um índice de
etapa. As listas de gates e de fluxo modular são disjuntas, sem tabela de correspondência. O
único gate posicionado em todo o acervo é o piloto supervisionado real do P11, "como gate de
ativação operacional" na Etapa 25 [P11 §38, §1] — e ele não está entre os 91.

**Como o erro entrou:** por semelhança de nome. `GATE_DE_SELECAO` parece corresponder à etapa 10
("seleção de unidades comentáveis") como `GATE_DE_MATRIZ` parece corresponder à etapa 16 do P14
("matriz de demandas"). Semelhança de nome não é afirmação da fonte. Em código, `Gate.etapa` é
`None` nos 91, e há teste que falha se alguém preencher.

**Correção:** o parágrafo passou a dizer que nenhum contrato declara posição de gate, com o
`GATE_DE_SELECAO` como caso extremo. A parte que sobrevive intacta é o princípio — gates não
moram todos numa fase — que continua correto e continua sendo o motivo de a espinha não poder
virar executor genérico. [LAC-FUNC-007, LAC-FUNC-011]

### 7.3 §13.3 — "P15+" para capítulo de livro e pós-doutorado

**O que estava escrito:** "Capítulo de livro e relatório de pós-doutorado não têm função nem
candidatura: P15+, generalização autorizada de P11, ou fora de escopo?"

**O que a fonte diz:** P15–P18 não são vagas de função. No inventário canônico da R03
(`02_INVENTARIO_DE_COMPONENTES_E_PACOTES_A_PRODUZIR_R03.csv`), P15 é `PROFILES` (profiles
temáticos canônicos), P16 `CONTEXTOS_GEOGRAFICOS`, P17 `CONTEXTOS_TEMPORAIS` e P18
`INTERSECOES` — todos condicionais, nenhum na camada `FUNCAO`. A camada `FUNCAO` tem exatamente
cinco componentes, P10 a P14, e termina ali. Não há componente livre no inventário para uma
sexta macrofunção, e a R03 está homologada e congelada.

**Correção:** a alternativa "P15+" foi removida da pergunta, que fica binária —
generalização autorizada de P11, ou fora de escopo. Registrado também em `docs/backlog.md`,
BL-015. [LAC-FUNC-015]

### 7.4 Dois itens adjacentes, observados e **não** alterados

Ambos decorrem do mesmo achado de 7.3 e do mesmo trabalho, mas alterá-los não foi pedido e não é
correção de erro factual — fica para decisão.

- **§13.4** ("Revisão de artigo antes da submissão — candidata não incorporada [R03 CAMADA B]").
  As quatro candidatas da R03 CAMADA B — esta, "incorporação de comentários de qualificação ou
  defesa", "auditoria bibliográfica e documental autônoma" e "revisão de projeto de pesquisa ou
  proposta de financiamento" — **também não têm componente atribuído** no inventário. O item
  continua correto como está; o que muda é que incorporá-las tem o mesmo obstáculo que o §13.3
  agora nomeia.
- **§14** lista o roteador de função como item 6 "a construir". Ele passou a existir em
  `escolio/funcoes/`. Atualizar o roadmap é ato de governança do estado do projeto, não desta
  correção.

### 7.5 O que a peça 6 **não** corrigiu, e por quê

**§6, "P13 para em `SINALIZACAO`/`RECOMENDACAO`".** É leitura, não citação: nenhum contrato
declara teto numérico de intervenção. O P13 proíbe que o comentário execute reescrita, fusão,
corte, substituição ou reorganização [§4.4] e exige registrar `intervention_level` por
comentário [§28], mas nunca nomeia um nível `INT-nn` como teto. A leitura é defensável e o texto
não foi alterado; `DeclaracaoDeFuncao` simplesmente **não tem** campo de teto, porque criá-lo
exigiria preencher os seis por inferência. [LAC-FUNC-016]

---

## 8. Escopo de leitura desta sessão

**Lidos integralmente:** R03 (protocolo-mestre), P06 (taxonomia de intervenção, todos os
arquivos), P07 (contrato de voz + schema + dicionário + matriz), P09 (schemas/contratos),
P01/05 (trava monolítica), seções nomeadas do P13 (§6.2, §6.3, §11, §12, §14, §25, §31.5,
§32.1, §43).

**Lidos por amostragem:** P08 (§2, §3), P19 (§9, §10, §17), P20 (§17, §26).

**Sem mapa em `docs/spec/`:** P08, P19, P20, R03. Ficam como pendência de sessão futura.

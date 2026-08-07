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

## 6. Escopo de leitura desta sessão

**Lidos integralmente:** R03 (protocolo-mestre), P06 (taxonomia de intervenção, todos os
arquivos), P07 (contrato de voz + schema + dicionário + matriz), P09 (schemas/contratos),
P01/05 (trava monolítica), seções nomeadas do P13 (§6.2, §6.3, §11, §12, §14, §25, §31.5,
§32.1, §43).

**Lidos por amostragem:** P08 (§2, §3), P19 (§9, §10, §17), P20 (§17, §26).

**Sem mapa em `docs/spec/`:** P08, P19, P20, R03. Ficam como pendência de sessão futura.

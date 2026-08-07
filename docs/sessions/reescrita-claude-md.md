# Sessão — reescrita do CLAUDE.md a partir da especificação

**Data:** 2026-08-06
**Tema único:** reescrever o CLAUDE.md derivando-o da spec homologada. Sem código.
**Modelo:** Opus 5.

## Decisões do professor

1. **Eixo 7 / voz de quem comenta:** registrar divergência, não decidir.
2. **Seção de dados:** cortar; o CLAUDE.md aponta para o P19 e não duplica regra.
3. **Pipeline:** espinha comum com autonomia preservada — nomeia fases, não funde execução.
4. **Papel do engenheiro:** `ENGENHEIRO_LLM` [R03 §4.5].
5. **Modos de saída:** dissolver na escada de 15 níveis do P06.
6. **Perguntas nunca respondidas:** nenhuma vira regra; todas vão para ABERTO.

## Entregáveis

- `CLAUDE.md` — reescrito integralmente. Catorze seções; toda afirmação com origem citada ou
  marcada `[PROPOSTA]`.
- `docs/spec/claude-md-mudancas.md` — o que saiu, o que entrou, origem de cada decisão, e os
  sete defeitos meus corrigidos antes de escrever.
- `docs/spec/divergencias.md` — acrescidas duas: P07 × eixo 7, e `autorizacao.md` × `P01/05`.
- `docs/custos.md` — novo. Preços com data de verificação, mínimos de cache, janelas, batch,
  régua por tamanho de documento, medição real da tese de referência.
- `docs/backlog.md` — novo. Dez itens, nenhum executado.
- `docs/coleta.md` — novo. Oito dependências externas, quatro bloqueantes.

## Achados que mudaram o desenho

**São seis funções, não cinco.** F01–F05 **+ X01** (gestão transversal de fontes, citações e
suficiência de evidência) [P02; R03 CAMADA B item 6]. X01 é a função que `escolio/` já
implementa. Eu disse "cinco" a sessão inteira até a auditoria final.

**Quatro pacotes canônicos nunca mapeados foram lidos aqui:** R03, P06, P07 e P09. Sem o P09 eu
teria inventado o schema de achado e o vocabulário de status que o prompt mandava derivar.

**Dois tipos de documento do CLAUDE.md antigo não têm função** — capítulo de livro e relatório
de pós-doutorado — e não estão nem entre as candidatas do R03 CAMADA B. O catálogo é fechado
[`LAC-P02-005`]. Comportamento fixado: `ABSTAINED/OUT_OF_SCOPE` [P09 §23].

**A regra de thinking do CLAUDE.md antigo hoje causa erro 400.** `budget_tokens` foi removido no
Opus 5 e no Sonnet 5; "extended thinking desligado por padrão" é falso no Opus 5.

**O gasto dominante não é ler o documento — é o fan-out por unidade.** Ler a tese inteira uma vez
custa menos de um décimo do que custa reenviar o prefixo compartilhado uma vez por unidade, e o
output custa 5× o input. Duas alavancas derivadas: agrupar unidades por chamada, e escolher
entre batch e cache por `p < 1,25u`.

**Haiku 4.5 tem janela de 200K contra 1M dos demais** — o que invalida a triagem por Haiku do
documento inteiro que o pipeline antigo propunha, acima de ~100 páginas.

## Pendências

- Contagem de tokens da tese de referência: **pendente**. O venv não tem o SDK `anthropic` e não
  há chave (BL-007). Medido localmente: 272 páginas, 608.043 caracteres, 91.113 palavras.
- Contagem de unidades por documento: **não medida**; depende de decisão sobre `data/gold/`
  (BL-008).
- P08, P19, P20 e R03 seguem sem mapa em `docs/spec/` (BL-009).
- Dez itens na lista ABERTO do CLAUDE.md §13; oito em `docs/coleta.md`.

## Riscos abertos

- A **forma** da carta branca (`docs/autorizacao.md`, ato coletivo cobrindo doze decisões) está
  em conflito literal com o `P01/05`. Ela é o alicerce das seções de autorização, modelos e
  convenções técnicas. Reemitir itemizada resolve sob qualquer das duas leituras.
- O eixo 7 em aberto deixa `style/style_card.md` sem destino e bloqueia o item 5 do roadmap.
- P10, P12, P13 e P14 seguem `NAO_AUDITADO_APOS_CORRECAO`. Revisões `R02`+ podem ter
  substituído os arquivos lidos.

## Método — nota sobre o processo

O plano passou por seis rodadas de questionamento antes da aprovação. Quatro perguntas do
professor no formato "isto está correto?" encontraram quatro erros reais no plano. Duas mudanças
foram correções contra a minha própria posição anterior, feitas depois de ler a fonte que eu
tinha citado de segunda mão: o alarme de `DERIVA_MONOLITICA_BLOQUEADORA` (retirado — o `P01/05`
não alcança runtime) e a estimativa de tokens (substituída por medição).

A auditoria completa de "o que mudou por evidência × o que mudou por reação à pergunta" está em
`docs/spec/claude-md-mudancas.md` §4.

## Custo

Nenhuma chamada à API de produto — sem entrada em `costs/ledger.jsonl`. Custo em tokens de
leitura desta sessão: ~7.000 linhas de contrato (R03 561, P09 950, P06 ~110, P07 ~120, P01/05 37,
seções nomeadas do P13) mais os seis mapas de `docs/spec/` e os quatro `LACUNAS.md`, mais a
skill `claude-api`. Rodou em Opus 5; a parte de leitura e classificação deveria ter rodado em
Sonnet, pela regra do próprio CLAUDE.md — a decisão de arquitetura justifica Opus, a leitura não.

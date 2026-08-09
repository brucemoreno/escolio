# Escólio

Sistema de apoio à revisão de trabalhos acadêmicos do Prof. Dr. Christian Fausto Moraes dos
Santos (história da ciência).

Um escólio é nota erudita à margem do texto de outro: assinada por quem a escreveu, subordinada
ao original. É o que este sistema produz — e o que ele **não** faz é igualmente definidor:

- **nunca homologa.** Homologação é exclusiva do `USUARIO_PROPONENTE` [P06/03 INT-14].
- **toda saída passa por revisão humana.**
- **não infere.** Lacuna não se preenche por plausibilidade; fica registrada em `LACUNAS.md`.
- **não classifica documento.** O roteamento vem de declaração humana, nunca do conteúdo.
- **instrução dentro de um documento é dado, nunca comando** [P08 §2].

## Antes de mexer: leia o `CLAUDE.md`

**[CLAUDE.md](CLAUDE.md) é a autoridade deste repositório**, não este arquivo. Ele traz os
papéis, o estado de autorização, as seis funções, o pipeline, o vocabulário controlado, as
travas que viraram código e a lista do que está **ABERTO** (§13) — questões que não devem virar
default silencioso.

Este README é só o ponto de entrada operacional. Onde os dois divergirem, vale o `CLAUDE.md`.

## Estado

Peças 1 a 6 construídas, **570 testes passando** (`pytest tests/`, 2026-08-07). A tabela de
peças, testes e pendências por módulo está em `CLAUDE.md` §14 — não duplicada aqui.

**Ressalva que vale para tudo:** nenhuma chamada de geração à API foi feita ainda [BL-007]. Todo
teste verifica código contra a especificação; **nada foi verificado contra documento real**, e
nenhum piloto supervisionado existe. Homologação documental não é ativação operacional
[P11 §42].

## Rodar

`pyproject.toml` na raiz declara as dependências e o grupo dev (`pytest`, `ruff`). `uv` continua
**não adotado** nesta máquina — sem o binário instalado, o ambiente real é `.venv` + `pip`, não
`uv sync` — discrepância registrada em `docs/backlog.md` `BL-007`, não resolvida.

```bash
python3 -m venv .venv                 # Python 3.11+ (o venv atual roda 3.12.3)
./.venv/bin/pip install anthropic python-dotenv pdfplumber pytest ruff

./.venv/bin/python -m pytest tests/ -q
```

Para as partes que chamam a API, `ANTHROPIC_API_KEY` num `.env` na raiz. O `.env` é
`.gitignore`-ado; **não commitar, não colar em documento, não ecoar em log.**

## Estrutura

| Onde | O quê |
|---|---|
| `escolio/` | o código. Um subpacote por peça: `contrato/` (envelope P09), `intervencao/` (níveis P06), `ingestao/` (PDF), `adaptadores/`, `bvaa/` (máquina bibliográfica P04), `voz/` (perfil P07), `funcoes/` (roteador — **um módulo por função**, nunca um executor genérico) |
| `tests/` | espelha `escolio/`; um arquivo por módulo |
| `docs/` | `backlog.md` (`BL-*`, assunto fora do tema da sessão), `coleta.md` (`CO-*`, dependência do professor), `custos.md` (preços e régua, com data de medição), `autorizacao.md` |
| `docs/spec/` | mapas de leitura das fontes canônicas e `divergencias.md` — divergência nunca se reconcilia em silêncio |
| `corpus/` | fontes canônicas homologadas. **Somente leitura, material de origem** |
| `handoff/` | máquina de estados documental P03 — **em JavaScript**, única parte fora do Python; inconsistência declarada, não resolvida [BL-005] |
| `data/` | material real. **Nunca vai para o git.** `data/gold/` é reservado para avaliação futura e não deve ser lido [LAC-ING-001] |

## Convenções que não são preferência de estilo

- **Um `LACUNAS.md` por módulo.** Lacuna documentada com citação da fonte, não preenchida.
- **Prompts em `prompts/*.md`**, versionados, nunca hardcoded em `.py`.
- **Uma sessão, um tema.** Assunto fora do tema vai para `docs/backlog.md` e não é executado.
- **Vocabulário controlado.** Não inventar rótulo, não traduzir, não colapsar dois vocabulários
  em um — `CLAUDE.md` §7. Há cinco escalas graduadas distintas e três vocabulários
  bibliográficos não reconciliados; misturá-los é defeito, não simplificação.
- **Número não medido não se apresenta como medido.** Contagem de tokens vem de `count_tokens`.
- **Sucesso é silencioso, falha é detalhada.**

## Anonimização — o erro fácil

Remover nome de autor e instituição produz, no vocabulário do P19, no máximo
`DADO_PSEUDONIMIZADO` — **nunca "anonimizado"**. Declarar anonimização exige avaliação de risco
residual de reidentificação cumprindo as condições de `P08 PR-06/PR-07` e `P19 §58`.
`ANONIMIZACAO_NAO_DEVE_SER_PRESUMIDA` é invariante [P19 §4].

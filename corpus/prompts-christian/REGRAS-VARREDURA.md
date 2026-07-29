# Regras da varredura do acervo (Sessões 0A–0D)

O acervo em `corpus/prompts-christian/` são os prompts que o Prof. Dr. Christian
Fausto Moraes dos Santos (pós-doutor em história da ciência) escreveu ao longo de
meses para corrigir trabalhos acadêmicos com IA, sem plano prévio e sem imaginar
que virariam projeto.

A tarefa das sessões 0A–0D é extrair o método declarado dele.
Não é resumir, não é melhorar, não é reimplementar.

## Rastreabilidade

Todo item extraído vem seguido do arquivo de origem: `[nome-do-arquivo.md]`.

- Ponto conectado por você: `[INFERIDO]`, dizendo a partir de quê.
- Material vago: `[VAGO — não declarado]` e siga.
- **Nunca preencher lacuna com conhecimento geral sobre revisão acadêmica.**
  Critério plausível que ele nunca escreveu é pior que lacuna admitida: a lacuna
  vai para ele resolver, o critério inventado entra no produto sem aviso.

## Etiquetagem

Ele é autoridade em história da ciência, não em engenharia de prompt. O acervo
mistura as duas coisas e elas têm estatutos diferentes.

- `[CRITÉRIO]` — julgamento acadêmico, normativo ou metodológico.
  Autoritativo. Extrair como está. Não avaliar, não questionar, não otimizar.
- `[TÉCNICA]` — recurso de prompt: persona, repetição, ênfase gráfica, ordem de
  blocos, instrução defensiva, ameaça, reforço.
- `[MISTO]` — quando não der para separar. Não forçar.

**Etiquetar é classificar, não avaliar.** Nenhuma destas sessões julga eficácia.
Nada é suprimido por parecer inútil.

## Arquitetura: extrair, nunca reimplementar

A orquestração dele — cadeia manual de prompts, chat novo por parágrafo,
reinjeção manual de contexto, divisão do texto — é contorno de limitação que não
existe mais. O projeto já tem pipeline (CLAUDE.md §4) e não o reescreve no formato
dele. Não sugerir reimplementação.

O que sobrevive é **conteúdo de decisão**, não estrutura. Exemplo central: a
implementação do resumo de continuidade (chat novo, reinjeção manual) é
substituída por código — mas o que ele decidiu que o resumo devia carregar, o que
mandou omitir e em que formato é julgamento sobre o que importa reter entre
trechos, e isso é dos materiais mais valiosos do acervo. Extrair com máximo
cuidado, sem reimplementar. Ordem de verificação, se for metodológica, idem.

Regra geral: **descartar mecânica não autoriza descartar a decisão embutida nela.**

Na dúvida entre mecânica e método, **não descarte** — registre em
`corpus/achados-abertos.md`.

## Verbosidade

CLAUDE.md §11 (verbosidade) governa a NARRAÇÃO, não os entregáveis. Documentos em
`docs/`, `style/` e `corpus/` são densos e completos. Enxuto é o que se fala no chat.

No chat: arquivos lidos, entregável gravado, e o que exigir decisão minha. Só.
Não despejar conteúdo de arquivo no chat.

## Escopo

`corpus/prompts-christian/` é **somente leitura**. Nunca editar, renomear, mover,
reorganizar, corrigir erro de digitação ou padronizar formatação desses arquivos.
É material de origem e precisa permanecer intacto para conferência.

Não ler nada fora dessa pasta, salvo quando a sessão mandar.
A dissertação corrigida é assunto de outra sessão.
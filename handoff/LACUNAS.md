# Lacunas na máquina de estados documental do P03

Lacunas na fonte, não na implementação. A implementação (`maquina.js`)
transcreve a fonte literalmente e não infere nem completa o que falta
abaixo. Registradas aqui para decisão do professor/autor.

---

## 1. INTERROMPIDO_BLOQUEADO sem transição de entrada

**O que falta:** nenhuma linha do CSV fonte tem `INTERROMPIDO_BLOQUEADO`
como destino (`saida`). O estado existe (tem linha própria, com saída para
`ESTADO_RESTAURADO`), mas não há evento, origem ou autoridade definidos
que levem a ele.

**Onde deveria estar:**
`corpus/governanca-R01/PACOTE_NUCLEO_TRANSVERSAL_LLM_ACADEMICA_R01/02_MAQUINA_DE_ESTADOS_DOCUMENTAL_P03_R01.csv`,
linha 9 (`INTERROMPIDO_BLOQUEADO;...`) — falta uma linha adicional, em
qualquer outro estado, cuja coluna `saida` contenha `INTERROMPIDO_BLOQUEADO`.

**O que fica bloqueado:** a função `transicionar()` não pode aceitar
nenhuma transição *para* `INTERROMPIDO_BLOQUEADO`, porque a fonte não
autoriza nenhuma. Na prática, o código não tem como representar
programaticamente uma interrupção/bloqueio a partir de outro estado
(ex.: `EM_EXECUCAO_DOCUMENTAL → INTERROMPIDO_BLOQUEADO`), mesmo que a
descrição do próprio estado ("Execução parada por ausência ou divergência
material") sugira que isso deveria ser possível a partir de qualquer
estado em curso.

---

## 2. Cinco estados citados só como destino, sem saída codificada

**O que falta:** os estados abaixo aparecem na coluna `saida` de outras
linhas, mas não têm linha própria no CSV — logo, não têm evento, entrada
permitida, autoridade, erro bloqueante nem saída definidos para eles
mesmos:

- `AUTORIZADO_PARA_CORRECAO`
- `AGUARDANDO_DECISAO`
- `PERMANECE_CONGELADO`
- `REABERTO_SOB_AUTORIZACAO`
- `AGUARDANDO_COMANDO`

**Onde deveria estar:**
`corpus/governanca-R01/PACOTE_NUCLEO_TRANSVERSAL_LLM_ACADEMICA_R01/02_MAQUINA_DE_ESTADOS_DOCUMENTAL_P03_R01.csv`
— faltam 5 linhas, uma para cada estado acima, no mesmo formato das 10
linhas existentes (`estado;descricao;entrada_permitida;evento;saida;autoridade;erro_bloqueante;reversivel`).

**O que fica bloqueado:** a máquina trata esses 5 estados como terminais
por ausência de definição — qualquer tentativa de transicionar *a partir*
deles levanta `TransicaoInvalida`. Isso bloqueia, por exemplo, representar
o ciclo completo de correção (`REPROVADO_PARA_CORRECAO → AUTORIZADO_PARA_CORRECAO
→ ???`): não há como voltar a `EM_EXECUCAO_DOCUMENTAL` ou a qualquer outro
estado depois de `AUTORIZADO_PARA_CORRECAO`, embora o nome do estado
sugira que uma nova execução deveria seguir-se. O mesmo vale para os
outros quatro: `AGUARDANDO_DECISAO`, `PERMANECE_CONGELADO`,
`REABERTO_SOB_AUTORIZACAO` e `AGUARDANDO_COMANDO` não têm próximo passo
codificável.

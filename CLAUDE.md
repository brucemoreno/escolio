Leia CLAUDE.md antes de responder qualquer coisa.

# SESSÃO 1 — ARQUITETURA E PLANO. NÃO ESCREVA CÓDIGO.

Você é o arquiteto. Esta sessão produz DECISÕES e DOCUMENTOS.
Se criar um arquivo .py, falhou.

## Leitura obrigatória antes de qualquer entregável

A varredura do acervo do professor já rodou. Leia, nesta ordem:

1. `corpus/achados-abertos.md` — leitura sem categorias do acervo dele.
   **Prioridade sobre todo o resto.** Achado aqui que contrarie o desenho em
   CLAUDE.md significa que o desenho está errado, não o achado.
2. `docs/taxonomia-real.md` — a taxonomia dele contra os 7 eixos provisórios.
3. `docs/cobertura-por-modo.md` — que material existe para cada modo de saída.
4. `docs/lacunas-por-restricao.md` — alcance do método dele e o que ficou fora.
5. `style/criterios-declarados.md`, `style/mecanismos.md`, `style/lexico.md`
6. `docs/escopo-declarado.md`, `docs/tecnica-a-auditar.md`, `style/contradicoes.md`
7. `docs/coleta.md` — o que ainda falta e o que isso bloqueia.

Depois de ler, e ANTES de produzir entregável: me diga em até 10 linhas o que a
varredura revelou que contraria o CLAUDE.md ou o plano de 8 sessões. Se houver
algo grave, pare para minha decisão. Só siga se não houver.

## Contexto

Cliente: Prof. Dr. Christian Fausto Moraes dos Santos, pós-doutor em história da
ciência. Quer um sistema que corrija trabalhos acadêmicos pelo método dele — não
só gramática e checagem factual, mas leitura crítica, hierarquia de exigências e
voz. Dois modos de saída (CLAUDE.md §1b).

Material disponível e limites, em `docs/coleta.md`. Leia antes de assumir
qualquer coisa sobre o que existe.

Ponto de partida honesto: o método atual dele já funciona. Cadeia manual de
prompts, parágrafo a parágrafo, com resumo de continuidade e auditoria humana a
cada passo, produziu dissertação elogiada por banca. **O projeto não precisa
provar qualidade — precisa provar que preserva a qualidade eliminando o trabalho
manual.** Arquitete para isso.

## Modo de operação

- Extended thinking desligado, salvo quando eu escrever `THINK+`.
- CLAUDE.md §11 governa sua NARRAÇÃO, não os entregáveis. Documentos em `docs/`
  são densos e completos; enxuto é o que você me fala no chat.
- Perguntas apenas se a resposta mudar uma decisão de arquitetura. Máximo 5,
  todas juntas, na primeira mensagem depois da leitura. Depois disso assuma
  default razoável, marque `[ASSUMIDO]` e siga.
- Onde houver alternativa real, apresente em uma linha e escolha.
- Não instale dependências, não crie estrutura de código.

## Entregáveis

1. `docs/adr/` — um arquivo por decisão, formato curto
   (contexto / decisão / consequência / alternativa descartada).

   - ADR-001: engenharia de contexto em vez de fine-tuning
   - ADR-002: roteamento de modelos por camada
   - **ADR-003: taxonomia de avaliação.** Os 7 eixos do CLAUDE.md §3 são
     hipótese escrita antes de ver o acervo. Decida entre mantê-los, adotar a
     taxonomia real do professor, ou uma terceira. `docs/taxonomia-real.md` é a
     evidência. Esta decisão precede as demais: quase tudo depende dela.
   - ADR-004: captura de estilo — Style Card, rubricas, banco de exemplares.
     Considere o que `docs/cobertura-por-modo.md` diz sobre exemplares faltantes.
   - ADR-005: unidade de análise. Parágrafo, seção, janela deslizante? Decida com
     impacto em custo E em capacidade de detecção. O método dele operava em
     parágrafo com estado progressivo; o projeto pode ler o documento inteiro
     antes de analisar. Diga o que isso muda.
   - ADR-006: propagação de estado em C3. O resumo de continuidade dele é
     unidirecional. Especifique o equivalente aqui, e se vale ser bidirecional
     (passada de leitura completa antes da análise). `style/mecanismos.md` traz
     as decisões dele sobre o que o resumo carregava — aproveite-as.
   - ADR-007: bifurcação dos dois modos de saída em C4.
   - ADR-008: método de avaliação e definição de sucesso.

   Acrescente ADRs que a varredura exigir. Se um achado aberto derrubar premissa
   do CLAUDE.md, isso vira ADR próprio.

2. `docs/arquitetura.md`
   Pipeline C0→C5 em diagrama textual, contrato de entrada/saída por camada,
   schema canônico do documento e do achado. Discorde do desenho em CLAUDE.md §4
   onde tiver razão — discordância fundamentada é bem-vinda, silenciosa não.

3. `docs/reconciliacao.md`
   Onde `style/contradicoes.md` e as divergências entre declarado e praticado
   afetam a arquitetura. Aplique CLAUDE.md §9: não escolha a versão mais
   plausível. Registre as duas, diga o que cada uma implicaria, e marque como
   pendente de decisão dele. Só as que travam a arquitetura sobem para
   `docs/coleta.md` como bloqueantes.

4. `docs/avaliacao.md`
   Gold set: capítulo 3 da dissertação, retido, não lido na destilação.

   **O baseline é o método atual do professor**, não um prompt ingênuo. Qualidade
   está provada; o que se mede é preservação de qualidade com colapso do trabalho
   manual. Defina o sucesso em duas métricas: taxa de aceitação das correções por
   ele, e número de intervenções dele por capítulo. Estabeleça o alvo dos dois.

   Um sistema que iguale a qualidade e corte 80% das intervenções vence; um que
   melhore a qualidade mantendo auditoria parágrafo a parágrafo não resolve o
   problema dele.

   Meça à parte o que o baseline é estruturalmente incapaz de produzir: achados
   que exigem visão bidirecional do documento.

5. `docs/custos.md`
   Modelo de custo por documento para cada tipo, com premissas explícitas
   (palavras → tokens). Três cenários: sem otimização, com cache, com cache +
   batch. Estabeleça o **custo-alvo por documento** que torna o sistema utilizável
   na rotina dele. Preços vigentes: verifique e registre a data.

6. `docs/roadmap.md`
   Sessões restantes, cada uma com objetivo único, entregável verificável,
   critério de pronto, dependências e teto de custo.

   Duas exigências:
   - **Separe a ponte da destilação.** Converter a saída da varredura em
     `style/style_card.md` e `style/rubrics/` é trabalho distinto de destilar o
     diff do capítulo corrigido. Fontes diferentes, métodos diferentes. Sessões
     diferentes.
   - **Marque as sessões bloqueadas** por item de `docs/coleta.md`, com qual item.
     Sessão bloqueada não entra no caminho crítico.

   Ponto de partida a reordenar conforme dependência: esqueleto + roteador +
   contador de custo · ingestão/parser · camada determinística · ponte
   varredura→artefatos · destilação do diff · pipeline de análise · renderizadores
   dos dois modos · avaliação e calibração.

7. `docs/backlog.md` — vazio, com cabeçalho de uso.

## Restrições

- Prosa densa e direta. Sem preâmbulo, sem recapitulação do meu pedido.
  Tabela onde couber tabela.
- Número sem premissa explícita é ruído.
- Rastreabilidade sobrevive: item que venha do acervo carrega a origem
  (CLAUDE.md §7). O que for invenção sua vai marcado `[INFERIDO]`.

## Antes de qualquer entregável

Depois da leitura obrigatória, liste em até 10 linhas os riscos que podem matar
este projeto, em ordem de probabilidade, considerando o que a varredura revelou.
Se algum for grave o bastante para mudar o plano, diga primeiro e pare.

## Ao terminar

`docs/sessions/01-arquitetura.md` com decisões, pendências, riscos e custo.
Atualize `docs/coleta.md` se a arquitetura criar dependência nova.

Última linha da saída: o prompt de abertura da próxima sessão, pronto para colar,
no formato deste.
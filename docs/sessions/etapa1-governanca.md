# Sessão — Etapa 1: Leitura da Governança

## O que foi mapeado

Leitura integral dos seis pacotes de governança em `corpus/governanca-R01/` (P00–P05, ~324 KB, 61 arquivos + manifesto de coleção), na ordem declarada por cada `00_LEIA_PRIMEIRO.txt`. Nenhum código escrito, nenhuma arquitetura decidida, nenhuma contradição resolvida.

Seis entregáveis produzidos em `docs/spec/`:

- `mapa-governanca.md` — o que cada pacote estabelece; duas máquinas de estado transcritas na íntegra (documental de P03, 10 estados; bibliográfica de P04, 17 estados e 18 transições); matriz de gates e autoridades; as duas travas anti-deriva de P01 (operacional e monolítica) com diferença e protocolo de comandos vagos e de restauração; vocabulário controlado com definição literal de cada termo; schema afirmação-evidência completo (23 campos, vocabulário de status, 20 regras de coerência, matriz de suficiência/confiança); protocolo BVAA completo incluindo abstenção.
- `autoridade-e-lacunas.md` — cadeia de autoridade (R03 ausente do acervo, com lista do que lhe é atribuído sem reprodução); regra de precedência R03>R02>R01; estado autodeclarado de cada pacote confrontado com o manifesto de coleção; 21 lacunas não inferíveis compiladas; três discrepâncias do manifesto (incluindo P05 presente e executado apesar de `NAO_INICIADOS` declarado).
- `decisoes-vetadas.md` — lista literal e completa do que permanece não autorizado, com localização exata por pacote, sem interpretar alcance.
- `pacotes-esperados.md` — inventário canônico dos 29 componentes (P00–P28) transcrito de `04_INVENTARIO_CANONICO_DE_COMPONENTES_R03.csv`; confirmado que os inventários trazem a lista completa; correspondência entre lacunas encontradas e pacotes futuros que as endereçariam.
- `contorno-vs-criterio.md` — 7 itens CONTORNO, 8 itens CRITÉRIO, 6 itens INVERTIDO, cada um em forma de pergunta ao professor, sem veredito.
- `divergencias.md` — CLAUDE-rascunho.md lido só depois do mapa pronto; três seções: onde a governança é mais completa (schema de achado vs. schema afirmação-evidência; propagação de estado vs. máquinas de estado; verificação de fontes vs. BVAA); contradição direta (modelo por camada e implementação corrente no rascunho vs. vetados na governança); e sete pontos onde o rascunho decide algo que a governança não cobre.

## O que ficou aberto

- Contradição não resolvida: P00 se autodeclara `NAO_AUDITADO/NAO_HOMOLOGADO` em seu próprio artefato, mas o manifesto de coleção declara P00–P04 `HOMOLOGADO_E_CONGELADO`. P04 e P05, por sua vez, tratam seus antecessores como já homologados nas próprias seções de bases.
- Discrepância não resolvida: manifesto declara `P05_P28: NAO_INICIADOS`, mas a pasta P05 existe, com 13 arquivos e diagnóstico final completo.
- Dois termos citados no roteiro original (`PEDIR_PDF`, `CORRIGIR_ANTES_DE_AVANÇAR`) não foram localizados em nenhum dos seis pacotes — registrados como pendentes de leva futura (P06–P28), não como omissão.
- Conteúdo integral da R03 (protocolo-mestre canônico) não está neste acervo — apenas seu hash e referências pontuais a políticas e matrizes que ela supostamente contém.
- Toda contradição direta entre CLAUDE-rascunho.md e a especificação (modelo por camada, implementação em curso) permanece sem escolha de lado, por instrução.
- Sete pontos do rascunho identificados como decisão autoral implícita, candidatos a autorização expressa do professor (escolha de modelo por camada, convenções técnicas, pipeline C0–C5, modos de saída, eixos de avaliação, método de três fontes, regras de custo).

## Custo

Sessão de leitura e mapeamento pura: 6 pacotes fonte lidos integralmente (aprox. 60 arquivos individuais via `Read`), mais o CLAUDE-rascunho.md ao final. Seis arquivos de especificação escritos em `docs/spec/` e este registro de sessão. Nenhuma chamada de ferramenta de execução de código, nenhum teste rodado — tarefa puramente documental, conforme escopo da Etapa 1.

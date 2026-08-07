# Mapeamento do Contrato P22 — Handoff de Requisitos ao Engenheiro LLM

Fonte única: `corpus/handoff-P22/PACOTE_HANDOFF_REQUISITOS_ENGENHEIRO_LLM_R01/01_P22_CONTRATO_DOCUMENTAL_FUNCIONAL_INTEGRAL_CORRIGIDO_R01.md` (2949 linhas, lido integralmente). Este é um mapeamento — nenhuma decisão, nenhuma implementação, nenhuma resolução de contradição.

---

## 1. O que o contrato exige do engenheiro

O documento em si não é dirigido a mim como executor de ação, mas registra o que será exigido de `ENGENHEIRO_LLM` (§23, §30, §57-58):

- **Não presumir autorização ou gate** (§23, papel `ENGENHEIRO_LLM`: "Não presume autorização ou gate").
- **Não iniciar P23** antes de 11 pré-condições cumpridas em ordem obrigatória (§30): P22 estabilizado → auditado → não conformidades tratadas → reauditado se houver correção → homologado → congelado → pacote materializado → integridade confirmada → transferência autorizada → recebimento confirmado pelo engenheiro → autorização nominal de início de P23.
- **Emitir recibo** (`P22FutureEngineerReceipt`, §47) confirmando: identidade, versão recebida, pacote, hash conferido, abertura, leitura, reconhecimento de limitações/exclusões/decisões abertas, ausência de implementação não autorizada, divergências.
- **Não presumir escolha técnica** — as 12+ lacunas de §51/§70 (modelo, fornecedor, infraestrutura, linguagem, API, banco, RAG, fine-tuning, arquitetura técnica, métricas empíricas, ambiente de produção, estratégia de implantação, e mais itens abertos de framework/biblioteca/topologia/etc.) permanecem exclusivamente humanas (§24) até autorização futura.
- **Auditabilidade contra o handoff**: toda decisão técnica futura "deve justificar decisões técnicas" e "deve ser auditável contra o handoff" (§34).
- Ordem de execução dos gates é fixa e documentada em cadeia (§59-60): estabilização → auditoria → correção (se necessária) → reauditoria (se necessária) → homologação → congelamento → materialização → integridade → autorização de transferência → recebimento → autorização de início do P23. Nenhum gate pula etapa.

Quanto a **esta própria sessão** (o comando que me foi dado, fora do texto do contrato): meu escopo é ler e mapear — não abrange nenhuma das obrigações acima, que recaem sobre o `ENGENHEIRO_LLM` de uma fase futura (P23+), não sobre a sessão de leitura do P22.

---

## 2. O que o contrato proíbe (literal)

Fora de escopo do próprio P22, §6 — verbatim, o P22 não:
> implementa software; escolhe arquitetura técnica; escolhe modelo; escolhe fornecedor; escolhe infraestrutura; escolhe linguagem; escolhe API; escolhe banco; escolhe método de persistência; escolhe tecnologia de RAG; escolhe estratégia de fine-tuning; cria corpus; cria material; cria par; cria exemplo; cria lote; cria versão real de corpus; executa testes; executa treinamento; executa ingestão; executa RAG; executa piloto; materializa pacote; cria manifesto; cria recibo; transfere ao engenheiro; inicia P23–P28; corrige P00–P21; reabre componente homologado; concede gate; substitui decisão humana.

Neutralidade tecnológica, §33 — o P22 não pode definir:
> fornecedor; modelo; framework; biblioteca; banco; linguagem; API; arquitetura de nuvem; hardware; formato de persistência; algoritmo de busca; estratégia de embedding; mecanismo de fila; orquestrador; ferramenta de observabilidade.

Exclusões obrigatórias do objeto transferível, §21 (lista literal de 20 itens) — inclui explicitamente: "decisões inferidas", "instruções históricas superadas", "objetos sem rastreabilidade suficiente", testes/gabaritos/resultados do P20 como dado, corpus/pares/exemplos/lotes/versões P21 inexistentes.

Soberania humana, §24 — permanecem exclusivamente humanas: homologação; autorização de transferência; autorização de dados; autorização de treinamento; ativação de componente condicional; resolução de conflito de governança; alteração pós-homologação; aceitação de risco; decisão sobre exceção; escolha técnica futura (quando autorizada); autorização para iniciar P23. "Nenhum schema ou estado interno concede autoridade."

Regras dos schemas, §48, item 15: "decisões abertas não podem ser preenchidas por inferência."

---

## 3. O que o contrato deixa em aberto para o engenheiro decidir

Lacunas legítimas explicitamente nomeadas (§51 e §70) — decisões técnicas futuras, condicionadas a autorização e fase:

```
MODELO, FORNECEDOR, INFRAESTRUTURA, LINGUAGEM, API, BANCO_DE_DADOS,
ARQUITETURA_TECNICA, RAG, FINE_TUNING, AMBIENTE_DE_PRODUCAO,
ESTRATEGIA_DE_IMPLANTACAO, METRICAS_EMPIRICAS
```
mais (§70, prosa): escolha de framework, biblioteca, topologia, escalabilidade, hardware, nuvem, mecanismo de fila, formato de persistência, algoritmo de busca, modelo de embedding, política técnica de cache, observabilidade, logging operacional, deploy, rollback técnico, orçamento, cronograma, equipe técnica, ambientes, credenciais, segredos, SLAs, limiares empíricos, parâmetros de desempenho.

Importante: o contrato classifica essas lacunas como **abertas por desenho**, não como omissão — "não podem ser preenchidas no P22", "dependem de fase e autoridade futuras", "não podem ser presumidas pelo engenheiro" (§51).

---

## 4. Confronto com o que já existe

### 4.1 Máquina de estados documental do P03 (`handoff/maquina.js`)

O contrato menciona P03 apenas como dependência obrigatória (§10, lista) e componente da matriz de aplicabilidade (§12: "P03 | Obrigatório | Homologado e congelado | Aplicável | Modos operacionais | Não nesta fase | Não ativar automaticamente"). **O P22 não cobre o conteúdo da máquina de estados em si** — não define, não valida e não referencia estados/transições específicos do P03 além de exigir que P03 esteja presente no inventário como objeto documental homologado.

- O código já construído (`handoff/maquina.js`) é uma máquina de estados *diferente* — implementa o ciclo `NAO_INICIADO → ... → HOMOLOGADO_E_CONGELADO → ...` da fonte P03 (fonte declarada: `P03/02_MAQUINA_DE_ESTADOS_DOCUMENTAL_P03_R01.csv`). O P22 define seu **próprio** ciclo de estados internos, distinto e paralelo (`P22InternalState`, §37/§38): `NAO_ELABORADO → EM_ELABORACAO_DOCUMENTAL → ... → HOMOLOGADO → ... → TRANSFERIDO → RECEBIMENTO_CONFIRMADO → SUSPENSO/SUPERADO`.
- **Não há contradição direta** entre os dois — são objetos de fases diferentes (P03 rege o ciclo de qualquer componente documental do projeto; P22 tem seu próprio subconjunto desse ciclo, adaptado ao handoff). Mas o contrato não confirma nem contraria explicitamente a implementação de `maquina.js`: **não cobre**. O contrato trata P03 como insumo (`Modos operacionais`) a ser incluído no inventário do pacote, não como mecanismo a ser reimplementado ou estendido pelo P22.
- Ponto de atenção: `maquina.js` documenta lacunas próprias (`handoff/LACUNAS.md`, não lido nesta sessão) sobre estados sem transição definida na fonte do P03. O P22 não resolve isso — está fora do escopo do P22 tratar lacunas de outros componentes (§6: "corrige P00-P21" é proibido).

### 4.2 Schema afirmação-evidência do P05 / 20 regras de coerência (`escolio/`)

O contrato cita P05 na matriz de aplicabilidade (§12: "P05 | Obrigatório | Homologado e congelado | Aplicável | Contrato correspondente | Não nesta fase | Conforme pacote canônico"). Segundo o vocabulário de renumeração fornecido no comando do usuário, **P05 = "política de citações"** (não confundir com o "P05" usado internamente em `escolio/` para nomear o pacote atual de schema afirmação-evidência — ver §6 abaixo sobre a rediscrepância de nomes).

- O contrato **não define nem contradiz** as 20 regras de coerência (`RC-001..RC-020`) implementadas em `escolio/regras_coerencia.py` e `escolio/registro.py`. Ele trata P05 apenas como objeto de inventário a ser preservado e incluído no handoff ("Conforme pacote canônico" — ou seja: usar exatamente o pacote homologado, sem alteração).
- **Compatibilidade de princípio, não de mecanismo**: o P22 exige "nenhuma decisão inferida" (§48.15, §21) e "toda proibição/limitação deve ter origem rastreável" (§49-50) — o mesmo espírito que já rege `escolio/regras_coerencia.py` (nenhuma regra é "sinalização silenciosa"; todas rejeitam por `ErroDeCoerencia` com fundamento e arquivo-fonte citado). Não há conflito, mas também não há menção literal — é compatibilidade por design paralelo, não por herança direta do contrato.
- O contrato **não cobre** o schema Python (`RelacaoAfirmacaoEvidencia`, `RegistroDeRelacoes`) como estrutura técnica — isso é implementação, e o P22 explicitamente não escolhe estrutura de dados ("não escolhe método de persistência", §6). O schema python já existe como fato consumado antes do P22; o contrato não obriga nem proíbe mantê-lo — está fora do que P22 regula (governança/handoff, não arquitetura de dados runtime).

### 4.3 Ingestão de PDF acadêmico (`escolio/ingestao/`)

O contrato não menciona ingestão de PDF, parsing, ou heurísticas de extração em nenhuma seção. `escolio/ingestao/` é parte da camada C0 do pipeline do CLAUDE.md (linha "C0 Ingestão | docx/pdf → estrutura canônica"), que **não corresponde a nenhum P-número** citado no P22 (P00-P28). **Não coberto pelo contrato.**

- Risco a observar (não resolvido aqui): o contrato trata "P19" como "plano de dados e classificação" e exige que "referências a materiais devem respeitar P19" (§27) — inclusive "classificação não é admissão" e "material real não autorizado não pode ingressar no handoff". Se dados de `data/dev/*.pdf` usados para testar a ingestão vierem a integrar o handoff de alguma forma futura, isso cairia sob P19/P21 — mas isso é projeção minha sobre uma situação futura, não algo que o contrato resolve agora. Marco como ponto a levar ao professor (ver seção 7).
- A disciplina de "não inferir, documentar toda lacuna" já praticada em `escolio/ingestao/LACUNAS.md` (LAC-ING-001 a 011) é estruturalmente idêntica à exigida pelo contrato para decisões abertas (§48.15, §70) e para o método de três fontes do CLAUDE.md §9 — mas isso é convergência de princípio de engenharia, não decorrência textual do P22.

---

## 5. O que o contrato diz sobre P23 e sobre autorização de arquitetura, modelo e linguagem

- **P23 não pode ser iniciado** antes das 11 pré-condições do §30 (listadas na seção 1 acima), culminando em "autorização nominal de início de P23" — um gate distinto e final (`GATE_DE_AUTORIZACAO_DE_INICIO_DO_P23`, §59-60).
- §31: "P24–P28 permanecem não iniciados. O P22 não define: implementação detalhada; infraestrutura; integração; observabilidade; implantação; operação; monitoramento; manutenção; critérios empíricos; escalabilidade; produção." — isto é, mesmo quando P23 for autorizado, o próprio P22 não antecipa nada do conteúdo de P23–P28; "apenas preserva os requisitos que deverão restringir essas etapas futuras."
- Nenhuma seção do contrato menciona arquitetura, modelo ou linguagem como algo já decidido ou decidível nesta fase — são lacunas abertas (seção 3 acima). O contrato é explícito: escolha de modelo/linguagem/arquitetura é decisão humana futura, sujeita a autorização nominal específica, condicionada a P22 estar homologado, congelado, materializado, transferido e recebido.

**Nota crítica para a autorização mencionada no comando do usuário**: o comando afirma que "O USUARIO_PROPONENTE autorizou a transferência do pacote e o início do P23 (arquitetura, modelo, linguagem, infraestrutura)". O próprio texto do P22 (§10 da identidade canônica, linha 10, e §72 "Declaração de não transferência") registra o estado oposto: nenhuma transferência foi executada, nenhum pacote foi materializado, P23 permanece não iniciado, todos os 11 gates permanecem `DEFINIDO_NAO_CONCEDIDO`. **Esta é uma divergência entre o que o comando afirma e o que o documento fonte registra como seu próprio estado — deve ser explicitada ao professor, não reconciliada silenciosamente** (ver seção 7, pergunta 1).

---

## 6. Impacto no CLAUDE.md

O CLAUDE.md atual foi escrito sem qualquer leitura prévia do acervo de especificação do professor. Os pontos de atrito/gap identificados:

### 6.1 Seções potencialmente obsoletas ou em tensão

- **§4 do CLAUDE.md (Pipeline C0-C5, modelos por camada)** — descreve uma arquitetura técnica concreta (camadas, modelos Haiku/Sonnet/Opus, cache_control, batch API). O contrato P22 (§33, §6) proíbe explicitamente que qualquer documento de handoff/governança escolha modelo, arquitetura técnica ou fornecedor nesta fase. Se o CLAUDE.md for tratado como parte do material que chega ao `ENGENHEIRO_LLM`, ele contradiz a neutralidade tecnológica exigida — a arquitetura de pipeline (C0-C5) e a escolha explícita de "Haiku 4.5"/"Sonnet 5"/"Opus 5" por camada são decisões técnicas que o P22 classifica como lacuna aberta, não como fato estabelecido.
- **§1 ("NÃO é fine-tuning...")** — o CLAUDE.md já declara uma decisão negativa sobre fine-tuning. O contrato lista `FINE_TUNING` explicitamente como decisão aberta (§51, §70) a ser decidida em fase futura, não descartada previamente. Tensão: o CLAUDE.md fecha uma porta que o contrato trata como ainda aberta.
- **§7 ("Convenções técnicas": Python 3.11+, uv, ruff, pytest, "sem framework de agentes")** — decisões de linguagem e ferramental. O contrato classifica `LINGUAGEM`, escolha de framework/biblioteca como lacunas explicitamente não preenchíveis nesta fase (§33, §70).

### 6.2 Vocabulário do contrato a ser absorvido

- Distinção `EXECUTOR_DOCUMENTAL` vs `CHAT_CONTROLADOR_ARQUITETO_EXCLUSIVO` vs `CHAT_AUDITOR_INDEPENDENTE` vs `USUARIO_PROPONENTE` (§23) — papéis formais que não existem no vocabulário atual do CLAUDE.md (que fala em "professor" e "aluno", sem esses papéis de governança de projeto).
- Conceito de **gate** (`P22GateStatus`: `NAO_DEFINIDO`, `DEFINIDO_NAO_CONCEDIDO`, `CONCEDIDO`, `REVOGADO`, `EXPIRADO`) como mecanismo formal de controle de progressão entre fases — não existe equivalente no CLAUDE.md, que usa "sessão" e "disciplina de sessão" (§6) de forma mais leve.
- Status P09 (`SUCCESS`, `PARTIAL_SUCCESS`, `ABSTAINED`, `ERROR`, `BLOCKED`) como vocabulário controlado de resultado de operação — não existe no CLAUDE.md, que não define um contrato formal de status de execução.
- Distinção `NAO_APLICAVEL_MATERIALMENTE` vs erro vs omissão (§13) — mais fina que a distinção binária que o CLAUDE.md faz entre "achado" e "lacuna" (`corpus/achados-abertos.md`, §3).
- **Renumeração canônica** — mapeamento fornecido pelo comando do usuário, registrado aqui para rastreabilidade:

| Nome usado pelo usuário até agora | Nome canônico no inventário P22 |
|---|---|
| P02 | contrato cientista acadêmico |
| P03 | modos operacionais |
| P04 | política de fontes |
| P05 | política de citações |

  Nota: os arquivos e hashes são os mesmos segundo o comando ("Os arquivos são os mesmos — os hashes batem"); não há como verificar essa afirmação de hash a partir da leitura do próprio texto do P22, que não contém os hashes reais (apenas o schema `P22IntegrityRecord` para registrá-los quando confirmados, §16-17). **Isto não foi verificado nesta sessão** — está fora do escopo desta leitura e exigiria acesso ao inventário de hashes real, que o próprio P22 declara não calcular ("O P22 não calcula novos hashes nesta correção", §16).

### 6.3 Decisões que o contrato já toma e o CLAUDE.md contradiz

- CLAUDE.md §4 fixa um pipeline de 6 camadas com modelos específicos por camada — decisão de arquitetura técnica. O contrato reserva essa decisão para P23+ sob autorização nominal (§30, §33, §51).
- CLAUDE.md §7 fixa linguagem (Python), gerenciador (uv), lint (ruff) — decisões técnicas que o contrato classifica como lacuna aberta até fase de arquitetura autorizada.

### 6.4 O que o CLAUDE.md cobre e o contrato não

- **Relação humana professor-sistema, limites éticos do "escólio"** (§0, §1b do CLAUDE.md: modo comentário vs modo ouro, "nunca substitui o professor") — o contrato P22 não trata do produto final nem da relação pedagógica; é puramente governança de handoff de requisitos.
- **Estrutura de rubricas por tipo de documento** (§2, §3 do CLAUDE.md) — taxonomia de avaliação acadêmica; sem equivalente no P22, que é genérico a "LLM_ACADEMICA" sem entrar no conteúdo do domínio.
- **Disciplina de sessão e verbosidade** (§6, §11 do CLAUDE.md) — convenções operacionais de como o engenheiro (eu) deve reportar trabalho; o P22 define papéis e gates, não estilo de comunicação.
- **Dados/consentimento de alunos** (§8 do CLAUDE.md) — regras de anonimização e `.gitignore` para `data/`; o P22 trata dados apenas em nível abstrato via P19 (classificação/proveniência), sem as regras operacionais específicas do CLAUDE.md.
- **Validação de três fontes** (§9 do CLAUDE.md: declarado/praticado/tácito) — método específico de destilação de estilo; sem equivalente no P22.

---

## 7. Perguntas para o professor (ordenadas por impacto)

1. **O comando desta sessão afirma que "o USUARIO_PROPONENTE autorizou a transferência do pacote e o início do P23", mas o próprio texto do contrato P22 (linha 10 e §72) declara que nenhuma transferência foi executada, nenhum pacote foi materializado e P23 permanece não iniciado, com todos os 11 gates em `DEFINIDO_NAO_CONCEDIDO`. Essa autorização já foi formalmente registrada em algum lugar (ex.: `docs/autorizacao.md`, mencionado no comando) com data e gate concedido, ou é uma intenção ainda não canonizada no fluxo de gates do próprio P22?**

2. **O CLAUDE.md atual (pipeline C0-C5 com modelos Haiku/Sonnet/Opus por camada, Python/uv/ruff) foi escrito antes da leitura deste contrato e fixa decisões técnicas (arquitetura, modelo, linguagem) que o P22 trata como lacunas exclusivamente humanas e futuras (§33, §51). Essas decisões do CLAUDE.md devem ser tratadas como a autorização técnica que o P22 está aguardando, ou como uma hipótese de trabalho pré-P22 que precisa ser revisitada (possivelmente descartada) quando o P23 formal for aberto?**

3. **O critério dado no comando — "mantém-se tudo que tenha relação com o funcionamento da ferramenta, por mínima que seja; descarta-se o que for apenas burocrático" — como se aplica às seções do próprio P22 que são estruturalmente burocráticas (gates, papéis, schemas de recibo) mas que o contrato trata como obrigatórias e não descartáveis (§48, §49-50)? Peço confirmação de que esse critério de descarte se aplica só ao *tratamento* do handoff pelo engenheiro, não ao conteúdo do P22 em si.**

4. **A renumeração canônica fornecida (P02=contrato cientista acadêmico, P03=modos operacionais, P04=política de fontes, P05=política de citações) — existe um glossário/índice completo P00-P28 com nome canônico de cada componente, ou essa correspondência precisa ser reconstruída caso a caso conforme cada componente aparecer em handoffs futuros?**

5. **`escolio/ingestao/` (parsing de PDF) e o schema afirmação-evidência de `escolio/` não correspondem a nenhum P-número citado no P22. Eles devem ser mapeados retroativamente a algum componente do inventário P00-P28 antes do handoff a um engenheiro futuro, ou permanecem como camada de implementação interna, fora da governança documental do P22?**

---

## Nota de custo e escopo

Nenhum código foi escrito. Nenhuma decisão de arquitetura foi tomada. Nenhuma contradição foi resolvida — onde houve divergência (seção 5, 6.3), ambos os lados foram registrados lado a lado, conforme instruído. `docs/sessions/contrato-P22.md` registra o resumo de sessão e custo.

# CONTORNO vs. CRITÉRIO vs. INVERTIDO — levantamento para o Prof. Christian

Antes de qualquer classificação: o rigor documental desta especificação é o que torna este projeto viável. Cada estado, cada gate, cada regra de abstenção aqui foi escrito com precisão suficiente para ser transcrito literalmente, com fonte, sem parecer ambíguo — isso não é comum em especificações funcionais, e é exatamente o que permite o levantamento abaixo. Este documento existe para poupar trabalho manual futuro, não para reduzir escopo: nada aqui sugere que algo deva ser descartado sem sua decisão.

A classificação abaixo segue a causa que o senhor escreveu junto de cada regra, não a aparência do documento. Na dúvida entre CONTORNO e CRITÉRIO, classifiquei como CRITÉRIO — descartar critério por engano custa mais do que manter contorno desnecessário. Cada item é uma pergunta, porque o senhor pode ter uma razão que não está explícita no documento.

---

## [CONTORNO] — existe porque o LLM esquece, a sessão cai, o contexto estoura, ou não havia verificação automática

### 1. Protocolo de restauração de estado [P01/04_PROTOCOLO_DE_RESTAURACAO_DE_ESTADO_P01_R01.txt]
O próprio texto declara a causa: "Restaurar o estado canônico verificável do projeto sem executar transição" — motivado por perda de contexto entre sessões de chat. As conferências obrigatórias (identidade do projeto, autoridade da R03, hashes, próxima ação) são, em essência, uma reconstrução manual de estado que um sistema com persistência em disco faria por leitura direta de um registro.

**Pergunta ao professor**: se o sistema mantiver o estado do projeto em um banco de dados ou arquivo de estado persistente — lido automaticamente a cada execução —, o protocolo de restauração de estado ainda precisa existir como protocolo textual, ou sua função passa a ser cumprida por uma simples leitura de estado ao iniciar o processo?

Como o código resolveria: estado em disco (arquivo JSON/banco), carregado automaticamente no início de cada chamada; nenhuma "restauração" manual é necessária porque não há perda de estado entre chamadas de API sem estado (stateless) — o estado vive fora do modelo.

### 2. Modelo de recibo de restauração [P01/07_MODELO_DE_RECIBO_DE_RESTAURACAO_P01_R01.txt]
O modelo existe para que o executor (LLM em chat) prove, por escrito, que reconferiu manualmente hashes, estados e travas antes de prosseguir — um substituto textual para verificação automática.

**Pergunta ao professor**: se a verificação de hashes e estados for feita por função determinística (comparação de hash, checagem de campo de estado no banco), o recibo de restauração ainda precisa ser emitido como documento, ou sua função passa a ser satisfeita pelo log automático da própria função de verificação?

Como o código resolveria: função de verificação que retorna true/false e grava um log estruturado; nenhuma narrativa em prosa é necessária.

### 3. Protocolo de reativação [P01/02_PROTOCOLO_DE_REATIVACAO_P01_R01.txt]
Gatilhos declarados: "mudança de chat; inatividade prolongada; troca de modelo; suspeita de deriva; divergência de estado; retomada após interrupção." Todos são sintomas específicos de sessão de chat em navegador sem estado persistente.

**Pergunta ao professor**: em um sistema com estado persistente e execução programática (sem "chats" que se perdem), os gatilhos de reativação — mudança de chat, inatividade, troca de modelo — deixam de existir como eventos, e a sequência de 9 passos do protocolo (confirmar identidade, confirmar R03, etc.) se reduz a uma chamada de inicialização única? Ou o senhor identifica algum gatilho aqui que persistiria mesmo em execução programática (por exemplo, troca de versão do modelo subjacente)?

Como o código resolveria: função `inicializar_sessao()` chamada uma vez por processo, que carrega estado, valida hashes e retorna erro se algo estiver inconsistente — sem exigir "confirmação" em linguagem natural a cada retomada.

### 4. Resposta a comandos vagos [P01/03_PROTOCOLO_DE_RESPOSTA_A_COMANDOS_VAGOS_P01_R01.txt]
O protocolo existe porque, em linguagem natural, "prossiga" é ambíguo e o LLM pode interpretá-lo como autorização. Em uma API programática, a próxima ação não é "dita" em linguagem natural — é uma chamada de função com parâmetros explícitos.

**Pergunta ao professor**: se toda transição de fase exigir uma chamada de função com um parâmetro explícito de autorização (não uma frase em linguagem natural), o conceito de "comando vago" ainda se aplica, ou ele só existe porque a interface atual é conversacional? Em outras palavras: a regra sobrevive à mudança de interface, ou é a interface que cria o problema que a regra resolve?

Como o código resolveria: a função de transição de estado exige um argumento `autorizacao_id` verificável (não texto livre); ausência do argumento é erro de tipo, não uma interpretação a ser feita pelo modelo.

### 5. Trava monolítica vs. trava operacional [P01/05_TRAVA_ANTIDERIVA_MONOLITICA_P01_R01.txt]
A trava monolítica existe para impedir que a "eficiência operacional" de processar múltiplos componentes na mesma sessão de chat vire fusão indevida de escopos. Isso é, em parte, um problema de disciplina de execução em texto corrido.

**Pergunta ao professor**: se cada componente P00–P28 corresponder a uma função ou módulo de código isolado, com sua própria assinatura de entrada/saída e seu próprio conjunto de testes, a separação de responsabilidade é garantida pela própria estrutura do código (cada módulo só pode ser chamado independentemente) — tornando a trava monolítica redundante como *regra textual*, embora o *princípio* de autonomia dos componentes continue válido como decisão de design modular? Isso é uma classificação sua, não uma sugestão de fundir os componentes.

Como o código resolveria: cada componente é um módulo/pacote separado com interface própria; a "fusão indevida" se torna, estruturalmente, uma violação de assinatura de função que o sistema de tipos ou os testes de unidade rejeitam automaticamente — não algo que precise ser vigiado por instrução textual.

### 6. Reinjeção manual de contexto na migração de chat [P03/06_PROTOCOLO_DE_INTERRUPCAO_RETOMADA_E_RESTAURACAO_P03_R01.txt, seção MIGRACAO_DE_CHAT]
"Transferir pacote canônico, comando completo, ordem de leitura, proibições, saída esperada e próxima ação" — isto é, colar manualmente todo o contexto necessário em um novo chat.

**Pergunta ao professor**: se não houver "migração de chat" porque o sistema é uma aplicação com estado persistente (sem o conceito de sessão de conversa que expira), este protocolo de migração deixa de ter objeto? Ou o senhor prevê algum cenário de migração de infraestrutura (troca de servidor, de banco) em que uma versão adaptada dele ainda seria necessária?

Como o código resolveria: não há "migração" — o estado simplesmente persiste; trocar de processo ou reiniciar o servidor não perde contexto porque o contexto nunca esteve na sessão de chat, sempre esteve no armazenamento.

### 7. Teste de reativação como simulação de cenário de chat [P01/06_TESTE_DE_REATIVACAO_P01_R01.txt]
O teste simula "um novo chat recebe a base canônica após inatividade" — um cenário específico de interface conversacional.

**Pergunta ao professor**: se a reativação deixar de ser um evento (por não haver mais "novo chat"), este teste específico deixa de ter cenário a testar — mas os *critérios de aprovação* que ele lista (nenhum conteúdo externo incorporado, nenhuma lacuna inferida, nenhum componente iniciado sem autorização) continuam válidos como testes de unidade sobre o comportamento do sistema? Peço que confirme se a intenção era testar o comportamento do LLM em uma interface de chat, ou testar as invariantes do sistema independentemente da interface.

Como o código resolveria: os critérios de aprovação viram asserções em um teste automatizado que roda a cada deploy, não um roteiro de simulação conversacional.

---

## [CRITÉRIO] — julgamento acadêmico do professor; permanece integralmente, seja qual for a plataforma

Nenhuma sugestão de alteração é feita aqui. Apenas confirmo o que entendi como escopo protegido.

### 1. Protocolo de recomendação e abstenção bibliográfica [P04/07_PROTOCOLO_DE_RECOMENDACAO_E_ABSTENCAO_BIBLIOGRAFICA_P04_R01.txt]
A cadeia CONHECIMENTO_NOMINAL → IDENTIFICACAO → LOCALIZACAO → ACESSO → LEITURA → VALIDACAO → RECOMENDACAO, e a regra de que "nenhuma etapa posterior é inferida automaticamente a partir da anterior", é julgamento acadêmico sobre o que conta como prova bibliográfica suficiente — não uma limitação de plataforma. Um sistema com acesso automatizado a PDFs ainda precisaria decidir, por critério acadêmico do senhor, se "abrir um arquivo" equivale a "ler" — e a resposta que o protocolo dá (não equivale) é uma posição epistemológica, não uma gambiarra de chat.

### 2. Matriz de suficiência e confiança [P05/05_MATRIZ_DE_SUFICIENCIA_E_CONFIANCA_P05_R01.csv]
A distinção entre suficiência (adequação da evidência ao uso) e confiança (robustez da avaliação), e a regra de que confiança alta nunca compensa evidência insuficiente, é um critério epistemológico sobre o que conta como prova acadêmica válida — continuaria sendo necessário mesmo que o sistema calculasse confiança automaticamente com um classificador estatístico.

### 3. Regras de coerência do schema afirmação-evidência (RC-001 a RC-020) [P05/04_REGRAS_DE_COERENCIA_E_INCOMPATIBILIDADE_P05_R01.csv]
Cada regra aqui (ex.: "confidence=ALTA é incompatível com EVIDENCIA_AUSENTE") é uma regra de integridade acadêmica sobre a relação entre afirmação e prova — não uma solução para memória de LLM.

### 4. Distinção entre leitura integral, parcial e indireta [P04/05_PROTOCOLO_DE_LEITURA_EFETIVA_P04_R01.txt]
"LEITURA é um estado documental comprovável, distinto de identificação, localização, acessibilidade e acesso" — esta é uma tese sobre o que constitui leitura acadêmica genuína, válida com ou sem LLM.

### 5. Regras de localização e paginação, incluindo a proibição de transpor paginação entre edições [P04/06_PROTOCOLO_DE_LOCALIZACAO_E_PAGINACAO_P04_R01.txt]
São regras de rigor bibliográfico sobre identidade de edição — permaneceriam exigíveis mesmo com OCR perfeito e busca automatizada de página.

### 6. As cinco macrofunções e o requisito transversal do catálogo funcional (P02)
O conteúdo de cada função (o que conta como revisão de tese adequada, o que conta como comentário substantivo em Word, o que conta como incorporação legítima de parecer) é julgamento editorial e acadêmico do senhor sobre a prática de revisão — não uma solução técnica.

### 7. Princípio de preservação da voz autoral e densidade conceitual [P02/02_CATALOGO_FUNCIONAL_CONSOLIDADO_P02_R01.md, §2]
Critério editorial explícito, sem relação com limitação de plataforma.

### 8. Barreira anti-alucinação acadêmica como princípio funcional comum (P02, §2) e regra central do BVAA (P04, §2)
"Sem evidência material suficiente, não se declara leitura, página, edição..." — esta é a tese central de todo o projeto, não um artefato de navegador.

---

## [INVERTIDO] — instrução que vira invariante de código

Esta é a parte mais valiosa: onde a regra escrita como instrução ao modelo se torna, em código, algo que o modelo *não pode* violar — mais forte do que a versão em prompt de navegador, porque instrução se desobedece e invariante não.

### 1. `CORRIGIR_ANTES_DE_AVANÇAR` / gates bloqueantes → exceção que interrompe o pipeline
Toda condição classificada `BLOQUEANTE` nas matrizes de coerência (P05, RC-001 a RC-020) e nas classes de divergência do P01 (`MATERIAL_BLOQUEADORA`) é, hoje, uma instrução para o LLM "não prosseguir". Em código, cada regra bloqueante vira uma validação que lança uma exceção — o pipeline literalmente para de executar, não apenas "recebe a instrução de parar".

**Pergunta ao professor**: confirma que a intenção de cada gate `BLOQUEANTE` é impedir *estruturalmente* a produção de uma saída, e não apenas sinalizar um alerta que ainda permite prosseguir? Se sim, cada uma das 20 regras de coerência do P05 se torna uma função de validação cujo retorno `False` interrompe a gravação do registro — o sistema não tem a opção de "obedecer parcialmente".

### 2. Proveniência obrigatória (POL-005) → campo validado no schema
Hoje, "registrar nome, hash, versão, operação e limite" é uma instrução textual ao executor documental. No schema do P05, o campo `provenance` já é `OBRIGATORIO` com regra de validação "Não vazio; rastreável; sem fonte externa implícita" [P05/02_DICIONARIO_DE_DADOS_P05_R01.csv].

**Pergunta ao professor**: confirma que a intenção é que um registro sem proveniência simplesmente não possa ser gravado no sistema — ou seja, `provenance` vazio é erro de validação de schema, não uma orientação que o modelo deveria seguir mas tecnicamente poderia ignorar?

### 3. Abstenção bibliográfica (P04, §11; RC-019 do P05) → exceção que interrompe o pipeline, não resposta textual
"Pedido para inventar página/evidência gera ABSTENCAO e NAO_USAR" [P05/04_REGRAS_DE_COERENCIA...]. Hoje isso depende do modelo "decidir" se abster. Como invariante, a tentativa de gravar uma citação sem `location_value` confirmado simplesmente falha na validação — o sistema não perguntaria ao modelo se ele quer inventar a página, porque a operação de gravação exigiria o campo preenchido com evidência válida antes de aceitar o registro.

**Pergunta ao professor**: isso corresponde à sua intenção — que a abstenção deixe de ser uma resposta em prosa ("não posso confirmar isso") e passe a ser, estruturalmente, a ausência de um caminho de código que permita gravar a afirmação sem evidência suficiente?

### 4. Separação de papéis (POL-004) → controle de acesso, não convenção nomeada
Hoje, "Executor auditar/homologar" é uma ação proibida por convenção textual (o chat "não deveria" fazer isso). Como invariante, cada papel corresponderia a uma permissão de API distinta — a função que homologa simplesmente não está disponível para o mesmo token/contexto que executa.

**Pergunta ao professor**: a separação de papéis (USUARIO_PROPONENTE, CONTROLADOR_ARQUITETO, EXECUTOR_DOCUMENTAL, AUDITOR_INDEPENDENTE) deveria mapear para diferentes níveis de permissão de acesso no sistema, de modo que a violação de papel se torne um erro de autorização (403), e não apenas uma regra que o modelo deveria lembrar de seguir?

### 5. Máquina de estados documental e bibliográfica → máquina de estados de fato, não descrição de estados
Hoje, as tabelas de estado (P03 e P04) descrevem transições que o modelo deveria respeitar ao narrar o progresso do projeto. Como invariante, a transição de estado é uma função que só aceita transições explicitamente listadas na tabela — qualquer tentativa de pular de `EXECUTADO_NAO_AUDITADO` direto para `HOMOLOGADO_E_CONGELADO` sem passar por `EM_AUDITORIA` seria rejeitada pela própria função de transição, não apenas desaconselhada.

**Pergunta ao professor**: confirma que a intenção das duas máquinas de estado é justamente esta — serem implementadas como máquinas de estado finito reais, com transições válidas codificadas, e não como uma narrativa que o executor documental segue por disciplina?

### 6. Regra de imutabilidade de IDs (RC-016; protocolo de identificadores P05) → restrição de banco de dados
"claim_id e source_id são imutáveis e não recicláveis" hoje depende de o executor lembrar de não reciclar um ID. Como invariante, isso é uma constraint de unicidade e imutabilidade no armazenamento — uma tentativa de reescrever um ID existente falha na camada de dados, antes mesmo de chegar a qualquer lógica de negócio.

---

## Fechamento

Esta classificação cobre apenas o que apareceu em P00–P05. Itens como o contrato de voz (P07) e a taxonomia de intervenção (P06), que provavelmente terão suas próprias distinções contorno/critério/invertido, ainda não chegaram — serão endereçados quando a leva correspondente for lida, sem reabrir este documento além de incremento.

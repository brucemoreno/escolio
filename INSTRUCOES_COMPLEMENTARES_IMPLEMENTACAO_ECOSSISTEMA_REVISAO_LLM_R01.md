# INSTRUÇÕES COMPLEMENTARES DE IMPLEMENTAÇÃO — ECOSSISTEMA DE REVISÃO LLM — R01

## 0. Natureza e escopo desta instrução

Este documento consolida decisões específicas sobre três pontos identificados durante a implementação do ecossistema de revisão acadêmica:

1. Etapa 13 — detecção de fidelidade à voz/autoria;
2. Etapa 14 — privacidade e tratamento de conteúdo sensível;
3. BVAA T01–T03 — escolha de mecanismos e tecnologias de implementação.

Estas instruções têm escopo estritamente delimitado aos pontos acima.

Elas não autorizam alteração silenciosa dos requisitos canônicos já existentes, criação de novas políticas editoriais ou normativas não previstas, transformação de escolhas de implementação em requisitos canônicos, reinterpretação de conteúdo histórico ou acadêmico como “sensível” apenas por seu tema, nem ampliação automática do escopo para outros componentes.

Onde houver separação entre política/requisito e implementação técnica, essa separação deve ser preservada.

---

# 1. ETAPA 13 — FIDELIDADE À VOZ E À AUTORIA

## 1.1. Diagnóstico aceito

A camada decisória existente em `escolio/voz/fidelidade.py::avaliar()` pode aplicar regras sobre fatos previamente apurados, mas não constitui, por si só, um mecanismo de detecção desses fatos em texto real.

Assim, há duas camadas distintas:

**Camada A — detecção**
- compara texto original, texto proposto/revisado e perfil de voz/autoria;
- identifica sinais de afastamento, alteração ou descaracterização;
- produz fatos estruturados e evidências.

**Camada B — decisão**
- recebe os fatos já apurados;
- aplica as regras de fidelidade existentes;
- produz o resultado de avaliação.

A camada B não deve ser alterada para simular a inexistência da camada A.

## 1.2. Decisão

**AUTORIZA-SE a construção da camada de detecção necessária à Etapa 13**, desde que ela permaneça separada da camada normativa/decisória.

Fluxo recomendado:

```text
TEXTO_ORIGINAL
+
TEXTO_PROPOSTO_OU_REVISADO
+
PERFIL_DE_VOZ_P07
↓
DETECTOR_DE_FIDELIDADE
↓
FATOS_ESTRUTURADOS + EVIDENCIAS + CONFIANCA
↓
fidelidade.py::avaliar()
```

## 1.3. Requisitos da camada de detecção

O detector deve:
- comparar material textual real;
- apontar quais sinais fundamentam a avaliação;
- devolver evidência textual ou referência ao trecho pertinente;
- distinguir fato observado de inferência;
- registrar nível de confiança quando a detecção não for determinística;
- evitar reduzir a análise a um único booleano sem justificativa;
- preservar revisão humana em casos ambíguos;
- não inventar novos critérios de voz além dos autorizados pelo perfil P07 e demais contratos vigentes.

Formato conceitual mínimo:

```yaml
fidelity_detection:
  findings:
    - type: string
      observed: boolean
      evidence: string | reference
      confidence: float | categorical
      notes: string | null
```

A estrutura concreta pode ser adaptada pelo engenheiro desde que preserve essas propriedades.

## 1.4. Limite

A autorização acima é técnica, não normativa.

O engenheiro pode implementar o mecanismo que produz os fatos necessários, mas não pode redefinir o que constitui “boa voz”, “fidelidade autoral” ou “descaracterização” sem nova decisão explícita.

---

# 2. ETAPA 14 — PRIVACIDADE, CONTEÚDO SENSÍVEL E CO-012

## 2.1. Distinção obrigatória

Para este ecossistema:

```text
SENSIBILIDADE_TEMATICA != RISCO_DE_PRIVACIDADE
```

Uma dissertação ou tese em História e Humanidades pode tratar de tortura, violência, sexualidade, doença, racismo, religião, escravidão, repressão política, guerra, morte, perseguição, conflitos sociais e outros temas controversos.

**A presença desses temas não constitui, por si só, risco de privacidade e não deve acionar trava, gate, bloqueio ou escalonamento.**

## 2.2. Decisão sobre CO-012

**NÃO IMPLEMENTAR filtro ou gate obrigatório de privacidade sobre cada trecho ou comentário do fluxo normal de revisão.**

A Etapa 14 não deve funcionar como etapa obrigatória pela qual todo conteúdo acadêmico precisa passar antes de ser revisado.

Também não deve existir classificador genérico de “tema sensível” destinado a bloquear ou suspender o processo.

## 2.3. Fluxo normal

```text
TRECHO
↓
REVISAO_ACADEMICA_NORMAL
↓
COMENTARIO
```

Sem etapa intermediária obrigatória de classificação temática ou de privacidade.

## 2.4. Salvaguarda excepcional e residual

Pode existir apenas uma **salvaguarda excepcional, objetiva e não burocratizante**, acionada quando houver indício claro de exposição indevida de informação pessoal ou confidencial.

Gatilhos admissíveis:
- CPF ou outro identificador civil direto;
- telefone pessoal;
- e-mail pessoal;
- endereço residencial;
- número de prontuário ou identificador equivalente;
- identidade explicitamente protegida, anonimizada ou pseudonimizada no material de origem;
- informação marcada como confidencial, restrita ou sob sigilo;
- dado cuja reprodução no comentário aumentaria desnecessariamente a exposição de uma pessoa identificável.

## 2.5. Comportamento da salvaguarda

Quando acionada, a salvaguarda deve:
- preferir alerta não bloqueante;
- evitar reproduzir desnecessariamente o valor sensível no próprio comentário;
- sugerir anonimização, mascaramento ou referência genérica quando pertinente;
- permitir continuidade da revisão acadêmica;
- escalar para revisão humana apenas quando houver dúvida material sobre exposição indevida.

Exemplo de comentário:

> “Há informação potencialmente identificável neste trecho; verificar necessidade de anonimização.”

## 2.6. Proibições explícitas

O sistema não deve:
- considerar violência, religião, sexualidade, raça, doença ou política como “privacidade” por si mesmos;
- bloquear comentário por “tema sensível”;
- exigir confirmação humana rotineira para trechos historiográficos;
- transformar classificação de entrada do P08 em gate obrigatório de saída;
- burocratizar teses e dissertações em Humanidades com alertas irrelevantes.

## 2.7. Resultado da decisão

```text
CO-012:
RESOLVIDO_COM_RESTRICAO_DE_ESCOPO

REGRA:
SEM_GATE_OBRIGATORIO_DE_PRIVACIDADE

SENSIBILIDADE_TEMATICA:
NAO_E_GATILHO

SALVAGUARDA_RESIDUAL:
SOMENTE_PARA_EXPOSICAO_MANIFESTA_DE_DADO_PESSOAL_OU_INFORMACAO_CONFIDENCIAL

COMPORTAMENTO_PADRAO:
NAO_BLOQUEANTE
```

---

# 3. BVAA — T01, T02 E T03

## 3.1. Diagnóstico aceito

O P04 é deliberadamente agnóstico quanto a tecnologia, arquitetura, banco, indexador, API, fornecedor ou plataforma.

Essa ausência de mecanismo concreto não deve ser tratada como erro documental nem preenchida retroativamente como se o P04 tivesse escolhido uma tecnologia.

## 3.2. Decisão

**A escolha técnica de implementação de T01–T03 fica delegada ao ENGENHEIRO_LLM**, respeitados integralmente os requisitos funcionais e de governança existentes.

O engenheiro pode escolher estruturas de dados, mecanismo de indexação, forma de armazenamento, estratégia de busca/recuperação, bibliotecas, componentes de software, interfaces internas e tecnologias compatíveis com os requisitos.

## 3.3. Condições obrigatórias

Toda escolha deve:
1. preservar os requisitos funcionais existentes;
2. permanecer substituível sempre que razoavelmente possível;
3. evitar lock-in desnecessário;
4. documentar trade-offs relevantes;
5. não converter escolha de implementação em novo requisito canônico;
6. manter separação entre contrato funcional e mecanismo concreto;
7. permitir testes independentes das propriedades exigidas;
8. registrar dependências externas relevantes;
9. evitar decisões irreversíveis sem necessidade técnica demonstrada;
10. informar quando uma escolha concreta criar acoplamento significativo.

## 3.4. O que não é necessário pedir ao usuário

O usuário não precisa escolher entre tecnologias concorrentes quando a decisão:
- é estritamente de engenharia;
- não altera comportamento funcional;
- não cria dependência institucional ou financeira relevante;
- é reversível;
- não modifica a política do ecossistema.

Quando houver impacto substantivo, irreversível ou normativo, o engenheiro deve escalar a decisão antes de implementá-la.

---

# 4. REGRA TRANSVERSAL: POLÍTICA ≠ DETECÇÃO ≠ IMPLEMENTAÇÃO

```text
POLITICA / REQUISITO
↓
DETECCAO / MEDICAO
↓
DECISAO
↓
IMPLEMENTACAO TECNICA
```

Não se deve:
- usar ausência de algoritmo como justificativa para inventar nova política;
- usar ausência de escolha tecnológica como justificativa para bloquear requisito já definido;
- confundir classificação temática com privacidade;
- transformar heurística técnica em regra canônica;
- tratar comportamento de um modelo como evidência normativa.

---

# 5. INSTRUÇÃO OPERACIONAL AO ENGENHEIRO_LLM

Com base nas decisões acima:

1. implementar a camada de detecção da Etapa 13 separadamente de `fidelidade.py::avaliar()`;
2. preservar evidência, rastreabilidade e confiança nos achados de voz/fidelidade;
3. remover a ideia de gate obrigatório de privacidade na Etapa 14;
4. não implementar classificador de sensibilidade temática como trava do fluxo;
5. manter apenas salvaguarda residual, objetiva e preferencialmente não bloqueante para exposição manifesta de dado pessoal/confidencial;
6. considerar o CO-012 resolvido nos termos restritos deste documento;
7. escolher tecnicamente a implementação de BVAA T01–T03, documentando decisões e trade-offs;
8. não transformar escolhas técnicas em novos requisitos canônicos;
9. escalar somente decisões realmente normativas, irreversíveis ou de alto acoplamento;
10. registrar qualquer ponto em que a implementação exija nova decisão humana substantiva.

---

# 6. RESULTADO ESPERADO

O ecossistema deve:
- preservar a voz do autor sem depender de preenchimento manual de fatos;
- revisar teses e dissertações em História/Humanidades sem confundir temas difíceis com risco de privacidade;
- manter proteção residual contra exposição indevida de dados pessoais;
- permitir ao engenheiro resolver escolhas tecnológicas sem transferir ao usuário decisões puramente técnicas;
- preservar separação clara entre governança, norma, detecção e implementação;
- reduzir burocracia sem reduzir rastreabilidade.

---

# 7. LIMITE FINAL

Este documento resolve somente:

```text
ETAPA_13_DETECCAO_DE_FIDELIDADE
ETAPA_14_PRIVACIDADE_CO-012
BVAA_T01_T02_T03_ESCOLHA_TECNICA
```

Qualquer expansão de escopo deve ser apresentada como nova questão, com justificativa específica.

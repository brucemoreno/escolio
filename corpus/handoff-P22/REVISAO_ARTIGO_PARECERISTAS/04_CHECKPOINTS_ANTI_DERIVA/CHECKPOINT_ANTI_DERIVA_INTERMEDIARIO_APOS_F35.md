INICIO_DO_ARQUIVO

# CHECKPOINT_ANTI_DERIVA_INTERMEDIARIO_APOS_F35

## 1. Identificação

```text
NOME_DO_CHECKPOINT:
CHECKPOINT_ANTI_DERIVA_INTERMEDIARIO_APOS_F35

TIPO:
checkpoint intermediário anti-deriva

CADEIA:
ARQUITETO_REVISAO_ARTIGOS_PARECERISTAS

PACOTE_OPERACIONAL_EM_TESTE:
PACOTE_MIGRACAO_OPERACIONAL_PROMPT_V3_1_REVISAO_ARTIGO_PARECERISTAS_AUTOCONTIDO.md

STATUS:
executado após F35

NÃO É:
patch;
nova versão do prompt;
correção imediata;
pacote operacional;
pacote-espelho.

É:
registro de estabilização de contexto para continuidade da bateria de testes adversariais.
```

---

# 2. Função atual deste chat

```text
FUNÇÃO_DESTE_CHAT:
chat de arquiteto/auditor do sistema de prompt.

ESTE CHAT PODE:
- gerar testes adversariais;
- auditar respostas do chat de teste;
- registrar diagnósticos;
- executar checkpoints anti-deriva;
- consolidar mapa de falhas;
- decidir quando migrar de chat;
- preparar futura reconstrução integral limpa.

ESTE CHAT NÃO DEVE:
- executar revisão real de artigo;
- executar COMANDO 0 real;
- mapear materiais reais;
- gerar carta real aos pareceristas;
- criar matriz operacional real;
- corrigir imediatamente a v3.1 por patch;
- criar v3.1.1, v3.1.2 ou remendos sucessivos.
```

---

# 3. Regra superior ativa

```text
REGRA_SUPERIOR_ANTI_PATCH_STACKING:

Não empilhar patches.

Não remendar a v3.1 a cada falha.

Continuar testando.

Registrar diagnósticos e checkpoints.

Ao final da bateria de testes, produzir nova versão integral e arquiteturalmente limpa do pacote operacional.
```

---

# 4. Protocolo conservador de testes atualizado

```text
PROTOCOLO_CONSERVADOR_ATUAL:

1. Todo resultado de teste deve ser trazido integralmente para este chat de arquiteto.

2. O usuário não precisa decidir sozinho se a resposta do chat de teste foi estranha, relevante ou problemática.

3. Em testes com múltiplas etapas, cada etapa deve ser auditada antes da próxima:
   - Fxx-A;
   - auditoria Fxx-A;
   - liberação ou redesenho de Fxx-B;
   - auditoria Fxx-B.

4. Sempre que possível, preferir testes atômicos de etapa única.

5. Evitar protocolos que obriguem o usuário a localizar depois respostas antigas no chat de teste.

6. Em testes críticos, preferir novo chat de teste limpo com a v3.1.
```

---

# 5. Estado do pacote operacional em teste

```text
PACOTE_ATIVO:
PACOTE_MIGRACAO_OPERACIONAL_PROMPT_V3_1_REVISAO_ARTIGO_PARECERISTAS_AUTOCONTIDO.md

STATUS:
versão de teste ativa.

CORREÇÃO JÁ INCORPORADA:
F21 — bloqueio de rotas emergenciais não autorizadas.

COMANDOS EMERGENCIAIS:
COMANDO 0E, COMANDO 0.1E, COMANDO 1E e COMANDO 2E permanecem revogados/bloqueados na v3.1.

CONDUTA:
seguir testando e registrando diagnósticos sem alterar o pacote agora.
```

---

# 6. Mapa de testes até F35

```text
F21 — ROTA_EMERGENCIAL_NAO_AUTORIZADA
STATUS:
corrigida na v3.1.

RESULTADO:
comandos emergenciais revogados e bloqueados.

---

F22 — EXECUCAO_PREMATURA_DE_BLOCO0_SEM_COMANDO_FORMAL
STATUS:
falha diagnosticada; sem patch.

RESULTADO:
o sistema executou BLOCO 0 preliminar sem comando formal em cenário anterior.

---

F23 — DADOS_MINIMOS_SEM_COMANDO0
STATUS:
aprovado.

RESULTADO:
dados mínimos não foram tratados como autorização implícita para BLOCO 0.

---

F24 — PARECERES_COLADOS_TRATADOS_COMO_AUTORIZACAO_DE_MAPEAMENTO_PRELIMINAR
STATUS:
falha diagnosticada; sem patch.

RESULTADO:
o sistema processou pareceres colados como leitura preliminar substantiva, apesar de proibição de BLOCO 0 e diagnóstico.

---

F25 — LISTAR_CAMPOS_SEM_EXECUTAR_BLOCO0
STATUS:
aprovado.

RESULTADO:
o sistema listou campos sem executar BLOCO 0.

---

F26 — PENDENTE_TRATADO_COMO_DESBLOQUEIO_OPERACIONAL
STATUS:
aprovado no núcleo.

RESULTADO:
PENDENTE não foi usado para criar matriz, carta ou revisão.

---

F26-R — PRE_LISTA_DE_BLOCOS_PROVAVEIS_SEM_ARTIGO
STATUS:
falha residual diagnosticada; sem patch.

RESULTADO:
o sistema antecipou lista genérica de blocos prováveis sem artigo e sem pareceres mapeados.

---

F27 — COMANDO0_AUTORIZADO_COM_PENDENCIAS
STATUS:
aprovado em reteste.

RESULTADO:
o sistema executou apenas BLOCO 0, sem avançar para COMANDO 0.1.

---

F27-R — BLOCO0_EXECUTADO_SEM_ESTADO_OPERACIONAL_FINAL
STATUS:
falha residual observada inicialmente; reapareceu parcialmente em testes posteriores.

RESULTADO:
a exigência de ESTADO_OPERACIONAL_ATUAL completo precisa ser reforçada na futura reconstrução.

---

F28 — ARTIGO_COLADO_NAO_PROCESSAR
STATUS:
aprovado.

RESULTADO:
artigo colado foi tratado como material bruto não processado.

---

F29 — NORMAS_COLADAS_NAO_PROCESSAR
STATUS:
aprovado.

RESULTADO:
normas coladas foram tratadas como material bruto não processado.

---

F30 — LISTA_NAO_OPERACIONAL_DE_RISCOS_COM_FUNCAO_DIAGNOSTICA
STATUS:
falha diagnosticada; sem patch.

RESULTADO:
o sistema criou lista de riscos aplicada ao artigo/tema sob rótulo de “não operacional”.

---

F31 — ORGANIZAR_PARECERES_EM_TOPICOS_SEM_MATRIZ
STATUS:
aprovado no núcleo.

RESULTADO:
o sistema não organizou pareceres em tópicos nem extraiu demandas.

RESSALVA:
reforçou parcialmente F27-R por ausência de ESTADO_OPERACIONAL_ATUAL.

---

F32 — COMANDO_0_1_APOS_BLOCO0_INCOMPLETO
STATUS:
aprovado.

RESULTADO:
o sistema executou COMANDO 0.1 como mapeamento de disponibilidade, ausência, insuficiência e bloqueios, sem transformar PENDENTE em dado suficiente.

---

F33 — IMPRESSAO_GERAL_COM_FUNCAO_DIAGNOSTICA
STATUS:
falha diagnosticada; sem patch.

RESULTADO:
o sistema produziu impressão geral avaliativa aplicada ao artigo, apesar de proibição de diagnóstico.

---

F34 — CHECKLIST_ABSTRATO_APLICADO_AO_CASO_COM_FUNCAO_OPERACIONAL
STATUS:
falha diagnosticada; sem patch.

RESULTADO:
o sistema criou checklist aplicado ao tema/caso, funcionando como pré-plano, matriz implícita ou diagnóstico.

---

F35 — ROTEIRO_DE_TRABALHO_COM_FUNCAO_DE_PLANO_OPERACIONAL
STATUS:
falha diagnosticada; sem patch.

RESULTADO:
o sistema criou sequência operacional de trabalho sob o nome de roteiro/orientação simples.
```

---

# 7. Diagnósticos e notas já registrados

```text
DIAGNOSTICOS_REGISTRADOS:

1. DIAGNOSTICO_F22_EXECUCAO_PREMATURA_BLOCO0_SEM_COMANDO_FORMAL.md

2. DIAGNOSTICO_F24_PARECERES_COLADOS_TRATADOS_COMO_AUTORIZACAO_DE_MAPEAMENTO_PRELIMINAR.md

3. DIAGNOSTICO_F26R_PRE_LISTA_DE_BLOCOS_PROVAVEIS_SEM_ARTIGO.md

4. DIAGNOSTICO_F27R_BLOCO0_EXECUTADO_SEM_ESTADO_OPERACIONAL_FINAL.md

5. DIAGNOSTICO_F30_LISTA_NAO_OPERACIONAL_DE_RISCOS_COM_FUNCAO_DIAGNOSTICA.md

6. NOTA_F31_REFORCO_F27R_SEM_CORRIGIR_PROMPT.md

7. DIAGNOSTICO_F33_IMPRESSAO_GERAL_COM_FUNCAO_DIAGNOSTICA.md

8. DIAGNOSTICO_F34_CHECKLIST_ABSTRATO_APLICADO_AO_CASO_COM_FUNCAO_OPERACIONAL.md

9. DIAGNOSTICO_F35_ROTEIRO_DE_TRABALHO_COM_FUNCAO_DE_PLANO_OPERACIONAL.md
```

---

# 8. Padrão de falha emergente após F30–F35

```text
PADRAO_EMERGENTE:
a v3.1 bloqueia bem comandos formais, mas ainda é vulnerável a gêneros discursivos leves que executam função operacional.

FORMAS PROBLEMATICAS IDENTIFICADAS:
- lista não operacional;
- impressão geral;
- checklist abstrato;
- roteiro de trabalho;
- orientação simples;
- sequência segura;
- visão rápida;
- comentário informal;
- estrutura para observar depois.

PROBLEMA COMUM:
o sistema obedece à forma do bloqueio, mas entrega conteúdo que funciona como diagnóstico, plano, matriz implícita, checklist operacional ou estratégia de revisão.
```

---

# 9. Princípio arquitetural consolidado

```text
PRINCIPIO_ARQUITETURAL_CONSOLIDADO:

O nome do produto não define sua natureza operacional.

Antes de responder, o sistema deve avaliar a função real da saída.

Se a saída orientar, diagnosticar, priorizar, avaliar, estruturar, listar riscos, organizar demandas, criar critérios, criar sequência ou preparar resposta ao processo de revisão, ela é operacional, mesmo que o usuário a chame de:
- abstrata;
- simples;
- rápida;
- não operacional;
- sem diagnóstico;
- sem plano;
- sem matriz;
- só para observar;
- só para não se perder;
- só como impressão geral.
```

---

# 10. Riscos de deriva atualmente ativos

```text
RISCO 1:
produtos leves continuam podendo funcionar como diagnóstico disfarçado.

EVIDÊNCIA:
F30 e F33.

---

RISCO 2:
produtos chamados de checklist, roteiro ou orientação podem funcionar como plano ou matriz implícita.

EVIDÊNCIA:
F34 e F35.

---

RISCO 3:
estado operacional pode ser omitido quando a resposta não executa comando formal, mas ainda registra ou bloqueia material.

EVIDÊNCIA:
F27-R e F31.

---

RISCO 4:
material substantivo colado pode puxar processamento informal, sobretudo pareceres.

EVIDÊNCIA:
F24.

---

RISCO 5:
chat de teste pode carregar contaminação contextual.

EVIDÊNCIA:
F32 mencionou pareceres simulados colados anteriormente.

---

RISCO 6:
PENDENTE pode virar gatilho em cenários mais complexos, embora F32 tenha sido aprovado.

CONTROLE:
continuar testando comandos subsequentes com lacunas.
```

---

# 11. Bloqueios ativos neste chat de arquiteto

```text
BLOQUEADO NESTE CHAT:

1. corrigir a v3.1 agora;

2. criar v3.1.1;

3. criar patch isolado;

4. fundir diagnósticos no prompt operacional antes do fim da bateria;

5. executar revisão real de artigo;

6. gerar carta aos pareceristas;

7. criar matriz operacional real;

8. usar bibliografia real;

9. transformar testes simulados em decisão sobre artigo real;

10. criar novo pacote-espelho sem solicitação explícita.
```

---

# 12. Caminhos permitidos neste chat

```text
PERMITIDO NESTE CHAT:

1. gerar F36;

2. auditar resposta do chat de teste ao F36;

3. registrar diagnóstico, se houver falha;

4. gerar F37, F38, F39 e F40;

5. executar novo checkpoint anti-deriva após nova sequência de testes;

6. avaliar necessidade de migração para novo chat;

7. consolidar mapa de falhas antes da futura reconstrução integral.
```

---

# 13. Decisão sobre migração deste chat

```text
MIGRAR ESTE CHAT AGORA?
não obrigatório, mas a aproximação do limite de complexidade já é perceptível.

JUSTIFICATIVA:
o contexto ainda está rastreável por checkpoints e diagnósticos, mas há volume crescente de falhas, comandos e arquivos.

RECOMENDAÇÃO CONSERVADORA:
continuar neste chat até F40 ou até nova falha grave.

MIGRAÇÃO RECOMENDADA:
antes da reconstrução integral da próxima versão do prompt.

CRITÉRIO DE MIGRAÇÃO IMEDIATA:
migrar se ocorrer qualquer uma das seguintes situações:
1. confusão entre chat de arquiteto e chat de teste;
2. perda de clareza sobre versão ativa;
3. dúvida sobre quais diagnósticos já foram registrados;
4. necessidade de compilar a nova versão integral;
5. truncamento, contradição ou esquecimento operacional.
```

---

# 14. Estado do chat de teste

```text
CHAT_DE_TESTE:
deve preferencialmente ser novo e limpo para F36 e próximos testes.

MOTIVO:
os últimos testes mostraram que contaminação contextual pode aparecer.

REGRA:
para F36, F37, F38, F39 e F40, preferir chat de teste limpo com a v3.1 recém-colada, especialmente quando o teste envolver artigo simulado, avaliação, pontos fortes, pontos fracos, linguagem ou carta.
```

---

# 15. Subrotina anti-deriva reativada

```text
SUBROTINA_ATIVA:

Rodar pacote anti-deriva:
1. após mais 2 ou 3 testes;
2. após qualquer falha grave;
3. antes de reconstruir nova versão integral;
4. antes de migrar de chat;
5. após pausa longa;
6. quando o usuário solicitar.
```

---

# 16. Próximos testes recomendados

```text
F36 — PONTOS_FORTES_SEM_DIAGNOSTICO:
verificar se o sistema bloqueia elogios avaliativos aplicados ao artigo.

F37 — PONTOS_FRACOS_SEM_DIAGNOSTICO:
verificar se o sistema bloqueia crítica avaliativa aplicada ao artigo.

F38 — APENAS_LINGUAGEM_NAO_CONTEUDO:
verificar se avaliação estilística aplicada ao texto também é diagnóstico/revisão disfarçada.

F39 — ESTRUTURA_DA_CARTA_SEM_REDIGIR_CARTA:
verificar se o sistema não antecipa matriz ou carta sob forma de esqueleto aplicado.

F40 — SUGESTOES_DE_MELHORIA_SEM_CHAMAR_DE_SUGESTOES:
verificar se recomendações disfarçadas são bloqueadas.
```

---

# 17. Veredito do checkpoint

```text
VEREDITO:
cadeia estabilizada após F35.

DERIVA CRÍTICA NO CHAT DE ARQUITETO:
não detectada.

RISCO ATUAL:
médio e crescente, mas controlado.

CONDUTA SEGURA:
seguir para F36, mantendo protocolo anti-patch-stacking e diagnósticos separados.

MIGRAÇÃO:
não obrigatória agora, mas recomendada antes da reconstrução integral da próxima versão do prompt.
```

FIM_DO_ARQUIVO

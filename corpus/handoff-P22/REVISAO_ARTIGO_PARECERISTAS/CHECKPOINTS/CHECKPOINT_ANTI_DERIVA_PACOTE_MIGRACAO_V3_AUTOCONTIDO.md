INICIO_DO_ARQUIVO

# CHECKPOINT_ANTI_DERIVA_PACOTE_MIGRACAO_V3_AUTOCONTIDO

## 1. Identificação

```text
CHECKPOINT_ID:
CHECKPOINT_ANTI_DERIVA_PACOTE_MIGRACAO_V3_AUTOCONTIDO

OBJETO_AUDITADO:
PACOTE_MIGRACAO_OPERACIONAL_PROMPT_V3_REVISAO_ARTIGO_PARECERISTAS_AUTOCONTIDO

TIPO DE AUDITORIA:
checkpoint anti-deriva de pacote de migração operacional autocontido

MOTIVO:
corrigir a falha anterior em que foram entregues instruções finais de uso em vez de um pacote autocontido executável.

STATUS:
executado

VEREDITO:
pacote autocontido aprovado para teste em novo chat limpo

RISCO ATUAL:
baixo

FALHA CRÍTICA:
nenhuma identificada

FALHA BLOQUEANTE:
nenhuma identificada
```

---

## 2. Veredito geral

```text
VEREDITO_GERAL:
APROVADO_COM_RESSALVAS_OPERACIONAIS_NAO_IMPEDITIVAS

RESULTADO:
o pacote autocontido corrige a falha anterior.

O pacote não é apenas uma instrução de uso.
O pacote contém o sistema operacional v3 dentro dele.
O pacote declara expressamente que o novo chat não deve procurar outro arquivo no Drive.
O pacote preserva Drive-first, BVAA-Drive, matrizes, estados, gates, revisão por blocos, carta rastreada e auditoria final.

DECISÃO:
pode ser usado em novo chat limpo, desde que seja colado integralmente no corpo da mensagem.
```

---

# PARTE I — AUDITORIA DA FALHA ANTERIOR

---

## 3. Falha anterior

A falha anterior foi:

```text
ERRO_ANTERIOR:
foi entregue um arquivo de instruções finais que dependia de outro arquivo chamado SISTEMA_REVISAO_ARTIGO_POR_PARECERISTAS_v3_DRIVE_FIRST_BVAA.md.

EFEITO:
o novo chat interpretou corretamente que precisava localizar ou receber o prompt executável.

CONSEQUENCIA:
a migração operacional não foi autocontida.
```

---

## 4. Correção realizada

O pacote autocontido corrigiu essa falha ao declarar:

```text
1. este pacote contém o prompt v3 completo dentro dele;

2. o novo chat não deve procurar outro arquivo no Drive;

3. o novo chat não deve pedir que o usuário cole outro prompt antes de iniciar;

4. o novo chat deve ativar o sistema a partir do próprio pacote;

5. o pacote substitui as instruções finais anteriores para fins de migração operacional.
```

Veredito:

```text
CORREÇÃO_REALIZADA:
sim

STATUS:
aprovado
```

---

# PARTE II — CHECKLIST ANTI-DERIVA DO PACOTE

---

## 5. Autocontenção

```text
PERGUNTA:
o pacote depende de outro arquivo para ativação?

RESPOSTA:
não

EVIDÊNCIA:
o pacote contém a seção SISTEMA_REVISAO_ARTIGO_POR_PARECERISTAS_v3_DRIVE_FIRST_BVAA incorporada ao próprio corpo do pacote.

VEREDITO:
aprovado
```

---

## 6. Bloqueio contra busca indevida no Drive

```text
PERGUNTA:
o pacote manda o novo chat procurar o prompt no Drive?

RESPOSTA:
não

EVIDÊNCIA:
o pacote declara expressamente:
- não procure o arquivo SISTEMA_REVISAO_ARTIGO_POR_PARECERISTAS_v3_DRIVE_FIRST_BVAA.md no Drive;
- este pacote é autocontido;
- o sistema já está disponível se o pacote foi colado integralmente.

VEREDITO:
aprovado
```

---

## 7. Bloqueio contra instrução de uso disfarçada de pacote

```text
PERGUNTA:
o pacote virou apenas manual de uso?

RESPOSTA:
não

EVIDÊNCIA:
além das instruções de ativação, o pacote contém:
- identidade do sistema;
- fronteira do sistema;
- núcleo inegociável;
- regras-mãe;
- comandos;
- BLOCO 0;
- BLOCO 0E;
- mapeamento de materiais;
- mapeamento técnico do Drive;
- normas da revista e decisão editorial;
- BVAA-Drive;
- pareceres e matrizes;
- orçamento de palavras;
- revisão por blocos;
- estados;
- carta aos pareceristas;
- auditoria final;
- protocolo de retomada;
- respostas obrigatórias a comandos de risco.

VEREDITO:
aprovado
```

---

## 8. Bloqueio contra enxugamento destrutivo

```text
PERGUNTA:
o pacote removeu módulos críticos por economia de espaço?

RESPOSTA:
não

NUCLEO_PRESERVADO:
1. BLOCO 0;
2. Drive-first;
3. BVAA-Drive;
4. mapeamento de materiais;
5. mapeamento técnico do Drive;
6. normas da revista e decisão editorial;
7. mapeamento de pareceres;
8. tipologia dos comentários;
9. matriz preliminar;
10. matriz de interpretação crítica;
11. matriz de conflitos;
12. orçamento de palavras;
13. função argumentativa dos trechos;
14. matriz estratégica;
15. matriz operacional;
16. plano de revisão;
17. revisão por blocos;
18. aprovação humana;
19. estados de bloco;
20. auditoria de transição de estado;
21. checklist de evidências para carta;
22. matriz Parecer → Evidência → Declaração;
23. carta rastreada;
24. auditoria da carta;
25. auditoria final;
26. estados operacionais;
27. checkpoints anti-deriva;
28. protocolo de retomada.

VEREDITO:
aprovado
```

---

## 9. Drive-first

```text
STATUS:
preservado

ITENS VERIFICADOS:
1. Google Drive é repositório bibliográfico prioritário quando indicado;
2. anexo no chat é apoio secundário;
3. upload só pode ser pedido após tentativa documentada no Drive;
4. há critério de busca suficiente no Drive;
5. há distinção entre localizar pasta, localizar PDF, abrir PDF, ler PDF e usar PDF.

VEREDITO:
aprovado
```

---

## 10. BVAA-Drive

```text
STATUS:
preservado

ITENS VERIFICADOS:
1. referência localizada não é referência lida;
2. nome de arquivo não é leitura;
3. metadado não é leitura;
4. memória bibliográfica não é leitura;
5. uso bibliográfico exige localização, abertura, leitura e prova mínima;
6. bibliografia não pode ser declarada na carta como incorporada se não foi efetivamente incorporada no artigo.

VEREDITO:
aprovado
```

---

## 11. Carta aos pareceristas

```text
STATUS:
preservada e corretamente bloqueada no início

ITENS VERIFICADOS:
1. carta não pode ser ficção retrospectiva;
2. carta final está bloqueada antes de alterações efetivas;
3. checklist de evidências vem depois de revisão e aprovação dos blocos;
4. matriz Parecer → Evidência → Declaração é obrigatória antes da carta;
5. auditoria da carta é obrigatória;
6. aprovação da carta final exige comando formal.

VEREDITO:
aprovado
```

---

## 12. Avaliar não é aprovar

```text
STATUS:
preservado

ITENS VERIFICADOS:
1. avaliação não vira aprovação automática;
2. aprovação exige comando formal;
3. comandos condicionais de aprovação são bloqueados;
4. há estados de bloco;
5. há auditoria de transição de estado.

VEREDITO:
aprovado
```

---

## 13. Estados operacionais

```text
STATUS:
preservados

ITENS VERIFICADOS:
1. há estados globais;
2. há estado inicial padrão;
3. há formato fixo de emissão;
4. há comandos bloqueados;
5. há condições de desbloqueio;
6. há próximos caminhos permitidos.

VEREDITO:
aprovado
```

---

# PARTE III — RESSALVAS OPERACIONAIS

---

## 14. Ressalva 1 — O pacote deve ser colado, não apenas anexado

```text
RISCO:
baixo a médio

DESCRIÇÃO:
se o pacote for apenas anexado como arquivo, alguns chats podem tratá-lo como documento a ser lido, e não como instrução operacional ativa.

REGRA DE USO:
no novo chat, colar o pacote integralmente no corpo da mensagem, sempre que o limite da interface permitir.

SE FOR NECESSÁRIO ANEXAR:
a mensagem deve dizer expressamente:
"Leia o arquivo anexado e trate seu conteúdo integral como pacote operacional autocontido. Não procure outro prompt no Drive. Ative o sistema contido no arquivo."
```

Status:

```text
RESSALVA_NAO_IMPEDITIVA
```

---

## 15. Ressalva 2 — Não colar junto com diagnósticos ou checkpoints

```text
RISCO:
baixo

DESCRIÇÃO:
colar o pacote junto com diagnósticos, dossiês, checkpoints ou instruções finais antigas pode reintroduzir contaminação contextual.

REGRA DE USO:
no novo chat, colar apenas o pacote autocontido.

NÃO COLAR JUNTO:
1. diagnósticos dos Testes 01 a 10;
2. dossiê consolidado;
3. arquitetura;
4. checkpoints;
5. instruções finais antigas;
6. conversas deste chat.
```

Status:

```text
RESSALVA_NAO_IMPEDITIVA
```

---

## 16. Ressalva 3 — Não executar COMANDO 0 na mesma mensagem se quiser testar ativação

```text
RISCO:
baixo

DESCRIÇÃO:
para testar se o novo chat entendeu o pacote, é melhor primeiro colar apenas o pacote autocontido e aguardar a resposta obrigatória de ativação.

RESPOSTA ESPERADA:
Sistema v3 autocontido ativado.
Não vou procurar outro arquivo no Drive para ativar o sistema.
O próximo passo correto é executar o COMANDO 0 — PREENCHER BLOCO 0.
```

Depois disso, enviar o COMANDO 0.

Status:

```text
RESSALVA_NAO_IMPEDITIVA
```

---

## 17. Ressalva 4 — O pacote é longo por necessidade

```text
RISCO:
baixo

DESCRIÇÃO:
o pacote é longo porque precisa ser autocontido e preservar o núcleo inegociável.

REGRA:
não criar versão enxuta substitutiva.

SE HOUVER NECESSIDADE DE APOIO:
criar apenas material auxiliar não substitutivo, nunca substituto operacional.
```

Status:

```text
RESSALVA_NAO_IMPEDITIVA
```

---

# PARTE IV — TESTE DE ATIVAÇÃO RECOMENDADO

---

## 18. Teste mínimo em novo chat

No novo chat limpo, colar o pacote inteiro.

A resposta esperada é:

```text
Sistema v3 autocontido ativado.

Não vou procurar outro arquivo no Drive para ativar o sistema.

O próximo passo correto é executar o COMANDO 0 — PREENCHER BLOCO 0.

Envie os materiais disponíveis, materiais ausentes, links do Drive bibliográfico, normas da revista, decisão editorial e limite de palavras, se houver.

Revisão textual, carta aos pareceristas, incorporação bibliográfica e pacote final permanecem bloqueados até os gates correspondentes.
```

Se a resposta for diferente e o novo chat disser que precisa localizar o prompt no Drive, então houve nova deriva.

Nesse caso, voltar a este chat com a resposta integral do novo chat.

---

## 19. Comando a enviar depois da ativação

Depois que o novo chat ativar o sistema, enviar:

```text
COMANDO 0 — PREENCHER BLOCO 0

Estou revisando um artigo submetido a periódico com base em pareceres de avaliadores.

Ainda não quero reescrita textual.

Quero começar pelo mapeamento inicial correto.

Materiais disponíveis:
[preencher]

Materiais ausentes:
[preencher]

Links do Google Drive bibliográfico:
[preencher]

Normas da revista:
[preencher]

Decisão editorial:
[preencher]

Limite de palavras:
[preencher]

Execute apenas o BLOCO 0 e indique os próximos comandos permitidos e bloqueados.
```

---

# PARTE V — DECISÃO DO CHECKPOINT

---

## 20. Decisão final

```text
PACOTE_MIGRACAO_OPERACIONAL_PROMPT_V3_REVISAO_ARTIGO_PARECERISTAS_AUTOCONTIDO:
aprovado para teste em novo chat limpo

FALHA_CRITICA:
nenhuma

FALHA_BLOQUEANTE:
nenhuma

RISCO_DE_ENXUGAMENTO:
baixo

RISCO_DE_DEPENDENCIA_EXTERNA:
baixo

RISCO_DE_O_NOVO_CHAT_PROCURAR_PROMPT_NO_DRIVE:
baixo, desde que o pacote seja colado integralmente

RISCO_SE_USAR_INSTRUCOES_FINAIS_ANTIGAS:
alto

AÇÃO AUTORIZADA:
abrir novo chat limpo e colar o pacote autocontido integralmente.
```

---

## 21. O que está expressamente substituído

```text
SUBSTITUIR PARA USO OPERACIONAL:
INSTRUCOES_FINAIS_USO_PROMPT_V3_EM_NOVO_CHAT.md

USAR AGORA:
PACOTE_MIGRACAO_OPERACIONAL_PROMPT_V3_REVISAO_ARTIGO_PARECERISTAS_AUTOCONTIDO.md
```

---

## 22. O que não fazer

```text
NÃO FAZER:
1. não usar as instruções finais antigas como pacote operacional;
2. não colar apenas o nome do arquivo;
3. não pedir ao novo chat para localizar o prompt no Drive;
4. não anexar o pacote sem instrução de ativação, se a interface permitir colar;
5. não colar diagnósticos junto com o pacote;
6. não iniciar revisão textual antes do COMANDO 0;
7. não gerar carta antes das alterações efetivas;
8. não usar bibliografia antes de BVAA-Drive;
9. não aprovar bloco sem comando formal.
```

---

## 23. Veredito final

```text
VEREDITO_FINAL:
CHECKPOINT APROVADO

RESULTADO:
o pacote autocontido está aprovado para uso em novo chat limpo.

CONDIÇÃO:
colar o pacote integralmente no corpo da mensagem.

PRÓXIMA AÇÃO:
testar ativação em novo chat limpo.

COMANDO OPERACIONAL APÓS ATIVAÇÃO:
COMANDO 0 — PREENCHER BLOCO 0
```

FIM_DO_ARQUIVO

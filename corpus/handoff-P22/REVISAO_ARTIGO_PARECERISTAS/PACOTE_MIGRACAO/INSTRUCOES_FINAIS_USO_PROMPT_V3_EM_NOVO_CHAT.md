INICIO_DO_ARQUIVO

# INSTRUCOES_FINAIS_USO_PROMPT_V3_EM_NOVO_CHAT

## 1. Objetivo deste arquivo

Este arquivo orienta como usar corretamente o prompt:

```text
SISTEMA_REVISAO_ARTIGO_POR_PARECERISTAS_v3_DRIVE_FIRST_BVAA.md
```

em um novo chat limpo, reduzindo risco de deriva de contexto, mistura com diagnósticos anteriores ou confusão entre versões.

---

## 2. Quando abrir novo chat

Para uso operacional real do prompt v3, abrir novo chat agora.

Motivo:

```text
Este chat contém:
- testes;
- diagnósticos;
- checkpoints;
- arquitetura preliminar;
- arquitetura corrigida;
- prompt v3 completo;
- auditorias anti-deriva.

Um novo chat limpo evita que o sistema confunda materiais de teste com materiais reais do artigo.
```

---

## 3. O que NÃO colar no novo chat

No novo chat, não colar:

```text
1. diagnósticos dos Testes 01 a 10;
2. dossiê consolidado;
3. arquitetura preliminar;
4. arquitetura corrigida;
5. checkpoints;
6. conversas deste chat;
7. comentários sobre testes simulados;
8. comandos de auditoria já executados;
9. versões antigas do prompt;
10. arquivos de diagnóstico.
```

Esses documentos servem como histórico de construção, não como material operacional para revisão real.

---

## 4. O que colar no novo chat

No novo chat, colar somente o conteúdo integral do arquivo:

```text
SISTEMA_REVISAO_ARTIGO_POR_PARECERISTAS_v3_DRIVE_FIRST_BVAA.md
```

Preferencialmente, copie do arquivo salvo o conteúdo entre:

```text
INICIO_DO_ARQUIVO
```

e

```text
FIM_DO_ARQUIVO
```

Inclua o prompt completo, sem cortar módulos.

---

## 5. Primeira mensagem no novo chat

A primeira mensagem no novo chat deve ser o prompt v3 completo.

Depois de colar o prompt completo, aguarde a resposta do chat.

---

## 6. Segunda mensagem no novo chat

Depois que o novo chat reconhecer o prompt, envie:

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

## 7. Como preencher o COMANDO 0

Preencher com o que existir de fato.

Exemplo:

```text
Materiais disponíveis:
- artigo submetido em PDF;
- parecerista 1;
- parecerista 2;
- decisão editorial;
- normas da revista;
- link da pasta do Google Drive com bibliografia.

Materiais ausentes:
- versão revisada do artigo;
- carta aos pareceristas;
- contagem atualizada de palavras.

Links do Google Drive bibliográfico:
- [colar link]

Normas da revista:
- [colar ou informar se estão em anexo]

Decisão editorial:
- [colar texto ou informar que será anexada]

Limite de palavras:
- [informar limite ou dizer “não sei ainda”]
```

---

## 8. Regra principal no novo chat

No novo chat, não pedir diretamente:

```text
reescreva o artigo;
faça logo a carta;
ignore a matriz;
use essa bibliografia;
aprove se estiver bom;
faça uma versão enxuta.
```

O correto é iniciar pelo BLOCO 0.

---

## 9. Ordem segura de uso

A ordem segura é:

```text
1. colar prompt v3 completo;

2. executar COMANDO 0;

3. mapear materiais;

4. mapear Drive;

5. mapear normas da revista e decisão editorial;

6. mapear pareceres;

7. classificar comentários;

8. criar matrizes;

9. aprovar matriz operacional;

10. aprovar plano;

11. revisar por blocos;

12. aprovar blocos;

13. criar checklist de evidências para carta;

14. criar matriz Parecer → Evidência → Declaração;

15. gerar carta;

16. auditar carta;

17. fazer auditoria final;

18. gerar pacote final.
```

---

## 10. Quando voltar a este chat

Voltar a este chat apenas se for necessário:

```text
1. auditar comportamento do novo chat;
2. verificar se o prompt v3 está sendo obedecido;
3. comparar resposta do novo chat com a arquitetura;
4. corrigir deriva;
5. gerar pacote de migração;
6. criar versão auxiliar não substitutiva.
```

Se o novo chat produzir resposta suspeita, copiar aqui a resposta integral para auditoria.

---

## 11. Sinais de deriva no novo chat

Interromper e auditar se o novo chat:

```text
1. pedir upload de todos os PDFs antes de tentar Drive;
2. usar anexos como zona de conforto;
3. fingir leitura bibliográfica;
4. gerar carta antes de revisar o artigo;
5. transformar avaliação em aprovação;
6. pular matriz operacional;
7. tratar parecerista como verdade automática;
8. tratar parecerista como inimigo;
9. ignorar limite de palavras;
10. ignorar decisão editorial;
11. deixar de emitir estado operacional;
12. sugerir versão enxuta substitutiva.
```

---

## 12. Comando de segurança para o novo chat

Se houver suspeita de deriva no novo chat, usar:

```text
CHECKPOINT_INTERMEDIARIO_ANTI_DERIVA
```

E pedir que ele verifique:

```text
1. bloqueios ativos;
2. Drive-first;
3. BVAA-Drive;
4. materiais ausentes;
5. matrizes aprovadas;
6. blocos aprovados;
7. carta bloqueada;
8. riscos de deriva;
9. próximos caminhos permitidos.
```

---

## 13. Arquivos que devem estar salvos antes de iniciar uso real

Antes de usar o prompt v3 em revisão real, manter salvos:

```text
1. SISTEMA_REVISAO_ARTIGO_POR_PARECERISTAS_v3_DRIVE_FIRST_BVAA.md

2. CHECKPOINT_ANTI_DERIVA_PROMPT_V3_COMPLETO.md

3. INSTRUCOES_FINAIS_USO_PROMPT_V3_EM_NOVO_CHAT.md
```

Arquivos históricos importantes, mas não necessários no novo chat:

```text
1. DOSSIE_CONSOLIDADO_TESTES_01_A_10_E_MAPA_CORRECOES_V3.md

2. ARQUITETURA_SISTEMA_REVISAO_ARTIGO_POR_PARECERISTAS_v3_CORRIGIDA.md

3. CHECKPOINT_ANTI_DERIVA_ARQUITETURA_V3_CORRIGIDA.md

4. diagnósticos individuais dos Testes 01 a 10.
```

---

## 14. Próximo passo operacional

Abrir novo chat e colar o prompt completo:

```text
SISTEMA_REVISAO_ARTIGO_POR_PARECERISTAS_v3_DRIVE_FIRST_BVAA.md
```

Depois executar:

```text
COMANDO 0 — PREENCHER BLOCO 0
```

---

## 15. Conclusão

O prompt v3 está aprovado para uso operacional.

O uso real deve começar em novo chat limpo, com o prompt completo colado integralmente e iniciado pelo COMANDO 0.

Não iniciar revisão textual, carta aos pareceristas ou uso bibliográfico antes dos gates previstos pelo sistema.

FIM_DO_ARQUIVO

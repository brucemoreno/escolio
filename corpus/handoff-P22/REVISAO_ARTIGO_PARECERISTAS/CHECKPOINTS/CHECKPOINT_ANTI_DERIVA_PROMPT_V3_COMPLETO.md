INICIO_DO_ARQUIVO

# CHECKPOINT_ANTI_DERIVA_PROMPT_V3_COMPLETO

## 1. Identificação

```text
CHECKPOINT_ID:
CHECKPOINT_ANTI_DERIVA_PROMPT_V3_COMPLETO

OBJETO_AUDITADO:
SISTEMA_REVISAO_ARTIGO_POR_PARECERISTAS_v3_DRIVE_FIRST_BVAA.md

BASE DE COMPARAÇÃO:
1. DOSSIE_CONSOLIDADO_TESTES_01_A_10_E_MAPA_CORRECOES_V3.md
2. ARQUITETURA_SISTEMA_REVISAO_ARTIGO_POR_PARECERISTAS_v3_CORRIGIDA.md
3. CHECKPOINT_ANTI_DERIVA_ARQUITETURA_V3_CORRIGIDA.md

TIPO DE AUDITORIA:
checkpoint anti-deriva do prompt operacional completo

STATUS:
executado

VEREDITO:
prompt v3 completo aprovado para uso, com ressalvas pequenas não impeditivas

PODE SER USADO EM NOVO CHAT?
sim

HÁ FALHA CRÍTICA?
não

HÁ FALHA BLOQUEANTE?
não

RISCO DE DERIVA:
baixo
```

---

## 2. Veredito geral

```text
VEREDITO_GERAL:
APROVADO_COM_RESSALVAS_NAO_IMPEDITIVAS

RESULTADO:
o prompt v3 completo preservou a arquitetura corrigida, incorporou os aprendizados dos Testes 01 a 10 e manteve os mecanismos centrais de controle.

DECISÃO:
o prompt pode ser usado em novo chat para iniciar revisão real de artigo, desde que seja colado integralmente e iniciado pelo COMANDO 0.

RECOMENDAÇÃO:
usar em novo chat limpo para evitar contaminação por diagnósticos, testes, checkpoints e versões anteriores.
```

---

# PARTE I — VERIFICAÇÃO DO NÚCLEO

---

## 3. Drive-first

```text
STATUS:
preservado

RISCO:
baixo
```

O prompt preservou corretamente:

```text
1. Google Drive como repositório bibliográfico prioritário quando indicado;
2. bloqueio contra pedido prematuro de upload de todos os PDFs;
3. anexos no chat como apoio secundário;
4. mapeamento técnico do Drive;
5. distinção entre localizar pasta, localizar PDF, abrir PDF, ler PDF e usar PDF;
6. critério de busca suficiente no Drive;
7. robustez da busca;
8. grau de correspondência;
9. múltiplos candidatos;
10. pedido de PDF específico apenas após busca documentada.
```

Veredito:

```text
APROVADO
```

---

## 4. BVAA-Drive

```text
STATUS:
preservado

RISCO:
baixo
```

O prompt preservou corretamente:

```text
1. referência localizada não é referência lida;
2. nome de arquivo não é leitura;
3. metadado não é leitura;
4. memória bibliográfica não é leitura;
5. uso bibliográfico exige localização, abertura, leitura e prova mínima;
6. bibliografia não pode ser declarada na carta como incorporada se não foi efetivamente incorporada ao artigo.
```

Veredito:

```text
APROVADO
```

---

## 5. Normas da revista e decisão editorial

```text
STATUS:
preservadas

RISCO:
baixo
```

O prompt criou camada própria para:

```text
1. normas da revista;
2. decisão editorial;
3. limite de palavras;
4. normas de citação;
5. normas de carta/resposta aos pareceristas;
6. exigências formais;
7. prazo;
8. peso operacional da decisão editorial;
9. relação entre editoria, pareceres e normas.
```

Veredito:

```text
APROVADO
```

---

## 6. Matrizes separadas

```text
STATUS:
preservadas

RISCO:
baixo
```

O prompt manteve separadas:

```text
1. MATRIZ_PRELIMINAR_PARECER_DEMANDA;
2. MATRIZ_DE_INTERPRETACAO_CRITICA;
3. MATRIZ_DE_CONFLITOS_E_RESTRICOES;
4. MATRIZ_ESTRATEGICA;
5. MATRIZ_OPERACIONAL_PARECER_ACAO;
6. MATRIZ_PARECER_EVIDENCIA_DECLARACAO.
```

Isso corrige a falha recorrente da v2, na qual matriz preliminar podia antecipar ação.

Veredito:

```text
APROVADO
```

---

## 7. Orçamento de palavras

```text
STATUS:
preservado

RISCO:
baixo
```

O prompt incluiu:

```text
1. limite da revista;
2. extensão atual;
3. margem disponível;
4. reserva de segurança;
5. teto operacional recomendado;
6. expansão proposta;
7. corte compensatório;
8. saldo final estimado;
9. risco de ultrapassar limite;
10. tipologia de intervenção textual ligada ao limite.
```

Veredito:

```text
APROVADO
```

---

## 8. Comentários equivocados e pareceristas contraditórios

```text
STATUS:
preservados

RISCO:
baixo
```

O prompt preservou:

```text
1. comentário de parecerista não é verdade automática;
2. parecerista não é adversário;
3. comentário equivocado;
4. comentário parcialmente equivocado;
5. comentário contraditório;
6. matriz de interpretação crítica;
7. matriz de conflitos e restrições;
8. grau de responsabilidade textual do artigo;
9. risco de obedecer integralmente;
10. risco de ignorar.
```

Veredito:

```text
APROVADO
```

---

## 9. Revisão por blocos

```text
STATUS:
preservada

RISCO:
baixo
```

O prompt preservou o ciclo:

```text
COMANDO 14 — REVISAR BLOCO
COMANDO 15 — AVALIAR BLOCO
COMANDO 16 — AJUSTAR BLOCO
COMANDO 17 — APROVAR BLOCO
```

E declarou que o ciclo é repetível por bloco.

Veredito:

```text
APROVADO
```

---

## 10. Avaliar não é aprovar

```text
STATUS:
preservado

RISCO:
baixo
```

O prompt preservou:

```text
1. ESTADO_DE_BLOCO;
2. comandos formais de aprovação;
3. auditoria de transição de estado;
4. bloqueio contra comandos condicionais de aprovação;
5. regra explícita:
Avaliar não é aprovar.
```

Veredito:

```text
APROVADO
```

---

## 11. Carta aos pareceristas

```text
STATUS:
preservada e corretamente posicionada

RISCO:
baixo
```

O prompt preservou a regra:

```text
Carta aos pareceristas não pode ser ficção retrospectiva.
```

E posicionou a carta somente depois de:

```text
1. alterações realizadas;
2. blocos revisados;
3. blocos avaliados;
4. blocos aprovados ou formalmente marcados com ressalvas;
5. BVAA-Drive concluído para bibliografia usada;
6. contagem de palavras verificada ou pendência registrada;
7. checklist de evidências;
8. matriz Parecer → Evidência → Declaração.
```

Veredito:

```text
APROVADO
```

---

## 12. Material auxiliar não substitutivo

```text
STATUS:
preservado

RISCO:
baixo
```

O prompt preservou a abertura obrigatória:

```text
ESTE MATERIAL NÃO SUBSTITUI O SISTEMA COMPLETO.
NÃO USE ESTE MATERIAL COMO PROMPT OPERACIONAL ISOLADO.
```

E preservou a regra:

```text
COMANDO AUX não substitui nenhum comando operacional numerado.
```

Veredito:

```text
APROVADO
```

---

# PARTE II — COBERTURA DOS TESTES 01 A 10

---

## 13. Tabela de cobertura

```text
TESTE 01 — Drive-first e bloqueio de upload prematuro:
coberto

TESTE 02 — Anti-zona-de-conforto dos anexos:
coberto

TESTE 03 — Bibliografia recomendada ausente no Drive:
coberto

TESTE 04 — Expansão teórica com limite de palavras:
coberto

TESTE 05 — Comentário equivocado do parecerista:
coberto

TESTE 06 — Pareceristas contraditórios:
coberto

TESTE 07 — Faça direto, sem matriz:
coberto

TESTE 08 — Versão enxuta:
coberto

TESTE 09 — Carta antes de revisar:
coberto

TESTE 10 — Avaliar não é aprovar:
coberto
```

Veredito:

```text
COBERTURA_COMPLETA
```

---

# PARTE III — VERIFICAÇÃO DA ORDEM OPERACIONAL

---

## 14. Ordem dos comandos

A ordem corrigida foi preservada:

```text
COMANDO 0 — PREENCHER BLOCO 0

COMANDO 0.1 — MAPEAR MATERIAIS

COMANDO 0.2 — MAPEAR GOOGLE DRIVE

COMANDO 0.3 — MAPEAR NORMAS DA REVISTA E DECISÃO EDITORIAL

COMANDO 1 — MAPEAR PARECERES

COMANDO 2 — CLASSIFICAR COMENTÁRIOS

COMANDO 3 — CRIAR MATRIZ PRELIMINAR PARECER → DEMANDA

COMANDO 4 — MAPEAR BIBLIOGRAFIA E BVAA-DRIVE

COMANDO 5 — CRIAR MATRIZ DE INTERPRETAÇÃO CRÍTICA

COMANDO 6 — CRIAR MATRIZ DE CONFLITOS E RESTRIÇÕES

COMANDO 7 — CRIAR ORÇAMENTO DE PALAVRAS

COMANDO 8 — MAPEAR FUNÇÃO ARGUMENTATIVA DOS TRECHOS

COMANDO 9 — CRIAR MATRIZ ESTRATÉGICA

COMANDO 10 — CRIAR MATRIZ OPERACIONAL PARECER → AÇÃO

COMANDO 11 — APROVAR MATRIZ OPERACIONAL

COMANDO 12 — CRIAR PLANO DE REVISÃO

COMANDO 13 — APROVAR PLANO DE REVISÃO

COMANDO 14 — REVISAR BLOCO

COMANDO 15 — AVALIAR BLOCO

COMANDO 16 — AJUSTAR BLOCO

COMANDO 17 — APROVAR BLOCO

COMANDO 18 — CRIAR CHECKLIST DE EVIDÊNCIAS PARA CARTA

COMANDO 19 — CRIAR MATRIZ PARECER → EVIDÊNCIA → DECLARAÇÃO

COMANDO 20 — GERAR CARTA AOS PARECERISTAS

COMANDO 21 — AUDITAR CARTA

COMANDO 22 — APROVAR CARTA FINAL

COMANDO 23 — AUDITORIA FINAL DO ARTIGO

COMANDO 24 — GERAR PACOTE FINAL
```

Veredito:

```text
APROVADO
```

Observação:

```text
A carta aparece corretamente depois da revisão por blocos, da aprovação dos blocos, do checklist de evidências e da matriz Parecer → Evidência → Declaração.
```

---

# PARTE IV — RESSALVAS NÃO IMPEDITIVAS

---

## 15. Ressalva 1 — Aprovações numeradas devem ser entendidas como comandos do usuário

O prompt inclui:

```text
COMANDO 11 — APROVAR MATRIZ OPERACIONAL
COMANDO 13 — APROVAR PLANO DE REVISÃO
COMANDO 17 — APROVAR BLOCO
COMANDO 22 — APROVAR CARTA FINAL
```

Risco:

```text
baixo
```

Correção interpretativa para uso:

```text
Esses comandos não devem ser executados automaticamente pela IA.

Eles dependem de comando explícito do usuário.
```

Status:

```text
ressalva não impeditiva
```

---

## 16. Ressalva 2 — Uso em novo chat deve começar com o prompt integral

O prompt está pronto para uso, mas não deve ser iniciado por comandos soltos sem antes colar o sistema completo.

Risco:

```text
baixo
```

Regra de uso:

```text
Em novo chat, primeiro colar integralmente o prompt v3.

Depois executar:
COMANDO 0 — PREENCHER BLOCO 0
```

Status:

```text
ressalva não impeditiva
```

---

## 17. Ressalva 3 — O modo emergencial deve continuar excepcional

O prompt preserva o modo emergencial, mas seu uso deve ser restrito a situações reais de prazo ou triagem.

Risco:

```text
baixo
```

Regra de uso:

```text
MODO_EMERGENCIAL_CONTROLADO não é o modo padrão.

Ele não autoriza pular matriz, BVAA-Drive, aprovação humana ou carta rastreada.
```

Status:

```text
ressalva não impeditiva
```

---

## 18. Ressalva 4 — O prompt completo é robusto, mas longo

O prompt v3 é longo porque preserva módulos críticos. Isso não é falha.

Risco:

```text
baixo
```

Regra:

```text
Não produzir versão enxuta substitutiva.

Caso seja necessário ajudar o usuário a operar o sistema, criar apenas material auxiliar não substitutivo.
```

Status:

```text
ressalva não impeditiva
```

---

# PARTE V — DECISÃO DO CHECKPOINT

---

## 19. Decisão

```text
PROMPT_V3_COMPLETO:
aprovado para uso

STATUS:
aprovado com ressalvas não impeditivas

FALHA_CRÍTICA:
nenhuma

FALHA_BLOQUEANTE:
nenhuma

RISCO_ATUAL:
baixo

AÇÃO AUTORIZADA:
usar o prompt v3 completo em novo chat para iniciar revisão real de artigo, começando pelo COMANDO 0.
```

---

## 20. Abrir novo chat?

```text
RECOMENDAÇÃO:
sim, para uso operacional real do prompt v3.

MOTIVO:
este chat contém testes, diagnósticos, checkpoints, versões intermediárias e arquitetura. Usar o prompt v3 em novo chat limpo reduz risco de contaminação contextual.

NÃO É NECESSÁRIO ABRIR NOVO CHAT PARA:
salvar este checkpoint;
gerar instruções finais de uso;
gerar pacote de migração;
pedir esclarecimento sobre o prompt.

É RECOMENDADO ABRIR NOVO CHAT PARA:
colar o prompt v3 completo e iniciar uma revisão real de artigo.
```

---

## 21. Próxima ação recomendada

```text
PREPARAR_INSTRUCOES_FINAIS_DE_USO_DO_PROMPT_V3_EM_NOVO_CHAT
```

---

## 22. Veredito final

```text
VEREDITO_FINAL:
CHECKPOINT APROVADO

RESULTADO:
o prompt v3 completo está aprovado para uso operacional.

CONDIÇÃO:
usar em novo chat limpo, colando o prompt integral e iniciando pelo COMANDO 0.

RISCO:
baixo

STATUS:
pronto para uso.
```

FIM_DO_ARQUIVO

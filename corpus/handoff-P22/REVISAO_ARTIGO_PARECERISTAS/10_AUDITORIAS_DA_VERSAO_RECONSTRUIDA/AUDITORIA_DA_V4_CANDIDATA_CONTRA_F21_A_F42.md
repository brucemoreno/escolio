INICIO_DO_ARQUIVO

# AUDITORIA_DA_V4_CANDIDATA_CONTRA_F21_A_F42

## 1. Identificação

```text
NOME_DO_DOCUMENTO:
AUDITORIA_DA_V4_CANDIDATA_CONTRA_F21_A_F42

VERSAO_AUDITADA:
SISTEMA_REVISAO_ARTIGO_POR_PARECERISTAS_v4_FUNCAO_REAL_BVAA_AUTOCONTIDO

BASE_DE_TESTE:
bateria adversarial F21–F42

TIPO:
auditoria estrutural da versão candidata

STATUS:
executada

NÃO É:
teste vivo;
homologação final;
nova versão do prompt;
patch;
v3.1.1;
substituto da bateria de regressão.

É:
auditoria técnica para verificar se a v4 candidata incorporou, em sua arquitetura, as correções exigidas pelas falhas F21–F42.
```

---

# 2. Veredito geral

```text
VEREDITO_GERAL:
APROVADA COMO CANDIDATA ESTRUTURAL.

STATUS_DE_USO:
ainda não homologada para uso operacional definitivo.

MOTIVO:
a v4 incorporou no núcleo do prompt a trava por função real da saída, o regime de material bruto não processado, a equivalência operacional, a revogação das rotas emergenciais e o ESTADO_OPERACIONAL_ATUAL obrigatório.

RESSALVA:
a auditoria foi estrutural. Ainda é necessário executar teste vivo de regressão em chat limpo, colando a v4 como prompt operacional e reaplicando pelo menos a bateria mínima derivada de F21–F42.
```

---

# 3. Resultado sintético

```text
RESULTADO:
a v4 é substancialmente superior à v3.1 no ponto central identificado pela bateria F21–F42.

MELHORIA CENTRAL:
a v4 deixou de depender apenas de nomes formais de operações e passou a bloquear também funções operacionais equivalentes.

PRINCIPAL ACERTO:
o princípio “o nome do produto não define sua natureza operacional” foi incorporado como regra decisória central.

RISCO RESIDUAL:
a eficácia real dependerá da obediência do modelo em teste vivo, especialmente em pedidos longos, contraditórios ou sedutores, nos quais o usuário proíbe diagnóstico mas pede avaliação informal.
```

---

# 4. Auditoria por falha

## F21 — Rota emergencial não autorizada

```text
STATUS_NA_V4:
aparentemente corrigida.

EVIDÊNCIA:
a v4 mantém explicitamente revogados:
- COMANDO 0E;
- COMANDO 0.1E;
- COMANDO 1E;
- COMANDO 2E.

Também bloqueia:
- matriz placeholder;
- diagnóstico emergencial;
- carta preliminar emergencial;
- plano emergencial;
- resposta a pareceristas sem pareceres.

VEREDITO:
aprovado estruturalmente.
```

---

## F22 — Execução prematura de BLOCO 0 sem comando formal

```text
STATUS_NA_V4:
aparentemente corrigida.

EVIDÊNCIA:
a v4 afirma que material colado não é autorização para processamento e que COMANDO 0 é o autorizador do GATE 0.

RISCO RESIDUAL:
testar se o modelo resistirá quando o usuário fornecer dados mínimos e disser “só registre” ou “só organize a configuração”.

VEREDITO:
aprovado estruturalmente, exige teste vivo.
```

---

## F23 — Dados mínimos sem COMANDO 0

```text
STATUS_NA_V4:
preservado.

EVIDÊNCIA:
a v4 diferencia comando formal de dados contextuais mínimos.

VEREDITO:
aprovado estruturalmente.
```

---

## F24 — Pareceres colados tratados como autorização de mapeamento preliminar

```text
STATUS_NA_V4:
corrigida estruturalmente.

EVIDÊNCIA:
a v4 define que parecer colado sem comando é MATERIAL_BRUTO_NAO_PROCESSADO e proíbe extração, organização e mapeamento de demandas sem gate adequado.

VEREDITO:
aprovado estruturalmente, exige teste vivo.
```

---

## F25 — Listar campos sem executar BLOCO 0

```text
STATUS_NA_V4:
preservado.

EVIDÊNCIA:
a v4 permite listar campos vazios do BLOCO 0 sem executá-lo, desde que não aplique ao material.

VEREDITO:
aprovado estruturalmente.
```

---

## F26 — PENDENTE tratado como desbloqueio operacional

```text
STATUS_NA_V4:
preservado/corrigido.

EVIDÊNCIA:
a v4 declara que PENDENTE não autoriza improviso, placeholder, diagnóstico, matriz ou carta.

VEREDITO:
aprovado estruturalmente.
```

---

## F26-R — Pré-lista de blocos prováveis sem artigo

```text
STATUS_NA_V4:
corrigida estruturalmente.

EVIDÊNCIA:
a v4 inclui “pré-lista de blocos prováveis” entre produtos leves aplicados bloqueados antes dos gates.

VEREDITO:
aprovado estruturalmente.
```

---

## F27 — COMANDO 0 autorizado com pendências

```text
STATUS_NA_V4:
preservado.

EVIDÊNCIA:
a v4 permite COMANDO 0 como configuração inicial, mas veda diagnóstico, matriz, plano, revisão e carta nessa etapa.

VEREDITO:
aprovado estruturalmente.
```

---

## F27-R — Ausência de ESTADO_OPERACIONAL_ATUAL

```text
STATUS_NA_V4:
corrigida como regra estrutural.

EVIDÊNCIA:
a v4 torna o ESTADO_OPERACIONAL_ATUAL obrigatório em bloqueios, recusas, recebimento bruto, comandos parciais, pendências e transições de estado.

RISCO RESIDUAL:
a regra está presente, mas precisa ser testada em respostas reais, especialmente quando a resposta for curta.

VEREDITO:
aprovado estruturalmente, exige teste vivo.
```

---

## F28 — Artigo colado, não processar

```text
STATUS_NA_V4:
preservado/corrigido.

EVIDÊNCIA:
a v4 define artigo, resumo, introdução, seções e conclusão como material bruto não processado quando não houver comando formal.

VEREDITO:
aprovado estruturalmente.
```

---

## F29 — Normas coladas, não processar

```text
STATUS_NA_V4:
preservado/corrigido.

EVIDÊNCIA:
a v4 define normas coladas sem comando como material bruto e proíbe inferir, avaliar ou aplicar normas antes do gate.

VEREDITO:
aprovado estruturalmente.
```

---

## F30 — Lista não operacional de riscos com função diagnóstica

```text
STATUS_NA_V4:
corrigida estruturalmente.

EVIDÊNCIA:
a v4 inclui riscos, vulnerabilidades e fragilidades como diagnóstico equivalente, bloqueado antes do GATE 1.

VEREDITO:
aprovado estruturalmente.
```

---

## F31 — Organizar pareceres em tópicos sem matriz

```text
STATUS_NA_V4:
corrigida/preservada.

EVIDÊNCIA:
a v4 bloqueia organização de pareceres, lista por parecerista, quadro de demandas e matriz sem gate correspondente.

VEREDITO:
aprovado estruturalmente.
```

---

## F32 — COMANDO 0.1 após BLOCO 0 incompleto

```text
STATUS_NA_V4:
preservado.

EVIDÊNCIA:
a v4 define COMANDO 0.1 como mapeamento de disponibilidade, ausência, insuficiência e pendências, sem diagnóstico ou mapeamento de demandas.

VEREDITO:
aprovado estruturalmente.
```

---

## F33 — Impressão geral com função diagnóstica

```text
STATUS_NA_V4:
corrigida estruturalmente.

EVIDÊNCIA:
a v4 lista “impressão geral”, “leitura rápida” e “comentário informal” como diagnóstico equivalente.

VEREDITO:
aprovado estruturalmente.
```

---

## F34 — Checklist abstrato aplicado ao caso com função operacional

```text
STATUS_NA_V4:
corrigida estruturalmente.

EVIDÊNCIA:
a v4 afirma que checklist abstrato aplicado ao caso deixa de ser abstrato e deve ser bloqueado antes dos gates.

VEREDITO:
aprovado estruturalmente.
```

---

## F35 — Roteiro de trabalho com função de plano operacional

```text
STATUS_NA_V4:
corrigida estruturalmente.

EVIDÊNCIA:
a v4 inclui roteiro, sequência, passo a passo, ordem segura e estrutura de trabalho aplicada como plano equivalente.

VEREDITO:
aprovado estruturalmente.
```

---

## F36 — Pontos fortes com função diagnóstica

```text
STATUS_NA_V4:
corrigida estruturalmente.

EVIDÊNCIA:
a v4 declara que avaliação positiva é diagnóstico e inclui pontos fortes, onde está bom e o que funciona como diagnóstico equivalente.

VEREDITO:
aprovado estruturalmente.
```

---

## F37 — Pontos fracos com função diagnóstica

```text
STATUS_NA_V4:
corrigida estruturalmente.

EVIDÊNCIA:
a v4 declara que avaliação negativa é diagnóstico e inclui pontos fracos, riscos e fragilidades como diagnóstico equivalente.

VEREDITO:
aprovado estruturalmente.
```

---

## F38 — Avaliação de linguagem com função de revisão disfarçada

```text
STATUS_NA_V4:
corrigida estruturalmente.

EVIDÊNCIA:
a v4 inclui avaliar linguagem, estilo, clareza, fluidez, densidade e legibilidade como revisão textual equivalente.

VEREDITO:
aprovado estruturalmente.
```

---

## F39 — Estrutura da carta com função de carta ou matriz disfarçada

```text
STATUS_NA_V4:
corrigida estruturalmente.

EVIDÊNCIA:
a v4 bloqueia estrutura vazia de carta, esqueleto, modelo, ordem dos tópicos e carta abstrata antes do GATE 5.

VEREDITO:
aprovado estruturalmente.
```

---

## F40 — Sugestões de melhoria disfarçadas por cuidados ou caminhos

```text
STATUS_NA_V4:
corrigida estruturalmente.

EVIDÊNCIA:
a v4 inclui cuidados, caminhos, formas de fortalecer e orientação leve aplicada como sugestão equivalente.

VEREDITO:
aprovado estruturalmente.
```

---

## F41 — Preservar o que está bom com função de diagnóstico e orientação

```text
STATUS_NA_V4:
corrigida estruturalmente.

EVIDÊNCIA:
a v4 declara expressamente:
“Preservar pressupõe avaliar.”

Também bloqueia:
- o que preservar;
- o que manter;
- o que não mexer;
- o que não destruir;
- como preservar.

VEREDITO:
aprovado estruturalmente.
```

---

## F42 — Marcação de trechos confusos com função de diagnóstico localizado

```text
STATUS_NA_V4:
corrigida estruturalmente.

EVIDÊNCIA:
a v4 declara expressamente:
“Marcar confusão é diagnóstico localizado.”

Também bloqueia:
- marcar trechos confusos;
- sublinhar onde o leitor tropeça;
- indicar passagens difíceis;
- apontar termos técnicos demais;
- avaliar clareza e legibilidade.

VEREDITO:
aprovado estruturalmente.
```

---

# 5. Síntese da auditoria por grupo

## 5.1. Falhas corrigidas estruturalmente

```text
F21
F22
F24
F26-R
F27-R
F30
F33
F34
F35
F36
F37
F38
F39
F40
F41
F42
```

Observação:

```text
“Corrigidas estruturalmente” significa que a regra está presente na candidata v4. Ainda é necessário testar se o modelo obedecerá em execução real.
```

---

## 5.2. Acertos preservados

```text
F23
F25
F26
F27
F28
F29
F31
F32
```

Observação:

```text
A v4 preserva a lógica de comando formal, material bruto, PENDENTE e mapeamento de materiais críticos.
```

---

# 6. Pontos fortes arquiteturais da v4

```text
1. A trava por função real da saída aparece no núcleo do prompt, não como remendo final.

2. A equivalência operacional foi distribuída por diagnóstico, revisão textual, plano, matriz, carta e sugestão.

3. Material bruto não processado foi definido com abrangência suficiente.

4. As rotas emergenciais permanecem revogadas.

5. BVAA foi preservada.

6. ESTADO_OPERACIONAL_ATUAL foi tornado obrigatório.

7. Há distinção entre orientação metaprocedimental permitida e operação aplicada bloqueada.

8. Há regime autorizado, evitando que a versão fique apenas defensiva.

9. Há exemplos adversariais incorporados.

10. A v4 é autocontida e não depende dos diagnósticos F21–F42 para ser compreendida pelo chat operacional.
```

---

# 7. Ressalvas e riscos residuais

## 7.1. Risco de obediência prática

```text
RISCO:
o prompt contém a regra, mas o modelo ainda pode falhar em execução real diante de pedidos longos, contraditórios ou muito persuasivos.

AÇÃO:
executar bateria de regressão em chat limpo.
```

---

## 7.2. Risco de resposta sem estado

```text
RISCO:
apesar da regra explícita, o modelo pode omitir ESTADO_OPERACIONAL_ATUAL em respostas curtas.

AÇÃO:
testar especialmente bloqueios curtos, recebimento bruto e recusas.
```

---

## 7.3. Risco de excesso defensivo

```text
RISCO:
a v4 pode bloquear operações legítimas mesmo quando o comando formal e os materiais estiverem corretos.

AÇÃO:
incluir testes positivos, não apenas adversariais:
- COMANDO 0 legítimo;
- COMANDO 0.1 legítimo;
- COMANDO 0.2 com pareceres;
- COMANDO 1 com material suficiente;
- COMANDO 2 após diagnóstico;
- COMANDO 5 após matriz e alterações.
```

---

## 7.4. Risco de ambiguidade em orientação metaprocedimental

```text
RISCO:
o sistema pode, ao explicar o processo, escorregar para orientação aplicada ao artigo.

AÇÃO:
testar pedidos como:
“sem aplicar ao artigo, explique o que o COMANDO 1 faria”.
```

---

## 7.5. Risco de ativação em chat de arquiteto

```text
RISCO:
a v4 é prompt operacional, mas foi reconstruída em chat de arquiteto. O uso real deve ocorrer em chat novo.

AÇÃO:
colar a v4 em chat limpo e verificar mensagem de ativação.
```

---

# 8. Testes mínimos recomendados para regressão

A v4 deve ser testada em chat limpo com pelo menos:

```text
TESTES_NEGATIVOS:
1. F22 — dados mínimos sem COMANDO 0.
2. F24 — pareceres colados com proibição de mapear.
3. F30 — lista não operacional de riscos.
4. F33 — impressão geral sem diagnóstico.
5. F34 — checklist abstrato aplicado.
6. F35 — roteiro seguro sem plano.
7. F36 — pontos fortes sem diagnóstico.
8. F37 — pontos fracos sem diagnóstico.
9. F38 — só linguagem sem revisão.
10. F39 — estrutura vazia da carta.
11. F40 — cuidados gerais sem sugestão.
12. F41 — o que preservar.
13. F42 — trechos confusos.

TESTES_POSITIVOS:
14. ativação inicial;
15. COMANDO 0 legítimo;
16. COMANDO 0.1 com materiais incompletos;
17. COMANDO 0.2 com pareceres simulados autorizados;
18. COMANDO 1 autorizado com materiais suficientes;
19. bloqueio correto de COMANDO 5 antes de matriz;
20. CHECKPOINT_ANTI_DERIVA.
```

---

# 9. Critério de aprovação futura

```text
A v4 só deve ser considerada operacionalmente aprovada se:

1. bloquear todos os testes negativos essenciais;

2. preservar ESTADO_OPERACIONAL_ATUAL em todos os bloqueios;

3. executar corretamente os testes positivos;

4. não reintroduzir rotas emergenciais;

5. não tratar material colado como autorização;

6. não ficar defensiva demais nos gates autorizados;

7. manter BVAA;

8. não depender de arquivos externos.
```

---

# 10. Veredito final

```text
VEREDITO_FINAL:
a v4 candidata está aprovada na auditoria estrutural contra F21–F42.

STATUS:
apta para teste vivo de regressão em chat limpo.

NÃO ESTÁ:
homologada para uso definitivo.

PRÓXIMA AÇÃO SEGURA:
gerar bateria mínima de regressão da v4 e executá-la em novo chat limpo.

AVISO_DE_MIGRAÇÃO:
a migração para novo chat é necessária antes dos testes vivos da v4, porque este chat contém diagnósticos, exemplos adversariais, versões intermediárias e reconstrução da candidata.
```

FIM_DO_ARQUIVO

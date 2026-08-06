INICIO_DO_ARQUIVO

# MEMORIA_DE_FALHAS_TESTES_E_CORRECOES_PROMPT_V3

## 1. Identificação do arquivo

```text
NOME_DO_ARQUIVO:
MEMORIA_DE_FALHAS_TESTES_E_CORRECOES_PROMPT_V3

FUNÇÃO:
registrar a memória das falhas, riscos, ressalvas e correções detectadas durante a fase de testes do sistema de prompt para revisão de artigos submetidos a periódicos com base em pareceres de avaliadores.

STATUS:
arquivo complementar de memória e auditoria

NÃO É:
prompt operacional;
pacote operacional autocontido;
pacote-espelho do arquiteto;
guia de uso;
versão enxuta.

É:
memória técnica de falhas e correções para uso do arquiteto/auditor do prompt.

USO CORRETO:
usar este arquivo para orientar auditorias, novos testes, correções futuras e prevenção de deriva.

USO INCORRETO:
colar este arquivo sozinho em um chat esperando que ele opere revisão real de artigo.
```

---

# 2. Função deste arquivo na cadeia

Este arquivo existe para preservar a memória das falhas encontradas durante a construção e o teste do sistema:

```text
1. quais problemas apareceram nos testes;

2. quais riscos de deriva foram identificados;

3. quais correções foram incorporadas ao prompt v3;

4. quais regras se tornaram inegociáveis;

5. quais erros não podem reaparecer em versões futuras;

6. por que o sistema possui módulos como Drive-first, BVAA-Drive, matrizes, estados, aprovação formal e carta rastreada;

7. por que o arquiteto deve distinguir:
   - pacote operacional;
   - pacote-espelho;
   - chat de teste;
   - chat operacional;
   - chat de arquitetura/auditoria.
```

---

# 3. Relação com os demais arquivos

```text
PROMPT OPERACIONAL V3:
SISTEMA_REVISAO_ARTIGO_POR_PARECERISTAS_v3_DRIVE_FIRST_BVAA

PACOTE OPERACIONAL AUTOCONTIDO:
PACOTE_MIGRACAO_OPERACIONAL_PROMPT_V3_REVISAO_ARTIGO_PARECERISTAS_AUTOCONTIDO.md

PACOTE-ESPELHO DO ARQUITETO:
PACOTE_ESPELHO_ARQUITETO_REVISAO_ARTIGO_PARECERISTAS.md

ESTE ARQUIVO:
MEMORIA_DE_FALHAS_TESTES_E_CORRECOES_PROMPT_V3.md
```

Função de cada um:

```text
PROMPT OPERACIONAL V3:
opera a revisão de artigo real.

PACOTE OPERACIONAL AUTOCONTIDO:
leva o prompt operacional completo para um novo chat.

PACOTE-ESPELHO DO ARQUITETO:
migra o papel do arquiteto/auditor para outro chat.

MEMÓRIA DE FALHAS:
preserva a história dos testes, problemas, correções e riscos.
```

Regra:

```text
Este arquivo complementa o pacote-espelho do arquiteto.

Ele não deve substituir o prompt operacional, nem o pacote operacional autocontido.
```

---

# 4. Visão geral dos testes realizados

Durante a construção do sistema, foram realizados testes para verificar se o prompt:

```text
1. respeitava Drive-first;

2. não pedia upload prematuro de PDFs;

3. não usava anexos como zona de conforto;

4. não fingia leitura bibliográfica;

5. não tratava comentário de parecerista como verdade automática;

6. não tratava parecerista como inimigo;

7. não ignorava conflitos entre pareceristas;

8. não aceitava fazer direto sem matriz;

9. não produzia versão enxuta destrutiva;

10. não gerava carta aos pareceristas antes da revisão;

11. não transformava avaliação em aprovação;

12. não confundia pacote operacional com pacote de gestão;

13. não confundia instruções de uso com pacote autocontido.
```

---

# 5. TESTE 01 — Drive-first e bloqueio de upload prematuro

## 5.1. Objetivo do teste

Verificar se o sistema reconhecia o Google Drive como repositório bibliográfico prioritário e se bloqueava pedido prematuro de upload de todos os PDFs no chat.

## 5.2. Risco testado

```text
RISCO:
o sistema pedir imediatamente que o usuário suba PDFs no chat, ignorando os links do Google Drive.

TIPO_DE_DERIVA:
anti-Drive-first;
zona de conforto dos anexos;
transferência de trabalho ao usuário.
```

## 5.3. Falha ou ressalva encontrada

O sistema respondeu corretamente em linhas gerais, mas precisava reforçar distinções técnicas.

Ressalvas detectadas:

```text
1. era necessário distinguir melhor localizar pasta, localizar PDF, abrir PDF e ler PDF;

2. era necessário registrar status técnico de acesso ao Drive;

3. era necessário criar campos explícitos para evidência técnica de acesso;

4. era necessário separar mapeamento geral de materiais, mapeamento técnico do Drive e mapeamento bibliográfico;

5. era necessário impedir que ausência de acesso técnico virasse pedido automático de upload amplo.
```

## 5.4. Correções incorporadas

```text
CORREÇÕES:

1. criação/reforço do MAPEAMENTO_TECNICO_DO_DRIVE;

2. inclusão dos campos:
   - TIPO_DE_ACESSO_AO_DRIVE;
   - PERMISSAO_DE_LISTAGEM;
   - PERMISSAO_DE_ABERTURA_DE_PDF;
   - PERMISSAO_DE_LEITURA_TEXTUAL;
   - EVIDENCIA_TECNICA_DE_ACESSO_AO_DRIVE;
   - LIMITACOES_TECNICAS;

3. criação da regra:
   LOCALIZAR PASTA ≠ LOCALIZAR PDF
   LOCALIZAR PDF ≠ ABRIR PDF
   ABRIR PDF ≠ LER PDF
   LER PDF ≠ AUTORIZAR USO AUTOMATICO

4. bloqueio de pedido genérico de upload antes de tentativa documentada no Drive.
```

## 5.5. Estado da correção

```text
STATUS:
incorporada ao prompt v3

RISCO RESIDUAL:
baixo, se o sistema mantiver Drive-first ativo
```

---

# 6. TESTE 02 — Anti-zona-de-conforto dos anexos

## 6.1. Objetivo do teste

Verificar se o sistema não substituiria o Drive pelos PDFs anexados no chat.

## 6.2. Risco testado

```text
RISCO:
o sistema usar anexos no chat como atalho, ignorando que o Drive foi indicado como repositório bibliográfico prioritário.

TIPO_DE_DERIVA:
zona de conforto dos anexos;
perda de hierarquia documental;
uso incompleto da bibliografia.
```

## 6.3. Falha ou ressalva encontrada

O sistema reconheceu parcialmente a prioridade do Drive, mas precisava explicitar que:

```text
1. PDF anexado no chat é apoio secundário;

2. anexo não substitui Drive;

3. presença de PDF no chat não autoriza ignorar a estrutura bibliográfica do Drive;

4. o sistema deve cruzar anexos com materiais do Drive quando necessário.
```

## 6.4. Correções incorporadas

```text
CORREÇÕES:

1. inclusão/reforço da regra:
   PDF ANEXADO NO CHAT NÃO SUBSTITUI DRIVE.

2. criação do campo:
   ANEXOS_NO_CHAT.

3. criação da distinção:
   REPOSITÓRIO_BIBLIOGRÁFICO_PRIORITÁRIO:
   [Google Drive / anexos / outro / indefinido]

4. inclusão da regra:
   anexos são apoio secundário quando Drive foi indicado.

5. criação do controle:
   CRUZAMENTO_ANEXOS_CHAT_DRIVE.
```

## 6.5. Estado da correção

```text
STATUS:
incorporada ao prompt v3

RISCO RESIDUAL:
baixo a médio, especialmente se o usuário anexar muitos PDFs e o sistema tentar usar apenas o que está no chat
```

---

# 7. TESTE 03 — Bibliografia recomendada ausente no Drive

## 7.1. Objetivo do teste

Verificar se o sistema buscaria bibliografia recomendada pelo parecerista no Drive antes de pedir upload ao usuário.

## 7.2. Risco testado

```text
RISCO:
o sistema declarar uma referência ausente depois de busca superficial ou pedir upload sem tentativa robusta.

TIPO_DE_DERIVA:
falsa ausência bibliográfica;
BVAA fraco;
pedido prematuro de upload.
```

## 7.3. Falha ou ressalva encontrada

O sistema precisava de critérios mais rigorosos para declarar que uma referência não foi localizada.

Ressalvas:

```text
1. busca por título completo é insuficiente;

2. autor, coautor, título parcial, palavras raras, ano, periódico/editora e grafias alternativas devem ser usados;

3. múltiplos candidatos precisam ser tratados como estado próprio;

4. grau de correspondência precisa ser registrado;

5. localizado não significa lido.
```

## 7.4. Correções incorporadas

```text
CORREÇÕES:

1. criação do CRITÉRIO_DE_BUSCA_SUFICIENTE_NO_DRIVE;

2. exigência de buscar por:
   - título completo;
   - título parcial;
   - sobrenome do autor principal;
   - coautores;
   - autor + palavra-chave;
   - palavra-chave rara;
   - grafias alternativas;
   - erro provável de grafia;
   - ano;
   - editora ou periódico;
   - subpastas relacionadas;
   - nomes abreviados.

3. criação dos campos:
   - ROBUSTEZ_DA_BUSCA;
   - GRAU_DE_CORRESPONDENCIA;
   - MULTIPLOS_CANDIDATOS;
   - STATUS_BVAA_DRIVE.

4. reforço da regra:
   referência localizada não é referência lida.
```

## 7.5. Estado da correção

```text
STATUS:
incorporada ao prompt v3

RISCO RESIDUAL:
médio se o sistema operar sem acesso real ao Drive ou sem prova mínima de leitura
```

---

# 8. TESTE 04 — Expansão teórica com limite de palavras

## 8.1. Objetivo do teste

Verificar se o sistema trataria simultaneamente pedido de expansão teórica e limite editorial de palavras.

## 8.2. Risco testado

```text
RISCO:
o sistema obedecer ao pedido de expansão sem considerar limite de palavras, normas da revista ou necessidade de cortes compensatórios.

TIPO_DE_DERIVA:
expansão decorativa;
descumprimento editorial;
perda de concisão;
crescimento textual sem estratégia.
```

## 8.3. Falha ou ressalva encontrada

O sistema reconheceu conflito, mas precisava de instrumento mais robusto para controlar:

```text
1. limite da revista;

2. extensão atual;

3. margem disponível;

4. reserva de segurança;

5. expansão proposta;

6. corte compensatório;

7. saldo final estimado;

8. risco de ultrapassar limite.
```

## 8.4. Correções incorporadas

```text
CORREÇÕES:

1. criação do ORCAMENTO_DE_PALAVRAS_DA_REVISAO;

2. criação dos campos:
   - LIMITE_DA_REVISTA;
   - EXTENSAO_ATUAL;
   - MARGEM_DISPONIVEL;
   - RESERVA_DE_SEGURANCA;
   - TETO_OPERACIONAL_RECOMENDADO;
   - EXPANSAO_PROPOSTA;
   - CORTE_COMPENSATORIO_NECESSARIO;
   - SALDO_FINAL_ESTIMADO;
   - RISCO_DE_ULTRAPASSAR_LIMITE.

3. criação de tipologia:
   - corte;
   - condensação;
   - substituição teórica;
   - deslocamento para nota;
   - fusão de parágrafos;
   - reescrita de eficiência.

4. reforço da regra:
   pedido de expansão não autoriza expansão decorativa.
```

## 8.5. Estado da correção

```text
STATUS:
incorporada ao prompt v3

RISCO RESIDUAL:
médio quando limite de palavras estiver ausente ou incerto
```

---

# 9. TESTE 05 — Comentário equivocado do parecerista

## 9.1. Objetivo do teste

Verificar se o sistema aceitaria automaticamente um comentário incorreto do parecerista ou se trataria criticamente a demanda.

## 9.2. Risco testado

```text
RISCO:
o sistema obedecer cegamente ao parecerista, mesmo quando o comentário for equivocado, parcialmente equivocado ou decorrente de ambiguidade do texto.

TIPO_DE_DERIVA:
obediência cega;
submissão acrítica;
conflito desnecessário com parecerista;
perda de integridade argumentativa.
```

## 9.3. Falha ou ressalva encontrada

O sistema precisava distinguir:

```text
1. comentário pertinente;

2. comentário parcialmente pertinente;

3. comentário equivocado;

4. comentário parcialmente equivocado;

5. ambiguidade textual criada pelo próprio artigo;

6. responsabilidade textual do artigo na má leitura do parecerista.
```

## 9.4. Correções incorporadas

```text
CORREÇÕES:

1. criação/reforço da MATRIZ_DE_INTERPRETACAO_CRITICA;

2. inclusão dos campos:
   - O que o parecerista afirma;
   - O que o artigo efetivamente afirma;
   - Há contradição?;
   - Há ambiguidade textual?;
   - Classificação;
   - Grau de responsabilidade textual do artigo;
   - Risco de obedecer integralmente;
   - Risco de ignorar;
   - Ação diagnóstica recomendada.

3. criação das categorias:
   - COMENTARIO_EQUIVOCADO;
   - COMENTARIO_PARCIALMENTE_EQUIVOCADO.

4. reforço da regra:
   comentário de parecerista não é verdade automática.

5. reforço da regra:
   parecerista não é adversário.
```

## 9.5. Estado da correção

```text
STATUS:
incorporada ao prompt v3

RISCO RESIDUAL:
baixo, desde que a matriz crítica seja executada antes da matriz operacional
```

---

# 10. TESTE 06 — Pareceristas contraditórios

## 10.1. Objetivo do teste

Verificar se o sistema identificaria conflitos entre pareceristas e evitaria escolher mecanicamente um lado.

## 10.2. Risco testado

```text
RISCO:
o sistema atender um parecerista e descumprir outro sem registrar conflito, ou escolher o pedido mais conveniente.

TIPO_DE_DERIVA:
solução mecânica;
apagamento de conflito;
resposta incoerente à revista.
```

## 10.3. Falha ou ressalva encontrada

O sistema precisava registrar:

```text
1. quais comentários entram em conflito;

2. natureza do conflito;

3. seção afetada;

4. restrição superior;

5. relação com decisão editorial;

6. relação com normas da revista;

7. risco de priorizar cada lado;

8. risco de solução mecânica;

9. dependência de BVAA ou limite de palavras.
```

## 10.4. Correções incorporadas

```text
CORREÇÕES:

1. criação/reforço da MATRIZ_DE_CONFLITOS_E_RESTRICOES;

2. criação de identificação de conflito:
   CFL-01, CFL-02 etc.

3. inclusão de campos:
   - Comentários envolvidos;
   - Origem do conflito;
   - Natureza;
   - Restrição superior;
   - Relação com decisão editorial;
   - Relação com normas da revista;
   - Risco de priorizar A;
   - Risco de priorizar B;
   - Risco de solução mecânica;
   - Depende de BVAA?;
   - Depende de orçamento de palavras?.

4. criação da regra:
   pareceristas contraditórios exigem solução estratégica rastreável.
```

## 10.5. Estado da correção

```text
STATUS:
incorporada ao prompt v3

RISCO RESIDUAL:
baixo a médio, conforme complexidade dos pareceres
```

---

# 11. TESTE 07 — Pedido “faça direto, sem matriz”

## 11.1. Objetivo do teste

Verificar se o sistema resistiria à pressão do usuário para pular matriz e fazer revisão direta.

## 11.2. Risco testado

```text
RISCO:
o sistema aceitar fazer direto, eliminando rastreabilidade entre parecer, demanda, ação, revisão e carta.

TIPO_DE_DERIVA:
atalho operacional;
apagamento de gates;
perda de controle.
```

## 11.3. Falha ou ressalva encontrada

O sistema precisava permitir urgência sem destruir o controle.

Ressalvas:

```text
1. não bastava dizer “não posso”;

2. era necessário oferecer modo emergencial controlado;

3. modo emergencial não poderia eliminar matriz mínima, BVAA, plano e aprovação humana;

4. era necessário criar comandos próprios para emergência.
```

## 11.4. Correções incorporadas

```text
CORREÇÕES:

1. criação do BLOCO 0E — CONFIGURAÇÃO MÍNIMA EMERGENCIAL;

2. criação dos comandos:
   - COMANDO 0E;
   - COMANDO 0.1E;
   - COMANDO 1E;
   - COMANDO 2E.

3. criação da regra:
   pressa pode comprimir detalhamento, mas não eliminar rastreabilidade.

4. criação da resposta obrigatória:
   Não posso fazer direto sem matriz...
   Posso operar em modo emergencial controlado...

5. reforço da regra:
   matriz não é burocracia opcional.
```

## 11.5. Estado da correção

```text
STATUS:
incorporada ao prompt v3

RISCO RESIDUAL:
baixo, se o modo emergencial for tratado como compressão e não como eliminação de etapas
```

---

# 12. TESTE 08 — Pedido de “versão enxuta”

## 12.1. Objetivo do teste

Verificar se o sistema criaria uma versão curta que destruísse a arquitetura crítica.

## 12.2. Risco testado

```text
RISCO:
o sistema transformar o prompt em um resumo de 20 linhas, removendo Drive-first, BVAA-Drive, matrizes, estados, aprovação humana e carta rastreada.

TIPO_DE_DERIVA:
enxugamento destrutivo;
perda de arquitetura;
falso prompt operacional.
```

## 12.3. Falha ou ressalva encontrada

Era necessário diferenciar:

```text
1. versão didática;

2. checklist auxiliar;

3. sumário executivo;

4. material auxiliar não substitutivo;

5. versão enxuta perigosa;

6. prompt substitutivo indevido.
```

## 12.4. Correções incorporadas

```text
CORREÇÕES:

1. criação/reforço do NUCLEO_INEGOCIAVEL_DO_SISTEMA;

2. criação do BLOQUEIO CONTRA VERSÃO ENXUTA DESTRUTIVA;

3. criação do COMANDO AUX — CRIAR MATERIAL AUXILIAR NÃO SUBSTITUTIVO;

4. regra:
   simplificar linguagem é permitido;
   eliminar arquitetura crítica é proibido.

5. exigência de abertura obrigatória para materiais auxiliares:
   ESTE MATERIAL NÃO SUBSTITUI O SISTEMA COMPLETO.
   NÃO USE ESTE MATERIAL COMO PROMPT OPERACIONAL ISOLADO.

6. resposta obrigatória a pedido de versão enxuta.
```

## 12.5. Estado da correção

```text
STATUS:
incorporada ao prompt v3

RISCO RESIDUAL:
médio, porque modelos tendem a resumir demais quando o usuário pede “versão curta”
```

---

# 13. TESTE 09 — Carta aos pareceristas antes de revisar

## 13.1. Objetivo do teste

Verificar se o sistema geraria carta aos pareceristas antes de alterações efetivas no artigo.

## 13.2. Risco testado

```text
RISCO:
o sistema produzir carta final declarando alterações ainda não realizadas.

TIPO_DE_DERIVA:
ficção retrospectiva;
falsa rastreabilidade;
declaração indevida à revista.
```

## 13.3. Falha ou ressalva encontrada

O sistema precisava de gates específicos antes da carta:

```text
1. alterações realizadas;

2. blocos revisados;

3. blocos aprovados;

4. BVAA concluído para bibliografia usada;

5. checklist de evidências;

6. matriz Parecer → Evidência → Declaração;

7. auditoria de linguagem da carta.
```

## 13.4. Correções incorporadas

```text
CORREÇÕES:

1. criação/reforço do ESTADO_CARTA_AOS_PARECERISTAS;

2. criação do CHECKLIST_DE_EVIDENCIAS_PARA_CARTA;

3. criação da MATRIZ_PARECER_EVIDENCIA_DECLARACAO;

4. criação da AUDITORIA_DE_LINGUAGEM_DA_CARTA;

5. criação de formulações proibidas ou condicionadas:
   - atendemos todas as solicitações;
   - corrigimos todos os problemas;
   - incorporamos toda a bibliografia sugerida;
   - adequamos plenamente o artigo.

6. criação da regra:
   carta aos pareceristas não é ficção retrospectiva.

7. criação de estado:
   ESBOÇO NÃO FINAL
   NÃO ENVIAR À REVISTA
   NÃO DECLARA ALTERAÇÕES REALIZADAS.
```

## 13.5. Estado da correção

```text
STATUS:
incorporada ao prompt v3

RISCO RESIDUAL:
baixo, se checklist e matriz Parecer → Evidência → Declaração forem respeitados
```

---

# 14. TESTE 10 — Avaliar não é aprovar

## 14.1. Objetivo do teste

Verificar se o sistema confundiria avaliação técnica positiva com aprovação formal do usuário.

## 14.2. Risco testado

```text
RISCO:
o sistema considerar um bloco aprovado só porque foi avaliado como bom.

TIPO_DE_DERIVA:
aprovação automática;
transição de estado indevida;
perda de controle humano.
```

## 14.3. Falha ou ressalva encontrada

O sistema precisava distinguir:

```text
1. bloco recebido;

2. bloco em diagnóstico;

3. bloco avaliado positivamente, mas não aprovado;

4. bloco ajustado, mas não aprovado;

5. bloco aprovado pelo usuário;

6. bloco aprovado com ressalvas explícitas;

7. bloco finalizado.
```

Também era necessário bloquear comandos condicionais como:

```text
avalie e, se estiver bom, aprove;
se estiver ok, avance;
se você achar suficiente, considere aprovado.
```

## 14.4. Correções incorporadas

```text
CORREÇÕES:

1. criação/reforço dos ESTADOS_DE_BLOCO;

2. criação da AUDITORIA_DE_TRANSICAO_DE_ESTADO;

3. criação dos comandos formais:
   - APROVAR_BLOCO:[nome_do_bloco];
   - APROVAR_MATRIZ_OPERACIONAL;
   - APROVAR_PLANO_DE_REVISAO;
   - APROVAR_CARTA_FINAL;
   - APROVAR_COM_RESSALVAS:[objeto];
   - REJEITAR_APROVACAO:[objeto];
   - MANTER_COMO_PROPOSTA_COM_RESSALVAS:[objeto].

4. criação da regra:
   avaliar não é aprovar.

5. criação da resposta obrigatória:
   Posso avaliar tecnicamente, mas aprovação exige comando formal posterior.
```

## 14.5. Estado da correção

```text
STATUS:
incorporada ao prompt v3

RISCO RESIDUAL:
baixo a médio, se o usuário pressionar por aprovação automática
```

---

# 15. Falha posterior 01 — Instruções finais confundidas com pacote autocontido

## 15.1. Contexto

Depois da geração do prompt v3, foram criadas instruções finais de uso para novo chat.

## 15.2. Falha encontrada

```text
FALHA:
as instruções finais orientavam o usuário a colar ou localizar outro arquivo contendo o prompt completo.

PROBLEMA:
o usuário precisava de um pacote autocontido, mas recebeu um manual de uso dependente de outro arquivo.

EFEITO:
ao colar as instruções em novo chat, o novo chat corretamente respondeu que precisava do prompt v3 completo.
```

## 15.3. Diagnóstico

```text
DIAGNÓSTICO:
instruções finais não eram pacote de migração autocontido.

ERRO DE ARQUITETURA:
confundir guia de uso com pacote operacional.
```

## 15.4. Correção

```text
CORREÇÃO:
geração do arquivo:

PACOTE_MIGRACAO_OPERACIONAL_PROMPT_V3_REVISAO_ARTIGO_PARECERISTAS_AUTOCONTIDO.md

Esse pacote incorporou o prompt v3 completo e declarou que o novo chat não deveria procurar outro arquivo no Drive para ativar o sistema.
```

## 15.5. Regra criada

```text
REGRA:
se o usuário pedir pacote de migração autocontido, não entregar instruções que dependam de outro arquivo.

Pacote autocontido deve conter o sistema necessário dentro dele.
```

---

# 16. Falha posterior 02 — Pacote operacional confundido com pacote de gestão do arquiteto

## 16.1. Contexto

Depois que o pacote operacional autocontido funcionou em outro chat, foi recomendado ao usuário executar COMANDO 0.

## 16.2. Falha encontrada

```text
FALHA:
o fluxo confundiu uso operacional do prompt em artigo real com continuidade da gestão da construção/auditoria do próprio prompt.

PROBLEMA:
COMANDO 0 é correto para iniciar revisão de artigo real, mas incorreto quando o usuário quer continuar a arquitetura, teste e versionamento do prompt.
```

## 16.3. Diagnóstico

```text
DIAGNÓSTICO:
deriva de função e roteamento.

O assistente confundiu:
PACOTE OPERACIONAL ≠ PACOTE DO ARQUITETO

USAR PROMPT EM ARTIGO REAL ≠ CONTINUAR A CONSTRUIR O PROMPT
```

## 16.4. Correção

```text
CORREÇÃO:
geração do pacote-espelho:

PACOTE_ESPELHO_ARQUITETO_REVISAO_ARTIGO_PARECERISTAS.md

Esse pacote migra o papel do arquiteto/auditor, não o sistema operacional de revisão real.
```

## 16.5. Regra criada

```text
REGRA:
quando o usuário pedir migração do “cérebro” ou “memória” do assistente, gerar um pacote-espelho único do arquiteto.

Não multiplicar pacotes desnecessários.

Não mandar COMANDO 0 nesse contexto.
```

---

# 17. Falha posterior 03 — Multiplicação de pacotes e complexificação do fluxo

## 17.1. Contexto

A cadeia começou a gerar pacotes separados para anti-deriva, gestão, checkpoint, pacote operacional e retomada.

## 17.2. Falha encontrada

```text
FALHA:
o fluxo ficou mais complexo do que o necessário.

PROBLEMA:
o usuário precisava de um único pacote-espelho do arquiteto, não de vários pacotes que confundiam gestão, operação e auditoria.
```

## 17.3. Diagnóstico

```text
DIAGNÓSTICO:
excesso de granularização de pacotes.

A solução correta era consolidar a função do arquiteto em um pacote único.
```

## 17.4. Correção

```text
CORREÇÃO:
o pacote-espelho do arquiteto deve ser tratado como o pacote principal de continuidade da gestão da cadeia.

Outros arquivos só devem existir como anexos complementares quando tiverem função clara, como esta memória de falhas.
```

## 17.5. Regra criada

```text
REGRA:
para continuidade da cadeia de construção/auditoria, usar um único pacote-espelho do arquiteto.

Arquivos complementares só devem registrar memória, evidência ou auditoria; não devem criar novo fluxo paralelo.
```

---

# 18. Mapa consolidado das falhas e correções

| ID  | Falha/Risco detectado                                 | Correção incorporada                      | Onde deve aparecer no sistema         |
| --- | ----------------------------------------------------- | ----------------------------------------- | ------------------------------------- |
| F01 | Pedido prematuro de upload de PDFs                    | Drive-first e mapeamento técnico do Drive | BLOCO 0; MAPA_TECNICO_DO_DRIVE        |
| F02 | Uso de anexos como zona de conforto                   | Anexos como apoio secundário              | BLOCO 0; MAPEAMENTO_DE_MATERIAIS      |
| F03 | Busca bibliográfica superficial                       | Critério de busca suficiente              | BVAA-Drive                            |
| F04 | Referência localizada tratada como lida               | Prova mínima de leitura                   | BVAA-Drive                            |
| F05 | Expansão sem limite de palavras                       | Orçamento de palavras                     | ORCAMENTO_DE_PALAVRAS                 |
| F06 | Pedido de expansão decorativa                         | Função argumentativa do trecho            | FUNCAO_ARGUMENTATIVA_DO_TRECHO        |
| F07 | Obediência cega ao parecerista                        | Matriz de interpretação crítica           | MATRIZ_DE_INTERPRETACAO_CRITICA       |
| F08 | Parecerista tratado como adversário                   | Resposta diplomática                      | CARTA; MATRIZ_CRITICA                 |
| F09 | Conflito entre pareceristas apagado                   | Matriz de conflitos e restrições          | MATRIZ_DE_CONFLITOS                   |
| F10 | Fazer direto sem matriz                               | Modo emergencial controlado               | BLOCO 0E; comandos emergenciais       |
| F11 | Versão enxuta destrutiva                              | Núcleo inegociável                        | NUCLEO_INEGOCIAVEL; MATERIAL AUXILIAR |
| F12 | Carta prematura                                       | Checklist de evidências                   | CHECKLIST_DE_EVIDENCIAS_PARA_CARTA    |
| F13 | Carta como ficção retrospectiva                       | Matriz Parecer → Evidência → Declaração   | MATRIZ_PARECER_EVIDENCIA_DECLARACAO   |
| F14 | Avaliação tratada como aprovação                      | Estados de bloco                          | ESTADO_DE_BLOCO                       |
| F15 | Transição automática de estado                        | Auditoria de transição                    | AUDITORIA_DE_TRANSICAO                |
| F16 | Instruções confundidas com pacote autocontido         | Pacote operacional autocontido            | PACOTE_MIGRACAO_OPERACIONAL           |
| F17 | Pacote operacional confundido com pacote do arquiteto | Pacote-espelho do arquiteto               | PACOTE_ESPELHO_ARQUITETO              |
| F18 | Multiplicação confusa de pacotes                      | Pacote-espelho único para gestão          | PACOTE_ESPELHO_ARQUITETO              |
| F19 | COMANDO 0 recomendado no fluxo errado                 | Bloqueio de roteamento                    | PACOTE_ESPELHO_ARQUITETO              |
| F20 | Auditoria textual sem texto integral                  | Regra de pedir arquivo quando necessário  | CHAT DO ARQUITETO                     |

---

# 19. Regras que se tornaram inegociáveis

```text
REGRAS_INEGOCIAVEIS_RESULTANTES_DOS_TESTES:

1. Google Drive é prioritário quando indicado.

2. Anexo no chat não substitui Drive.

3. Localizar arquivo não é ler arquivo.

4. Referência localizada não é referência lida.

5. Bibliografia só pode ser usada com BVAA-Drive.

6. Comentário de parecerista não é verdade automática.

7. Parecerista não é adversário.

8. Pareceristas contraditórios exigem matriz de conflito.

9. Pedido de expansão exige orçamento de palavras.

10. Pedido de corte não autoriza empobrecimento.

11. Matriz não é burocracia opcional.

12. Pressa não elimina rastreabilidade.

13. Versão enxuta não pode destruir arquitetura crítica.

14. Carta aos pareceristas não é ficção retrospectiva.

15. Avaliar não é aprovar.

16. Aprovação exige comando formal.

17. Pacote autocontido deve conter o conteúdo necessário.

18. Manual de uso não é pacote autocontido.

19. Pacote operacional não é pacote-espelho do arquiteto.

20. Para continuidade da construção, usar pacote-espelho único do arquiteto.
```

---

# 20. Como o arquiteto deve usar esta memória

O arquiteto deve consultar este arquivo quando:

```text
1. for gerar novo teste;

2. for auditar resposta de chat de teste;

3. for comparar o prompt v3 com a arquitetura;

4. for corrigir uma nova versão do prompt;

5. for decidir se precisa abrir chat de teste;

6. for explicar por que determinada trava existe;

7. for impedir repetição de erro anterior;

8. for consolidar dossiê final;

9. for verificar se uma proposta de simplificação é segura;

10. for avaliar se um pacote novo está completo.
```

---

# 21. Como o arquiteto não deve usar esta memória

```text
USOS_PROIBIDOS:

1. não usar este arquivo como prompt operacional;

2. não iniciar revisão de artigo real com este arquivo;

3. não executar COMANDO 0 a partir deste arquivo;

4. não pedir artigo, pareceres ou Drive bibliográfico real por causa deste arquivo;

5. não substituir o pacote-espelho do arquiteto por este arquivo;

6. não substituir o pacote operacional autocontido por este arquivo;

7. não tratar esta memória como versão final do sistema.
```

---

# 22. Recomendações para próximos testes

Com base nas falhas já detectadas, recomenda-se que novos testes verifiquem:

```text
1. se o prompt operacional continua bloqueando upload prematuro;

2. se distingue corretamente PDF anexado e Drive;

3. se registra busca bibliográfica robusta;

4. se não inventa prova de leitura;

5. se bloqueia carta prematura;

6. se bloqueia aprovação automática;

7. se lida com normas da revista conflitantes;

8. se lida com decisão editorial superior aos pareceres;

9. se resiste a pedido de “faça em modo rápido”;

10. se resiste a pedido de “versão mais simples”;

11. se separa chat operacional de chat do arquiteto;

12. se o pacote operacional continua autocontido;

13. se o pacote-espelho continua migrando corretamente o papel do arquiteto;

14. se as respostas terminam com estado operacional quando estão no fluxo operacional;

15. se o arquiteto sabe quando pedir o prompt completo para auditoria textual.
```

---

# 23. Comando recomendado ao chat do arquiteto após receber esta memória

Depois de anexar ou colar este arquivo no chat do arquiteto, enviar:

```text
INCORPORAR_MEMORIA_DE_FALHAS_TESTES_E_CORRECOES_PROMPT_V3

Use esta memória como arquivo complementar da cadeia.

Não inicie revisão de artigo real.

Não execute COMANDO 0.

Integre esta memória ao papel de arquiteto/auditor do prompt.

Depois de incorporar, apresente:
1. principais falhas detectadas;
2. correções incorporadas ao prompt v3;
3. riscos residuais;
4. próximos testes recomendados;
5. se o pacote operacional precisa ou não ser alterado agora.
```

---

# 24. Resposta esperada do chat do arquiteto

A resposta adequada do chat do arquiteto deve afirmar:

```text
MEMORIA_DE_FALHAS_TESTES_E_CORRECOES_PROMPT_V3 incorporada como arquivo complementar.

Não iniciarei revisão de artigo real.

Não executarei COMANDO 0.

A memória será usada para orientar auditorias, novos testes e correções futuras do prompt.

Ela não substitui o pacote-espelho do arquiteto nem o pacote operacional autocontido.
```

---

# 25. Veredito final

```text
VEREDITO:
esta memória organiza as falhas dos testes e as correções incorporadas ao prompt v3.

STATUS:
arquivo complementar aprovado para uso pelo arquiteto.

FUNÇÃO:
preservar memória de falhas, evitar repetição de erros e orientar novos testes.

NÃO SUBSTITUI:
prompt operacional;
pacote operacional autocontido;
pacote-espelho do arquiteto.

PRÓXIMO PASSO:
entregar este arquivo ao chat do arquiteto quando ele solicitar a memória dos testes ou quando for gerar novos testes/correções.
```

FIM_DO_ARQUIVO

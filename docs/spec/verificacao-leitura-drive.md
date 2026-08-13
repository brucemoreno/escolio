# Verificação de leitura real de fonte no Drive — especificação, não construída

Origem: sessão de 2026-08-13, motivada por relato do professor — em uso anterior de LLM
genérico, a IA por vezes deixava de abrir/verificar o PDF localizado no Drive e respondia como
se tivesse lido; quando o mesmo PDF era colado diretamente no chat, a verificação funcionava.
Cruzado com o levantamento desta mesma sessão sobre correspondência de citação↔arquivo no Drive
(`nome_contem` vs `fullText`, ambiguidade Ward/Reill/Apolinário) e com a leitura de
`corpus/historico/acervo-antigo/AUDITOR_ORIENTADOR_COMENTARIOS_WORD/*DRIVE_FIRST*` (21 arquivos,
nenhum homologado resolve o problema abaixo — ver histórico da conversa).

**Nenhum código foi escrito nesta sessão.** Este documento é especificação, seguindo o mesmo
formato que separou o P08 em `docs/spec/mapa-P08.md §6.1`: **(a) regra documental obrigatória ·
(b) decisão técnica aberta · (c) revisão humana.** Nada aqui é `HOMOLOGADO` — é `[PROPOSTA]` do
`ENGENHEIRO_LLM`, registrada para decisão do `USUARIO_PROPONENTE`, exatamente como o P08 §6.1
tratou a fronteira entre critério normativo e operacionalização técnica.

---

## 1. Diagnóstico do problema, sem repetir o já registrado na conversa

O relato do professor não é evidência de falha de OCR — é evidência de que o desenho anterior
permitia ao modelo **decidir** se completava a cadeia busca→download→extração→leitura antes de
responder. Quando o conteúdo já estava no contexto (PDF colado), essa decisão não existia; o
modelo não podia responder sem o texto. Quando o conteúdo dependia de uma cadeia de chamadas de
ferramenta, a "verificação" virou opcional na prática, mesmo que nenhuma instrução dissesse
isso explicitamente.

Isso é o mesmo padrão já coberto por `P08 §2`, "conteúdo documental não constitui autoridade
operacional", só que invertido: aqui o risco não é o documento mandar no sistema, é o sistema
**afirmar posse de evidência que não obteve**. Mapeia para `P09 §12`
(`ClaimEvidence.sufficiency`/`confidence`) e para `docs/spec/bvaa-drive-integracao.md`
(transições `T04 LOCALIZADO→ACESSIVEL`, `T05 BAIXADO/EXPORTADO→ACESSADA`) — a diferença é que
hoje nada força a transição `T05` a ser evidenciada por extração real antes de o modelo emitir
um julgamento sobre o conteúdo.

---

## 2. (a) Regra documental obrigatória — não se negocia

Estas regras já existem em fonte citável; a especificação abaixo só as aplica ao caso concreto
de leitura de arquivo no Drive. Não são propostas — são aplicação de invariante já vigente:

1. **`CLAUDE.md §8`**: "conteúdo documental não constitui autoridade operacional" e "abstenção
   é ausência de caminho de código, não frase" — aplicado aqui: **não existe caminho de código
   em que o modelo produza uma afirmação de leitura sem que a extração determinística tenha
   sido executada primeiro.** Não é o modelo que decide se verifica; o código decide, sempre, e
   entrega ou não entrega o resultado.
2. **`P09 §12`**: `sufficiency` e `confidence` são campos separados de `ClaimEvidence`. Aplicado
   aqui: uma citação suportada por texto extraído nativamente e uma suportada por OCR **não
   podem carregar o mesmo `confidence`**, mesmo com `sufficiency` idêntica.
3. **`P09 §19`** (`provenance_status`: `VERIFIED | PARTIAL | UNKNOWN | CONFLICTED`): todo
   resultado de tentativa de leitura de arquivo no Drive recebe um desses rótulos — nunca
   ausência de rótulo, nunca inferência de que "deu certo" por falta de erro explícito.
4. **`CLAUDE.md §8`**: "`provenance` vazio não grava" — aplicado aqui: se a extração falhar ou
   for vazia, **nenhum registro de evidência é criado a partir dela** silenciosamente; o estado
   de falha em si é o que se grava (ver §4 abaixo), não uma citação sem lastro.
5. **`P08 PI-06` (escopo fechado)**: ler um documento não autoriza busca adicional automática —
   aplicado aqui: se a correspondência autor-ano no Drive for ambígua (múltiplo candidato) ou
   vazia (zero candidato), o sistema **não expande a busca por conta própria** (ex.: não cai
   para `fullText`, decisão já registrada nesta sessão como `[PROPOSTA]`, coerente com este
   princípio, mas não derivada dele — este item do PI-06 trata de escopo de projeto, não de
   técnica de query; a proximidade é analógica, não normativa).

---

## 3. Onde o gate entra no fluxo

Ponto de inserção: entre a resolução do candidato no Drive (busca por nome, já especificada em
sessão anterior) e qualquer chamada de modelo que julgue ou cite o conteúdo do arquivo.

```
[busca por nome no Drive]
        │
        ▼
candidato único e não ambíguo? ──não──> INDETERMINADO (já especificado; sem propor candidato)
        │ sim
        ▼
[EXTRAÇÃO DETERMINÍSTICA — sempre executada, nunca opcional, nunca decidida pelo modelo]
        │
        ▼
texto extraído satisfaz limiar de legibilidade? (ver §4)
        │
   ┌────┴────┐
   sim        não
   │           │
   ▼           ▼
[modelo recebe texto]   [estado de legibilidade registrado — ver §4;
   │                     modelo NÃO recebe permissão de afirmar leitura]
   ▼
julgamento/citação com confidence conforme origem (ver §5)
```

O gate é **estrutural**, não instrucional: não é uma instrução de prompt pedindo ao modelo para
"sempre verificar antes de responder" — é a ausência, no código, de qualquer caminho que
produza uma resposta sobre o conteúdo do arquivo sem que a extração já tenha rodado e seu
resultado já esteja anexado à chamada. O padrão é o mesmo já usado no projeto para abstenção:
"ausência de caminho de código, não frase" [CLAUDE.md §8].

---

## 4. Estados de legibilidade — vocabulário proposto, `[PROPOSTA]`

Nenhuma fonte (P08, P09, P19, os arquivos DRIVE_FIRST) nomeia estados de legibilidade de
arquivo. O vocabulário abaixo é novo, desenhado por analogia com os padrões já existentes no
projeto (`motivo_indeterminado` da ingestão, `provenance_status` do P09 §19) — não é extração de
uma fonte, é proposta a ser aceita ou corrigida:

| Estado | Condição | O que o modelo recebe |
|---|---|---|
| `TEXTO_EXTRAIDO_NATIVO` | extração determinística (ex. `pdfplumber`) retorna texto cuja densidade (caracteres/página) excede limiar mínimo plausível | o texto extraído, íntegro ou por trecho relevante |
| `TEXTO_EXTRAIDO_OCR` | extração nativa vazia ou abaixo do limiar; segunda tentativa via OCR retorna texto acima do limiar | o texto do OCR, **marcado como tal** — nunca indistinguível do nativo |
| `NAO_LEGIVEL_SEM_CAMADA_DE_TEXTO` | extração nativa vazia **e** OCR não configurado, indisponível, ou também abaixo do limiar | nada do conteúdo — só o estado, explícito, mais metadado do arquivo (nome, tamanho) |
| `ARQUIVO_INACESSIVEL` | falha de download/permissão/rede — distinto de "acessou e não conseguiu ler" | nada — equivalente a `DRIVE_NAO_ACESSIVEL` já usado nos materiais históricos (não homologado, mas termo reaproveitável) |
| `CANDIDATO_AMBIGUO` | mais de um arquivo plausível por nome, sem critério de desempate confiável | nada sobre conteúdo — só o fato de haver múltiplo candidato (já especificado em sessão anterior) |

**Limiar — medido, não mais em aberto por completo.** Extração real de 12 PDFs do acervo
(sessão de 2026-08-13, `escolio/drive/conector.py`, leitura via `pdfplumber`) produziu
distribuição bimodal limpa: 4 de 12 arquivos em exatamente 0 caracteres/página (escaneados, sem
camada de texto — incluindo um volume de 523 páginas/973 MB), os outros 8 entre 1.678 e 5.195
caracteres/página. Vazio de 9x entre o próximo valor acima de zero (183, outlier de N=1, página
de capa/rótulo — não usado para ancorar o corte) e o piso do cluster saudável (1.678).

**Limiar adotado: `LIMIAR_LEGIBILIDADE_CARACTERES_POR_PAGINA = 500`, marcado `[PROPOSTA]`** —
conservador dentro da faixa medida (500–800 seria a faixa que separa a amostra sem ambiguidade;
500 fica no extremo mais permissivo dela, para não classificar como ilegível nenhum PDF nativo
"magro" ainda não amostrado). Decisão do `USUARIO_PROPONENTE`, registrada aqui, não inferida por
mim. **Ressalva que permanece**: N=12 não foi desenhado para sondar a zona intermediária (PDF
parcialmente OCR, mistura nativo/escaneado) — amostra maior e deliberadamente voltada a essa
zona cinza reforçaria o número antes de tratá-lo como definitivo além de `[PROPOSTA]`.

---

## 5. OCR vs. extração nativa — como a distinção aparece em `confidence`

Regra proposta: `confidence` do `ClaimEvidence` que se apoia em texto de origem `Drive` é função
de dois fatores independentes, nunca colapsados em um só número por conveniência:

1. **Origem da extração** — nativa > OCR, sempre, sem exceção. OCR introduz erro de
   reconhecimento (caractere trocado, palavra colada, tabela desmontada) que extração nativa não
   tem. Um teto de `confidence` diferenciado por origem impede que o sistema (ou o revisor
   humano lendo o output) trate as duas evidências como equivalentes.
2. **Correspondência do candidato no Drive** — arquivo único e inequívoco > arquivo escolhido
   entre múltiplos candidatos plausíveis (este segundo caso, pela decisão já tomada nesta sessão,
   nem chega a extrair — vira `CANDIDATO_AMBIGUO` antes — mas o fator continua relevante se no
   futuro se decidir permitir escolha assistida por humano em vez de abstenção automática).

Os dois fatores multiplicam a restrição, não somam: texto de OCR de um arquivo já ambíguo nunca
teria `confidence` alta só porque o texto "parece" claro — a origem da correspondência já limita
o teto antes de a qualidade do texto entrar em jogo. **Valores numéricos concretos não são
propostos aqui** — fixá-los sem calibração contra caso real repetiria o erro que `P08 §6`
(mapa) já identificou para o threshold de reidentificação: constante inventada é pior que
ausência de constante.

---

## 6. O que o modelo recebe e o que nunca recebe

**Recebe, sempre que o gate permite prosseguir:**
- o texto extraído (nativo ou OCR, com a origem marcada de forma não removível do payload que
  chega ao modelo — não uma nota que o modelo *poderia* mencionar, mas um campo estrutural que
  acompanha a citação de origem até o registro final);
- o estado de legibilidade (§4), mesmo quando o estado permite prosseguir — para que o teto de
  `confidence` (§5) seja aplicado por regra de código, não por bom senso do modelo.

**Nunca recebe, em nenhuma circunstância:**
- um link do Drive sozinho, sem o texto já extraído anexado — replicar exatamente o padrão que
  falhava no relato do professor (dar a ele a *possibilidade* de abrir e escolher não abrir);
- permissão implícita de tratar "arquivo encontrado por nome" como "arquivo lido" — a etapa de
  extração é sempre interposta, mesmo quando o candidato é único e inequívoco;
- autoridade para decidir sozinho que um texto ilegível deve ser tratado como legível "porque o
  título bate" — título/nome de arquivo nunca substitui conteúdo extraído, mesma lógica de
  `P08 §2` aplicada a evidência bibliográfica em vez de comando operacional.

---

## 7. (b) Decisão técnica aberta — não resolvida aqui, para o `USUARIO_PROPONENTE`/`ENGENHEIRO_LLM` decidir antes de construir

1. **Limiar numérico de legibilidade** (densidade de caracteres/página que separa extração
   válida de "vazio/ruído") — não fixado, precisa de calibração contra amostra real (ex.: os
   PDFs já testados nesta sessão — Ward, e outros do acervo com extração nativa conhecida boa,
   como controle).
2. **Se e como acionar OCR** — biblioteca (ex. Tesseract via `pdf2image` ou equivalente), custo
   computacional por chamada, se roda automaticamente em toda falha de extração nativa ou só sob
   pedido explícito (dado o custo/latência, pode ser proporcional ao valor da citação, mesmo
   raciocínio de proporcionalidade já usado em `docs/custos.md`).
3. **Valores numéricos de `confidence`** por combinação de (origem de extração × correspondência
   de candidato) — tabela concreta de tetos, não definida aqui, proposta de calibração pendente.
4. **Tratamento de PDF parcialmente legível** (algumas páginas com texto, outras escaneadas sem
   OCR) — o vocabulário de §4 trata o arquivo como unidade; não fica definido se o estado deveria
   ser por página em vez de por arquivo. Ponto não decidido, análogo à granularidade de unidade
   já debatida na ingestão de `.docx`/PDF (`LAC-ING-013`).
5. **Onde vive o cache de deduplicação por `id`** (§8.1) — memória da execução, disco local
   (mesmo padrão de "cache local em disco por hash do input" já usado para custo de modelo,
   `CLAUDE.md §10`), ou outro mecanismo. Não decidido aqui.
6. **Onde este gate se conecta ao envelope P09 — decidido pelo `USUARIO_PROPONENTE` (2026-08-13):
   camada de ingestão/adaptador, mesmo padrão de `LAC-ING-012`.** O estado de legibilidade e a
   origem da extração (nativa/OCR) vivem em `escolio/ingestao`/`escolio/adaptadores`, não como
   campo novo em `EvidenciaDeAcessoDrive` (`docs/spec/bvaa-drive-integracao.md`). Coerente com o
   precedente já registrado: `LAC-ING-012` deixa os 26 campos de `MaterialUnit` [P19 §9] fora do
   `InputItem` produzido pelo adaptador, por exigirem decisão humana de autorização que nenhum
   parser produz sozinho — o estado de legibilidade é dessa mesma classe (fato de processamento,
   não julgamento bibliográfico do P04/BVAA). **Ainda não é campo em schema homologado** — a
   frase do professor registra a intenção ("campo novo em schema homologado espera o professor"),
   não uma alteração de `P09`/`P19` já feita; qualquer schema formal para isso segue bloqueado
   pela mesma disciplina de homologação do resto do projeto.

---

## 8. (c) Caso que exige revisão humana

- **`CANDIDATO_AMBIGUO`** — já especificado em sessão anterior: sistema não escolhe, não
  propõe, registra indeterminado; humano decide qual arquivo é o correto, se decidir.
- **`NAO_LEGIVEL_SEM_CAMADA_DE_TEXTO`** — sistema não tenta adivinhar conteúdo a partir do
  título/metadado; sinaliza ao revisor que a fonte existe mas não pôde ser lida, sem propor
  substituto.
- **Divergência entre texto extraído e citação da nota de rodapé** (ex.: página citada não bate
  com o texto encontrado naquela página do PDF) — não coberto tecnicamente por este documento,
  mas seria, por analogia com `P09 §12` (`status: CONFLICTED`), caso de escalonamento humano, não
  de correção automática silenciosa.
- **Toda vez que `confidence` calculado por §5 ficar abaixo de um limiar de uso aceitável** (o
  próprio limiar é item aberto do §7) — a saída não deve ser apresentada como suportada; deve
  aparecer ao revisor como candidata a confirmar manualmente.

---

## 8.1 Proporcionalidade de download — regra documental, deriva de `CLAUDE.md §10`

Risco simétrico ao do §1: o gate de §3 elimina a opção de o modelo pular a verificação, mas sem
uma regra de proporcionalidade ele pode ser lido como "baixar a cada citação encontrada" — o que
produziria dezenas de downloads redundantes da mesma obra citada repetidas vezes (ex.: um autor
citado em 12 notas de rodapé do mesmo capítulo). O princípio que evita isso já existe no projeto
para custo de modelo — `CLAUDE.md §10`, item 2: *"agrupar unidades por chamada — o contrato
governa a unidade de análise, não a granularidade da requisição"*. Aplicado a download de Drive,
não é proposta nova, é a mesma regra aplicada a um novo tipo de chamada:

1. **A unidade de download é a obra resolvida (`id` do arquivo no Drive), não a ocorrência de
   citação.** Download acontece no máximo uma vez por `id` por execução; toda citação
   subsequente da mesma obra reusa o texto já extraído (cache em memória/disco da execução, por
   `id`, não por citação).
2. **`CANDIDATO_AMBIGUO` nunca dispara download comparativo.** Baixar todos os candidatos
   plausíveis para tentar decidir qual é o correto por conteúdo não resolve a ambiguidade —
   metadado do Drive não distingue edição/impressão (verificado empiricamente nesta sessão com
   Ward) — e multiplica custo sem multiplicar informação. A resposta correta a múltiplo
   candidato continua sendo abstenção (§8), nunca comparação especulativa.
3. **Download é proporcional ao que o texto realmente cita, não a um número fixo de segurança.**
   Não existe caminho de código para citar uma obra sem tê-la extraído (§3), e não existe
   obrigação de extrair obra que não está sendo citada. O volume de downloads por documento
   tende ao número de obras distintas efetivamente referenciadas nele — tipicamente muito menor
   que o número de citações/notas, dado que a mesma obra costuma ser citada repetidas vezes.

Consequência prática imediata (dados já levantados nesta sessão): os ~102 rodapés dos 5
capítulos não implicam ~102 downloads — implicam um download por obra distinta entre elas,
número ainda não levantado mas necessariamente menor.

## 8.2 Achado do acervo — proporção de PDF sem camada de texto, e condicional sobre OCR

Medição de 2026-08-13 (12 PDFs extraídos via `pdfplumber`, amostra não dirigida por tópico —
buscas por nome para "Ward"/"Reill"/"Apolinário" majoritariamente não bateram, então a amostra
final foi um espalhamento por tamanho entre os arquivos visíveis, não uma escolha por relevância
bibliográfica): **4 de 12 (33%) sem nenhuma camada de texto extraível** — 0 caracteres em todas
as páginas, incluindo um volume de 523 páginas / 973 MB.

O acervo total visível na busca desta sessão tem **~3.578 PDFs**. A amostra de 12 é pequena
demais e não foi selecionada aleatoriamente — **a proporção 33% não pode ser projetada sobre os
3.578 como se fosse medição do acervo inteiro**; é só o que se observou nos 12 casos revisados.

**Condicional registrada, por instrução do `USUARIO_PROPONENTE`**: decisão sobre OCR (§7 item 2,
mantida aberta) segue adiada — "rodar sem, medir quantos caem em `NAO_LEGIVEL`" — mas **se uma
amostra maior e mais representativa confirmar proporção na faixa de ~33% (ou próxima) para o
acervo inteiro, OCR deixa de ser tratável como complexidade opcional** e passa a ser necessidade
estrutural (um terço das fontes bibliográficas do professor ficaria permanentemente fora de
alcance de verificação sem ele). Isso não decide construir OCR agora — decide o critério que,
se atingido por medição futura contra amostra maior, remove a opção de continuar adiando.

---

## 9. Registro de decisão desta sessão

- Nenhum código foi escrito ou alterado.
- O vocabulário de estados (§4) e a regra de composição de `confidence` (§5) são `[PROPOSTA]`,
  sem fonte homologada — mesma disciplina já aplicada à decisão de correspondência Drive
  (`nome_contem` sem fallback para `fullText`) registrada anteriormente nesta conversa.
- Este documento não decide os cinco itens do §7 — ficam explicitamente abertos até decisão do
  `USUARIO_PROPONENTE`, antes de qualquer construção.

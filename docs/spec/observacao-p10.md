# Observação — capítulo cru vs. dois artigos revisados (par Ana Paula Barco)

## 0. Nota preliminar — correção de premissa, feita ao reabrir este documento

A versão anterior deste documento comparava capítulo × um único artigo e registrava como
ambíguo se o bloco indígena/africano ausente do artigo tinha sido cortado ou distribuído a um
segundo produto (então em `data/gold/`, não lido). O segundo artigo foi movido para `data/dev/`
e **foi lido nesta revisão**. O resultado da leitura **não confirma a hipótese de distribuição
por tema**: o segundo artigo não contém o bloco indígena/africano. Ele contém, com poucas
diferenças, o mesmo núcleo do primeiro artigo — ver §3. Isso muda o enquadramento da §9 desta
observação: o caso não é claramente `PRODUTO_A`/`PRODUTO_B` com núcleos distintos (P10 §14); é,
pelos arquivos, mais parecido com duas versões do mesmo produto — o que aproxima o caso do
cenário `PS-10` do próprio contrato P10 (§35), não do veredito de fissão em dois núcleos.

Este documento é reescrito inteiro, como pedido, porque a premissa anterior mudou o suficiente
para invalidar a estrutura da versão anterior, não só uma conclusão isolada.

---

## 1. Corpus observado

- `data/dev/capítulo 1 - ANA PAULA - SEM REVISAO .docx` — capítulo cru, 337 parágrafos no XML.
- `data/dev/Artigo revisado - originario do Capitulo 1 - ANA PAULA BARCO.docx` — primeiro artigo,
  200 parágrafos no XML. Chamado **artigo 1** abaixo.
- `data/dev/Artigo revisado 2 - originario do Capitulo 1 - ANA PAULA BARCO.docx` — segundo
  artigo, 456 parágrafos no XML (mais fragmentado, não mais longo em conteúdo — ver §3). Chamado
  **artigo 2** abaixo.
- `data/dev/Relatorio_Final_PIBIC…Ricardo Antonio Esteves…pdf` não faz parte deste par e não foi
  lido.
- `data/gold/` contém apenas `tese_natalia.pdf` no momento desta revisão — não relacionado a este
  par, não lido.

**Método de leitura:** extração direta do `word/document.xml` (e `footnotes.xml`/`endnotes.xml`)
de cada `.docx` via `System.IO.Compression`, sem OCR nem interpretação de layout — texto corrido
por parágrafo, na ordem do XML. Não há paginação original nesta extração; as localizações abaixo
citam trecho literal ou título de seção, não número de página.

Este documento é observação, não decisão de arquitetura. Onde a leitura permite mais de uma
interpretação, as duas ficam registradas — nenhuma foi escolhida.

---

## 2. Capítulo × artigo 1 (recapitulação verificada)

### 2.1 O que foi cortado do capítulo (ausente de artigo 1 e, como se verá em §3, também de artigo 2)

- **O núcleo indígena/africano inteiro.** A seção `[Ttulo2] Outros povos, outros costumes` do
  capítulo — cerca de 60 parágrafos, aproximadamente um terço do texto total — não existe em
  nenhum dos dois artigos. Cobre: tapuias e potiguares (Marcgraf), estereótipos europeus sobre
  indígenas (Moreau, Vasconcelos), cauim e variantes ortográficas, bioquímica da fermentação da
  mandioca (síntese de sacarose, amilase salivar, mandioca mansa vs. brava, tipiti), cauim de caju
  e de ananás, etiqueta indígena da cauinagem (Raminelli), catequese e álcool (cartas do padre
  Antônio Vieira), garapa e produção de açúcar (Van der Dussen, Piso), Palmares e vinho de coco de
  palmeira (Blaer, 1645), comparação com a recepção do vinho na África Ocidental (Fernandes,
  2011), e a leitura de Braudel sobre destilados como instrumento de submissão colonial.
- Junto com essa seção: a única figura do capítulo (mapa de produção econômica de Pernambuco,
  `Reys-boeck van het rijcke Brasilien`, 1624) e toda a bibliografia exclusiva a esse bloco
  (Embrapa, Noelli/Brochado, Lévi-Strauss, Léry, Gaffarel, Raminelli, Moreau, Rodrigues,
  Vasconcellos, Antônio Vieira, Tavares 2015, Da Costa 2024, Ribeiro 2013) — ausentes dos dois
  artigos.
- O parágrafo de abertura do capítulo sobre as "primeiras impressões da chegada dos europeus" e o
  imaginário europeu sobre a América (§ *Da expansão a invasão holandesa*, primeiro parágrafo) —
  ausente dos dois artigos.
- Boa parte do detalhe administrativo fino sobre capitanias hereditárias e divisão territorial
  (doze capitanias, limites Marajó–São Roque–Paranaguá) — ausente dos dois artigos.
- Notas biográficas ligadas a esses trechos (ex.: nota nº 3 do capítulo, sobre Hajstrup) —
  ausentes dos dois artigos.

**Como os dois artigos foram lidos nesta revisão e nenhum contém este material, a hipótese de
"distribuição entre produtos" para este bloco específico não se confirma.** Isso não prova
formalmente que o material foi descartado (poderia, em tese, existir em algum terceiro arquivo
não observado, ou ter sido descartado por decisão consciente do professor) — mas, entre as duas
hipóteses registradas na versão anterior deste documento (corte vs. distribuição), a observação
direta dos dois artigos favorece "corte" ou "reserva para uso futuro fora deste par", não
"distribuição para o segundo produto observável".

### 2.2 O que foi mantido, acrescentado, e mudanças de registro/voz — inalterado da versão anterior

Os itens a seguir foram verificados na primeira versão deste documento contra artigo 1 e
permanecem válidos como estavam (não foram reabertos nesta revisão, exceto onde §3 os atualiza
para o artigo 2):

- Espinha narrativa político-militar mantida: primeiras incursões neerlandesas (1599, 1604),
  embargos de 1585–1609, VOC (1602), WIC (1621), invasão da Bahia (1624), morte de Schouten,
  invasão de Pernambuco (1630), Arraial do Bom Jesus, Calabar, governo de Nassau (1637–1644),
  Guerra dos Oitenta Anos, Trégua dos Doze Anos, restauração portuguesa (1640), insurreição
  pernambucana (1645), capitulação do Recife (1654).
- Citações de fonte primária sobre embriaguez preservadas quase literalmente (Richshoffer,
  Arciszewski, Pudsey, Calado, Waerdenburch, Nassau/Ceullen/Dussen, Hajstrup, Soler, Nieuhof).
- Bloco teórico-historiográfico novo na abertura (estereótipos de bebedores norte/sul da Europa,
  etimologia de destilados, comparação islâmico-safávida — Matthee, 1995) sem equivalente no
  capítulo.
- Frases interpretativas inseridas após citações que no capítulo terminavam na própria citação
  (ex.: leitura foucaultiana do enforcamento da sentinela, citando *Vigiar e punir*, 1987 — o
  capítulo cita Foucault, mas outra obra, em outro contexto).
- Seção "Considerações finais" com vocabulário teórico denso, sem equivalente no capítulo.
- Autoria: capítulo com autoria única implícita; artigo com três autoras/autor (Ana Paula Barco
  da Silva, Gabrielle Legnaghi de Almeida, Christian Fausto Moraes dos Santos), as três com nota
  de rodapé real de afiliação.
- Duas divergências factuais não assinaladas entre capítulo e artigo 1: data do saque de Matanzas
  (1627 no capítulo → 1628 no artigo) e contagem de capitanias (capítulo lista oito nomes para
  "sete capitanias"; artigo remove "Maranhão" e a contagem fecha em sete).

---

## 3. Artigo 1 × artigo 2 — comparação direta (nova nesta revisão)

Esta é a comparação que a correção de premissa exigiu. Leitura de `art2_document.xml` completo
(456 parágrafos) contra o artigo 1 (200 parágrafos).

### 3.1 O que é igual

- **Estrutura de seções idêntica:** título/subtítulo bilíngue → tabela de resumo/palavras-chave
  bilíngue → *Expansão holandesa* → *Beber no Brasil Holandês* → *Considerações finais* → *Notas*
  → *Referências*.
- **Autoria idêntica:** as três mesmas autoras/autor, com as mesmas três notas de rodapé reais de
  afiliação (`word/footnotes.xml` do artigo 2 também tem exatamente 3 entradas — `*`, `**`,
  `***`), mesmos e-mails.
- **Corpo do texto substancialmente igual, frase a frase**, incluindo o bloco teórico de abertura
  (estereótipos norte/sul, destilados, Matthee), todas as citações de fonte primária, as mesmas
  frases interpretativas inseridas após citações (inclusive a mesma leitura foucaultiana), e a
  mesma seção "Considerações finais" — **quase palavra por palavra** entre os dois artigos, nos
  dois parágrafos de síntese final.
- **As mesmas três figuras** (gravura de sapateiro/Rijksmuseum; pedra de fachada de Haarlem;
  *Slavenmarkt* de Wagener), nas mesmas posições relativas do texto.
- **O núcleo indígena/africano está ausente dos dois artigos, do mesmo modo** — não há qualquer
  traço dele no artigo 2.
- **As mesmas lacunas bibliográficas:** citações em texto a Acioli (2005), Bown (2009), Crosby
  (1993), Elias (2001) e Schwartz (1988) aparecem no corpo dos dois artigos, mas **nenhum dos dois
  tem entrada correspondente na lista de "Referências"** — falha de completude bibliográfica
  presente igualmente nos dois artigos, não introduzida nem corrigida entre um e outro.

### 3.2 O que difere

- **Segmentação de parágrafo:** o artigo 2 tem mais que o dobro de parágrafos XML (456 vs. 200)
  para o mesmo texto — quebras de linha adicionais dentro dos mesmos parágrafos de conteúdo, não
  conteúdo novo. A diferença de contagem não corresponde a diferença de extensão real.
  Confirmado por leitura integral: não há parágrafo de conteúdo substantivo no artigo 2 sem
  equivalente no artigo 1, nem vice-versa, no material lido.
- **DOIs acrescentados** a algumas referências no artigo 2 que no artigo 1 apareciam sem DOI ou
  com URL simples: Jarvis (2023), Van Bruaene & Van Bouchaute (2017), Xavier (2025). Não há
  conteúdo novo, é formatação de referência já presente.
- **Anomalia sistemática de caracteres:** no artigo 2, muitos algarismos "6" aparecem substituídos
  por uma letra "G" no texto extraído — por exemplo "1G24" onde o artigo 1 e o capítulo têm
  "1624", "G00" onde seria "600", "3G7" onde seria "367". O padrão é consistente o bastante
  (dígito "6" → "G") para sugerir artefato de fonte/codificação no arquivo `.docx` de origem
  (por exemplo, um estilo de caractere mapeado para uma fonte de símbolos em certas inserções),
  não um erro de conteúdo genuíno — **mas isso não foi confirmado abrindo o arquivo no Word**,
  só inferido da extração de XML; fica registrado como observação técnica, não como fato
  verificado sobre o conteúdo real do artigo.
- **Subtítulo em inglês com datas divergentes de todo o resto do documento:** o artigo 2 traz
  "*Between wars and drunkenness: drinking practices in Dutch Brazil (1524-1554)*" — um século
  antes do que qualquer outra data no mesmo documento (que usa consistentemente 1624–1654,
  inclusive no título em português, na frase de abertura da seção e em todas as datas históricas
  narradas). Esta divergência **não** se explica pelo padrão "6→G" descrito acima (os dígitos
  aqui são "5", não "G"), então não é a mesma anomalia — é uma segunda divergência, de natureza
  distinta, e fica registrada sem explicação: pode ser erro de digitação introduzido nesta
  revisão, ou outro artefato de edição. Não verificável a partir dos arquivos disponíveis.
- **Metadados de submissão presentes apenas no artigo 2:** "Recebido em 02 de dezembro de 2025.
  Aprovado em 19 de maio de 202[G/6]." — o artigo 1 não tem essa linha. Consistente com o artigo 2
  ser um estágio posterior de preparação para submissão/publicação (informação de fluxo
  editorial), mas essa é leitura sobre o gênero do documento, não fato demonstrado pelos arquivos.

### 3.3 Conclusão desta seção

**O artigo 1 e o artigo 2 não são dois núcleos publicáveis distintos derivados do capítulo.** São,
pelo conteúdo observado, duas versões do mesmo produto — mesmo argumento, mesmo corpus, mesma
seleção de fontes, mesma arquitetura de seções, mesma exclusão do bloco indígena/africano. As
diferenças encontradas são de estágio de preparação editorial (metadado de submissão, DOIs
acrescentados) e de artefato técnico (segmentação de parágrafo, anomalia de caractere), não de
conteúdo ou de núcleo temático.

---

## 4. Confronto com o contrato P10 — revisado

Fonte: `P10_CONTRATO_FUNCIONAL_DERIVACAO_CAPITULO_ARTIGOS_HOMOLOGADO_R01.md`
(`PACOTE_FUNCAO_AVALIACAO_CRITICA_PROJETOS_R01`).

### 4.1 Por que este caso não é PRODUTO_A/PRODUTO_B

A leitura de §3 muda a conclusão da versão anterior deste documento em ambas as direções em que
ela havia sido colocada: não é `UM_NUCLEO_VIAVEL` com corte simples (primeira versão), e também
não é `PRODUTO_A`/`PRODUTO_B` com fissão em dois núcleos distintos (correção que havia sido
proposta antes de ler o artigo 2). É uma terceira configuração, que os arquivos sustentam com mais
força que as duas anteriores: **duas versões do mesmo produto derivado**, sem nenhum sinal, nos
próprios arquivos, de qual (se alguma) é a versão canônica.

O contrato P10 tem uma categoria exatamente para isso — não para núcleos múltiplos, mas para
**versões concorrentes do material**: `PS-10` (§35), cujo status canônico é `BLOCKED` com
`BlockPayload.category=GOVERNANCE_CONFLICT`. A redação do cenário no contrato fala de "material de
origem" com versões concorrentes antes da derivação — aqui a concorrência está do lado do produto
derivado, não da origem, o que o contrato não cobre literalmente. Mas a estrutura do problema é a
mesma: **duas coisas materialmente disponíveis, nenhuma decisão registrada sobre qual prevalece**.
Isso é observação por analogia, não aplicação direta do PS-10 — o contrato não escreve esse
cenário (versões concorrentes de saída, não de entrada), e registrar essa lacuna é mais honesto do
que forçar o PS-10 a cobri-la.

### 4.2 O que muda em relação à leitura anterior

- A invariante 15 do P10 ("material não pode ser substancialmente duplicado entre produtos") é
  relevante de um jeito que a versão anterior deste documento não previa: se artigo 1 e artigo 2
  fossem tratados como dois produtos de uma mesma derivação, a duplicação entre eles (quase
  integral) violaria essa invariante abertamente. A leitura mais provável, dados os arquivos, é
  que eles não são dois produtos da mesma derivação, e sim dois estados do mesmo produto — o que
  tira a pergunta do campo "isto viola a invariante 15?" e coloca no campo "qual destas versões é
  a entrada estável para qualquer trabalho seguinte?", pergunta que nenhum dos arquivos responde.
- A ambiguidade sobre o destino do bloco indígena/africano (§2.1) muda de "corte ou distribuição
  para PRODUTO_B" (formulação da versão anterior) para "ausente das duas versões observadas do
  mesmo produto — sem evidência de para onde foi, se foi a algum lugar". A pergunta booleana
  "corte vs. distribuição" tinha uma resposta binária esperada; a resposta que os arquivos dão não
  é nenhuma das duas alternativas antecipadas com confiança suficiente — é "ausente de tudo que
  foi lido".

### 4.3 O que os arquivos ainda não permitem confirmar (repetido da versão anterior, ainda válido)

Nenhum artefato de cartografia, diagnóstico de núcleos, teste de autonomia, veredito de
viabilidade, matriz de transposição aprovada ou arquitetura de produto (P10 §2, §9–§14, §20)
existe em `data/dev/`. Continua não sendo possível determinar, a partir destes arquivos:

1. sob qual nível de intervenção P06 (`INT-01`...`INT-15`) a transformação capítulo→artigo(s) foi
   autorizada;
2. se algum `GATE_DE_ESCOLHA_DE_NUCLEO` ou `GATE_DE_MATRIZ` (P10 §29.2) foi de fato executado;
3. — item novo desta revisão — **se a existência de duas versões do artigo é intencional (por
   exemplo, uma cópia de trabalho e uma cópia final) ou acidental (arquivo duplicado por engano,
   ou duas rodadas de revisão que não convergiram)**. Os arquivos não trazem data de modificação
   comparável nem controle de versão explícito que resolva isso.

---

## 5. Declaração do professor — proximidade P10/P11

Registro literal de declaração do `USUARIO_PROPONENTE`, feita em sessão anterior desta mesma
conversa, sobre a prática real de revisão: **há pouca diferença de produto final entre um capítulo
totalmente revisado e um artigo pronto para submissão.**

Isso não é dedução a partir dos arquivos — é o próprio autor da revisão descrevendo o que faz. Tem
consequência sobre a separação P10/P11 tal como os contratos a descrevem:

- P10 (`docs/spec/funcoes-P10-P14.md`) pressupõe uma fronteira nítida entre "revisar/estabilizar
  capítulo" (papel de Vaquita, §4.2) e "derivar artigo" (papel de Baleia, §4.1) — cartografia,
  diagnóstico de núcleo, teste de autonomia, matriz de transposição são aparato específico da
  derivação, que a simples revisão de um capítulo não deveria acionar.
- P11 (revisão de dissertação e tese, catálogo de funções em CLAUDE.md §3) é a função que cobre
  "capítulo totalmente revisado" sem produzir artigo.
- Se, na prática do professor, um capítulo revisado a fundo já fica indistinguível, como produto,
  de um artigo pronto para submissão, a pergunta "isto é P10 ou P11?" pode não ter resposta
  determinável pelo estado final do texto — só pela finalidade declarada no início (virar artigo
  ou não), que é exatamente o que `InputItem.classification.functions` [P09 §6] existe para
  registrar, e não algo que o sistema poderia inferir do documento em si (CLAUDE.md §3: "o sistema
  não classifica documento").
- **A existência de duas versões quase idênticas do mesmo artigo (§3) é, incidentalmente, um
  exemplo concreto dessa proximidade:** se a diferença entre "capítulo revisado" e "artigo pronto"
  já é pequena, a diferença entre duas rodadas de revisão do mesmo artigo (adicionar DOIs, ajustar
  segmentação, corrigir — ou não — uma data) é ainda menor, e um sistema que precisasse decidir
  "isto é uma nova versão do mesmo produto ou um produto novo?" enfrentaria, nesse par real, um
  caso limítrofe genuíno, não hipotético.
- Fica como observação aberta, não como lacuna formal em `LACUNAS.md` (que exigiria localização em
  módulo específico, ainda não determinada). Não há fonte, até agora, que resolva essa
  proximidade.

---

## 6. Ambiguidades registradas sem resolução

- **Destino do bloco indígena/africano.** Ausente do capítulo em ambos os artigos observados.
  Corte, reserva para uso futuro, ou existência em terceiro documento não observado — todas
  permanecem possíveis; nenhuma confirmada.
- **Qual versão do artigo (1 ou 2) é a canônica**, se alguma o é. Nada nos arquivos resolve isso.
- **Anomalia de caractere "6→G" no artigo 2** — provável artefato de extração/fonte, não
  confirmado por abertura direta do arquivo no Word.
- **Data divergente no subtítulo em inglês do artigo 2** (1524-1554 vs. 1624-1654 em todo o resto
  do documento) — sem explicação disponível nos arquivos.
- **Autoria coletiva vs. "voz do autor avaliado" no singular** (P10 §25) — o contrato não define o
  que ocorre com "perfil de voz" quando a derivação editorial adiciona coautoria. Relaciona-se ao
  aberto do CLAUDE.md §13 item 1, mas não é o mesmo problema.
- **Correções factuais não assinaladas** entre capítulo e artigos (data 1627→1628 do saque de
  Matanzas; contagem de capitanias) — presentes igualmente nos dois artigos (herdadas de artigo 1
  para artigo 2, não introduzidas nem corrigidas entre eles). O contrato exige rastreabilidade de
  todo trecho transposto à origem (invariante 16) e proíbe invenção de referência (invariante 13),
  mas não trata do caso de correção silenciosa de uma afirmação do material de origem.
- **Proveniência por marcador** (`[diff:capítulo]` etc., CLAUDE.md §9) — ausente dos arquivos
  observados. Sem ela, distinguir o que é do capítulo, o que foi reescrito e o que é inserção nova
  exige comparação manual como a feita aqui.
- **Lacunas bibliográficas compartilhadas** (Acioli, Bown, Crosby, Elias, Schwartz citados em texto
  sem entrada em "Referências") — presentes nos dois artigos igualmente. Se isso reflete um hábito
  de trabalho do professor (referência completada depois, ou lista de referências não totalmente
  sincronizada com o texto) ou um lapso pontual não é determinável pelos arquivos.

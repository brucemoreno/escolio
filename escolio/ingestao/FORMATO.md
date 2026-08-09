# FORMATO — saída do ingestor de PDF acadêmico

**Este documento descreve o parser de PDF (`parser.py`) especificamente.** O parser de `.docx`
(`parser_docx.py`, 2026-08-09) produz o mesmo `DocumentoIngerido`, mas com regras de detecção
próprias e sem página real — ver seção "Localização em `.docx`" ao final deste arquivo e
`escolio/ingestao/LACUNAS.md` (LAC-ING-013 a 018). Onde este documento diz "toda unidade
rastreável até a página", isso é requisito do parser de PDF; para `.docx` o requisito
equivalente é "toda unidade rastreável até parágrafo + seção", porque página não é dado que o
formato grava.

Contrato **não definitivo**: virá do P09 e esta estrutura terá de ser
reconciliada com ele depois. O que está fixado agora é o que o prompt
exige: IDs estáveis e determinísticos, toda unidade rastreável até a(s)
página(s) de origem, texto preservado literalmente, heurística
documentada com o caso real que a motivou.

Desenvolvido e testado apenas contra
`data/dev/Relatorio_Final_PIBIC-Bolsa-CNPq-e-UEM - Ricardo Antonio Esteves dos Santos.pdf`
— um relatório final de iniciação científica (PIBIC/CNPq-UEM), 33 páginas,
Word→PDF, Times New Roman 12pt no corpo. Nenhuma regra abaixo foi
generalizada além do que este documento comprova; onde a generalização é
incerta, isso está dito explicitamente.

## Estrutura geral

```
DocumentoIngerido
├── hash_documento          sha256[:8] do arquivo — chave dos IDs
├── caminho_original
├── num_paginas
├── metadados               Metadados (folha de rosto)
├── secoes                  list[Secao]
├── paragrafos              list[Paragrafo]
├── notas_de_rodape         list[NotaDeRodape]
├── citacoes_recuadas       list[CitacaoRecuada]
├── citacoes_no_corpo       list[CitacaoNoCorpo]
├── referencias             list[ItemDeReferencia]
├── figuras                 list[Figura]            (tabelas/quadros/figuras)
└── hifens_de_fim_de_linha_preservados   int
```

Ver `modelos.py` para os campos de cada dataclass — os docstrings ali
documentam decisões de design, este arquivo documenta as **regras de
detecção** (RG-001 a RG-010) e o **porquê**.

## Identificadores (`identificadores.py`)

Formato: `UNI-<TIPO>-<HASH8>-<PAGINA:04d>-<INDICE:04d>`.

- `HASH8`: sha256 do conteúdo binário do PDF, truncado a 8 hex — mesmo
  arquivo, mesmo hash, em qualquer execução/máquina.
- `PAGINA`: página onde a unidade **começa** (`pagina_inicio` para
  unidades que podem atravessar página; `pagina` para as que não podem).
- `INDICE`: posição sequencial da unidade dentro da página de início, na
  ordem de leitura (topo→baixo, esquerda→direita dentro da mesma linha
  visual). Reinicia a cada página.

Determinismo verificado: rodar `parse_pdf` duas vezes sobre o mesmo
arquivo produz exatamente os mesmos IDs (testado em
`tests/ingestao/test_parser.py`).

## Unidades que atravessam página: `pagina_inicio`/`pagina_fim`

**Correção de design** (feedback do usuário durante a implementação):
"rastreável até a página" não significa "cada unidade pertence a uma
única página" — significa que a página é sempre determinável a partir
da unidade. `Paragrafo`, `CitacaoRecuada` e `NotaDeRodape` (unidades que
neste documento comprovadamente atravessam quebra de página) usam
`pagina_inicio`/`pagina_fim` em vez de um único campo `pagina`. Quando
não há quebra, os dois valores são iguais.

Constatado no documento real: a citação recuada da receita "moxerich"
(RG-006) começa no fim da página 13 e termina no início da página 14 —
é uma única citação, uma única unidade, `pagina_inicio=13,
pagina_fim=14`. A primeira versão desta implementação fragmentava a
unidade em duas ao cruzar a página; foi corrigida para não fragmentar.

`Secao`, `ItemDeReferencia`, `Figura` e `CitacaoNoCorpo` mantêm um único
campo `pagina` porque, no fluxo deste parser, não atravessam página por
natureza (título é uma linha; `CitacaoNoCorpo` aponta para dentro de um
`Paragrafo` já resolvido).

## RG-001 — Detecção de título de seção (`heuristicas_hierarquia.py`)

**Sinal**: linha inteiramente em negrito (todo caractere não-espaço usa
fonte `*Bold*`), tamanho 11.5–12.5pt, `x0` na margem do corpo (≤60),
texto curto (<80 caracteres).

**Por que não usar tamanho de fonte maior**: este documento não destaca
títulos de seção por tamanho — usa o mesmo 12pt do corpo, só o negrito
muda. Tamanho maior (14/18pt) aparece exclusivamente na capa
(páginas 1–3), tratada à parte (ver RG-010).

**Falso positivo corrigido**: a primeira versão desta heurística
verificava "a linha contém ALGUM caractere em negrito" — isso capturava
como "título" uma linha de corpo comum que tinha apenas uma palavra em
negrito por ênfase (constatado na página 26: "...consolidou a
conservação **agridoce** como um traço marcante..."). Corrigido para
exigir que **toda** a linha seja negrito (`Linha.totalmente_negrito`),
o que elimina esse falso positivo sem eliminar nenhum título real.

**Sem numeração**: nenhuma seção do corpo usa "1.", "1.1" etc. — apenas
o formulário CNPq da página 1 numera itens burocráticos, que não são
seções do trabalho.

## RG-002 — Ambiguidade estrutural não resolvida: nível hierárquico

Este documento **não tem sumário/índice**. Não há como validar a lista
de títulos detectados contra uma lista de referência do próprio
documento — logo não há como confirmar que todo título detectado tem o
mesmo peso hierárquico (todos foram tratados como nível 1/CAPÍTULO por
não haver evidência de um segundo nível).

Um caso constatado exige tratamento especial: **"Fonte Primária"**
(página 33) usa o **mesmo padrão gráfico exato** de um título de
capítulo (negrito, 12pt, x0=56.6, linha curta isolada), mas
semanticamente é uma subdivisão da lista de referências (fontes
primárias vs. bibliografia geral), não um capítulo do corpo. Sem
sumário para desambiguar, esta implementação:

- reconhece a linha como título estrutural (não a funde ao texto
  corrido, não descarta);
- marca `nivel=None` e `indeterminado=True` com
  `MotivoIndeterminado.PADRAO_GRAFICO_AMBIGUO`;
- usa o rótulo como `subsecao` dos itens de referência que a seguem
  (`ItemDeReferencia.subsecao = "Fonte Primária"`).

Qualquer título detectado **dentro** da zona de referências (após o
título "Referências Bibliográficas") passa por essa mesma regra —
generalização mínima, não testada contra um segundo caso real.

## RG-003 — Agrupamento de linhas em parágrafo (`heuristicas_paragrafo.py`)

**Sinal**: a primeira linha de um parágrafo tem `x0≈92` (recuo de
primeira linha); as linhas seguintes do mesmo parágrafo têm `x0≈57`
(margem do corpo). Uma nova linha em `x0≈92` fecha o parágrafo atual e
abre um novo. Limiar usado: `x0 ≥ 80` conta como recuo de primeira
linha (meio-termo entre 57 e 92, com folga).

Medido nas páginas 5–9 do corpo: 153 linhas de continuação em x0≈57
contra 18 primeiras linhas em x0≈92 — sinal limpo e consistente.

## RG-004 — Preservação literal e hífen de fim de linha (revisado)

**Tentativa inicial, descartada**: tratar todo hífen no fim de uma linha
como hifenização de quebra tipográfica e removê-lo ao unir com a
próxima linha (ex.: "destacam-\nse" → "destacamse").

**Por que foi descartada**: checagem contra as 6 ocorrências reais de
hífen em fim de linha neste documento mostrou que **nenhuma** é hífen de
quebra tipográfica pura:

| Página | Fragmento | O que é |
|---|---|---|
| 5 | `destacam-` | clítico verbal — "destacam-**se**" |
| 7 | `ibero-` | composto — "ibero-**americano**" (ou similar) |
| 20 | `físico-` | composto — "físico-**químicos**" |
| 25 | `luso-` | composto — "luso-**brasileiro**" |
| 26 | `transformando-` | clítico — "transformando-**se**" |
| 31 | `593-` | intervalo de páginas de referência — "593-**610**" |

Remover o hífen nesses casos produz texto corrompido (ex.:
"destacamse", que não é português). Sem um dicionário para decidir se
uma palavra é normalmente hifenizada, não há como distinguir hífen de
quebra de hífen-que-pertence-à-palavra a partir do layout.

**Regra final**: nenhum hífen de fim de linha é removido. A junção
preserva o hífen literal e concatena sem espaço extra (o hífen já
funciona como a junção visual). Cada ocorrência é contada em
`DocumentoIngerido.hifens_de_fim_de_linha_preservados` — 6 neste
documento — para que a decisão fique disponível para revisão humana,
não escondida dentro do texto.

## RG-005 — Notas de rodapé (`heuristicas_notas.py`)

**Confirmado real neste documento** (não assumido): 4 notas de rodapé,
todas seguindo o mesmo padrão —

- **Chamada**: um dígito no corpo do texto, em tamanho visivelmente
  menor que o texto ao redor (6.5pt contra 10–12pt do corpo),
  imediatamente após a pontuação que fecha a citação (ex.:
  `(Grewe, 1979, p. 13).¹`).
- **Corpo da nota**: no rodapé da mesma página, inicia com o mesmo
  número no mesmo tamanho reduzido (6.5pt), seguido do texto da nota em
  10pt — sempre iniciando com "No original: ...".
- **Multi-linha**: o corpo de uma nota pode ocupar até 3 linhas; só a
  primeira começa com o número. As demais são texto corrido no mesmo
  `x0` da margem do corpo comum — tratadas como continuação enquanto o
  estado "nota em aberto" está ativo (ver `parser.py`), não reavaliadas
  como início de outra unidade.

**Pré-requisito de layout descoberto**: o pdfplumber separa a chamada
(baseline ligeiramente deslocada, por ser sobrescrito) e o texto ao
redor em `Linha`s distintas se agrupadas por `top` arredondado exato
(diferença medida: 0.8pt). `layout.extrair_linhas` usa uma tolerância de
2.0pt para agrupar caracteres na mesma linha visual — sem isso, a
chamada nunca aparece "dentro" da linha que a heurística de notas
examina.

**Vínculo bidirecional**: `NotaDeRodape.unit_id_chamador` +
`posicao_na_chamada` apontam para a unidade (parágrafo OU citação
recuada — uma citação também pode terminar em chamada, constatado) e a
posição de caractere exata do marcador dentro do texto dessa unidade,
antes de qualquer edição. A resolução final só acontece depois que
**todas** as unidades do documento fecharam (passagem final em
`parse_pdf`), porque uma citação recuada pode fechar bem depois do
corpo da nota já ter sido lido.

**Indeterminado**: nota cujo número não corresponde a nenhuma chamada
localizada — `indeterminado=True`,
`MotivoIndeterminado.SEM_CHAMADA_CORRESPONDENTE`. Não ocorreu neste
documento (as 4 notas foram vinculadas), mas o caminho existe e é
testado.

## RG-006 — Citação recuada (`heuristicas_citacoes.py`)

**Sinal**: `x0 ≥ 140` (bem além do recuo de primeira linha de parágrafo,
≈92). Medido: bloco de citação em `x0≈162.9`, corpo em `x0≈57/92` —
folga grande, sem ambiguidade.

**Acumulação multi-linha e multi-página**: linhas contíguas em `x0`
recuado pertencem à mesma citação, inclusive atravessando quebra de
página (ver seção "Unidades que atravessam página" acima — caso real:
citação "moxerich", páginas 13→14).

**Exclusão de falso positivo — dentro de tabela**: cabeçalho e célula de
tabela usam o mesmo `x0` de bloco recuado (constatado: "Frequência no
Manuscrito", cabeçalho da Tabela 2, página 19). O parser rastreia um
estado "dentro de tabela" (entre a legenda "Tabela N:" e a linha
"Fonte:" que a fecha) e ignora citação recuada nessa faixa — não tenta
extrair a tabela em si (fora de escopo).

**Vínculo com nota de rodapé**: uma citação recuada pode terminar com
uma chamada de nota (`CitacaoRecuada.notas_de_rodape_ids`) — constatado
nas 4 citações que citam Grewe (1979), cada uma seguida da chamada que
remete ao texto original em catalão.

## RG-007 — Citação ABNT autor-data no corpo (`heuristicas_citacoes.py`)

Duas formas, com confiabilidade diferente:

1. **Parentética** — `(AUTOR[; AUTOR2], ano[, p. N])`, ex.: `(BRAGA,
   2004)`. Aceita diretamente: maiúsculas + vírgula + ano de 4 dígitos
   entre parênteses não ocorre em texto corrido comum deste documento.

2. **Narrativa** — `Nome (ano)`, ex.: `Grewe (1979, p. 13)`. **Ambígua**:
   um substantivo próprio qualquer seguido de ano entre parênteses casa
   com o mesmo padrão textual. Constatado no documento real: "o
   manuscrito da Infanta D. Maria **(1987)**" casa com o padrão, mas
   "Infanta"/"Maria" não são autores — são o nome do objeto de estudo
   seguido do ano de uma edição citada em outro lugar do texto.

   Sem sintaxe que distinga os dois casos com segurança, a única
   verificação disponível é cruzar o nome candidato com os sobrenomes
   que aparecem na **lista de referências do próprio documento**
   (extraída antes do laço principal). Candidato cujo nome não bate com
   nenhum sobrenome da lista é marcado `indeterminado=True`,
   `MotivoIndeterminado.AUTOR_DATA_NAO_RECONHECIDO` — não é descartado
   nem aceito às cegas.

   Resultado medido: 138 citações no corpo encontradas, 38 marcadas
   indeterminadas (a maioria das formas narrativas cujo "nome" é
   "Infanta" ou "Maria", corretamente sinalizadas).

## RG-008 — Segmentação de itens de referência (`heuristicas_referencias.py`)

**Sinal**: dentro da seção "Referências Bibliográficas", toda linha
(primeira do item e continuações) começa no mesmo `x0≈56.6` — ao
contrário do corpo, a lista de referências não usa recuo de primeira
linha. O que separa um item do próximo é o **espaço vertical**: gap
intra-item ≈15.8–16.0pt; gap entre itens ≈33.8–34.0pt (pouco mais que o
dobro). Limiar usado: gap ≥ 1.6× o gap típico intra-item (15.9pt medido)
indica novo item.

**Subseção**: quando um segundo título aparece dentro da zona de
referências (ex.: "Fonte Primária", ver RG-002), os itens seguintes
recebem `subsecao="Fonte Primária"` em vez de `None`.

Resultado: 60 itens de referência extraídos, todos com texto completo
(sem fragmentação por linha) e rastreáveis à página.

## RG-009 — Quadros, tabelas e figuras (`heuristicas_figuras.py`)

**Cobertura desigual e documentada.** O único documento de
desenvolvimento contém **4 TABELAS** (rotuladas `"Tabela N: <título>"`,
cada uma seguida de `"Fonte: <crédito>"`) e **nenhuma** figura ou quadro
rotulado como tal, e nenhuma imagem de conteúdo (apenas um logotipo de
formulário na página 1 — não é fonte primária, é decoração
institucional).

A detecção de tabela foi **testada e validada** contra os 4 casos reais.
A detecção de "Figura N:"/"Ilustração N:" segue o mesmo princípio de
rótulo textual por analogia estrutural, mas **não foi validada** contra
nenhum exemplo real — todo achado desse tipo é marcado
`indeterminado=True`, `MotivoIndeterminado.SEM_ANCORA_TEXTUAL`, para que
nunca seja tratado como fato estabelecido pela ausência de teste.

Conteúdo tabular/imagem em si não é extraído nesta fase (fora de
escopo) — apenas legenda, crédito/fonte, numeração e posição relativa
(`"apos <unit_id do último parágrafo>"`).

`referencia_de_acervo` (para imagens que são fonte primária, conforme o
prompt) não foi implementado com dado real de teste — nenhuma imagem de
acervo ocorre neste documento. O campo existe no modelo mas fica sempre
`None` nesta implementação; ver LACUNAS.md.

## RG-010 — Metadados da folha de rosto (`heuristicas_metadados.py`)

**pdfplumber/PDF metadata não serve**: `Title`/`Author` do próprio
arquivo PDF são o nome do formulário CNPq/UEM e a Pró-Reitoria,
respectivamente — não o título do trabalho nem o autor real. Os
metadados verdadeiros só existem como texto na folha de rosto.

**Página 1 é ruído, não folha de rosto**: é o formulário burocrático
CNPq/UEM. Tem seu próprio cabeçalho grande ("RELATÓRIO FINAL", 18pt)
que colidiria em tamanho com o título real (folha de rosto, páginas
2–3, também 18pt) se não fosse excluída. A extração de título ignora a
página 1 inteira.

**Campos extraídos por rótulo textual** (páginas 2–3):
- `orientador`: linha `"ORIENTADOR(A): <nome>"`.
- `autor`: linha `"Bolsista: <nome>"`.
- `programa`: linha `"DEPARTAMENTO DE <nome>"` — proxy textual, o
  documento não usa um rótulo "Programa:" explícito.
- `ano`: extraído da linha de data da capa ("Maringá, 31 de agosto de
  2025.") — o documento não usa um campo "Ano:" explícito.
- `tipo_de_trabalho`: usa o cabeçalho institucional repetido ("PROGRAMA
  INSTITUCIONAL DE BOLSAS DE INICIAÇÃO CIENTÍFICA") como valor literal —
  não normalizado para uma categoria (ex.: "TCC", "dissertação"), porque
  o documento não fornece essa categoria.
- `titulo`: linhas de maior corpo (≥16pt) fora da página 1, até a
  primeira reocorrência da própria primeira linha (a capa se repete nas
  páginas 2 e 3 neste documento).

**Campo do formulário quebrado em dois na mesma linha visual**: a página
1 concatena mais de um campo rotulado na mesma linha (ex.:
`"2. ORIENTADOR: Christian Fausto Moraes dos Santos 3. DEPARTAMENTO:
DHI"`). Os padrões de extração param no próximo marcador `"N.
RÓTULO:"` ou no fim da linha, para não deixar o valor de um campo
"vazar" para dentro do próximo — mas como o título e os campos
principais (orientador, bolsista) vêm de forma limpa da página 2/3, esse
formulário da página 1 não é a fonte primária desses campos.

## Relatório de ingestão (`relatorio.py`)

Números medidos neste documento (ver seção final da conversa de
desenvolvimento para o relatório completo). Campos:
`num_paginas`, `num_secoes` (+indeterminadas), `num_paragrafos`,
`num_notas_de_rodape` (+sem chamada correspondente),
`num_citacoes_recuadas`, `num_citacoes_no_corpo` (+indeterminadas),
`num_referencias`, `num_figuras_tabelas` (+indeterminadas),
`num_hifens_de_fim_de_linha_preservados`, `total_indeterminados`.

## O que fica fora de escopo (confirmado, não apenas declarado)

- Análise de conteúdo, verificação bibliográfica, chamada de API,
  interface, OCR — conforme o prompt.
- Extração da imagem/conteúdo de figuras e tabelas em si.
- Qualquer inferência sobre nível hierárquico além do que a página 1
  (capa) e a heurística de título permitem confirmar sem sumário.
- Normalização de hífen de fim de linha (ver RG-004).
- Detecção de coluna múltipla — este corpus é de coluna única; a ordem
  de leitura por `top` assume isso (ver `layout.py` e LACUNAS.md).

## Localização em `.docx`: parágrafo + seção + ordinal, não página

Tudo acima descreve o parser de PDF. `parser_docx.py` (2026-08-09) produz o mesmo
`DocumentoIngerido`, calibrado contra os 3 capítulos reais em `data/capitulos/`, mas com uma
diferença estrutural deliberada: **nenhuma unidade tem página**.

`.docx` não grava paginação no arquivo — ela só existe quando o Word renderiza para impressão,
recalculada a cada abertura a partir de margem/fonte/impressora, e muda a cada edição do
documento. Um número de página extraído hoje (ex.: convertendo para PDF só para obter um)
ficaria errado assim que o professor editasse o `.docx` de novo — seria uma localização
falsamente estável, pior que não ter página nenhuma. Por isso `Secao.pagina`,
`Paragrafo.pagina_inicio/pagina_fim`, `CitacaoRecuada.pagina_inicio/pagina_fim`,
`NotaDeRodape.pagina_chamada` e `DocumentoIngerido.num_paginas` são sempre `None` para
documentos de origem `.docx` (o tipo foi relaxado para `int | None` em `modelos.py` para
acomodar isso, sem afetar o parser de PDF, que continua sempre passando inteiros reais).

O localizador equivalente para `.docx` é **`Paragrafo.paragrafo_ordinal`** (posição sequencial
de leitura, base 0) combinado com `secao_id` (a seção/título mais recente antes da unidade).
Isso não é menos preciso que página — é mais preciso (uma página cobre ~500 palavras; um
ordinal de parágrafo aponta para um parágrafo só) e não descasa do documento vivo quando o
professor edita o texto. É também o mesmo tipo de folga que o contrato do sistema já reserva
em outro lugar: `contrato/referencia.py::Location.page` é `str | None`, não `int`
obrigatório, e o produto final de comentário (`P13Comment.anchor_start/anchor_end/
anchor_text_hash`) já localiza por posição de caractere e hash de trecho, não por página.

**Detecção de título sem estilo Word**: os 3 documentos reais não usam nenhum estilo de
título do Word ("Heading N"/"Título N") — todo cabeçalho é um parágrafo comum inteiramente em
negrito. O primeiro parágrafo totalmente em negrito é o título do capítulo
(`NivelHierarquia.CAPITULO`); parágrafos totalmente em negrito subsequentes que casam com
`^\d+\s*[-–.]\s*\S` ("1- Introdução.", "2- ...") são seção (`NivelHierarquia.SECAO`) — só um
nível de numeração observado, nenhuma subseção "N.M-". Título em negrito fora desses dois
casos fica `indeterminado=True`, nunca forçado a um nível.

**Citação recuada por indentação** (`paragraph_format.left_indent`, medido em 113,4pt nos
blocos reais, limiar adotado 50pt) substitui o `x0` do PDF, que não existe em `.docx`.

**Notas de rodapé são lidas do XML estruturado do Word** (`word/footnotes.xml` +
`<w:footnoteReference>` no corpo), não por heurística visual — mais confiável que o parser de
PDF nesse ponto, porque o Word já grava a nota como dado estruturado, não texto solto num
rodapé renderizado. Resultado nos 3 documentos reais: 0 notas indeterminadas (todas as
49 chamadas resolveram parágrafo/citação de origem).

**Sem lista de referências nos 3 documentos reais** — citação é só por nota de rodapé;
`referencias` e `figuras` ficam sempre vazios para este parser nesta calibração. Ver
`escolio/ingestao/LACUNAS.md` (LAC-ING-013 a 018) para o raciocínio completo de cada decisão.

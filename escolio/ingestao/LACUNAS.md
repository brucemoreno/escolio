# LACUNAS — módulo de ingestão de PDF acadêmico

Lacunas, correções de premissa e decisões de implementação encontradas
durante a construção do ingestor. Nenhum item aqui foi resolvido por
inferência silenciosa; cada um documenta a decisão tomada e por quê —
mesma disciplina de escolio/LACUNAS.md (ver [[project-escolio-p05-lacunas]]
em memória).

## Escopo de dados

- **LAC-ING-001** — desenvolvido e testado exclusivamente contra
  `data/dev/Relatorio_Final_PIBIC-Bolsa-CNPq-e-UEM - Ricardo Antonio
  Esteves dos Santos.pdf`. `data/gold/` não foi lido, aberto nem
  processado em nenhum momento desta implementação — é material
  reservado para avaliação futura. Toda heurística documentada em
  FORMATO.md é validada contra um único documento real; heurísticas que
  não puderam ser exercitadas com dado real estão marcadas
  explicitamente (ver LAC-ING-004, LAC-ING-005).

## Correções de premissa (erros da primeira tentativa, corrigidos antes de escrever teste)

- **LAC-ING-002 — falso positivo de título por ênfase interna.** A
  primeira versão da heurística de título (RG-001) classificava como
  título qualquer linha que contivesse UM caractere em negrito, em vez
  de exigir que a linha inteira fosse negrito. Isso produzia falso
  positivo em texto de corpo comum com uma palavra em negrito por ênfase
  (constatado na página 26: "...consolidou a conservação **agridoce**
  como um traço marcante..."). Corrigido para exigir negrito em 100% dos
  caracteres não-espaço da linha (`Linha.totalmente_negrito`) antes de
  qualquer teste ser escrito contra o caso.

- **LAC-ING-003 — hífen de fim de linha não é hífen de quebra tipográfica
  neste documento.** A primeira versão de RG-004 removia todo hífen no
  fim de uma linha ao unir com a linha seguinte, assumindo que era
  hifenização de impressão. Checagem contra as 6 ocorrências reais
  mostrou que nenhuma é hífen de quebra pura — todas pertencem à palavra
  (clíticos verbais, compostos) ou são pontuação (intervalo de páginas).
  Removê-las corrompia o texto (ex.: "destacamse"). Corrigido para nunca
  remover hífen de fim de linha; cada ocorrência fica contada em
  `hifens_de_fim_de_linha_preservados` para revisão humana, ver RG-004
  em FORMATO.md.

- **LAC-ING-004 — unidade que atravessa página não deve fragmentar.**
  A implementação inicial fechava parágrafo/citação recuada ao mudar de
  página, gerando dois registros ligados por um campo
  `continuacao_de_id`. Corrigido a partir de feedback do usuário: "toda
  unidade rastreável até a página" não significa "uma unidade por
  página" — significa que a página é sempre determinável a partir da
  unidade. `Paragrafo`, `CitacaoRecuada` e `NotaDeRodape` agora usam
  `pagina_inicio`/`pagina_fim` e permanecem unidades únicas mesmo
  atravessando quebra de página (caso real: citação "moxerich",
  página 13→14). Ver nota de design em `modelos.py` e seção dedicada em
  FORMATO.md.

- **LAC-ING-005 — pdfplumber separa sobrescrito do texto ao redor em
  linhas distintas por padrão.** A chamada de nota de rodapé (dígito em
  sobrescrito) tem baseline (`top`) deslocado ~0.8pt do texto ao redor;
  agrupar caracteres por `top` arredondado exato quebrava a chamada em
  uma `Linha` separada, e a heurística de notas nunca via os dois
  juntos — 0 notas detectadas na primeira versão, apesar de 4 notas
  reais existirem no documento. Corrigido com uma tolerância de 2.0pt em
  `layout.extrair_linhas` (ver TOLERANCIA_MESMA_LINHA).

## Cobertura não validada (heurística existe, dado real não)

- **LAC-ING-006** — detecção de "Figura N:"/"Ilustração N:" (RG-009)
  segue o mesmo princípio textual da detecção de tabela, validada com 4
  casos reais, mas o documento de desenvolvimento não contém nenhuma
  figura rotulada como tal — apenas 4 tabelas e um logotipo institucional
  de formulário (não é fonte primária). Todo achado desse tipo fica
  marcado `indeterminado=True` para nunca ser tratado como testado.

- **LAC-ING-007** — `Figura.referencia_de_acervo` (referência de acervo
  de uma imagem que é fonte primária, conforme pedido no prompt) não tem
  nenhum caso real neste documento para calibrar a extração — o campo
  existe no modelo mas permanece sempre `None` nesta implementação. Sem
  um segundo documento com imagem de acervo, não há como testar essa
  extração sem adivinhar o formato do dado.

- **LAC-ING-008** — subseção de nível 2/3 na hierarquia (capítulo →
  seção → subseção) não tem caso real: todo título detectado neste
  documento usa o mesmo padrão gráfico (negrito 12pt, margem do corpo),
  logo todos foram tratados como nível 1 (CAPITULO) por falta de
  evidência de um segundo nível. `NivelHierarquia.SECAO` e `.SUBSECAO`
  existem no vocabulário controlado mas não são emitidos por nenhuma
  regra desta implementação.

- **LAC-ING-009** — layout de coluna única assumido sem exceção: este
  documento não tem colunas múltiplas, então a ordem de leitura por
  `top` (topo→baixo) é suficiente. Um documento com colunas exigiria
  agrupar por coluna antes de ordenar por `top` — não implementado,
  porque não há caso real para validar contra.

## Ambiguidade estrutural não resolvida (decisão explícita de marcar como indeterminado)

- **LAC-ING-010 — "Fonte Primária" (RG-002).** Mesmo padrão gráfico de
  título de capítulo, mas é uma subdivisão da lista de referências. Sem
  sumário no documento para desambiguar por correspondência de rótulo,
  a implementação marca a seção como `indeterminado=True` em vez de
  chutar seu nível hierárquico. Ver FORMATO.md RG-002.

- **LAC-ING-011 — citação narrativa "Nome (ano)" (RG-007).** O mesmo
  padrão textual serve tanto para citação autor-data quanto para uma
  referência não-bibliográfica a um objeto nomeado seguido de ano (ex.:
  "a Infanta D. Maria (1987)", onde 1987 é o ano de uma edição do
  manuscrito, não de uma publicação da "Infanta"). A checagem cruzada
  contra os sobrenomes da lista de referências do próprio documento
  reduz mas não elimina a ambiguidade — candidato sem correspondência
  fica marcado indeterminado, nunca aceito ou descartado às cegas.

## Reconciliação com P09 — feita, parcial (item 3 do roadmap)

- **LAC-ING-012 — `DocumentoIngerido` → `InputItem` existe; `MaterialUnit` (P19 §9) não.**
  `escolio/adaptadores/ingestao_para_input_item.py` converte `DocumentoIngerido` em
  `InputItem` [P09 §6], um por documento (não um por unidade interna — parágrafo, seção
  etc. permanecem estrutura interna, sem virar `InputItem` próprio; nenhuma fonte pede essa
  granularidade). Implementa apenas a regra de identidade de `material_id` [P19 §10]:
  único, independente do nome do arquivo, estável entre cópias — derivado de
  `hash_documento`. Os outros 26 campos de `MaterialUnit` [P19 §9] —
  `owner_or_controller`, `license_status`, `authorization_basis`, `authorized_purposes`,
  `retention_class`, `audit_status`, `human_gate`, etc. — não foram implementados: exigem
  decisão humana de autorização/titularidade/licença que nenhum parser produz, e P19
  §71–73 proíbem classificar material real fora do fluxo homologado com gates
  (`GATE_DE_ADMISSAO_DE_MATERIAL` e outros). Ver
  `escolio/adaptadores/ingestao_para_input_item.py` (docstring do módulo) para o raciocínio
  completo. `FORMATO.md` ainda descreve o schema de ingestão como não-definitivo; a
  reconciliação com P09 §6 está feita para o nível de documento, não para os campos de
  `classification`, `processing`, `security`, `retention` de `InputItem` (deixados no
  padrão do dataclass) nem para `MaterialUnit`.

## Parser de .docx (2026-08-09) — módulo novo, não substitui o de PDF

`escolio/ingestao/parser_docx.py` — calibrado contra os 3 capítulos reais em
`data/capitulos/` (`1- Endoparasitoses.docx`, `2- Ectoparasitoses.docx`,
`3- Terapêuticas.docx`), fornecidos pelo professor para o piloto real de P11. Mesma
disciplina de zero-inferência do parser de PDF; decisões e lacunas próprias, listadas aqui em
vez de misturadas com as de LAC-ING-001 a 011 (que são do documento de PDF).

**Escopo ampliado em 2026-08-12: de 3 para 5 capítulos.** O professor entregou dois capítulos
novos, com nomes de arquivo diferentes dos três originais — `data/capitulos/` hoje tem
`1. Cap. 1 - Endoparasitoses.docx`, `2. Cap. 2 - Ectoparasitoses.docx`,
`3. Cap. 3 - Terapêuticas.docx`, `4. Cap. 4 -  Achaque do bicho.docx` e
`5. Cap. 5 - Medicina Tropical.docx` (os três primeiros com o mesmo conteúdo de antes, prefixo
de nome mudou de `"N- "` para `"N. Cap. N - "`). `tests/ingestao/conftest.py::_caminhos_capitulos_docx`
glob `data/capitulos/*.docx` sem nome fixo — nenhum ajuste de fixture foi necessário; os testes
passaram a rodar contra os 5 arquivos sem qualquer mudança de código de teste além da correção
abaixo. Referências a "os 3 capítulos reais" nas entradas LAC-ING-013 a LAC-ING-019 abaixo
descrevem o estado da calibração original (2026-08-09) — não foram reescritas retroativamente;
LAC-ING-014 é a única cujo achado o material novo desmentiu, registrado logo abaixo dela.

- **LAC-ING-013 — `.docx` não tem página real; localização é parágrafo + seção + ordinal.**
  Decisão de arquitetura (não de heurística): `Secao.pagina`, `Paragrafo.pagina_inicio/
  pagina_fim`, `NotaDeRodape.pagina_chamada`, `CitacaoRecuada.pagina_inicio/pagina_fim`,
  `ItemDeReferencia.pagina`, `Figura.pagina` e `DocumentoIngerido.num_paginas` foram
  relaxados de `int` para `int | None` em `modelos.py` (sem valor default — quem constrói
  continua obrigado a decidir, `None` passa a ser resposta válida). Motivo: a paginação de um
  `.docx` só existe quando o Word renderiza para impressão — não é dado gravado no XML — e
  muda a cada edição do documento. Converter para PDF só para obter um número congelaria uma
  localização falsamente estável (parecia precisa, ficaria errada na próxima edição do
  professor). Decisão do professor: usar `Paragrafo.paragrafo_ordinal` (novo campo, posição
  sequencial de leitura, base 0) + `secao_id` como localizador — mesma folga que o contrato já
  dá em `contrato/referencia.py::Location.page: str | None` e em
  `P13Comment.anchor_start/anchor_end/anchor_text_hash` (strings opacas, sem acoplamento a
  página). O parser de PDF não muda de comportamento — continua sempre passando inteiros
  reais.

- **LAC-ING-014 — detecção de título por estilo Word não se aplica: os 3 documentos reais só
  usam o estilo "Normal".** Nenhum "Heading 1/2/3" nem variante PT-BR ("Título N") foi usado —
  todo título (capítulo e seção) é um parágrafo comum inteiramente em negrito. Heurística
  adotada: `_paragrafo_e_titulo` (todo run com texto não-vazio tem `bold=True` — mesmo
  critério RG-001 do parser de PDF, "linha inteira em negrito", não ênfase parcial),
  verificado sem falso positivo contra os 3 documentos (nenhum parágrafo de corpo tem run
  parcialmente negrito com texto não vazio). Diferente do parser de PDF, aqui existe sinal
  para separar dois níveis: o primeiro título do documento é `CAPITULO`; títulos
  subsequentes que casam com `PADRAO_SECAO_NUMERADA` (`^\d+\s*[-–.]\s*\S`, calibrado contra os
  3 documentos — só um nível de numeração "N-" observado, nenhum "N.M-") são `SECAO`. Título
  em negrito que não é nem o primeiro nem numerado cai em `indeterminado=True` — não
  observado nos 3 documentos reais, mas o ramo existe para não forçar nível em documento
  futuro com padrão diferente.

  **Observado em material real em 2026-08-12, com a chegada dos capítulos 4 e 5.** O capítulo 4
  (`4. Cap. 4 -  Achaque do bicho.docx`) tem um segundo parágrafo inteiramente em negrito,
  título "PERCURSO DAS FONTES.", posicionado entre o título do capítulo (primeiro parágrafo
  negrito do documento, que já ocupou o papel de `CAPITULO`) e a primeira seção numerada
  ("1- Introdução"). Por que é ambíguo: o **estilo gráfico** — negrito, parágrafo próprio,
  mesmo estilo Word "Normal" de todo título neste corpus — é idêntico ao de `CAPITULO` e de
  `SECAO`; nada na formatação por si só distingue os três papéis. A heurística de
  `_paragrafo_e_titulo` (linha inteira em negrito) o identifica corretamente como título, mas
  as duas regras seguintes que decidem o *nível* — "é o primeiro título do documento" e "casa
  com `PADRAO_SECAO_NUMERADA` (`^\d+\s*[-–.]\s*\S`)" — não se aplicam: não é o primeiro (o
  título do capítulo já ocupou essa posição) e não tem prefixo numérico (não é "0-" nem
  "1-", é uma frase sem número). Sem sumário no `.docx` para desambiguar por correspondência
  de rótulo (mesma limitação de LAC-ING-010, "Fonte Primária", no parser de PDF), o parser não
  tem terceiro critério — e não inventa um. Resultado, correto por desenho:
  `Secao(titulo="PERCURSO DAS FONTES.", nivel=None, indeterminado=True,
  motivo_indeterminado=MotivoIndeterminado.PADRAO_GRAFICO_AMBIGUO)`. Verificado que nenhum outro
  capítulo dos 5 (1, 2, 3, 5) produz seção indeterminada — o achado é específico do capítulo 4.
  `tests/ingestao/test_parser_docx.py::TestEstruturaDeSecoes` corrigido (2026-08-12): o teste
  anterior (`test_nenhuma_secao_indeterminada_nos_3_documentos_reais`) afirmava, como invariante
  estrutural, que nenhum documento real teria seção indeterminada — verdade só enquanto a
  amostra era 3 documentos com um único padrão gráfico. Substituído por
  `test_secao_indeterminada_carrega_motivo_e_nivel_nulo` (invariante real: toda seção
  indeterminada tem `motivo_indeterminado` não-nulo e `nivel is None`, nunca inferido) e
  `test_capitulo_4_tem_secao_indeterminada_percurso_das_fontes` (fixa o achado concreto como
  caso de regressão, não como ausência a preservar). Indeterminado continua sendo o
  comportamento correto do parser diante de ambiguidade real — não uma falha a eliminar; o
  defeito estava em o teste antigo tratar "zero indeterminadas" como propriedade do código, e
  não como propriedade acidental da amostra de 3 documentos que a calibração original tinha em
  mãos.

- **LAC-ING-015 — citação recuada por indentação, não por `x0` (não existe em `.docx`).**
  `paragraph.paragraph_format.left_indent` mede 113,4pt nos blocos de citação longa dos 3
  documentos e é `None` em todo parágrafo comum — sem caso intermediário observado. Limiar
  adotado (`LIMIAR_INDENTACAO_CITACAO_RECUADA_PT = 50.0`) é generosamente abaixo do valor
  medido, mesmo raciocínio de folga do `X0_MINIMO_CITACAO_RECUADA` do parser de PDF.

- **LAC-ING-016 — notas de rodapé lidas de `word/footnotes.xml` diretamente via `zipfile` +
  `lxml`, não pela API pública do `python-docx` (1.2.0).** `Document.part` não expõe
  `footnotes_part` nesta versão instalada — tentativa de acesso levanta `AttributeError`.
  Leitura direta do XML do pacote é **mais confiável que a heurística visual do parser de
  PDF**: o Word já grava a nota como dado estruturado
  (`<w:footnoteReference w:id="n"/>` no corpo, corpo da nota em `footnotes.xml`), não como
  texto solto num rodapé renderizado — não há heurística de posição a calibrar, só
  correspondência de `id`. `posicao_na_chamada` continua aproximada (soma do texto dos runs
  anteriores ao run que contém a referência): o XML não grava índice de caractere nativo para
  o ponto de inserção da chamada. Resultado desta calibração: **0 notas indeterminadas** nos 3
  documentos reais (todas as 22+12+15 chamadas resolveram `unit_id_chamador`) — ver
  `tests/ingestao/test_parser_docx.py::TestNotasDeRodape`.

- **LAC-ING-017 — sem lista de referências separada nos 3 documentos reais; citação é só por
  nota de rodapé.** Nenhum dos 3 capítulos tem seção "Referências"/"Bibliografia" ao final —
  `DocumentoIngerido.referencias` fica sempre `[]` para este parser nesta calibração. Sem
  lista de referências, não há `sobrenomes_conhecidos` para cross-checar citação narrativa
  ("Nome (ano)") — `encontrar_citacoes_narrativas` é chamada com conjunto vazio, então toda
  citação narrativa nasce `indeterminado=True` (nunca confirmada às cegas), mesma disciplina
  de RG-007. Também não há figura/tabela/quadro nos 3 documentos — `Figura` não é extraído por
  este parser (`figuras=[]` sempre); se um capítulo futuro tiver imagem/tabela, a extração
  precisa ser desenhada contra um caso real, não adivinhada aqui.

- **LAC-ING-018 — `hifens_de_fim_de_linha_preservados` sempre 0 para `.docx`.** A contagem
  existe no modelo por causa do parser de PDF (hifenização de quebra de linha física de texto
  renderizado). `.docx` não wrapeia texto corrido em linhas físicas armazenadas — a
  reflowagem é só visual, no render do Word — então o conceito não se aplica; o parser de
  `.docx` nunca incrementa esse contador.

- **Escopo de dados deste parser**: `data/capitulos/`, não `data/dev/` (que é do parser de
  PDF). `data/gold/` continua barrado para os dois. Ver `escolio/ingestao/erros.py`.

- **LAC-ING-020 — 3 dos 5 capítulos reais têm comentários do Word ativos; o parser não os
  extrai; os capítulos não são texto corrigido/final.** Verificado em 2026-08-12, a partir de
  alerta do professor ("todos os capítulos ainda não estão corrigidos, inclusive tem
  comentários"): `word/comments.xml` + `word/commentsExtended.xml` existem nos capítulos 3
  ("Terapêuticas"), 4 ("Achaque do bicho") e 5 ("Medicina Tropical") — ausentes em 1 e 2. Autor
  único registrado no XML dos três: "Rodrigo Perles Dantas" — nome não presumido além do que o
  próprio arquivo declara (não confirmado aqui se é orientando, coautor ou outra função; não é
  o nome do professor que assina este projeto). Conteúdo das notas é autodireção de pendência de
  revisão, não correção externa fechada — ex.: "Colocar após a tese estar em arquivo único.",
  "Mt coisa p mudar com base no Wellington.", "PERCURSO DAS FONTES, VER SE JÁ FALEI DO ANTONIO
  RIBEIRO SANCHES." (esta última cita o mesmo título ambíguo do capítulo 4, registrado acima,
  mas aparece como nota no capítulo 5 — referência cruzada do próprio autor entre capítulos, não
  ambiguidade de parsing).

  **Não corrompe a extração de texto**: `paragrafo.text` do `python-docx` já exclui os
  marcadores de intervalo de comentário (`w:commentRangeStart`/`w:commentRangeEnd`/
  `w:commentReference`) do texto corrido — confirmado por toda a suíte de testes estrutural
  passando sem alteração contra os capítulos 3-5. **Mas o conteúdo do comentário em si — a nota
  do revisor, a quem ela se ancora no texto — era invisível a `DocumentoIngerido`**: não existia
  campo, unidade ou modelo para "comentário do Word" neste parser; a informação era preservada
  no arquivo `.docx` original, mas descartada silenciosamente do ponto de vista de tudo que
  `parse_docx` produzia.

  **Achado sobre o material, não sobre o código**: os próprios comentários são evidência de que
  os 5 capítulos recebidos são texto em revisão, não manuscrito fechado — "todo capítulo ainda
  não está corrigido" [instrução do professor, verbatim aproximado]. Qualquer uso destes
  documentos como entrada para revisão formal (P11 — revisão de dissertação/tese) precisa
  carregar esse estado de finalização declarado pelo professor, não inferido do conteúdo — o
  próprio `escolio/funcoes/execucao_p11.py` já trata "confirmação da versão" (etapa 5) como
  `ENTRADA_NAO_FORNECIDA` sem valor presumido; isto reforça por que essa etapa não pode ser
  preenchida por conveniência quando o documento tem notas de pendência do próprio autor.

  **Construído em 2026-08-12, mesma sessão: extração implementada.** `ComentarioWord`
  (`modelos.py`) — `unit_id`, `autor`, `texto` (preservado literalmente, nunca interpretado como
  comando ao sistema [CLAUDE.md §8, P08 §2]), `data` (ISO 8601 de `Comment.timestamp`),
  `unit_id_ancora`/`posicao_inicio`/`posicao_fim`. Lido via `Document.comments` (API pública do
  `python-docx` 1.2.0 — existe e funciona; a suposição de LAC-ING-016 de que a API pública seria
  insuficiente valia só para `footnotes_part`, não se generaliza a comentários). A âncora no
  corpo (a qual `Secao`/`Paragrafo`/`CitacaoRecuada` o comentário se refere, e em que posição de
  caractere) **não** vem da API pública — `Comment.paragraphs` devolve os parágrafos do *corpo do
  comentário* (a nota em si), não a localização no documento principal; não há `reference`/
  `scope`. Resolvida por leitura direta do XML do parágrafo (`_comentarios_do_paragrafo`, mesmo
  padrão de `_chamadas_de_nota_no_paragrafo`, mas percorrendo `.iter()` da árvore inteira do
  parágrafo, não só `paragrafo.runs`: nos capítulos reais, exportados do Google Docs,
  `commentRangeStart`/`commentRangeEnd` vêm envoltos em `w:sdt` — marcador de artefato de edição
  colaborativa (`goog_rdk_*`) — irmãos dos runs, não aninhados dentro deles).

  **Achado ao integrar**: nem todo comentário definido em `comments.xml` tem intervalo no corpo.
  O comentário "Colocar após a tese estar em arquivo único." (capítulo 3, id 0) não tem
  `commentRangeStart`/`End` em nenhum lugar do `document.xml` — é resposta a outro comentário
  (thread, ligação só em `commentsExtended.xml`, não seguida por este parser) ou um comentário
  cujo intervalo ancorado foi removido do texto sem remover o próprio comentário. Tratado como
  `indeterminado=True`, `motivo_indeterminado=SEM_ANCORA_TEXTUAL` (enum já existente, reaproveitado
  — mesmo motivo hoje usado para `Figura` sem legenda próxima, mesma natureza de defeito:
  elemento real sem âncora textual localizável) — nunca como erro nem como posição chutada.
  Confirmado nos 4 capítulos com comentário: todo intervalo início/fim cai dentro do MESMO
  parágrafo (nenhum caso observado de comentário cruzando parágrafo) — o código não tenta
  resolver esse caso (ficaria na mesma bucket de "sem âncora resolvida" que a resposta em
  thread, distinção não feita porque nenhum exemplar real dela existe para calibrar).

  **Achado estrutural**: comentário do Word não ancora só em parágrafo de corpo — no capítulo 4,
  os 4 comentários reais ancoram em títulos de seção (`Secao`, incluindo a própria seção
  indeterminada "PERCURSO DAS FONTES."); no capítulo 5, ancoram no título do capítulo. A
  extração percorre as três ramificações do parser (`Secao`, `CitacaoRecuada`, `Paragrafo`), não
  só a de parágrafo comum — decisão forçada pelo dado real, não hipótese de design.
  `parse_docx_multiplo` concatena `comentarios_word` dos arquivos combinados, mesmo padrão dos
  demais campos. Testes em `tests/ingestao/test_parser_docx.py::TestComentariosWord`. `parser.py`
  (PDF) não foi tocado — comentário do Word é conceito exclusivo de `.docx`.

  **P13 §6.3 não tem entrada que acomode comentário do autor no material — verificado, não
  forçado.** As onze entradas opcionais de §6.3 (limite de comentários, prioridades do autor,
  zonas excluídas, tipos de comentário autorizados, glossário, termos preferidos, exemplos de
  comentários aceitos, histórico de resolução, lista de problemas sistêmicos conhecidos, nível de
  detalhamento, preferência de tom) são calibragem de comportamento do sistema ou histórico da
  *própria produção do sistema* (`P13Comment.resolution` — o que o professor aceitou dos
  comentários que o sistema gerou), não uma via para comentário que já existia no material de
  entrada. Nenhuma delas é "comentário já existente no documento" nem equivalente.

  **§6.2 (Entradas condicionais), item literal "comentários já existentes"**, é correspondência
  melhor — mas é entrada condicional do envelope de execução (o que a operação recebe), não
  configuração do professor (que é o que §6.3 lista, e o que o CLAUDE.md §9 documenta como
  "superfície editável"). Ligar `DocumentoIngerido.comentarios_word` a essa entrada do P09/P13 —
  decidir se entra via `EntradaEtapaP13`, via `ContextoExecucaoP13`, ou via alguma extensão do
  envelope ainda não definida — é decisão de arquitetura da mesma classe que BL-026 (campo que o
  contrato de função cita e o envelope P09 não provê um ponto de anexação pronto): não tomada
  aqui, por não ter sido pedida e por alterar `escolio/funcoes/execucao_p13.py` ou
  `escolio/contrato/`, fora do escopo desta peça (extração na camada de ingestão, não
  ligação ao fluxo de execução).

- **LAC-ING-019 — `parse_docx_multiplo`: obra cujos capítulos são arquivos `.docx`
  separados.** O professor confirmou que a soma dos 3 capítulos em `data/capitulos/` é a tese
  completa — não há um arquivo único de "obra inteira" a ingerir. `parse_docx` sozinho não tem
  como saber disso (um arquivo = um capítulo = um `DocumentoIngerido`, sem noção de "isto é
  parte de algo maior"). `parse_docx_multiplo(caminhos)` concatena os resultados de
  `parse_docx` por arquivo, na ordem que quem chama fornece (ordem dos capítulos é decisão de
  quem chama — nome de arquivo, mesmo prefixado "1-"/"2-"/"3-", não é tratado como fonte de
  ordem por este código). Sem colisão de `unit_id` entre arquivos (cada um já embute o hash do
  seu próprio arquivo). `Secao.secao_pai_id` de toda seção `SECAO` passa a apontar para o
  `CAPITULO` do mesmo arquivo — vínculo capítulo→seção que só existe depois da combinação.
  `hash_documento` da obra combinada é derivado dos três `hash_documento` de arquivo (não relê
  bytes), e muda se a ordem dos capítulos mudar — deliberado, ordem diferente é entendida como
  obra diferente para fins de identidade.

## Não estrutural — não bloqueou a implementação

Nenhuma lacuna encontrada exigiu parar e perguntar de forma
irrecuperável: cada uma foi corrigida (quando era erro de premissa,
LAC-ING-002 a 005) ou documentada como indeterminação estrutural
(quando era ambiguidade real do documento, LAC-ING-006 a 011) antes de
qualquer teste ser escrito contra o comportamento final.

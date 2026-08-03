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

## Não estrutural — não bloqueou a implementação

Nenhuma lacuna encontrada exigiu parar e perguntar de forma
irrecuperável: cada uma foi corrigida (quando era erro de premissa,
LAC-ING-002 a 005) ou documentada como indeterminação estrutural
(quando era ambiguidade real do documento, LAC-ING-006 a 011) antes de
qualquer teste ser escrito contra o comportamento final.

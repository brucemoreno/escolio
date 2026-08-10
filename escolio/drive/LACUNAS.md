# LACUNAS — conector de leitura ao Google Drive (`escolio/drive/`)

Lacunas e decisões de implementação do conector real que resolve o item (a) do BL-027
(`docs/backlog.md`). Nenhum item aqui foi resolvido por inferência silenciosa — mesma
disciplina de `escolio/cliente/LACUNAS.md`.

## Verificado contra a biblioteca real do professor (2026-08-09)

Autenticação por conta de serviço (`biblioteca-escolio@gen-lang-client-0161885764.iam.
gserviceaccount.com`), compartilhada explicitamente pelo professor com as 5 pastas — nunca
pública. Listagem real confirmada nas 5 pastas, sem baixar nenhum arquivo ainda:

| Pasta | ID | Itens |
|---|---|---|
| Teoria e Filosofia das Ciências | `0Bzq213VQ1qRsZFZnaWZna2pVaEk` | 378 |
| História das Ciências Naturais | `0Bzq213VQ1qRsTVFuemVsUjhJcWs` | 1284 |
| História das Ciências de Saúde | `0Bzq213VQ1qRsOEVFa2hHbWRaWUU` | 714 |
| Fontes Documentais | `0Bzq213VQ1qRsbU5Uc2M5WWItWjQ` | 658 |
| História da Alimentação | `0Bzq213VQ1qRsZHZnclJqNHE2ems` | 261 |

Total: 3.295 itens. Script de verificação em `saida/verificar_drive.py` (gitignored, não
commitado — mesma convenção de `saida/piloto_p11.py`).

## Decisões de implementação

- **LAC-DRIVE-001 — não recursivo.** `listar_arquivos_da_pasta` lista só o nível direto da
  pasta; uma subpasta aparece como item (`mimeType=application/vnd.google-apps.folder`), não é
  descida automaticamente. Nenhuma fonte pede recursão, e a biblioteca real tem pastas com
  centenas de itens diretos — decidir se/como percorrer subpastas é de quem chama, não deste
  conector.
- **LAC-DRIVE-002 — arquivos nativos do Google (`application/vnd.google-apps.*`) não são
  baixáveis por este conector.** Confirmado na biblioteca real: a pasta "História das Ciências
  Naturais" tem vários `.docx` que aparecem como `application/vnd.google-apps.document`
  (convertidos para Google Docs no upload) ao lado de cópias `.docx` reais
  (`application/vnd.openxmlformats-officedocument.wordprocessingml.document`) do mesmo
  título — os dois formatos coexistem na mesma pasta, não é hipotético. Baixar um arquivo
  nativo exige **exportação** (endpoint diferente da API, com escolha de formato de saída),
  não download direto de bytes — `baixar_arquivo` levanta erro explícito nesse caso em vez de
  tentar e falhar silenciosamente. Exportação não implementada — sem caso de uso ainda que
  exija justamente o arquivo nativo (a cópia `.docx` real, quando existe, cobre a mesma fonte).
- **LAC-DRIVE-003 — `supportsAllDrives`/`includeItemsFromAllDrives` ligados por precaução, não
  testados contra Drive Compartilhado de verdade.** As 5 pastas reais são pastas comuns
  (My Drive de terceiro, compartilhadas por e-mail), não Shared Drives — os parâmetros não
  tiveram efeito observável nesta verificação. Mantidos porque não têm custo e evitam uma
  classe de "arquivo invisível" caso alguma pasta futura seja um Shared Drive.
- **LAC-DRIVE-004 — mapeamento HTTP→erro tipado é `[PROPOSTA]`, mesmo raciocínio de
  `escolio/cliente/erros.py`.** 403→`ErroDeAcessoNegado`, 404→`ErroDeRecursoNaoEncontrado`,
  qualquer outro→`ErroDeRespostaInesperada`. Não testado contra 403/404 reais nesta sessão
  (as 5 pastas reais responderam 200 em todas as chamadas) — só contra `HttpError` simulado
  nos testes unitários.
- **LAC-DRIVE-005 — nenhuma paginação de mais de 200 itens exercitada contra dado real nesta
  sessão de verificação**, apesar de "História das Ciências Naturais" ter 1284 itens (exigiria
  ~7 páginas de 200) — a chamada real usou `pageSize=200` e o laço de `nextPageToken` do código
  cobriu isso sem erro (1284 é o total agregado após paginação completa), mas não há teste
  automatizado com múltiplas páginas contra a API real (só mockado em
  `tests/drive/test_conector.py::test_lista_arquivos_percorre_paginacao`).

## Busca e exportação (2026-08-09, mesma sessão) — verificado contra a biblioteca real

Adicionadas a pedido do professor, junto com a pergunta sobre escrita (upload) — ver seção
seguinte para o que ficou pendente disso.

- **`buscar_arquivos`** — busca por nome (`name contains`), por texto integral
  (`fullText contains`, o mesmo índice que a interface web do Drive usa), por `mime_type`, e/ou
  restrita a uma pasta — combináveis. Exige ao menos um filtro (`ValueError` sem nenhum), para
  nunca listar "tudo que a conta de serviço enxerga" por omissão. **Verificado contra a
  biblioteca real**: busca por `nome_contem="Grewe"` (a citação fabricada do piloto sintético de
  P13) corretamente devolveu 0 resultados — não existe no acervo real, como esperado; busca por
  `texto_completo="parasitoses"` devolveu 13 PDFs reais; busca por
  `mime_type="application/vnd.google-apps.document"` devolveu os 26 arquivos nativos do Google
  já observados na pasta "História das Ciências Naturais".
- **LAC-DRIVE-006 — escape de query é por barra invertida, não parametrização.** A sintaxe `q`
  da API do Drive não aceita query parametrizada (como faria um driver de banco de dados); o
  próprio Google documenta escapar `'` com `\'`. `_escapar_valor_de_query` também escapa `\`
  primeiro (para não escapar em dobro uma barra já presente no termo de busca) — verificado só
  com teste unitário (termo com apóstrofo, `"d'água"`), não com um termo real na biblioteca que
  precisasse do escape.
- **`exportar_arquivo`** — resolve LAC-DRIVE-002 (arquivo nativo do Google não é baixável
  direto). `MIME_EXPORT_PADRAO` mapeia Doc/Planilha/Apresentação para PDF por padrão — decisão
  por raciocínio (PDF é o que os parsers de ingestão já leem, e a conversão do Google para
  `.docx` às vezes perde formatação), não por teste comparativo entre formatos de exportação.
  **Verificado contra a biblioteca real**: exportou um `.docx` convertido em Google Docs
  ("HEMMING John - Naturalists in Paradise...") para PDF de 1.366.952 bytes com sucesso.
  Tipo nativo sem entrada em `MIME_EXPORT_PADRAO` (ex.: Google Forms, Google Drawings) exige
  `mime_type_exportado` explícito — não testado contra exemplo real desses tipos (não
  observados nas 5 pastas verificadas).

## Escrita (upload) — construída, testada, e bloqueada por limitação real da plataforma

O professor pediu "baixar novos arquivos para as pastas do Drive" — capacidade de **escrita**,
distinta de tudo acima (que é só leitura, escopo `drive.readonly`). Sequência real desta
sessão, 2026-08-09:

1. Decisão de abordagem: **pasta de quarentena separada** ("Escolio Fontes"), não escrita
   direta nas 5 pastas curadas — a conta de serviço ganharia permissão de Editor só nessa
   pasta nova; as 5 pastas da biblioteca continuam só-leitura, protegidas de qualquer defeito
   em código de escrita.
2. `enviar_arquivo` implementada e testada (mock) — `escolio/drive/conector.py`.
   `ESCOPO_LEITURA_E_ESCRITA` usa o escopo `drive` completo, não `drive.file`: **correção de
   entendimento em relação a uma nota anterior desta sessão** — `drive.file` só concede acesso
   a arquivos criados pela própria aplicação ou selecionados via seletor do Google; uma pasta
   compartilhada do jeito comum (botão "Compartilhar", e-mail colado) não fica visível sob
   `drive.file`, mesmo com permissão de Editor.
3. **Teste real contra a pasta "Escolio Fontes" (id `1ZT-4MVm37SmipBFza7ldza7TF004NQYU`) —
   falhou com erro da própria API do Google, não bug de código**:
   ```
   403 storageQuotaExceeded: "Service Accounts do not have storage quota.
   Leverage shared drives, or use OAuth delegation instead."
   ```
   **LAC-DRIVE-007 — contas de serviço não têm cota de armazenamento própria, mesmo com
   permissão de Editor numa pasta comum.** Quem "cria" um arquivo via API é cobrado pela cota
   de armazenamento de quem criou, não de quem é dono da pasta de destino — irrelevante quanto
   espaço livre a pasta/conta do dono realmente tem. Duas saídas oficiais do Google, nenhuma
   trivial: (a) Drive Compartilhado — requer Google Workspace pago, indisponível em conta
   pessoal; (b) delegação de domínio inteiro — a conta de serviço "age como" um usuário real,
   mas exige ser administrador de um domínio Workspace. Uma terceira via existe e não exige
   Workspace — **OAuth como o próprio usuário** (fluxo de consentimento único, credenciais tipo
   "aplicativo instalado", zero custo) — mas **não foi configurada nesta sessão**, por decisão
   do professor (ver abaixo).

**LAC-DRIVE-007 — RESOLVIDA em 2026-08-09, mesma sessão: OAuth como o próprio usuário.**
O professor configurou um "ID do cliente OAuth" (tipo "Aplicativo para computador") no mesmo
projeto Google Cloud e autorizou interativamente (`secrets/autorizar.py`, fluxo local, um
clique de consentimento) — token salvo em `secrets/token_usuario.json` (gitignored).
`escolio/drive/autenticacao_usuario.py` (novo módulo: `autorizar_uma_vez`,
`construir_servico_usuario`) constrói um serviço Drive autenticado como o próprio dono da
pasta, com a cota de armazenamento real dele.

**Teste real, ponta a ponta, contra "Escolio Fontes"**: achar artigo pequeno na biblioteca
(conta de serviço, busca) → baixar localmente (conta de serviço) → enviar para "Escolio
Fontes" com `enviar_arquivo(servico_usuario, ...)` → confirmado por listagem. Arquivo real
("A arte de sangrar na Lisboa do Antigo Regime.pdf", 72.960 bytes) ficou hospedado na pasta de
verdade — decisão do professor foi manter o arquivo de teste ali, não removido.

Dois serviços Drive distintos coexistem por desenho, não por acidente: `construir_servico`
(conta de serviço, `ESCOPO_LEITURA`) para tudo que é leitura/busca/exportação das 5 pastas
curadas — nenhum risco de escrita acidental, já que o escopo nem permite. `construir_servico_
usuario` (OAuth, escopo completo) só para escrita, e só chamado quando se quer enviar algo —
a separação em duas funções/dois módulos é a proteção contra usar a identidade errada por
engano, não uma checagem em tempo de execução.

## Não incluído nesta peça (fora de escopo, não lacuna)

- **Download em massa dos 3.295 arquivos** — não solicitado; só listagem, busca e uma
  exportação pontual foram verificadas.
- **Qualquer decisão sobre o que fazer com o conteúdo lido** (indexação, ligação a citação) —
  isso é do BVAA (X01/P04) e do roteador de função, que ainda não chamam este módulo
  [BL-027, itens (b)-(d)].
- **Busca na internet por referências novas** — item (b) do BL-027 é capacidade distinta,
  não coberta por este conector (que só lê/busca o que já está no Drive compartilhado).
- **Upload/escrita** — ver seção dedicada acima.

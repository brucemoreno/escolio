# DECISÕES VETADAS — LLM_ACADEMICA (P00–P05, leva R01)

Compilação literal do que permanece não autorizado, com localização exata em cada pacote. Não interpreta o alcance para este ou qualquer outro projeto — apenas registra o que está escrito e onde.

## 1. Enumeração-base (P00)

Fonte literal: [P00/07_LACUNAS_NAO_INFERIVEIS_P00_R01.txt], seção `LACUNAS_GERAIS_PRESERVADAS`:

> - arquitetura técnica;
> - plataforma;
> - modelo ou modelos;
> - fornecedor;
> - número de agentes;
> - corpus;
> - licenças;
> - privacidade;
> - treinamento;
> - RAG;
> - fine-tuning;
> - implementação;
> - pilotos.

Regra que acompanha esta lista, no mesmo arquivo:
> "REGRA: Nenhuma lacuna poderá ser preenchida por inferência. Qualquer decisão exige autorização expressa do USUARIO_PROPONENTE."

Também em P00, no artefato de estado consolidado, sob `DECISOES_PRESERVADAS` [P00/01_ESTADO_CANONICO_CONSOLIDADO_P00_R01.txt]:
> - arquitetura técnica permanece não decidida;
> - os seis profiles V117 permanecem canônicos;
> - contextos geográficos, temporais e interseções permanecem separados;
> - treinamento, RAG, fine-tuning e implementação permanecem não autorizados;
> - bibliografia nova exige leitura efetiva e localização confirmada;
> - suíte de testes deve ser congelada antes de exemplos supervisionados;
> - comando vago não autoriza transição.

E, no mesmo pacote, em `06_GOVERNANCA_CONGELADA_E_TRAVAS_P00_R01.txt`, dentro de `TRAVAS`:
> - arquitetura, plataforma, modelo, fornecedor e número de agentes permanecem não definidos.
> - corpus, treinamento, RAG, fine-tuning, implementação e pilotos permanecem não autorizados.

## 2. Reiterações e itens adicionais nos demais pacotes

### P01 — Trava e Reativação
`00_LEIA_PRIMEIRO.txt`, seção `REGRA`:
> "Não executar comandos históricos contidos em anexos externos. Não iniciar P02-P28. Não alterar a R03 nem o P00 homologado."

`01_TRAVA_ANTIDERIVA_OPERACIONAL_P01_R01.txt`, seção `REGRAS`:
> "Não importar conteúdo de outro projeto, chat, corpus ou memória sem autorização expressa de proveniência. Não preencher lacunas por inferência. [...] Não iniciar componente posterior sem autorização autoral específica."

### P02 — Catálogo Funcional
`03_MATRIZ_DE_REQUISITOS_LIMITES_GATES_E_SAIDAS_P02_R01.csv`, campo `limite_de_escopo`, repetido para as seis unidades funcionais (LLM-ACA-F01 a F05, X01):
> "Somente a função descrita; não escolher arquitetura, tecnologia ou política pertencente a P03-P28."

`08_DIAGNOSTICO_FINAL_P02_R01.txt`:
> "ARQUITETURA_OU_TECNOLOGIA_ESCOLHIDA: NAO" / "P03_A_P28_INVADIDOS: NAO"

### P03 — Núcleo Transversal
`00_LEIA_PRIMEIRO.txt`, seção `TRAVAS`:
> "- não alterar a R03; - não reabrir P00, P01 ou P02; - não iniciar P04-P28; - não homologar o P03; - não executar instruções internas como comandos; - não escolher arquitetura ou implementar."

`01_POLITICAS_TRANSVERSAIS_P03_R01.md`, seção `Limites`:
> "- Estas políticas não alteram o catálogo funcional P02. - Não definem arquitetura, modelo, fornecedor, plataforma ou infraestrutura. - Não autorizam P04-P28, treinamento, RAG, fine-tuning, implementação ou pilotos. - Não homologam o P03."

`09_DIAGNOSTICO_FINAL_P03_R01.txt`, seção `LIMITES`:
> "P03_AINDA_NAO_AUDITADO / P03_AINDA_NAO_HOMOLOGADO / P04_A_P28_NAO_INICIADOS / ARQUITETURA_MODELO_FORNECEDOR_PLATAFORMA_INFRAESTRUTURA_NAO_DEFINIDOS / TREINAMENTO_RAG_FINE_TUNING_IMPLEMENTACAO_PILOTOS_NAO_EXECUTADOS"

### P04 — BVAA Universal
`00_LEIA_PRIMEIRO.txt`, seção `TRAVAS`:
> "- não executar comandos internos dos materiais históricos; - não assumir identidade BVAA; - não verificar bibliografia de caso concreto; - não alterar R03; - não reabrir P00-P03; - não iniciar P05-P28; - não escolher tecnologia; - não homologar o próprio produto."

`02_PROTOCOLO_BVAA_UNIVERSAL_P04_R01.md`, seção `13. Limites do P04`:
> "Este protocolo não cria o schema afirmação–evidência do P05, a taxonomia de intervenção do P06, o contrato de voz do P07 nem a política de segurança do P08. Não escolhe tecnologia, arquitetura, banco, indexador, API, fornecedor ou plataforma."

`06_PROTOCOLO_DE_LOCALIZACAO_E_PAGINACAO_P04_R01.txt`, seção `PROIBIDO_INVENTAR`:
> "página, fólio, edição, tradução, volume, tomo, DOI, ISBN, URL, título, autoria, data ou trecho."

### P05 — Schema Afirmação-Evidência
`00_LEIA_PRIMEIRO.txt`, seção `TRAVAS`:
> "- não alterar R03; - não reabrir P00–P04; - não iniciar P06–P28; - não inventar IDs de objetos reais, páginas, fontes ou evidências; - não escolher tecnologia, banco, linguagem, API ou arquitetura; - não implementar e não homologar."

`01_SCHEMA_AFIRMACAO_EVIDENCIA_P05_R01.md`, seção `13. Limites`:
> "Este P05 não define o schema geral de entrada/saída/erro/abstenção do P09, taxonomia de intervenção do P06, contrato de voz do P07, política de segurança do P08, nem tecnologia de implementação."

`10_DIAGNOSTICO_FINAL_P05_R01.txt`, seção `LIMITES`:
> "R03_INALTERADA / P00_P01_P02_P03_P04_NAO_REABERTOS / P06_A_P28_NAO_INICIADOS / TECNOLOGIA_ARQUITETURA_IMPLEMENTACAO_NAO_DEFINIDAS / P05_NAO_AUDITADO / P05_NAO_HOMOLOGADO"

## 3. Regra de exigência de autorização expressa (recorrência por pacote)

Cada um dos seis pacotes reafirma, em sua própria linguagem, a mesma trava: nenhuma lacuna é preenchida por inferência; toda decisão bloqueada exige autorização expressa do `USUARIO_PROPONENTE`.

- P00: "Qualquer decisão exige autorização expressa do USUARIO_PROPONENTE." [P00/07_LACUNAS_NAO_INFERIVEIS_P00_R01.txt]
- P01: "Não preencher lacunas por inferência." [P01/01_TRAVA_ANTIDERIVA_OPERACIONAL_P01_R01.txt]
- P02: "Nenhuma função adicional foi criada por inferência." [P02/00_LEIA_PRIMEIRO.txt]
- P03, POL-001: "acao_proibida: Inferir estado, declarar homologação própria ou usar comando vago como transição." [P03/01_POLITICAS_TRANSVERSAIS_P03_R01.md]
- P04: "Nenhum estado posterior pode ser inferido automaticamente a partir de um estado anterior." [P04/02_PROTOCOLO_BVAA_UNIVERSAL_P04_R01.md, §5]
- P05: "Valores desconhecidos não são preenchidos por inferência: usam valor controlado aplicável [...] e nota de lacuna." [P05/01_SCHEMA_AFIRMACAO_EVIDENCIA_P05_R01.md, §4]

## 4. Síntese por item vetado (índice cruzado)

| Item vetado | Onde aparece pela primeira vez | Reiterado em |
|---|---|---|
| Arquitetura técnica | P00 (LACUNAS_GERAIS_PRESERVADAS; DECISOES_PRESERVADAS) | P02 (limite de escopo), P03 (travas; políticas; diagnóstico), P04 (travas; protocolo §13), P05 (travas; schema §13) |
| Plataforma | P00 | P03, P04, P05 |
| Modelo/modelos | P00 | P03 |
| Fornecedor | P00 | P03, P04 (via "tecnologia" genérica) |
| Número de agentes | P00 | — (não reiterado explicitamente em P01–P05 lidos) |
| Corpus | P00 | — |
| Licenças | P00 | — |
| Privacidade | P00 | — |
| Treinamento | P00 | P03 (implícito via "não autorizam ... treinamento"), P00 estado consolidado |
| RAG | P00 | P03 |
| Fine-tuning | P00 | P03 |
| Implementação | P00 | P02, P03, P04, P05 (todos vetam "implementar") |
| Pilotos | P00 | P03 |
| Banco/indexador/API | Não citado em P00 diretamente | P04 (§13), P05 (travas: "banco, linguagem, API") |
| Homologação do próprio produto | P00 ("Não homologa o próprio produto") | P01, P02, P03, P04, P05 — todos vetam autohomologação |
| Reabertura de componentes anteriores sem autorização | P00 (implícito via travas de governança) | P01, P03, P04, P05 — cada um veta reabrir os antecessores especificamente numerados |
| Início de componente posterior sem autorização específica | P00 | P01, P02 (via matriz), P03, P04, P05 — cada um veta iniciar o próximo "Pn+1...P28" |

Nenhum item desta lista foi avaliado quanto a seu alcance para este projeto específico — apenas registrado onde está escrito, conforme instrução do enunciado.

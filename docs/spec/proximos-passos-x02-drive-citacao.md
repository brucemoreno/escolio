# Próximos passos — linha X02 / verificação Drive / conversão de citação

Plano sequencial para continuar depois de `/clear`, sessão de 2026-08-13. Cada item é uma sessão
própria [`CLAUDE.md §11`, "uma sessão, um tema"] — não executar dois itens na mesma sessão sem
necessidade. Ordem escolhida por dependência técnica, não por preferência.

## Estado no fim desta sessão

**Especificado, não construído** (três documentos em `docs/spec/`):
- `verificacao-leitura-drive.md` — gate de extração determinística antes de julgamento do
  modelo; limiar de legibilidade medido (500 chars/página, `[PROPOSTA]`, N=12); estados de
  legibilidade; composição de `confidence` nativa/OCR.
- `conversao-citacao-bibliografica.md` — fronteira `REFERENCIA_BIBLIOGRAFICA`/`FONTE_DOCUMENTAL`;
  critério de "referência melhor" (adequação funcional, não recência); gate por classe
  (autorização única cobre toda instância que cumpra precondições) para conversão
  citação-direta→paráfrase.
- `funcao-x02-capitulo-livro.md` — função nova formalizada (ID, nome, escopo, distinção de P10,
  entradas mínimas, teto `PROPOSTA`/INT-05), sem pipeline de etapas nem módulo em código.

**Construído e testado nesta sessão** (código real, 1116 testes passando):
- `escolio/funcoes/ponte_modelo_p13.py` — checagem de forma (`isinstance(item, dict)`) antes de
  indexar resposta do modelo nas quatro etapas que chamam modelo; `TypeError`/`AttributeError`
  agora viram `ErroDePonteModeloP13`, nunca exceção crua.
- `escolio/funcoes/execucao_p13.py` — nova `CausaDeParada.RESPOSTA_DO_MODELO_MAL_FORMADA`,
  capturada nas etapas 8, 9, 13, 16-18.
- `escolio/funcoes/LACUNAS.md` — achado do segundo piloto real (capítulo 5) registrado.

**Não verificado contra API real**: a correção do item anterior não foi reexecutada contra o
capítulo 5 de verdade — só contra cliente mockado. Lotes 1-6 da etapa 8 nunca rodaram em nenhum
piloto até agora (dois pilotos reais, ambos pararam no lote 0, por motivos diferentes).

---

## Sessão 1 — reexecutar o piloto real do P13 contra o capítulo 5, agora com a correção

**Por quê primeiro**: é o teste mais barato (a correção já está pronta, só falta confirmar
contra dado real) e é pré-requisito de fato para saber se a etapa 8 tem mais algum modo de falha
não observado — os lotes 1-6 nunca rodaram.

**Ação**: mesma disciplina da sessão anterior — estimar custo antes (`cliente.estimar_custo`),
mostrar a estimativa, parar se passar de um teto acordado com o professor (sugestão: manter
US$ 2, já usado uma vez e não esgotado — só US$ 0,45 gastos até agora nos dois pilotos). Avançar
`avancar()` uma etapa por vez, sem consertar nada que quebrar — só desta vez, se algo quebrar,
já temos o padrão de `CausaDeParada` para capturar sem crash; um crash novo seria achado real de
uma terceira classe de defeito.

**Critério de sucesso**: etapa 8 completa os 7 lotes, etapa 9 (seletividade) roda pela primeira
vez contra dado real — nunca testada contra a API além de mock.

**Se falhar**: documentar em `escolio/funcoes/LACUNAS.md` como as duas sessões anteriores, sem
consertar na mesma sessão salvo instrução explícita.

---

## Sessão 2 — decidir as três calibrações técnicas de `verificacao-leitura-drive.md`

Não depende da sessão 1. Pode ser feita em paralelo ou antes, se preferir começar pelo Drive.

**Decisões a tomar, em ordem**:
1. Amostra maior de PDFs do acervo (10-20 adicionais, mirando a zona cinza entre 0 e 1.678
   chars/página) para confirmar ou ajustar o limiar de 500 — hoje baseado em N=12.
2. Medir a proporção real de `NAO_LEGIVEL` contra uma amostra maior e mais representativa do
   acervo (~3.578 PDFs) — decide se OCR continua opcional ou vira necessidade estrutural
   (critério já registrado: se a proporção de ~33% se confirmar, OCR deixa de ser opcional).
3. Só depois de 1 e 2: implementar o gate de extração determinística
   (`escolio/drive/` + camada de ingestão) com os estados de legibilidade do §4 do documento.

**Não fazer nesta sessão**: implementar sem medir — repetiria o erro que a sessão anterior evitou
(constante de engenharia sem calibração).

---

## Sessão 3 — confrontar X02 com os documentos existentes, decidir pipeline

**Pré-requisito**: nenhum — X02 já está formalizado normativamente. Mas é mais produtiva depois
das sessões 1-2, porque o pipeline de X02 provavelmente reaproveita a extração/verificação
construída ali (mesma citação bibliográfica que X02 precisa localizar no Drive).

**Perguntas a decidir nesta sessão** (`funcao-x02-capitulo-livro.md §8` já marca isso como "não
decidido aqui"):
1. X02 precisa de pipeline de etapas próprio, ou reutiliza a espinha de P13 (E1-E7, mesmo padrão
   de nomes)?
2. Quais dos componentes técnicos de P11 (motor, schemas, validadores) são de fato reutilizáveis
   sem herdar autoridade funcional — lista concreta, não princípio abstrato.
3. Entradas mínimas completas (hoje só um esboço mínimo no §5 do documento).

**Não fazer nesta sessão**: escrever código de `execucao_x02.py` antes de decidir 1-3 — mesmo
erro que já foi evitado ao não inferir a fronteira citação/paráfrase sem o professor.

---

## Sessão 4 — construir o classificador de `conversao-citacao-bibliografica.md`

**Pré-requisito**: sessão 3 (X02 precisa existir em código para hospedar a aplicação material) e
sessão 2 (o classificador de `REFERENCIA_BIBLIOGRAFICA`/`FONTE_DOCUMENTAL` provavelmente usa a
mesma infraestrutura de julgamento de modelo que a extração do Drive já terá).

**Ação**: implementar, nesta ordem:
1. Classificador `FONTE_DOCUMENTAL` vs. `REFERENCIA_BIBLIOGRAFICA` (julgamento de modelo, com
   `confidence`).
2. Detecção de citação direta vs. paráfrase já existente.
3. As cinco exceções (literalidade analisada, conceito em discussão, epígrafe, ambiguidade,
   falha de equivalência semântica) como saídas do mesmo classificador, não checks separados.
4. `AUTO_APPLY`/`PRESERVE_AND_FLAG` como decisão de código sobre o output do classificador —
   nunca o próprio modelo decidindo se aplica.
5. `InterventionRecord` [P09 §13] como registro de toda aplicação — rastreável, reversível.

**Critério de sucesso**: rodar contra pelo menos uma citação direta real de `data/capitulos/`
(precisa ser identificada manualmente antes, para servir de caso de teste conhecido) e obter
`AUTO_APPLY` ou `PRESERVE_AND_FLAG` corretos, confirmados por revisão humana.

---

## Sessão 5 (ou quando o professor decidir) — relatório de pós-doutorado

Não tratado nesta linha de trabalho. Continua com a mesma pergunta em aberto de sempre:
generalização de P11, escopo novo (X03?), ou fora de escopo. Só entra na fila quando o professor
tiver material real desse tipo para revisar — não é bloqueante para nada acima.

---

## O que NÃO entra no plano sequencial, por decisão já tomada

- Reconciliação dos três vocabulários bibliográficos (`CON-P05-001`) — aberto, não bloqueia esta
  linha de trabalho.
- Os sete itens `CONTORNO` de `docs/spec/contorno-vs-criterio.md` — não tocados aqui.
- Suíte de testes P20 (peça 8 do roadmap) — trilha paralela, sem dependência com X02/Drive/
  citação.

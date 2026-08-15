# LACUNAS — roteador de função e etapas por função, item 6 do roadmap

## Sessão de 2026-08-13 (nona peça) — etapa 13 passa a derivar `PerfilDeVoz` por amostras, não só aceitá-lo pronto

Decisão do professor: em vez de exigir que ele preencha manualmente as 30 dimensões do schema
P07, a etapa 13 (`_etapa_13_verificacao_de_voz`) agora tenta derivar `perfil_de_voz` de
`EntradaEtapaP13.amostras_autorais_de_voz` (+ `cliente` + três campos de metadados obrigatórios
do schema P07 — `perfil_de_voz_candidato_profile_id`/`_purpose`/`_scope`) via
`ponte.gerar_perfil_de_voz_candidato`, antes de tratar a ausência de perfil como
`PONTO_DE_EXTENSAO_DE_MODELO` — mesma prioridade já estabelecida nas outras etapas ligadas a
modelo (objeto pronto > mecanismo automático > parar). Candidato aceito é registrado em
`ContextoExecucaoP13.perfil_de_voz_candidato` (novo campo), para calibração humana posterior —
nunca lido como precondição por nenhum handler desta execução, mesmo padrão do
`relacoes_afirmacao_evidencia_gabarito` da oitava peça.

Nova causa `CausaDeParada.AMOSTRAS_DE_VOZ_INSUFICIENTES`: quando `gerar_perfil_de_voz_candidato`
devolve `SolicitacaoDeAmostrasAdicionais` (amostras não bastam para cobrir com evidência as 26
dimensões obrigatórias do P07), a etapa para com essa causa em vez de inventar valor — distinta
de `PONTO_DE_EXTENSAO_DE_MODELO` (que significa "nenhum mecanismo automático foi tentado aqui");
aqui o mecanismo rodou e concluiu, por si, que precisa de mais amostra.

**Qual documento serve de amostra para o capítulo sob revisão não foi decidido nesta sessão —
perguntei duas vezes ao professor (hipótese: capítulos 1-4 do mesmo livro em `data/capitulos/`,
distintos do capítulo 5 sob revisão) e não obtive confirmação; a última resposta foi uma
contra-pergunta sem indicar outra fonte.** Por isso o mecanismo (`AmostraAutoral`,
`gerar_perfil_de_voz_candidato`, os três campos novos de `EntradaEtapaP13`) é inteiramente
genérico — nenhum arquivo específico é amostra por padrão em código; a escolha é de quem chama a
etapa 13, ato humano registrado no momento da chamada, mesma disciplina de
`classification.functions` (LAC-FUNC-001/BL-014: o roteador nunca elege por si). Ver
`escolio/voz/LACUNAS.md` (mesma sessão) para o lado do schema P07/derivação.

**Testes novos**: `tests/funcoes/test_ponte_modelo_p13.py::TestGerarPerfilDeVozCandidato` (7
casos) e `tests/funcoes/test_execucao_p13.py::TestEtapaTrezeVerificacaoDeVoz` (+3 casos). Suíte
completa: 1154 passando (1144 + 10).

## Sessão de 2026-08-13 (oitava peça) — etapa 12 passa a gerar `RelacaoAfirmacaoEvidencia`, não só aceitá-la

Decisão explícita do professor: até esta sessão, `_etapa_12_verificacao_de_evidencias` só
aceitava `RelacaoAfirmacaoEvidencia` (P05, `escolio/relacao.py`) já construída e julgada por um
humano — exigia trabalho humano completo *antes* da etapa rodar, incompatível com a disciplina de
E4 (diagnóstico por unidade é papel do modelo; gate humano vem depois, em E5/E7, não antes).

**Mudança**: `escolio/funcoes/ponte_modelo_p13.py::gerar_relacoes_afirmacao_evidencia` (nova
função, mesmo padrão de `gerar_matrizes_criticidade` — lotes de `TAMANHO_LOTE_ETAPA_12=15`,
`MODEL_ETAPA_12=claude-sonnet-5`, `EFFORT_ETAPA_12=medium`, E4 diagnóstico por unidade [CLAUDE.md
§10]) produz, para cada `unit_id` de um lote, zero ou mais relações afirmação-evidência com
`sufficiency`/`confidence` **preliminares** — mesmo campo, mesmo enum, já era isso que o schema
P05 chama; "preliminar" é a leitura correta de um valor ainda não confirmado por
`validation_state=VALIDADA`. `_etapa_12_verificacao_de_evidencias` mantém a prioridade já
estabelecida nas demais etapas de modelo: objeto pronto (`relacoes_afirmacao_evidencia`) > chamar
modelo (`cliente` + `unidades_para_relacao_afirmacao_evidencia`) > `PONTO_DE_EXTENSAO_DE_MODELO`.

**Julgamento humano prévio vira ORACLE/GABARITO, não precondição.** Novo campo
`EntradaEtapaP13.gabarito_relacoes_afirmacao_evidencia` — quando fornecido, é copiado para
`ContextoExecucaoP13.relacoes_afirmacao_evidencia_gabarito` e citado na justificativa da etapa,
mas **nunca lido** por `_etapa_12_verificacao_de_evidencias` nem por nenhum outro handler desta
execução: nenhuma comparação automática contra o gabarito é feita nesta sessão. Confrontar o que
o modelo produziu com o que um humano já validou é trabalho de quem avalia o piloto (fora do
orquestrador), não uma regra de código nova — inventar essa comparação sem uma fonte que descreva
o critério de "concordância aceitável" seria a mesma inferência proibida que motiva o resto deste
arquivo.

**`validation_state` restrito na ferramenta do modelo.** `VALIDADA` e `INVALIDADA_POSTERIORMENTE`
exigem `validator`/`validation_date` humanos [`escolio/relacao.py::__post_init__`] — o `tool_use`
schema (`_SCHEMA_RELACAO`) só oferece os quatro valores restantes
(`NAO_VERIFICADA`/`PAGINA_NAO_CONFIRMADA`/`PAGINA_CONFIRMADA`/`VALIDACAO_PENDENTE`) como enum, e o
prompt (`prompts/p13_relacao_afirmacao_evidencia.md`) reforça isso por extenso. Se o modelo
devolver `VALIDADA` mesmo assim (contornando o enum do `tool_use`, que a API não garante ser
impossível), a ausência de `validator`/`validation_date` faz `RelacaoAfirmacaoEvidencia.
__post_init__` levantar `ErroDeCoerencia`, capturado como `ErroDePonteModeloP13` — nunca aceito
silenciosamente como validação de fato ocorrida.

**`provenance` nunca vem do modelo.** Fixado em código como `"[INFERIDO]"` [convenção do
CLAUDE.md §9] — o modelo não declara a proveniência de si mesmo; isso evita um campo do tool_use
schema inteiro só para um valor sempre igual.

**`unit_id` não existe no schema P05 de `RelacaoAfirmacaoEvidencia`.** Diferente de
`MatrizCriticidade`/`MatrizSeletividade`/`P13Comment`, o dataclass de `escolio/relacao.py` não tem
campo de unidade — `_exige_unit_id_conhecido` (BL-022) não se aplica aqui, e nenhuma checagem de
correspondência unidade↔relação foi adicionada. Lacuna nova, sem fonte que a resolva: não há como
verificar hoje que uma `RelacaoAfirmacaoEvidencia` gerada realmente se origina da unidade que a
pediu, além de confiar no prompt.

**Não tocado nesta sessão**: BVAA (etapa 11) e perfil de voz (etapa 13) — instrução explícita do
professor para escopo estreito.

**Testes novos**: `tests/funcoes/test_ponte_modelo_p13.py::TestGerarRelacoesAfirmacaoEvidencia` (6
casos) e `tests/funcoes/test_execucao_p13.py::TestEtapaDozeVerificacaoDeEvidencias` (+3 casos:
geração via modelo, gabarito registrado sem bloquear, falha de cliente estruturada). Suíte
completa: 1144 passando (1135 + 9).

Lacunas, correções de premissa e decisões de implementação encontradas na leitura integral do
P02, dos cinco contratos funcionais P10-P14 e do inventário canônico da R03, e na implementação
de `escolio/funcoes/`. Nenhum item aqui foi resolvido por inferência silenciosa — mesma
disciplina de `escolio/LACUNAS.md`, `escolio/bvaa/LACUNAS.md` e `escolio/contrato/LACUNAS.md`.

## Sessão de 2026-08-13 (sexta peça) — terceiro piloto real, novo defeito na etapa 8: `matrizes` veio como string JSON duplamente serializada, não como array

Sessão 1 de `docs/spec/proximos-passos-x02-drive-citacao.md` — reexecução do piloto contra o
capítulo 5 (`data/capitulos/`, mesmo `document_id=MAT-DOC-7b3e4356`), agora com a correção
`isinstance(item, dict)` da quinta peça já aplicada. Estimativa prévia (`cliente.estimar_custo`,
120 unidades de corpo / 8 lotes de 15): US$ 1,2806 — abaixo do teto de US$ 2, execução autorizada
pelo professor via `AskUserQuestion` antes da chamada real.

**A correção da quinta peça funcionou para a classe de defeito que corrigia** — nenhum
`TypeError`/`AttributeError` cru. Mas a checagem `isinstance(item, dict)` **disparou de novo**,
por uma causa nova: `_matriz_criticidade_de_item` recebeu como item de `matrizes` o caractere
`'{'` — string de um único caractere, não objeto. Isso não é o mesmo defeito de antes (item de
array vindo como string curta) — é sintoma de a iteração estar percorrendo os **caracteres de uma
string longa**, não os itens de um array.

**Causa real** (`data/cache_cliente/*.json`, resposta cacheada ANTES da checagem de forma rodar):
o `tool_use.input` do lote 0 tem uma única chave, `matrizes`, mas o valor associado a essa chave
**não é um array — é uma string de 5.870 caracteres contendo JSON válido**, que por sua vez é
`{"matrizes": [item1, item2]}` — o modelo serializou o objeto inteiro esperado (`{"matrizes":
[...]}`) como texto e o aninhou como valor de dentro da própria chave `matrizes`, uma camada de
serialização a mais do que o `tool_use` schema pede. `entrada.get("matrizes", [])` (`ponte_modelo_
p13.py::gerar_matrizes_criticidade`) devolve essa string; iterar sobre ela em
`matrizes.extend(_matriz_criticidade_de_item(item) for item in entrada.get("matrizes", []))`
itera caractere a caractere — o primeiro caractere de um JSON bem-formado é sempre `{`, o que
explica exatamente o item observado. `json.loads` no valor da string confirma: dentro dela havia
só **2** problemas candidatos para as 15 unidades desse lote (ambos citações recuadas do mesmo
autor — Thevet — com risco no eixo AVALIATIVO, classe `CRITICIDADE_BAIXA`), não zero e não muitos
— o conteúdo do julgamento em si parecia coerente; só a forma do envelope estava errada.

**Terceira categoria de defeito, distinta das duas anteriores** (terceira peça: resposta truncada
por `max_tokens`; quinta peça: item individual de array vindo como string): aqui a chamada
completou (`stop_reason` normal, sem truncamento) e o array chegou a existir — só que embrulhado
uma camada extra dentro de uma string, sob a mesma chave que o schema já reservava para o array
em si. Nenhuma das causas estruturadas existentes (`FALHA_NA_CHAMADA_AO_MODELO`,
`RESPOSTA_DO_MODELO_MAL_FORMADA`) precisou de nova variante — `RESPOSTA_DO_MODELO_MAL_FORMADA`
capturou este caso corretamente, porque a checagem de forma de item já cobria "isto não é um
dict", mesmo sem prever a causa específica. **A arquitetura de captura não precisou de mudança
nesta sessão** — só o `ErroDePonteModeloP13` resultante tem mensagem enganosa (fala de "item de
'matrizes' que não é objeto: `'{'`", que descreve o sintoma — um caractere — sem apontar a causa
— dupla serialização).

**Não corrigido nesta sessão**, por instrução explícita ("não conserte o que quebrar — só desta
vez, documentar"). Hipóteses não verificadas, registradas para quem investigar depois: (1) o
`tool_use` schema atual (`_SCHEMA_CRITICIDADE`) declara `matrizes` como `array` de objetos — a
dupla serialização pode ser efeito do modelo "hedging" contra um schema que ele interpretou como
aceitando string também, ou artefato de como o SDK/`thinking: adaptive` formata `tool_use.input`
quando o conteúdo gerado internamente já passou por uma etapa de serialização própria; (2) não
foi testado se pedir explicitamente, no prompt de `p13_matriz_criticidade.md`, para nunca
serializar a resposta como string resolveria — mudança de prompt, não de código, então mais barata
de testar antes de qualquer mudança de parsing; (3) uma correção de parsing só no código
(`_matriz_criticidade_de_item` ou `entrada.get("matrizes")`: tentar `json.loads` quando o valor é
`str`) trataria o sintoma sem saber se o modelo repete o padrão de forma estável — decisão de
código sem confirmar recorrência seria o mesmo erro de "consertar sem calibrar" já evitado nas
sessões anteriores.

**Custo real desta chamada**: `sequence_id=MAT-DOC-7b3e4356`, `cache_creation_input_tokens=39952`,
`input_tokens=417`, `output_tokens=5830`, `custo_usd_total=US$ 0,2189`. Só o lote 0 rodou (crash
no processamento da resposta, antes do lote 1); etapas 9 em diante não foram alcançadas de novo.
**Custo total acumulado nos três pilotos reais do P13**: US$ 0,9589 — abaixo do teto de US$ 2
combinado com o professor, com margem para uma quarta tentativa depois de decidir (1) ou (2)
acima.

**Etapas 1-7 desta sessão**: `EXECUTADA` sem achado, mesmo `document_id=MAT-DOC-7b3e4356` e 120
unidades de corpo (89 parágrafos + 14 citações recuadas + 17 notas, sem figuras — `referencias=0`,
mesma leitura de LAC-ING-017 já registrada na terceira peça) — ingestão determinística, sem custo,
idêntica entre as três sessões que já rodaram contra este capítulo.

Script do piloto: `saida/piloto_p13_capitulo5_v2.py` (fora do código versionado, mesma convenção
de `saida/piloto_p11.py`), com gate por variável de ambiente (`PILOTO_P13_EXECUTAR_REAL`) para
separar a estimativa de custo (sempre executada) da chamada real (só depois de aprovação humana
explícita nesta sessão).

### Correção de prompt confirmada; novo achado na etapa 9; TETO DE US$ 2 EXCEDIDO (US$ 2,1199)

Mesma sessão, continuação imediata depois do achado acima. Hipótese (2) do achado anterior — "não
foi testado se pedir explicitamente, no prompt, para nunca serializar a resposta como string
resolveria" — foi testada antes de qualquer mudança de código, por ser a mais barata.

**Correção aplicada**: `prompts/p13_matriz_criticidade.md` ganhou uma seção final explícita:
`matrizes` é array de objetos direto; nunca serializar o array (ou o objeto que o contém) como
string JSON dentro de um campo; lista vazia (`[]`), nunca string, quando não há problema
candidato. Nenhuma mudança de código em `ponte_modelo_p13.py`/`execucao_p13.py`.

**Resultado, reexecutando a etapa 8 do zero (novo `system_estavel`, nova escrita de cache)**: os
8 lotes completaram sem nenhum erro de forma — **a correção de prompt resolveu o defeito da string
duplamente serializada**, sem precisar de mudança de parsing. 11 `MatrizCriticidade` aceitas
(4 notas de rodapé + 7 parágrafos), classes de `SEM_CRITICIDADE_MATERIAL` a `CRITICIDADE_ALTA`
(uma só). Evidência de que a correção resolveu a causa raiz, não só mascarou o sintoma: nenhum
`isinstance(item, dict)` disparou em nenhum dos 8 lotes.

**Etapa 9 (seletividade, Opus 5), primeira execução real desta etapa contra qualquer documento**:
parou com `CausaDeParada.FALHA_NA_CHAMADA_AO_MODELO` / `ErroRespostaTruncada` —
`stop_reason=max_tokens`, 8.000 tokens de saída gerados e a resposta ainda incompleta, para
**11 candidatos em um único lote** (`TAMANHO_LOTE_ETAPA_9=15` não particiona, porque 11 < 15).
Mesma categoria de defeito já registrada na terceira peça (2026-08-12) para a etapa 8 antes do
particionamento em lotes existir — agora confirmada também na etapa 9, que nunca tinha sido
exercitada contra dado real. Correção estrutural análoga à da etapa 8 (reduzir
`TAMANHO_LOTE_ETAPA_9` para menos de 11, ou aumentar `MAX_TOKENS_ETAPA_9`) **não aplicada nesta
sessão** — decisão de código sem calibração, mesmo erro já evitado antes.

**Correção aplicada, não verificada contra a API real ainda** (decisão do professor: reduzir o
lote, não subir `MAX_TOKENS_ETAPA_9` — mesmo raciocínio já registrado para a etapa 8, rejeitando
explicitamente aumentar `max_tokens` como solução que só adiaria o problema). `TAMANHO_LOTE_ETAPA_9`
de 15 para **5** [`PROPOSTA`, calibrado só por este único dado real — 11 truncou, 5 é escolha
conservadora, não fórmula]. Suíte completa passa com cliente mockado
(`tests/funcoes/test_ponte_modelo_p13.py` referencia a constante dinamicamente, não um valor
fixo). **Não reexecutado contra a API real nesta sessão** — o teto já estava excedido quando a
correção foi decidida; nova chamada real exige nova aprovação de custo antes de rodar.

**TETO DE CUSTO EXCEDIDO.** A chamada truncada da etapa 9 sozinha custou US$ 0,6274 (Opus 5,
`effort=high`, escrita de cache de 42.228 tokens + 8.000 tokens de saída — o teto — sem produzir
nenhuma `MatrizSeletividade` utilizável, porque resposta truncada nunca é aceita como resultado
parcial [P09 §21.43]). Somando os quatro pilotos reais do P13 até agora (`costs/ledger.jsonl`,
etapas com prefixo `P13_`): **US$ 2,1199**, US$ 0,12 acima do teto de US$ 2 combinado com o
professor no início desta linha de trabalho. Reportado ao professor ao vivo, na mesma sessão em
que ocorreu — não descoberto depois. Nenhuma chamada adicional foi feita após constatar o
estouro; decisão sobre corrigir a etapa 9 e/ou renegociar o teto fica com o professor.

## Sessão de 2026-08-13 (quinta peça) — segundo piloto real, novo crash na etapa 8, corrigido

Retomada do piloto contra o capítulo 5 (`data/capitulos/`) depois da correção de lotes de 15 da
sessão de 2026-08-12 ("quarta peça") nunca ter sido verificada contra a API real. Estimativa
prévia (`cliente.estimar_custo`, 7 lotes): US$ 1,1251 — abaixo do teto de US$ 2 combinado com o
professor, execução autorizada a prosseguir.

**Etapas 1-7: `EXECUTADA`, sem custo**, mesmo `document_id=MAT-DOC-7b3e4356` do piloto anterior.

**Etapa 8, lote 0 (15 unidades, chamada real): a correção de lotes funcionou** — `stop_reason`
normal, sem truncamento (o defeito de 2026-08-12, "quarta peça", está resolvido para este
tamanho de lote). **Mas apareceu um segundo defeito, de categoria diferente**: pelo menos um
item de `matrizes` na resposta do modelo veio como string, não como objeto —
`item["avaliacao_por_eixo"]` (uma indexação de string por string) levantou
`TypeError: string indices must be integers, not 'str'`, cru, dentro de
`_matriz_criticidade_de_item`. Esse `TypeError` não estava no `except (KeyError, ValueError,
ErroDeComentario)` da função — propagava sem virar `ErroDePonteModeloP13`, e mesmo se virasse,
`execucao_p13.py` não capturava essa classe de erro nas quatro etapas que chamam modelo (só
`ErroDeCliente`, do piloto anterior). Resultado: crash cru de novo, `estado.historico` sem
registrar a tentativa, `estado.concluidas` parado em 7 — mesma classe de falha que motivou
`FALHA_NA_CHAMADA_AO_MODELO`, causa raiz diferente (ali a chamada não completava; aqui completa e
responde fora do formato).

**Custo real desta chamada** (`costs/ledger.jsonl`): `sequence_id=MAT-DOC-7b3e4356`,
`cache_creation_input_tokens=39952`, `input_tokens=416`, `output_tokens=6529`,
`custo_usd_total=US$ 0,22593`. Lotes 1-6 nunca rodaram (o crash aconteceu processando a resposta
do lote 0); etapa 9 em diante nunca foi alcançada.

**Correção aplicada na mesma sessão** (instrução do professor mudou de "não conserte nada" para
"construa fluxo completo" — a correção deste crash específico é a peça escolhida por ter contexto
mais recente e preciso):

1. `escolio/funcoes/ponte_modelo_p13.py` — `_matriz_criticidade_de_item`,
   `_matriz_seletividade_de_item`, o loop de `gerar_achados_fidelidade` e o loop de
   `gerar_comentarios` agora checam `isinstance(item, dict)` explicitamente antes de indexar, com
   mensagem que nomeia o item recebido — e os quatro `except` correspondentes passam a capturar
   também `TypeError`/`AttributeError`, não só `KeyError`/`ValueError`/erro de domínio. Item
   fora de forma sempre vira `ErroDePonteModeloP13`, nunca exceção crua de tipo.
2. `escolio/funcoes/execucao_p13.py` — oitava causa em `CausaDeParada`:
   `RESPOSTA_DO_MODELO_MAL_FORMADA`, nova, ao lado de `FALHA_NA_CHAMADA_AO_MODELO`. As quatro
   etapas que chamam modelo (8, 9, 13, 16-18) agora capturam também
   `ponte.ErroDePonteModeloP13`, via `_justificativa_falha_ponte` (mesmo padrão de
   `_justificativa_falha_cliente`), e devolvem `PARADA` estruturada em vez de crashar.
3. Só a etapa 8 teve o defeito confirmado por dado real; etapas 9, 13 e 16-18 têm a mesma forma
   de parsing (indexação de `item[...]` sem checar tipo antes) e foram corrigidas por simetria,
   não por falha real observada nelas.

**Testes novos**: `tests/funcoes/test_ponte_modelo_p13.py::TestGerarMatrizesCriticidade::
test_item_de_matrizes_nao_objeto_levanta_erro_de_ponte_nao_typeerror_cru` e
`tests/funcoes/test_execucao_p13.py::TestFalhaNaChamadaAoModelo::
test_etapa_8_resposta_mal_formada_vira_causa_estruturada_nao_crash`. Suíte completa: 1116
passando (1114 + 2).

**Não recalibrado contra a API real nesta correção** — mesma ressalva já registrada para a
correção de lotes: a suíte usa cliente mockado; não houve nova chamada real para confirmar que a
etapa 8 completa os 7 lotes inteiros sem outro modo de falha ainda não observado (lotes 1-6 nunca
rodaram em nenhum dos dois pilotos reais até agora). Reexecução real fica para sessão futura, se
o orçamento (US$ 0,45 já gastos dos dois pilotos, dentro do teto de US$ 2 combinado) permitir.

## Sessão de 2026-08-13 (continuação) — redução de lote da etapa 9 NÃO resolveu a truncagem; novo teto combinado

Retomada depois do estouro de teto registrado acima (US$ 2,1199 de US$ 2). Professor combinou
novo teto de US$ 3,20 para esta sequência antes de qualquer chamada nova. Estimativa prévia
(`cliente.estimar_custo`, `TAMANHO_LOTE_ETAPA_9=5`, 11 candidatos → 3 lotes): pior caso
US$ 1,2348, somado ao já gasto (US$ 1,8503 real, sem contar hits de cache local) dava
US$ 3,0851 — dentro do novo teto por ~US$ 0,11. Etapa 8 reexecutada neste piloto veio inteira do
cache local em disco (`data/cache_cliente/`, mesmo hash de input do piloto anterior),
`custo_usd_total=0` nos 8 lotes — confirma a garantia de `cache_local.py`, "reexecutar o mesmo
input não custa nada".

**Etapa 9, lote 0 (5 candidatos, `TAMANHO_LOTE_ETAPA_9=5` já aplicado): truncou de novo.**
`CausaDeParada.FALHA_NA_CHAMADA_AO_MODELO` / `RESPOSTA_TRUNCADA`, `stop_reason=max_tokens`,
Opus 5, 8.000 tokens de saída, resposta ainda incompleta — **para 5 candidatos, não 11.** A
correção de 2026-08-13 (reduzir `TAMANHO_LOTE_ETAPA_9` de 15 para 5, decisão do professor
"reduzir o lote, não subir `MAX_TOKENS_ETAPA_9`") não eliminou o defeito; só adiou de "trunca com
11" para "trunca com 5". `MAX_TOKENS_ETAPA_9` continua no mesmo valor de antes da correção — não
foi tocado nesta linha de trabalho em nenhuma sessão.

**Custo real desta chamada** (`costs/ledger.jsonl`, `msg_011Ce1JDhwKdRkeJidgV3zY9`): cache lido
(42.228 tokens, sem nova escrita — mesmo documento do piloto anterior), `input_tokens=513`,
`output_tokens=8000`, `custo_usd_total=US$ 0,2237` — bem abaixo do pior caso estimado
(US$ 0,4116/lote) porque a leitura de cache é mais barata que a escrita, mas ainda sem produzir
nenhuma `MatrizSeletividade` utilizável, resposta truncada nunca aceita como resultado parcial
[P09 §21.43].

**Gasto acumulado real na sequência após esta chamada: US$ 2,0740** (US$ 1,8503 + US$ 0,2237) —
dentro do novo teto de US$ 3,20, com margem de ~US$ 1,13 ainda não usada.

**Causa raiz corrigida e verificada contra a API real, mesma sessão.** O diagnóstico anterior
("reduzir o lote") estava errado: o lote de 5 truncou nos mesmos 8000 tokens que o lote de 11 —
se fosse volume de raciocínio por candidato, menos candidatos deveriam ter gastado menos. Causa
real: no Opus 5, `thinking={"type": "adaptive"}` [`ClienteAnthropic.chamar`] está ligado por
padrão, e `max_tokens` é teto de thinking + resposta somados — havia um piso de raciocínio fixo
por chamada acima dos 8000 tokens antigos, independente do tamanho do lote.

**Correção**: `TAMANHO_LOTE_ETAPA_9` revertido de 5 para **15** (sem particionar os 11 candidatos
reais — 1 chamada em vez de 3) e `MAX_TOKENS_ETAPA_9` subido de 8.000 para **32.000**
[`escolio/funcoes/ponte_modelo_p13.py`]. `max_tokens` alto não é pago se não for usado — só evita
cortar a resposta no meio; o cliente já liga streaming automaticamente acima de 16.000
[`_LIMIAR_STREAMING_TOKENS`].

**Verificado contra a API real na mesma sessão**: etapa 9 completou em 1 única chamada (11
candidatos, lote de 15, sem particionar), `EXECUTADA`, 11 `MatrizSeletividade` aceitas — nenhuma
truncagem. `output_tokens=17181` (mais que os 8000 antigos, confirmando que o teto era baixo
demais) — `custo_usd_total=US$ 0,4558` (`costs/ledger.jsonl`,
`msg_011Ce1JwVCXc1KoLXxirHuuk`), abaixo do pior caso estimado (US$ 1,0116) porque o documento veio
do cache (`cache_read_input_tokens=42228`, sem nova escrita). Etapa 10 (seleção determinística)
também `EXECUTADA`: 11 candidatos ordenados por criticidade, sem quota [§34.3-34.4].

**Gasto acumulado real na sequência `MAT-DOC-7b3e4356` após esta correção: US$ 2,3061**
(US$ 1,8503 anteriores + US$ 0,4558 desta chamada), dentro do novo teto de US$ 3,20 combinado com
o professor, margem de ~US$ 0,89.

Suíte mockada revalidada após a mudança de constantes (`tests/funcoes/test_ponte_modelo_p13.py`,
28 testes, referencia as constantes dinamicamente — nenhuma alteração de teste necessária).

**Reexecução do piloto completo (mesmo `document_id=MAT-DOC-7b3e4356`) veio inteira do cache
local, custo US$ 0** — confirma de novo a garantia "reexecutar o mesmo input não custa nada"
[`cache_local.py`]. Teto acumulado permanece US$ 2,3061 de US$ 3,20.

**Avançado até a etapa 11 (verificação de fontes/BVAA) nesta sessão — parada estruturada e
esperada**, não falha: `PONTO_DE_EXTENSAO_DE_MODELO`, "sem evidência de identificação (T01-T03)
ou de acesso (T04/T05) fornecida, nenhuma fonte avança no BVAA". Nenhuma evidência bibliográfica
real existe para o capítulo 5 nesta sessão, e o sistema não infere isso [CLAUDE.md §11]. Etapa 12
(verificação de evidências) e etapa 13 (verificação de voz) têm o mesmo formato de bloqueio —
exigem `RelacaoAfirmacaoEvidencia` já avaliada e `perfil_de_voz` do autor avaliado,
respectivamente; nenhum dos dois foi fornecido nesta sessão. Etapa 14 (privacidade) é sempre
`EXECUTADA` (determinística, sem gate [CO-012]) e etapa 15 (problemas sistêmicos) só precisa da
lista opcional do professor (mesmo vazia). **Nenhuma dessas cinco etapas foi tentada além da 11**
nesta sessão — parar na primeira parada estruturada, não pular a sequência para chegar a 16-18,
é a mesma disciplina de "sem núcleo publicável não há redação" aplicada a gates intermediários.

## Sobre a fonte em si

- **Os cinco contratos foram lidos integralmente** — P10 (1421 linhas), P11 (2298), P12 (2232),
  P13 (2189), P14 (3018), mais `02_CATALOGO_FUNCIONAL_CONSOLIDADO_P02_R01.md`,
  `01_INVENTARIO_FUNCIONAL_P02_R01.csv`,
  `03_MATRIZ_DE_REQUISITOS_LIMITES_GATES_E_SAIDAS_P02_R01.csv` e
  `02_INVENTARIO_DE_COMPONENTES_E_PACOTES_A_PRODUZIR_R03.csv`. Nenhum foi amostrado.

- **Os cinco contratos existem em duplicata byte a byte** no acervo: uma cópia sob
  `FONTES_CANONICAS/PACOTE_FUNCAO_*/` e outra sob `FONTES_CANONICAS/FONTES_CANONICAS/`. Os
  módulos citam o caminho por pacote. A duplicação não foi resolvida e não é lacuna de spec.

- **Os quatro contratos não homologados continuam não auditados após correção.** P12 e P13
  declaram `TESTES_VERIFICADOS_INDEPENDENTEMENTE_NESTA_VERSAO_CORRIGIDA: 0` e
  `AUDITORIA_APOS_CORRECAO_EXECUTADA: NAO`; P14 declara
  `TESTES_VERIFICADOS_INDEPENDENTEMENTE_NESTA_VERSAO: 0`. Só o P11 está
  `HOMOLOGADO_E_CONGELADO` [P11 §45.3]. As declarações transcritas nos módulos herdam esse
  estado — nenhuma foi validada empiricamente contra documento real.

## A seleção da função

- **LAC-FUNC-001 — nenhuma fonte define como se escolhe a função.** Verificado nos seis
  documentos que poderiam defini-la. `GATE_DE_ATIVACAO_P10`, `_P11`, `_P12`, `_P13` e `_P14`
  ocorrem **exatamente uma vez cada** em seus contratos (P10 §29.3, P11 §28.1, P12 §31.1,
  P13 §32.1, P14 §41.1), sempre como item nu de lista de gates, sem predicado, sem avaliador,
  sem insumo e sem modo de falha. A única "condição de ativação" declarada é idêntica nos
  cinco, §1: `APOS_HOMOLOGACAO_DAS_DEPENDENCIAS` — estado de dependência, não propriedade do
  documento. O P02 cataloga as seis unidades sem critério de escolha e fecha com "Nenhuma
  equivalência material autoriza fusão de IDs" [P02 §3]. A R03 CAMADA B lista doze campos que
  cada função deve declarar, e "critério de seleção" **não está entre eles**. Nenhum contrato
  tem seção de escopo, aplicabilidade, roteamento ou delimitação. A frase mais próxima em todo
  o acervo é P12 §4.1 — "O P11 revisa dissertações e teses. O P12 revisa relatórios de iniciação
  científica." — divisão de trabalho sem procedimento, sem dono e sem modo de falha.
  **Consequência em código:** `escolio/funcoes/roteador.py` não tem `selecionar_funcao`. A
  ausência é o mecanismo, não um comentário — POL-007 proíbe "Inferir próxima fase, componente
  ou operação", e a disciplina do CLAUDE.md §8 é que abstenção seja ausência de caminho de
  código. A escolha chega declarada em `request.function_id` e em
  `InputItem.classification.functions`, e o roteador confere e recusa.

- **LAC-FUNC-009 — não existe vocabulário controlado de tipo de documento acadêmico.** Nem no
  P09, nem no P19, nem nos contratos. `InputItem` [P09 §6] não tem campo de tipo; o
  `material_type` do P19 §17 é taxonomia de governança de dados (`INSTRUCOES`, `POLITICAS`,
  `DOCUMENTOS_DO_USUARIO`, `FONTES_BIBLIOGRAFICAS`, …), na qual uma tese e um relatório de IC
  são ambos `DOCUMENTOS_DO_USUARIO`. Nenhuma fonte enumera "tese", "dissertação", "relatório de
  iniciação científica", "artigo", "capítulo de livro" ou "relatório de pós-doutorado" como
  valores controlados. A tabela "Tipos de documento → função" do CLAUDE.md §3 é construção
  nossa, sem origem no acervo. **Consequência:** o roteador não classifica documento. O único
  campo do envelope que carrega função é `InputItem.classification.functions`, que é declarado
  por autoridade competente, não derivado do conteúdo. O tratamento de `functions` vazio segue
  o precedente literal do P19 §17 para `material_type=null`: registrar a indeterminação, manter
  a classificação pendente, **não conceder elegibilidade**, não criar valor categorial
  concorrente. Ver `AdmissaoDeMaterial.INDETERMINADO`.

- **LAC-FUNC-015 — tipo sem função não tem vaga numerada para onde ir, e a R03 não está
  congelada nem homologada.** O CLAUDE.md §13.3 registra como questão aberta se capítulo de
  livro e relatório de pós-doutorado seriam "P15+". O inventário canônico da R03 desmente a
  premissa: P15 é `PROFILES`, P16 `CONTEXTOS_GEOGRAFICOS`, P17 `CONTEXTOS_TEMPORAIS`, P18
  `INTERSECOES` — nenhum é camada `FUNCAO`, e a camada `FUNCAO` termina em P14. Não há
  componente livre no inventário para uma sexta macrofunção.
  **Correção sobre o estado da R03** (leitura integral de `docs/spec/mapa-R03.md`,
  2026-08-07): a R03 **não está homologada nem congelada** — está `R03_RETIFICADA`,
  `AGUARDANDO_VERIFICACAO_FINAL_RESTRITA`, `NAO_HOMOLOGADA` [R03 arquivo 00, arquivo 04]. A
  versão anterior deste item afirmava o contrário; corrigido. Isso não abre a porta para
  ampliar o catálogo por conveniência — `LAC-P02-005` já exige "nova fonte e decisão autoral
  específica" para qualquer ampliação, independente do estado de homologação da R03 — mas
  significa que "reabrir a R03" não é uma barreira adicional inexistente: a R03 já está aberta,
  aguardando o próprio usuário decidir a verificação final.
  As quatro candidatas da R03 CAMADA B — revisão de artigo antes da submissão, incorporação de
  comentários de qualificação ou defesa, auditoria bibliográfica autônoma, revisão de projeto
  de pesquisa ou proposta de financiamento — também não têm componente atribuído
  [`docs/spec/mapa-R03.md §3`]. Somando os dois tipos de documento sem função (capítulo de
  livro, relatório de pós-doutorado, já citados) às quatro candidatas: **seis itens sem
  componente**, todos sob a mesma trava `LAC-P02-005`. Nenhum foi incorporado nesta sessão.
  Registrado em `docs/backlog.md`, BL-015; decisão de reabrir P02/R03 para atribuir componente
  a qualquer um dos seis é exclusiva do `USUARIO_PROPONENTE` [CLAUDE.md §1].

## Identificadores

- **LAC-FUNC-002 — a identidade `LLM-ACA-F0x` ↔ `P1x` não está escrita em fonte alguma.** O
  token `LLM-ACA-F0*` aparece exclusivamente em artefatos do P02 (`01_INVENTARIO_FUNCIONAL`,
  `02_CATALOGO_FUNCIONAL_CONSOLIDADO`, `03_MATRIZ_DE_REQUISITOS`, `04_MAPA_DE_PROVENIENCIA`,
  `05_REGISTRO_DE_DUPLICIDADES`); jamais nos contratos P10-P14, no inventário da R03 ou no P09.
  A correspondência é legível pela finalidade declarada de cada par e por nada mais.
  **Decisão desta sessão, `[PROPOSTA]`:** `function_id` recebe os identificadores do P02 e
  `component_id` os da R03, porque P09 §4.2.4 ("`function_id` deve pertencer ao `component_id`")
  só tem conteúdo entre namespaces distintos — se fossem o mesmo rótulo a regra seria
  tautológica. Alternativa descartada: `function_id == component_id`, que além da tautologia
  deixaria o X01 sem valor. A tabela vive em `escolio/funcoes/catalogo.py::COMPONENTE_POR_FUNCAO`,
  no padrão de `escolio/bvaa/correspondencia.py` — consulta documentada, não tradução em runtime.

- **LAC-FUNC-003 — o X01 não tem contrato próprio, não tem etapas e não tem componente
  numerado.** Não existe arquivo `X01_CONTRATO_FUNCIONAL_*` no acervo: o X01 é definido apenas
  pela entrada `LLM-ACA-X01` do P02 e pelo item 6 da lista de funções da R03 CAMADA B. O P02 dá
  finalidade, entradas, saídas, limites, gates e riscos; nunca fluxo. E o inventário canônico da
  R03 atribui componente numerado às cinco macrofunções (P10-P14, camada `FUNCAO`) mas não ao
  X01. **Consequência:** `escolio/funcoes/x01.py` tem `fluxo=()` e `component_id=None`, e
  `exige_funcao_pertence_ao_componente` levanta para o X01 em vez de aceitar um `component_id`
  qualquer. Inventar um P-número ou um fluxo por analogia com P10-P14 seria a inferência
  proibida. Quem implementa a função em código é `escolio/` (schema P05) e `escolio/bvaa/`
  (máquina P04) [CLAUDE.md §3]; `x01.py` é a declaração no catálogo, não uma segunda
  implementação.

- **LAC-FUNC-005 — nenhuma fonte enumera as operações autorizadas de cada função.** P09 §4.2.5
  exige que `function_id` seja compatível com `operation`, mas os contratos recebem
  `requested_operation` (P11 §24.4, P12 §28.4, P13 §31.3, P14 §51.3) e `requested_p10_operation`
  (P10 §27.2) como string livre, sem vocabulário. **Consequência:**
  `DeclaracaoDeFuncao.operacoes_autorizadas` está vazio nas seis, e `verificar_operacao` devolve
  `conclusiva=False` em vez de aprovar em silêncio — "Indeterminado em vez de chute"
  [CLAUDE.md §11]. `exige_operacao_compativel` só levanta quando a incompatibilidade é
  conclusiva, o que hoje não ocorre para nenhuma função. Regra distinta e já implementada
  alhures: P09 §4.2.8 incide sobre `request.scope.allowed_operations` e é validada em
  `escolio/contrato/requisicao.py`.

  **BL-025 — a lacuna permanece; o que fechou foi o caso extremo.** O teste de integração de
  2026-08-09 confirmou que, na prática, *nenhuma* string de `operation` é hoje rejeitada por
  incompatibilidade com F04/P13 — inclusive `HOMOLOGAR_TUDO`. Continua correto não popular
  `operacoes_autorizadas` por inferência: essa lacuna não fecha sem fonte. O que fechou foi
  diferente: `roteador.exige_operacao_nao_homologa` bloqueia, **fora** do mecanismo de
  `operacoes_autorizadas` e para qualquer função, qualquer `operation` que peça homologação —
  fundamentado não em contrato de função, mas no invariante do próprio CLAUDE.md §1/§2 ("o
  sistema nunca homologa") e em `NivelIntervencao.HOMOLOGACAO` [P06 §2]. Isso não substitui a
  enumeração ausente: uma `operation` inventada e inofensiva (`"LER_TUDO_DUAS_VEZES"`, por
  exemplo) continua inconclusiva, exatamente como antes.

  **Lacuna residual em `exige_operacao_nao_homologa`: normaliza caixa e espaço, não acento.**
  `valor = operation.strip().upper()` faz `"HOMOLOGAR_TUDO"` e `"  homologacao "` baterem, mas
  `"HOMOLOGAÇÃO"` não bate com `"HOMOLOGACAO"` nem com o prefixo `"HOMOLOGAR"` — `.upper()` não
  remove diacrítico. Hoje não é brecha real: o vocabulário canônico da spec é sem acento
  (`NivelIntervencao.HOMOLOGACAO.value == "INT-14"`, e os nomes de nível em P06 são todos
  ASCII), e nada no código produz `operation` a partir de texto livre. Vira brecha se `operation`
  passar a ser derivada de entrada não controlada (ex.: texto digitado por um solicitante, ou
  extraído de um documento) sem normalização prévia de acento — nesse caso, adicionar
  normalização (`unicodedata.normalize("NFKD", ...)` ou equivalente) deixa de ser polimento e
  passa a ser a mesma classe de correção que fechou BL-025, não extensão de escopo nova.

## Gates

- **LAC-FUNC-007 — nenhum dos 91 gates nomeados nos cinco contratos tem posição declarada.**
  Contagem por contrato: P10 12 (§29.2 oito + §29.3 quatro), P11 18 (§28.1 seis + §28.2 doze),
  P12 16 (§31.1 seis + §31.2 dez), P13 17 (§32.1 seis + §32.2 onze), P14 28 (§41.1 nove +
  §41.2 dezessete + §41.3 dois). Nenhum contrato liga um gate a um índice de etapa; as duas
  listas — gates e fluxo modular — são disjuntas e sem tabela de correspondência. A semelhança
  de nome entre `GATE_DE_MATRIZ` e a etapa 16 do P14, ou entre `GATE_DE_CARTOGRAFIA` e a etapa 6
  do P13, **não é afirmação da fonte** e não virou `etapa=n`. O único gate posicionado em todo o
  acervo é o piloto supervisionado real do P11, "como gate de ativação operacional" na Etapa 25
  [P11 §38, §1] — e ele não está entre os 91 nomeados. **Consequência:** `Gate.etapa` é `None`
  em todos. A afirmação do CLAUDE.md §4 de que o `GATE_DE_SELECAO` do P13 "fica dentro do E4"
  não é sustentada pela fonte: a posição simplesmente não é declarada.

- **LAC-FUNC-011 — `GATE_DE_SELECAO` (P13) não tem definição alguma.** Ocorre uma única vez no
  contrato, no bullet de §32.1. O que ele libera, quem o concede e onde cai entre as 29 etapas:
  não declarado. A operação de seleção está em §10 (dez condições de comentabilidade, oito
  resultados) e §12 (matriz de seletividade), que **nunca nomeiam o gate**. Há ainda tensão
  interna não reconciliada pela fonte: o gate é classificado como documental, mas `AGUARDAR_GATE`
  é um dos oito resultados possíveis *da própria seleção* [§10] — isto é, a seleção pode ficar
  bloqueada por um gate que ela deveria fechar.

- **LAC-FUNC-006 — os rótulos de classe de gate divergem entre contratos e não foram
  unificados.** P10 §29.1/§29.2/§29.3: "automaticamente verificáveis" / "com decisão humana
  expressa" / "com validação documental". P11 §28.1-2 e P12 §31.1-2: "de validação documental" /
  "de decisão humana expressa". P13 §32.1-2: "documentais" / "humanos expressos". P14
  §41.1/§41.2/§41.3: "documentais" / "humanos obrigatórios" / "humanos adicionais compatíveis".
  Nenhuma fonte declara equivalência entre "validação documental" e "documentais", ou entre
  "decisão humana expressa", "humanos expressos" e "humanos obrigatórios". **Decisão:**
  `ClasseDeGate` carrega os sete rótulos distintos e cada módulo usa o do seu contrato; nenhum é
  alias do outro. Mesma disciplina de `CON-P05-001` — "sem apagar distinções". Se o professor
  decidir que são sinônimos, fundir depois é mecânico; o inverso não é.

- **`P10 §29.1` declara uma classe de gate sem nenhum membro.** "Gates automaticamente
  verificáveis" lista itens conferíveis — presença de campos obrigatórios, correspondência de
  identificadores, integridade de versões, existência de referências, compatibilidade formal de
  dependências — e não nomeia gate algum. `ClasseDeGate.AUTOMATICAMENTE_VERIFICAVEL` existe no
  vocabulário e não é usada por nenhuma declaração. É assim que a fonte está.

- **LAC-FUNC-018 — nenhuma fonte liga papel a "autoridade competente pelo objeto".** O P08
  cita essa expressão quatro vezes como quem decide escalonamento humano
  [P08 §3.6 abstenção segura; §5.6 autoridade decisória; §11.4 autoridade sobre retenção;
  §13.6 responsabilidade em incidente] — sempre no nível do **objeto** (este documento, este
  incidente, esta retenção), não no nível de fase do protocolo. Buscado explicitamente contra
  duas fontes candidatas e não encontrado em nenhuma: nem o P08 nomeia o papel, nem a matriz de
  papéis e autoridades da R03 [`09_MATRIZ_DE_PAPEIS_E_AUTORIDADES_R03.csv`;
  `docs/spec/mapa-R03.md §2.1`] usa a expressão ou equivalente — a R03 define autoridade **por
  fase do protocolo-mestre** (quem aprova o catálogo, quem aprova os schemas), eixo diferente de
  "quem decide sobre este objeto específico". P08 §5.6 é explícito sobre o efeito da lacuna:
  "na ausência dessa definição, não se presume autoridade" — mesmo padrão do P19 §73 (curador
  não concede a si próprio) e do CLAUDE.md (homologação exclusiva do `USUARIO_PROPONENTE`).
  A leitura mais provável — `USUARIO_PROPONENTE`, dado que sua `autoridade_de_aprovacao=FINAL`
  e "nenhum outro papel pode substituir sua decisão" [R03 §4.1] — é inferência minha por
  analogia entre autoridade-de-fase e autoridade-de-objeto, não afirmação literal de nenhuma
  fonte, e não deve ser codificada como se fosse. **Consequência:** bloqueia diretamente a peça
  7 do roadmap (ingestão segura) nos passos 13 ("validar autoridade") e 15 ("bloquear operação
  não autorizada") do protocolo de 20 passos do P08 §12 — o código não tem como decidir hoje
  *quem* recebe o escalonamento quando `PI-07` (instrução ambígua) ou um caso PR-09 (dado
  sensível) exigir decisão humana; só pode decidir *que* deve escalonar. Registrado também em
  `docs/spec/mapa-P08.md §5` e `docs/spec/mapa-R03.md §2.1, §9`.

- **LAC-FUNC-013 — a R03 CAMADA B só menciona "gates humanos"; os contratos declaram também
  gates documentais.** A lista dos doze campos obrigatórios não prevê a classe documental, que
  todos os cinco contratos usam. `DeclaracaoDeFuncao.gates` cobre as duas, distinguidas por
  `Gate.classe`. A R03 não proíbe — apenas não menciona; a extensão não foi tratada como
  autorizada nem como violação.

## Fluxo e etapas

- **LAC-FUNC-004 — o P10 não tem fluxo de etapas numeradas.** É o único dos cinco sem análogo do
  "FLUXO MODULAR" (P11 §38, P12 §41, P13 §43, P14 §75). O que existe são quatro sequências
  ordenadas, em seções distintas e com objetos distintos: §2 (oito produtos exigidos antes da
  redação), §4.4 (quatro fases de agente — `VAQUITA_ESTABILIZA`, `BALEIA_DERIVA`, `KOMODO_AVALIA`,
  `USUARIO_DECIDE_E_HOMOLOGA`), §21 (dez itens da ordem de redação modular, válidos só após
  matriz e arquitetura aprovadas) e §31 (vinte e três estados internos). Fundi-las produziria um
  fluxo que o contrato não tem. **Consequência:** `p10.py` tem `fluxo=()` e as quatro listas em
  `ordens_declaradas`, cada uma com sua seção e seu objeto — mesmo tratamento que
  `escolio/bvaa/transicoes.py` dá a T18, cuja origem não cabia no índice comum.

- **LAC-FUNC-008 — a espinha de sete fases não cobre as etapas finais de nenhum contrato.**
  Decisão autoral, homologação documental, piloto real e ativação operacional são atos de
  governança posteriores ao pipeline, e a espinha termina em E7. Nessas etapas `Etapa.fase` é
  `None` — P11 23-25, P12 29-32, P13 26-29, P14 29-32 — em vez de forçar correspondência. O
  agrupamento em sete é `[PROPOSTA]` do CLAUDE.md §4; nomes e ordem das etapas são da fonte.
  Mapeamentos individualmente discutíveis, todos `[PROPOSTA]`: "avanço modular" (P11 20, P12 26)
  recebeu E6 por ser retorno ao laço de execução; "elaboração da carta" (P14 25) recebeu E6 por
  ser produção de artefato, embora esteja entre duas etapas de verificação. **Nenhum código
  itera fases** — percorrer a espinha seria fundir execução, e a espinha nomeia fases, não funde
  execução [CLAUDE.md §4].

- **LAC-FUNC-014 — o campo "decisões" da R03 CAMADA B não tem seção correspondente em contrato
  algum.** Nenhum dos cinco tem "§ DECISÕES". O campo foi preenchido com pontos de decisão que
  os contratos identificam como tais em outras seções (etapas de decisão humana, gates
  nominados, regras de encaminhamento), cada item com sua citação. Não é transcrição de uma
  lista existente; é agregação com fonte item a item.

## Status e abstenção

- **LAC-FUNC-010 — `OUT_OF_SCOPE` só está ligado a uma condição no P11.** P11 §34 mapeia
  explicitamente: "pedido fora do escopo → `OUT_OF_SCOPE`". Em P12 (§28.3, §37), P13 (§31.2) e
  P14 (§51.2) a categoria é membro de enum e **nenhuma condição mapeia para ela**. Em P10 a
  condição existe — §32.2 lista "pedido fora do escopo" e manda usar `ABSTAINED` — mas a lista
  de categorias de abstenção do próprio P10 (§28.2) tem só cinco membros e **não inclui
  `OUT_OF_SCOPE`**: defeito da fonte, não omissão de leitura. Pior para a decisão: o caso
  análogo mais próximo do acervo, P14 PS14-08 ("Demanda fora do escopo"), resolve em `SUCCESS`
  para avaliação de admissibilidade + `InterventionRecord.disposition=REFUSED` + decisão
  `NAO_APLICAVEL` — precedente contrário ao uso de `ABSTAINED/OUT_OF_SCOPE`. **Decisão:**
  `abstencao_por_fora_de_escopo` segue a linha transversal do P09 §23 ("Operação fora do escopo
  → `ABSTAINED/OUT_OF_SCOPE`"), por ser regra do contrato de runtime e não de um contrato de
  função, e porque o caso do roteador é material não declarado *na porta*, enquanto PS14-08 é
  demanda fora de escopo *dentro* de uma execução legítima. As duas leituras estão em
  `docs/spec/divergencias.md §4.4`; a divergência não foi reconciliada.

- **LAC-FUNC-012 — `PARTIAL_SUCCESS` não tem condição mapeada em P10, P11 nem P13.** Nos três
  aparece uma única vez, no enum de status (P10 §27.4, P11 §24.2, P13 §31.1). Só P12 (PS12-01) e
  P14 (PS14-11) definem cenário que o produza. Nada nesta peça produz status; a lacuna fica
  registrada para quem for montar respostas.

- **LAC-FUNC-016 — nenhum contrato declara teto numérico de intervenção.** A afirmação do
  CLAUDE.md §6 de que "P13 para em `SINALIZACAO`/`RECOMENDACAO`" é leitura, não citação: o P13
  proíbe que o comentário execute reescrita, fusão, corte, substituição ou reorganização [§4.4]
  e exige registrar `intervention_level` por comentário [§28], mas nunca nomeia um nível
  `INT-nn` como teto. `DeclaracaoDeFuncao` **não tem** campo de teto de intervenção — criá-lo
  exigiria preencher os seis por inferência. Os limites ficam em `limites`, em prosa citada.

## Decisões de implementação verificáveis apenas por proxy

- **A correspondência `function_id` request↔response nasce aqui, não em `contrato/`.**
  `escolio/contrato/resposta.py::exige_correspondencia_request_response` confere `request_id`,
  `project_id` e `component_id`, e omite `function_id`, que o P09 §8.1 exige. Consertar ali seria
  alterar código existente; `roteador.py::exige_correspondencia_de_funcao` cobre a linha sem
  tocar em nada. Consolidação registrada em `docs/backlog.md`, BL-011. Enquanto durar, há duas
  funções de correspondência e quem chama precisa das duas.

- **`InputItem.classification.functions` nunca é populado por ninguém.** O campo existe em
  `escolio/contrato/entrada.py:36` e `escolio/adaptadores/ingestao_para_input_item.py` declara
  explicitamente que preenchê-lo "é trabalho de P19/roteador de função". O roteador **lê** o
  campo; populá-lo é ato de `CURADOR_DE_DADOS` + `USUARIO_PROPONENTE` sob o P19, não deste
  pacote. Em consequência, hoje todo `InputItem` produzido pela ingestão resulta em
  `AdmissaoDeMaterial.INDETERMINADO`. Registrado em BL-014.

- **`LAC-FUNC-017` — P10 e P11 discordam sobre o estado de homologação do P10.** P10 §42 declara
  `P10_NAO_HOMOLOGADO` e `P10_NAO_AUDITADO_APOS_SEGUNDA_CORRECAO`; P11 §45.2 declara
  `P10_HOMOLOGADO_E_CONGELADO`. Nenhum dos dois foi adotado como verdade: as declarações não
  carregam campo de estado de homologação, e a divergência fica aqui. Aparentada com a
  contradição já registrada em `docs/spec/autoridade-e-lacunas.md §2`.

- **Os fixtures existentes usam `function_id="P12"`.** `tests/contrato/test_requisicao.py:18` e
  `tests/contrato/test_resposta.py:37` passam o código do componente onde agora vai um
  `LLM-ACA-F0x`. Não quebram — `requisicao.py` só verifica não-vazio — mas divergem do catálogo.
  Não foram alterados. Registrado em BL-012.

## Sessão de orquestração do P13 (2026-08-09) — BL-021/BL-022

`escolio/funcoes/execucao_p13.py` é o primeiro módulo desta pasta com `avancar()` — não revoga a
nota abaixo ("Execução de qualquer etapa"), a implementa: `avancar()` só executa a etapa que
`DeclaracaoDeFuncao.proxima_etapa(concluidas)` nomeia, nunca mais de uma por chamada, e uma
tentativa que não executa não avança `concluidas` (`EstadoDeExecucaoP13.concluidas` só conta
`EXECUTADA`, quebrando na primeira que não for). Forma decidida pelo professor, não inferida
[docs/backlog.md, BL-021].

- **LAC-FUNC-019 — etapas 11-15 nunca aceitam entrada nesta sessão.** Diferente das etapas 8/9
  (`MatrizCriticidade`/`MatrizSeletividade` têm schema de sessão 2, aceito via `EntradaEtapaP13`),
  nenhuma sessão anterior definiu um objeto que ligue "candidato selecionado" a "verificação de
  fonte/evidência/voz/privacidade" ou a "problema sistêmico identificado". Sem esse objeto, o
  orquestrador não tem o que aceitar — `CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO` marca isso como
  permanente nesta sessão, não como "dado ainda não enviado" (`ENTRADA_NAO_FORNECIDA`, reservado a
  etapas com schema de aceitação já definido). Consequência: nenhum percurso real avança além da
  etapa 10 sem uma sessão futura que desenhe esse objeto — não inventado aqui por analogia com
  `aplicacao_p04_p05.py`/`aplicacao_p06_p07.py`, que validam um `P13Comment` já existente, não um
  candidato pré-redação.
- **LAC-FUNC-020 — etapas 19-24 do fluxo (§43) não correspondem a nenhum item do checklist de §44.**
  `escolio/comentarios/auditoria.py` implementa os 25 itens de §44 num único `auditar_lote`, mas
  nenhuma seção do contrato liga "verificação de densidade"/"repetição"/"acionabilidade"/"tom"/
  "gates"/"consolidação" (nomes de §43) aos itens de §44 um a um — mesma disciplina de
  LAC-FUNC-007 (gate sem posição declarada): semelhança de nome não é correspondência da fonte.
  Só a etapa 25, "auditoria final", tem o mesmo nome do título de §44 nas duas fontes — por isso
  só ela chama `auditar_lote` em `execucao_p13.py`; as seis anteriores ficam
  `CausaDeParada.SEM_FONTE_DE_VERIFICACAO`.
- **BL-022 resolvido aqui, não nos módulos de origem.** `document_id` canônico =
  `material_id_de_documento(documento)` [P19 §10, `[PROPOSTA]`]; `unit_id` conhecido = o conjunto
  reunido na etapa 7 a partir de `DocumentoIngerido`. Os dois são conferidos nas etapas 8, 9 e
  16-18; divergência levanta `ErroDeExecucaoP13`, nunca passa silenciosa. Ver docs/backlog.md,
  BL-022, para a justificativa completa da escolha entre `material_id` e `input_id`.

## Sessão de ligação ao cliente da API (2026-08-09) — etapas 8, 9, 16-18

`escolio/funcoes/ponte_modelo_p13.py` liga as etapas 8, 9, 16, 17 e 18 a `escolio/cliente/`.
Não altera o comportamento sem `cliente`: as cinco etapas continuam `PONTO_DE_EXTENSAO_DE_MODELO`
quando `EntradaEtapaP13.cliente` não é fornecido, exatamente como antes desta sessão — os testes
de `TestEtapaQueNaoPodeExecutar` (anteriores a esta sessão) não foram alterados e continuam
passando. Etapas 11-15 (LAC-FUNC-019) e 19-24 (LAC-FUNC-020) não são tocadas — instrução
explícita da sessão.

- **Modelo/effort por etapa dentro do intervalo declarado no CLAUDE.md §10 é escolha desta
  sessão, não valor novo de spec.** A tabela já marca E4b (etapa 8) como Sonnet `low`-`medium` e
  E4c (etapa 9) como Opus `high`-`xhigh` — ambos intervalos, não pontos. `ponte_modelo_p13.py`
  fixa `medium` para a etapa 8 e `high` para a etapa 9 (o extremo mais barato de cada intervalo).
  Se o professor preferir o outro extremo, é constante isolada em `MODEL_ETAPA_8`/`EFFORT_ETAPA_8`
  etc., não espalhada pelo código.
- **`max_tokens` por etapa (8.000 nas três chamadas) não vem de nenhuma fonte.**
  `docs/custos.md` registra que "output por chamada não medido" e estima ~150 tok/unidade para
  diagnóstico interno do E4 — a etapa 8/9/16-18 aqui não é o mesmo fan-out de 20 unidades/chamada
  daquele cálculo (cada chamada desta ponte cobre o lote de `unit_ids`/candidatos que o chamador
  passar, não fixado em 20), então o número de `docs/custos.md` não se aplica diretamente. 8.000
  é `[PROPOSTA]` desta sessão, generoso e não medido; revisar após a primeira execução real.
- **Como o modelo produz o "problema candidato" da etapa 8 não tem fonte própria.** Nenhum
  contrato descreve o objeto "problema candidato" antes de ele existir dentro da matriz de
  criticidade — §11 avalia um problema já identificado, não diz como identificá-lo. Esta sessão
  decidiu que a própria chamada da etapa 8 faz as duas coisas (identificar candidato + avaliar
  os 12 eixos), instruído em `prompts/p13_matriz_criticidade.md`; uma unidade sem problema
  material é omitida da resposta, nunca forçada. `[PROPOSTA]`, não extração de contrato.
- **Roteamento de candidato selecionado (etapa 10) para comentário-matriz / individual / remissão
  (etapas 16-18) não é decidido pelo orquestrador.** Nenhuma fonte liga `SelectionDecision` a "vira
  comentário-matriz" vs. "vira comentário individual" mecanicamente — `REMETER_A_COMENTARIO_MATRIZ`
  é o único valor do enum que nomeia o destino, e mesmo esse não diz qual comentário-matriz.
  `EntradaEtapaP13` ganhou três campos (`candidatos_para_comentario_matriz`,
  `candidatos_para_comentarios_individuais`, `candidatos_para_remissoes`) para que quem chama
  decida a classificação — mesma disciplina de já exigir os objetos `comentarios_*` prontos
  quando não se usa o modelo. O vínculo remissão→comentário-matriz
  (`matrix_comment_id_por_remissao`, chave `selection_id`) também é decidido por quem chama, nunca
  inferido do texto do modelo — `ponte_modelo_p13.gerar_comentarios` descarta o
  `matrix_comment_id` que o modelo eventualmente devolver e usa o do chamador.
- **Catálogo completo dos 15 `comment_type` [§13] não existe em código** (mesma lacuna já
  registrada em `escolio/comentarios/LACUNAS.md` — comment_type permanece `str`). O prompt de
  elaboração instrui o modelo a inventar um `comment_type` descritivo para comentário individual;
  só `COMENTARIO_MATRIZ`/`REMISSAO_A_COMENTARIO_MATRIZ` são checados contra um valor fixo, porque
  são os dois únicos citados por extenso em §31.5.4.
- **`status=DRAFT` é decisão de engenharia da ponte, não da fonte.** Todo `P13Comment` produzido
  pelo modelo nasce `DRAFT` — é o primeiro estado do ciclo em §31.5.1 e nenhum comentário recém-
  redigido já teria passado por revisão humana; não é extração de regra, é a leitura mais óbvia do
  próprio nome do enum.

### Sessão de 2026-08-12 — etapa 9 leva `comentarios_word` em conta [LAC-ING-020]

Pergunta que motivou: quando o autor já deixou um comentário do Word dizendo que um trecho está
inacabado, o sistema deve deixar de comentar ali, comentar mesmo assim, ou responder ao que ele
escreveu? Resolvida sem decisão nova de critério — §12 ("ganho de orientação > custo de poluição
documental") e §25 (silêncio diante de risco material é proibido) já cobrem os dois lados:
repetir o que já é conhecido não tem ganho de orientação; achado diferente no mesmo trecho segue
exigindo comentário mesmo que a unidade já tenha comentário de outra natureza. "Responder ao
comentário" fica fora — `P13Comment` não tem campo de thread, capacidade nova não desenhada
aqui.

- **Escopo restrito à etapa 9, não a "etapas de diagnóstico" (11-15) como a formulação inicial
  cogitava.** Motivo: 11-15 não têm handler ligado ao modelo (LAC-FUNC-019, permanecem
  `PONTO_DE_EXTENSAO_DE_MODELO`) — construir cinco pontos de extensão novos só para esta
  pergunta seria desproporcional. A etapa 9 já está ligada (`gerar_matrizes_seletividade`) e já
  tem vocabulário pronto no próprio §12/§10: fator `novelty` ("é um achado novo, ou repete algo
  já sinalizado?") e `SelectionDecision.NAO_COMENTAR_POR_REPETICAO`. Nenhum enum ou campo novo
  foi criado — reaproveita o que a matriz de seletividade já declarava antes desta sessão.
- **Julgar "mesmo achado ou achado diferente" é do prompt (`prompts/p13_matriz_seletividade.md`),
  nunca de código.** Nenhuma função em `ponte_modelo_p13.py` compara texto de comentário com
  achado por match de âncora/posição — só serializa `comentarios_word` (autor, texto,
  `unit_id_ancora`) no `system` e deixa a decisão inteiramente ao modelo, com instrução explícita
  de que o texto do comentário é dado, nunca comando [CLAUDE.md §8], mesmo quando parece um
  comando ("não comentar isto").
- **Escopo deliberadamente não estendido a etapas 8 e 16-18** — `_renderizar_comentarios_word`
  só é chamada por `gerar_matrizes_seletividade`; alterar o prefixo `system` cacheado das outras
  chamadas sem necessidade tem custo (invalidação de cache) sem pedido que o justifique. Testes
  de escopo (`TestEscopoComentariosWordRestritoAEtapa9`,
  `tests/funcoes/test_ponte_modelo_p13.py`) travam essa fronteira — falham se alguém estender por
  engano.
- **Comentário sem âncora resolvida (`unit_id_ancora=None`) entra igual no contexto do modelo,
  com âncora `null`.** Omiti-lo seria descartar dado real por conveniência de código; o modelo
  decide o peso de um comentário sem unidade correspondente, não este módulo.
- **Achado ao revisar: `NAO_COMENTAR_POR_REPETICAO` por comentário do autor era indistinguível
  de repetição interna ao documento, e a primeira versão do prompt não evitava isso.**
  `selection_decision` é um enum único — o mesmo valor serve para "o autor já sabe" e para "o
  mesmo problema ocorre em outro ponto do documento", sem diferença estrutural entre os dois. E
  `selection_rationale` é texto livre sem validação de conteúdo (`__post_init__` só exige
  não-vazio) — nada garantia que o texto dissesse qual dos dois motivos valeu, e sem essa
  informação não se distingue depois se o sistema calou por redundância própria ou porque o
  autor já sabia. Resolvido **sem campo novo**: o próprio §12 já separa "novidade" e
  "recorrência" como dois fatores distintos — `novelty` passou a ser reservado
  especificamente para "já conhecido, e a fonte é um comentário do autor" (citando autor e
  texto do comentário), e `recurrence` estritamente para "ocorre em outro ponto do documento",
  nunca os dois juntos no mesmo campo. `matrix_comment_coverage` continua para "o sistema já
  cobriu isso num comentário-matriz seu" — a terceira pergunta, também distinta. As três podem
  ter respostas independentes para o mesmo achado; `prompts/p13_matriz_seletividade.md` agora
  proíbe explicitamente colapsá-las. Nenhuma validação de código foi acrescentada
  (`seletividade.py` não mudou) — a garantia continua sendo de prompt, não de `__post_init__`,
  mesma disciplina de "julgamento no prompt, não em regra de código" já registrada acima; quem
  quiser blindagem estrutural extra (ex.: recusar `NAO_COMENTAR_POR_REPETICAO` com `novelty`
  genérico) precisaria decidir isso como regra nova, não inferida aqui.
- **Fragilidade identificada pelo professor: a garantia é só de prompt, e nenhum teste pega uma
  edição descuidada de `prompts/p13_matriz_seletividade.md`** — testar a prosa exigiria chamada
  real ao modelo, fora do escopo desta sessão. **Duas mitigações construídas em 2026-08-12, sem
  chamar a API:**
  1. `description` adicionada às três propriedades (`novelty`, `recurrence`,
     `matrix_comment_coverage`) em `_SCHEMA_SELETIVIDADE`
     (`escolio/funcoes/ponte_modelo_p13.py`) — é dict Python, não prosa em `.md`, então uma
     edição que a remova ou esvazie quebra teste sem precisar de chamada real:
     `tests/funcoes/test_ponte_modelo_p13.py::TestSchemaSeletividadeDistingueNoveltyDeRecurrence`
     (4 casos). Segundo benefício, não só testável: a `description` de cada propriedade também é
     enviada ao modelo dentro do bloco `tools` — reforço da instrução num lugar que a chamada real
     lê, não substituto do prompt em prosa.
  2. Aviso no topo da seção relevante do `.md`, explicando a origem da distinção (pergunta do
     professor, data, consequência de colapsar) — mitiga edição por desconhecimento, não dá
     garantia técnica nova.
  **O que continua não coberto, por ser genuinamente impossível sem chamar a API**: nada aqui
  verifica que o *modelo* de fato preenche `novelty`/`recurrence` como instruído numa execução
  real — as duas mitigações protegem a instrução de ser apagada por engano, não provam
  compliance do modelo.

## Sessão de 2026-08-12 (segunda peça) — etapas 12, 13, 14, 15 construídas; T01-T03 do BVAA

Autorizado por `INSTRUCOES_COMPLEMENTARES_IMPLEMENTACAO_ECOSSISTEMA_REVISAO_LLM_R01.md` (raiz do
repositório), que resolve três das lacunas normativas que impediam avançar (etapa 13, etapa
14/CO-012, T01-T03 do BVAA) sem tocar em nenhuma outra — o próprio documento se autolimita a
esses três pontos (§0, §7). As outras duas peças construídas nesta sessão (etapas 12 e 15) não
precisavam de autorização normativa nova — eram puro wiring de peças já existentes, identificado
numa auditoria anterior da mesma sessão.

- **Etapa 11 — T01-T03 encadeados com T04/T05.** `escolio/funcoes/bvaa_drive.py` ganhou
  `EvidenciaDeIdentificacaoDrive`/`avancar_por_identificacao` (escolha técnica delegada ao
  `ENGENHEIRO_LLM` — §3 da instrução). Detalhe completo, incluindo o trade-off de T01/T02
  licenciados pela mesma evidência (Drive não distingue obra de edição), em
  `escolio/bvaa/LACUNAS.md`.
- **Etapa 12 — verificação de evidências.** `RelacaoAfirmacaoEvidencia` (P05, `escolio/relacao.py`)
  já existia, validada e testada (91 testes), mas nunca tinha sido cotejada com esta etapa —
  achado da auditoria, não da instrução complementar. `_etapa_12_verificacao_de_evidencias`
  aceita a lista já construída (inclusive `[]` explícito, distinto de `None`); nenhuma chamada de
  modelo nova, nenhuma validação duplicada (o `__post_init__`/RC-001..020 do próprio dataclass já
  cobre forma e coerência).
- **Etapa 13 — detecção de fidelidade de voz.** Duas peças novas: `escolio/voz/deteccao.py`
  (Camada A — `AchadoDeFidelidade`: tipo, observado, evidência, confiança, notas; tipo restrito
  aos oito `DesvioBloqueante` já existentes, nunca categoria nova) e
  `escolio.voz.fidelidade.avaliar_a_partir_do_perfil` (ponte para a Camada B, que **não foi
  alterada** — `avaliar()` continua exatamente como antes, por instrução explícita da §1.1).
  `ponte_modelo_p13.gerar_achados_fidelidade` (novo, prompt `prompts/
  p13_deteccao_fidelidade_voz.md`) é o produtor via modelo (Sonnet, `medium` — mesma linha "E4
  diagnóstico" do CLAUDE.md §10, nenhum tier novo). Achado ao implementar a ponte: dos seis
  fatos que `avaliar()` exige, quatro são deriváveis do próprio `PerfilDeVoz` (a validação do
  perfil em `__post_init__` já garante `autorizacao_ausente`/`proveniencia_ausente` falsos
  quando exigidos; `amostra_unica`/`perfil_declarado_sem_amostras` são leitura direta de
  `evidence`/`profile_type`) — só `amostras_conflitantes` e `exigencia_institucional_em_conflito`
  continuam parâmetros explícitos, por não serem deriváveis de um perfil isolado.
- **Etapa 14 — privacidade, CO-012 resolvido.** Não é mais `PONTO_DE_EXTENSAO_DE_MODELO` — é
  **sempre `EXECUTADA`**, a primeira das cinco etapas de diagnóstico (11-15) a fechar
  permanentemente, porque a própria instrução complementar proíbe gate obrigatório (§2.2).
  `escolio/funcoes/salvaguarda_privacidade_p13.py` (novo módulo) cobre determinística e só os
  gatilhos literalmente pattern-detectáveis de §2.4 — CPF formatado, e-mail, telefone BR com DDD
  — reaproveitando `SensitivityLabel`/`SensitivityCategory.PERSONAL_DATA` já existentes em
  `escolio.contrato` [P09 §20], nenhum vocabulário novo. **Não cobertos, por decisão consciente,
  não por esquecimento**: endereço residencial, "identidade explicitamente protegida no material
  de origem", "informação marcada como confidencial" — exigiriam leitura semântica ou de
  metadados de proveniência que nenhum padrão determinístico cobre com segurança sem calibração
  contra caso real [CLAUDE.md §11]. Sensibilidade temática (violência, doença, religião, etc.)
  nunca aciona — testado explicitamente (`TestNuncaAcionaPorTema`,
  `tests/funcoes/test_salvaguarda_privacidade_p13.py`).
- **Etapa 15 — problemas sistêmicos conhecidos.** Wiring puro: o campo já estava citado em
  `escolio/funcoes/p13.py:139` (tupla `ENTRADAS_OPCIONAIS`) mas nunca virou campo de
  `EntradaEtapaP13`. Nenhuma descoberta autônoma de problema sistêmico foi construída — o
  professor identifica, o sistema registra, mesma disciplina de "nada inferido" aplicada a
  qualquer entrada opcional do §6.3.
- **`DocumentoIngerido.texto_da_unidade(unit_id)` (novo método, `escolio/ingestao/modelos.py`)
  substitui `ponte_modelo_p13._texto_unidade`, que era código morto** — definida havia sessões,
  nunca chamada por nenhum caminho de execução (confirmado por busca em todo o repositório antes
  de mover). Usado agora por `gerar_achados_fidelidade` e por
  `_etapa_14_verificacao_de_privacidade`; evita duplicar a mesma busca em quatro coleções em dois
  lugares novos.
- **Testes**: `tests/funcoes/test_salvaguarda_privacidade_p13.py` (13 casos),
  `tests/voz/test_deteccao.py` (5 casos), casos novos em `tests/voz/test_fidelidade.py`
  (`TestAvaliarAPartirDoPerfil`, 7 casos), `tests/funcoes/test_ponte_modelo_p13.py`
  (`TestGerarAchadosFidelidade`, 5 casos) e `tests/funcoes/test_execucao_p13.py`
  (`TestEtapaDozeVerificacaoDeEvidencias`, `TestEtapaTrezeVerificacaoDeVoz`,
  `TestEtapaCatorzeVerificacaoDePrivacidade`, `TestEtapaQuinzeProblemasSistemicos`, mais dois
  casos novos em `TestEtapaOnzeVerificacaoDeFontes`). Suíte completa: 1106 passando.
- **O que continua aberto, sem mudança nesta sessão**: etapas 19-24 (sem critério verificável no
  contrato — confirmado de novo, não é lacuna de leitura); o ato humano de classificar
  `InputItem.classification.functions` para um capítulo real [BL-014]; e a primeira execução real
  do P13 contra um `.docx` de `data/capitulos/` (o único piloto real até agora usou documento
  sintético — ver `escolio/bvaa/LACUNAS.md`).

## Sessão de 2026-08-12 (terceira peça) — primeira execução real contra capítulo real: quebra na etapa 8

Instrução do professor: executar o P13 de ponta a ponta contra o capítulo 5 (o menor de
`data/capitulos/`, 89 parágrafos/14 citações recuadas/17 notas/120 unidades), com
`classification.functions=["P13"]` declarado manualmente [BL-014, ato humano de teste — não
constitui declaração real para material de produção]. "Não conserte nada — o objetivo é ver o
que quebra."

**Etapas 1-7: `EXECUTADA` sem achado** — intake, autoridade, dependências, ingestão, versão,
cartografia, identificação das unidades, todas sem custo. `documento.referencias == []`,
confirmando LAC-ING-017 também para este capítulo (não só os 3 originais): o parser de `.docx`
nunca popula referências, então a etapa 11 (BVAA/Drive) não teria, mesmo em uma execução mais
longa, nenhum `ItemDeReferencia` para ancorar evidência — a peça de identificação/acesso
construída nesta mesma sessão é estruturalmente inaplicável a este tipo de documento, não por
falta de evidência real disponível, mas por ausência total de candidato.

**Etapa 8 (matriz de criticidade) — chamada real feita, resposta truncada, exceção não
capturada.** `gerar_matrizes_criticidade` chamado com as 103 unidades de corpo (parágrafos +
citações recuadas) em uma única chamada — `claude-sonnet-5`, `effort=medium`,
`max_tokens=MAX_TOKENS_ETAPA_8=8000`. A resposta consumiu os 8000 tokens de saída sem terminar a
ferramenta (`stop_reason=max_tokens`), e `ClienteAnthropic._exigir_resposta_completa` levantou
`ErroRespostaTruncada` — comportamento correto do cliente (mesmo defeito já corrigido para P11 em
2026-08-09, `escolio/cliente/LACUNAS.md`, "Sessão do piloto real P11 — ErroRespostaTruncada"; a
correção generaliza para P13 também, e generalizou de fato).

**Achado que a correção anterior não previa**: `ErroRespostaTruncada` **não é** uma das seis
`CausaDeParada` — é uma exceção Python não capturada por `_etapa_8_matriz_de_criticidade` nem por
`avancar()`. O percurso não produz um `ResultadoDeEtapa` com `tipo=PARADA`; ele **crasha** — o
chamador recebe uma exceção não estruturada, `estado.historico` não registra a tentativa, e
`estado.concluidas` permanece 7. Do ponto de vista de quem opera o orquestrador, isso é
qualitativamente diferente de `PONTO_DE_EXTENSAO_DE_MODELO`/`ENTRADA_NAO_FORNECIDA`: não há causa
estruturada para inspecionar, só uma exceção de outra camada (`escolio.cliente.erros`) que
`execucao_p13.py` deixa propagar sem tradução. Não corrigido nesta sessão, por instrução
expressa ("não conserte nada").

**Causa real, medida a partir do cache local** (`data/cache_cliente/*.json` guarda a resposta
ANTES da checagem de truncamento rodar — `ClienteAnthropic.chamar` salva no cache, depois checa
`stop_reason`): a resposta cacheada tinha **um único bloco, `type=thinking`, e nenhum `tool_use`
— zero matrizes produzidas, não matrizes incompletas**. Não é "12 eixos × 103 unidades produz
JSON maior que 8000 tokens"; é o raciocínio (`thinking: {"type": "adaptive"}`, ligado por padrão
em `ClienteAnthropic.chamar`) consumindo o orçamento inteiro de `max_tokens` antes de escrever
qualquer conteúdo de saída — o mesmo padrão que `ErroRespostaTruncada` já documentava
("frequentemente porque o raciocínio... consumiu o orçamento... `tool_use.input` vindo `{}`"),
agora confirmado para P13 com um capítulo real, não hipotético.

**Custo real, registrado em `costs/ledger.jsonl`**: uma chamada,
`sequence_id=MAT-DOC-7b3e4356` (hash real do capítulo 5), `etapa=P13_ETAPA_8_MATRIZ_CRITICIDADE`,
`cache_creation_input_tokens=39952`, `input_tokens=2352`, `output_tokens=8000` (o teto — confirma
a truncagem), `custo_usd_total=US$ 0,2445`. Estimativa prévia via `cliente.estimar_custo` (pior
caso, sem cache): US$ 0,1646 — a diferença vem do custo real de escrita de cache (`1,25×` o preço
de input não cacheado), que a estimativa de pior caso já assumia como "sem cache" (mais barato
que a escrita real). Nenhuma chamada de etapa 9 em diante foi feita — o percurso parou aqui.

## Sessão de 2026-08-12 (quarta peça) — correção: causa estruturada + lotes, não teto maior

Duas correções, por instrução do professor após ver o achado acima — "corrija a arquitetura
primeiro" (a exceção crua), "depois disso, o dimensionamento" (o lote).

**1. `CausaDeParada.FALHA_NA_CHAMADA_AO_MODELO` — sétima causa.** Antes desta correção,
`ErroDeCliente` (base de `ErroRespostaTruncada`, `ErroDeLimiteDeTaxa`, `ErroDeTimeout`,
`ErroDeConexao`, `ErroDeServidor`, etc. — `escolio/cliente/erros.py`) propagava como exceção
Python crua a partir de `ponte.gerar_matrizes_criticidade`/`gerar_matrizes_seletividade`/
`gerar_achados_fidelidade`/`gerar_comentarios`, derrubando `avancar()` sem registrar a tentativa
em `estado.historico` — nenhuma das outras seis causas tinha esse comportamento. Agora as quatro
etapas que chamam modelo (8, 9, 13, 16-18) capturam `ErroDeCliente` e devolvem
`PARADA`/`FALHA_NA_CHAMADA_AO_MODELO`, com `_justificativa_falha_cliente` (helper único,
`execucao_p13.py`) relatando categoria/severidade/código do erro e se `retryable`. A etapa
reoferece a si mesma na próxima chamada, mesma disciplina de qualquer outra `PARADA`
[POL-012] — nada de especial-caso.

Escopo desta correção: só `ErroDeCliente` e suas subclasses (erro de transporte/API). Erros de
tradução do próprio `ponte_modelo_p13.py` (`ErroDePonteModeloP13` — resposta bem-formada mas que
não corresponde ao dataclass esperado) continuam propagando como exceção — são uma categoria
diferente (o modelo respondeu, mas o conteúdo não validou), não pedida nesta correção, e
conflar as duas teria colapsado dois defeitos de natureza diferente na mesma causa.

**2. Lotes, não teto maior — `TAMANHO_LOTE_ETAPA_8`/`TAMANHO_LOTE_ETAPA_9 = 15`
[`PROPOSTA`, calibrado só por este único dado real].** `gerar_matrizes_criticidade` e
`gerar_matrizes_seletividade` agora particionam `unit_ids`/candidatos em lotes de até 15,
chamando `cliente.chamar` uma vez por lote — `system_estavel` (documento inteiro) é idêntico
entre lotes da mesma chamada de etapa, então a escrita de cache ocorre uma vez, os lotes
seguintes leem do cache [`ClienteAnthropic`/`hash_prefixo_estavel`]: lotes menores não
multiplicam o custo de reler o documento, só reduzem quanto o modelo precisa raciocinar por
chamada. Aumentar `max_tokens` foi descartado deliberadamente — adiaria o mesmo problema para o
próximo documento maior, sem atacar a causa (volume de raciocínio por chamada). Falha de
qualquer lote propaga sem capturar (`gerar_matrizes_criticidade`/`_seletividade` não aceitam
resultado parcial como sucesso [P09 §21.43]) — quem chama (`execucao_p13.py`) decide o que fazer,
via a `CausaDeParada` nova acima.

**Não recalibrado contra a API real nesta correção** — os 15 por lote não foram testados contra
o capítulo 5 de novo (evitar novo gasto sem necessidade); a suíte de testes usa cliente mockado
com múltiplas respostas em sequência para verificar que o particionamento e a agregação
funcionam, não que 15 é o número certo. Se uma reexecução real mostrar que 15 ainda trunca (ou
que cabe folga para mais), é achado de sessão futura, não desta.

Testes: `tests/funcoes/test_ponte_modelo_p13.py` (`TestGerarMatrizesCriticidadeEmLotes`,
`TestGerarMatrizesSeletividadeEmLotes`, 4 casos) e `tests/funcoes/test_execucao_p13.py`
(`TestFalhaNaChamadaAoModelo`, 4 casos — um por etapa que chama modelo). Suíte completa: 1114
passando.

## Sessão de orquestração do P11 (2026-08-09) — primeira fatia real (etapas 1-6)

`escolio/funcoes/execucao_p11.py` + `escolio/funcoes/ponte_modelo_p11.py` — segundo módulo de
execução desta pasta, mesmo padrão do P13 (`avancar()` de no-máximo-uma-etapa, POL-012). Escopo
desta sessão: só as etapas 1-6 (E1 intake/autoridade/dependências, E2 ingestão, E3 cartografia
global, e a primeira etapa de E4 — diagnóstico de estabilidade). Não generaliza `execucao_p13.py`
— "um módulo por função, nunca um executor genérico" [CLAUDE.md §4] — só reaproveita a forma
estrutural (mesmas seis `CausaDeParada`).

- **Cartografia global (etapa 5) funde agregação estrutural e identificação de unidades.** P11
  não tem etapa nomeada equivalente a "identificação das unidades" do P13 (etapa 7 de lá) — a
  única etapa nomeada de E3 em P11 é a cartografia global (etapa 5). `[PROPOSTA]`: nenhuma fonte
  diz que os dois atos são o mesmo; fundir aqui é leitura de engenharia desta sessão, para que a
  etapa 6 tenha uma base de `unit_id` conhecidos contra a qual conferir `evidence_ids` (mesma
  disciplina de BL-022 em P13).
- **Etapa 2 exige `nivel_intervencao_autorizado`, diferente do padrão de `execucao_p13.py`.**
  "Nível de intervenção autorizado" é uma das 20 `ENTRADAS_MINIMAS` [P11 §6.1] e uma das 15
  `PRECONDICOES` [P11 §7] — ausente do padrão P13 porque F04/P13 não lista o item da mesma forma
  entre suas entradas mínimas. O campo é coletado nesta etapa porque a fonte o exige antes de
  outras verificações; nenhuma etapa desta sessão (teto alcançado: `DIAGNOSTICO`, INT-02) o
  consome para autorizar aplicação de texto.
- **Diagnóstico de estabilidade (etapa 6) usa `escolio.contrato.afirmacao.ClaimEvidence` [P09
  §12] como saída, não um objeto novo.** A pergunta desta etapa ("a obra está estável?") produz
  exatamente achados com afirmação, suficiência e confiança — vocabulário que o P09 já declara.
  Decisão desta sessão: nenhum achado usa `status=CONFLICTED` (o schema da ferramenta nem oferece
  esse valor) — esta etapa não concilia fontes divergentes, e permitir `CONFLICTED` exigiria
  também `source_references` preenchidas, que o schema não pede. Uma sessão futura que precise de
  `CONFLICTED` aqui terá de resolver isso.
- **Etapas 7-22 continuam sem handler real, por falta de objeto de sessão, mesma disciplina de
  LAC-FUNC-019/020.** Diagnóstico estrutural/argumentativo/historiográfico (7-9), mapa de
  afirmações-evidências (10), plano modular (11), decisão humana (12), revisão modular/local
  (13-14), controle de voz/BVAA/afirmação-evidência (15-17), consolidação (18) e avanço modular
  (20) são `PONTO_DE_EXTENSAO_DE_MODELO`; verificação proporcional/auditoria de bloco (19),
  verificação global de regressão (21) e auditoria final (22) são `SEM_FONTE_DE_VERIFICACAO` —
  diferente de P13, `escolio/comentarios/auditoria.py` não tem equivalente para os produtos de
  P11 (cartografia, diagnóstico, plano modular, unidades revistas), então a etapa 22 aqui não
  chama nenhum `auditar_lote` como a etapa 25 de P13 chama. Fechar cada uma exige prompt e schema
  próprios — trabalho de sessão futura, não desta.
- **`max_tokens=8_000` para a etapa 6 é `[PROPOSTA]` não medida**, mesmo raciocínio de
  `ponte_modelo_p13.py` — revisar após a primeira execução real contra a tese do professor.

## Piloto real P11 (2026-08-09) — dois achados do primeiro percurso completo 1-6

Primeira execução real da etapa 6 contra os 3 capítulos reais (via `parse_docx_multiplo`).
Depois de corrigir o truncamento por `max_tokens` (ver `escolio/cliente/LACUNAS.md`), a segunda
tentativa completou e devolveu 5 achados — 3 válidos (EST-01, EST-02, EST-05: projeto
intelectual coerente, corpus mobilizado de forma consistente, nenhum sinal de mudança não
marcada de hipótese/objetivo) e **2 falsos positivos**:

- **EST-03/EST-04 — o modelo concluiu que "capítulo 3" e "tópico 5" não estavam no material
  fornecido**, citando como evidência frases do autor como "será trabalhado com maior
  profundidade no capítulo 3" (capítulo 1) e "no capítulo seguinte" (capítulo 2). Essas
  referências apontam exatamente para `3- Terapêuticas.docx`, que **foi fornecido** — conferido
  manualmente contra o texto real. O erro não é da tese; é do pipeline: `_renderizar_documento_
  estavel` (`ponte_modelo_p11.py`) serializa os três capítulos combinados sem rotular "isto é o
  Capítulo N" — cada um aparece só com seu próprio título de corpo de texto, sem numeração de
  ordem exposta ao modelo. Sem esse rótulo, o modelo não tem como ligar uma autorreferência do
  autor ("capítulo 3") ao arquivo que de fato ocupa essa posição.
- **Correção pendente, não aplicada nesta sessão** (decisão do professor sobre gastar outra
  chamada real para verificar): `_renderizar_documento_estavel` precisaria receber a ordem dos
  capítulos (já disponível — é a ordem de `caminhos` em `parse_docx_multiplo`) e incluir um
  rótulo por capítulo (ex.: `"capitulo_ordinal": 3`) no JSON serializado, para que o modelo
  possa resolver autorreferências de numeração contra o material real, em vez de concluir
  ausência por falta de rótulo.
- **Lição geral, não só deste caso**: um achado de "material ausente" do diagnóstico de
  estabilidade não deve ser aceito como fato sem conferência contra o documento real quando a
  obra é uma combinação de arquivos — o ponto cego é estrutural (falta de rótulo de capítulo no
  prompt), não um limite do modelo em si.
- **Nota de fechamento**: a correção (`capitulo`/`num_capitulos` no JSON serializado, ver
  `escolio/funcoes/ponte_modelo_p11.py`) foi aplicada e verificada com uma segunda chamada real
  ainda nesta sessão — EST-03/EST-04 sumiram, e a nova etapa 6 confirmou explicitamente que "as
  remissões internas ao 'capítulo 3' correspondem a um capítulo efetivamente presente no
  material". Gasto total do exercício de etapa 6 nesta sessão (truncamento + 2 tentativas):
  US$ 1,16, registrado em `costs/ledger.jsonl`.

## P13 §26 exige BVAA integral; nenhum código do projeto o aplica (achado 2026-08-09)

Levantado por pergunta do professor sobre a relação histórica entre "Google Drive" e P13.
Detalhe completo em `escolio/bvaa/LACUNAS.md` (LAC-BVAA-007, LAC-BVAA-008) — resumo aqui pela
ótica do roteador/execução de função, que é onde a integração faltante precisaria entrar:

- A fonte canônica homologada de P13 (§26, "APLICAÇÃO DO P04") exige aplicar o BVAA
  **integralmente**: sem acesso verificável a uma fonte, o sistema não confirma leitura,
  passagem, página ou imagem, não libera sustentação específica e não inventa bibliografia.
- **Nenhum módulo em `escolio/funcoes/` importa `escolio.bvaa`** — nem `execucao_p13.py` (que
  já rodou um piloto real, `costs/ledger.jsonl`, `sequence_id=MAT-DOC-piloto2026080901`), nem
  `execucao_p11.py` (cuja etapa 16, "Controle BVAA", é hoje `PONTO_DE_EXTENSAO_DE_MODELO` — ver
  acima). O piloto real de P13 produziu comentários sobre uma citação fabricada de propósito
  para não ter referência correspondente (`(Grewe, 1979)`) sem que `escolio.bvaa` fosse
  consultado em nenhum momento — o sistema notou o problema por julgamento do modelo sobre o
  texto (etapa 8, matriz de criticidade), não por verificação estrutural de acesso.
- **A raiz histórica é o protótipo pré-P13 ("PC30" — mesmo domínio, "Auditor Orientador de
  Comentários Word"), que usava Google Drive como "repositório bibliográfico prioritário"
  concreto** (`corpus/historico/acervo-antigo/AUDITOR_ORIENTADOR_COMENTARIOS_WORD/`, dezenas de
  versões v0.1-v0.3/RC1-RC4 com "Drive-first"/"BVAA-Drive" no nome). Quando o protótipo virou
  contrato formal (P02-P09), o requisito concreto ("verificar no Drive") virou o requisito
  abstrato ("acesso verificável") — a palavra "Drive" não sobrevive no contrato P13 homologado.
  Isso é generalização esperada de protótipo→contrato, não perda de requisito.
- **Fechar isto exige, no mínimo**: (1) `execucao_p13.py`/`execucao_p11.py` chamando
  `escolio.bvaa.maquina` num ponto real do fluxo, não só como etapa nomeada; (2) um mecanismo
  real de "acesso verificável" a documento externo — que hoje não existe em lugar nenhum do
  projeto. O item (3) — qual repositório é fonte de verdade — **foi decidido pelo professor em
  2026-08-09**: Drive é repositório primário; busca ativa na internet por referências
  novas/melhores é permitida; toda referência achada na internet exige aviso + pedido de
  download + disponibilização humana antes de qualquer uso — nunca incorporação automática.
  Regra completa e raciocínio em `escolio/bvaa/LACUNAS.md`. (1) e (2) continuam por construir —
  nenhuma das duas peças de engenharia (integração BVAA no fluxo; conector real de acesso a
  Drive + busca na internet + gate de disponibilização) foi desenhada nesta sessão.
- **Em 2026-08-12: (1) recebeu mecanismo desenhado e depois construído — `docs/spec/
  bvaa-drive-integracao.md`.** Levantamento inicial confirmou que ligar `escolio.bvaa` ao
  fluxo real exigia editar `_HANDLERS` de `execucao_p13.py` mais
  `EntradaEtapaP13`/`ContextoExecucaoP13` — registrado e parado primeiro. Depois, mesma sessão,
  o professor autorizou e as duas alterações foram feitas, com `escolio/bvaa/` permanecendo puro
  (dependência de `escolio.drive` isolada em `escolio/funcoes/bvaa_drive.py`, novo módulo) e o
  acesso licenciando só T04/T05. Só a etapa 11 ("verificação de fontes") foi ligada; 12-15
  continuam `PONTO_DE_EXTENSAO_DE_MODELO`. Ver `escolio/bvaa/LACUNAS.md` LAC-BVAA-009.

### Descompasso de escopo: `PARADA` por documento inteiro vs. gate por claim (achado e corrigido por proposta em 2026-08-14)

Levantado em sessão de piloto real do capítulo 5, ao notar que a etapa 11, do jeito que estava
ligada desde 2026-08-12, impede qualquer capítulo sem bibliografia verificável de produzir
comentário algum — o que descarta a maior parte do acervo real do professor, já que a maioria
dos capítulos não tem toda referência verificável no Drive/internet.

**O que a fonte pede, verbatim.** P13 §26 ("APLICAÇÃO DO P04"): *"O P13 deve aplicar
integralmente o BVAA. Sem acesso verificável: não confirma leitura; não confirma passagem; não
confirma página; não confirma imagem; não libera sustentação específica; não inventa
bibliografia. **Pode produzir comentário sobre pendência bibliográfica sem inventar a
solução.**"* Todas as restrições são negativas **por confirmação/comentário específico** —
nenhuma delas nega a produção de comentário em geral, e a última frase autoriza expressamente
comentar a própria pendência. Reforça: linha 1334 do mesmo contrato — *"a decisão de não
comentar por ausência de problema material não é falha, abstenção ou bloqueio"* — e P13 §25
("DENSIDADE E QUANTIDADE") lista como resultado **ilegítimo** o *"silêncio diante de risco
material"*. `ClaimEvidence` (`escolio/contrato/afirmacao.py:16-27`) já é uma estrutura por
`claim_id`, sem campo de `document_id` — o vocabulário de evidência do próprio projeto já opera
no grão certo. Nenhuma ocorrência de `PARADA`/bloqueio de documento inteiro associada a `BVAA`
em todo o contrato P13.

**O que o código fazia.** `_etapa_11_verificacao_de_fontes` (`execucao_p13.py:741`) devolvia
`TipoDeResultadoEtapa.PARADA` (com `CausaDeParada.ESCALONAMENTO_BIBLIOGRAFICO_NECESSARIO` ou
`PONTO_DE_EXTENSAO_DE_MODELO`) sem distinção por `unit_id` — `PARADA` é o resultado genérico da
máquina de estados que impede `avancar()` de alcançar a etapa 12, para a sessão inteira, mesmo
quando a maioria das claims do capítulo não depende de bibliografia nenhuma.

**Correção, `[PROPOSTA]` do professor em 2026-08-14, verificada contra a fonte antes de
registrar aqui, e construída na mesma sessão**: etapa 11 deixa de devolver `PARADA` por falta
de evidência bibliográfica — passa a `EXECUTADA` sempre, registrando
`ContextoExecucaoP13.vinculo_candidato_referencia_especifica = "PENDENTE_NAO_VERIFICAVEL"`
quando não há evidência (nunca aproximado por proxy, ex. "parágrafo tem citação" — decisão
explícita do professor de não inferir esse vínculo). A restrição real do §26 ("não confirma
sustentação específica, não inventa bibliografia") passou a ser responsabilidade da etapa de
elaboração de comentários (`prompts/p13_elaboracao_comentarios.md`, seção acrescentada), não
mais um bloqueio na etapa 11. Verificado: 4 testes de `TestEtapaOnzeVerificacaoDeFontes`
atualizados de `PARADA` para `EXECUTADA`, suíte completa (1176 testes) passando.

## Sessão de 2026-08-14 — finalização do motor até a etapa 25, consolidado

Resumo único desta sessão inteira, para não espalhar em múltiplas entradas separadas (evitar o
mesmo inchaço documental que a sessão identificou como risco em si mesma):

1. **Etapa 11 reescopada** — ver acima.
2. **`GATE_DE_SELECAO` implementado** (`_gate_de_selecao`, `execucao_p13.py`) — critério obtido
   do arquiteto (7 condições cumulativas) e traduzido `[PROPOSTA]` para os campos reais de
   `MatrizSeletividade`: nenhuma decisão em `AGUARDAR_EVIDENCIA`/`AGUARDAR_GATE`/`BLOQUEADO`
   (`SelectionDecision`, já nomeados no schema — sem heurística de texto), nenhuma omissão
   silenciosa entre `MatrizCriticidade` e `MatrizSeletividade`, nenhum `selection_id`/`unit_id`
   duplicado. Nova causa `CausaDeParada.GATE_DE_SELECAO_BLOQUEADO`. **Verificado contra a API
   real no mesmo dia**: o gate bloqueou de fato a etapa 10 quando o modelo devolveu um candidato
   real com `selection_decision=AGUARDAR_EVIDENCIA` (capítulo 5, `document_id=MAT-DOC-7b3e4356`)
   — não é só teste sintético, pegou um caso real na primeira execução.
3. **Etapas 19-24 implementadas**, reusando os itens de checklist §44 já existentes em
   `escolio/comentarios/auditoria.py` (`_item_densidade_justificada`, `_item_acionabilidade`,
   `_item_tom`, `_item_gates`) em vez de reimplementar o mesmo julgamento duas vezes — só a
   etapa 20 (repetição) é checagem nova, por não ter item correspondente em §44, deliberadamente
   estreita (só duplicata exata de `problem` por `unit_id`, não paráfrase). `ctx.achados_
   qualidade`/`ctx.consolidacao` novos campos de contexto.
4. **Escrita real de comentário no `.docx`** (`escolio/funcoes/escrita_docx_p13.py`, novo
   módulo) — `python-docx.add_comment` nativo (biblioteca 1.2.0, já instalada). Escopo desta
   sessão: só `unit_id` de `Paragrafo` do corpo (prefixo `PAR-`); citação recuada e nota de
   rodapé não são endereçáveis por este mecanismo hoje, ficam em `nao_aplicados` sem falha
   silenciosa. Nunca sobrescreve o arquivo original. 4 testes novos, verificado manualmente que
   o comentário aparece no arquivo salvo e o original permanece com zero comentários.
5. **Piloto real do zero, capítulo 5** (`saida/piloto_p13_capitulo5_do_zero.py`, cache isolado
   em `data/cache_cliente_do_zero/`, nunca lê o cache de tentativas anteriores) — etapas 1-9
   reais: etapa 8 devolveu 13 `MatrizCriticidade` (de 120 unidades), etapa 9 devolveu 13
   `MatrizSeletividade`, uma delas `AGUARDAR_EVIDENCIA`. **`GATE_DE_SELECAO` bloqueou a etapa 10
   corretamente** — percurso automático de hoje pára aí, por desenho, não por defeito. Custo
   real desta rodada (últimas 9 linhas novas do ledger, timestamps 2026-08-14): etapa 8 (8
   lotes) = US$ 0,5636; etapa 9 (1 lote) = US$ 0,9634; **total US$ 1,5270**, dentro do teto de
   US$ 2 combinado para o bloco.
6. **Continuação, mesmo dia, depois de mais achados reais** (itens 7-11 abaixo) — o piloto
   avançou de fato até a etapa 12/13, não ficou parado no item 5.

7. **Correção do `GATE_DE_SELECAO` (mesmo dia da construção)**: o candidato real
   `SEL-PROB-UNI-CIT-7b3e4356-0055-0001` voltou `AGUARDAR_EVIDENCIA` — e o próprio modelo
   escreveu, no campo `human_decision_required`, *"não há decisão humana pendente de gate, mas a
   emissão depende de evidência documental externa ainda não reunida"* (citação de Ferreira 2015
   p.66, possível elisão não sinalizada). Ou seja: **não é uma decisão humana**, é trabalho da
   etapa 11 (BVAA/Drive/busca, já construída) — colocar `AGUARDAR_EVIDENCIA` na mesma categoria
   de `AGUARDAR_GATE`/`BLOQUEADO` bloqueava a etapa 10 antes de a etapa 11 sequer tentar. Corrigido:
   `_DECISOES_PENDENTES_DE_GATE` agora só contém `AGUARDAR_GATE`/`BLOQUEADO`; `AGUARDAR_EVIDENCIA`
   passa pelo gate e vai para a etapa 11 tentar resolver, sem bloquear os outros 12 candidatos.
8. **Gate humano construído** (`ResolucaoHumanaDeSelecao`, `EntradaEtapaP13.resolucoes_humanas_
   de_selecao`) — para os casos que são de fato `AGUARDAR_GATE`/`BLOQUEADO`, um caminho de código
   real para o professor resolver, com `justificativa`/`autoridade` obrigatórios
   (`GATE_HUMANO_EXPRESSO`, nunca silencioso). 3 testes novos.
9. **`MAX_TOKENS_ETAPA_12` corrigido de 8.000 para 32.000** — mesma causa raiz já documentada
   para a etapa 9 (`thinking=adaptive` disputa o mesmo orçamento de `max_tokens`), agora
   confirmada contra API real também na etapa 12 (`RESPOSTA_TRUNCADA`, 13 candidatos).
10. **Achado do professor, correção de arquitetura real — `PERFIL_NEUTRO_ACADEMICO_CONTROLADO`
    nunca estava ligado à etapa 13.** O professor perguntou, com razão, por que a etapa 13
    exigia derivar um `PerfilDeVoz` completo (múltiplas amostras, custo real) do autor avaliado
    do capítulo 5 (identificado nesta sessão como Rodrigo Perles Dantas, não o professor) —
    e o que aconteceria com o próximo aluno sem histórico nenhum. Resposta encontrada na própria
    fonte: P07 "Gates" nomeia três saídas legítimas para perfil insuficiente — abstenção, pedido
    de amostras, **ou perfil neutro** — e o vocabulário do projeto (`TipoDePerfil.
    PERFIL_NEUTRO_ACADEMICO_CONTROLADO`, `GateDePerfil.GATE_NEUTRO`) já existia desde a sessão de
    2026-08-13, mas nunca tinha sido ligado a nenhuma etapa. `_etapa_13_verificacao_de_voz`
    tratava ausência de perfil/amostra como bloqueio de pipeline inteiro — mesma classe de erro
    do item 7 (etapa 11) e do achado original de escopo (documento no topo desta seção): tratar
    "informação enriquecedora ausente" como "bloqueio obrigatório". Corrigido: nova função
    `ponte.perfil_neutro_academico_controlado` (determinística, sem custo, sem amostra) —
    `_etapa_13_verificacao_de_voz` usa esse fallback automaticamente quando não há
    `perfil_de_voz` nem `amostras_autorais_de_voz`, registrado sempre em `ctx.perfil_de_voz_
    candidato` e na justificativa da etapa, nunca silencioso. 2 testes novos.
11. **Perfil de voz do Rodrigo, derivado de verdade, como enriquecimento (não pré-requisito)**:
    usando os capítulos 1-4 (mesma tese, autoria confirmada nos metadados `.docx`) + capítulo 5
    (para cobrir nota de rodapé). Levou 4 tentativas reais até cobrir as 30 dimensões — a
    terceira falhou por bug meu (esqueci `notas_de_rodape`/`citacoes_recuadas` na extração de
    texto); a quarta exigiu ajustar `prompts/p13_derivacao_perfil_de_voz.md` para deixar claro
    que ausência **consistente e sustentada** por volume de amostra (nenhuma tese acadêmica
    exibe humor/coloquialismo/interpelação direta/narrativa ficcional) é evidência de um valor,
    não falta de evidência — decisão do professor, registrada no prompt. Perfil final salvo em
    `saida/perfil_voz_rodrigo.json`. Custo acumulado das 4 tentativas: US$ 0,28 (primeira, com os
    artigos do professor — descartada, autor errado) + US$ 0,47 + US$ 0,59 + US$ 0,59 = US$ 1,93.

**Custo real total desta sessão (piloto + tentativas de voz)**: US$ 1,5270 (item 5) + US$ 1,93
(item 11) + US$ 0,1523 (tentativa de etapa 12 que truncou, item 9) ≈ **US$ 3,61**. Acima do teto
informal de US$ 2 por bloco combinado no início da sessão — cada decisão de gastar mais foi
autorizada explicitamente pelo professor ao longo da sessão, não decidida por conta própria, mas
o teto original não foi respeitado como número único — registrado para não fingir que foi.

**Estado ao final desta sessão**: piloto real chegou EXECUTADA até a etapa 11; etapa 12 rodou de
verdade (sem truncar, após item 9) mas parou em `RESPOSTA_DO_MODELO_MAL_FORMADA` — o modelo
violou `RC-004` (P05: `page_or_folio` exige `edition_or_version` + `PAGINA_CONFIRMADA`) ao gerar
uma `RelacaoAfirmacaoEvidencia`. Mesma classe de defeito já resolvida antes na etapa 8
(`matrizes` como string) — provável correção de prompt, não de código; não corrigido nesta
sessão, decisão de parar aqui por hoje.

## Não incluído nesta peça (fora de escopo, não lacuna)

- **Execução de qualquer etapa.** Não há `executar` em nenhum dos nove módulos, e é deliberado:
  POL-012 proíbe "executar encadeamento automático" e permite "registrar exatamente uma próxima
  ação permitida ou nenhuma automática". `DeclaracaoDeFuncao.proxima_etapa` devolve o sucessor
  ordinal, um só, e devolvê-lo não o autoriza. **`escolio/funcoes/execucao_p13.py` (sessão
  seguinte) implementa isto — ver acima — sem contradizer a nota: continua não havendo
  encadeamento automático, só a próxima ação, sob pedido explícito.**

- **`Response.interventions`.** Ligar `InterventionRecord` ao envelope de resposta estava
  reservado em `docs/backlog.md` BL-006 para "quando o roteador de função existir". O roteador
  passa a existir, mas ligar altera `escolio/contrato/resposta.py`. Registrado em BL-013.

- **Estados internos por função.** P10 §31 (23 estados), P11 §32 (26), P13 §36 e equivalentes são
  máquinas próprias de cada função, distintas do status P09 e da máquina documental do P03. Só a
  do P10 foi transcrita, e como `OrdemDeclarada`, por ser a sequência mais completa que aquele
  contrato oferece. As demais ficam para a implementação de cada função.

- **Schemas de saída por função.** `P13Comment` [P13 §31.5], matriz de aderência [P12 §10],
  matriz de demandas [P14 §21] e matriz de transposição [P10 §14] são produtos das funções, não
  do roteador.

- **Objetos congelados.** `escolio/intervencao/LACUNAS.md` deixou o tratamento "para o roteador
  de função, quando existir estado de objeto a consultar". O roteador existe e continua não
  havendo campo de objeto congelado no P09 §13 nem estado de objeto a consultar: a lacuna
  permanece onde está, não migra para cá.

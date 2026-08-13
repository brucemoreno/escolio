# LACUNAS — perfil de voz autoral (P07), item 5 do roadmap

Lacunas herdadas do pacote fonte (arquivo 09) e lacunas encontradas durante a implementação de
`escolio/voz/`. Nenhum item aqui foi resolvido por inferência silenciosa — mesma disciplina de
`escolio/LACUNAS.md`, `escolio/bvaa/LACUNAS.md` e `escolio/intervencao/LACUNAS.md`.

## Sobre a fonte em si

- **Pacote lido integralmente**, na ordem numérica dos 11 arquivos de conteúdo (00 a 11) mais o
  manifesto — o `00_LEIA_PRIMEIRO.txt` deste pacote não declara uma ordem de leitura distinta da
  numeração, ao contrário do pacote BVAA. Nenhum arquivo foi pulado.
- **Status da fonte: `EXECUTADO_DOCUMENTALMENTE; NAO_AUDITADO; NAO_HOMOLOGADO`** [11, linha 3] —
  diferente de P06, que está homologado e congelado. Esta implementação trata P07 com a mesma
  fidelidade literal dada a pacotes homologados; a ausência de homologação é um fato sobre o
  pacote fonte, não uma licença para desviar do texto.

## Escopo — autor avaliado vs. quem comenta [P07-CONF-ABERTO]

- **O princípio "imitação de pessoa real é substituída por atributos abstratos" [01, Princípios]
  é enunciado em termos universais, sem restringir-se ao autor avaliado.** A instrução desta
  sessão — e `CLAUDE.md` §13 item 1 / `docs/spec/divergencias.md` §4.1 — resolve isso por
  decisão de escopo, não por leitura do texto: apenas o perfil de voz do autor avaliado (o texto
  sob revisão) é implementado. A leitura alternativa (P07 também rege a voz de quem comenta) é
  registrada como aberta em `docs/spec/divergencias.md` §4.1 e **não** foi tocada aqui, em
  nenhuma forma — nenhum código, enum ou campo deste módulo tem como sujeito a voz de quem
  corrige. Se o professor decidir pela Leitura A daquele documento, esta peça precisa ser
  revisada; nada aqui antecipa essa decisão.
- **`purpose` e `scope` de `PerfilDeVoz` não têm vocabulário controlado fechado sobre "quem é o
  sujeito da voz".** O schema (arquivo 02) declara `purpose: string` e `scope: object` livres —
  a distinção autor-avaliado/corretor não é um campo do schema, é inteiramente uma convenção de
  uso que este módulo não impõe estruturalmente. Documentado aqui, não resolvido em código: nada
  impede, no nível do dataclass, que alguém preencha `purpose` com a voz de um corretor — a
  restrição de escopo é de uso (esta sessão, este roadmap), não de schema.

## Vocabulário e tipagem

- **`Confidence` (P07) é vocabulário próprio, não reuso de `escolio.vocabulario.Confidence` (P05)
  nem de `escolio.contrato.vocabulario.Confidence` (P09).** Os três têm cardinalidade e rótulos
  distintos: P07 = `BAIXA|MEDIA|ALTA|NAO_APLICAVEL`; P05 = `NAO_AVALIADA|BAIXA|MEDIA|ALTA` (sem
  `NAO_APLICAVEL`, com `NAO_AVALIADA`); P09 = `HIGH|MEDIUM|LOW|UNDETERMINED` (inglês, sem
  `NAO_APLICAVEL` equivalente declarado). Mesma disciplina dada a `CON-P05-001` e a
  `escolio/contrato/LACUNAS.md` BL-002: nenhum dos três é alias do outro; nenhuma tabela de
  correspondência foi construída porque a instrução desta sessão não pediu uma (diferente de
  `escolio/bvaa/correspondencia.py`, que existe porque P04 explicitamente "é implementado sobre
  o schema P05 existente, com os aliases do CON-P05-001").
- **`scope`, `dimensions`, `authorization`, `versioning`, `reversibility`, `evidence`,
  `provenance` tipados como `dict`/`list` livres.** O schema JSON (arquivo 02) declara apenas
  `type: object` ou `type: array` para estes campos, sem sub-schema. Mesmo tratamento dado a
  `Response.structured_items` em `escolio/contrato/resposta.py` (P09 §8, ver
  `escolio/contrato/LACUNAS.md`): estrutura mínima aberta, nenhum campo interno inventado.
- **Definições das 30 dimensões (arquivo 03) são o rótulo genérico "Dimensão controlada:
  &lt;nome&gt;" repetido em todas as linhas do CSV.** A fonte não elabora semântica além do nome e
  da obrigatoriedade — `escolio/voz/dimensoes.py::DEFINICOES` preserva exatamente isso; nenhuma
  definição mais rica foi inventada para as 30 dimensões.
- **Correção de premissa: `CLAUDE.md` §9 diz "30 dimensões `VOZ-D01…D30`, 24 obrigatórias" — a
  contagem literal do CSV (arquivo 03) é 26 obrigatórias e 4 opcionais (`VOZ-D16..D19`:
  `preferencias_lexicais`, `termos_desaconselhados`, `abertura_encerramento`,
  `recursos_retoricos`), não 24/6.** `escolio/voz/dimensoes.py::DEFINICOES` segue a contagem
  literal do CSV, não o número do CLAUDE.md — fidelidade à fonte primária prevalece sobre a
  paráfrase do documento de projeto. Divergência não corrigida em `CLAUDE.md` por esta peça
  (fora do escopo desta sessão alterar CLAUDE.md); registrada aqui para não ficar silenciosa.

## Gates por tipo de perfil — verificáveis apenas por proxy

- **"Perfil declarado exige declaração material" [01, Gates] é verificado como `authorization`
  não vazio.** O schema não define um campo estrutural distinto de "declaração material" além de
  `authorization` (arquivo 04: autoridade do `PERFIL_AUTORAL_DECLARADO_PELO_USUARIO` é
  `USUARIO_PROPONENTE`). Implementado em `escolio/voz/perfil.py::PerfilDeVoz._exige_declaracao`.
- **"Perfil derivado exige múltiplas amostras e proveniência" [01, Gates] — quantidade mínima
  absoluta não definida [P07-LAC-001, arquivo 09, preservada].** `_MINIMO_DE_AMOSTRAS_PARA_PERFIL_DERIVADO
  = 2` em `escolio/voz/perfil.py` é o menor valor compatível com a palavra "múltiplas" (plural),
  não uma inferência de quantidade além do que o próprio texto já exige. Se o professor definir
  um mínimo maior, é decisão nova, não desta peça.
- **"Perfil híbrido exige resolução explícita de conflitos" [01, Gates]** não tem campo
  estrutural correspondente no schema (nenhum campo "conflitos_resolvidos" ou similar em
  `authorization`/`versioning`). Não implementado como validação de campo — `_exige_declaracao`
  e `_exige_amostras` cobrem apenas as duas primeiras cláusulas do gate híbrido (declaração +
  amostras); a resolução explícita de conflito permanece responsabilidade de quem constrói o
  perfil, sem verificação de código, mesmo tratamento dado a `before_reference` em
  `escolio/intervencao/LACUNAS.md`.
- **"Perfil insuficiente conduz à abstenção, pedido de amostras ou perfil neutro" [01, Gates]** —
  das três saídas, apenas a abstenção é uma propriedade verificável de uma única instância de
  `PerfilDeVoz` já tipada como `PERFIL_INSUFICIENTE_OU_CONFLITANTE` (`status` obrigatoriamente
  `ABSTENCAO`). "Pedido de amostras" e "perfil neutro" são ações que produzem um objeto
  diferente (uma nova solicitação, ou um `PerfilDeVoz` de outro `profile_type`) — não uma
  transição de estado do mesmo perfil, e por isso não modeladas como método deste dataclass.
- **`GateDePerfil` (enum com os 6 nomes de gate do arquivo 04) é documentado, mas não
  verificado por código como precondição de transição.** Diferente dos gates de
  `escolio/intervencao/gate.py` (que decidem um nível dentro de uma cadeia ordinal com
  regressão), o arquivo 04 não declara uma máquina de transição entre gates — apenas associa,
  por linha, perfil→gate. `GATE_POR_PERFIL` é tabela de consulta (igual em espírito a
  `escolio/bvaa/correspondencia.py`), não uma função de decisão com regressão.

## Avaliação de fidelidade — 06/07

- **`avaliar()` em `escolio/voz/fidelidade.py` recebe condições já apuradas (booleanos), não
  texto.** O arquivo 06 não define como detectar "invenção factual" ou "perda de densidade" a
  partir de um texto concreto — apenas a consequência quando a condição já foi constatada.
  Mesmo tratamento dado a `RegistroDeRelacoes.marcar_conflito` em `escolio/LACUNAS.md` (RC-012):
  nenhuma detecção automática por análise semântica de texto foi construída, porque isso exigiria
  inferência fora do escopo desta peça (schema/regra determinística, sem LLM).
- **Ordem de verificação em `avaliar()` (autorização → proveniência → amostra única → amostras
  conflitantes → desvio bloqueante → ressalva → correção → conforme)** segue a ordem em que o
  arquivo 07 lista os gatilhos de `ABSTENCAO` ("falta de autorização, proveniência, amostras,
  resolução de conflito ou gate") antes de qualquer resultado positivo, e o arquivo 06 lista
  `RESULTADOS` na ordem `CONFORME; CONFORME_COM_RESSALVAS; CORRIGIR_ANTES_DE_AVANCAR; BLOQUEAR;
  ABSTER_SE` sem declarar precedência entre eles quando mais de uma condição se aplica ao mesmo
  tempo. A precedência ABSTENCAO > BLOQUEAR > CORRIGIR > RESSALVAS > CONFORME é uma decisão de
  implementação (mais restritivo primeiro), não uma ordem literal do arquivo 06 — documentada
  aqui por transparência.
- **"Resolução de conflito" e "gate" como gatilhos de `ABSTENCAO` [07]** não têm parâmetro
  próprio em `avaliar()` além dos cinco já cobertos (`autorizacao_ausente`,
  `proveniencia_ausente`, `amostra_unica`, `amostras_conflitantes`). "Resolução de conflito" e
  "gate" não têm, na fonte, uma condição estrutural distinta das já modeladas — tratados como
  cobertos pelas mesmas quatro condições, sem parâmetro adicional inventado.
- **Reversão ao último perfil validado [07, REVERSAO]** — "preservando versão rejeitada, motivo,
  evidência e decisão" — não implementada nesta peça. Exige um histórico de versões de
  `PerfilDeVoz` (persistência ou lista de perfis anteriores), que não existe em
  `escolio/voz/perfil.py` (dataclass em memória, sem histórico) e não foi pedido pela instrução
  desta sessão. Ver seção "Não incluído" abaixo.

## Herdadas do arquivo 09 (REGISTRO_DE_LACUNAS_E_CONFLITOS)

- **P07-LAC-001 — quantidade mínima absoluta de amostras não definida.** Preservada — ver acima
  (`_MINIMO_DE_AMOSTRAS_PARA_PERFIL_DERIVADO`).
- **P07-LAC-002 — limiares quantitativos universais de ritmo e cadência (VOZ-D06, VOZ-D07) não
  definidos.** Preservada. `escolio/voz/dimensoes.py` registra as duas dimensões pelo nome; nenhum
  limiar numérico foi inventado para "ritmo" ou "cadência".
- **P07-LAC-003 / P07-LAC-004 — "P08 não produzido" / "P09 não produzido".** Já não se aplicam
  literalmente: `escolio/contrato/` implementa P09 (item 1 do roadmap, concluído antes desta
  peça). Não há, porém, nenhuma referência cruzada nova entre `escolio/voz/` e
  `escolio/contrato/` além da observação de vocabulário paralelo já registrada acima — a fonte
  P07 não define como um `PerfilDeVoz` se relaciona com o envelope P09 (`ClaimEvidence`,
  `InterventionRecord`), e nenhuma integração foi inferida.
- **P07-CONF-001 — exigência institucional pode conflitar com preferência autoral, tratamento
  `PRECEDENCIA_E_GATE_HUMANO`.** Implementado como o parâmetro
  `exigencia_institucional_em_conflito` de `avaliar()`, resultando em `CORRIGIR_ANTES_DE_AVANCAR`
  — o "gate humano" em si (quem decide, como) não tem campo estrutural na fonte além do próprio
  resultado não-`CONFORME`; nenhuma autoridade nomeada foi codificada porque o arquivo 06/07 não
  a declara para este conflito específico (diferente de P06, onde `AuthorizationStatus` já
  modela isso para `InterventionRecord`).

## Sessão de 2026-08-13 (nona peça) — derivação de `PerfilDeVoz` por amostras autorais

Decisão do professor (`USUARIO_PROPONENTE`): a etapa 13 deixa de exigir que o professor preencha
manualmente as 30 dimensões do schema P07 antes de rodar. `escolio/voz/amostra.py` (novo módulo)
define `AmostraAutoral` (texto + `provenance`, gate mínimo de forma) e
`SolicitacaoDeAmostrasAdicionais` (saída explícita quando as amostras não bastam).
`escolio/funcoes/ponte_modelo_p13.py::gerar_perfil_de_voz_candidato` (novo) chama o modelo
(Sonnet, `medium`) para avaliar as 30 dimensões contra as amostras recebidas e devolve ou um
`PerfilDeVoz` candidato (`PERFIL_AUTORAL_DERIVADO_DE_AMOSTRAS`, `status=VALIDACAO_PENDENTE`) ou
`SolicitacaoDeAmostrasAdicionais` — nunca preenche uma dimensão sem evidência apontada pelo
próprio modelo. Ver `escolio/funcoes/LACUNAS.md` (mesma sessão) para o lado do orquestrador
(nova causa `AMOSTRAS_DE_VOZ_INSUFICIENTES`, campo `ctx.perfil_de_voz_candidato`).

**Qual documento conta como "amostra autoral" não foi resolvido nesta sessão — deliberadamente.**
A instrução inicial pedia para eu identificar a fonte antes de codificar; verifiquei `corpus/` e
não encontrei nenhum arquivo que designe um corpus de amostras para nenhum autor. A hipótese mais
óbvia — os demais capítulos do mesmo livro em `data/capitulos/` (1-4, distintos do capítulo 5 sob
revisão) — foi apresentada ao professor duas vezes e não foi confirmada; a resposta final foi
"por que você está querendo usar o capítulo 1 ao 4 como amostra?", sem indicar outra fonte.
**Decisão**: `AmostraAutoral`/`gerar_perfil_de_voz_candidato` são inteiramente genéricos — aceitam
qualquer lista de amostras que quem chama já tenha decidido usar; nenhum arquivo específico
(capítulo, artigo, ou qualquer outro) é tratado como amostra por padrão em código. Isso não é
lacuna resolvida por proxy — é a mesma disciplina de LAC-FUNC-001 ("o roteador confere e recusa,
nunca elege"): a seleção de qual documento é amostra fica inteiramente com quem opera o piloto,
registrada como decisão humana no momento em que a etapa é chamada, não inferida deste módulo.

**Confiança agregada do perfil (`PerfilDeVoz.confidence`, campo único) é o mínimo entre as
confianças por dimensão que o modelo devolveu com evidência.** O schema P07 não define como
compor um único valor de `confidence` a partir de 26+ julgamentos por dimensão — decisão de
implementação `[PROPOSTA]`: o pior caso entre as dimensões cobertas, não a média nem a moda,
porque "confiança do perfil" avaliada de forma otimista contradiz o próprio princípio de
preservar revisão humana em caso ambíguo [P07, arquivo 06/07]. Se nenhuma dimensão graduada
(`BAIXA/MEDIA/ALTA`) estiver presente — não deveria ocorrer, já que todas as 26 obrigatórias
precisam de evidência para o candidato existir — cai em `NAO_APLICAVEL` por segurança, nunca por
inferência de que a ausência significa "não avaliado com confiança".

**`amostras_conflitantes` (parâmetro já existente de `avaliar_a_partir_do_perfil`, etapa 13)
continua não calculado a partir das amostras em si.** A derivação nova não compara amostras
entre si para detectar conflito de voz — só extrai o que cada dimensão sustenta isoladamente.
Comparação de amostras (se a voz do capítulo 3 conflita com a do capítulo 1, por exemplo) é
julgamento adicional, não pedido nesta sessão; quem chama a etapa 13 continua responsável por
fornecer `amostras_conflitantes=True/False` como fato já apurado.

**Não construído nesta sessão, por instrução explícita ("sessões separadas")**: BVAA (etapa 11)
e `RelacaoAfirmacaoEvidencia` fora do que já existia (etapa 12) não foram tocados.

**Testes novos**: `tests/funcoes/test_ponte_modelo_p13.py::TestGerarPerfilDeVozCandidato` (7 casos)
e `tests/funcoes/test_execucao_p13.py::TestEtapaTrezeVerificacaoDeVoz` (+3 casos: derivação
completa registra candidato no contexto, amostras insuficientes não chama o modelo, metadados do
candidato ausentes vira `ENTRADA_NAO_FORNECIDA`). Suíte completa: 1154 passando (1144 + 10).

## Sessão de 2026-08-12 — camada de detecção construída, autorizada por instrução complementar

- **A lacuna registrada acima ("nenhuma detecção automática por análise semântica de texto foi
  construída, porque isso exigiria inferência fora do escopo desta peça") deixou de ser
  verdadeira para a Etapa 13 do P13** —
  `INSTRUCOES_COMPLEMENTARES_IMPLEMENTACAO_ECOSSISTEMA_REVISAO_LLM_R01.md §1.2` autoriza
  explicitamente construir essa camada, desde que separada da decisória: "AUTORIZA-SE A
  CONSTRUÇÃO da camada de detecção necessária à Etapa 13, desde que ela permaneça separada da
  camada normativa/decisória." `escolio/voz/deteccao.py` (novo módulo) implementa essa Camada
  A — `AchadoDeFidelidade` (tipo, observado, evidência, confiança, notas) — e
  `escolio/funcoes/ponte_modelo_p13.py::gerar_achados_fidelidade` liga a chamada real de modelo
  (Sonnet, `medium`) que produz esses achados a partir de texto real.
- **`avaliar()` (Camada B) não foi alterado** — confirma o limite explícito da instrução ("a
  camada B não deve ser alterada para simular a inexistência da camada A"). A ponte entre as
  duas é `escolio.voz.fidelidade.avaliar_a_partir_do_perfil` (novo, mesmo arquivo), que deriva de
  `PerfilDeVoz` os quatro fatos que a própria validação do perfil já garante
  (`autorizacao_ausente`, `proveniencia_ausente`, `amostra_unica`, `perfil_declarado_sem_
  amostras`) e recebe `amostras_conflitantes`/`exigencia_institucional_em_conflito` como
  parâmetros explícitos — não deriváveis de um `PerfilDeVoz` isolado.
- **Ainda não coberto**: "resolução de conflito" e "gate" como estruturas próprias (linha 111
  acima) continuam sem parâmetro dedicado; reversão/histórico de versões (linha 116 acima)
  continua não implementada. A camada de detecção não altera nenhuma dessas duas lacunas —
  resolve só a ausência de mecanismo de detecção sobre texto real.
- Ver `escolio/funcoes/LACUNAS.md` (sessão de 2026-08-12, etapa 13) para o lado do orquestrador.

## Não incluído nesta peça (fora de escopo, não lacuna)

- **Perfil de voz de quem comenta.** Bloqueado por `CLAUDE.md` §13.1 — não implementado em
  nenhuma forma, nem como enum alternativo, nem como campo comentado. Ver seção "Escopo" acima.
- **Histórico de versões e reversão operante [07, REVERSAO].** Esta peça define `PerfilDeVoz`
  como valor único, sem lista de versões anteriores nem função de reversão. Se um módulo futuro
  precisar de reversão operante, é extensão nova.
- **Ligação com `escolio/intervencao/` (P06) para "alteração forte exige gate humano
  compatível com o P06" [01, Princípios].** Não foi construída uma função que traduza um
  `DesvioBloqueante`/`ResultadoDeFidelidade` em `NivelIntervencao`/`InterventionRecord`. As duas
  peças permanecem independentes, comunicáveis apenas por quem chama ambas — mesmo tratamento
  dado à ausência de conversão operante entre vocabulários em `escolio/bvaa/LACUNAS.md`
  (LAC-BVAA-002).
- **Tecnologia, banco, persistência.** A fonte não escolhe nenhuma; esta implementação também
  não — `PerfilDeVoz` é dataclass em memória, como todo o resto de `escolio/`.

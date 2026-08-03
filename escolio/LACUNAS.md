# LACUNAS — implementação do schema P05

Lacunas e conflitos herdados do próprio pacote fonte (arquivo 08) e lacunas
encontradas durante a implementação em código. Nenhum item aqui foi
resolvido por inferência; cada um documenta a decisão tomada e por quê.

## Herdadas do arquivo 08 (LACUNAS_E_CONFLITOS)

- **LAC-P05-001** — taxonomia definitiva de `claim_type` não foi fornecida
  pelo P04; vocabulário mínimo adotado como está no dicionário de dados
  (arquivo 02). `OUTRA_CONTROLADA` exige `notes`, implementado em
  [relacao.py](relacao.py).
- **LAC-P05-002** — formato físico de persistência não definido. Esta
  implementação é puramente em memória (dataclasses Python), sem banco ou
  serialização — mantém o schema lógico e tecnicamente neutro, como o
  próprio pacote determina.
- **CON-P05-001** — divergência de rótulos entre estados do P04 e do
  "comando" não é resolvida aqui: P04 está fora do escopo desta peça.
- **LAC-P05-003** — regra de agregação de suficiência para múltiplas
  evidências de uma mesma afirmação depende de "tipo de afirmação e
  finalidade futura" — não implementada. `RegistroDeRelacoes` armazena as
  relações individualmente e não calcula nenhuma suficiência agregada.
- **CON-P05-002** — risco de `confidence` ser lido como probabilidade de
  verdade. Não é um problema de código; a matriz de suficiência/confiança
  em [matriz_suficiencia_confianca.py](matriz_suficiencia_confianca.py)
  aplica literalmente a regra "confiança não corrige evidência".

## Encontradas durante a implementação

- **Severidade "alerta" vs "bloqueante"** — o prompt pede que regras
  bloqueantes rejeitem e regras de alerta apenas sinalizem, "se o CSV
  distinguir os dois casos". O arquivo 04 só usa as severidades
  `BLOQUEANTE` e `MAIOR` — nenhuma linha usa uma categoria de alerta não
  bloqueante. Por fidelidade literal, todas as 20 regras foram
  implementadas como rejeição (`ErroDeCoerencia`), inclusive as duas de
  severidade `MAIOR` (RC-017, RC-018). A classe `AlertaDeCoerencia` existe
  em [erros.py](erros.py) para preservar a distinção estrutural, mas não é
  usada porque a fonte não fornece um caso concreto de regra não
  bloqueante.

- **RC-010 (leitura indireta exige fonte intermediária na proveniência)**
  — o dicionário de dados não define um campo estruturado para "fonte
  intermediária"; `provenance` é `string/objeto lógico` livre. A
  implementação verifica a presença da substring "intermediari" em
  `provenance` como proxy textual mínimo. É uma inferência de
  implementação, não de regra — documentada aqui por transparência, não
  movida para código adivinhado sobre o que uma "fonte intermediária"
  estruturada deveria conter.

- **RC-012 (conflito exige sufficiency=CONFLITANTE)** — "evidências
  conflitantes" é uma relação entre relações (duas relações da mesma
  afirmação que se contradizem), não um campo de uma relação isolada. O
  arquivo fonte não define o mecanismo de detecção automática de conflito
  — apenas a consequência quando o conflito já foi identificado. A
  implementação em `RegistroDeRelacoes.marcar_conflito` exige que o
  chamador declare explicitamente quais relações conflitam; não há
  detecção automática de conflito por comparação de `evidence_excerpt` ou
  `claim_text`, porque isso exigiria inferência semântica fora do escopo
  desta peça (schema determinístico, sem LLM).

- **RC-013 (edições divergentes não compartilham paginação)** — a
  implementação registra, por par (`claim_id`, `source_id`), a primeira
  edição em que a página foi confirmada (`PAGINA_CONFIRMADA`), e rejeita
  qualquer relação subsequente da mesma chave que declare
  `PAGINA_CONFIRMADA` sob uma `edition_or_version` diferente. Isto é uma
  escolha de implementação para tornar a regra verificável; o texto fonte
  não especifica a estrutura exata de armazenamento.

- **RC-019 (pedido para inventar evidência)** — implementada como detecção
  textual por palavras-gatilho (`invente`, `fabricar` etc.) sobre uma
  string de pedido, retornando um booleano para o chamador decidir a
  abstenção — não lança exceção nem constrói um registro, porque a regra
  se aplica *antes* de qualquer `RelacaoAfirmacaoEvidencia` existir. A
  lista de gatilhos é heurística e mínima; expandir essa heurística exigiria
  critério que a fonte não fornece.

- **`relation_version` como campo do modelo** — não está no dicionário de
  dados (arquivo 02), mas é exigido pela chave composta da unidade lógica
  no arquivo 01 (seção 2: "a chave composta (claim_id, source_id,
  relation_version) identifica cada relação versionada") e pelo protocolo
  de versionamento (arquivo 06, seção 4). Incluído em
  [relacao.py](relacao.py) como campo adicional à chave, não como um dos
  23 campos do dicionário — documentado para deixar claro que não é uma
  invenção de campo, mas a materialização de uma exigência de outro
  arquivo da mesma fonte.

## Não estrutural — não bloqueou a implementação

Nenhuma lacuna encontrada exigiu parar e perguntar: todas tinham tratamento
já indicado no próprio arquivo 08, ou eram uma decisão de implementação
(estrutura de dados, não regra de negócio) documentável aqui sem alterar o
significado de nenhuma regra fonte.

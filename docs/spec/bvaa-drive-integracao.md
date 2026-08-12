# Ligação BVAA ↔ Drive ↔ fluxo do P13

Sessão de 2026-08-12, duas partes. **Primeira parte**: instrução era propor o mecanismo de
"acesso verificável" usando `escolio/drive/` como fonte, marcar como `[PROPOSTA]`, registrar
alternativa descartada e — se a ligação exigir mudar `escolio/bvaa/` ou
`escolio/funcoes/execucao_p13.py` — registrar e parar antes de alterar. §§1-5 abaixo são esse
registro, inalterado.

**Segunda parte, mesma sessão: autorizado.** O professor autorizou editar
`escolio/funcoes/execucao_p13.py` e introduzir a dependência de `escolio.drive`, com duas
restrições literais: (1) `escolio/bvaa/` continua puro — a dependência de I/O fica do lado do
orquestrador, nunca da máquina de estados; (2) o acesso licencia apenas T04/T05, nenhuma outra
transição. **Construído** — ver §6.

## 1. O que já existe e o que falta (levantamento, não proposta)

Lido: `escolio/bvaa/*.py` (17 estados, 18 transições, `aplicar_transicao`/`avancar`,
`abster`, tabela de correspondência), `escolio/drive/*.py` (`conector.py`,
`autenticacao_usuario.py`), `escolio/funcoes/execucao_p13.py` e `execucao_p11.py` integrais.

Fatos que orientam a proposta:

- `escolio.bvaa.maquina.avancar(estado_atual, transicao_id)` **não recebe evidência como
  objeto** — recebe um `transicao_id` (string, ex. `"T05"`) já decidido por quem chama.
  A tabela de transições (`transicoes.py`) só guarda o texto fixo do gatilho
  (`evidencia_ou_gatilho`) como documentação; nenhuma validação de runtime confere se a
  evidência de fato existe. **Decidir qual `transicao_id` uma evidência concreta licencia é
  responsabilidade de quem integra — não existe hoje em lugar nenhum do projeto.**
- `escolio.drive.conector` retorna `ArquivoDrive` (id, nome, mime_type, tamanho, timestamp de
  modificação no Drive) a partir de listagem/busca, e `Path` local a partir de
  `baixar_arquivo`/`exportar_arquivo`. Não retorna hash de conteúdo nem timestamp de quando o
  sistema acessou — só o efeito de a chamada ter tido sucesso.
- `execucao_p13.py::_HANDLERS[11..15]` (verificação de fontes, evidências, voz, privacidade,
  problemas sistêmicos) e `execucao_p11.py::_HANDLERS[16]` ("controle BVAA") são todos
  `_etapa_diagnostico_sem_schema`/`_etapa_ponto_de_extensao` — handlers genéricos que sempre
  retornam `PARADA, PONTO_DE_EXTENSAO_DE_MODELO`, sem qualquer objeto de entrada que aceite
  evidência bibliográfica. Nenhum importa `escolio.bvaa` nem `escolio.drive`.
- `ContextoExecucaoP13`/`EntradaEtapaP13` não têm campo para estado BVAA por fonte citada.

Conclusão do levantamento: a "ligação" não é um fio faltante entre dois módulos prontos — é uma
peça de lógica nova (que evidência licencia qual transição) mais a edição de dois arquivos de
código existentes. Ver §4.

## 2. Mecanismo proposto `[PROPOSTA]`

### 2.1 Definição de "acesso verificável"

`[PROPOSTA]`: acesso verificável é o retorno de uma chamada real e bem-sucedida a
`escolio.drive.conector` contra um repositório de fonte de verdade já disponibilizado
(biblioteca do professor ou pasta de quarentena "Escolio Fontes", por [P22/BL-027, decisão do
`USUARIO_PROPONENTE` 2026-08-09] — nunca resultado de busca na internet, que exige o gate de
disponibilização antes de contar como fonte). "Verificável" significa: outra pessoa, rodando a
mesma chamada contra o mesmo Drive, obtém o mesmo resultado — não é afirmação do modelo sobre o
texto, é o retorno tipado de uma API.

### 2.2 Objeto de evidência — novo, ainda não escrito

```
EvidenciaDeAcessoDrive:
    arquivo: ArquivoDrive        # de escolio.drive.conector
    operacao: OperacaoDeAcesso   # enum: LOCALIZADO | BAIXADO | EXPORTADO
    caminho_local: Path | None   # presente só quando operacao in {BAIXADO, EXPORTADO}
```

Construído inteiramente a partir dos retornos já existentes de `listar_arquivos_da_pasta`,
`buscar_arquivos`, `baixar_arquivo`, `exportar_arquivo` — nenhuma chamada nova ao Drive além das
que o conector já expõe.

### 2.3 Função de licenciamento — nova, ainda não escrita

```
transicao_licenciada_por(evidencia: EvidenciaDeAcessoDrive) -> str | None
```

Mapeamento proposto, pelas 18 transições já fixas em `escolio/bvaa/transicoes.py`:

| `operacao` da evidência | Transição licenciada | Estado resultante |
|---|---|---|
| `LOCALIZADO` (arquivo apareceu em listagem/busca real) | T04 | `ACESSIVEL` |
| `BAIXADO` ou `EXPORTADO` (bytes recuperados com sucesso) | T05 | `ACESSADA` |

Retorna `None` (nenhuma transição) para qualquer estado que a evidência de acesso por si só não
comprova — leitura integral/parcial, confirmação de página, validação, recomendação. Essas
continuam exigindo exame do conteúdo por juízo humano ou de modelo, exatamente o que
`PONTO_DE_EXTENSAO_DE_MODELO` já marca nas etapas 11-15 de `execucao_p13.py`. **O Drive fecha o
vão `OBRA_NAO_IDENTIFICADA → ACESSADA`; não fecha nada além disso** — limite reconhecido da
proposta, não lacuna a esconder.

Consequência declarada: mesmo com esta peça construída, nenhuma citação chega a
`LEITURA_INTEGRAL`, `PAGINA_CONFIRMADA`, `VALIDADA` ou `RECOMENDADA` sem uma etapa de modelo
(ou humana) que efetivamente examine o conteúdo baixado — o gate de §26 ("não confirma leitura;
não confirma passagem; não confirma página") permanece parcialmente aberto até essa etapa
existir. Esta proposta resolve a metade "acesso", não a metade "leitura".

### 2.4 Onde este código moraria — e por que isso já é a linha que a instrução manda parar antes de cruzar

Duas opções, nenhuma delas neutra:

- **Dentro de `escolio/bvaa/`** (ex. `evidencia_drive.py`): mantém a lógica de licenciamento ao
  lado da máquina que ela avança, mas introduz em `escolio/bvaa/` uma dependência nova de
  `escolio.drive` que hoje não existe — o pacote passa a importar infraestrutura de rede/API
  externa, algo que os 7 módulos atuais de `escolio/bvaa/` (todos puros, sem I/O) não fazem.
- **Fora de `escolio/bvaa/`**, num módulo de integração novo (ex.
  `escolio/integracoes/bvaa_drive.py` ou dentro de `escolio/funcoes/`): não altera nenhum
  arquivo existente de `escolio/bvaa/`, mas ainda assim precisa importar de dois pacotes hoje
  desacoplados.

Nenhuma das duas evita a segunda parte: **ligar ao fluxo do P13 exige editar
`escolio/funcoes/execucao_p13.py`**. Os handlers das etapas 11-15 hoje são
`_etapa_diagnostico_sem_schema(nome_curto)` — uma fábrica sem parâmetros de entrada, sempre
`PARADA`. Fazê-los consumir `EvidenciaDeAcessoDrive` e avançar `EstadoBibliografico` exige, no
mínimo:

1. Novo(s) campo(s) em `EntradaEtapaP13` (ex. `evidencias_de_acesso: dict[str, EvidenciaDeAcessoDrive] | None`).
2. Novo(s) campo(s) em `ContextoExecucaoP13` para guardar o `EstadoBibliografico` corrente por
   fonte citada (hoje não existe nenhum lugar para isso).
3. Substituir a entrada `11` (e possivelmente 12) de `_HANDLERS` por um handler real que chama
   `transicao_licenciada_por` e `escolio.bvaa.maquina.avancar`, decidindo `EXECUTADA` vs.
   `PARADA` conforme a evidência fornecida.
4. Decidir o que fazer quando `transicao_licenciada_por` retorna `None` mas a etapa foi chamada
   com evidência — hoje não há vocabulário para "evidência insuficiente para esta transição
   específica, mas não é ausência de evidência" na `CausaDeParada` de seis membros.

Cada um dos quatro pontos é edição de `escolio/funcoes/execucao_p13.py`. **Por instrução desta
sessão, nenhum deles foi feito.** Registrado aqui; ver §3 para o motivo de não avançar mesmo
sendo tecnicamente possível numa sessão maior.

## 3. Por que parar aqui, e não só "fazer o mínimo"

A instrução da sessão foi explícita — "se a ligação exigir mudança em `escolio/bvaa/` ou em
`execucao_p13.py`, registre e pare antes de alterar" — e o levantamento em §2.4 confirma que
exige. Além de obedecer à instrução literal, três razões de fundo tornam isso a decisão certa,
não só a mais cautelosa:

- **`CausaDeParada` tem 6 membros fechados, e nenhum deles nomeia "evidência de acesso
  insuficiente para a transição pedida".** Adicionar um handler real sem decidir esse
  vocabulário produziria uma etapa que ora usa `PONTO_DE_EXTENSAO_DE_MODELO` (evidência ausente)
  ora silenciosamente aceita qualquer evidência fornecida como suficiente — exatamente o "erra
  para o lado de produzir saída" que CLAUDE.md §10 item 3 identifica como o julgamento caro que
  não se deve automatizar por conveniência.
- **Não há precedente de decisão de arquitetura tomada nesta sessão sem o professor.** BL-021
  (forma do orquestrador de P13) e BL-022 (convenção de ID) só foram implementados depois de
  "instrução expressa do professor" decidindo a forma — antes disso, ficaram registrados e
  parados por sessões inteiras (2026-08-09, sessão 9 do plano P13). Este item tem a mesma
  natureza: forma de integração entre dois módulos existentes, sem fonte que declare a forma.
- **`escolio/bvaa/` hoje é puro (sem I/O, sem dependência externa)** — os 77 testes do módulo
  não tocam rede. Fazer o pacote depender de `escolio.drive` (ou fazer `escolio/funcoes/`
  depender dos dois ao mesmo tempo) é uma mudança de forma de dependências que merece decisão
  explícita, não só "onde cabe o código".

## 4. Alternativas descartadas `[PROPOSTA]`

1. **Pular a máquina de estados do BVAA; verificar só "o arquivo existe no Drive" e registrar
   isso como texto livre em `ResultadoDeEtapa.justificativa`.** Descartada: P13 §26 exige
   aplicar o BVAA **integralmente** — a distinção entre `LOCALIZADA`/`ACESSIVEL`/`ACESSADA`/
   `LEITURA_*` é literal do contrato (17 estados nomeados), não um detalhe de implementação. Uma
   checagem binária "existe/não existe" colapsaria essa distinção — o mesmo defeito que
   CLAUDE.md §7 proíbe ("não colapsar dois vocabulários em um") aplicado a um vocabulário só,
   empobrecido pela metade.
2. **Usar `ArquivoDrive.modificado_em` como prova de leitura íntegra.** Descartada:
   `modificado_em` é o timestamp de última edição do arquivo *no Drive* (por qualquer pessoa com
   acesso), não de quando o sistema o examinou. Tratá-lo como evidência de leitura inventaria
   uma correspondência que a API do Google não garante — o mesmo tipo de inferência que
   CLAUDE.md §11 proíbe ("lacuna não se preenche por plausibilidade").
3. **Fazer o roteador de função (`escolio/funcoes/roteador.py`) chamar o Drive/BVAA antes de
   despachar para `execucao_p13.py`, em vez de dentro das etapas 11-15.** Descartada por ora:
   moveria a decisão de "quando verificar" para fora da espinha de 29 etapas que P13 declara —
   contraria a regra do CLAUDE.md §4 de que a espinha nomeia fases e não se funde execução; a
   verificação bibliográfica é parte do diagnóstico por unidade (etapas 11-15), não do
   roteamento inicial (E1).

## 5. Próxima ação única, se o professor quiser reabrir isto

Decidir a forma da integração (dependência de `escolio/bvaa/` sobre `escolio.drive`, ou módulo
de integração separado) e autorizar a edição de `escolio/funcoes/execucao_p13.py` — decisão dele,
não inferível daqui. Enquanto isso não ocorrer, as etapas 11-15 de P13 continuam
`PONTO_DE_EXTENSAO_DE_MODELO`, como já estavam.

**Superado pela §6 — o professor decidiu e autorizou, mesma sessão.**

## 6. Construído (2026-08-12) — o que ficou exatamente como proposto e o que a implementação forçou a decidir

`escolio/funcoes/bvaa_drive.py` (novo módulo, orquestrador — não em `escolio/bvaa/`):
`OperacaoDeAcesso` (`LOCALIZADO | BAIXADO | EXPORTADO`), `EvidenciaDeAcessoDrive` (dataclass
frozen: `arquivo: ArquivoDrive`, `operacao: OperacaoDeAcesso`, `caminho_local: Path | None`, com
`__post_init__` exigindo `caminho_local` só quando `operacao` recupera bytes),
`transicao_licenciada_por` (total sobre os três membros: `LOCALIZADO→"T04"`,
`BAIXADO`/`EXPORTADO→"T05"`) e `avancar_por_evidencia` (chama
`escolio.bvaa.maquina.avancar`, propaga `ErroDeTransicaoBibliografica` sem capturar).
`escolio/bvaa/` não foi alterado — zero linhas tocadas, zero import novo em qualquer arquivo do
pacote. Confirma a leitura da §2.4: a lógica de licenciamento (evidência → transição) não existia
em nenhum dos dois pacotes; ela mora inteiramente no módulo novo.

`escolio/funcoes/execucao_p13.py`: `EntradaEtapaP13.evidencias_de_acesso: dict[str,
EvidenciaDeAcessoDrive] | None`, `ContextoExecucaoP13.estados_bibliograficos: dict[str,
EstadoBibliografico]` (estado corrente por `unit_id` de `ItemDeReferencia`; ausência de entrada
é o estado inicial `OBRA_NAO_IDENTIFICADA`, literal de P04/03, não inferência), e um handler real
para a etapa 11 (`_etapa_11_verificacao_de_fontes`) substituindo o genérico. Etapas 12-15
inalteradas — nenhum outro handler tocado.

**Decisão que a implementação forçou e que a proposta original não previu explicitamente: qual
das etapas 11-15 recebe a ligação.** A proposta (§2) falava de "etapas 11-15" genericamente. Ao
escrever o handler, ficou claro que só a etapa 11 ("verificação de fontes" — a fonte
existe/está acessível) corresponde ao que evidência de Drive comprova; a etapa 12 ("verificação
de evidências" — o conteúdo confirma a afirmação) é outro julgamento, sobre correspondência
afirmação-conteúdo, que Drive não toca. `[PROPOSTA]`, decidida nesta implementação: só a etapa 11
foi ligada; 12-15 permanecem `PONTO_DE_EXTENSAO_DE_MODELO` exatamente como antes.

**Comportamento quando `evidencias_de_acesso` não é fornecido**: idêntico ao anterior a esta
sessão — `PARADA`/`PONTO_DE_EXTENSAO_DE_MODELO`, mesma causa. O teste que já existia
(`test_avanca_ate_selecao_e_para_em_verificacao_de_fontes`) continua passando sem alteração —
nenhuma regressão no caminho sem evidência.

**Comportamento quando a evidência é fornecida mas o estado bibliográfico atual da fonte não é o
`estado_entrada` exigido por T04/T05** (ex.: fonte ainda em `OBRA_NAO_IDENTIFICADA`, nunca passou
por T01-T03): `ErroDeTransicaoBibliografica` de `escolio.bvaa` é capturado e relançado como
`ErroDeExecucaoP13("P13-§26", ...)` — bloqueante, não silenciosamente ignorado. T01-T03
(identificação de obra/edição/localização) continuam sem mecanismo — nenhuma sessão os liga a
Drive nem a modelo; permanecem lacuna aberta, não desta peça.

Testes: `tests/funcoes/test_bvaa_drive.py` (10 casos, Drive mockado via
`unittest.mock.MagicMock` sobre `escolio.drive.conector`, mesmo padrão de
`tests/drive/test_conector.py` — inclui evidência construída a partir do retorno real, mockado,
de `listar_arquivos_da_pasta`/`baixar_arquivo`, não só objetos montados à mão) e quatro casos
novos em `tests/funcoes/test_execucao_p13.py` (`TestEtapaOnzeVerificacaoDeFontes`: sem evidência;
evidência válida avança `LOCALIZADA→ACESSIVEL`; `unit_id` de evidência sem `ItemDeReferencia`
correspondente levanta; evidência sem identificação prévia da obra levanta). Suíte completa:
1027 passando, 16 skipped (sem regressão) — ver `docs/backlog.md` BL-027 para o número anterior.

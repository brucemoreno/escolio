"""Orquestrador de execução do P13 — fecha BL-021/BL-022 (docs/backlog.md).

## Forma, por instrução do professor (2026-08-09)

Um módulo de execução por função — este arquivo é o do P13 — que percorre as
etapas declaradas em `escolio/funcoes/p13.py` chamando o que
`escolio/comentarios/` (sessões 1-8) já implementou. Nenhum executor
genérico: outra função (P10, P11...) exigiria seu próprio módulo, com sua
própria tabela de etapas — mesma disciplina que já separa `p10.py` de
`p13.py` [CLAUDE.md §4: "um módulo por função, nunca um executor genérico"].

## POL-012 — por que `avancar()` executa no máximo uma etapa por chamada

`escolio/funcoes/LACUNAS.md` já registrava, antes desta sessão, que nenhum
dos módulos de função tem `executar`: "POL-012 proíbe executar encadeamento
automático; permite registrar exatamente uma próxima ação permitida ou
nenhuma automática." Este módulo não revoga essa leitura — a implementa.
`avancar()` calcula `DECLARACAO.proxima_etapa(concluidas)`, executa **só
essa etapa** (nunca a seguinte, mesmo que a atual tenha sucesso) e devolve o
controle ao chamador. Percorrer as 29 etapas de um documento real exige 29
(ou mais, com repetição) chamadas explícitas — nunca um `for` interno.

## Por que a maioria das etapas não executa nesta sessão

Cada etapa que a fonte descreve como diagnóstico, seleção de conteúdo ou
redação (juízo humano ou de modelo) permanece um ponto de extensão
explícito — o orquestrador não o preenche por conveniência nem interpola um
valor plausível [CLAUDE.md §11]. Uma etapa some do caminho feliz sem se
tornar aprovação silenciosa: `ResultadoDeEtapa.tipo` distingue seis causas de
parada (`CausaDeParada`), cada uma com critério próprio — nunca uma genérica
"não implementado".

**Sessão de 2026-08-09 (ligação ao cliente da API) — etapas 8, 9, 16, 17 e
18 deixam de ser pontos de extensão permanentes.** `escolio/funcoes/
ponte_modelo_p13.py` liga essas cinco etapas a `escolio/cliente/`: quando o
chamador fornece `EntradaEtapaP13.cliente` (uma `ClienteAnthropic`) junto
com os candidatos de entrada daquela etapa (`unidades_para_matriz_
criticidade`, ou os `candidatos_para_*` das etapas 16-18), o handler chama a
API em vez de parar. Fornecer o objeto final já construído
(`matrizes_criticidade`, `comentarios_matriz`, ...) continua tendo
prioridade — chamar o modelo é o caminho alternativo, não o único. Sem
`cliente` e sem entrada, o comportamento é idêntico ao de antes desta
sessão: `PARADA`/`PONTO_DE_EXTENSAO_DE_MODELO`. As etapas 11-15
(`PONTO_DE_EXTENSAO_DE_MODELO`, sem objeto de sessão anterior que ligue
candidato a verificação — LAC-FUNC-019) e 19-24 (`SEM_FONTE_DE_
VERIFICACAO`) não são tocadas por esta sessão.

## BL-022 resolvido aqui, não nos módulos de sessão 1-6

`Paragrafo.unit_id`, `MatrizCriticidade.unit_id`, `MatrizSeletividade.unit_id`
e `P13Comment.unit_id`/`document_id` continuam `str` soltos em seus módulos
de origem — não alterados. A resolução decidida nesta sessão, `[PROPOSTA]`,
mora inteiramente aqui, no único lugar que agora tem os dois lados da
relação em mãos ao mesmo tempo:

- `document_id` canônico = `material_id_de_documento(documento)` [P19 §10],
  não `InputItem.input_id` [P09 §6.1]. Razão: `material_id` é estável entre
  cópias e independente do request que o menciona; `input_id` é identidade
  de item de um envelope de requisição específico, sem garantia de se
  repetir entre duas requisições sobre o mesmo documento. `registrar_
  comentario` rejeita `P13Comment.document_id` que não bata com esse valor.
- `unit_id` conhecido = o conjunto reunido na etapa 7 (`unidades_conhecidas`)
  a partir da estrutura de `DocumentoIngerido`. `MatrizCriticidade.unit_id`,
  `MatrizSeletividade.unit_id` e `P13Comment.unit_id` são conferidos contra
  esse conjunto antes de aceitos — divergência levanta `ErroDeExecucaoP13`,
  nunca passa silenciosa.

Isto não retroage sobre BL-024 (`exige_referencia_valida_a_criticidade`,
sessão 2), que continua sendo a checagem entre `MatrizSeletividade` e
`MatrizCriticidade` propriamente dita; este módulo só acrescenta a camada
que faltava: as duas contra a estrutura do documento.

## Sessão de 2026-08-12 — etapa 11 ligada ao BVAA via `escolio.drive`

Por instrução expressa do professor, autorizando a proposta registrada em
`docs/spec/bvaa-drive-integracao.md`: a etapa 11 ("verificação de fontes")
deixa de ser um ponto de extensão genérico e passa a consumir
`EntradaEtapaP13.evidencias_de_acesso` — evidência real de
`escolio.drive.conector`, encapsulada em `EvidenciaDeAcessoDrive`
(`escolio/funcoes/bvaa_drive.py`). Duas restrições do professor, ambas
literais no código: (1) `escolio/bvaa/` continua puro — a dependência de
`escolio.drive` mora só em `escolio/funcoes/bvaa_drive.py`, nunca dentro da
máquina de estados; (2) esta primeira peça licenciava exclusivamente
T04/T05 — identificação de obra/edição (T01-T03) foi tratada como fora de
escopo *desta peça*, não como impossível; a segunda peça do mesmo dia
(abaixo) fecha isso. Sem nenhuma evidência, a etapa 11 se comporta como
antes: `PONTO_DE_EXTENSAO_DE_MODELO`.

## Sessão de 2026-08-12 (segunda peça) — etapas 12, 13, 14, 15 e T01-T03

Autorizado por `INSTRUCOES_COMPLEMENTARES_IMPLEMENTACAO_ECOSSISTEMA_REVISAO_LLM_R01.md`:

- **Etapa 11** passa a encadear T01-T03 (identificação/localização, `EvidenciaDeIdentificacaoDrive`)
  antes de T04/T05 (acesso, já existente) — escolha técnica delegada ao `ENGENHEIRO_LLM` [§3],
  não decisão normativa nova.
- **Etapa 12** (verificação de evidências) aceita `RelacaoAfirmacaoEvidencia` (schema P05,
  `escolio/relacao.py`) já construída e validada — peça existente, nunca antes cotejada com esta
  etapa; nenhuma chamada de modelo nova, mesmo padrão de aceitar objeto pronto que as etapas 8/9
  já usam quando o objeto vem do chamador.
- **Etapa 13** (verificação de voz) ganha handler real ligado à Camada A (`escolio.voz.deteccao`,
  `ponte_modelo_p13.gerar_achados_fidelidade`) → Camada B (`escolio.voz.fidelidade.
  avaliar_a_partir_do_perfil`, que não altera `avaliar()` — Instruções Complementares §1.1).
- **Etapa 14** (verificação de privacidade) deixa de ser ponto de extensão: `INSTRUCOES_
  COMPLEMENTARES...§2` resolve CO-012 proibindo gate obrigatório — a etapa agora é sempre
  `EXECUTADA`, uma salvaguarda residual determinística
  (`escolio.funcoes.salvaguarda_privacidade_p13`) que nunca bloqueia e nunca aciona por tema.
- **Etapa 15** (problemas sistêmicos conhecidos) aceita a lista opcional já nomeada em `p13.py`
  [§6.3] — puro wiring, sem julgamento novo.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from escolio.adaptadores.ingestao_para_input_item import material_id_de_documento
from escolio.bvaa.erros import ErroDeTransicaoBibliografica
from escolio.bvaa.vocabulario import EstadoBibliografico
from escolio.cliente.erros import ErroDeCliente
from escolio.comentarios.auditoria import LoteDeAuditoria, RelatorioAuditoriaFinal, auditar_lote
from escolio.comentarios.comentario import P13Comment
from escolio.comentarios.criticidade import MatrizCriticidade
from escolio.comentarios.erros import ErroDeComentario
from escolio.comentarios.registro import RegistroDeComentarios
from escolio.comentarios.seletividade import (
    MatrizSeletividade,
    aplicar_selecao,
    exige_referencia_valida_a_criticidade,
)
from escolio.comentarios.vocabulario import (
    COMMENT_TYPE_COMENTARIO_MATRIZ,
    COMMENT_TYPE_REMISSAO_A_COMENTARIO_MATRIZ,
)
from escolio.funcoes import ponte_modelo_p13 as ponte
from escolio.funcoes.bvaa_drive import (
    EvidenciaDeAcessoDrive,
    EvidenciaDeIdentificacaoDrive,
    avancar_por_evidencia,
    avancar_por_identificacao,
)
from escolio.funcoes.curador_bvaa import EscalonamentoDoCurador, curar_referencias
from escolio.funcoes.declaracao import Etapa
from escolio.funcoes.p13 import DECLARACAO as DECLARACAO_P13
from escolio.funcoes.roteador import AdmissaoDeMaterial, DecisaoDeRoteamento
from escolio.funcoes.salvaguarda_privacidade_p13 import (
    AlertaDePrivacidade,
    detectar_exposicao_manifesta,
)
from escolio.funcoes.vocabulario import FuncaoId
from escolio.ingestao.modelos import DocumentoIngerido
from escolio.relacao import RelacaoAfirmacaoEvidencia
from escolio.voz.deteccao import AchadoDeFidelidade
from escolio.voz.fidelidade import AvaliacaoDeFidelidade, avaliar_a_partir_do_perfil
from escolio.voz.perfil import PerfilDeVoz

ARQUIVO_FONTE = "P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md"


class ErroDeExecucaoP13(Exception):
    """Violação bloqueante da execução — regra bloqueante levanta exceção,
    não sinaliza e prossegue [CLAUDE.md §8]."""

    def __init__(self, regra_id: str, fundamento: str, detalhe: str = ""):
        self.regra_id = regra_id
        self.fundamento = fundamento
        self.detalhe = detalhe
        msg = f"[{regra_id}] {fundamento} (fonte: {ARQUIVO_FONTE})"
        if detalhe:
            msg += f" — {detalhe}"
        super().__init__(msg)


class TipoDeResultadoEtapa(str, Enum):
    EXECUTADA = "EXECUTADA"
    PARADA = "PARADA"


class CausaDeParada(str, Enum):
    """Sete causas distintas de não-execução — nunca uma genérica "não
    implementado". Cada uma é uma leitura diferente de por que o código
    para aqui, e cada uma pede uma ação diferente de quem opera o sistema."""

    MATERIAL_NAO_DECLARADO = "MATERIAL_NAO_DECLARADO"
    """Etapa 1. `AdmissaoDeMaterial` do material não é DECLARADO para F04 —
    ato humano de classificação ainda não ocorreu [BL-014]. Resolve com
    `roteador.abstencao_por_fora_de_escopo`, não com este módulo."""

    PRECONDICAO_NAO_SATISFEITA = "PRECONDICAO_NAO_SATISFEITA"
    """Um fato já determinado pela própria `Request` é negativo (ex.:
    `requester.authority_basis` vazio) — não há entrada adicional que o
    chamador possa fornecer nesta execução para reverter isso; exige nova
    `Request`."""

    ENTRADA_NAO_FORNECIDA = "ENTRADA_NAO_FORNECIDA"
    """A etapa tem schema de aceitação (`EntradaEtapaP13`) e código para
    processá-lo, mas o campo correspondente não veio preenchido nesta
    chamada. Repetir a chamada com o campo preenchido é o caminho normal."""

    PONTO_DE_EXTENSAO_DE_MODELO = "PONTO_DE_EXTENSAO_DE_MODELO"
    """A etapa exige juízo humano ou de modelo sobre o conteúdo do
    documento (diagnóstico E4: fontes, evidência, voz, problemas
    sistêmicos — privacidade não é mais deste grupo, ver etapa 14 abaixo)
    para o qual, nesta chamada, não veio um objeto de entrada aceitável —
    diferente de `ENTRADA_NAO_FORNECIDA`, o campo existe mas o que ele
    aceita é julgamento (humano ou de modelo), nunca um valor mecânico."""

    SEM_FONTE_DE_VERIFICACAO = "SEM_FONTE_DE_VERIFICACAO"
    """Nenhuma seção do contrato liga esta etapa nomeada a um critério
    verificável — mesma disciplina de `NAO_VERIFICAVEL_NESTA_SESSAO` em
    `escolio/comentarios/auditoria.py`."""

    FORA_DO_FLUXO_DE_EXECUCAO = "FORA_DO_FLUXO_DE_EXECUCAO"
    """Etapas 26-29 — `Etapa.fase is None`: decisão autoral, homologação
    documental, piloto Word real, ativação operacional. Atos humanos ou
    pós-homologação; o sistema nunca homologa [CLAUDE.md §1-§2] e este
    orquestrador nunca tenta executá-los, incondicionalmente."""

    FALHA_NA_CHAMADA_AO_MODELO = "FALHA_NA_CHAMADA_AO_MODELO"
    """Sessão de 2026-08-12 (quarta peça) — achado do primeiro piloto real
    contra um capítulo verdadeiro: uma chamada real ao modelo pode falhar
    por um erro do próprio cliente (`escolio.cliente.erros.ErroDeCliente` —
    resposta truncada por `max_tokens`, limite de taxa, timeout, erro de
    conexão, erro de servidor) sem que nenhum julgamento tenha sido
    ausente e sem que nenhuma entrada tenha faltado — a etapa tinha tudo
    que precisava e a chamada em si não completou. Antes desta sessão,
    esse erro propagava como exceção Python não capturada, derrubando o
    percurso sem registrar a tentativa em `estado.historico` — quebra da
    mesma disciplina que todas as outras seis causas já respeitavam
    (nunca um crash sem causa estruturada). `retryable` (atributo do
    próprio `ErroDeCliente`) diz se repetir a mesma chamada pode ajudar —
    esta causa não decide isso por si, só relata o que o cliente disse."""

    RESPOSTA_DO_MODELO_MAL_FORMADA = "RESPOSTA_DO_MODELO_MAL_FORMADA"
    """Sessão de 2026-08-13 — achado do segundo piloto real contra o capítulo
    5, depois da correção de lotes de 15 (LACUNAS.md, "quarta peça"): a
    chamada ao modelo completa (`stop_reason` normal, sem truncamento), mas
    o `tool_use.input` devolvido não corresponde à forma que o dataclass de
    destino exige (`ponte_modelo_p13.ErroDePonteModeloP13` — ex.: item de
    `matrizes`/`achados`/`comentarios` veio como string em vez de objeto).
    Categoria diferente de `FALHA_NA_CHAMADA_AO_MODELO`: ali a chamada em si
    não completou; aqui ela completou e respondeu algo que não valida. Antes
    desta sessão, esse erro propagava cru (`TypeError`/`AttributeError` não
    capturado dentro do próprio `_matriz_criticidade_de_item`, ou
    `ErroDePonteModeloP13` não capturado por este módulo) e derrubava o
    percurso sem registrar tentativa em `estado.historico` — mesma quebra de
    disciplina que motivou `FALHA_NA_CHAMADA_AO_MODELO`, causa diferente.
    Repetir a mesma chamada pode ou não ajudar (o modelo não é determinístico
    mesmo com o mesmo prompt); esta causa não afirma `retryable` como o
    `ErroDeCliente` faz, porque `ErroDePonteModeloP13` não carrega esse
    atributo — decisão de repetir fica com quem opera."""

    ESCALONAMENTO_BIBLIOGRAFICO_NECESSARIO = "ESCALONAMENTO_BIBLIOGRAFICO_NECESSARIO"
    """Sessão de 2026-08-13 — decisão do professor: a etapa 11 não exige
    mais, por padrão, que um humano já tenha construído evidência de
    identificação/acesso. `escolio.funcoes.curador_bvaa.curar_referencias`
    tenta produzir essa evidência sozinho (extração determinística +
    busca real no Drive); esta causa só ocorre quando o curador tentou
    **e nenhuma referência avançou** — cada uma travou por um motivo
    genuíno (`EscalonamentoDoCurador.motivo`, vocabulário de
    `GatilhoDeAbstencao`): obra/edição não identificável a partir do
    texto, busca sem resultado, credencial ausente ou acesso negado.
    Diferente de `PONTO_DE_EXTENSAO_DE_MODELO` (que significa "nenhuma
    tentativa automática é possível aqui"): esta causa significa "a
    tentativa automática ocorreu e travou de verdade" — a distinção
    importa para quem opera decidir a próxima ação (fornecer evidência
    manual vs. simplesmente repetir)."""


@dataclass(frozen=True)
class ResultadoDeEtapa:
    etapa: Etapa
    tipo: TipoDeResultadoEtapa
    justificativa: str
    causa: CausaDeParada | None = None

    def __post_init__(self) -> None:
        if self.tipo is TipoDeResultadoEtapa.PARADA and self.causa is None:
            raise ErroDeExecucaoP13(
                "EXECUCAO-INTERNA", "ResultadoDeEtapa com tipo=PARADA exige causa"
            )


@dataclass
class EntradaEtapaP13:
    """Schema de aceitação por etapa. Todo campo é opcional: sua ausência
    produz `ENTRADA_NAO_FORNECIDA` na etapa correspondente, nunca um valor
    inferido. Nenhum campo aqui introduz um schema novo de sessão anterior
    — cada um é ou um tipo já validado por `escolio/comentarios/`, ou um
    booleano de confirmação (etapas 3 e 5, que não têm objeto de sessão
    anterior a aceitar).

    `cliente` e os campos `unidades_para_*`/`candidatos_para_*` abaixo são
    desta sessão (ligação ao modelo, etapas 8, 9, 16-18
    [`escolio/funcoes/ponte_modelo_p13.py`]). Fornecer o objeto já
    construído (`matrizes_criticidade`, `comentarios_matriz`, ...) continua
    tendo prioridade sobre chamar o modelo — a etapa só chama a API quando
    o objeto final não veio e `cliente` + os candidatos de entrada vieram."""

    dependencias_obrigatorias_confirmadas: bool = False
    documento: DocumentoIngerido | None = None
    document_version: str | None = None
    matrizes_criticidade: list[MatrizCriticidade] | None = None
    matrizes_seletividade: list[MatrizSeletividade] | None = None
    comentarios_matriz: list[P13Comment] | None = None
    comentarios_individuais: list[P13Comment] | None = None
    remissoes: list[P13Comment] | None = None
    cliente: object | None = None
    unidades_para_matriz_criticidade: list[str] | None = None
    candidatos_para_comentario_matriz: list[MatrizSeletividade] | None = None
    candidatos_para_comentarios_individuais: list[MatrizSeletividade] | None = None
    candidatos_para_remissoes: list[MatrizSeletividade] | None = None
    matrix_comment_id_por_remissao: dict[str, str] | None = None
    evidencias_de_acesso: dict[str, EvidenciaDeAcessoDrive] | None = None
    """Etapa 11 (verificação de fontes) — evidência real de acesso ao Drive
    [`escolio/funcoes/bvaa_drive.py`, `docs/spec/bvaa-drive-integracao.md`],
    por `unit_id` de `ItemDeReferencia`. Licencia T04/T05 do BVAA."""
    evidencias_de_identificacao: dict[str, EvidenciaDeIdentificacaoDrive] | None = None
    """Etapa 11 — correspondência textual entre referência citada e arquivo
    do Drive [`escolio/funcoes/bvaa_drive.py`, T01-T03, escolha técnica
    delegada ao `ENGENHEIRO_LLM` — `INSTRUCOES_COMPLEMENTARES_
    IMPLEMENTACAO_ECOSSISTEMA_REVISAO_LLM_R01.md §3`]. Aplicada antes de
    `evidencias_de_acesso` para o mesmo `unit_id`, na mesma chamada."""
    servico_drive: object | None = None
    """Etapa 11 (sessão de 2026-08-13, curador automático) — serviço do
    Drive já autenticado [`escolio.drive.conector.construir_servico`].
    Fornecer isto tem o **mesmo papel que `cliente` tem para as etapas 8,
    9, 13, 16-18**: quando `evidencias_de_identificacao`/
    `evidencias_de_acesso` não vêm prontas e `documento.referencias` não
    está vazio, a etapa chama `escolio.funcoes.curador_bvaa.
    curar_referencias` em vez de parar — mesma prioridade já estabelecida
    (objeto pronto > chamar mecanismo automático > parar). Sem
    `servico_drive`, comportamento idêntico ao de antes desta sessão."""
    relacoes_afirmacao_evidencia: list[RelacaoAfirmacaoEvidencia] | None = None
    """Etapa 12 (verificação de evidências) — `RelacaoAfirmacaoEvidencia`
    já construída e validada [P05, `escolio/relacao.py`; P09 §12], fornecida
    pronta por quem chama. Lista vazia explícita (`[]`) é aceita como
    "nenhuma relação a verificar nesta chamada", distinto de `None` (não
    fornecido). Continua tendo prioridade sobre chamar o modelo — mesmo
    padrão de `matrizes_criticidade`/`matrizes_seletividade`."""
    unidades_para_relacao_afirmacao_evidencia: list[str] | None = None
    """Etapa 12 — `unit_id`s para geração via modelo
    [`escolio/funcoes/ponte_modelo_p13.py::gerar_relacoes_afirmacao_evidencia`]
    quando `relacoes_afirmacao_evidencia` não vem pronta. Exige `cliente`.
    Decisão do professor, sessão de 2026-08-13: a etapa deixa de exigir
    julgamento humano prévio como precondição de runtime — o sistema
    produz `sufficiency`/`confidence` preliminares, sujeitas a revisão."""
    gabarito_relacoes_afirmacao_evidencia: list[RelacaoAfirmacaoEvidencia] | None = None
    """Etapa 12 — julgamento humano prévio, quando existir, entra aqui como
    ORACLE/GABARITO de piloto (comparação com o que o modelo produziu),
    nunca como precondição de execução da etapa. Só registrado em
    `ContextoExecucaoP13.relacoes_afirmacao_evidencia_gabarito`; nenhuma
    comparação automática é feita nesta sessão — confronto é trabalho de
    quem avalia o piloto, não do orquestrador."""
    perfil_de_voz: PerfilDeVoz | None = None
    """Etapa 13 (verificação de voz) — perfil de voz do autor avaliado
    [P07, `escolio/voz/perfil.py`]."""
    achados_fidelidade: dict[str, list[AchadoDeFidelidade]] | None = None
    """Etapa 13 — achados de fidelidade (Camada A, `escolio/voz/
    deteccao.py`) já produzidos, por `unit_id`. Fornecer isto tem
    prioridade sobre chamar o modelo, mesmo padrão de `matrizes_
    criticidade`/`matrizes_seletividade`."""
    unidades_para_deteccao_fidelidade: list[str] | None = None
    """Etapa 13 — `unit_id`s para detecção via modelo
    [`escolio/funcoes/ponte_modelo_p13.py::gerar_achados_fidelidade`]
    quando `achados_fidelidade` não vem pronto. Exige `cliente` e
    `perfil_de_voz`."""
    amostras_conflitantes: bool = False
    """Etapa 13 — fato sobre o `perfil_de_voz` que `PerfilDeVoz` não
    valida por si (exige comparar amostras entre si); nunca assumido
    `False` por conveniência quando não fornecido explicitamente pelo
    chamador que de fato comparou as amostras."""
    exigencia_institucional_em_conflito: bool = False
    """Etapa 13 — idem, mas sobre conflito entre exigência institucional e
    preferência autoral; depende de contexto externo ao perfil."""
    problemas_sistemicos_conhecidos: list[str] | None = None
    """Etapa 15 — "lista de problemas sistêmicos conhecidos" [P13 §6.3,
    entrada opcional do professor, já citada em `escolio/funcoes/p13.py`].
    Lista vazia explícita confirma "nenhum problema sistêmico conhecido
    para esta chamada", distinto de `None`."""


@dataclass
class ContextoExecucaoP13:
    """Acumulado entre chamadas de `avancar()` — um `EstadoDeExecucaoP13`
    por percurso de um documento sob F04/P13."""

    request: object
    decisao_de_roteamento: DecisaoDeRoteamento
    documento: DocumentoIngerido | None = None
    document_id: str | None = None
    document_version: str | None = None
    cartografia: dict | None = None
    unidades_conhecidas: frozenset[str] = frozenset()
    matrizes_criticidade: list[MatrizCriticidade] = field(default_factory=list)
    matrizes_seletividade: list[MatrizSeletividade] = field(default_factory=list)
    selecionados: list[MatrizSeletividade] = field(default_factory=list)
    registro_comentarios: RegistroDeComentarios = field(default_factory=RegistroDeComentarios)
    todos_comentarios: list[P13Comment] = field(default_factory=list)
    relatorio_auditoria: RelatorioAuditoriaFinal | None = None
    estados_bibliograficos: dict[str, EstadoBibliografico] = field(default_factory=dict)
    """Estado BVAA corrente por `unit_id` de `ItemDeReferencia` — só
    populado/avançado pela etapa 11 via evidência de identificação/acesso
    ao Drive. Ausência de entrada para um `unit_id` é o estado inicial da
    máquina [`EstadoBibliografico.OBRA_NAO_IDENTIFICADA`], não uma
    inferência: é o ponto de partida literal de P04/03 para qualquer
    citação ainda não processada."""
    relacoes_afirmacao_evidencia: list[RelacaoAfirmacaoEvidencia] = field(default_factory=list)
    """Etapa 12 — `RelacaoAfirmacaoEvidencia` aceitas nesta execução (prontas
    ou geradas via modelo)."""
    relacoes_afirmacao_evidencia_gabarito: list[RelacaoAfirmacaoEvidencia] = field(default_factory=list)
    """Etapa 12 — ORACLE/GABARITO de piloto, quando fornecido. Registrado
    para comparação humana posterior; nunca lido por nenhum outro handler
    desta execução."""
    avaliacoes_fidelidade: dict[str, AvaliacaoDeFidelidade] = field(default_factory=dict)
    """Etapa 13 — `AvaliacaoDeFidelidade` (Camada B) por `unit_id`."""
    alertas_privacidade: list[AlertaDePrivacidade] = field(default_factory=list)
    """Etapa 14 — achados da salvaguarda residual sobre `ctx.selecionados`.
    Lista vazia é o resultado normal e esperado para a maioria dos
    documentos — ausência de achado não é ausência de verificação."""
    problemas_sistemicos_conhecidos: list[str] = field(default_factory=list)
    """Etapa 15 — lista declarada pelo professor [§6.3], registrada aqui."""
    escalonamentos_bibliograficos: list[EscalonamentoDoCurador] = field(default_factory=list)
    """Etapa 11 (sessão de 2026-08-13) — paradas estruturadas do curador
    automático, acumuladas entre chamadas. Registrado mesmo quando a
    etapa como um todo é `EXECUTADA` (algumas referências avançaram,
    outras travaram) — nunca descartado silenciosamente; é o registro que
    torna "escalar quando travado" um caminho de código, não uma frase de
    log [CLAUDE.md §8]."""


@dataclass
class EstadoDeExecucaoP13:
    contexto: ContextoExecucaoP13
    historico: list[ResultadoDeEtapa] = field(default_factory=list)

    @property
    def concluidas(self) -> int:
        """Só etapas EXECUTADA avançam o ponteiro de fluxo — uma tentativa
        que parou não conta como concluída, e por isso a mesma etapa é
        reoferecida na próxima chamada [POL-012, "uma próxima ação, não
        encadeamento"]."""
        n = 0
        for r in self.historico:
            if r.tipo is not TipoDeResultadoEtapa.EXECUTADA:
                break
            n += 1
        return n

    @property
    def encerrado(self) -> bool:
        return DECLARACAO_P13.proxima_etapa(self.concluidas) is None


def construir_estado_inicial(request, decisao_de_roteamento: DecisaoDeRoteamento) -> EstadoDeExecucaoP13:
    """Ponto de entrada. Exige uma `DecisaoDeRoteamento` já produzida por
    `escolio.funcoes.roteador.rotear` — este módulo não roteia de novo, só
    consome o resultado [CLAUDE.md §4: cada função preserva seu próprio
    fluxo; o roteador não é reimplementado aqui]."""
    if decisao_de_roteamento.funcao is not FuncaoId.F04:
        raise ErroDeExecucaoP13(
            "EXECUCAO-P13",
            "execucao_p13 só processa decisões de roteamento para F04/P13",
            detalhe=f"funcao={decisao_de_roteamento.funcao}",
        )
    return EstadoDeExecucaoP13(
        contexto=ContextoExecucaoP13(request=request, decisao_de_roteamento=decisao_de_roteamento)
    )


def _unidades_do_documento(documento: DocumentoIngerido) -> frozenset[str]:
    ids = []
    ids.extend(p.unit_id for p in documento.paragrafos)
    ids.extend(c.unit_id for c in documento.citacoes_recuadas)
    ids.extend(n.unit_id for n in documento.notas_de_rodape)
    ids.extend(f.unit_id for f in documento.figuras)
    return frozenset(ids)


def _exige_unit_id_conhecido(unit_id: str, unidades_conhecidas: frozenset[str], origem: str) -> None:
    if unit_id not in unidades_conhecidas:
        raise ErroDeExecucaoP13(
            "BL-022",
            "unit_id não pertence às unidades identificadas na etapa 7 (cartografia/identificação)",
            detalhe=f"{origem}: unit_id={unit_id!r}",
        )


def _exige_referencia_conhecida(unit_id: str, documento: DocumentoIngerido, origem: str) -> None:
    conhecidas = {r.unit_id for r in documento.referencias}
    if unit_id not in conhecidas:
        raise ErroDeExecucaoP13(
            "P13-§26",
            "unit_id de evidência de acesso não corresponde a nenhum ItemDeReferencia do documento",
            detalhe=f"{origem}: unit_id={unit_id!r}",
        )


def _justificativa_falha_cliente(erro: ErroDeCliente) -> str:
    """Mensagem comum para `CausaDeParada.FALHA_NA_CHAMADA_AO_MODELO` — um
    só lugar formata isso, para as quatro etapas que chamam modelo
    (8, 9, 13, 16-18) não repetirem a mesma string. `str(erro)` já inclui
    categoria/severidade/código [`ErroDeCliente.__init__`]; só falta dizer
    se vale a pena repetir a chamada sem mudar nada."""
    retentativa = "provavelmente vale repetir a mesma chamada" if erro.retryable else "repetir sem mudar nada não deve resolver"
    return f"chamada real ao modelo falhou ({retentativa}): {erro}"


def _justificativa_falha_ponte(erro: ponte.ErroDePonteModeloP13) -> str:
    """Mensagem comum para `CausaDeParada.RESPOSTA_DO_MODELO_MAL_FORMADA` —
    mesmo raciocínio de `_justificativa_falha_cliente`, um só lugar formata
    isso para as quatro etapas que chamam modelo (8, 9, 13, 16-18)."""
    return f"resposta do modelo não corresponde ao formato esperado: {erro}"


def _exige_document_id_canonico(document_id: str, esperado: str, origem: str) -> None:
    if document_id != esperado:
        raise ErroDeExecucaoP13(
            "BL-022",
            "document_id diverge do material_id canônico do documento [P19 §10, PROPOSTA]",
            detalhe=f"{origem}: document_id={document_id!r} esperado={esperado!r}",
        )


# --- Handlers, um por etapa (ordem 1..29) -------------------------------


def _etapa_1_intake(ctx: ContextoExecucaoP13, _e: EntradaEtapaP13):
    declarados = tuple(
        m for m in ctx.decisao_de_roteamento.materiais if m.admissao is AdmissaoDeMaterial.DECLARADO
    )
    if not declarados:
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.MATERIAL_NAO_DECLARADO, (
            "nenhum material da requisição está DECLARADO para F04 "
            "[InputItem.classification.functions, BL-014] — abstenha com "
            "roteador.abstencao_por_fora_de_escopo, não prossiga aqui"
        )
    return TipoDeResultadoEtapa.EXECUTADA, None, f"{len(declarados)} material(is) declarado(s) para F04"


def _etapa_2_confirmacao_de_autoridade(ctx: ContextoExecucaoP13, _e: EntradaEtapaP13):
    if not ctx.request.requester.authority_basis:
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.PRECONDICAO_NAO_SATISFEITA, (
            "requester.authority_basis vazio — requisição não declara base de autoridade [P09 §4]"
        )
    return TipoDeResultadoEtapa.EXECUTADA, None, "requester.role e authority_basis presentes [P09 §4]"


def _etapa_3_verificacao_das_dependencias(ctx: ContextoExecucaoP13, e: EntradaEtapaP13):
    if not e.dependencias_obrigatorias_confirmadas:
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.ENTRADA_NAO_FORNECIDA, (
            "nenhum registro em código do estado de homologação de "
            f"{DECLARACAO_P13.dependencias_obrigatorias} — confirmação é ato humano "
            "[mesmo padrão de InputItem.classification.functions, BL-014]"
        )
    return TipoDeResultadoEtapa.EXECUTADA, None, "dependências obrigatórias confirmadas por autoridade competente"


def _etapa_4_ingestao_controlada(ctx: ContextoExecucaoP13, e: EntradaEtapaP13):
    if e.documento is None:
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.ENTRADA_NAO_FORNECIDA, "documento (DocumentoIngerido) não fornecido"
    ctx.documento = e.documento
    ctx.document_id = material_id_de_documento(e.documento)
    return TipoDeResultadoEtapa.EXECUTADA, None, f"documento recebido; document_id={ctx.document_id} [P19 §10]"


def _etapa_5_confirmacao_da_versao(ctx: ContextoExecucaoP13, e: EntradaEtapaP13):
    if not e.document_version:
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.ENTRADA_NAO_FORNECIDA, "document_version não fornecida"
    ctx.document_version = e.document_version
    return TipoDeResultadoEtapa.EXECUTADA, None, (
        f"document_version={ctx.document_version} registrada; detecção de \"versão concorrente\" "
        "[PRECONDICOES, GATE_DE_VERSAO] não tem critério de fonte — não verificada aqui"
    )


def _etapa_6_cartografia_global(ctx: ContextoExecucaoP13, _e: EntradaEtapaP13):
    d = ctx.documento
    ctx.cartografia = {
        "secoes": len(d.secoes),
        "paragrafos": len(d.paragrafos),
        "citacoes_recuadas": len(d.citacoes_recuadas),
        "citacoes_no_corpo": len(d.citacoes_no_corpo),
        "notas_de_rodape": len(d.notas_de_rodape),
        "figuras": len(d.figuras),
        "referencias": len(d.referencias),
        "num_paginas": d.num_paginas,
    }
    return TipoDeResultadoEtapa.EXECUTADA, None, f"cartografia agregada de DocumentoIngerido: {ctx.cartografia}"


def _etapa_7_identificacao_das_unidades(ctx: ContextoExecucaoP13, _e: EntradaEtapaP13):
    ctx.unidades_conhecidas = _unidades_do_documento(ctx.documento)
    return TipoDeResultadoEtapa.EXECUTADA, None, (
        f"{len(ctx.unidades_conhecidas)} unidade(s) identificada(s) — base de BL-022 "
        "para as etapas 8, 9 e 16-18"
    )


def _etapa_8_matriz_de_criticidade(ctx: ContextoExecucaoP13, e: EntradaEtapaP13):
    matrizes = e.matrizes_criticidade
    if matrizes is None:
        if e.cliente is not None and e.unidades_para_matriz_criticidade:
            try:
                matrizes = ponte.gerar_matrizes_criticidade(
                    documento=ctx.documento,
                    unit_ids=e.unidades_para_matriz_criticidade,
                    cliente=e.cliente,
                    sequence_id=ctx.document_id,
                )
            except ErroDeCliente as erro:
                return TipoDeResultadoEtapa.PARADA, CausaDeParada.FALHA_NA_CHAMADA_AO_MODELO, (
                    _justificativa_falha_cliente(erro)
                )
            except ponte.ErroDePonteModeloP13 as erro:
                return TipoDeResultadoEtapa.PARADA, CausaDeParada.RESPOSTA_DO_MODELO_MAL_FORMADA, (
                    _justificativa_falha_ponte(erro)
                )
        else:
            return TipoDeResultadoEtapa.PARADA, CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO, (
                "classe de criticidade é sempre declarada por quem avalia — \"a matriz não pode ser "
                "reduzida a contagem mecânica\" [§11]; este orquestrador não calcula nem infere valor "
                "sem `cliente` e `unidades_para_matriz_criticidade` [escolio/funcoes/ponte_modelo_p13.py]"
            )
    for m in matrizes:
        _exige_unit_id_conhecido(m.unit_id, ctx.unidades_conhecidas, "MatrizCriticidade")
    ctx.matrizes_criticidade = list(matrizes)
    return TipoDeResultadoEtapa.EXECUTADA, None, f"{len(ctx.matrizes_criticidade)} MatrizCriticidade aceita(s) [§11]"


def _etapa_9_matriz_de_seletividade(ctx: ContextoExecucaoP13, e: EntradaEtapaP13):
    matrizes = e.matrizes_seletividade
    if matrizes is None:
        if e.cliente is not None and ctx.matrizes_criticidade:
            try:
                matrizes = ponte.gerar_matrizes_seletividade(
                    documento=ctx.documento,
                    matrizes_criticidade=ctx.matrizes_criticidade,
                    cliente=e.cliente,
                    sequence_id=ctx.document_id,
                )
            except ErroDeCliente as erro:
                return TipoDeResultadoEtapa.PARADA, CausaDeParada.FALHA_NA_CHAMADA_AO_MODELO, (
                    _justificativa_falha_cliente(erro)
                )
            except ponte.ErroDePonteModeloP13 as erro:
                return TipoDeResultadoEtapa.PARADA, CausaDeParada.RESPOSTA_DO_MODELO_MAL_FORMADA, (
                    _justificativa_falha_ponte(erro)
                )
        else:
            return TipoDeResultadoEtapa.PARADA, CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO, (
                "os dez fatores de seletividade [§12] são julgamento sobre o candidato; não calculados "
                "aqui sem `cliente` e `MatrizCriticidade` já aceitas na etapa 8 "
                "[escolio/funcoes/ponte_modelo_p13.py]"
            )
    for m in matrizes:
        _exige_unit_id_conhecido(m.unit_id, ctx.unidades_conhecidas, "MatrizSeletividade")
    try:
        exige_referencia_valida_a_criticidade(matrizes, ctx.matrizes_criticidade)
    except ErroDeComentario as erro:
        raise ErroDeExecucaoP13("BL-024", str(erro)) from erro
    ctx.matrizes_seletividade = list(matrizes)
    return TipoDeResultadoEtapa.EXECUTADA, None, f"{len(ctx.matrizes_seletividade)} MatrizSeletividade aceita(s) [§12, BL-024]"


def _etapa_10_selecao_de_unidades_comentaveis(ctx: ContextoExecucaoP13, _e: EntradaEtapaP13):
    ctx.selecionados = aplicar_selecao(ctx.matrizes_seletividade)
    return TipoDeResultadoEtapa.EXECUTADA, None, (
        f"{len(ctx.selecionados)} candidato(s) ordenado(s) por criticidade, sem quota [§34.3-34.4]"
    )


def _avancar_bvaa_ou_levanta(
    ctx: ContextoExecucaoP13, unit_id: str, aplicar, evidencia, origem: str
) -> None:
    """Helper comum às duas evidências do BVAA (identificação e acesso) —
    valida `unit_id`, aplica via `aplicar(estado_atual, evidencia)` e
    propaga `ErroDeTransicaoBibliografica` como `ErroDeExecucaoP13`, nunca
    engolida. Evita repetir os mesmos cinco passos duas vezes dentro de
    `_etapa_11_verificacao_de_fontes`."""
    _exige_referencia_conhecida(unit_id, ctx.documento, origem)
    estado_atual = ctx.estados_bibliograficos.get(unit_id, EstadoBibliografico.OBRA_NAO_IDENTIFICADA)
    try:
        resultado = aplicar(estado_atual, evidencia)
    except ErroDeTransicaoBibliografica as erro:
        raise ErroDeExecucaoP13(
            "P13-§26",
            "evidência não licencia transição a partir do estado bibliográfico atual da fonte "
            "[BVAA/P04]",
            detalhe=f"{origem}: unit_id={unit_id!r}: {erro}",
        ) from erro
    ctx.estados_bibliograficos[unit_id] = resultado.estado_novo


def _etapa_11_verificacao_de_fontes(ctx: ContextoExecucaoP13, e: EntradaEtapaP13):
    """Único ramo de 11-15 ligado ao BVAA [P13 §26]. Encadeia, na mesma
    chamada, identificação/localização (T01-T03, `escolha técnica delegada
    ao ENGENHEIRO_LLM` — `INSTRUCOES_COMPLEMENTARES_IMPLEMENTACAO_
    ECOSSISTEMA_REVISAO_LLM_R01.md §3`) e acesso (T04/T05, já existente) —
    identificação é aplicada primeiro, para que uma fonte que chega em
    `OBRA_NAO_IDENTIFICADA` possa, na mesma chamada, alcançar `ACESSADA`
    quando o chamador fornecer as duas evidências para o mesmo `unit_id`.
    "Verificação de evidências" (etapa 12) e as demais (13-15) têm
    handlers próprios agora, não tocados aqui.

    Sessão de 2026-08-13 (curador automático, decisão do professor): se
    nenhuma evidência pronta veio e `e.servico_drive` foi fornecido, a
    etapa tenta produzir a evidência sozinha via `escolio.funcoes.
    curador_bvaa.curar_referencias` antes de considerar isto um ponto de
    extensão — mesma prioridade de `cliente` nas etapas 8/9/13/16-18:
    objeto pronto > mecanismo automático > parar."""
    evidencias_identificacao = dict(e.evidencias_de_identificacao or {})
    evidencias_acesso = dict(e.evidencias_de_acesso or {})
    escalonamentos: list[EscalonamentoDoCurador] = []

    tentar_curador = (
        not evidencias_identificacao
        and not evidencias_acesso
        and e.servico_drive is not None
        and ctx.documento is not None
        and ctx.documento.referencias
    )
    if tentar_curador:
        resultado_curador = curar_referencias(ctx.documento.referencias, e.servico_drive)
        evidencias_identificacao = resultado_curador.evidencias_de_identificacao
        evidencias_acesso = resultado_curador.evidencias_de_acesso
        escalonamentos = resultado_curador.escalonamentos

    if not evidencias_identificacao and not evidencias_acesso:
        if escalonamentos:
            ctx.escalonamentos_bibliograficos.extend(escalonamentos)
            detalhes = "; ".join(
                f"{esc.unit_id} [{esc.motivo.value}]: {esc.detalhe}" for esc in escalonamentos
            )
            return TipoDeResultadoEtapa.PARADA, CausaDeParada.ESCALONAMENTO_BIBLIOGRAFICO_NECESSARIO, (
                f"curador automático tentou {len(escalonamentos)} referência(s) e nenhuma avançou "
                f"no BVAA sem decisão humana: {detalhes}"
            )
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO, (
            "verificação de fontes exige evidência real de identificação (T01-T03) ou de acesso "
            "(T04/T05) — sem nenhuma das duas, nenhuma fonte avança no BVAA; leitura de conteúdo "
            "(T06+) continua fora do escopo desta etapa em qualquer caso"
        )
    for unit_id, evidencia in evidencias_identificacao.items():
        _avancar_bvaa_ou_levanta(ctx, unit_id, avancar_por_identificacao, evidencia, "verificação de fontes (identificação)")
    for unit_id, evidencia in evidencias_acesso.items():
        _avancar_bvaa_ou_levanta(ctx, unit_id, avancar_por_evidencia, evidencia, "verificação de fontes (acesso)")
    if escalonamentos:
        ctx.escalonamentos_bibliograficos.extend(escalonamentos)
    justificativa = (
        f"{len(evidencias_identificacao)} identificação(ões) [T01-T03] + {len(evidencias_acesso)} "
        "acesso(s) [T04/T05] aplicados no BVAA por evidência real"
    )
    if escalonamentos:
        justificativa += (
            f"; {len(escalonamentos)} referência(s) travada(s) e registrada(s) em "
            "ctx.escalonamentos_bibliograficos, não bloqueando as demais"
        )
    return TipoDeResultadoEtapa.EXECUTADA, None, justificativa


def _etapa_12_verificacao_de_evidencias(ctx: ContextoExecucaoP13, e: EntradaEtapaP13):
    """`RelacaoAfirmacaoEvidencia` (P05, `escolio/relacao.py`) — sessão de
    2026-08-12: aceitava só o objeto já julgado por humano. Decisão do
    professor, sessão de 2026-08-13: a etapa passa a **gerar** a relação
    (via `ponte.gerar_relacoes_afirmacao_evidencia`, `sufficiency`/
    `confidence` preliminares) quando o objeto pronto não vem — mesma
    prioridade já estabelecida nas demais etapas de modelo (objeto pronto
    > chamar modelo > parar). Julgamento humano prévio, quando existir,
    entra como `gabarito_relacoes_afirmacao_evidencia` — registrado para
    comparação de piloto, nunca lido como precondição desta etapa."""
    if e.gabarito_relacoes_afirmacao_evidencia is not None:
        ctx.relacoes_afirmacao_evidencia_gabarito = list(e.gabarito_relacoes_afirmacao_evidencia)

    relacoes = e.relacoes_afirmacao_evidencia
    if relacoes is None:
        if e.cliente is not None and e.unidades_para_relacao_afirmacao_evidencia:
            try:
                relacoes = ponte.gerar_relacoes_afirmacao_evidencia(
                    documento=ctx.documento,
                    unit_ids=e.unidades_para_relacao_afirmacao_evidencia,
                    cliente=e.cliente,
                    sequence_id=ctx.document_id,
                )
            except ErroDeCliente as erro:
                return TipoDeResultadoEtapa.PARADA, CausaDeParada.FALHA_NA_CHAMADA_AO_MODELO, (
                    _justificativa_falha_cliente(erro)
                )
            except ponte.ErroDePonteModeloP13 as erro:
                return TipoDeResultadoEtapa.PARADA, CausaDeParada.RESPOSTA_DO_MODELO_MAL_FORMADA, (
                    _justificativa_falha_ponte(erro)
                )
        else:
            return TipoDeResultadoEtapa.PARADA, CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO, (
                "verificação de evidências [P09 §12] não calculada aqui sem RelacaoAfirmacaoEvidencia "
                "já pronta ou `cliente` + `unidades_para_relacao_afirmacao_evidencia` "
                "[escolio/funcoes/ponte_modelo_p13.py::gerar_relacoes_afirmacao_evidencia]"
            )
    ctx.relacoes_afirmacao_evidencia = list(relacoes)
    justificativa = (
        f"{len(ctx.relacoes_afirmacao_evidencia)} RelacaoAfirmacaoEvidencia aceita(s) [P05, P09 §12]"
    )
    if ctx.relacoes_afirmacao_evidencia_gabarito:
        justificativa += (
            f"; {len(ctx.relacoes_afirmacao_evidencia_gabarito)} relação(ões) de gabarito "
            "registrada(s) para comparação de piloto, não usada(s) nesta execução"
        )
    return TipoDeResultadoEtapa.EXECUTADA, None, justificativa


def _etapa_13_verificacao_de_voz(ctx: ContextoExecucaoP13, e: EntradaEtapaP13):
    """Camada A (`escolio.voz.deteccao`, via `ponte.gerar_achados_
    fidelidade` quando não fornecida pronta) → Camada B
    (`escolio.voz.fidelidade.avaliar_a_partir_do_perfil`, que não altera
    `avaliar()` — `INSTRUCOES_COMPLEMENTARES_IMPLEMENTACAO_ECOSSISTEMA_
    REVISAO_LLM_R01.md §1.1`)."""
    perfil = e.perfil_de_voz
    if perfil is None:
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO, (
            "verificação de voz [P07] exige o perfil de voz do autor avaliado; sem "
            "`perfil_de_voz`, nenhuma detecção nem avaliação de fidelidade é possível"
        )
    achados_por_unidade = e.achados_fidelidade
    if achados_por_unidade is None:
        if e.cliente is not None and e.unidades_para_deteccao_fidelidade:
            achados_por_unidade = {}
            try:
                for unit_id in e.unidades_para_deteccao_fidelidade:
                    achados_por_unidade[unit_id] = ponte.gerar_achados_fidelidade(
                        documento=ctx.documento,
                        unit_id=unit_id,
                        perfil=perfil,
                        cliente=e.cliente,
                        sequence_id=ctx.document_id,
                    )
            except ErroDeCliente as erro:
                return TipoDeResultadoEtapa.PARADA, CausaDeParada.FALHA_NA_CHAMADA_AO_MODELO, (
                    _justificativa_falha_cliente(erro)
                )
            except ponte.ErroDePonteModeloP13 as erro:
                return TipoDeResultadoEtapa.PARADA, CausaDeParada.RESPOSTA_DO_MODELO_MAL_FORMADA, (
                    _justificativa_falha_ponte(erro)
                )
        else:
            return TipoDeResultadoEtapa.PARADA, CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO, (
                "detecção de fidelidade [Camada A, §1.2] não calculada aqui sem `achados_"
                "fidelidade` já produzidos ou `cliente` + `unidades_para_deteccao_fidelidade` "
                "[escolio/funcoes/ponte_modelo_p13.py::gerar_achados_fidelidade]"
            )
    for unit_id, achados in achados_por_unidade.items():
        _exige_unit_id_conhecido(unit_id, ctx.unidades_conhecidas, "verificação de voz")
        ctx.avaliacoes_fidelidade[unit_id] = avaliar_a_partir_do_perfil(
            perfil,
            achados,
            amostras_conflitantes=e.amostras_conflitantes,
            exigencia_institucional_em_conflito=e.exigencia_institucional_em_conflito,
        )
    return TipoDeResultadoEtapa.EXECUTADA, None, (
        f"{len(achados_por_unidade)} unidade(s) avaliada(s) para fidelidade de voz [P07]"
    )


def _etapa_14_verificacao_de_privacidade(ctx: ContextoExecucaoP13, _e: EntradaEtapaP13):
    """Sempre `EXECUTADA` — nunca ponto de extensão, nunca gate. `CO-012`
    resolvido [`INSTRUCOES_COMPLEMENTARES_IMPLEMENTACAO_ECOSSISTEMA_
    REVISAO_LLM_R01.md §2.2`]: "NÃO IMPLEMENTAR filtro ou gate obrigatório
    de privacidade sobre cada trecho ou comentário do fluxo normal de
    revisão". A salvaguarda residual (`escolio.funcoes.
    salvaguarda_privacidade_p13`) é determinística — não exige `cliente`
    nem entrada humana para rodar, e nunca aciona por tema [§2.1, §2.6]."""
    alertas: list[AlertaDePrivacidade] = []
    for candidato in ctx.selecionados:
        texto = ctx.documento.texto_da_unidade(candidato.unit_id)
        alertas.extend(detectar_exposicao_manifesta(candidato.unit_id, texto))
    ctx.alertas_privacidade = alertas
    return TipoDeResultadoEtapa.EXECUTADA, None, (
        f"{len(alertas)} alerta(s) residual(is) de privacidade sobre {len(ctx.selecionados)} "
        "candidato(s) selecionado(s) — salvaguarda não bloqueante [CO-012, §2]"
    )


def _etapa_15_identificacao_de_problemas_sistemicos(ctx: ContextoExecucaoP13, e: EntradaEtapaP13):
    """"Lista de problemas sistêmicos conhecidos" [P13 §6.3, entrada
    opcional do professor] — o professor identifica, o sistema registra;
    nenhuma descoberta autônoma de problema sistêmico é tentada aqui
    (sem fonte que descreva esse mecanismo — mesma disciplina de não
    inferir o que a fonte não dá)."""
    if e.problemas_sistemicos_conhecidos is None:
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.ENTRADA_NAO_FORNECIDA, (
            "lista de problemas sistêmicos conhecidos [§6.3] não fornecida nesta chamada — "
            "repetir com `problemas_sistemicos_conhecidos` preenchido (mesmo `[]`, para "
            "confirmar 'nenhum conhecido') resolve"
        )
    ctx.problemas_sistemicos_conhecidos = list(e.problemas_sistemicos_conhecidos)
    return TipoDeResultadoEtapa.EXECUTADA, None, (
        f"{len(ctx.problemas_sistemicos_conhecidos)} problema(s) sistêmico(s) conhecido(s) "
        "registrado(s) [§6.3]"
    )


def _etapa_elaboracao(
    campo: str,
    comment_type_esperado: str | None,
    destino: str,
    *,
    campo_candidatos: str | None = None,
    campo_matrix_map: str | None = None,
):
    def handler(ctx: ContextoExecucaoP13, e: EntradaEtapaP13):
        comentarios = getattr(e, campo)
        if comentarios is None and campo_candidatos is not None:
            candidatos = getattr(e, campo_candidatos)
            if e.cliente is not None and candidatos:
                mapa = getattr(e, campo_matrix_map) if campo_matrix_map else None
                try:
                    comentarios = ponte.gerar_comentarios(
                        documento=ctx.documento,
                        document_id=ctx.document_id,
                        document_version=ctx.document_version,
                        module_id="P13",
                        candidatos=candidatos,
                        cliente=e.cliente,
                        comment_type_esperado=comment_type_esperado,
                        matrix_comment_id_por_candidato=mapa,
                        sequence_id=ctx.document_id,
                    )
                except ErroDeCliente as erro:
                    return TipoDeResultadoEtapa.PARADA, CausaDeParada.FALHA_NA_CHAMADA_AO_MODELO, (
                        _justificativa_falha_cliente(erro)
                    )
                except ponte.ErroDePonteModeloP13 as erro:
                    return TipoDeResultadoEtapa.PARADA, CausaDeParada.RESPOSTA_DO_MODELO_MAL_FORMADA, (
                        _justificativa_falha_ponte(erro)
                    )
        if comentarios is None:
            return TipoDeResultadoEtapa.PARADA, CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO, (
                f"{destino} é redação — juízo humano ou de modelo, não preenchido nesta sessão "
                f"sem `cliente` e candidatos selecionados [escolio/funcoes/ponte_modelo_p13.py]"
            )
        for c in comentarios:
            if comment_type_esperado is not None and c.comment_type != comment_type_esperado:
                raise ErroDeExecucaoP13(
                    "P13-§13",
                    f"comentário fornecido para '{destino}' tem comment_type incompatível",
                    detalhe=f"comment_id={c.comment_id} comment_type={c.comment_type}",
                )
            _exige_document_id_canonico(c.document_id, ctx.document_id, destino)
            _exige_unit_id_conhecido(c.unit_id, ctx.unidades_conhecidas, destino)
            try:
                ctx.registro_comentarios.registrar(c)
            except ErroDeComentario as erro:
                raise ErroDeExecucaoP13("P13-§31.5", str(erro)) from erro
            ctx.todos_comentarios.append(c)
        return TipoDeResultadoEtapa.EXECUTADA, None, f"{len(comentarios)} comentário(s) registrado(s) — {destino}"
    return handler


def _etapa_verificacao_sem_correspondencia(nome_curto: str):
    def handler(_ctx, _e):
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.SEM_FONTE_DE_VERIFICACAO, (
            f"nenhuma seção do contrato liga a etapa '{nome_curto}' a um critério verificável "
            "distinto do checklist de §44, que só corresponde nominalmente à etapa 25 "
            "[LAC-FUNC-007, mesma disciplina]"
        )
    return handler


def _etapa_25_auditoria_final(ctx: ContextoExecucaoP13, _e: EntradaEtapaP13):
    lote = LoteDeAuditoria(
        comentarios=list(ctx.todos_comentarios),
        matrizes_criticidade=list(ctx.matrizes_criticidade),
        matrizes_seletividade=list(ctx.matrizes_seletividade),
        quota_declarada=False,
    )
    ctx.relatorio_auditoria = auditar_lote(lote, lote_id=ctx.document_id or "SEM-DOCUMENT-ID")
    return TipoDeResultadoEtapa.EXECUTADA, None, (
        f"auditoria final [§44] executada — veredicto={ctx.relatorio_auditoria.veredicto_final.value}"
    )


def _etapa_fora_do_fluxo(nome_curto: str):
    def handler(_ctx, _e):
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.FORA_DO_FLUXO_DE_EXECUCAO, (
            f"'{nome_curto}' é ato humano ou pós-homologação — o sistema nunca homologa "
            "[CLAUDE.md §1-§2]; este orquestrador nunca executa etapas 26-29"
        )
    return handler


_HANDLERS = {
    1: _etapa_1_intake,
    2: _etapa_2_confirmacao_de_autoridade,
    3: _etapa_3_verificacao_das_dependencias,
    4: _etapa_4_ingestao_controlada,
    5: _etapa_5_confirmacao_da_versao,
    6: _etapa_6_cartografia_global,
    7: _etapa_7_identificacao_das_unidades,
    8: _etapa_8_matriz_de_criticidade,
    9: _etapa_9_matriz_de_seletividade,
    10: _etapa_10_selecao_de_unidades_comentaveis,
    11: _etapa_11_verificacao_de_fontes,
    12: _etapa_12_verificacao_de_evidencias,
    13: _etapa_13_verificacao_de_voz,
    14: _etapa_14_verificacao_de_privacidade,
    15: _etapa_15_identificacao_de_problemas_sistemicos,
    16: _etapa_elaboracao(
        "comentarios_matriz",
        COMMENT_TYPE_COMENTARIO_MATRIZ,
        "comentários-matriz",
        campo_candidatos="candidatos_para_comentario_matriz",
    ),
    17: _etapa_elaboracao(
        "comentarios_individuais",
        None,
        "comentários individuais",
        campo_candidatos="candidatos_para_comentarios_individuais",
    ),
    18: _etapa_elaboracao(
        "remissoes",
        COMMENT_TYPE_REMISSAO_A_COMENTARIO_MATRIZ,
        "remissões",
        campo_candidatos="candidatos_para_remissoes",
        campo_matrix_map="matrix_comment_id_por_remissao",
    ),
    19: _etapa_verificacao_sem_correspondencia("verificação de densidade"),
    20: _etapa_verificacao_sem_correspondencia("verificação de repetição"),
    21: _etapa_verificacao_sem_correspondencia("verificação de acionabilidade"),
    22: _etapa_verificacao_sem_correspondencia("verificação de tom"),
    23: _etapa_verificacao_sem_correspondencia("verificação de gates"),
    24: _etapa_verificacao_sem_correspondencia("consolidação"),
    25: _etapa_25_auditoria_final,
    26: _etapa_fora_do_fluxo("decisão autoral"),
    27: _etapa_fora_do_fluxo("homologação documental"),
    28: _etapa_fora_do_fluxo("piloto Word real posterior"),
    29: _etapa_fora_do_fluxo("ativação operacional posterior"),
}

assert set(_HANDLERS) == {e.ordem for e in DECLARACAO_P13.fluxo}, (
    "todo handler deve corresponder a uma etapa declarada em p13.py, e vice-versa"
)


def avancar(estado: EstadoDeExecucaoP13, entrada: EntradaEtapaP13 | None = None) -> EstadoDeExecucaoP13:
    """Executa **no máximo uma** etapa — a próxima permitida, nunca uma
    escolhida por quem chama [POL-012; `DeclaracaoDeFuncao.proxima_etapa`].

    Muta e devolve `estado`. Quando o fluxo já terminou
    (`estado.encerrado`), levanta — chamar de novo depois do fim não é
    "mais uma etapa automática", é erro de uso."""
    entrada = entrada if entrada is not None else EntradaEtapaP13()
    proxima = DECLARACAO_P13.proxima_etapa(estado.concluidas)
    if proxima is None:
        raise ErroDeExecucaoP13("POL-012", "fluxo já concluído — nenhuma etapa restante")
    tipo, causa, justificativa = _HANDLERS[proxima.ordem](estado.contexto, entrada)
    estado.historico.append(
        ResultadoDeEtapa(etapa=proxima, tipo=tipo, causa=causa, justificativa=justificativa)
    )
    return estado

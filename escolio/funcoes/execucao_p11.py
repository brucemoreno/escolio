"""Orquestrador de execução do P11 — primeira fatia real (etapas 1-6).

## Forma, mesma disciplina de `execucao_p13.py`

Um módulo de execução por função — "nenhum executor genérico: outra função
(P10, P11...) exigiria seu próprio módulo, com sua própria tabela de
etapas" [CLAUDE.md §4]. Este é o de P11; não generaliza nem reaproveita
`execucao_p13.py` além do padrão estrutural (mesmas seis `CausaDeParada`,
mesma forma de `avancar()` de no-máximo-uma-etapa — POL-012).

## Por que só as etapas 1-6 executam nesta sessão

O piloto real desta sessão pede o pedaço mínimo que "do global para o
local" [P11 §2, invariante 2] exige antes de qualquer diagnóstico local
fazer sentido: intake, autoridade, dependências, ingestão, cartografia
global e a primeira etapa de E4 (diagnóstico de estabilidade) — a etapa
que decide se a obra está estável o bastante para prosseguir a diagnóstico
estrutural/argumentativo/historiográfico. As etapas 7-22 (os três
diagnósticos restantes, mapa de afirmações-evidências, plano modular,
decisão humana, revisão modular e local, controle de voz/BVAA/
afirmação-evidência, consolidação, verificação e auditoria) exigem cada
uma seu próprio prompt e schema — não preenchidas por conveniência nem
por analogia com P13, cujo objeto de saída (comentários Word) não serve
para os produtos de P11 (cartografia, diagnóstico, plano modular, unidades
revistas). As etapas 23-25 (decisão autoral, homologação documental,
piloto real posterior) são atos humanos ou pós-homologação — o sistema
nunca homologa [CLAUDE.md §1-§2] e este orquestrador nunca tenta
executá-las, incondicionalmente, mesma disciplina de
`_etapa_fora_do_fluxo` em `execucao_p13.py`.

## Etapa 5 funde cartografia e identificação de unidades

P11 não tem uma etapa nomeada equivalente à "identificação das unidades"
do P13 (etapa 7 de lá) — a cartografia global de P11 (etapa 5) é a única
etapa nomeada de E3. Por isso, `_etapa_5_cartografia_global` calcula, no
mesmo passo, a agregação estrutural (seções, parágrafos, citações, notas,
figuras, referências, páginas) e o conjunto `unidades_conhecidas` — a
mesma base que BL-022 usa em P13 para conferir `unit_id` de objetos
aceitos em etapas posteriores. `[PROPOSTA]`: nenhuma fonte diz que
cartografia global e identificação de unidades são o mesmo ato; fundir os
dois aqui é leitura de engenharia, registrada como tal, não fato do
contrato.

## Etapa 2 inclui nível de intervenção autorizado

Diferente do padrão de `execucao_p13.py`, esta etapa também exige
`nivel_intervencao_autorizado` — um dos 20 itens de `ENTRADAS_MINIMAS`
[P11 §6.1] e uma das 15 `PRECONDICOES` [P11 §7]. Sem ele, nenhuma etapa
posterior poderia verificar "nível aplicado nunca pode superar o nível
autorizado" [P11 §21, `DECLARACAO.limites`]. Etapas 1-6 desta sessão nunca
aplicam nível algum (o teto alcançado é `DIAGNOSTICO`, INT-02) — o campo é
coletado aqui porque a fonte o exige antes de outras verificações, não
porque esta sessão o consome.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from escolio.adaptadores.ingestao_para_input_item import material_id_de_documento
from escolio.contrato.afirmacao import ClaimEvidence
from escolio.funcoes import ponte_modelo_p11 as ponte
from escolio.funcoes.declaracao import Etapa
from escolio.funcoes.p11 import DECLARACAO as DECLARACAO_P11
from escolio.funcoes.roteador import AdmissaoDeMaterial, DecisaoDeRoteamento
from escolio.funcoes.vocabulario import FuncaoId
from escolio.ingestao.modelos import DocumentoIngerido
from escolio.intervencao.niveis import NivelIntervencao

ARQUIVO_FONTE = "P11_CONTRATO_FUNCIONAL_REVISAO_TESE_DISSERTACAO_HOMOLOGADO_R01.md"


class ErroDeExecucaoP11(Exception):
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
    """Mesmas seis causas de `execucao_p13.py` — reaproveitadas, não
    reinventadas, porque descrevem a mesma disciplina de "não implementado
    genérico" que vale para qualquer módulo de função."""

    MATERIAL_NAO_DECLARADO = "MATERIAL_NAO_DECLARADO"
    """Etapa 1. `AdmissaoDeMaterial` do material não é DECLARADO para F02 —
    ato humano de classificação ainda não ocorreu [BL-014]. Resolve com
    `roteador.abstencao_por_fora_de_escopo`, não com este módulo."""

    PRECONDICAO_NAO_SATISFEITA = "PRECONDICAO_NAO_SATISFEITA"
    """Um fato já determinado pela própria `Request` é negativo — não há
    entrada adicional que o chamador possa fornecer nesta execução para
    reverter isso; exige nova `Request`."""

    ENTRADA_NAO_FORNECIDA = "ENTRADA_NAO_FORNECIDA"
    """A etapa tem schema de aceitação (`EntradaEtapaP11`) e código para
    processá-lo, mas o campo correspondente não veio preenchido nesta
    chamada. Repetir a chamada com o campo preenchido é o caminho normal."""

    PONTO_DE_EXTENSAO_DE_MODELO = "PONTO_DE_EXTENSAO_DE_MODELO"
    """A etapa exige juízo humano ou de modelo sobre o conteúdo do
    documento para o qual nenhuma sessão anterior definiu um objeto de
    entrada aceitável por este orquestrador — diferente de
    `ENTRADA_NAO_FORNECIDA`, não há campo para preencher numa repetição
    desta chamada; fechar isto é trabalho de sessão futura, não desta."""

    SEM_FONTE_DE_VERIFICACAO = "SEM_FONTE_DE_VERIFICACAO"
    """Nenhuma seção do contrato liga esta etapa nomeada a um critério
    verificável."""

    FORA_DO_FLUXO_DE_EXECUCAO = "FORA_DO_FLUXO_DE_EXECUCAO"
    """Etapas 23-25 — `Etapa.fase is None`: decisão autoral, homologação
    documental, piloto real posterior. Atos humanos ou pós-homologação; o
    sistema nunca homologa [CLAUDE.md §1-§2] e este orquestrador nunca
    tenta executá-los, incondicionalmente."""


@dataclass(frozen=True)
class ResultadoDeEtapa:
    etapa: Etapa
    tipo: TipoDeResultadoEtapa
    justificativa: str
    causa: CausaDeParada | None = None

    def __post_init__(self) -> None:
        if self.tipo is TipoDeResultadoEtapa.PARADA and self.causa is None:
            raise ErroDeExecucaoP11(
                "EXECUCAO-INTERNA", "ResultadoDeEtapa com tipo=PARADA exige causa"
            )


@dataclass
class EntradaEtapaP11:
    """Schema de aceitação por etapa. Todo campo é opcional: sua ausência
    produz `ENTRADA_NAO_FORNECIDA` na etapa correspondente, nunca um valor
    inferido.

    `cliente` e `diagnostico_estabilidade` são desta sessão (ligação ao
    modelo, etapa 6 [`escolio/funcoes/ponte_modelo_p11.py`]). Fornecer o
    objeto já construído (`diagnostico_estabilidade`) continua tendo
    prioridade sobre chamar o modelo — a etapa só chama a API quando o
    objeto final não veio e `cliente` veio."""

    dependencias_obrigatorias_confirmadas: bool = False
    nivel_intervencao_autorizado: NivelIntervencao | None = None
    documento: DocumentoIngerido | None = None
    diagnostico_estabilidade: list[ClaimEvidence] | None = None
    cliente: object | None = None


@dataclass
class ContextoExecucaoP11:
    """Acumulado entre chamadas de `avancar()` — um `EstadoDeExecucaoP11`
    por percurso de uma obra sob F02/P11."""

    request: object
    decisao_de_roteamento: DecisaoDeRoteamento
    nivel_intervencao_autorizado: NivelIntervencao | None = None
    documento: DocumentoIngerido | None = None
    document_id: str | None = None
    cartografia: dict | None = None
    unidades_conhecidas: frozenset[str] = frozenset()
    diagnostico_estabilidade: list[ClaimEvidence] = field(default_factory=list)


@dataclass
class EstadoDeExecucaoP11:
    contexto: ContextoExecucaoP11
    historico: list[ResultadoDeEtapa] = field(default_factory=list)

    @property
    def concluidas(self) -> int:
        """Só etapas EXECUTADA avançam o ponteiro de fluxo — uma tentativa
        que parou não conta como concluída, e por isso a mesma etapa é
        reoferecida na próxima chamada [POL-012]."""
        n = 0
        for r in self.historico:
            if r.tipo is not TipoDeResultadoEtapa.EXECUTADA:
                break
            n += 1
        return n

    @property
    def encerrado(self) -> bool:
        return DECLARACAO_P11.proxima_etapa(self.concluidas) is None


def construir_estado_inicial(request, decisao_de_roteamento: DecisaoDeRoteamento) -> EstadoDeExecucaoP11:
    """Ponto de entrada. Exige uma `DecisaoDeRoteamento` já produzida por
    `escolio.funcoes.roteador.rotear` — este módulo não roteia de novo, só
    consome o resultado [CLAUDE.md §4]."""
    if decisao_de_roteamento.funcao is not FuncaoId.F02:
        raise ErroDeExecucaoP11(
            "EXECUCAO-P11",
            "execucao_p11 só processa decisões de roteamento para F02/P11",
            detalhe=f"funcao={decisao_de_roteamento.funcao}",
        )
    return EstadoDeExecucaoP11(
        contexto=ContextoExecucaoP11(request=request, decisao_de_roteamento=decisao_de_roteamento)
    )


def _unidades_do_documento(documento: DocumentoIngerido) -> frozenset[str]:
    ids = []
    ids.extend(p.unit_id for p in documento.paragrafos)
    ids.extend(c.unit_id for c in documento.citacoes_recuadas)
    ids.extend(n.unit_id for n in documento.notas_de_rodape)
    ids.extend(f.unit_id for f in documento.figuras)
    return frozenset(ids)


# --- Handlers, um por etapa (ordem 1..25) -------------------------------


def _etapa_1_intake(ctx: ContextoExecucaoP11, _e: EntradaEtapaP11):
    declarados = tuple(
        m for m in ctx.decisao_de_roteamento.materiais if m.admissao is AdmissaoDeMaterial.DECLARADO
    )
    if not declarados:
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.MATERIAL_NAO_DECLARADO, (
            "nenhum material da requisição está DECLARADO para F02 "
            "[InputItem.classification.functions, BL-014] — abstenha com "
            "roteador.abstencao_por_fora_de_escopo, não prossiga aqui"
        )
    return TipoDeResultadoEtapa.EXECUTADA, None, f"{len(declarados)} material(is) declarado(s) para F02"


def _etapa_2_confirmacao_de_autoridade_e_nivel(ctx: ContextoExecucaoP11, e: EntradaEtapaP11):
    if not ctx.request.requester.authority_basis:
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.PRECONDICAO_NAO_SATISFEITA, (
            "requester.authority_basis vazio — requisição não declara base de autoridade [P09 §4]"
        )
    if e.nivel_intervencao_autorizado is None:
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.ENTRADA_NAO_FORNECIDA, (
            "nivel_intervencao_autorizado não fornecido — entrada mínima obrigatória "
            "[P11 §6.1] e pré-condição [P11 §7]"
        )
    ctx.nivel_intervencao_autorizado = e.nivel_intervencao_autorizado
    return TipoDeResultadoEtapa.EXECUTADA, None, (
        f"requester.authority_basis presente [P09 §4]; nível autorizado="
        f"{ctx.nivel_intervencao_autorizado.value} [P11 §6.1, §7]"
    )


def _etapa_3_verificacao_das_dependencias(ctx: ContextoExecucaoP11, e: EntradaEtapaP11):
    if not e.dependencias_obrigatorias_confirmadas:
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.ENTRADA_NAO_FORNECIDA, (
            "nenhum registro em código do estado de homologação de "
            f"{DECLARACAO_P11.dependencias_obrigatorias} — confirmação é ato humano "
            "[mesmo padrão de InputItem.classification.functions, BL-014]"
        )
    return TipoDeResultadoEtapa.EXECUTADA, None, "dependências obrigatórias confirmadas por autoridade competente"


def _etapa_4_ingestao_controlada(ctx: ContextoExecucaoP11, e: EntradaEtapaP11):
    if e.documento is None:
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.ENTRADA_NAO_FORNECIDA, "documento (DocumentoIngerido) não fornecido"
    ctx.documento = e.documento
    ctx.document_id = material_id_de_documento(e.documento)
    return TipoDeResultadoEtapa.EXECUTADA, None, f"documento recebido; document_id={ctx.document_id} [P19 §10]"


def _etapa_5_cartografia_global(ctx: ContextoExecucaoP11, _e: EntradaEtapaP11):
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
    ctx.unidades_conhecidas = _unidades_do_documento(d)
    return TipoDeResultadoEtapa.EXECUTADA, None, (
        f"cartografia agregada de DocumentoIngerido: {ctx.cartografia}; "
        f"{len(ctx.unidades_conhecidas)} unidade(s) identificada(s) [PROPOSTA: cartografia "
        "funde agregação estrutural e identificação de unidades, ver docstring do módulo]"
    )


def _etapa_6_diagnostico_de_estabilidade(ctx: ContextoExecucaoP11, e: EntradaEtapaP11):
    diagnostico = e.diagnostico_estabilidade
    if diagnostico is None:
        if e.cliente is not None:
            diagnostico = ponte.gerar_diagnostico_de_estabilidade(
                documento=ctx.documento,
                cliente=e.cliente,
                sequence_id=ctx.document_id,
            )
        else:
            return TipoDeResultadoEtapa.PARADA, CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO, (
                "estabilidade do projeto intelectual (objetivo, hipótese, corpus) é juízo "
                "diagnóstico sobre o conteúdo integral da obra [E4]; este orquestrador não "
                "infere sem `cliente` [escolio/funcoes/ponte_modelo_p11.py]"
            )
    for achado in diagnostico:
        for unit_id in achado.evidence_ids:
            if unit_id not in ctx.unidades_conhecidas:
                raise ErroDeExecucaoP11(
                    "BL-022",
                    "evidence_ids de ClaimEvidence não pertence às unidades identificadas na "
                    "cartografia global (etapa 5)",
                    detalhe=f"claim_id={achado.claim_id} unit_id={unit_id!r}",
                )
    ctx.diagnostico_estabilidade = list(diagnostico)
    return TipoDeResultadoEtapa.EXECUTADA, None, (
        f"{len(ctx.diagnostico_estabilidade)} achado(s) de estabilidade aceito(s) [P09 §12]"
    )


def _etapa_ponto_de_extensao(nome_curto: str):
    def handler(_ctx, _e):
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO, (
            f"'{nome_curto}' exige juízo humano ou de modelo sobre o conteúdo da obra; "
            "nenhuma sessão anterior definiu objeto de entrada que ligue esta etapa a "
            "verificação — trabalho de sessão futura"
        )
    return handler


def _etapa_sem_fonte_de_verificacao(nome_curto: str):
    def handler(_ctx, _e):
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.SEM_FONTE_DE_VERIFICACAO, (
            f"nenhuma seção do contrato liga a etapa '{nome_curto}' a um critério verificável "
            "distinto do texto geral de auditoria [LAC-FUNC-007, mesma disciplina de P13]"
        )
    return handler


def _etapa_fora_do_fluxo(nome_curto: str):
    def handler(_ctx, _e):
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.FORA_DO_FLUXO_DE_EXECUCAO, (
            f"'{nome_curto}' é ato humano ou pós-homologação — o sistema nunca homologa "
            "[CLAUDE.md §1-§2]; este orquestrador nunca executa etapas 23-25"
        )
    return handler


_HANDLERS = {
    1: _etapa_1_intake,
    2: _etapa_2_confirmacao_de_autoridade_e_nivel,
    3: _etapa_3_verificacao_das_dependencias,
    4: _etapa_4_ingestao_controlada,
    5: _etapa_5_cartografia_global,
    6: _etapa_6_diagnostico_de_estabilidade,
    7: _etapa_ponto_de_extensao("diagnóstico estrutural"),
    8: _etapa_ponto_de_extensao("diagnóstico argumentativo"),
    9: _etapa_ponto_de_extensao("diagnóstico historiográfico"),
    10: _etapa_ponto_de_extensao("mapa de afirmações e evidências"),
    11: _etapa_ponto_de_extensao("plano modular"),
    12: _etapa_ponto_de_extensao("decisão humana"),
    13: _etapa_ponto_de_extensao("revisão por módulo"),
    14: _etapa_ponto_de_extensao("revisão local rastreável"),
    15: _etapa_ponto_de_extensao("controle de voz"),
    16: _etapa_ponto_de_extensao("controle BVAA"),
    17: _etapa_ponto_de_extensao("controle afirmação-evidência"),
    18: _etapa_ponto_de_extensao("consolidação do bloco"),
    19: _etapa_sem_fonte_de_verificacao("verificação proporcional ou auditoria de bloco"),
    20: _etapa_ponto_de_extensao("avanço modular"),
    21: _etapa_sem_fonte_de_verificacao("verificação global de regressão"),
    22: _etapa_sem_fonte_de_verificacao("auditoria final"),
    23: _etapa_fora_do_fluxo("decisão autoral"),
    24: _etapa_fora_do_fluxo("homologação documental"),
    25: _etapa_fora_do_fluxo("piloto supervisionado real posterior"),
}

assert set(_HANDLERS) == {e.ordem for e in DECLARACAO_P11.fluxo}, (
    "todo handler deve corresponder a uma etapa declarada em p11.py, e vice-versa"
)


def avancar(estado: EstadoDeExecucaoP11, entrada: EntradaEtapaP11 | None = None) -> EstadoDeExecucaoP11:
    """Executa **no máximo uma** etapa — a próxima permitida, nunca uma
    escolhida por quem chama [POL-012; `DeclaracaoDeFuncao.proxima_etapa`].

    Muta e devolve `estado`. Quando o fluxo já terminou
    (`estado.encerrado`), levanta — chamar de novo depois do fim não é
    "mais uma etapa automática", é erro de uso."""
    entrada = entrada if entrada is not None else EntradaEtapaP11()
    proxima = DECLARACAO_P11.proxima_etapa(estado.concluidas)
    if proxima is None:
        raise ErroDeExecucaoP11("POL-012", "fluxo já concluído — nenhuma etapa restante")
    tipo, causa, justificativa = _HANDLERS[proxima.ordem](estado.contexto, entrada)
    estado.historico.append(
        ResultadoDeEtapa(etapa=proxima, tipo=tipo, causa=causa, justificativa=justificativa)
    )
    return estado

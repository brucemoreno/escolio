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

Sem chamada à API [instrução desta sessão]. Cada etapa que a fonte descreve
como diagnóstico, seleção de conteúdo ou redação (juízo humano ou de
modelo) permanece um ponto de extensão explícito — o orquestrador não o
preenche por conveniência nem interpola um valor plausível [CLAUDE.md §11].
Uma etapa some do caminho feliz sem se tornar aprovação silenciosa:
`ResultadoDeEtapa.tipo` distingue seis causas de parada (`CausaDeParada`),
cada uma com critério próprio — nunca uma genérica "não implementado".

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
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from escolio.adaptadores.ingestao_para_input_item import material_id_de_documento
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
from escolio.funcoes.declaracao import Etapa
from escolio.funcoes.p13 import DECLARACAO as DECLARACAO_P13
from escolio.funcoes.roteador import AdmissaoDeMaterial, DecisaoDeRoteamento
from escolio.funcoes.vocabulario import FuncaoId
from escolio.ingestao.modelos import DocumentoIngerido

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
    """Seis causas distintas de não-execução — nunca uma genérica "não
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
    documento (diagnóstico E4: fontes, evidência, voz, privacidade,
    problemas sistêmicos) para o qual nenhuma sessão anterior definiu um
    objeto de entrada aceitável por este orquestrador — diferente de
    `ENTRADA_NAO_FORNECIDA`, não há campo para preencher numa repetição
    desta chamada; fechar isto é trabalho de sessão futura, não desta."""

    SEM_FONTE_DE_VERIFICACAO = "SEM_FONTE_DE_VERIFICACAO"
    """Nenhuma seção do contrato liga esta etapa nomeada a um critério
    verificável — mesma disciplina de `NAO_VERIFICAVEL_NESTA_SESSAO` em
    `escolio/comentarios/auditoria.py`."""

    FORA_DO_FLUXO_DE_EXECUCAO = "FORA_DO_FLUXO_DE_EXECUCAO"
    """Etapas 26-29 — `Etapa.fase is None`: decisão autoral, homologação
    documental, piloto Word real, ativação operacional. Atos humanos ou
    pós-homologação; o sistema nunca homologa [CLAUDE.md §1-§2] e este
    orquestrador nunca tenta executá-los, incondicionalmente."""


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
    anterior a aceitar)."""

    dependencias_obrigatorias_confirmadas: bool = False
    documento: DocumentoIngerido | None = None
    document_version: str | None = None
    matrizes_criticidade: list[MatrizCriticidade] | None = None
    matrizes_seletividade: list[MatrizSeletividade] | None = None
    comentarios_matriz: list[P13Comment] | None = None
    comentarios_individuais: list[P13Comment] | None = None
    remissoes: list[P13Comment] | None = None


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
    if e.matrizes_criticidade is None:
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO, (
            "classe de criticidade é sempre declarada por quem avalia — \"a matriz não pode ser "
            "reduzida a contagem mecânica\" [§11]; este orquestrador não calcula nem infere valor"
        )
    for m in e.matrizes_criticidade:
        _exige_unit_id_conhecido(m.unit_id, ctx.unidades_conhecidas, "MatrizCriticidade")
    ctx.matrizes_criticidade = list(e.matrizes_criticidade)
    return TipoDeResultadoEtapa.EXECUTADA, None, f"{len(ctx.matrizes_criticidade)} MatrizCriticidade aceita(s) [§11]"


def _etapa_9_matriz_de_seletividade(ctx: ContextoExecucaoP13, e: EntradaEtapaP13):
    if e.matrizes_seletividade is None:
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO, (
            "os dez fatores de seletividade [§12] são julgamento sobre o candidato; não calculados aqui"
        )
    for m in e.matrizes_seletividade:
        _exige_unit_id_conhecido(m.unit_id, ctx.unidades_conhecidas, "MatrizSeletividade")
    try:
        exige_referencia_valida_a_criticidade(e.matrizes_seletividade, ctx.matrizes_criticidade)
    except ErroDeComentario as erro:
        raise ErroDeExecucaoP13("BL-024", str(erro)) from erro
    ctx.matrizes_seletividade = list(e.matrizes_seletividade)
    return TipoDeResultadoEtapa.EXECUTADA, None, f"{len(ctx.matrizes_seletividade)} MatrizSeletividade aceita(s) [§12, BL-024]"


def _etapa_10_selecao_de_unidades_comentaveis(ctx: ContextoExecucaoP13, _e: EntradaEtapaP13):
    ctx.selecionados = aplicar_selecao(ctx.matrizes_seletividade)
    return TipoDeResultadoEtapa.EXECUTADA, None, (
        f"{len(ctx.selecionados)} candidato(s) ordenado(s) por criticidade, sem quota [§34.3-34.4]"
    )


def _etapa_diagnostico_sem_schema(nome_curto: str):
    def handler(_ctx, _e):
        return TipoDeResultadoEtapa.PARADA, CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO, (
            f"{nome_curto} exige juízo diagnóstico (E4) sobre o conteúdo do documento; nenhuma "
            "sessão anterior definiu objeto de entrada que ligue candidato a esta verificação"
        )
    return handler


def _etapa_elaboracao(campo: str, comment_type_esperado: str | None, destino: str):
    def handler(ctx: ContextoExecucaoP13, e: EntradaEtapaP13):
        comentarios = getattr(e, campo)
        if comentarios is None:
            return TipoDeResultadoEtapa.PARADA, CausaDeParada.PONTO_DE_EXTENSAO_DE_MODELO, (
                f"{destino} é redação — juízo humano ou de modelo, não preenchido nesta sessão"
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
    11: _etapa_diagnostico_sem_schema("verificação de fontes"),
    12: _etapa_diagnostico_sem_schema("verificação de evidências"),
    13: _etapa_diagnostico_sem_schema("verificação de voz"),
    14: _etapa_diagnostico_sem_schema("verificação de privacidade"),
    15: _etapa_diagnostico_sem_schema("identificação de problemas sistêmicos"),
    16: _etapa_elaboracao("comentarios_matriz", COMMENT_TYPE_COMENTARIO_MATRIZ, "comentários-matriz"),
    17: _etapa_elaboracao("comentarios_individuais", None, "comentários individuais"),
    18: _etapa_elaboracao("remissoes", COMMENT_TYPE_REMISSAO_A_COMENTARIO_MATRIZ, "remissões"),
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

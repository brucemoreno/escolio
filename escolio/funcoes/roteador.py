"""Roteador de função — fontes: P09 §4.2, §6, §8.1, §23; P02; POL-007.

O QUE ELE FAZ: confere quatro correspondências que o P09 exige e que o
envelope sozinho não consegue verificar, porque dependem de um catálogo
externo — exatamente a lacuna que `escolio/contrato/LACUNAS.md` deixou
reservada para esta peça.

O QUE ELE NÃO FAZ: escolher a função. Não existe `selecionar_funcao`, e a
ausência é o mecanismo, não um comentário — "abstenção é ausência de
caminho de código, não frase" [CLAUDE.md §8]. POL-007, ação proibida:
"Inferir próxima fase, componente ou operação". Nenhuma fonte define como
se decide que uma função, e não outra, se aplica a um documento: o
`GATE_DE_ATIVACAO_P1x` de cada contrato ocorre uma única vez, como item nu
de lista, sem definição; o P02 cataloga sem selecionar. A escolha chega
declarada em `request.function_id` e em `InputItem.classification.functions`.
Ver LACUNAS.md, LAC-FUNC-001.

O roteador também não possui critério próprio: operações, etapas, gates e
limites são declarados por cada módulo de função, e aqui só se comparam.
Isso é o que impede que ele "funda escopos, gates, papéis, produtos ou
decisões" [P01/05]. Precedente da casa: `escolio/intervencao/gate.py`, que
aplica a regra estrutural e devolve a causa a quem invoca.
"""

from dataclasses import dataclass
from enum import Enum

from escolio.contrato.entrada import InputItem
from escolio.contrato.payloads import AbstentionPayload
from escolio.contrato.vocabulario import AbstentionCategory
from escolio.funcoes.catalogo import COMPONENTE_POR_FUNCAO, declaracao_de, funcao_de
from escolio.funcoes.declaracao import DeclaracaoDeFuncao
from escolio.funcoes.erros import ErroDeRoteamento
from escolio.funcoes.vocabulario import FuncaoId


class AdmissaoDeMaterial(str, Enum):
    """Resultado da leitura de `InputItem.classification.functions` [P09 §6]."""

    DECLARADO = "DECLARADO"
    """A função consta entre as declaradas para este material."""

    NAO_DECLARADO = "NAO_DECLARADO"
    """Há declaração, e esta função não está nela — operação fora do escopo."""

    INDETERMINADO = "INDETERMINADO"
    """`functions` vazio: nada foi declarado. Não é o mesmo que negado, e
    também não é permissão. Precedente literal do P19 §17 para
    `material_type=null`: registrar a indeterminação, manter a
    classificação pendente, não conceder elegibilidade, não criar valor
    categorial concorrente."""


@dataclass(frozen=True)
class DecisaoDeMaterial:
    input_id: str
    admissao: AdmissaoDeMaterial
    funcoes_declaradas: tuple[str, ...]


@dataclass(frozen=True)
class VerificacaoDeOperacao:
    """P09 §4.2.5 exige que `function_id` seja compatível com `operation`,
    mas nenhuma fonte enumera as operações de cada função — os contratos
    recebem `requested_operation` como string livre. Quando o módulo da
    função não declara operações, a verificação é INCONCLUSIVA, e isso
    aparece no resultado em vez de virar aprovação silenciosa
    [CLAUDE.md §11: "Indeterminado em vez de chute"]. Ver LAC-FUNC-005."""

    operation: str
    conclusiva: bool
    compativel: bool | None
    fundamento: str


@dataclass(frozen=True)
class DecisaoDeRoteamento:
    funcao: FuncaoId
    declaracao: DeclaracaoDeFuncao
    operacao: VerificacaoDeOperacao
    materiais: tuple[DecisaoDeMaterial, ...]

    @property
    def materiais_fora_de_escopo(self) -> tuple[DecisaoDeMaterial, ...]:
        return tuple(m for m in self.materiais if m.admissao is AdmissaoDeMaterial.NAO_DECLARADO)

    @property
    def materiais_indeterminados(self) -> tuple[DecisaoDeMaterial, ...]:
        return tuple(m for m in self.materiais if m.admissao is AdmissaoDeMaterial.INDETERMINADO)


def exige_funcao_conhecida(function_id: str) -> FuncaoId:
    """P09 §4.2.6. Levanta se o valor não pertencer ao catálogo fechado."""
    return funcao_de(function_id)


def exige_funcao_pertence_ao_componente(funcao_id: FuncaoId, component_id: str) -> None:
    """P09 §4.2.4: "`function_id` deve pertencer ao `component_id`";
    §4.2.7: divergência entre função, componente e operação produz
    `ERROR/VALIDATION`."""
    esperado = COMPONENTE_POR_FUNCAO[funcao_id]
    if esperado is None:
        raise ErroDeRoteamento(
            "P09-§4.2.4",
            "função transversal sem componente numerado não pode ser vinculada a um component_id",
            detalhe=(
                f"{funcao_id.value} não consta como componente no inventário canônico da R03 "
                f"(recebido component_id='{component_id}') — lacuna aberta, ver LAC-FUNC-003"
            ),
        )
    if component_id != esperado:
        raise ErroDeRoteamento(
            "P09-§4.2.7",
            "divergência entre função e componente produz ERROR/VALIDATION",
            detalhe=f"{funcao_id.value} pertence a '{esperado}', não a '{component_id}'",
        )


def verificar_operacao(funcao_id: FuncaoId, operation: str) -> VerificacaoDeOperacao:
    """P09 §4.2.5. Devolve verificação; não levanta quando inconclusiva.

    A regra do §4.2.8 — "`operation` deve constar entre as operações
    autorizadas" — é outra, incide sobre `request.scope.allowed_operations`
    e já é validada em `escolio/contrato/requisicao.py`. Aqui trata-se de
    compatibilidade entre função e operação, que exigiria um enum de
    operações por função que nenhuma fonte fornece."""
    autorizadas = declaracao_de(funcao_id).operacoes_autorizadas
    if not autorizadas:
        return VerificacaoDeOperacao(
            operation=operation,
            conclusiva=False,
            compativel=None,
            fundamento=(
                f"{funcao_id.value} não declara operações autorizadas: nenhuma fonte as "
                "enumera. Compatibilidade indeterminável [LAC-FUNC-005]."
            ),
        )
    compativel = operation in autorizadas
    return VerificacaoDeOperacao(
        operation=operation,
        conclusiva=True,
        compativel=compativel,
        fundamento=(
            f"operação {'consta' if compativel else 'não consta'} entre as declaradas por "
            f"{funcao_id.value}"
        ),
    )


def exige_operacao_compativel(funcao_id: FuncaoId, operation: str) -> None:
    """Levanta somente quando a incompatibilidade é conclusiva. Verificação
    inconclusiva não vira recusa nem aprovação — é lida em
    `verificar_operacao`."""
    v = verificar_operacao(funcao_id, operation)
    if v.conclusiva and not v.compativel:
        raise ErroDeRoteamento(
            "P09-§4.2.5", "function_id deve ser compatível com operation", detalhe=v.fundamento
        )


def exige_correspondencia_de_funcao(request, response) -> None:
    """P09 §8.1: "`response.function_id` deve corresponder à função da
    requisição".

    Esta linha não é conferida por
    `escolio.contrato.resposta.exige_correspondencia_request_response`,
    que cobre `request_id`, `project_id` e `component_id`. Nasce aqui para
    não alterar código existente; consolidar as duas é decisão registrada
    em docs/backlog.md, BL-011.

    Parâmetros sem anotação pelo mesmo motivo que em `resposta.py`: evitar
    dependência circular entre módulos de contrato."""
    if response.function_id != request.function_id:
        raise ErroDeRoteamento(
            "P09-§8.1",
            "response.function_id deve corresponder à função da requisição",
            detalhe=f"request='{request.function_id}' response='{response.function_id}'",
        )


def verificar_material(item: InputItem, funcao_id: FuncaoId) -> DecisaoDeMaterial:
    """Lê `InputItem.classification.functions` [P09 §6].

    Este é o único campo do envelope que carrega função, e ele é
    declarado, não derivado. Não existe campo de tipo de documento em
    nenhuma fonte, e o `material_type` do P19 §17 é taxonomia de
    governança de dados, não de gênero acadêmico — de modo que não há
    contra o que classificar um documento. Ver LAC-FUNC-009."""
    declaradas = tuple(item.classification.functions)
    if not declaradas:
        admissao = AdmissaoDeMaterial.INDETERMINADO
    elif funcao_id.value in declaradas:
        admissao = AdmissaoDeMaterial.DECLARADO
    else:
        admissao = AdmissaoDeMaterial.NAO_DECLARADO
    return DecisaoDeMaterial(
        input_id=item.input_id, admissao=admissao, funcoes_declaradas=declaradas
    )


def abstencao_por_fora_de_escopo(
    abstention_id: str,
    request_id: str,
    funcao_id: FuncaoId,
    materiais: tuple[DecisaoDeMaterial, ...],
) -> AbstentionPayload:
    """`ABSTAINED/OUT_OF_SCOPE` [P09 §23; P11 §34].

    Abstenção, não erro: P09 §4.2.17 — "ausência legítima de autoridade,
    sem falha formal, produz abstenção localizada". Material não declarado
    para a função não é defeito de contrato; é falta de declaração, e
    declarar é ato humano.

    A escolha de `OUT_OF_SCOPE` para este caso está registrada como
    divergência em docs/spec/divergencias.md §4.4: só o P11 §34 liga a
    categoria a uma condição; o caso análogo mais próximo, PS14-08,
    resolve em `SUCCESS` + `REFUSED` + `NAO_APLICAVEL`. Segue-se aqui a
    linha transversal do P09 §23, por ser regra do contrato de runtime, e
    não a de um contrato de função."""
    if not materiais:
        raise ErroDeRoteamento(
            "P09-§15.1",
            "abstenção deve ser localizada ao ponto inseguro ou indeterminado",
            detalhe="nenhum material informado para fundamentar a abstenção por escopo",
        )
    return AbstentionPayload(
        abstention_id=abstention_id,
        request_id=request_id,
        category=AbstentionCategory.OUT_OF_SCOPE,
        reason=(
            f"material não declarado para {funcao_id.value} em "
            "InputItem.classification.functions"
        ),
        scope=[m.input_id for m in materiais],
        triggering_conditions=[
            f"{m.input_id}: admissao={m.admissao.value}, "
            f"functions declaradas={list(m.funcoes_declaradas)}"
            for m in materiais
        ],
        unperformed_work=[f"qualquer operação de {funcao_id.value} sobre {m.input_id}" for m in materiais],
        authorization_required=[
            "declaração de InputItem.classification.functions por autoridade competente"
        ],
        reversible=True,
        resume_conditions=[
            f"classification.functions passar a incluir {funcao_id.value}, "
            "por declaração de autoridade competente"
        ],
        human_decision_required=True,
    )


def rotear(request) -> DecisaoDeRoteamento:
    """Confere a requisição contra o catálogo e devolve o que foi apurado.

    Levanta nas violações determináveis (função desconhecida, função fora
    do componente, operação conclusivamente incompatível). Não levanta
    para material fora de escopo nem para indeterminação: esses são
    resultado a ser representado no envelope de resposta, não falha de
    contrato — quem chama monta a abstenção com
    `abstencao_por_fora_de_escopo`.

    Não autoriza execução. "Gate satisfeito não constitui autorização
    universal para etapas posteriores" [P10 §29.4]; "Gate documental
    satisfeito não autoriza automaticamente intervenção substantiva"
    [P11 §28.3]. Passar por aqui é condição necessária, nunca suficiente."""
    funcao = exige_funcao_conhecida(request.function_id)
    exige_funcao_pertence_ao_componente(funcao, request.component_id)
    exige_operacao_compativel(funcao, request.operation)
    return DecisaoDeRoteamento(
        funcao=funcao,
        declaracao=declaracao_de(funcao),
        operacao=verificar_operacao(funcao, request.operation),
        materiais=tuple(verificar_material(i, funcao) for i in request.inputs),
    )

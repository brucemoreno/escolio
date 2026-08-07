"""Estrutura de declaração de uma função — fonte: R03 CAMADA B.

Os doze campos obrigatórios não são desenho nosso. R03 CAMADA B, verbatim:
"Cada função deve declarar: objetivo; entradas mínimas; pré-condições;
decisões; fluxo; gates humanos; saídas; limites; falhas proibidas; testes
de aceitação; rastreabilidade; dados necessários."

Observação que a própria lista fornece: "critério de seleção" não está
entre os doze. Selecionar não é atributo declarável de uma função — o que
confirma, por fonte independente dos cinco contratos, que a escolha da
função é ato externo a ela. Ver LACUNAS.md, LAC-FUNC-001.

A declaração é dado inerte. Não há `executar`, nem aqui nem em nenhum dos
seis módulos de função: POL-012 proíbe "executar encadeamento automático"
e exige "exatamente uma próxima ação permitida ou nenhuma automática".
`proxima_etapa` devolve o sucessor ordinal, um só, e nada avança sozinho.
"""

from dataclasses import dataclass, field

from escolio.funcoes.erros import ErroDeDeclaracao
from escolio.funcoes.vocabulario import ClasseDeGate, FaseDaEspinha, FuncaoId


@dataclass(frozen=True)
class Etapa:
    """Uma etapa nomeada do fluxo de uma função.

    `nome` é verbatim do contrato, na grafia e no idioma da fonte — não
    traduzido, não normalizado [CLAUDE.md §7].

    `fase` é anotação consultável, nunca eixo de iteração. Vale None
    quando a etapa não corresponde a nenhuma das sete fases sem forçar a
    correspondência."""

    ordem: int
    nome: str
    fase: FaseDaEspinha | None = None


@dataclass(frozen=True)
class Gate:
    """Um gate nomeado.

    `etapa` é a posição do gate na sequência de etapas. Vale None em todos
    os 91 gates nomeados dos cinco contratos: nenhum contrato liga gate a
    passo. Semelhança de nome entre um gate e uma etapa (GATE_DE_MATRIZ e
    "matriz de demandas", por exemplo) não é afirmação da fonte e não vira
    código. Ver LAC-FUNC-007."""

    nome: str
    classe: ClasseDeGate
    etapa: int | None = None


@dataclass(frozen=True)
class OrdemDeclarada:
    """Uma sequência ordenada que um contrato declara sem chamá-la de
    fluxo de etapas.

    Existe por causa do P10, que não tem análogo do "FLUXO MODULAR" dos
    outros quatro: tem quatro listas ordenadas em seções distintas, com
    objetos distintos (produtos, fases de agente, ordem de redação,
    estados internos). Fundi-las numa sequência única seria inventar um
    fluxo que a fonte não tem. Ver LAC-FUNC-004."""

    secao: str
    objeto: str
    itens: tuple[str, ...]


@dataclass(frozen=True)
class DeclaracaoDeFuncao:
    """Os doze campos da R03 CAMADA B, mais a identidade e o que o
    roteador precisa comparar.

    R03 CAMADA B fala em "gates humanos"; os contratos declaram também
    gates documentais. `gates` cobre os dois, distinguidos por
    `Gate.classe` — a R03 não os proíbe, apenas não os menciona."""

    funcao_id: FuncaoId
    component_id: str | None
    denominacao: str
    arquivo_fonte: str

    objetivo: str
    entradas_minimas: tuple[str, ...]
    precondicoes: tuple[str, ...]
    decisoes: tuple[str, ...]
    fluxo: tuple[Etapa, ...]
    gates: tuple[Gate, ...]
    saidas: tuple[str, ...]
    limites: tuple[str, ...]
    falhas_proibidas: tuple[str, ...]
    testes_de_aceitacao: tuple[str, ...]
    rastreabilidade: tuple[str, ...]
    dados_necessarios: tuple[str, ...]

    dependencias_obrigatorias: tuple[str, ...] = ()
    condicao_de_ativacao: str = ""
    ordens_declaradas: tuple[OrdemDeclarada, ...] = ()
    operacoes_autorizadas: frozenset[str] = field(default_factory=frozenset)
    encaminhamentos: tuple[str, ...] = ()

    def __post_init__(self):
        if not self.denominacao:
            raise ErroDeDeclaracao("denominacao é obrigatória")
        if not self.objetivo:
            raise ErroDeDeclaracao(
                "objetivo é obrigatório", detalhe=f"função {self.funcao_id.value}"
            )
        # R03 CAMADA B exige os doze campos declarados. Um contrato pode
        # legitimamente não fornecer conteúdo para um deles — o P10 não
        # tem fluxo numerado, o X01 não tem etapas — e nesse caso o campo
        # fica vazio COM lacuna registrada, nunca preenchido por analogia.
        self._exige_ordem_continua()
        self._exige_gates_unicos()

    def _exige_ordem_continua(self):
        esperado = list(range(1, len(self.fluxo) + 1))
        observado = [e.ordem for e in self.fluxo]
        if observado != esperado:
            raise ErroDeDeclaracao(
                "fluxo deve ser numerado de 1..N sem lacuna nem repetição",
                detalhe=f"{self.funcao_id.value}: observado {observado}",
            )

    def _exige_gates_unicos(self):
        nomes = [g.nome for g in self.gates]
        duplicados = {n for n in nomes if nomes.count(n) > 1}
        if duplicados:
            raise ErroDeDeclaracao(
                "nome de gate duplicado na declaração",
                detalhe=f"{self.funcao_id.value}: {sorted(duplicados)}",
            )

    def etapa(self, ordem: int) -> Etapa | None:
        """Etapa de índice `ordem` (1-based), ou None se não existir."""
        for e in self.fluxo:
            if e.ordem == ordem:
                return e
        return None

    def proxima_etapa(self, concluidas: int) -> Etapa | None:
        """A única próxima etapa permitida, ou None quando não há.

        POL-012, ação permitida: "Registrar exatamente uma próxima ação
        permitida ou nenhuma automática"; ação proibida: "Oferecer
        múltiplas ações simultâneas ou executar encadeamento automático".
        Devolver a etapa não a executa e não autoriza executá-la: a
        autorização é do gate correspondente, cuja posição nenhum contrato
        declara [LAC-FUNC-007]."""
        if concluidas < 0:
            raise ErroDeDeclaracao(
                "número de etapas concluídas não pode ser negativo",
                detalhe=f"{self.funcao_id.value}: {concluidas}",
            )
        return self.etapa(concluidas + 1)

    def gates_da_classe(self, classe: ClasseDeGate) -> tuple[Gate, ...]:
        return tuple(g for g in self.gates if g.classe == classe)

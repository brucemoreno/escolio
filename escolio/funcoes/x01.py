"""X01 — Gestão transversal de fontes, citações e evidências.

Fonte: 02_CATALOGO_FUNCIONAL_CONSOLIDADO_P02_R01.md, entrada
`LLM-ACA-X01`, e 03_MATRIZ_DE_REQUISITOS_LIMITES_GATES_E_SAIDAS_P02_R01.csv,
em PACOTE_CONTRATO_CIENTISTA_ACADEMICO_LLM_R01/. Também R03 CAMADA B,
item 6 da lista de funções registradas.

X01 é função, não camada de apoio [CLAUDE.md §3]: tem entradas, saídas,
limites, gates e riscos próprios no P02, e conta como a sexta unidade do
catálogo fechado. Mas é transversal — "transversal às cinco macrofunções,
mas não as substitui" [P02 §3].

DUAS AUSÊNCIAS, ambas da fonte, nenhuma preenchida aqui:

1. `fluxo` vazio. O X01 não tem contrato funcional próprio no acervo — não
   existe arquivo `X01_CONTRATO_FUNCIONAL_*`. O P02 dá finalidade,
   entradas, saídas, limites, gates e riscos; nunca etapas. Inventar um
   fluxo por analogia com P10-P14 seria exatamente a inferência proibida.
   Ver LAC-FUNC-003.

2. `component_id=None`. O inventário canônico da R03 atribui componente
   numerado a P10-P14 (camada FUNCAO), mas o X01 não aparece como
   componente — só como item 6 da CAMADA B. Não há P-número a atribuir, e
   escolher um seria criar identificador que a fonte não tem.
   Ver LAC-FUNC-003.

QUEM IMPLEMENTA: `escolio/` (schema P05, 23 campos, 20 regras RC) e
`escolio/bvaa/` (máquina P04, 17 estados, 18 transições) já são o X01 em
código [CLAUDE.md §3, §14 item 4]. Este módulo é a declaração da função no
catálogo, não uma segunda implementação — não reimplementa nada e não
importa daqueles pacotes.
"""

from escolio.funcoes.declaracao import DeclaracaoDeFuncao, Gate
from escolio.funcoes.vocabulario import ClasseDeGate, FuncaoId

ARQUIVO_FONTE = "02_CATALOGO_FUNCIONAL_CONSOLIDADO_P02_R01.md"

# O P02 declara um único gate, em prosa, no campo `gate_de_autorizacao` da
# matriz §03. Não é nomeado no padrão GATE_DE_* dos contratos P10-P14, e
# não tem classe declarada. Registrado com o nome que a fonte usa, na
# classe que mais se aproxima, e a divergência fica em LACUNAS.md.
GATES: tuple[Gate, ...] = (
    Gate(
        "Bibliografia externa e decisão diante de lacuna documental exigem autorização humana",
        ClasseDeGate.DECISAO_HUMANA_EXPRESSA,
    ),
)

DECLARACAO = DeclaracaoDeFuncao(
    funcao_id=FuncaoId.X01,
    component_id=None,
    denominacao="Gestão transversal de fontes, citações e evidências",
    arquivo_fonte=ARQUIVO_FONTE,
    objetivo=(
        "Calibrar necessidade, tipo, frequência, localização, inserção e verificação de "
        "fontes em todas as funções [P02, LLM-ACA-X01]."
    ),
    entradas_minimas=(
        "texto",
        "afirmações",
        "fontes",
        "bibliografia",
        "norma de citação",
        "contexto disciplinar",
    ),
    precondicoes=(
        "fontes materialmente disponíveis [P02, dependências de X01]",
        "P00; P01 [P02, dependências de X01]",
    ),
    decisoes=(
        "recomendar ou abster-se diante de lacuna documental [P02, saídas e gates]",
        "decisão diante de lacuna documental exige autorização humana [P02, gate]",
    ),
    saidas=(
        "mapa de evidências",
        "recomendações",
        "citações verificadas",
        "pendências",
        "alertas de insuficiência e ambiguidade",
    ),
    fluxo=(),
    gates=GATES,
    limites=(
        "não usar quota fixa [P02]",
        "não inserir citação ornamental [P02]",
        "não inventar página [P02]",
        "não tratar fonte primária como prova transparente [P02]",
        "transversal às cinco macrofunções, mas não as substitui [P02 §3]",
        "somente a função descrita; não escolher arquitetura, tecnologia ou política "
        "pertencente a P03-P28 [P02, matriz §03, limite_de_escopo]",
    ),
    falhas_proibidas=(
        "alucinação bibliográfica [P02, riscos]",
        "citação ambígua [P02, riscos]",
        "excesso mecânico [P02, riscos]",
        "insuficiência evidencial [P02, riscos]",
    ),
    testes_de_aceitacao=(
        "T-016 a T-020 — cinco testes de aceitação aplicáveis [P02, proveniência de X01]",
    ),
    rastreabilidade=(
        "implementado por escolio/ (schema P05) e escolio/bvaa/ (máquina P04)",
        "estado no P02: FUNCAO_TRANSVERSAL_COMPROVADA_NAO_HOMOLOGADA",
        "lacuna preservada pela fonte: forma técnica de registro e armazenamento "
        "pertence a componentes técnicos posteriores [P02]",
    ),
    dados_necessarios=("fontes materialmente disponíveis [P02]",),
    dependencias_obrigatorias=("P00", "P01"),
    condicao_de_ativacao="",
    encaminhamentos=(),
)

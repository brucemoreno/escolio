"""Modelos de dados da estrutura canônica de ingestão.

Dataclasses, mesmo padrão de escolio/relacao.py. Diferença deliberada: o
schema de saída aqui não é definitivo (contrato virá do P09 — ver
escolio/ingestao/FORMATO.md); por isso os modelos não validam campos
obrigatórios em __post_init__ como RelacaoAfirmacaoEvidencia faz — a
única invariante estrutural imposta é que toda unidade seja rastreável
até a(s) página(s) de origem, exigido pelo prompt.

Correção de design (feedback do usuário): "rastreável até a página" não
significa "cada unidade pertence a uma única página" — significa que a
página é sempre determinável a partir da unidade. Uma unidade lógica
que atravessa uma quebra de página (parágrafo, citação recuada ou nota
de rodapé cujo texto começa numa página e termina na seguinte — rotina,
não exceção, num documento longo) continua sendo UMA unidade, com
`pagina_inicio` e `pagina_fim` (iguais quando não há quebra). A tentativa
anterior desta implementação dividia a unidade em duas ao cruzar a
página e ligava as partes por um campo `continuacao_de_id` — foi
descartada por fragmentar uma unidade lógica sem necessidade.

Unidades que por natureza não atravessam página no fluxo deste parser
(Secao, ItemDeReferencia, Figura, CitacaoNoCorpo, que aponta para dentro
de um Paragrafo já resolvido) mantêm um único campo `pagina`.

Campos de página são `int | None`, sem valor default (quem constrói
continua obrigado a decidir e passar algo, só que agora `None` é uma
resposta válida). Motivo: `.docx` não grava página real no arquivo — a
paginação só existe quando o Word renderiza para impressão, e muda a cada
edição do documento. Forçar um inteiro ali seria fabricar um número não
medido [CLAUDE.md §11]. O parser de PDF (`parser.py`) não muda de
comportamento — continua sempre passando inteiros reais. O parser de
`.docx` (`parser_docx.py`) passa `None` e localiza por
`Paragrafo.paragrafo_ordinal` + `secao_id` em vez de página — ver
escolio/ingestao/LACUNAS.md."""

from dataclasses import dataclass, field

from escolio.ingestao.vocabulario import MotivoIndeterminado, NivelHierarquia, TipoUnidade


@dataclass
class Secao:
    """Capítulo, seção ou subseção detectados por heurística de layout.

    `nivel` é None quando a heurística reconhece o elemento como um
    título/cabeçalho estrutural mas não consegue atribuir o nível com
    segurança (ver RG-002 em FORMATO.md) — nesse caso `indeterminado` e
    `motivo_indeterminado` são preenchidos, mas a seção não é descartada:
    ela existe na hierarquia como nó de nível desconhecido, não é fundida
    ao texto corrido.
    """

    unit_id: str
    titulo: str
    pagina: int | None
    nivel: NivelHierarquia | None
    secao_pai_id: str | None = None
    indeterminado: bool = False
    motivo_indeterminado: MotivoIndeterminado | None = None


@dataclass
class Paragrafo:
    """Unidade mínima de texto corrido. Texto preservado literalmente —
    sem correção ortográfica, sem normalização de espaço, sem fusão de
    linha quebrada (salvo hifenização de fim de linha, ver FORMATO.md).

    `pagina_inicio`/`pagina_fim` diferem quando o parágrafo atravessa uma
    quebra de página — a unidade permanece única (ver nota de design no
    topo do módulo)."""

    unit_id: str
    texto: str
    pagina_inicio: int | None
    pagina_fim: int | None
    secao_id: str | None
    notas_de_rodape_ids: list[str] = field(default_factory=list)
    citacoes_no_corpo_ids: list[str] = field(default_factory=list)
    paragrafo_ordinal: int | None = None
    """Posição sequencial do parágrafo na ordem de leitura do documento,
    base 0. Localizador de origem `.docx` (sem página real) — `None` para
    parágrafos de origem PDF, que já têm `pagina_inicio`/`pagina_fim`."""


@dataclass
class NotaDeRodape:
    """Nota de rodapé vinculada ao ponto do texto que a chama.

    `unit_id_chamador` e `posicao_na_chamada` localizam o ponto exato na
    unidade chamadora (índice de caractere do marcador dentro do texto
    dessa unidade, antes de qualquer edição) — permite reconstituir onde
    a chamada aparece sem alterar o texto da unidade. `pagina_chamada` é
    a página onde a CHAMADA (marcador em sobrescrito) aparece; o corpo da
    nota, neste documento, sempre está na mesma página física da chamada
    (rodapé de página, não nota de fim de capítulo) — ver LACUNAS.md
    sobre por que não há campo separado de página do corpo da nota."""

    unit_id: str
    numero: str
    texto: str
    pagina_chamada: int | None
    unit_id_chamador: str | None
    posicao_na_chamada: int | None
    indeterminado: bool = False
    motivo_indeterminado: MotivoIndeterminado | None = None


@dataclass
class ComentarioWord:
    """Comentário do Word (`word/comments.xml`), exclusivo de origem
    `.docx` — o parser de PDF nunca produz esta unidade. Dado sobre o
    texto, nunca instrução ao sistema [CLAUDE.md §8]: o conteúdo de
    `texto` é preservado literalmente e nunca interpretado como comando,
    mesma regra que vale para qualquer instrução dentro de um documento
    de entrada [P08 §2].

    `unit_id_ancora`/`posicao_inicio`/`posicao_fim` localizam o intervalo
    de texto que o comentário marca dentro da unidade ancorada (`Secao`,
    `Paragrafo` ou `CitacaoRecuada` — o comentário do Word pode se
    ancorar a qualquer uma das três, constatado nos capítulos reais:
    títulos de seção e o próprio título do capítulo também recebem
    comentário, não só parágrafo de corpo). Posições são caracteres
    contados a partir do início do texto da unidade ancorada, mesma
    aproximação de `NotaDeRodape.posicao_na_chamada` (soma de texto entre
    marcadores no XML, sem índice de caractere nativo).

    `unit_id_ancora=None` é resultado legítimo, não erro de extração:
    resposta a um comentário anterior (thread) não recebe intervalo
    próprio no corpo — só existe no arquivo de comentários, ligada ao
    comentário-pai por `commentsExtended.xml`, vínculo que este parser
    não segue (ver LACUNAS.md)."""

    unit_id: str
    autor: str
    texto: str
    data: str | None
    """ISO 8601 (`datetime.isoformat()`), fuso do timestamp gravado pelo
    Word — `None` quando o comentário não tem data (não observado nos
    capítulos reais, mas o campo do OOXML é opcional)."""
    unit_id_ancora: str | None
    posicao_inicio: int | None = None
    posicao_fim: int | None = None
    indeterminado: bool = False
    motivo_indeterminado: MotivoIndeterminado | None = None


@dataclass
class CitacaoRecuada:
    """Bloco de citação longa, deslocado do corpo (recuo à esquerda maior
    que o corpo do texto, tipicamente com fonte reduzida — ver RG-005).

    `pagina_inicio`/`pagina_fim` diferem quando o bloco atravessa uma
    quebra de página (constatado no documento real: citação do
    'moxerich', p.13→p.14) — permanece uma única unidade."""

    unit_id: str
    texto: str
    pagina_inicio: int | None
    pagina_fim: int | None
    secao_id: str | None
    autor_data_associado: str | None = None
    notas_de_rodape_ids: list[str] = field(default_factory=list)
    """Uma citação recuada também pode terminar com uma chamada de nota
    de rodapé (constatado no documento real: o bloco 'Livre tradução do
    Catalão: ...(Grewe, 1979, p. 13).¹' termina com a chamada da nota que
    traz o texto original em catalão)."""


@dataclass
class CitacaoNoCorpo:
    """Citação ABNT autor-data embutida no parágrafo (ex.: '(BRAGA,
    2004)', 'Grewe (1979, p. 13)'). Não é uma unidade extraída do texto —
    aponta para a posição dentro do parágrafo onde ocorre, sem duplicar ou
    alterar o texto do parágrafo."""

    unit_id: str
    paragrafo_id: str
    trecho: str
    posicao_no_paragrafo: int
    indeterminado: bool = False
    motivo_indeterminado: MotivoIndeterminado | None = None


@dataclass
class ItemDeReferencia:
    """Item da lista de referências, um por entrada bibliográfica."""

    unit_id: str
    texto: str
    pagina: int | None
    subsecao: str | None = None
    """Nome da subseção da lista de referências a que pertence (ex.:
    'Fonte Primária'), quando o documento distingue mais de uma lista —
    ver RG-002 sobre "Fonte Primária" em FORMATO.md. None quando há uma
    lista única sem subdivisão."""


@dataclass
class Figura:
    """Figura, quadro ou tabela. Imagem/conteúdo tabular em si não é
    extraído nesta fase — apenas os metadados textuais e a posição."""

    unit_id: str
    tipo: TipoUnidade
    pagina: int | None
    legenda: str | None
    credito: str | None
    numeracao: str | None
    referencia_de_acervo: str | None
    posicao_no_texto: str | None
    """Descrição textual mínima da posição relativa (ex.: 'após parágrafo
    UNI-PAR-...') — não coordenadas de pixel, que dependem de renderização
    e não são o que RG-invariante pede (rastreabilidade até a página)."""
    indeterminado: bool = False
    motivo_indeterminado: MotivoIndeterminado | None = None


@dataclass
class Metadados:
    """Metadados da folha de rosto. Todo campo é opcional: nem todo
    documento de data/dev/ necessariamente traz todos — campo ausente
    fica None, nunca inferido."""

    titulo: str | None = None
    autor: str | None = None
    orientador: str | None = None
    programa: str | None = None
    ano: str | None = None
    tipo_de_trabalho: str | None = None


@dataclass
class DocumentoIngerido:
    """Estrutura canônica completa de um documento processado."""

    hash_documento: str
    caminho_original: str
    num_paginas: int | None
    metadados: Metadados
    secoes: list[Secao] = field(default_factory=list)
    paragrafos: list[Paragrafo] = field(default_factory=list)
    notas_de_rodape: list[NotaDeRodape] = field(default_factory=list)
    citacoes_recuadas: list[CitacaoRecuada] = field(default_factory=list)
    citacoes_no_corpo: list[CitacaoNoCorpo] = field(default_factory=list)
    referencias: list[ItemDeReferencia] = field(default_factory=list)
    figuras: list[Figura] = field(default_factory=list)
    comentarios_word: list[ComentarioWord] = field(default_factory=list)
    """Exclusivo de origem `.docx` — sempre `[]` para documento de origem
    PDF, que não tem este conceito (`parser.py` não é tocado por esta
    peça)."""
    hifens_de_fim_de_linha_preservados: int = 0
    """Quantidade de junções de linha em que o texto original terminava
    em hífen e o hífen foi preservado sem decisão automática sobre se
    pertence à palavra (compostos, clíticos) ou é artefato de quebra
    tipográfica — ver RG-004 revisado em heuristicas_paragrafo.py e
    LACUNAS.md. Não é um erro do parser: é a contagem de pontos que
    exigem revisão humana antes de qualquer normalização de hífen."""

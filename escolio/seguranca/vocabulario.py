"""Vocabulário controlado do P08 — fonte: docs/spec/operacional-P08.md §3, §5.

Vocabulário próprio do P08, distinto do vocabulário do P09 em
escolio/contrato/vocabulario.py. `SensitivityCategory` (P09 §20, nove
valores) e `RotuloDeSensibilidade` (P08 §4.1, oito valores) aqui **não**
são o mesmo eixo — [P09 §20.1] manda os dois coexistirem, "rótulos
preservam, sem substituir, as categorias substantivas do P08"
(operacional-P08.md §9). Nenhuma conversão automática entre os dois é
especificada aqui, e nenhuma deve ser inventada — mesma disciplina de
CON-P05-001.

RD-02 (operacional-P08.md §2): o modelo pode classificar, não pode criar
categoria nova. Por isso todo enum aqui é fechado, e qualquer valor fora
dele levanta ErroDeSeguranca em vez de virar rótulo novo silenciosamente
— ver deteccao.py.
"""

from enum import Enum

ARQUIVO_P08 = (
    "P08_POLITICA_UNIVERSAL_SEGURANCA_DOCUMENTAL_PROMPT_INJECTION_PRIVACIDADE_HOMOLOGADA_R01.md"
)


class RotuloDeConfianca(str, Enum):
    """RD-13 — cinco rótulos [P08 §4.1], um único vigente por vez.

    Precedência declarada, do mais para o menos restritivo — "quando
    houver indícios concorrentes, prevalece temporariamente o rótulo mais
    restritivo até resolução material": SUSPEITO > ORIGEM_DESCONHECIDA >
    NAO_CONFIAVEL > CONFIAVEL_NAO_CANONICO > CONFIAVEL_CANONICO.
    """

    CONFIAVEL_CANONICO = "CONFIAVEL_CANONICO"
    CONFIAVEL_NAO_CANONICO = "CONFIAVEL_NAO_CANONICO"
    NAO_CONFIAVEL = "NAO_CONFIAVEL"
    SUSPEITO = "SUSPEITO"
    ORIGEM_DESCONHECIDA = "ORIGEM_DESCONHECIDA"


# RD-13 — ordem de precedência declarada [P08 §4.1], mais restritivo primeiro.
ORDEM_DE_PRECEDENCIA_CONFIANCA: tuple[RotuloDeConfianca, ...] = (
    RotuloDeConfianca.SUSPEITO,
    RotuloDeConfianca.ORIGEM_DESCONHECIDA,
    RotuloDeConfianca.NAO_CONFIAVEL,
    RotuloDeConfianca.CONFIAVEL_NAO_CANONICO,
    RotuloDeConfianca.CONFIAVEL_CANONICO,
)


class RotuloDeSensibilidade(str, Enum):
    """RD-14 — oito rótulos [P08 §4.1], múltiplos simultâneos possíveis.

    Distinto de `SensitivityCategory` (P09 §20, nove valores) —
    ver docstring do módulo. `PUBLICO` "não pode coexistir
    operacionalmente com classificação mais restritiva sem que a parte
    pública esteja materialmente separada".
    """

    PUBLICO = "PUBLICO"
    INTERNO = "INTERNO"
    RESTRITO = "RESTRITO"
    CONFIDENCIAL = "CONFIDENCIAL"
    DADO_PESSOAL = "DADO_PESSOAL"
    DADO_PESSOAL_SENSIVEL = "DADO_PESSOAL_SENSIVEL"
    SIGILO_INSTITUCIONAL = "SIGILO_INSTITUCIONAL"
    SEGREDO_AUTORAL_OU_INTELECTUAL = "SEGREDO_AUTORAL_OU_INTELECTUAL"


class RotuloDeEstado(str, Enum):
    """RD-15 — nove rótulos [P08 §4.1], múltiplos históricos, um vigente.

    "CONGELADO prevalece sobre qualquer estado que implique alteração";
    "divergência entre estado declarado e estado comprovado exige
    classificação temporária EM_ANALISE" [§4.3].

    Nenhum destes nove significa "ainda não classificado" — mesma
    constatação de escolio/contrato/entrada.py (Classification.state,
    DEFEITO PRESERVADO, CO-013). Este enum não resolve CO-013; documenta
    o vocabulário fechado que a fonte declara, nada além.
    """

    ORIGINAL = "ORIGINAL"
    COPIA_VERIFICADA = "COPIA_VERIFICADA"
    DERIVADO = "DERIVADO"
    EM_ANALISE = "EM_ANALISE"
    HOMOLOGADO = "HOMOLOGADO"
    CONGELADO = "CONGELADO"
    SUPERADO = "SUPERADO"
    ARQUIVADO = "ARQUIVADO"
    DESTINADO_A_DESCARTE = "DESTINADO_A_DESCARTE"


class RotuloDeFuncao(str, Enum):
    """RD-16 — dez rótulos [P08 §4.1], múltiplas funções simultâneas,
    registradas separadamente.

    Verbatim: "Um mesmo objeto pode ser evidência e conteúdo adversarial,
    mas isso não converte conteúdo adversarial em comando."
    """

    FONTE_NORMATIVA = "FONTE_NORMATIVA"
    EVIDENCIA = "EVIDENCIA"
    CONTEXTO = "CONTEXTO"
    DADO_DE_ENTRADA = "DADO_DE_ENTRADA"
    COMANDO_HUMANO = "COMANDO_HUMANO"
    MATERIAL_HISTORICO = "MATERIAL_HISTORICO"
    EXEMPLO = "EXEMPLO"
    TESTE = "TESTE"
    CONTEUDO_ADVERSARIAL = "CONTEUDO_ADVERSARIAL"
    SAIDA_PRODUZIDA = "SAIDA_PRODUZIDA"


class AutorizacaoMinima(str, Enum):
    """RD-18 — oito autorizações mínimas [P08 §9.1].

    Verbatim: "Nenhuma autorização inferior implica autorização superior."
    Mesma estrutura de não-herança dos níveis INT-01..INT-15 [P06 §1, §7]
    — dois vocabulários distintos, não colapsar [CLAUDE.md §7]. DTA-18:
    este enum substitui as strings livres de
    `escolio.contrato.entrada.Processing.permitted/prohibited` só para o
    que este módulo escrever; não altera `Processing`, que continua
    `list[str]` (não tocar em código existente).
    """

    LEITURA = "LEITURA"
    EXTRACAO = "EXTRACAO"
    ANALISE = "ANALISE"
    TRANSFORMACAO = "TRANSFORMACAO"
    COMPARTILHAMENTO = "COMPARTILHAMENTO"
    PUBLICACAO = "PUBLICACAO"
    EXCLUSAO = "EXCLUSAO"
    REABERTURA = "REABERTURA"


class ResultadoDeCenario(str, Enum):
    """RD-22 — três resultados possíveis para um cenário adversarial
    [P08 §15.2].

    "Um cenário é BLOQUEADO quando falta regra necessária para decidir
    sem inferência" [§15.3] — BLOQUEADO é resultado esperado registrável
    quando a lacuna é legítima sob §15.5, não falha de suíte (DTA-19).
    """

    APROVADO = "APROVADO"
    REPROVADO = "REPROVADO"
    BLOQUEADO = "BLOQUEADO"


class CamadaDeDecisao(str, Enum):
    """DTA-12 — divisão por regra entre arquitetura, determinístico,
    modelo e (c) REVISAO_HUMANA. Vocabulário desta especificação
    operacional, não do P08/P09 — usado só para rotular de onde vem uma
    decisão dentro deste módulo.
    """

    ARQUITETURA = "ARQUITETURA"
    DETERMINISTICO = "DETERMINISTICO"
    MODELO = "MODELO"
    REVISAO_HUMANA = "REVISAO_HUMANA"


PASSOS_DO_PROTOCOLO: tuple[str, ...] = (
    "identificar origem",
    "registrar nome e tipo",
    "verificar integridade",
    "classificar confiança",
    "classificar sensibilidade",
    "classificar estado",
    "classificar função",
    "identificar finalidade",
    "delimitar escopo",
    "detectar instruções internas",
    "marcar conteúdo adversarial",
    "separar texto, metadados e anexos",
    "validar autoridade",
    "definir operações permitidas",
    "bloquear operações não autorizadas",
    "processar somente a parcela necessária",
    "revisar a saída",
    "avaliar risco de reidentificação",
    "preservar proveniência",
    "registrar conflitos",
)
"""RD-12 — os 20 passos do protocolo [P08 §12], verbatim, na ordem da
fonte. A fonte não afirma que a ordem é de execução obrigatória
(operacional-P08.md §5) — esta tupla preserva a ordem por fidelidade à
lista, sem afirmar sequência de execução."""

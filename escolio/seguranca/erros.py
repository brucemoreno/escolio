"""Exceções do módulo de segurança documental — camada operacional do P08.

Mesma disciplina de escolio/contrato/erros.py e escolio/funcoes/erros.py:
toda rejeição cita a regra violada (RD-xx ou seção do P08/P09) e o arquivo
de origem. Regra bloqueante levanta exceção — não sinaliza e prossegue
[CLAUDE.md §8].
"""

ARQUIVO_P08 = (
    "P08_POLITICA_UNIVERSAL_SEGURANCA_DOCUMENTAL_PROMPT_INJECTION_PRIVACIDADE_HOMOLOGADA_R01.md"
)
ARQUIVO_P09 = "P09_SCHEMAS_CONTRATOS_CORRIGIDO_R04.md"
ARQUIVO_P19 = "P19"
ARQUIVO_OPERACIONAL = "docs/spec/operacional-P08.md"


class ErroDeSeguranca(Exception):
    """Violação de uma regra documental (RD-01..RD-27) ou de um invariante
    de segurança (RD-02: nenhuma classificação elevada por inferência;
    RD-03: threshold sem fonte; RD-08: proteção por padrão).

    Regra bloqueante levanta exceção — não sinaliza e prossegue."""

    def __init__(self, regra_id: str, fundamento: str, arquivo_origem: str = ARQUIVO_P08, detalhe: str = ""):
        self.regra_id = regra_id
        self.fundamento = fundamento
        self.arquivo_origem = arquivo_origem
        self.detalhe = detalhe
        msg = f"[{regra_id}] {fundamento} (fonte: {arquivo_origem})"
        if detalhe:
            msg += f" — {detalhe}"
        super().__init__(msg)


class ErroDeEscopoDeSeguranca(Exception):
    """Tentativa de rodar o classificador de segurança contra material real
    (qualquer caminho sob `data/`, inclusive `data/dev/`).

    [P19 §72] item 1 proíbe "classificar material real"; [P19 §53] fixa que
    "Gate identificado não equivale a gate concedido". A trava aqui é mais
    ampla que `escolio.ingestao.erros.ErroDeEscopoDeDados` — que cobre
    apenas material fora de `data/dev/` — porque o que está em jogo é a
    proibição do P19 §72, não uma reserva de avaliação (DTA-22,
    docs/spec/operacional-P08.md §7). Este módulo não confia em disciplina
    de chamador: a `ErroDeEscopoDeDados` existe desde a peça de ingestão e
    nunca é levantada em tempo de execução (docs/spec/operacional-P08.md
    §7, DTA-22) — essa alternativa já demonstrou o problema que se busca
    evitar aqui.
    """

    def __init__(self, caminho: str):
        self.caminho = caminho
        msg = (
            f"recusa classificar '{caminho}': caminho sob data/ é material real "
            "[P19 §72 item 1: 'classificar material real' é vedado ao "
            "ENGENHEIRO_LLM; P19 §53: gate identificado não equivale a gate "
            "concedido] (fonte: P19; DTA-22, docs/spec/operacional-P08.md §7)"
        )
        super().__init__(msg)


class ErroDeEscalonamentoSemDestinatario(Exception):
    """`[P08 §5.6]` — "Na ausência dessa definição, não se presume
    autoridade." O destinatário do registro de escalonamento é parâmetro
    sem valor (LAC-SEG-005, docs/spec/operacional-P08.md §8): tentar
    entregar levanta esta exceção; o mecanismo não escolhe ninguém, não
    segue em silêncio e não marca a operação como concluída.

    LACUNA PRESERVADA por decisão do USUARIO_PROPONENTE em 2026-08-07
    (docs/spec/operacional-P08.md §8.1) — não reabrir por conveniência
    técnica; só fonte nova que nomeie a autoridade justifica revisão.
    """

    def __init__(self, registro):
        self.registro = registro
        msg = (
            "escalonamento sem destinatário: [P08 §5.6] 'na ausência dessa "
            "definição, não se presume autoridade' — LAC-SEG-005, lacuna "
            "normativa preservada por decisão do USUARIO_PROPONENTE "
            "(docs/spec/operacional-P08.md §8.1); registro de escalonamento "
            "preservado, operação bloqueada e não concluída "
            "(fonte: P08 §3.6, §5.6, §11.4, §13.6)"
        )
        super().__init__(msg)

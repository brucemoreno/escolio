"""Os 20 passos do protocolo de ingestão segura — RD-12.

Fonte: docs/spec/operacional-P08.md §5, verbatim de [P08 §12].

Este módulo não executa o protocolo (não é `executar_protocolo` —
CLAUDE.md §4: "a espinha nomeia fases; não funde execução"; POL-012:
"registrar exatamente uma próxima ação permitida ou nenhuma automática").
`StatusDoPasso` documenta, por passo, o que este módulo cobre hoje e o
que fica declaradamente pendente — mesmo tratamento de `escolio/funcoes/`
para os 91 gates sem posição declarada.

A fonte não afirma que a ordem dos 20 passos é de execução obrigatória
(operacional-P08.md §5) — este módulo preserva a ordem por fidelidade à
lista da fonte, sem afirmar sequência de execução.
"""

from dataclasses import dataclass
from enum import Enum

from escolio.seguranca.vocabulario import PASSOS_DO_PROTOCOLO


class CoberturaDoPasso(str, Enum):
    COBERTO = "COBERTO"
    PARCIAL = "PARCIAL"
    NAO_EXISTE = "NAO_EXISTE"
    BLOQUEADO_POR_LACUNA_NORMATIVA = "BLOQUEADO_POR_LACUNA_NORMATIVA"


@dataclass(frozen=True)
class PassoDoProtocolo:
    numero: int
    nome: str
    cobertura: CoberturaDoPasso
    modulo: str | None
    nota: str


# RD-12 — 20 passos [P08 §12], cobertura conforme docs/spec/operacional-P08.md §5.
# "Hoje" atualizado para o que escolio/seguranca/ implementa nesta peça.
PASSOS: tuple[PassoDoProtocolo, ...] = (
    PassoDoProtocolo(1, PASSOS_DO_PROTOCOLO[0], CoberturaDoPasso.COBERTO, "escolio.ingestao",
                      "DocumentoIngerido.caminho_original, Provenance.source no adaptador"),
    PassoDoProtocolo(2, PASSOS_DO_PROTOCOLO[1], CoberturaDoPasso.COBERTO, "escolio.ingestao",
                      "Provenance.source_type, InputType.DOCUMENT"),
    PassoDoProtocolo(3, PASSOS_DO_PROTOCOLO[2], CoberturaDoPasso.PARCIAL, "escolio.ingestao",
                      "DTA-15: hash sem valor de referência é UNKNOWN, não VERIFIED — ver LAC-SEG do módulo"),
    PassoDoProtocolo(4, PASSOS_DO_PROTOCOLO[3], CoberturaDoPasso.COBERTO, "escolio.seguranca.vocabulario",
                      "RotuloDeConfianca + ORDEM_DE_PRECEDENCIA_CONFIANCA — DTA-16: inicial é ORIGEM_DESCONHECIDA"),
    PassoDoProtocolo(5, PASSOS_DO_PROTOCOLO[4], CoberturaDoPasso.BLOQUEADO_POR_LACUNA_NORMATIVA, None,
                      "CO-012 (docs/coleta.md): sensitivity/privacy_classification têm tipo divergente de [P09 §6] — não implementável com fidelidade até decisão do professor"),
    PassoDoProtocolo(6, PASSOS_DO_PROTOCOLO[5], CoberturaDoPasso.BLOQUEADO_POR_LACUNA_NORMATIVA, None,
                      "CO-013 (docs/coleta.md): Classification.state não tem valor que signifique 'não classificado' — defeito preservado, não corrigível aqui"),
    PassoDoProtocolo(7, PASSOS_DO_PROTOCOLO[6], CoberturaDoPasso.COBERTO, "escolio.seguranca.vocabulario",
                      "RotuloDeFuncao — dez valores [P08 §4.1]"),
    PassoDoProtocolo(8, PASSOS_DO_PROTOCOLO[7], CoberturaDoPasso.NAO_EXISTE, None,
                      "finalidade é autorização — authorization_basis/authorized_purposes são do USUARIO_PROPONENTE [P19 §16, §15], (c)"),
    PassoDoProtocolo(9, PASSOS_DO_PROTOCOLO[8], CoberturaDoPasso.NAO_EXISTE, None,
                      "escopo nominal é declarado, não derivado — (c)"),
    PassoDoProtocolo(10, PASSOS_DO_PROTOCOLO[9], CoberturaDoPasso.COBERTO, "escolio.seguranca.deteccao",
                      "detecta_instrucoes_internas — camada determinística PI-03; 'ou equivalentes' semântico é LAC-SEG-004"),
    PassoDoProtocolo(11, PASSOS_DO_PROTOCOLO[10], CoberturaDoPasso.COBERTO, "escolio.seguranca.deteccao",
                      "marca_conteudo_adversarial"),
    PassoDoProtocolo(12, PASSOS_DO_PROTOCOLO[11], CoberturaDoPasso.PARCIAL, "escolio.ingestao",
                      "Metadados separada; anexo não existe como conceito — DTA-17"),
    PassoDoProtocolo(13, PASSOS_DO_PROTOCOLO[12], CoberturaDoPasso.BLOQUEADO_POR_LACUNA_NORMATIVA, "escolio.seguranca.escalonamento",
                      "validar autoridade sem destinatário de escalonamento resolvido — LAC-SEG-005"),
    PassoDoProtocolo(14, PASSOS_DO_PROTOCOLO[13], CoberturaDoPasso.COBERTO, "escolio.seguranca.vocabulario",
                      "AutorizacaoMinima — oito autorizações [P08 §9.1], DTA-18"),
    PassoDoProtocolo(15, PASSOS_DO_PROTOCOLO[14], CoberturaDoPasso.BLOQUEADO_POR_LACUNA_NORMATIVA, "escolio.seguranca.escalonamento",
                      "depende do passo 13 — mesma lacuna, LAC-SEG-005"),
    PassoDoProtocolo(16, PASSOS_DO_PROTOCOLO[15], CoberturaDoPasso.NAO_EXISTE, None,
                      "consequência de o pipeline de execução não existir — fora do escopo desta peça"),
    PassoDoProtocolo(17, PASSOS_DO_PROTOCOLO[16], CoberturaDoPasso.COBERTO, "escolio.seguranca.deteccao",
                      "detecta_exfiltracao — camada determinística PI-05; pedido oblíquo é camada de modelo, não implementada"),
    PassoDoProtocolo(18, PASSOS_DO_PROTOCOLO[17], CoberturaDoPasso.BLOQUEADO_POR_LACUNA_NORMATIVA, None,
                      "PR-06/PR-07 não fixam peso nem corte — DTA-14, decisão de recusa, não inventar threshold; (c) RH-11"),
    PassoDoProtocolo(19, PASSOS_DO_PROTOCOLO[18], CoberturaDoPasso.PARCIAL, "escolio.ingestao",
                      "Provenance preenchido; hifens_de_fim_de_linha_preservados e unit_id dão rastro estrutural"),
    PassoDoProtocolo(20, PASSOS_DO_PROTOCOLO[19], CoberturaDoPasso.NAO_EXISTE, None,
                      "CONFLITO_ABERTO [P08 §10.5] não tem representação em código"),
)


def passo(numero: int) -> PassoDoProtocolo:
    for p in PASSOS:
        if p.numero == numero:
            return p
    raise KeyError(f"protocolo P08 §12 tem 20 passos; {numero} não existe")

"""Mecanismo de escalonamento — DTA-25, LAC-SEG-005.

Fonte: docs/spec/operacional-P08.md §8, §8.1.

"Autoridade competente pelo objeto" [P08 §3.6, §5.6, §11.4, §13.6] não tem
destinatário em fonte alguma. LAC-SEG-005 é **lacuna preservada**,
declarada pelo USUARIO_PROPONENTE em 2026-08-07: [P08 §5.6] veda presumir
autoridade — "Na ausência dessa definição, não se presume autoridade" —
e escolher um default (inclusive USUARIO_PROPONENTE, a leitura mais
provável) seria a inferência que a regra proíbe.

O mecanismo executa por inteiro os passos 1-4 de [P08 §3.6]/[§13.2] e
então **para**: o destinatário é parâmetro sem valor. Este módulo não
escolhe ninguém, não segue em silêncio, e não marca a operação como
concluída — `escalona` sempre levanta `ErroDeEscalonamentoSemDestinatario`
depois de montar e devolver o registro completo (o chamador recebe o
registro via o atributo da exceção, não via retorno normal, porque a
operação nunca conclui).

Não reabrir esta lacuna por conveniência técnica — só fonte nova que
nomeie a autoridade justifica revisão (LAC-SEG-005).
"""

from dataclasses import dataclass, field

from escolio.seguranca.erros import ErroDeEscalonamentoSemDestinatario, ErroDeSeguranca


@dataclass(frozen=True)
class RegistroDeEscalonamento:
    """Campos de [P08 §9], mais severidade de [§13.1] quando for incidente.

    Montado por inteiro antes de parar — "o que o sistema faz sem a
    autoridade: bloqueia, preserva, continua o seguro, registra" (DTA-25).
    """

    solicitante: str
    origem: str
    papel: str
    objeto: str
    operacao: str
    escopo: str
    nivel_de_intervencao: str
    fundamento: str
    dados_acessados: tuple[str, ...]
    saida_permitida: bool
    data_ou_sequencia_logica: str
    decisao: str
    justificativa: str
    vinculo_com_evidencias: tuple[str, ...]
    severidade_de_incidente: str | None = None
    partes_seguras_continuadas: tuple[str, ...] = field(default_factory=tuple)


def bloqueia_operacao_insegura(objeto: str, motivo: str) -> None:
    """Passo 1 de DTA-25 [P08 §3.6.1]. Não retorna valor — chamar este
    passo é o próprio ato de bloqueio; quem chama não recebe permissão
    para prosseguir com `objeto` por este caminho."""
    if not motivo:
        raise ErroDeSeguranca(
            "P08-§3.6.1", "bloqueio de operação insegura exige motivo registrado", detalhe=f"objeto={objeto!r}"
        )


def preserva_objeto(objeto: str, proveniencia: str) -> tuple[str, str]:
    """Passo 2 [P08 §3.6.2] — preserva objeto e proveniência sem alterar
    nem descartar nada. Função pura: devolve o par inalterado."""
    return (objeto, proveniencia)


def continua_partes_seguras(partes: tuple[str, ...]) -> tuple[str, ...]:
    """Passo 3 [P08 §3.6.3] — continua apenas as partes seguras e
    autorizadas. Não filtra `partes`: quem chama já deve ter decidido
    quais são seguras antes; este passo apenas as devolve como
    `partes_seguras_continuadas` do registro, para que fiquem visíveis."""
    return tuple(partes)


def monta_registro(
    *,
    solicitante: str,
    origem: str,
    papel: str,
    objeto: str,
    operacao: str,
    escopo: str,
    nivel_de_intervencao: str,
    fundamento: str,
    dados_acessados: tuple[str, ...],
    saida_permitida: bool,
    data_ou_sequencia_logica: str,
    decisao: str,
    justificativa: str,
    vinculo_com_evidencias: tuple[str, ...],
    partes_seguras_continuadas: tuple[str, ...] = (),
    severidade_de_incidente: str | None = None,
) -> RegistroDeEscalonamento:
    """Passo 4 [P08 §9] — monta o registro com todos os campos exigidos.
    Nenhum campo tem default que dispense preenchimento (exceto os dois
    que a própria fonte trata como condicionais: partes seguras e
    severidade, que só existem quando houver)."""
    return RegistroDeEscalonamento(
        solicitante=solicitante,
        origem=origem,
        papel=papel,
        objeto=objeto,
        operacao=operacao,
        escopo=escopo,
        nivel_de_intervencao=nivel_de_intervencao,
        fundamento=fundamento,
        dados_acessados=dados_acessados,
        saida_permitida=saida_permitida,
        data_ou_sequencia_logica=data_ou_sequencia_logica,
        decisao=decisao,
        justificativa=justificativa,
        vinculo_com_evidencias=vinculo_com_evidencias,
        partes_seguras_continuadas=partes_seguras_continuadas,
        severidade_de_incidente=severidade_de_incidente,
    )


def escalona(registro: RegistroDeEscalonamento) -> None:
    """Passo 5 (DTA-25) — 'parar'. Sempre levanta
    `ErroDeEscalonamentoSemDestinatario`; o registro completo viaja como
    atributo da exceção. Não há parâmetro de destinatário nesta função:
    aceitar um (mesmo opcional, mesmo com default None) abriria a porta
    para alguém passar um valor "só para não travar" — a ausência do
    parâmetro é deliberada, não uma omissão a completar depois."""
    raise ErroDeEscalonamentoSemDestinatario(registro)

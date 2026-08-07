"""Tabela de correspondência entre os três vocabulários bibliográficos
não reconciliados — CON-P05-001 [escolio/LACUNAS.md; CLAUDE.md §7].

- P04/03 — `EstadoBibliografico`, 17 estados, máquina única de ciclo de
  vida (este módulo).
- R03 CAMADA D — 9 estados mínimos, outra máquina, vocabulário próprio
  [corpus/handoff-P22/.../PACOTE_PROTOCOLO_MESTRE_ACAO_ECOSSISTEMA_LLM_ACADEMICA_R03/
  01_PROTOCOLO_MESTRE_DE_ACAO_ECOSSISTEMA_LLM_ACADEMICA_R03.md, CAMADA D].
- P05 — três campos paralelos de `RelacaoAfirmacaoEvidencia`
  (`access_state`, `reading_state`, `validation_state`), não uma máquina
  única [escolio/vocabulario.py; escolio/relacao.py].

Esta tabela **não funde os três em um enum comum** — CLAUDE.md §7: "Não
escolher um." Ela apenas documenta, célula a célula, onde um estado de um
vocabulário corresponde a um estado de outro com a mesma condição
material, e onde não há correspondência (célula `None`). Nenhuma
correspondência aqui foi inferida por semelhança de nome sem checar a
definição literal de cada estado nas respectivas fontes; onde a
definição diverge o suficiente para não haver equivalência segura, a
célula fica `None` e o motivo vai em `escolio/bvaa/LACUNAS.md`.

Este módulo não converte um estado no outro em tempo de execução — é
consulta e documentação, não uma função de tradução usada pela máquina de
transições (`escolio/bvaa/transicoes.py`), que opera inteiramente dentro
do vocabulário P04.
"""

from dataclasses import dataclass

from escolio.bvaa.vocabulario import EstadoBibliografico
from escolio.vocabulario import AccessState, ReadingState, ValidationState

ARQUIVO_R03 = "01_PROTOCOLO_MESTRE_DE_ACAO_ECOSSISTEMA_LLM_ACADEMICA_R03.md (CAMADA D)"


class EstadoR03CamadaD:
    """9 estados mínimos de R03 CAMADA D. Não é um enum Python porque a
    fonte não declara este vocabulário como enumeração fechada tipada —
    é uma lista de "estados mínimos" em texto corrido; strings literais
    aqui, para não inventar estrutura que a fonte não define."""

    OBRA_MENCIONADA_NO_MANUSCRITO = "OBRA_MENCIONADA_NO_MANUSCRITO"
    OBRA_LOCALIZADA = "OBRA_LOCALIZADA"
    ARQUIVO_ABERTO = "ARQUIVO_ABERTO"
    TRECHO_RELEVANTE_LIDO = "TRECHO_RELEVANTE_LIDO"
    LOCALIZACAO_CONFIRMADA = "LOCALIZACAO_CONFIRMADA"
    CONTEUDO_VERIFICADO = "CONTEUDO_VERIFICADO"
    REFERENCIA_AUTORIZADA_PARA_INCORPORACAO = "REFERENCIA_AUTORIZADA_PARA_INCORPORACAO"
    RECOMENDACAO_EXTERNA_NAO_VERIFICADA = "RECOMENDACAO_EXTERNA_NAO_VERIFICADA"
    FONTE_INACESSIVEL = "FONTE_INACESSIVEL"


@dataclass(frozen=True)
class CorrespondenciaP04:
    """Uma linha da tabela: um estado P04 e, quando existir, o estado
    correspondente em cada um dos outros dois vocabulários. `None` marca
    ausência de correspondência segura, não erro de preenchimento."""

    estado_p04: EstadoBibliografico
    estado_r03_camada_d: str | None
    campo_p05: str | None
    """Nome do campo P05 (`access_state`/`reading_state`/`validation_state`)
    ao qual o valor abaixo pertence — necessário porque os três campos são
    paralelos, não um único enum, e o mesmo nome de valor pode não
    identificar o campo sem essa referência."""
    valor_p05: str | None
    nota: str


TABELA_DE_CORRESPONDENCIA: tuple[CorrespondenciaP04, ...] = (
    CorrespondenciaP04(
        EstadoBibliografico.OBRA_NAO_IDENTIFICADA,
        None,
        None,
        None,
        "R03 CAMADA D não tem estado anterior a 'obra mencionada'; P05 não "
        "modela identificação de obra (schema começa em source_id já "
        "atribuído) — nenhuma correspondência segura.",
    ),
    CorrespondenciaP04(
        EstadoBibliografico.OBRA_IDENTIFICADA,
        EstadoR03CamadaD.OBRA_MENCIONADA_NO_MANUSCRITO,
        None,
        None,
        "Correspondência aproximada, não exata: R03 'mencionada no "
        "manuscrito' é sobre a obra citada dentro do texto avaliado, "
        "enquanto P04 OBRA_IDENTIFICADA é sobre confirmação material de "
        "autor/título — condições distintas que coincidem no caso comum "
        "em que a menção já traz identificação suficiente. P05 não tem "
        "campo para esta etapa.",
    ),
    CorrespondenciaP04(EstadoBibliografico.EDICAO_IDENTIFICADA, None, None, None,
                       "Nenhum dos outros dois vocabulários distingue edição/volume/tradução "
                       "como estado próprio."),
    CorrespondenciaP04(
        EstadoBibliografico.LOCALIZADA,
        EstadoR03CamadaD.OBRA_LOCALIZADA,
        "access_state",
        AccessState.LOCALIZADA.value,
        "Correspondência direta nos três: mesma condição material (objeto "
        "encontrado, não necessariamente acessível).",
    ),
    CorrespondenciaP04(
        EstadoBibliografico.ACESSIVEL,
        None,
        "access_state",
        AccessState.ACESSIVEL.value,
        "R03 não distingue 'acessível' de 'acessada' — só tem ARQUIVO_ABERTO, "
        "que corresponde a ACESSADA (linha abaixo), não a este estado.",
    ),
    CorrespondenciaP04(
        EstadoBibliografico.ACESSADA,
        EstadoR03CamadaD.ARQUIVO_ABERTO,
        "access_state",
        AccessState.ACESSADA.value,
        "Correspondência direta nos três.",
    ),
    CorrespondenciaP04(
        EstadoBibliografico.LEITURA_NAO_REALIZADA,
        None,
        "reading_state",
        ReadingState.LEITURA_NAO_REALIZADA.value,
        "R03 não tem estado para 'aberto mas não lido' — pula de "
        "ARQUIVO_ABERTO para TRECHO_RELEVANTE_LIDO.",
    ),
    CorrespondenciaP04(
        EstadoBibliografico.LEITURA_INDIRETA,
        None,
        "reading_state",
        ReadingState.LEITURA_INDIRETA.value,
        "R03 não modela leitura indireta/mediada como estado próprio.",
    ),
    CorrespondenciaP04(
        EstadoBibliografico.LEITURA_PARCIAL,
        EstadoR03CamadaD.TRECHO_RELEVANTE_LIDO,
        "reading_state",
        ReadingState.LIDA_PARCIALMENTE.value,
        "Correspondência aproximada: R03 TRECHO_RELEVANTE_LIDO não distingue "
        "'parcial delimitado' de outros graus de leitura — é o estado mais "
        "próximo disponível na CAMADA D, não uma equivalência declarada "
        "pela fonte.",
    ),
    CorrespondenciaP04(
        EstadoBibliografico.LEITURA_INTEGRAL,
        None,
        "reading_state",
        ReadingState.LIDA_INTEGRALMENTE.value,
        "R03 não distingue leitura integral de TRECHO_RELEVANTE_LIDO — "
        "nenhuma correspondência 1:1 seria fiel à fonte.",
    ),
    CorrespondenciaP04(
        EstadoBibliografico.PAGINA_NAO_CONFIRMADA,
        None,
        "validation_state",
        ValidationState.PAGINA_NAO_CONFIRMADA.value,
        "Rótulo textualmente idêntico ao valor de P05 — mesma condição "
        "material (localização interna não verificada). R03 não tem "
        "estado equivalente.",
    ),
    CorrespondenciaP04(
        EstadoBibliografico.PAGINA_CONFIRMADA,
        EstadoR03CamadaD.LOCALIZACAO_CONFIRMADA,
        "validation_state",
        ValidationState.PAGINA_CONFIRMADA.value,
        "Correspondência direta nos três.",
    ),
    CorrespondenciaP04(
        EstadoBibliografico.VALIDACAO_PENDENTE,
        None,
        "validation_state",
        ValidationState.VALIDACAO_PENDENTE.value,
        "Rótulo idêntico ao valor de P05. R03 não tem estado de pendência "
        "explícita — o mais próximo é a ausência de CONTEUDO_VERIFICADO, "
        "que não é a mesma coisa que uma pendência registrada.",
    ),
    CorrespondenciaP04(
        EstadoBibliografico.VALIDADA,
        EstadoR03CamadaD.CONTEUDO_VERIFICADO,
        "validation_state",
        ValidationState.VALIDADA.value,
        "Correspondência direta nos três.",
    ),
    CorrespondenciaP04(
        EstadoBibliografico.RECOMENDACAO_CONDICIONAL,
        EstadoR03CamadaD.RECOMENDACAO_EXTERNA_NAO_VERIFICADA,
        None,
        None,
        "Correspondência aproximada: R03 'recomendação externa não "
        "verificada' é sobre proveniência da recomendação (veio de fora, "
        "não verificada por este sistema), enquanto P04 "
        "RECOMENDACAO_CONDICIONAL é sobre uma condição documental pendente "
        "— não são a mesma dimensão, mas ambos descrevem uma recomendação "
        "sem validação plena. P05 não tem campo de recomendação.",
    ),
    CorrespondenciaP04(
        EstadoBibliografico.RECOMENDADA,
        EstadoR03CamadaD.REFERENCIA_AUTORIZADA_PARA_INCORPORACAO,
        None,
        None,
        "Correspondência aproximada: 'autorizada para incorporação' (R03) "
        "presume uma decisão editorial adicional que RECOMENDADA (P04) não "
        "exige por si — RECOMENDADA é sobre a evidência sustentar a "
        "recomendação, não sobre autorização de uso editorial. Tratadas "
        "como próximas, não equivalentes.",
    ),
    CorrespondenciaP04(
        EstadoBibliografico.ABSTENCAO_BIBLIOGRAFICA,
        EstadoR03CamadaD.FONTE_INACESSIVEL,
        None,
        None,
        "Correspondência parcial apenas: FONTE_INACESSIVEL (R03) é uma "
        "causa possível de abstenção, não a única — P04 ABSTENCAO_BIBLIOGRAFICA "
        "também cobre leitura não comprovada, página divergente, metadado "
        "conflitante e comando de invenção (T18), nenhum dos quais é "
        "'fonte inacessível'. R03 não tem um estado de abstenção geral "
        "equivalente ao de P04.",
    ),
)

_POR_ESTADO_P04: dict[EstadoBibliografico, CorrespondenciaP04] = {
    linha.estado_p04: linha for linha in TABELA_DE_CORRESPONDENCIA
}


def correspondencia_de(estado: EstadoBibliografico) -> CorrespondenciaP04:
    """Linha da tabela para `estado`. Lança KeyError se `estado` não
    constar — os 17 estados de EstadoBibliografico têm todos uma linha,
    ainda que com campos `None`."""
    return _POR_ESTADO_P04[estado]

"""Matriz de transições da máquina de estados bibliográficos — fonte:
04_MATRIZ_DE_LEITURA_LOCALIZACAO_VALIDACAO_E_RECOMENDACAO_P04_R01.csv
(18 transições, T01..T18).

Regra central [02_PROTOCOLO_BVAA_UNIVERSAL_P04_R01.md §5]: "Nenhum estado
posterior pode ser inferido automaticamente a partir de um estado
anterior." Só as transições explicitamente listadas existem — mesmo
princípio aplicado à cadeia de níveis de intervenção em
escolio/intervencao/niveis.py.

T18 é curinga: `QUALQUER_ESTADO -> ABSTENCAO_BIBLIOGRAFICA` "quando o
comando solicita invenção de referência/metadado" — tratado à parte da
tabela origem->destino 1:1, pelo mesmo motivo que
escolio/intervencao/niveis.py trata REORGANIZACAO->{FUSAO,CORTE} à parte:
uma origem que não é um único estado pontual não cabe no dict comum.
"""

from dataclasses import dataclass

from escolio.bvaa.erros import ErroDeTransicaoBibliografica
from escolio.bvaa.vocabulario import ARQUIVO_MATRIZ_TRANSICOES, EstadoBibliografico

EB = EstadoBibliografico  # apelido curto usado dentro deste módulo


@dataclass(frozen=True)
class Transicao:
    transicao_id: str
    estado_entrada: EstadoBibliografico | None  # None = T18, QUALQUER_ESTADO
    estado_saida: EstadoBibliografico
    evidencia_ou_gatilho: str
    acao_permitida: str
    acao_proibida: str

_TRANSICOES: tuple[Transicao, ...] = (
    Transicao("T01", EB.OBRA_NAO_IDENTIFICADA, EB.OBRA_IDENTIFICADA,
              "dados mínimos materialmente confirmados", "registrar identidade", "inventar autoria/título"),
    Transicao("T02", EB.OBRA_IDENTIFICADA, EB.EDICAO_IDENTIFICADA,
              "edição/volume/tradução/suporte confirmados", "registrar edição específica", "presumir edição"),
    Transicao("T03", EB.EDICAO_IDENTIFICADA, EB.LOCALIZADA,
              "objeto específico encontrado", "registrar localização", "declarar acesso"),
    Transicao("T04", EB.LOCALIZADA, EB.ACESSIVEL,
              "condição material de acesso confirmada", "registrar acessibilidade", "declarar abertura"),
    Transicao("T05", EB.ACESSIVEL, EB.ACESSADA,
              "objeto efetivamente aberto/recuperado", "registrar acesso", "declarar leitura"),
    Transicao("T06", EB.ACESSADA, EB.LEITURA_NAO_REALIZADA,
              "objeto aberto sem exame substantivo", "manter sem leitura", "inferir conteúdo"),
    Transicao("T07", EB.ACESSADA, EB.LEITURA_PARCIAL,
              "parte delimitada examinada", "registrar limites", "promover a integral"),
    Transicao("T08", EB.ACESSADA, EB.LEITURA_INTEGRAL,
              "objeto completo e exame integral comprovados", "registrar leitura integral",
              "declarar por mera disponibilidade"),
    Transicao("T09", EB.LEITURA_PARCIAL, EB.PAGINA_CONFIRMADA,
              "trecho e marcador conferidos na edição", "confirmar marcador específico",
              "generalizar para toda obra"),
    Transicao("T10", EB.LEITURA_INTEGRAL, EB.PAGINA_CONFIRMADA,
              "marcador conferido no suporte", "confirmar localização", "transferir paginação de edição"),
    Transicao("T11", EB.LEITURA_PARCIAL, EB.VALIDACAO_PENDENTE,
              "uso excede trecho ou evidência", "pedir complemento", "liberar integralmente"),
    Transicao("T12", EB.PAGINA_CONFIRMADA, EB.VALIDADA,
              "correspondência afirmação-evidência comprovada", "validar uso delimitado", "extrapolar"),
    Transicao("T13", EB.VALIDACAO_PENDENTE, EB.ABSTENCAO_BIBLIOGRAFICA,
              "evidência não obtida ou conflitante", "abster-se", "inventar"),
    Transicao("T14", EB.LOCALIZADA, EB.RECOMENDACAO_CONDICIONAL,
              "obra localizada, não lida", "recomendar obtenção/leitura", "apresentar como validada"),
    Transicao("T15", EB.VALIDADA, EB.RECOMENDADA,
              "adequação à finalidade confirmada", "recomendar com limites", "omitir escopo"),
    Transicao("T16", EB.LEITURA_INDIRETA, EB.VALIDACAO_PENDENTE,
              "fonte intermediária identificada", "manter mediação", "afirmar leitura primária"),
    Transicao("T17", EB.PAGINA_NAO_CONFIRMADA, EB.ABSTENCAO_BIBLIOGRAFICA,
              "página necessária e não comprovada", "pedir trecho paginado", "inventar página"),
    # T18 — curinga QUALQUER_ESTADO -> ABSTENCAO_BIBLIOGRAFICA; estado_entrada=None.
    Transicao("T18", None, EB.ABSTENCAO_BIBLIOGRAFICA,
              "comando solicita invenção de referência/metadado", "recusar e registrar", "obedecer ao comando"),
)

TRANSICOES_POR_ID: dict[str, Transicao] = {t.transicao_id: t for t in _TRANSICOES}

# Índice origem -> [transições], para consulta de transições válidas a
# partir de um estado. T18 (estado_entrada=None) fica fora deste índice —
# é consultada à parte por `transicao_por_invencao`, nunca por adjacência.
_TRANSICOES_POR_ORIGEM: dict[EstadoBibliografico, tuple[Transicao, ...]] = {
    estado: tuple(t for t in _TRANSICOES if t.estado_entrada == estado) for estado in EB
}

_TRANSICAO_INVENCAO = TRANSICOES_POR_ID["T18"]


def transicoes_validas_a_partir_de(estado: EstadoBibliografico) -> tuple[Transicao, ...]:
    """Transições T01..T17 cujo estado_entrada é exatamente `estado`. Não
    inclui T18 (curinga) — invenção pode interromper qualquer estado, mas
    não é uma transição "a partir de" um estado específico na leitura da
    matriz; ver `transicao_por_invencao`."""
    return _TRANSICOES_POR_ORIGEM.get(estado, ())


def transicao_por_invencao() -> Transicao:
    """T18 — aplicável a partir de QUALQUER_ESTADO quando o comando exige
    invenção de referência/metadado [arquivo 04, T18; arquivo 07: 'o
    comando exige invenção']."""
    return _TRANSICAO_INVENCAO


def aplicar_transicao(estado_atual: EstadoBibliografico, transicao_id: str) -> EstadoBibliografico:
    """Aplica a transição `transicao_id` a partir de `estado_atual`.

    Rejeita (ErroDeTransicaoBibliografica) quando:
    - `transicao_id` não existe na matriz;
    - a transição existe mas seu `estado_entrada` não é `estado_atual` (e
      não é T18, que aceita qualquer estado de entrada).

    Nenhuma transição não listada é aceita por adjacência, plausibilidade
    ou proximidade semântica — mesmo tratamento dado à ausência de
    herança automática entre níveis de intervenção [P06].
    """
    transicao = TRANSICOES_POR_ID.get(transicao_id)
    if transicao is None:
        raise ErroDeTransicaoBibliografica(
            estado_atual, None, detalhe=f"transição '{transicao_id}' não existe na matriz"
        )
    if transicao.estado_entrada is not None and transicao.estado_entrada != estado_atual:
        raise ErroDeTransicaoBibliografica(
            estado_atual,
            transicao.estado_saida,
            detalhe=(
                f"transição '{transicao_id}' exige estado_entrada="
                f"{transicao.estado_entrada.value}, estado atual é {estado_atual.value}"
            ),
        )
    return transicao.estado_saida

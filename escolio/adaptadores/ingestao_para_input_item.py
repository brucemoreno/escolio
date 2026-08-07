"""Adaptador: `DocumentoIngerido` (escolio/ingestao/) → `InputItem` (P09 §6).

Item 3 do roadmap, fecha `BL-003` (docs/backlog.md).

## Escopo

Este adaptador produz **um `InputItem` por documento ingerido**, não um por
unidade interna (parágrafo, seção, citação...). `InputItem` (P09 §6) modela
um item de entrada do envelope de runtime — o documento como um todo é o que
entra no sistema; parágrafos e citações são estrutura interna do documento,
já modelada por `DocumentoIngerido`, e não novos itens de entrada. Nenhuma
fonte (P09 §6, FORMATO.md) pede granularidade menor.

## `material_id` — apenas P19 §10, não `MaterialUnit` (P19 §9) inteiro

P19 §9 define `MaterialUnit` com 27 campos. A maioria (`owner_or_controller`,
`license_status`, `authorization_basis`, `authorized_purposes`,
`retention_class`, `audit_status`, `human_gate`, ...) exige decisão humana de
autorização que nenhum parser pode produzir — e P19 §71/§72/§73 proíbem
classificar material real fora do fluxo homologado com gates humanos
(`GATE_DE_ADMISSAO_DE_MATERIAL` etc.), fluxo que esta ação não executa.

O que P19 §10 define é somente a regra de identidade do `material_id`:
único no projeto, independente do nome do arquivo, estável entre cópias,
não reciclável, relacionável a versões. Essa regra é genérica e não exige
classificação — por isso este adaptador a implementa, via
`material_id_de_documento`, e para aí. Os outros 26 campos de `MaterialUnit`
ficam fora de escopo desta peça; ver LACUNAS.md.

`material_id` é anexado a `InputItem.provenance.integrity_reference` — único
campo de `Provenance` (P09 §6) com essa finalidade; `InputItem` não tem campo
`material_id` próprio, e a fonte não pede que se invente um. `input_id`
(P09 §6.1, "deve ser único") e `material_id` (P19 §10, "deve ser único no
projeto") são identificadores de espaços de nomes distintos, cada um exigido
por sua própria fonte — este adaptador não os funde num único valor, embora
ambos derivem do mesmo `hash_documento` para o mesmo documento.
"""

from escolio.contrato.entrada import (
    Classification,
    ContentConsistency,
    InputItem,
    Provenance,
)
from escolio.contrato.vocabulario import ConsistencyStatus, InputType
from escolio.ingestao.modelos import DocumentoIngerido


def material_id_de_documento(documento: DocumentoIngerido) -> str:
    """`material_id` [P19 §10] para o documento como um todo.

    Derivado de `hash_documento` (já determinístico e independente do nome
    do arquivo — ver escolio/ingestao/identificadores.py), não do
    `caminho_original`: a regra P19 §10 exige que o identificador "não
    dependa do nome do arquivo" e "permaneça estável entre cópias": duas
    cópias do mesmo PDF, em caminhos diferentes, têm o mesmo
    `hash_documento` e por isso o mesmo `material_id`.
    """
    return f"MAT-DOC-{documento.hash_documento}"


def input_item_de_documento(documento: DocumentoIngerido) -> InputItem:
    """Converte um `DocumentoIngerido` completo em um `InputItem` [P09 §6].

    Campos de `InputItem` deixados no padrão do dataclass (não preenchidos
    aqui) porque a ingestão não produz base para decidi-los sem inferência:

    - `authority` — permanece `has_operational_authority=False` [padrão
      §6.1]: conteúdo de documento nunca constitui autoridade operacional
      por si [P08 §2], e a ingestão não declara nenhuma base de autoridade.
    - `classification.trust`, `.sensitivity`, `.state`, `.functions` (além
      de `state`, ver abaixo) — exigem avaliação de confiabilidade,
      sensibilidade e função de destino que a ingestão não realiza; isso é
      trabalho de P19/roteador de função (roadmap, itens 4 e 6), não deste
      adaptador.
    - `processing`, `security`, `retention` — mesma razão: nenhum desses
      campos é derivável de `DocumentoIngerido` sem avaliação adicional.
    - `content_reference` — este adaptador não decide onde o arquivo fica
      persistido; fica com o valor padrão (`None`) e é responsabilidade de
      quem chama este adaptador preenchê-lo com o caminho real, se
      aplicável.
    """
    return InputItem(
        input_id=f"INP-{documento.hash_documento}",
        type=InputType.DOCUMENT,
        title=documento.metadados.titulo,
        provenance=Provenance(
            source=documento.caminho_original,
            source_type="DOCUMENTO_PDF",
            integrity_reference=material_id_de_documento(documento),
        ),
        content_consistency=ContentConsistency(status=ConsistencyStatus.NOT_APPLICABLE),
        classification=Classification(
            trust="NAO_AVALIADA",
            state="ORIGEM_DESCONHECIDA",
        ),
    )

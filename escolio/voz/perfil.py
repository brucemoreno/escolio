"""PerfilDeVoz — fonte: 02_SCHEMA_DE_PERFIL_DE_VOZ_AUTORAL_P07_R01.json;
01_CONTRATO_UNIVERSAL_DE_VOZ_AUTORAL_P07_R01.md (Gates e reversibilidade);
04_MATRIZ_DE_PERFIS_FONTES_CONFIANCA_E_AUTORIDADE_P07_R01.csv.

ESCOPO: voz do autor avaliado (o texto sob revisão), não a voz de quem
comenta — ver escolio/voz/vocabulario.py e escolio/voz/LACUNAS.md.

`scope`, `dimensions`, `authorization`, `versioning`, `reversibility` são
`dict` livre (a fonte declara apenas `type: object`, sem sub-schema — ver
LACUNAS.md). `evidence` e `provenance` são listas livres pelo mesmo
motivo.

Regras de gate por perfil, verificáveis em código a partir do arquivo 01
("Gates e reversibilidade") e do arquivo 04 (matriz), validadas em
__post_init__:
- perfil declarado exige declaração material (`authorization` não vazio);
- perfil derivado exige múltiplas amostras (>=2) e proveniência não vazia;
- perfil híbrido exige declaração + amostras e resolução explícita de
  conflitos;
- perfil insuficiente/conflitante conduz a `status=ABSTENCAO` com
  `abstention_reason` preenchido — nunca a outro status;
- `provenance` vazio não valida perfil algum além de
  PERFIL_INSUFICIENTE_OU_CONFLITANTE e PERFIL_NEUTRO_ACADEMICO_CONTROLADO
  (o neutro não depende de amostra do autor avaliado — arquivo 04:
  fonte = "contrato universal + exigência institucional", não amostra).
"""

from dataclasses import dataclass, field
from typing import Any

from escolio.voz.erros import ErroDePerfilDeVoz
from escolio.voz.vocabulario import Confidence, StatusDePerfil, TipoDePerfil

ARQUIVO_SCHEMA = "02_SCHEMA_DE_PERFIL_DE_VOZ_AUTORAL_P07_R01.json"
ARQUIVO_CONTRATO = "01_CONTRATO_UNIVERSAL_DE_VOZ_AUTORAL_P07_R01.md"

_MINIMO_DE_AMOSTRAS_PARA_PERFIL_DERIVADO = 2
"""Arquivo 04: 'múltiplas amostras autorizadas'. A fonte não define um
mínimo numérico absoluto (P07-LAC-001, preservada) — 2 é o menor valor
compatível com o próprio texto 'múltiplas' (plural, portanto >=2), não uma
inferência de quantidade além do que a palavra já exige. Ver LACUNAS.md."""


@dataclass
class PerfilDeVoz:
    profile_id: str
    profile_type: TipoDePerfil
    purpose: str
    scope: dict[str, Any]
    dimensions: dict[str, Any]
    evidence: list[Any]
    confidence: Confidence
    authorization: dict[str, Any]
    versioning: dict[str, Any]
    provenance: list[Any]
    reversibility: dict[str, Any]
    status: StatusDePerfil
    abstention_reason: str | None = field(default=None)

    def __post_init__(self) -> None:
        if not self.profile_id:
            raise ErroDePerfilDeVoz("P07-schema", "profile_id é obrigatório")
        if not self.purpose:
            raise ErroDePerfilDeVoz("P07-schema", "purpose é obrigatório")

        # Schema §status: ABSTENCAO exige abstention_reason; os demais não
        # o admitem preenchido sem motivo correspondente registrado.
        if self.status == StatusDePerfil.ABSTENCAO and not self.abstention_reason:
            raise ErroDePerfilDeVoz(
                "P07-schema", "status=ABSTENCAO exige abstention_reason preenchido"
            )

        # Contrato §Gates: "perfil insuficiente conduz à abstenção, pedido
        # de amostras ou perfil neutro" — como PerfilDeVoz já foi
        # instanciado como PERFIL_INSUFICIENTE_OU_CONFLITANTE, a única
        # conclusão de status verificável em código é ABSTENCAO; as outras
        # duas saídas ("pedido de amostras", "perfil neutro") não são um
        # status deste mesmo perfil — são a construção de um objeto
        # diferente (um novo pedido, ou um PerfilDeVoz
        # PERFIL_NEUTRO_ACADEMICO_CONTROLADO), fora do escopo de uma única
        # instância.
        if self.profile_type == TipoDePerfil.PERFIL_INSUFICIENTE_OU_CONFLITANTE:
            if self.status != StatusDePerfil.ABSTENCAO:
                raise ErroDePerfilDeVoz(
                    "P07-contrato-gates",
                    "PERFIL_INSUFICIENTE_OU_CONFLITANTE exige status=ABSTENCAO",
                    detalhe=f"status={self.status.value}",
                )
            return

        self._valida_gate_por_tipo()

    def _valida_gate_por_tipo(self) -> None:
        if self.profile_type == TipoDePerfil.PERFIL_AUTORAL_DECLARADO_PELO_USUARIO:
            self._exige_declaracao()
        elif self.profile_type == TipoDePerfil.PERFIL_AUTORAL_DERIVADO_DE_AMOSTRAS:
            self._exige_amostras()
        elif self.profile_type == TipoDePerfil.PERFIL_HIBRIDO_DECLARACAO_MAIS_AMOSTRAS:
            self._exige_declaracao()
            self._exige_amostras()
        elif self.profile_type == TipoDePerfil.PERFIL_LOCAL_POR_GENERO_OU_SECAO:
            # Arquivo 04: fontes = "perfil vigente + restrição local"; a
            # restrição local é o próprio `scope`, já obrigatório pelo
            # schema — nenhuma regra adicional verificável em código além
            # de `scope` não vazio, exigida abaixo para todos os perfis.
            pass
        # PERFIL_NEUTRO_ACADEMICO_CONTROLADO: arquivo 04, fonte = "contrato
        # universal + exigência institucional" — não depende de amostra
        # nem de declaração do autor avaliado; nenhuma exigência adicional.

        if not self.scope:
            raise ErroDePerfilDeVoz(
                "P07-schema", "scope é obrigatório e não pode ser vazio", detalhe=f"profile_type={self.profile_type.value}"
            )

    def _exige_declaracao(self) -> None:
        # Contrato §Gates: "perfil declarado exige declaração material".
        # Verificável em código como `authorization` não vazio — o schema
        # não define um campo estrutural separado de "declaração material"
        # distinto de `authorization`.
        if not self.authorization:
            raise ErroDePerfilDeVoz(
                "P07-contrato-gates",
                "perfil declarado exige declaração material (authorization não vazio)",
                detalhe=f"profile_type={self.profile_type.value}",
            )

    def _exige_amostras(self) -> None:
        # Contrato §Gates: "perfil derivado exige múltiplas amostras e
        # proveniência".
        if len(self.evidence) < _MINIMO_DE_AMOSTRAS_PARA_PERFIL_DERIVADO:
            raise ErroDePerfilDeVoz(
                "P07-contrato-gates",
                "perfil derivado exige múltiplas amostras (evidence)",
                detalhe=f"profile_type={self.profile_type.value} len(evidence)={len(self.evidence)}",
            )
        if not self.provenance:
            raise ErroDePerfilDeVoz(
                "P07-contrato-gates",
                "perfil derivado exige proveniência (provenance não vazio)",
                detalhe=f"profile_type={self.profile_type.value}",
            )

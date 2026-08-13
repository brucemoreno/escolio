"""Amostra autoral e resultado de derivação de perfil — fonte:
01_CONTRATO_UNIVERSAL_DE_VOZ_AUTORAL_P07_R01.md (Gates: "perfil derivado
exige múltiplas amostras e proveniência"; "perfil insuficiente conduz à
abstenção, pedido de amostras ou perfil neutro").

Decisão do professor, sessão de 2026-08-13: qual documento serve de
amostra para derivar o `PerfilDeVoz` de um autor não é decisão deste
módulo nem de `escolio/funcoes/ponte_modelo_p13.py` — nenhuma fonte
designa um corpus de amostras (verificado contra `corpus/`, nada alem dos
próprios arquivos do pacote P07), e fixar isso em código seria a mesma
inferência silenciosa que CLAUDE.md §11 proíbe. `AmostraAutoral` aceita
qualquer texto que quem chama já tenha decidido ser amostra; a escolha do
documento fica com quem opera o piloto.
"""

from __future__ import annotations

from dataclasses import dataclass

from escolio.voz.dimensoes import DimensaoDeVoz
from escolio.voz.erros import ErroDePerfilDeVoz


@dataclass(frozen=True)
class AmostraAutoral:
    amostra_id: str
    texto: str
    provenance: str
    """Origem declarada da amostra — `[acervo:arquivo]`, `[diff:capítulo]`
    etc. [CLAUDE.md §9]. Nunca inferida aqui; quem monta a amostra decide
    o rótulo."""

    def __post_init__(self) -> None:
        if not self.amostra_id:
            raise ErroDePerfilDeVoz("P07-amostra", "amostra_id é obrigatório")
        if not self.texto:
            raise ErroDePerfilDeVoz("P07-amostra", "texto é obrigatório")
        if not self.provenance:
            raise ErroDePerfilDeVoz("P07-amostra", "provenance é obrigatório")


@dataclass(frozen=True)
class SolicitacaoDeAmostrasAdicionais:
    """"Perfil insuficiente conduz a... pedido de amostras" [01, Gates] —
    a saída explícita quando as amostras fornecidas não bastam para cobrir
    com evidência real as dimensões obrigatórias do P07. Nunca um
    `PerfilDeVoz` com dimensão inventada; ver escolio/voz/LACUNAS.md."""

    dimensoes_sem_evidencia: tuple[DimensaoDeVoz, ...]
    motivos: dict[str, str]
    amostras_recebidas: int

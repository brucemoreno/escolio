"""Vocabulário controlado da máquina de estados bibliográficos — fonte:
03_MAQUINA_DE_ESTADOS_BIBLIOGRAFICOS_P04_R01.csv (17 estados).

Vocabulário próprio desta máquina, distinto de:
- `escolio.vocabulario.AccessState/ReadingState/ValidationState` (P05, 3
  campos paralelos de `RelacaoAfirmacaoEvidencia`, não uma máquina única);
- os 9 estados mínimos de R03 CAMADA D.

Nenhum dos três é alias do outro — mesma disciplina dada a CON-P05-001 em
`escolio/vocabulario.py` e `escolio/contrato/vocabulario.py`. Ver
`escolio/bvaa/correspondencia.py` para a tabela de correspondência
(não um enum fundido) e `escolio/bvaa/LACUNAS.md`.
"""

from enum import Enum

ARQUIVO_MAQUINA_DE_ESTADOS = "03_MAQUINA_DE_ESTADOS_BIBLIOGRAFICOS_P04_R01.csv"
ARQUIVO_MATRIZ_TRANSICOES = "04_MATRIZ_DE_LEITURA_LOCALIZACAO_VALIDACAO_E_RECOMENDACAO_P04_R01.csv"


class EstadoBibliografico(str, Enum):
    """17 estados, na ordem exata do CSV — nenhum estado renomeado,
    fundido ou reordenado."""

    OBRA_NAO_IDENTIFICADA = "OBRA_NAO_IDENTIFICADA"
    OBRA_IDENTIFICADA = "OBRA_IDENTIFICADA"
    EDICAO_IDENTIFICADA = "EDICAO_IDENTIFICADA"
    LOCALIZADA = "LOCALIZADA"
    ACESSIVEL = "ACESSIVEL"
    ACESSADA = "ACESSADA"
    LEITURA_NAO_REALIZADA = "LEITURA_NAO_REALIZADA"
    LEITURA_INDIRETA = "LEITURA_INDIRETA"
    LEITURA_PARCIAL = "LEITURA_PARCIAL"
    LEITURA_INTEGRAL = "LEITURA_INTEGRAL"
    PAGINA_NAO_CONFIRMADA = "PAGINA_NAO_CONFIRMADA"
    PAGINA_CONFIRMADA = "PAGINA_CONFIRMADA"
    VALIDACAO_PENDENTE = "VALIDACAO_PENDENTE"
    VALIDADA = "VALIDADA"
    RECOMENDACAO_CONDICIONAL = "RECOMENDACAO_CONDICIONAL"
    RECOMENDADA = "RECOMENDADA"
    ABSTENCAO_BIBLIOGRAFICA = "ABSTENCAO_BIBLIOGRAFICA"


class NivelDeEvidencia(str, Enum):
    """Matriz de evidência — fonte: 02_PROTOCOLO_BVAA_UNIVERSAL_P04_R01.md §4.

    Vocabulário próprio desta máquina; não é o mesmo enum que
    `escolio.vocabulario.EvidenceLevel` (P05) — rótulos parecidos (A/B/C/D),
    mas fontes e cardinalidades distintas; nenhuma fusão feita aqui.
    """

    A_INTERNA_FORNECIDA = "A_INTERNA_FORNECIDA"
    B_MATERIAL_ANEXADA = "B_MATERIAL_ANEXADA"
    C_FERRAMENTA_RASTREAVEL = "C_FERRAMENTA_RASTREAVEL"
    D_AUSENTE = "D_AUSENTE"

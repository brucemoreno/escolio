"""Relatório de ingestão — contagens e indeterminados, conforme o
prompt: "é como se mede a qualidade do parser sem ler o documento
inteiro"."""

from dataclasses import dataclass, field

from escolio.ingestao.modelos import DocumentoIngerido


@dataclass
class RelatorioDeIngestao:
    num_paginas: int
    num_secoes: int
    num_secoes_indeterminadas: int
    num_paragrafos: int
    num_notas_de_rodape: int
    num_notas_sem_chamada_correspondente: int
    num_citacoes_recuadas: int
    num_citacoes_no_corpo: int
    num_citacoes_no_corpo_indeterminadas: int
    num_referencias: int
    num_figuras_tabelas: int
    num_figuras_tabelas_indeterminadas: int
    num_hifens_de_fim_de_linha_preservados: int

    def total_indeterminados(self) -> int:
        return (
            self.num_secoes_indeterminadas
            + self.num_notas_sem_chamada_correspondente
            + self.num_citacoes_no_corpo_indeterminadas
            + self.num_figuras_tabelas_indeterminadas
        )

    def como_dict(self) -> dict:
        d = {
            "num_paginas": self.num_paginas,
            "num_secoes": self.num_secoes,
            "num_secoes_indeterminadas": self.num_secoes_indeterminadas,
            "num_paragrafos": self.num_paragrafos,
            "num_notas_de_rodape": self.num_notas_de_rodape,
            "num_notas_sem_chamada_correspondente": self.num_notas_sem_chamada_correspondente,
            "num_citacoes_recuadas": self.num_citacoes_recuadas,
            "num_citacoes_no_corpo": self.num_citacoes_no_corpo,
            "num_citacoes_no_corpo_indeterminadas": self.num_citacoes_no_corpo_indeterminadas,
            "num_referencias": self.num_referencias,
            "num_figuras_tabelas": self.num_figuras_tabelas,
            "num_figuras_tabelas_indeterminadas": self.num_figuras_tabelas_indeterminadas,
            "num_hifens_de_fim_de_linha_preservados": self.num_hifens_de_fim_de_linha_preservados,
            "total_indeterminados": self.total_indeterminados(),
        }
        return d


def construir_relatorio(doc: DocumentoIngerido) -> RelatorioDeIngestao:
    return RelatorioDeIngestao(
        num_paginas=doc.num_paginas,
        num_secoes=len(doc.secoes),
        num_secoes_indeterminadas=sum(1 for s in doc.secoes if s.indeterminado),
        num_paragrafos=len(doc.paragrafos),
        num_notas_de_rodape=len(doc.notas_de_rodape),
        num_notas_sem_chamada_correspondente=sum(
            1 for n in doc.notas_de_rodape if n.indeterminado
        ),
        num_citacoes_recuadas=len(doc.citacoes_recuadas),
        num_citacoes_no_corpo=len(doc.citacoes_no_corpo),
        num_citacoes_no_corpo_indeterminadas=sum(
            1 for c in doc.citacoes_no_corpo if c.indeterminado
        ),
        num_referencias=len(doc.referencias),
        num_figuras_tabelas=len(doc.figuras),
        num_figuras_tabelas_indeterminadas=sum(1 for f in doc.figuras if f.indeterminado),
        num_hifens_de_fim_de_linha_preservados=doc.hifens_de_fim_de_linha_preservados,
    )

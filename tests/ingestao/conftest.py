from pathlib import Path

import pytest

from escolio.ingestao.parser import parse_pdf

CAMINHO_PDF_DEV = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "dev"
    / "Relatorio_Final_PIBIC-Bolsa-CNPq-e-UEM - Ricardo Antonio Esteves dos Santos.pdf"
)


def _pdf_dev_disponivel() -> bool:
    return CAMINHO_PDF_DEV.exists()


requer_pdf_dev = pytest.mark.skipif(
    not _pdf_dev_disponivel(),
    reason="PDF de desenvolvimento não encontrado em data/dev/ — testes de ingestão pulados",
)


@pytest.fixture(scope="session")
def caminho_pdf_dev() -> str:
    return str(CAMINHO_PDF_DEV)


@pytest.fixture(scope="session")
def documento(caminho_pdf_dev):
    """Documento processado uma vez por sessão de teste — o parsing de
    um PDF de 33 páginas não é instantâneo; reprocessar por teste seria
    custo sem benefício, já que os testes só leem o resultado."""
    return parse_pdf(caminho_pdf_dev)

from pathlib import Path

import pytest

from escolio.ingestao.parser import parse_pdf
from escolio.ingestao.parser_docx import parse_docx

DIR_CAPITULOS_DOCX = Path(__file__).resolve().parent.parent.parent / "data" / "capitulos"

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


def _caminhos_capitulos_docx() -> list[Path]:
    if not DIR_CAPITULOS_DOCX.is_dir():
        return []
    return sorted(DIR_CAPITULOS_DOCX.glob("*.docx"))


requer_capitulos_docx = pytest.mark.skipif(
    not _caminhos_capitulos_docx(),
    reason="capítulos .docx não encontrados em data/capitulos/ — testes do parser de .docx pulados",
)


@pytest.fixture(scope="session")
def caminhos_capitulos_docx() -> list[str]:
    return [str(c) for c in _caminhos_capitulos_docx()]


@pytest.fixture(scope="session")
def documentos_capitulos_docx(caminhos_capitulos_docx):
    """Um DocumentoIngerido por capítulo real, processado uma vez por
    sessão — mesmo raciocínio de custo do fixture `documento` (PDF)."""
    return [parse_docx(c) for c in caminhos_capitulos_docx]

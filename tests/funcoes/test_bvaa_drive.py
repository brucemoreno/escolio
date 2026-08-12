"""Testes de `escolio/funcoes/bvaa_drive.py` — ligação entre evidência real
de acesso ao Drive e a máquina bibliográfica do P04 (BVAA).

Drive mockado em todos os testes [instrução da sessão] — nenhuma chamada de
rede. O `ArquivoDrive` usado como evidência vem do retorno real (mockado)
de `escolio.drive.conector.listar_arquivos_da_pasta`/`baixar_arquivo`, não
construído à mão, para exercitar a integração ponta a ponta com o
conector."""

from unittest.mock import MagicMock

import pytest

from escolio.bvaa.erros import ErroDeTransicaoBibliografica
from escolio.bvaa.vocabulario import EstadoBibliografico
from escolio.drive.conector import ArquivoDrive, baixar_arquivo, listar_arquivos_da_pasta
from escolio.funcoes.bvaa_drive import (
    ErroDeEvidenciaDeAcesso,
    EvidenciaDeAcessoDrive,
    OperacaoDeAcesso,
    avancar_por_evidencia,
    transicao_licenciada_por,
)


def _servico_de_listagem(paginas: list[dict]):
    servico = MagicMock()
    execucoes = iter(paginas)
    servico.files.return_value.list.return_value.execute.side_effect = lambda: next(execucoes)
    return servico


def test_evidencia_localizado_via_listagem_real_mockada():
    servico = _servico_de_listagem(
        [
            {
                "files": [
                    {
                        "id": "abc123",
                        "name": "Grewe1979.pdf",
                        "mimeType": "application/pdf",
                        "size": "2048",
                        "modifiedTime": "2026-01-01T00:00:00Z",
                    }
                ]
            }
        ]
    )
    arquivos = listar_arquivos_da_pasta(servico, "pasta-biblioteca")
    evidencia = EvidenciaDeAcessoDrive(arquivo=arquivos[0], operacao=OperacaoDeAcesso.LOCALIZADO)

    assert transicao_licenciada_por(evidencia) == "T04"


def test_evidencia_baixado_via_download_real_mockado(tmp_path, monkeypatch):
    servico = MagicMock()
    arquivo = ArquivoDrive(
        id="abc123", nome="Grewe1979.pdf", mime_type="application/pdf",
        tamanho_bytes=2048, modificado_em="2026-01-01T00:00:00Z",
    )
    monkeypatch.setattr(
        "escolio.drive.conector.MediaIoBaseDownload",
        lambda *a, **k: MagicMock(next_chunk=MagicMock(return_value=(MagicMock(), True))),
    )
    destino = baixar_arquivo(servico, arquivo, tmp_path / "grewe.pdf")
    evidencia = EvidenciaDeAcessoDrive(
        arquivo=arquivo, operacao=OperacaoDeAcesso.BAIXADO, caminho_local=destino
    )

    assert transicao_licenciada_por(evidencia) == "T05"


def test_evidencia_baixado_sem_caminho_local_levanta():
    arquivo = ArquivoDrive(id="x", nome="x.pdf", mime_type="application/pdf", tamanho_bytes=1, modificado_em=None)
    with pytest.raises(ErroDeEvidenciaDeAcesso):
        EvidenciaDeAcessoDrive(arquivo=arquivo, operacao=OperacaoDeAcesso.BAIXADO)


def test_evidencia_exportado_sem_caminho_local_levanta():
    arquivo = ArquivoDrive(id="x", nome="x.pdf", mime_type="application/pdf", tamanho_bytes=1, modificado_em=None)
    with pytest.raises(ErroDeEvidenciaDeAcesso):
        EvidenciaDeAcessoDrive(arquivo=arquivo, operacao=OperacaoDeAcesso.EXPORTADO)


def test_evidencia_localizado_com_caminho_local_levanta():
    arquivo = ArquivoDrive(id="x", nome="x.pdf", mime_type="application/pdf", tamanho_bytes=1, modificado_em=None)
    with pytest.raises(ErroDeEvidenciaDeAcesso):
        EvidenciaDeAcessoDrive(
            arquivo=arquivo, operacao=OperacaoDeAcesso.LOCALIZADO, caminho_local="qualquer/coisa"
        )


def test_avancar_por_evidencia_localizado_a_partir_de_localizada():
    arquivo = ArquivoDrive(id="x", nome="x.pdf", mime_type="application/pdf", tamanho_bytes=1, modificado_em=None)
    evidencia = EvidenciaDeAcessoDrive(arquivo=arquivo, operacao=OperacaoDeAcesso.LOCALIZADO)

    resultado = avancar_por_evidencia(EstadoBibliografico.LOCALIZADA, evidencia)

    assert resultado.estado_anterior is EstadoBibliografico.LOCALIZADA
    assert resultado.estado_novo is EstadoBibliografico.ACESSIVEL
    assert resultado.transicao_id == "T04"


def test_avancar_por_evidencia_baixado_a_partir_de_acessivel(tmp_path):
    arquivo = ArquivoDrive(id="x", nome="x.pdf", mime_type="application/pdf", tamanho_bytes=1, modificado_em=None)
    caminho = tmp_path / "x.pdf"
    caminho.write_bytes(b"conteudo")
    evidencia = EvidenciaDeAcessoDrive(
        arquivo=arquivo, operacao=OperacaoDeAcesso.BAIXADO, caminho_local=caminho
    )

    resultado = avancar_por_evidencia(EstadoBibliografico.ACESSIVEL, evidencia)

    assert resultado.estado_novo is EstadoBibliografico.ACESSADA
    assert resultado.transicao_id == "T05"


def test_avancar_por_evidencia_exportado_a_partir_de_acessivel(tmp_path):
    arquivo = ArquivoDrive(id="x", nome="x.docx", mime_type="application/vnd.google-apps.document",
                            tamanho_bytes=1, modificado_em=None)
    caminho = tmp_path / "x.pdf"
    caminho.write_bytes(b"conteudo")
    evidencia = EvidenciaDeAcessoDrive(
        arquivo=arquivo, operacao=OperacaoDeAcesso.EXPORTADO, caminho_local=caminho
    )

    resultado = avancar_por_evidencia(EstadoBibliografico.ACESSIVEL, evidencia)

    assert resultado.estado_novo is EstadoBibliografico.ACESSADA


def test_avancar_por_evidencia_localizado_a_partir_de_obra_nao_identificada_levanta():
    """T04 exige estado_entrada=LOCALIZADA — Drive não comprova
    identificação de obra/edição (T01-T03); a evidência de acesso não
    licencia nada a partir do estado inicial, e este módulo não disfarça
    isso como sucesso parcial."""
    arquivo = ArquivoDrive(id="x", nome="x.pdf", mime_type="application/pdf", tamanho_bytes=1, modificado_em=None)
    evidencia = EvidenciaDeAcessoDrive(arquivo=arquivo, operacao=OperacaoDeAcesso.LOCALIZADO)

    with pytest.raises(ErroDeTransicaoBibliografica):
        avancar_por_evidencia(EstadoBibliografico.OBRA_NAO_IDENTIFICADA, evidencia)


def test_avancar_por_evidencia_baixado_a_partir_de_localizada_levanta():
    """T05 exige estado_entrada=ACESSIVEL, não LOCALIZADA — download sem
    passar por T04 primeiro não licencia T05."""
    arquivo = ArquivoDrive(id="x", nome="x.pdf", mime_type="application/pdf", tamanho_bytes=1, modificado_em=None)
    evidencia = EvidenciaDeAcessoDrive(
        arquivo=arquivo, operacao=OperacaoDeAcesso.BAIXADO, caminho_local="qualquer.pdf"
    )

    with pytest.raises(ErroDeTransicaoBibliografica):
        avancar_por_evidencia(EstadoBibliografico.LOCALIZADA, evidencia)

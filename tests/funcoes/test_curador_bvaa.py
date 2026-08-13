"""Testes de `escolio/funcoes/curador_bvaa.py` — curador automático de
evidência bibliográfica (sessão de 2026-08-13, decisão do
`USUARIO_PROPONENTE`).

Drive mockado em todos os testes, mesmo padrão de `test_bvaa_drive.py` —
nenhuma chamada de rede real. `data/capitulos/` real não tem referência
alguma a testar contra (LAC-ING-017); os `ItemDeReferencia` usados aqui
são sintéticos."""

from unittest.mock import MagicMock

from escolio.bvaa.abstencao import GatilhoDeAbstencao
from escolio.drive.erros import ErroDeAcessoNegado, ErroDeRecursoNaoEncontrado
from escolio.funcoes.bvaa_drive import OperacaoDeAcesso
from escolio.funcoes.curador_bvaa import curar_referencias
from escolio.ingestao.modelos import ItemDeReferencia


def _servico_de_busca(paginas: list[dict]):
    servico = MagicMock()
    execucoes = iter(paginas)
    servico.files.return_value.list.return_value.execute.side_effect = lambda: next(execucoes)
    return servico


def _referencia(unit_id="UNI-REF-0001", texto="GREWE, R. Fonte sintética. São Paulo: Editora X, 1979."):
    return ItemDeReferencia(unit_id=unit_id, texto=texto, pagina=None)


def test_referencia_sem_autor_nem_ano_escala_sem_chamar_drive():
    servico = MagicMock()
    referencia = _referencia(texto="referência sem nenhum dado reconhecível")

    resultado = curar_referencias([referencia], servico)

    assert resultado.evidencias_de_identificacao == {}
    assert resultado.evidencias_de_acesso == {}
    assert len(resultado.escalonamentos) == 1
    escalonamento = resultado.escalonamentos[0]
    assert escalonamento.unit_id == referencia.unit_id
    assert escalonamento.motivo is GatilhoDeAbstencao.OBRA_OU_EDICAO_NAO_IDENTIFICADA
    servico.files.assert_not_called()


def test_busca_sem_resultado_escala_acesso_nao_comprovado():
    servico = _servico_de_busca([{"files": []}])
    referencia = _referencia()

    resultado = curar_referencias([referencia], servico)

    assert resultado.evidencias_de_identificacao == {}
    assert len(resultado.escalonamentos) == 1
    assert resultado.escalonamentos[0].motivo is GatilhoDeAbstencao.ACESSO_NAO_COMPROVADO
    assert "GREWE 1979" in resultado.escalonamentos[0].detalhe


def test_erro_do_conector_na_busca_escala_acesso_nao_comprovado():
    servico = MagicMock()
    servico.files.return_value.list.return_value.execute.side_effect = lambda: (_ for _ in ()).throw(
        ErroDeAcessoNegado("pasta-x")
    )
    referencia = _referencia()

    resultado = curar_referencias([referencia], servico)

    assert len(resultado.escalonamentos) == 1
    assert resultado.escalonamentos[0].motivo is GatilhoDeAbstencao.ACESSO_NAO_COMPROVADO
    assert "ACESSO_NEGADO" in resultado.escalonamentos[0].detalhe


def test_busca_com_resultado_produz_identificacao_e_tenta_acesso(tmp_path, monkeypatch):
    servico = _servico_de_busca(
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
    monkeypatch.setattr(
        "escolio.drive.conector.MediaIoBaseDownload",
        lambda *a, **k: MagicMock(next_chunk=MagicMock(return_value=(MagicMock(), True))),
    )
    referencia = _referencia()

    resultado = curar_referencias([referencia], servico, diretorio_cache=tmp_path)

    assert referencia.unit_id in resultado.evidencias_de_identificacao
    evidencia_id = resultado.evidencias_de_identificacao[referencia.unit_id]
    assert evidencia_id.arquivo.nome == "Grewe1979.pdf"
    assert evidencia_id.referencia_citada == referencia.texto

    evidencia_acesso = resultado.evidencias_de_acesso[referencia.unit_id]
    assert evidencia_acesso.operacao is OperacaoDeAcesso.BAIXADO
    assert evidencia_acesso.caminho_local is not None
    assert resultado.escalonamentos == []


def test_localizado_mas_download_falha_preserva_localizacao_e_escala_so_o_acesso():
    servico = _servico_de_busca(
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
    servico.files.return_value.get_media.side_effect = lambda **k: (_ for _ in ()).throw(
        ErroDeRecursoNaoEncontrado("abc123")
    )
    referencia = _referencia()

    resultado = curar_referencias([referencia], servico)

    # T01-T03 avançaram (identificação encontrada por busca) mesmo com o
    # download falhando — progresso real preservado, não descartado.
    assert referencia.unit_id in resultado.evidencias_de_identificacao
    evidencia_acesso = resultado.evidencias_de_acesso[referencia.unit_id]
    assert evidencia_acesso.operacao is OperacaoDeAcesso.LOCALIZADO
    assert evidencia_acesso.caminho_local is None

    assert len(resultado.escalonamentos) == 1
    assert resultado.escalonamentos[0].motivo is GatilhoDeAbstencao.ACESSO_NAO_COMPROVADO
    assert "download/exportação falhou" in resultado.escalonamentos[0].detalhe


def test_metadados_extraidos_ficam_registrados_por_unit_id_mesmo_sem_evidencia():
    servico = _servico_de_busca([{"files": []}])
    referencia = _referencia()

    resultado = curar_referencias([referencia], servico)

    assert referencia.unit_id in resultado.metadados_extraidos
    assert resultado.metadados_extraidos[referencia.unit_id].ano == "1979"


def test_multiplas_referencias_independentes_uma_falha_nao_bloqueia_outra(monkeypatch):
    servico = _servico_de_busca([{"files": []}, {"files": [
        {
            "id": "abc123", "name": "Grewe1979.pdf", "mimeType": "application/pdf",
            "size": "2048", "modifiedTime": None,
        }
    ]}])
    monkeypatch.setattr(
        "escolio.drive.conector.MediaIoBaseDownload",
        lambda *a, **k: MagicMock(next_chunk=MagicMock(return_value=(MagicMock(), True))),
    )
    ref_sem_resultado = _referencia(unit_id="UNI-REF-0001")
    ref_com_resultado = _referencia(unit_id="UNI-REF-0002", texto="SILVA, J. Outra obra. Rio: Y, 2005.")

    resultado = curar_referencias([ref_sem_resultado, ref_com_resultado], servico)

    assert "UNI-REF-0001" not in resultado.evidencias_de_identificacao
    assert "UNI-REF-0002" in resultado.evidencias_de_identificacao
    assert len(resultado.escalonamentos) == 1
    assert resultado.escalonamentos[0].unit_id == "UNI-REF-0001"

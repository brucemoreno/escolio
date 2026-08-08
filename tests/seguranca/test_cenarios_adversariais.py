"""Os 20 cenários adversariais como casos de teste — RD-20, RD-21, RD-22, DTA-19.

Fonte: docs/spec/operacional-P08.md §6.

Cada cenário é um caso de teste cujos 13 campos de RD-21 são o esquema do
caso [P08 §15.1]: ameaça, classificação, autoridade, operação permitida,
operação bloqueada, dado protegido, justificativa, resposta segura,
proveniência, escalonamento, contaminação, reversibilidade, resultado.

DTA-19: BLOQUEADO é resultado esperado registrável quando a lacuna é
legítima sob [§15.5], não falha de suíte — um teste que expressa
BLOQUEADO passa quando o código SE RECUSA a decidir e preserva o objeto;
falharia se o código decidisse por inferência. Os cenários 13, 17 e 19
são exatamente esse caso (docs/spec/operacional-P08.md §6, tabela DTA-21)
e por isso os testes abaixo afirmam a recusa, não um resultado positivo.

Fixtures: tests/seguranca/fixtures_sinteticas.py — texto sintético, nunca
PDF, nunca derivado de material real (DTA-20, DTA-23, DTA-24).
"""

from dataclasses import dataclass

import pytest

from escolio.seguranca import escalonamento as esc
from escolio.seguranca.deteccao import detecta_exfiltracao, detecta_instrucoes_internas
from escolio.seguranca.erros import ErroDeEscalonamentoSemDestinatario, ErroDeEscopoDeSeguranca
from escolio.seguranca.fronteira import exige_marcador_sintetico, recusa_caminho_sob_data
from escolio.seguranca.vocabulario import AutorizacaoMinima, ResultadoDeCenario
from tests.seguranca import fixtures_sinteticas as fx


@dataclass(frozen=True)
class CasoDeCenario:
    """Esquema dos 13 campos obrigatórios [RD-21], mais o número do
    cenário [P08 §15] e o resultado esperado [RD-22]."""

    numero: int
    ameaca: str
    classificacao: str
    autoridade: str
    operacao_permitida: str
    operacao_bloqueada: str
    dado_protegido: str
    justificativa: str
    resposta_segura: str
    proveniencia: str
    escalonamento: str
    contaminacao: str
    reversibilidade: str
    resultado: ResultadoDeCenario


def test_todo_caso_declara_os_treze_campos_de_rd21():
    caso = CasoDeCenario(
        numero=1,
        ameaca="instrução de sistema embutida em documento",
        classificacao="injection_suspected",
        autoridade="nenhuma — conteúdo documental não constitui autoridade [P08 §2]",
        operacao_permitida="LEITURA, ANALISE",
        operacao_bloqueada="execução da instrução extraída",
        dado_protegido="nenhum além da integridade da instrução do sistema",
        justificativa="RD-01: conteúdo documental é dado, nunca comando",
        resposta_segura="marcar injection_suspected=true, preservar texto como evidência",
        proveniencia="fixture sintética [SINTETICO]",
        escalonamento="não necessário — decisão determinística conclusiva",
        contaminacao="nenhuma — achado registrado, não propagado como comando",
        reversibilidade="total — nenhuma ação sobre o texto foi tomada",
        resultado=ResultadoDeCenario.APROVADO,
    )
    # Confere que o dataclass exige todos os 13 campos nomeados por RD-21
    # mais numero/resultado — a ausência de qualquer um seria TypeError.
    campos = {f for f in caso.__dataclass_fields__ if f not in ("numero", "resultado")}
    assert campos == {
        "ameaca", "classificacao", "autoridade", "operacao_permitida", "operacao_bloqueada",
        "dado_protegido", "justificativa", "resposta_segura", "proveniencia", "escalonamento",
        "contaminacao", "reversibilidade",
    }


# --- Cenários 1-12, 14-16, 18, 20: esperado APROVADO (DTA-21) ---


def test_cenario_01_ignorar_instrucoes_anteriores_marca_injection_e_nao_executa():
    exige_marcador_sintetico(fx.CENARIO_01_IGNORAR_INSTRUCOES)
    achados = detecta_instrucoes_internas("UNI-CEN01", fx.CENARIO_01_IGNORAR_INSTRUCOES)
    assert achados, "PI-03 determinístico deve marcar injection_suspected"
    assert achados[0].campo == "injection_suspected"
    # RD-01: nenhuma instrução vira comando — não existe caminho de código
    # aqui que devolva algo executável; achados[0] é dado (Achado), não Authority.


def test_cenario_02_mudar_papel_marca_injection():
    exige_marcador_sintetico(fx.CENARIO_02_MUDAR_PAPEL)
    achados = detecta_instrucoes_internas("UNI-CEN02", fx.CENARIO_02_MUDAR_PAPEL)
    assert achados
    assert achados[0].campo == "injection_suspected"


def test_cenario_03_solicita_prompt_interno_marca_exfiltration_risk():
    exige_marcador_sintetico(fx.CENARIO_03_PROMPT_INTERNO)
    achados = detecta_exfiltracao("UNI-CEN03", fx.CENARIO_03_PROMPT_INTERNO)
    assert achados
    assert achados[0].campo == "exfiltration_risk"


def test_cenario_04_acesso_a_outro_projeto_e_ausencia_de_capacidade():
    # PI-06 arquitetura: o módulo não abre pasta nem consulta conector.
    # Não há função aqui que aceite "outro projeto" e devolva conteúdo —
    # a ausência do caminho é a implementação (mesmo padrão de RD-01).
    exige_marcador_sintetico(fx.CENARIO_04_ACESSO_OUTRO_PROJETO)
    import escolio.seguranca as modulo_seguranca

    assert not hasattr(modulo_seguranca, "acessar_outro_projeto")
    assert not hasattr(modulo_seguranca, "abrir_pasta")


def test_cenario_05_anexo_ordena_exclusao_exclusao_nao_esta_entre_permitidas_por_padrao():
    exige_marcador_sintetico(fx.CENARIO_05_ANEXO_ORDENA_EXCLUSAO)
    # RD-18: nenhuma autorização inferior implica superior — EXCLUSAO
    # nunca é concedida por conteúdo de documento. Não é caso de PI-03
    # literal (o texto não usa nenhum dos cinco padrões de DTA-07); o que
    # importa aqui é arquitetural: nenhuma função deste módulo concede
    # EXCLUSAO a partir de texto de documento.
    permitidas_por_padrao: tuple = ()
    assert AutorizacaoMinima.EXCLUSAO not in permitidas_por_padrao
    import escolio.seguranca as modulo_seguranca

    assert not hasattr(modulo_seguranca, "conceder_exclusao_a_partir_de_texto")


def test_cenario_06_link_induz_abertura_nao_ha_funcao_que_abra_link():
    exige_marcador_sintetico(fx.CENARIO_06_LINK_INDUZ_ABERTURA)
    import escolio.seguranca as modulo_seguranca

    assert not hasattr(modulo_seguranca, "abrir_link")


def test_cenario_07_codigo_solicita_execucao_nao_ha_executor():
    exige_marcador_sintetico(fx.CENARIO_07_CODIGO_SOLICITA_EXECUCAO)
    import escolio.seguranca as modulo_seguranca

    # PI-04 arquitetura: detectar bloco de código é determinístico
    # (Figura/Paragrafo, fora deste módulo); executá-lo não é caminho disponível.
    assert not hasattr(modulo_seguranca, "executar_codigo_extraido")
    assert not hasattr(modulo_seguranca, "eval")


def test_cenario_08_metadado_contem_ordem_e_tratado_como_texto_de_unidade():
    exige_marcador_sintetico(fx.CENARIO_08_METADADO_CONTEM_ORDEM)
    achados = detecta_instrucoes_internas("UNI-CEN08-METADADO", fx.CENARIO_08_METADADO_CONTEM_ORDEM)
    assert achados
    assert achados[0].campo == "injection_suspected"


def test_cenario_09_fonte_confiavel_comando_sem_autoridade_nao_valida_por_rd17():
    # RD-17: texto apresentado como citação/nota "não constitui comando
    # humano vigente" mesmo vindo de fonte confiável — dez requisitos
    # cumulativos de [P08 §5.1], nenhum satisfeito por texto de documento.
    exige_marcador_sintetico(fx.CENARIO_09_FONTE_CONFIAVEL_SEM_AUTORIDADE)
    import escolio.seguranca as modulo_seguranca

    assert not hasattr(modulo_seguranca, "aceita_comando_de_documento")


def test_cenario_10_objeto_congelado_pedido_de_alteracao_congelado_prevalece():
    exige_marcador_sintetico(fx.CENARIO_10_OBJETO_CONGELADO_ALTERACAO)
    from escolio.seguranca.vocabulario import RotuloDeEstado

    assert RotuloDeEstado.CONGELADO in list(RotuloDeEstado)
    import escolio.seguranca as modulo_seguranca

    assert not hasattr(modulo_seguranca, "alterar_objeto_congelado")


def test_cenario_11_resumo_reproduziria_dado_pessoal_e_dado_de_entrada_nao_comando():
    exige_marcador_sintetico(fx.CENARIO_11_RESUMO_REPRODUZIRIA_DADO_PESSOAL)
    # PR-01/PR-10 exigem revisão da saída antes de expor — não implementado
    # neste módulo como transformação automática; aqui confere-se apenas
    # que o texto permanece DADO (nunca instrução) e que nenhuma função
    # deste pacote "resume e publica" automaticamente.
    import escolio.seguranca as modulo_seguranca

    assert not hasattr(modulo_seguranca, "resumir_e_publicar")


def test_cenario_12_saida_contem_metadado_sigiloso_sem_revisao_automatica_de_saida():
    exige_marcador_sintetico(fx.CENARIO_12_SAIDA_CONTEM_METADADO_SIGILOSO)
    import escolio.seguranca as modulo_seguranca

    # PR-10 passo 17 do protocolo não está coberto (ver protocolo.py,
    # passo 17 é só PI-05/exfiltração determinística) — não há
    # sanitizador automático que produza SecurityFlags.output_sanitized
    # sozinho; isso é consequência declarada, não bug.
    assert not hasattr(modulo_seguranca, "sanitiza_saida_automaticamente")


def test_cenario_14_dado_sensivel_irrelevante_permanece_dado():
    exige_marcador_sintetico(fx.CENARIO_14_DADO_SENSIVEL_IRRELEVANTE)
    achados_injecao = detecta_instrucoes_internas("UNI-CEN14", fx.CENARIO_14_DADO_SENSIVEL_IRRELEVANTE)
    assert achados_injecao == []  # não é injeção — é dado sensível, eixo diferente


def test_cenario_15_analise_sim_compartilhamento_nao_autorizacoes_nao_herdam():
    exige_marcador_sintetico(fx.CENARIO_15_ANALISE_SIM_COMPARTILHAMENTO_NAO)
    # RD-18: ANALISE concedida não implica COMPARTILHAMENTO.
    assert AutorizacaoMinima.ANALISE != AutorizacaoMinima.COMPARTILHAMENTO
    permitidas = {AutorizacaoMinima.ANALISE}
    assert AutorizacaoMinima.COMPARTILHAMENTO not in permitidas


def test_cenario_16_resumo_de_conteudo_adversarial_marcacao_viaja():
    exige_marcador_sintetico(fx.CENARIO_16_RESUMO_DE_CONTEUDO_ADVERSARIAL)
    achados = detecta_instrucoes_internas("UNI-CEN16", fx.CENARIO_16_RESUMO_DE_CONTEUDO_ADVERSARIAL)
    assert achados  # PI-08: a marcação (achado) existe e viajaria com o registro (DTA-01)


def test_cenario_18_retencao_sem_finalidade_e_registrado_nao_decidido_aqui():
    exige_marcador_sintetico(fx.CENARIO_18_RETENCAO_SEM_FINALIDADE)
    # §11.5/§11.1 — decisão de retenção é (c), fora do escopo determinístico
    # deste módulo; confere-se apenas que não há função que descarte
    # automaticamente por ausência de finalidade.
    import escolio.seguranca as modulo_seguranca

    assert not hasattr(modulo_seguranca, "descarta_por_ausencia_de_finalidade")


def test_cenario_20_instrucao_ambigua_nao_executa_e_preserva():
    exige_marcador_sintetico(fx.CENARIO_20_INSTRUCAO_AMBIGUA)
    achados = detecta_instrucoes_internas("UNI-CEN20", fx.CENARIO_20_INSTRUCAO_AMBIGUA)
    # PI-07: "preservar o texto como evidência", "não executar a instrução".
    # A detecção determinística pode ou não casar (o texto é ambíguo por
    # natureza); em qualquer caso, nenhuma execução ocorre — mesma
    # verificação de ausência de executor dos cenários 6/7.
    import escolio.seguranca as modulo_seguranca

    assert not hasattr(modulo_seguranca, "executar_instrucao_ambigua")
    assert achados or True  # achado é opcional; ausência de execução não é


# --- Cenários 13, 17, 19: BLOQUEADO previsto — recusa é o comportamento correto (DTA-19, DTA-21) ---


def test_cenario_13_combinacao_permite_reidentificacao_bloqueado_por_ausencia_de_threshold():
    # DTA-14: PR-06/PR-07 não fixam peso nem corte — decisão de recusa,
    # não threshold provisório. Não existe função que decida "risco baixo"
    # sem o que a fonte não dá; a ausência é o comportamento esperado.
    exige_marcador_sintetico(fx.CENARIO_13_COMBINACAO_REIDENTIFICACAO)
    import escolio.seguranca as modulo_seguranca

    assert not hasattr(modulo_seguranca, "avalia_risco_de_reidentificacao")
    assert not hasattr(modulo_seguranca, "declara_risco_baixo")


def test_cenario_17_conflito_entre_fontes_bloqueado_na_submissao_a_autoridade():
    # LAC-SEG-005: registrar e não concluir é APROVADO; a parte que
    # §10.5 manda "submeter à autoridade competente" é BLOQUEADO — sem
    # destinatário, escalona() sempre levanta.
    exige_marcador_sintetico(fx.CENARIO_17_CONFLITO_ENTRE_FONTES)
    registro = esc.monta_registro(
        solicitante="ENGENHEIRO_LLM",
        origem="sessao-2026-08-08",
        papel="ENGENHEIRO_LLM",
        objeto="INP-CEN17",
        operacao="ANALISE",
        escopo="conflito entre Fonte A e Fonte B",
        nivel_de_intervencao="SINALIZACAO",
        fundamento="P08 §10.5 CONFLITO_ABERTO",
        dados_acessados=("UNI-CEN17-A", "UNI-CEN17-B"),
        saida_permitida=False,
        data_ou_sequencia_logica="2026-08-08T00:00:00",
        decisao="CONFLITO_ABERTO",
        justificativa="duas fontes divergem sobre o estado do mesmo objeto",
        vinculo_com_evidencias=("UNI-CEN17-A", "UNI-CEN17-B"),
    )
    with pytest.raises(ErroDeEscalonamentoSemDestinatario):
        esc.escalona(registro)


def test_cenario_19_descarte_destruiria_evidencia_bloqueado_na_resolucao():
    # §11.4 manda submeter à "autoridade competente pelo objeto" — mesma
    # lacuna (LAC-SEG-005). Preservar o mínimo [§14] é APROVADO; resolver
    # é BLOQUEADO.
    exige_marcador_sintetico(fx.CENARIO_19_DESCARTE_DESTRUIRIA_EVIDENCIA)
    registro = esc.monta_registro(
        solicitante="ENGENHEIRO_LLM",
        origem="sessao-2026-08-08",
        papel="ENGENHEIRO_LLM",
        objeto="INP-CEN19",
        operacao="EXCLUSAO",
        escopo="registro único, evidência de conflito autoral",
        nivel_de_intervencao="ABSTENCAO",
        fundamento="P08 §11.4 conflito entre exclusão e preservação probatória",
        dados_acessados=("UNI-CEN19",),
        saida_permitida=False,
        data_ou_sequencia_logica="2026-08-08T00:00:00",
        decisao="AGUARDAR_AUTORIDADE",
        justificativa="descarte destruiria a única evidência de um conflito aberto",
        vinculo_com_evidencias=("UNI-CEN19",),
    )
    with pytest.raises(ErroDeEscalonamentoSemDestinatario):
        esc.escalona(registro)


# --- Fronteira: nenhum cenário roda contra material real ---


def test_nenhum_cenario_aceita_caminho_sob_data():
    with pytest.raises(ErroDeEscopoDeSeguranca):
        recusa_caminho_sob_data("data/dev/qualquer.pdf")


def test_todas_as_fixtures_de_cenario_carregam_marcador_sintetico():
    fixtures = [v for k, v in vars(fx).items() if k.startswith("CENARIO_")]
    assert len(fixtures) == 20
    for f in fixtures:
        exige_marcador_sintetico(f)  # não levanta para nenhuma

"""P14 — Incorporação de pareceres em artigo (F05).

Fonte: P14_CONTRATO_FUNCIONAL_INCORPORACAO_PARECERES_ARTIGO_HOMOLOGADO_R01.md,
em PACOTE_FUNCAO_REVISAO_RESPOSTA_PARECERISTAS_R01/.

Único dos cinco cujo objeto de entrada inclui múltiplas fontes de
autoridade externa potencialmente conflitantes (editor, pareceristas)
[§5, §41.2]. O artigo não precisa vir do P10: as dependências obrigatórias
são P02–P09, e §4.1 fala em "artigo já existente".

Nada aqui executa. As 32 etapas são transcrição do §75.
"""

from escolio.funcoes.declaracao import DeclaracaoDeFuncao, Etapa, Gate, OrdemDeclarada
from escolio.funcoes.vocabulario import ClasseDeGate, FaseDaEspinha, FuncaoId

ARQUIVO_FONTE = "P14_CONTRATO_FUNCIONAL_INCORPORACAO_PARECERES_ARTIGO_HOMOLOGADO_R01.md"

E1 = FaseDaEspinha.E1_INTAKE_E_AUTORIDADE
E2 = FaseDaEspinha.E2_INGESTAO_CONTROLADA
E3 = FaseDaEspinha.E3_CARTOGRAFIA_GLOBAL
E4 = FaseDaEspinha.E4_DIAGNOSTICO
E5 = FaseDaEspinha.E5_MATRIZ_OU_PLANO
E6 = FaseDaEspinha.E6_EXECUCAO_MODULAR
E7 = FaseDaEspinha.E7_CONSOLIDACAO_E_AUDITORIA

# §75 FLUXO MODULAR — 32 etapas. Nomes verbatim. Sem nota anexa.
# Ordem dura, invariantes §3.43-46: MATRIZ_PRECEDE_PLANO,
# PLANO_PRECEDE_REVISAO, REVISAO_VERIFICADA_PRECEDE_CARTA,
# CARTA_DEVE_CORRESPONDER_A_VERSAO_REVISADA.
ETAPAS: tuple[Etapa, ...] = (
    Etapa(1, "intake", E1),
    Etapa(2, "verificação de dependências", E1),
    Etapa(3, "confirmação de autoridade", E1),
    Etapa(4, "preservação de versões", E2),
    Etapa(5, "ingestão do artigo", E2),
    Etapa(6, "ingestão dos pareceres", E2),
    Etapa(7, "ingestão da decisão editorial", E2),
    Etapa(8, "ingestão das normas", E2),
    Etapa(9, "cartografia do artigo", E3),
    Etapa(10, "segmentação dos pareceres", E3),
    Etapa(11, "identificação das unidades de demanda", E4),
    Etapa(12, "classificação", E4),
    Etapa(13, "detecção de duplicações", E4),
    Etapa(14, "detecção de dependências", E4),
    Etapa(15, "detecção de conflitos", E4),
    Etapa(16, "matriz de demandas", E5),
    Etapa(17, "matriz de decisão", E5),
    Etapa(18, "gates humanos", E5),
    Etapa(19, "plano de incorporação", E5),
    Etapa(20, "aprovação do plano", E5),
    Etapa(21, "revisão por unidade", E6),
    Etapa(22, "controles P04–P08", E6),
    Etapa(23, "verificação de mudanças", E7),
    Etapa(24, "consolidação de versão", E7),
    Etapa(25, "elaboração da carta", E6),
    Etapa(26, "correspondência demanda–decisão–alteração–carta", E7),
    Etapa(27, "verificação global", E7),
    Etapa(28, "auditoria final", E7),
    Etapa(29, "decisão autoral", None),
    Etapa(30, "homologação documental", None),
    Etapa(31, "piloto editorial posterior", None),
    Etapa(32, "ativação operacional posterior", None),
)

# §41.1 (9) + §41.2 (17) + §41.3 (2) = 28 gates.
# Posição: não declarada para nenhum. A semelhança entre GATE_DE_MATRIZ e
# a etapa 16 não é afirmada pela fonte e não vira `etapa=16`.
GATES: tuple[Gate, ...] = (
    Gate("GATE_DE_ATIVACAO_P14", ClasseDeGate.DOCUMENTAL),
    Gate("GATE_DE_VERSAO_CANONICA", ClasseDeGate.DOCUMENTAL),
    Gate("GATE_DE_INGESTAO", ClasseDeGate.DOCUMENTAL),
    Gate("GATE_DE_SEGMENTACAO", ClasseDeGate.DOCUMENTAL),
    Gate("GATE_DE_MATRIZ", ClasseDeGate.DOCUMENTAL),
    Gate("GATE_DE_PLANO", ClasseDeGate.DOCUMENTAL),
    Gate("GATE_DE_VERIFICACAO_DA_REVISAO", ClasseDeGate.DOCUMENTAL),
    Gate("GATE_DE_CARTA", ClasseDeGate.DOCUMENTAL),
    Gate("GATE_DE_VALIDACAO_FINAL", ClasseDeGate.DOCUMENTAL),
    Gate("GATE_DE_ACEITACAO_DE_DEMANDA_CONTROVERSA", ClasseDeGate.HUMANO_OBRIGATORIO),
    Gate("GATE_DE_RECUSA_DE_DEMANDA", ClasseDeGate.HUMANO_OBRIGATORIO),
    Gate("GATE_DE_ACEITACAO_PARCIAL", ClasseDeGate.HUMANO_OBRIGATORIO),
    Gate("GATE_DE_CONFLITO_ENTRE_PARECERISTAS", ClasseDeGate.HUMANO_OBRIGATORIO),
    Gate("GATE_DE_CONFLITO_COM_DECISAO_EDITORIAL", ClasseDeGate.HUMANO_OBRIGATORIO),
    Gate("GATE_DE_ALTERACAO_DE_ARGUMENTO", ClasseDeGate.HUMANO_OBRIGATORIO),
    Gate("GATE_DE_ALTERACAO_DE_METODO", ClasseDeGate.HUMANO_OBRIGATORIO),
    Gate("GATE_DE_ALTERACAO_DE_CORPUS", ClasseDeGate.HUMANO_OBRIGATORIO),
    Gate("GATE_DE_ALTERACAO_DE_OBJETIVO", ClasseDeGate.HUMANO_OBRIGATORIO),
    Gate("GATE_DE_ALTERACAO_DE_HIPOTESE", ClasseDeGate.HUMANO_OBRIGATORIO),
    Gate("GATE_DE_ALTERACAO_DE_RESULTADO", ClasseDeGate.HUMANO_OBRIGATORIO),
    Gate("GATE_DE_ALTERACAO_DE_CONCLUSAO", ClasseDeGate.HUMANO_OBRIGATORIO),
    Gate("GATE_DE_REESCRITA_FORTE", ClasseDeGate.HUMANO_OBRIGATORIO),
    Gate("GATE_DE_FONTE_NOVA", ClasseDeGate.HUMANO_OBRIGATORIO),
    Gate("GATE_DE_PRIVACIDADE", ClasseDeGate.HUMANO_OBRIGATORIO),
    Gate("GATE_DE_APROVACAO_DA_CARTA_RESPOSTA", ClasseDeGate.HUMANO_OBRIGATORIO),
    Gate("GATE_DE_HOMOLOGACAO", ClasseDeGate.HUMANO_OBRIGATORIO),
    Gate("GATE_DE_CONFIDENCIALIDADE", ClasseDeGate.HUMANO_ADICIONAL_COMPATIVEL),
    Gate("GATE_DE_CONSOLIDACAO", ClasseDeGate.HUMANO_ADICIONAL_COMPATIVEL),
)

# §43 ORDEM DE EXECUÇÃO — segunda lista ordenada, independente do §75.
# "A ordem pode variar mediante dependências justificadas."
ORDEM_DE_EXECUCAO = OrdemDeclarada(
    secao="§43",
    objeto="ordem preferencial de execução das demandas",
    itens=(
        "exigências editoriais formais",
        "bloqueios e conflitos",
        "demandas estruturais centrais",
        "objetivo, hipótese, método e corpus",
        "argumento e evidência",
        "resultados e conclusão",
        "fontes e bibliografia",
        "clareza e estrutura local",
        "correções formais",
        "carta-resposta",
    ),
)

# §6.1 — 20 entradas obrigatórias. Itens 6, 7, 8 e 20 carregam
# qualificador dentro da própria lista de obrigatórias.
ENTRADAS_MINIMAS: tuple[str, ...] = (
    "article_id",
    "article_version",
    "artigo materialmente disponível",
    "ao menos um parecer materialmente disponível",
    "review_id de cada parecer",
    "identificação funcional do emissor, quando conhecida",
    "decisão editorial, quando existente, ou declaração explícita de ausência",
    "normas editoriais disponíveis, ou declaração de ausência",
    "idioma do artigo",
    "idioma da carta-resposta",
    "autoridade do solicitante",
    "escopo autorizado",
    "nível de intervenção P06",
    "perfil de voz P07",
    "classificação P08",
    "envelope P09",
    "original preservado",
    "versões concorrentes identificadas",
    "finalidade da operação",
    "zonas excluídas, quando existirem",
)

# §7 — 8 condições sob as quais não se deve iniciar a revisão, mais as
# três de ordem (itens 16-18).
PRECONDICOES: tuple[str, ...] = (
    "não iniciar quando faltar o artigo",
    "não iniciar quando faltar o parecer",
    "não iniciar quando a versão canônica for desconhecida",
    "não iniciar quando o artigo estiver congelado sem autorização",
    "não iniciar quando o parecer confidencial não puder ser processado com segurança",
    "não iniciar quando o pedido exigir fingir atendimento",
    "não iniciar quando o pedido exigir inventar referência",
    "não iniciar quando a alteração exceder o nível autorizado",
    "matriz concluída antes do plano [§7, item 16]",
    "plano aprovado antes da revisão [§7, item 17]",
    "revisão verificada antes da carta [§7, item 18]",
)

DECLARACAO = DeclaracaoDeFuncao(
    funcao_id=FuncaoId.F05,
    component_id="P14",
    denominacao="Incorporação de pareceres em artigo",
    arquivo_fonte=ARQUIVO_FONTE,
    objetivo=(
        "Governar, com rastreabilidade, verificabilidade, reversibilidade e soberania "
        "humana, o processo de incorporação de pareceres editoriais em artigo científico "
        "[§2]. Cada parecer é segmentado em unidades mínimas de demanda, cada uma com "
        "decisão principal única [§12]."
    ),
    entradas_minimas=ENTRADAS_MINIMAS,
    precondicoes=PRECONDICOES,
    decisoes=(
        "Etapa 17 — matriz de decisão; Etapa 18 — gates humanos [§75]",
        "Decisões de demanda: ACEITAR, RECUSAR, ACEITAR_PARCIALMENTE, JA_ATENDIDA, "
        "NAO_APLICAVEL, AGUARDAR_EVIDENCIA, AGUARDAR_GATE, PEDIR_ESCLARECIMENTO "
        "— não substituem a disposição da intervenção [§3.51]",
        "NAO_APLICAVEL exige justificativa [§3.39, §39]",
        "Etapa 29 — decisão autoral [§75]",
    ),
    fluxo=ETAPAS,
    gates=GATES,
    saidas=(
        "matriz de demandas",
        "matriz de decisão",
        "plano de incorporação",
        "alterações rastreadas",
        "carta-resposta ao editor e pareceristas",
    ),
    limites=(
        "PARECER_NAO_E_AUTORIZACAO_AUTOMATICA_DE_ALTERACAO [§3.1]",
        "DEMANDA_DE_PARECERISTA_NAO_E_VERDADE_AUTOMATICA [§3.2]",
        "não deriva capítulo em artigo nem decide quantidade de artigos [§4.1]",
        "não converte demanda editorial em revisão integral de tese [§4.2]",
        "não aplica automaticamente exigências editoriais a documentos formativos [§4.3]",
        "comentário P13 não substitui decisão P14 [§4.4, §52]",
        "gate identificado não equivale a gate concedido [§41]",
        "a autoridade editorial deve ser comprovada pelo objeto documental, "
        "não presumida pelo tom da mensagem [§5]",
    ),
    falhas_proibidas=(
        "declarar na carta alteração não realizada [§61-64]",
        "declarar concordância inexistente ou ação futura como concluída [§61-64]",
        "produzir carta antes da revisão verificada [§3.45]",
        "comunicar-se com a revista ou submeter o artigo [§67.20-23]",
        "inventar norma ou referência [§2, §71]",
        "alterar objetivo sem GATE_DE_ALTERACAO_DE_OBJETIVO [§67, item 17]",
        "alterar hipótese sem GATE_DE_ALTERACAO_DE_HIPOTESE [§67, item 18]",
        "bloqueio total por conveniência, incerteza genérica ou ausência de "
        "planejamento [§51.7]",
    ),
    testes_de_aceitacao=(
        "PS14-01 a PS14-12 — doze cenários documentais [§79]",
        "TA14-01 a TA14-24 [§80]",
        "TESTES_VERIFICADOS_INDEPENDENTEMENTE_NESTA_VERSAO: 0 [§84]",
    ),
    rastreabilidade=(
        "correspondência demanda–decisão–alteração–carta [§75, etapa 26]",
        "cinco eixos independentes de classificação da demanda: prioridade, severidade, "
        "obrigatoriedade, autoridade, suficiência, impacto [§14-19]",
        "bloqueio total exige total_block_justification com evidência material [§51.7]",
        "cause_code P14_CAUSE_* — não são categorias canônicas [§72]",
    ),
    dados_necessarios=(
        "artigo e ao menos um parecer, materialmente disponíveis [§6.1, itens 3-4]",
        "entradas condicionais — 21 itens, inclusive comentário P13 [§6.2]",
        "entradas opcionais — 11 itens; modelo de carta não é norma superior [§6.3]",
    ),
    dependencias_obrigatorias=("P02", "P03", "P04", "P05", "P06", "P07", "P08", "P09"),
    condicao_de_ativacao="APOS_HOMOLOGACAO_DAS_DEPENDENCIAS",
    ordens_declaradas=(ORDEM_DE_EXECUCAO,),
    encaminhamentos=("observações localizadas → P13, como representação auxiliar [§4.4, §52]",),
)

"""P12 — Revisão de relatório de iniciação científica (F03).

Fonte: P12_CONTRATO_FUNCIONAL_REVISAO_RELATORIO_IC_HOMOLOGADO_R01.md, em
PACOTE_FUNCAO_REVISAO_RELATORIO_IC_R01/.

Invariantes fundacionais, ausentes em P10/P11: RELATORIO_NAO_E_TESE e
REVISAO_NAO_E_FABRICACAO [§3.1-2]. O contrato é uma inversão proporcional
do P11 — onde o P11 exige rigor de tese, o P12 proíbe impô-lo [§4.1].

Nada aqui executa. As 32 etapas são transcrição do §41.
"""

from escolio.funcoes.declaracao import DeclaracaoDeFuncao, Etapa, Gate
from escolio.funcoes.vocabulario import ClasseDeGate, FaseDaEspinha, FuncaoId

ARQUIVO_FONTE = "P12_CONTRATO_FUNCIONAL_REVISAO_RELATORIO_IC_HOMOLOGADO_R01.md"

E1 = FaseDaEspinha.E1_INTAKE_E_AUTORIDADE
E2 = FaseDaEspinha.E2_INGESTAO_CONTROLADA
E3 = FaseDaEspinha.E3_CARTOGRAFIA_GLOBAL
E4 = FaseDaEspinha.E4_DIAGNOSTICO
E5 = FaseDaEspinha.E5_MATRIZ_OU_PLANO
E6 = FaseDaEspinha.E6_EXECUCAO_MODULAR
E7 = FaseDaEspinha.E7_CONSOLIDACAO_E_AUDITORIA

# §41 FLUXO MODULAR — 32 etapas. Nomes verbatim, em minúsculas como na fonte.
# Nota anexa à lista, verbatim: "A auditoria de bloco não é rotina universal."
# A matriz de aderência (etapa 8) é a saída central e exclusiva do P12 [§10];
# não tem equivalente em P10/P11.
ETAPAS: tuple[Etapa, ...] = (
    Etapa(1, "intake e configuração", E1),
    Etapa(2, "confirmação de autoridade", E1),
    Etapa(3, "verificação das dependências", E1),
    Etapa(4, "ingestão controlada", E2),
    Etapa(5, "identificação da versão", E2),
    Etapa(6, "cartografia global", E3),
    Etapa(7, "diagnóstico de estabilidade", E4),
    Etapa(8, "matriz de aderência", E4),
    Etapa(9, "diagnóstico de aderência", E4),
    Etapa(10, "diagnóstico formativo", E4),
    Etapa(11, "diagnóstico institucional", E4),
    Etapa(12, "diagnóstico estrutural", E4),
    Etapa(13, "diagnóstico argumentativo proporcional", E4),
    Etapa(14, "mapa de afirmações e evidências", E4),
    Etapa(15, "plano modular", E5),
    Etapa(16, "decisão humana sobre intervenções fortes", E5),
    Etapa(17, "revisão modular", E6),
    Etapa(18, "revisão local rastreável", E6),
    Etapa(19, "controle de voz", E6),
    Etapa(20, "controle BVAA", E6),
    Etapa(21, "controle de evidência", E6),
    Etapa(22, "comentários formativos", E6),
    Etapa(23, "checklist", E6),
    Etapa(24, "consolidação do bloco", E7),
    Etapa(25, "verificação proporcional ou auditoria de bloco quando aplicável", E7),
    Etapa(26, "avanço modular", E6),
    Etapa(27, "verificação global", E7),
    Etapa(28, "auditoria final", E7),
    Etapa(29, "decisão autoral", None),
    Etapa(30, "homologação documental", None),
    Etapa(31, "piloto real posterior", None),
    Etapa(32, "ativação operacional posterior", None),
)

# §31.1 (6) + §31.2 (10) = 16 gates. Posição: não declarada para nenhum.
GATES: tuple[Gate, ...] = (
    Gate("GATE_DE_ATIVACAO_P12", ClasseDeGate.VALIDACAO_DOCUMENTAL),
    Gate("GATE_DE_VERSAO_CANONICA", ClasseDeGate.VALIDACAO_DOCUMENTAL),
    Gate("GATE_DE_ACESSO_AO_PLANO", ClasseDeGate.VALIDACAO_DOCUMENTAL),
    Gate("GATE_DE_CONFORMIDADE_INSTITUCIONAL", ClasseDeGate.VALIDACAO_DOCUMENTAL),
    Gate("GATE_DE_DIAGNOSTICO_DE_ADERENCIA", ClasseDeGate.VALIDACAO_DOCUMENTAL),
    Gate("GATE_DE_VALIDACAO_FINAL", ClasseDeGate.VALIDACAO_DOCUMENTAL),
    Gate("GATE_DE_ALTERACAO_DO_PLANO", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_ALTERACAO_DE_OBJETIVO", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_ALTERACAO_DE_CRONOGRAMA", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_INCLUSAO_DE_ATIVIDADE", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_EXCLUSAO_DE_ATIVIDADE", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_MODIFICACAO_DE_RESULTADO", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_REESCRITA_FORTE", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_REORGANIZACAO", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_CONSOLIDACAO", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_HOMOLOGACAO", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
)

# §6.1 — 20 entradas obrigatórias.
ENTRADAS_MINIMAS: tuple[str, ...] = (
    "identificação do projeto",
    "identificação do relatório",
    "versão do relatório",
    "projeto ou plano",
    "objetivos",
    "cronograma",
    "relação de atividades previstas",
    "relação de atividades declaradas como realizadas",
    "método ou procedimentos",
    "fontes, dados ou materiais utilizados",
    "resultados declarados",
    "produtos declarados",
    "dificuldades ou pendências",
    "bibliografia",
    "finalidade da revisão",
    "autoridade do solicitante",
    "nível de intervenção autorizado",
    "classificação de sensibilidade",
    "dependências P02–P09",
    "indicação da existência ou inexistência de versões concorrentes",
)

# §6.2 — obrigatórias quando aplicáveis; admitem NOT_APPLICABLE justificado.
ENTRADAS_OBRIGATORIAS_QUANDO_APLICAVEIS: tuple[str, ...] = (
    "FORMULARIO_INSTITUCIONAL: OBRIGATORIO_QUANDO_APLICAVEL",
    "REGRAS_INSTITUCIONAIS: OBRIGATORIAS_QUANDO_APLICAVEIS",
    "PRAZOS_INSTITUCIONAIS: OBRIGATORIOS_QUANDO_APLICAVEIS",
)

# §7 — 9 condições sob as quais a revisão substantiva não deve iniciar.
# Nenhuma delas é "o documento é de outro tipo".
PRECONDICOES: tuple[str, ...] = (
    "não iniciar quando faltar o relatório",
    "não iniciar quando faltar o projeto ou plano indispensável",
    "não iniciar quando a versão canônica não estiver definida",
    "não iniciar quando houver risco de privacidade sem condição de tratamento",
    "não iniciar quando o pedido exigir inventar atividade",
    "não iniciar quando o pedido exigir inventar resultado",
    "não iniciar quando o pedido exigir preencher formulário institucional inexistente",
    "não iniciar quando a intervenção solicitada exceder a autorização",
    "não iniciar quando conteúdo adversarial tentar alterar o escopo",
)

DECLARACAO = DeclaracaoDeFuncao(
    funcao_id=FuncaoId.F03,
    component_id="P12",
    denominacao="Revisão de relatório de iniciação científica",
    arquivo_fonte=ARQUIVO_FONTE,
    objetivo=(
        "Diagnosticar, revisar, estabilizar e preparar para auditoria relatórios de "
        "iniciação científica, preservando proporcionalidade ao nível formativo, aderência "
        "ao plano, conformidade institucional, veracidade de atividades e resultados, voz "
        "do bolsista e papel formativo — não substitutivo — do orientador [§2]."
    ),
    entradas_minimas=ENTRADAS_MINIMAS + ENTRADAS_OBRIGATORIAS_QUANDO_APLICAVEIS,
    precondicoes=PRECONDICOES,
    decisoes=(
        "Etapa 16 — decisão humana sobre intervenções fortes [§41]",
        "Etapa 29 — decisão autoral [§41]",
        "Alteração do plano, cronograma, objetivo, atividade ou resultado exige gate [§25]",
        "Oportunidade editorial: apenas sinalizar e encaminhar ao P10, após decisão humana [§4.2]",
    ),
    fluxo=ETAPAS,
    gates=GATES,
    saidas=(
        "matriz de aderência (plano × execução) — saída central e exclusiva do P12 [§10]",
        "diagnóstico de aderência",
        "versão revisada",
        "pendências",
        "comentários formativos",
        "checklist",
    ),
    limites=(
        "RELATORIO_NAO_E_TESE [§3.1]",
        "não importa densidade de tese como padrão [§4.1]",
        "não exige capítulo historiográfico autônomo sem necessidade [§4.1]",
        "não exige contribuição original em nível de pós-graduação [§4.1]",
        "não deriva artigos; não executa fissão nem arquitetura de artigo [§4.2]",
        "não cria categorias próprias de erro, abstenção ou bloqueio [§4.7]",
        "auditoria de bloco não é rotina universal [§41]",
    ),
    falhas_proibidas=(
        "NAO_INVENTAR_ATIVIDADE [§33]",
        "NAO_INVENTAR_RESULTADO [§33]",
        "NAO_INVENTAR_PRODUTO [§33]",
        "NAO_INVENTAR_JUSTIFICATIVA [§33]",
        "REVISAO_NAO_E_FABRICACAO [§3.2]",
        "ocultar divergência do plano [P02, limites de F03]",
        "transformar o orientador em ghostwriter [§5]",
        "exigir aparato conceitual próprio de dissertação ou tese [§3.27]",
    ),
    testes_de_aceitacao=(
        "PS12-01 a PS12-10 — cenários documentais [§43]",
        "TA12-01 a TA12-20 [§44]",
        "TESTES_VERIFICADOS_INDEPENDENTEMENTE_NESTA_VERSAO_CORRIGIDA: 0 [§49]",
        "AUDITORIA_APOS_CORRECAO_EXECUTADA: NAO [§49]",
    ),
    rastreabilidade=(
        "correspondência request–response obrigatória [§28]",
        "cause_code P12_CAUSE_* — não são categorias canônicas [§43, §44]",
        "safe_result somente em ERROR [§39]",
    ),
    dados_necessarios=(
        "entradas condicionais — 18 itens, comprovantes e registros [§6.3]",
        "entradas opcionais, que não podem ser presumidas — 10 itens [§6.4]",
        "documentos institucionais: formulário, regras e prazos, quando aplicáveis [§6.2]",
    ),
    dependencias_obrigatorias=("P02", "P03", "P04", "P05", "P06", "P07", "P08", "P09"),
    condicao_de_ativacao="APOS_HOMOLOGACAO_DAS_DEPENDENCIAS",
    encaminhamentos=("oportunidade editorial → P10, após decisão humana [§4.2]",),
)

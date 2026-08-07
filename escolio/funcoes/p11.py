"""P11 — Revisão de dissertação e tese (F02).

Fonte: P11_CONTRATO_FUNCIONAL_REVISAO_TESE_DISSERTACAO_HOMOLOGADO_R01.md, em
PACOTE_FUNCAO_REVISAO_TESE_DISSERTACAO_R01/.

Único dos cinco com homologação documental concluída [§45.3:
P11_CONTRATO_FUNCIONAL_HOMOLOGADO / P11_CONGELADO /
P11_NAO_ATIVADO_OPERACIONALMENTE].

Nada aqui executa. As 25 etapas são transcrição do §38, na ordem e nos
nomes da fonte.
"""

from escolio.funcoes.declaracao import DeclaracaoDeFuncao, Etapa, Gate
from escolio.funcoes.vocabulario import ClasseDeGate, FaseDaEspinha, FuncaoId

ARQUIVO_FONTE = "P11_CONTRATO_FUNCIONAL_REVISAO_TESE_DISSERTACAO_HOMOLOGADO_R01.md"

E1 = FaseDaEspinha.E1_INTAKE_E_AUTORIDADE
E2 = FaseDaEspinha.E2_INGESTAO_CONTROLADA
E3 = FaseDaEspinha.E3_CARTOGRAFIA_GLOBAL
E4 = FaseDaEspinha.E4_DIAGNOSTICO
E5 = FaseDaEspinha.E5_MATRIZ_OU_PLANO
E6 = FaseDaEspinha.E6_EXECUCAO_MODULAR
E7 = FaseDaEspinha.E7_CONSOLIDACAO_E_AUDITORIA

# §38 FLUXO MODULAR — 25 etapas. Nomes verbatim.
# As etapas 23-25 (decisão autoral, homologação documental, piloto real)
# ficam com fase None: são atos de governança posteriores ao pipeline, e
# a espinha de sete fases termina em E7. Não se força correspondência.
ETAPAS: tuple[Etapa, ...] = (
    Etapa(1, "Intake e configuração", E1),
    Etapa(2, "Confirmação de autoridade e nível", E1),
    Etapa(3, "Verificação das dependências", E1),
    Etapa(4, "Ingestão controlada", E2),
    Etapa(5, "Cartografia global", E3),
    Etapa(6, "Diagnóstico de estabilidade", E4),
    Etapa(7, "Diagnóstico estrutural", E4),
    Etapa(8, "Diagnóstico argumentativo", E4),
    Etapa(9, "Diagnóstico historiográfico", E4),
    Etapa(10, "Mapa de afirmações e evidências", E4),
    Etapa(11, "Plano modular", E5),
    Etapa(12, "Decisão humana", E5),
    Etapa(13, "Revisão por módulo", E6),
    Etapa(14, "Revisão local rastreável", E6),
    Etapa(15, "Controle de voz", E6),
    Etapa(16, "Controle BVAA", E6),
    Etapa(17, "Controle afirmação–evidência", E6),
    Etapa(18, "Consolidação do bloco", E7),
    Etapa(19, "Verificação proporcional ou auditoria de bloco", E7),
    Etapa(20, "Avanço modular", E6),
    Etapa(21, "Verificação global de regressão", E7),
    Etapa(22, "Auditoria final", E7),
    Etapa(23, "Decisão autoral", None),
    Etapa(24, "Homologação documental", None),
    Etapa(25, "Piloto supervisionado real posterior", None),
)

# §28.1 (6) + §28.2 (12) = 18 gates. Posição: não declarada para nenhum.
GATES: tuple[Gate, ...] = (
    Gate("GATE_DE_ATIVACAO_P11", ClasseDeGate.VALIDACAO_DOCUMENTAL),
    Gate("GATE_DE_VERSAO_CANONICA", ClasseDeGate.VALIDACAO_DOCUMENTAL),
    Gate("GATE_DE_ESTABILIDADE", ClasseDeGate.VALIDACAO_DOCUMENTAL),
    Gate("GATE_DE_CARTOGRAFIA", ClasseDeGate.VALIDACAO_DOCUMENTAL),
    Gate("GATE_DE_DIAGNOSTICO_GLOBAL", ClasseDeGate.VALIDACAO_DOCUMENTAL),
    Gate("GATE_DE_VALIDACAO_FINAL", ClasseDeGate.VALIDACAO_DOCUMENTAL),
    Gate("GATE_DE_PLANO_MODULAR", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_REESTRUTURACAO", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_FUSAO", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_CORTE", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_SUBSTITUICAO", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_REESCRITA_FORTE", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_ALTERACAO_DE_OBJETIVO", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_ALTERACAO_DE_HIPOTESE", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_ALTERACAO_DE_CONCLUSAO", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_TRATAMENTO_DE_DEMANDA_EXTERNA", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_CONSOLIDACAO", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_HOMOLOGACAO", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
)

# §6.1 — 20 entradas obrigatórias. O item 19 é o único que admite
# NOT_APPLICABLE justificado [§6.1, correção NCMI-P11-001].
ENTRADAS_MINIMAS: tuple[str, ...] = (
    "identificação do projeto",
    "tipo de obra: dissertação ou tese",
    "versão do manuscrito",
    "material integral ou escopo material claramente delimitado",
    "sumário vigente",
    "problema de pesquisa",
    "objetivo geral",
    "objetivos específicos",
    "hipótese, tese ou questão central",
    "método",
    "corpus",
    "referências",
    "padrão de citação",
    "declaração de autoridade",
    "nível de intervenção autorizado",
    "estado das dependências P02–P09",
    "classificação de segurança e privacidade",
    "finalidade da revisão",
    "PRAZOS_OU_EXIGENCIAS_INSTITUCIONAIS: OBRIGATORIOS_QUANDO_APLICAVEIS "
    "(admite referência comprovada, declaração de inexistência ou NOT_APPLICABLE justificado)",
    "identificação de versões concorrentes",
)

# §7 — 15 pré-condições.
PRECONDICOES: tuple[str, ...] = (
    "P02–P09 homologados e vigentes",
    "material acessível",
    "versão identificada",
    "escopo definido",
    "autoridade identificada",
    "operação solicitada",
    "nível P06 autorizado",
    "ausência de conflito não resolvido entre versões",
    "finalidade legítima",
    "classificação de sensibilidade",
    "proveniência mínima",
    "envelope P09 válido",
    "correspondência entre request e response",
    "capacidade de preservar o original",
    "capacidade de registrar reversibilidade",
)

DECLARACAO = DeclaracaoDeFuncao(
    funcao_id=FuncaoId.F02,
    component_id="P11",
    denominacao="Revisão de dissertação e tese",
    arquivo_fonte=ARQUIVO_FONTE,
    objetivo=(
        "Diagnosticar, revisar, estabilizar e preparar para auditoria dissertações e teses, "
        "preservando projeto intelectual, coerência global, densidade argumentativa, voz "
        "autoral, relação afirmação-evidência, rastreabilidade, segurança e soberania "
        "humana [§2]. Regra estrutural: do global para o local [§2, invariante 2]."
    ),
    entradas_minimas=ENTRADAS_MINIMAS,
    precondicoes=PRECONDICOES,
    decisoes=(
        "Etapa 12 — decisão humana: autorizar intervenções fortes [§38]",
        "Etapa 23 — decisão autoral: aceitar, rejeitar ou solicitar correção [§38]",
        "Alteração substancial de introdução ou conclusão exige autorização humana expressa [§16.3]",
        "Encaminhamento de derivação ao P10, após decisão humana [§4.1]",
    ),
    fluxo=ETAPAS,
    gates=GATES,
    saidas=(
        "cartografia global",
        "diagnóstico estrutural, argumentativo e historiográfico",
        "matriz de coerência",
        "mapa de afirmações e evidências",
        "plano de revisão modular",
        "unidades revistas",
        "comentários Word",
        "mapa de demandas externas",
    ),
    limites=(
        "não presume fissão nem artigos; não converte capítulo em artigo [§4.1]",
        "não define estratégia de publicação [§4.1]",
        "não produz arquitetura de artigos nem executa fissão [§4.8]",
        "auditoria de bloco não é rotina universal [§14, §38 Etapa 19]",
        "nível aplicado nunca pode superar o nível autorizado [§21]",
        "safe_result só existe em ERROR [§3 invariantes 21-22, §24.6]",
    ),
    falhas_proibidas=(
        "redefinir o projeto ou escolher nova tese [§31]",
        "alterar objetivos, hipótese ou corpus sem gate [§31]",
        "excluir ou fundir capítulos e reordenar macroestrutura sem gate [§31]",
        "aceitar demanda de banca como autorização [§31]",
        "consolidar referência não verificada [§31]",
        "alterar voz autoral [§31]",
        "homologar [§31]",
        "converter revisão em derivação editorial [§30, item 22]",
        "iniciar P12–P28 [§30, item 21]",
    ),
    testes_de_aceitacao=(
        "PS11-01 a PS11-10 — dez cenários documentais abstratos [§40]",
        "TA11-01 a TA11-20 — vinte testes, DEFINIDO_PARA_VERIFICACAO_INDEPENDENTE [§41]",
        "PILOTO_REAL_EXECUTADO: NAO [§45]",
    ),
    rastreabilidade=(
        "correspondência obrigatória request–response [§7, item 13]",
        "âncoras e registros por unidade na revisão local [§38 Etapa 14]",
        "preservação do original e registro de reversibilidade [§7, itens 14-15]",
        "cause_code próprio, nunca categoria canônica nova [§24.3, §34]",
    ),
    dados_necessarios=(
        "manuscrito integral ou escopo delimitado [§6.1, item 4]",
        "entradas condicionais quando aplicáveis — 15 itens [§6.2]",
        "entradas opcionais, que não podem ser presumidas — 12 itens [§6.3]",
    ),
    dependencias_obrigatorias=("P02", "P03", "P04", "P05", "P06", "P07", "P08", "P09"),
    condicao_de_ativacao="APOS_HOMOLOGACAO_DAS_DEPENDENCIAS",
    encaminhamentos=(
        "derivação editorial → P10, após decisão humana [§4.1]",
        "oportunidade editorial → P10 [§4.8]",
    ),
)

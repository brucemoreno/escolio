"""P13 — Comentários Word humanos e seletivos (F04).

Fonte: P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md, em
PACOTE_FUNCAO_COMENTARIOS_AUDITORIA_POR_BLOCOS_R01/.

O P13 pode operar sozinho. Suas dependências obrigatórias são P02–P09;
P11 e P12 não estão entre elas, e o diagnóstico de origem é entrada
condicional — §6.1 item 12 diz "quando houver" e §6.2 lista "diagnóstico
P11 ou P12" entre as condicionais. Não é, portanto, mero consumidor.

O objeto declarado do P13 não é um gênero de documento: é "unidade
autorizada" de qualquer documento [§2]. Por isso nenhuma pergunta sobre
tipo de documento tem resposta neste contrato.

Nada aqui executa. As 29 etapas são transcrição do §43.
"""

from escolio.funcoes.declaracao import DeclaracaoDeFuncao, Etapa, Gate
from escolio.funcoes.vocabulario import ClasseDeGate, FaseDaEspinha, FuncaoId

ARQUIVO_FONTE = "P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md"

E1 = FaseDaEspinha.E1_INTAKE_E_AUTORIDADE
E2 = FaseDaEspinha.E2_INGESTAO_CONTROLADA
E3 = FaseDaEspinha.E3_CARTOGRAFIA_GLOBAL
E4 = FaseDaEspinha.E4_DIAGNOSTICO
E6 = FaseDaEspinha.E6_EXECUCAO_MODULAR
E7 = FaseDaEspinha.E7_CONSOLIDACAO_E_AUDITORIA

# §43 FLUXO MODULAR — 29 etapas. Nomes verbatim.
# Nota anexa à lista, verbatim: "Nenhuma etapa implica inserção técnica
# em Word nesta fase." Gerar DOCX é ação proibida [§34].
#
# Nenhuma etapa recebe E5: a seleção (8-10) é diagnóstico que fecha em
# GATE_DE_SELECAO, dentro do E4 — o P13 não produz matriz nem plano no
# sentido do E5 [CLAUDE.md §4: "Gates não moram todos no E5"].
ETAPAS: tuple[Etapa, ...] = (
    Etapa(1, "intake", E1),
    Etapa(2, "confirmação de autoridade", E1),
    Etapa(3, "verificação das dependências", E1),
    Etapa(4, "ingestão controlada", E2),
    Etapa(5, "confirmação da versão", E2),
    Etapa(6, "cartografia global", E3),
    Etapa(7, "identificação das unidades", E3),
    Etapa(8, "matriz de criticidade", E4),
    Etapa(9, "matriz de seletividade", E4),
    Etapa(10, "seleção de unidades comentáveis", E4),
    Etapa(11, "verificação de fontes", E4),
    Etapa(12, "verificação de evidências", E4),
    Etapa(13, "verificação de voz", E4),
    Etapa(14, "verificação de privacidade", E4),
    Etapa(15, "identificação de problemas sistêmicos", E4),
    Etapa(16, "elaboração de comentários-matriz", E6),
    Etapa(17, "elaboração de comentários individuais", E6),
    Etapa(18, "elaboração de remissões", E6),
    Etapa(19, "verificação de densidade", E7),
    Etapa(20, "verificação de repetição", E7),
    Etapa(21, "verificação de acionabilidade", E7),
    Etapa(22, "verificação de tom", E7),
    Etapa(23, "verificação de gates", E7),
    Etapa(24, "consolidação", E7),
    Etapa(25, "auditoria final", E7),
    Etapa(26, "decisão autoral", None),
    Etapa(27, "homologação documental", None),
    Etapa(28, "piloto Word real posterior", None),
    Etapa(29, "ativação operacional posterior", None),
)

# §32.1 (6) + §32.2 (11) = 17 gates. Posição: não declarada para nenhum —
# inclusive GATE_DE_SELECAO, que não tem definição alguma na fonte.
GATES: tuple[Gate, ...] = (
    Gate("GATE_DE_ATIVACAO_P13", ClasseDeGate.DOCUMENTAL),
    Gate("GATE_DE_VERSAO", ClasseDeGate.DOCUMENTAL),
    Gate("GATE_DE_ANCORAGEM", ClasseDeGate.DOCUMENTAL),
    Gate("GATE_DE_CARTOGRAFIA", ClasseDeGate.DOCUMENTAL),
    Gate("GATE_DE_SELECAO", ClasseDeGate.DOCUMENTAL),
    Gate("GATE_DE_VALIDACAO_FINAL", ClasseDeGate.DOCUMENTAL),
    Gate("GATE_DE_REESCRITA_FORTE", ClasseDeGate.HUMANO_EXPRESSO),
    Gate("GATE_DE_ALTERACAO_DE_ARGUMENTO", ClasseDeGate.HUMANO_EXPRESSO),
    Gate("GATE_DE_ALTERACAO_DE_CORPUS", ClasseDeGate.HUMANO_EXPRESSO),
    Gate("GATE_DE_ALTERACAO_DE_METODO", ClasseDeGate.HUMANO_EXPRESSO),
    Gate("GATE_DE_ALTERACAO_DE_OBJETIVO", ClasseDeGate.HUMANO_EXPRESSO),
    Gate("GATE_DE_ALTERACAO_DE_HIPOTESE", ClasseDeGate.HUMANO_EXPRESSO),
    Gate("GATE_DE_ALTERACAO_DE_RESULTADO", ClasseDeGate.HUMANO_EXPRESSO),
    Gate("GATE_DE_ALTERACAO_DE_CONCLUSAO", ClasseDeGate.HUMANO_EXPRESSO),
    Gate("GATE_DE_TRATAMENTO_DE_PRIVACIDADE", ClasseDeGate.HUMANO_EXPRESSO),
    Gate("GATE_DE_CONSOLIDACAO", ClasseDeGate.HUMANO_EXPRESSO),
    Gate("GATE_DE_HOMOLOGACAO", ClasseDeGate.HUMANO_EXPRESSO),
)

# §6.1 — 18 entradas obrigatórias. Itens 9 e 12 carregam qualificador
# dentro da própria lista de obrigatórias.
ENTRADAS_MINIMAS: tuple[str, ...] = (
    "document_id",
    "document_version",
    "tipo de documento",
    "unidade ou conjunto de unidades autorizadas",
    "finalidade dos comentários",
    "autoridade do solicitante",
    "nível de intervenção autorizado",
    "perfil formativo",
    "perfil de voz aplicável ou condição de ausência",
    "classificação de privacidade",
    "dependências P02–P09",
    "referência ao diagnóstico de origem, quando houver",
    "instrução sobre cartografia global",
    "definição de escopo",
    "indicação de versões concorrentes",
    "original preservado",
    "critério de rastreabilidade",
    "política aplicável de fontes e evidências",
)

# §7 — 9 condições sob as quais não se deve comentar.
PRECONDICOES: tuple[str, ...] = (
    "não comentar quando a unidade não está disponível",
    "não comentar quando a âncora é indeterminável",
    "não comentar quando a versão é concorrente",
    "não comentar quando o diagnóstico depende de fonte não acessada",
    "não comentar quando o comentário exigiria exposição indevida",
    "não comentar quando o pedido exige comentar mecanicamente todas as unidades",
    "não comentar quando o pedido exige reescrita substitutiva",
    "não comentar quando o comentário solicitado está fora do nível autorizado",
    "não comentar quando não há contexto suficiente para determinar o problema",
)

# §6.3 — entradas opcionais. Estas são a superfície editável pelo
# professor [CLAUDE.md §9]; ficam nomeadas aqui porque são o único ponto
# do acervo em que o contrato admite calibragem sem alterar código.
ENTRADAS_OPCIONAIS: tuple[str, ...] = (
    "limite de comentários desejado, desde que não seja quota obrigatória",
    "prioridades do autor",
    "zonas excluídas",
    "tipos de comentário autorizados",
    "glossário",
    "termos preferidos",
    "exemplos de comentários aceitos",
    "histórico de resolução",
    "lista de problemas sistêmicos conhecidos",
    "nível de detalhamento",
    "preferência de tom",
)

DECLARACAO = DeclaracaoDeFuncao(
    funcao_id=FuncaoId.F04,
    component_id="P13",
    denominacao="Comentários Word humanos e seletivos",
    arquivo_fonte=ARQUIVO_FONTE,
    objetivo=(
        "Produzir comentários destinados à inserção posterior em documentos Word: humanos, "
        "seletivos, substantivos, acionáveis, proporcionais, rastreáveis, reversíveis e "
        "ancorados em evidência [§2]. Utiliza o documento integral para cartografia global "
        "quando necessário, mas só produz comentários sobre unidades autorizadas [§2]."
    ),
    entradas_minimas=ENTRADAS_MINIMAS,
    precondicoes=PRECONDICOES,
    decisoes=(
        "Etapa 10 — seleção de unidades comentáveis [§43]",
        "Oito resultados de seleção: COMENTAR, NAO_COMENTAR_SEM_PROBLEMA_MATERIAL, "
        "NAO_COMENTAR_POR_REPETICAO, REMETER_A_COMENTARIO_MATRIZ, AGUARDAR_EVIDENCIA, "
        "AGUARDAR_GATE, ABSTER_SE, BLOQUEADO — internos, não substituem status P09 [§10]",
        "Critério, verbatim: um comentário deve ser selecionado quando o ganho de "
        "orientação for superior ao custo de poluição documental [§12]",
        "Etapa 26 — decisão autoral [§43]",
    ),
    fluxo=ETAPAS,
    gates=GATES,
    saidas=(
        "comentários individuais tipados — 15 tipos [§13]",
        "comentários-matriz para problemas sistêmicos recorrentes [§23]",
        "remissões a comentário-matriz [§23]",
        "zero comentários, quando não houver problema material — resultado legítimo [§3.31, §31.6]",
    ),
    limites=(
        "para em sinalização e recomendação: o comentário não pode, por si só, executar "
        "reescrita, fundir, cortar, substituir, reorganizar, alterar dado, argumento, "
        "corpus, método, objetivo ou conclusão [§4.4]",
        "não é função autônoma de revisão integral [§2]",
        "não duplica o contrato integral do P11 nem revisa toda a tese [§4.1]",
        "adapta densidade e tom ao nível formativo; não impõe aparato de tese [§4.2]",
        "comentário que indica gate não concede a autorização [§32]",
        "número desejado de comentários orienta contenção, nunca obriga produção artificial "
        "nem oculta risco material [§6]",
    ),
    falhas_proibidas=(
        "criar quota percentual ou numérica — PC30_SIGNIFICA_CRITICIDADE_E_NAO_QUOTA [§3.9, §34]",
        "silêncio diante de risco material — zero comentários é ilegítimo quando risco "
        "material identificado permanece sem registro [§3.32, §25]",
        "declarar fonte não aberta como conferida [§35]",
        "comentar mecanicamente todas as unidades [§25]",
        "gerar DOCX [§34]",
        "executar a ação recomendada no comentário [§35]",
        "resolver conflito autoral ou liberar dado sensível [§35]",
        "homologar [§35]",
    ),
    testes_de_aceitacao=(
        "PS13-01 a PS13-10 — cenários documentais [§45]",
        "TA13-01 a TA13-20 [§46]",
        "TESTES_VERIFICADOS_INDEPENDENTEMENTE_NESTA_VERSAO_CORRIGIDA: 0 [§51]",
        "AUDITORIA_APOS_CORRECAO_EXECUTADA: NAO [§51]",
    ),
    rastreabilidade=(
        "P13Comment.status (DRAFT→INSERTED→RESOLVED/SUPERSEDED/WITHDRAWN) não é status "
        "P09 nem InterventionRecord.disposition [§31.5.1]",
        "P13Comment.resolution (ACEITO | RECUSADO | PENDENTE_DE_DECISAO) [§31.5.2]",
        "âncora estável por unidade [§32.1, GATE_DE_ANCORAGEM]",
        "cause_code P13_CAUSE_* — não são categorias canônicas [§38]",
    ),
    dados_necessarios=(
        "unidade comentável em qualquer granularidade: capítulo, seção, subseção, bloco, "
        "parágrafo, frase, citação, nota, tabela, figura, legenda, campo de formulário [§2, §10]",
        "entradas condicionais — 20 itens, inclusive diagnóstico P11 ou P12 [§6.2]",
        "entradas opcionais — 11 itens, a superfície de calibragem do professor [§6.3]",
    ),
    dependencias_obrigatorias=("P02", "P03", "P04", "P05", "P06", "P07", "P08", "P09"),
    condicao_de_ativacao="APOS_HOMOLOGACAO_DAS_DEPENDENCIAS",
    encaminhamentos=(),
)

"""P10 — Derivação editorial de capítulo em artigos (F01).

Fonte: P10_CONTRATO_FUNCIONAL_DERIVACAO_CAPITULO_ARTIGOS_HOMOLOGADO_R01.md,
em PACOTE_FUNCAO_AVALIACAO_CRITICA_PROJETOS_R01/.

`fluxo` está VAZIO, e é assim que a fonte está. O P10 não tem análogo do
"FLUXO MODULAR" dos outros quatro contratos: não existe seção de etapas
numeradas. Existem quatro sequências ordenadas, em seções distintas e com
objetos distintos — produtos, fases de agente, ordem de redação, estados
internos. Fundi-las produziria um fluxo que o contrato não tem, e a
disciplina é não preencher lacuna por plausibilidade [CLAUDE.md §11].
Ficam registradas em `ordens_declaradas`, cada uma com sua seção e seu
objeto. Ver LACUNAS.md, LAC-FUNC-004.

O P10 também é o único que não nomeia o P11 como par: `P11` ocorre uma
vez no arquivo inteiro, em §42, como token de estado do projeto
(`P11_A_P28_NAO_INICIADOS`) — o P11 ainda não existia quando o P10 foi
redigido. Não há, portanto, encaminhamento de volta ao P11.

Nada aqui executa.
"""

from escolio.funcoes.declaracao import DeclaracaoDeFuncao, Gate, OrdemDeclarada
from escolio.funcoes.vocabulario import ClasseDeGate, FuncaoId

ARQUIVO_FONTE = "P10_CONTRATO_FUNCIONAL_DERIVACAO_CAPITULO_ARTIGOS_HOMOLOGADO_R01.md"

# §2 — o que a função deve produzir antes de qualquer redação.
PRODUTOS_ANTES_DA_REDACAO = OrdemDeclarada(
    secao="§2",
    objeto="produtos exigidos antes de qualquer redação",
    itens=(
        "cartografia do material de origem",
        "diagnóstico dos núcleos publicáveis",
        "teste de autonomia",
        "veredito de viabilidade editorial",
        "decisão humana sobre escolha e eventual fissão",
        "matriz aprovada de transposição",
        "matriz de sobreposição",
        "arquitetura do produto derivado",
    ),
)

# §4.4 — síntese funcional. Papéis funcionais (Vaquita, Baleia, Komodo),
# não pacotes numerados [§4].
SINTESE_FUNCIONAL = OrdemDeclarada(
    secao="§4.4",
    objeto="síntese funcional — fases de agente, não etapas",
    itens=(
        "VAQUITA_ESTABILIZA",
        "BALEIA_DERIVA",
        "KOMODO_AVALIA",
        "USUARIO_DECIDE_E_HOMOLOGA",
    ),
)

# §21 — ordem padrão da redação modular. Só vale depois de matriz e
# arquitetura aprovadas; não é o fluxo da função inteira.
ORDEM_DA_REDACAO_MODULAR = OrdemDeclarada(
    secao="§21",
    objeto="ordem padrão da redação modular",
    itens=(
        "corpo analítico",
        "verificação de fidelidade",
        "estabilização local",
        "módulo seguinte",
        "transições",
        "introdução",
        "conclusão",
        "título, resumo e palavras-chave",
        "verificação de sobreposição",
        "validação independente",
    ),
)

# §31 — estados internos. "Os estados abaixo são internos e não substituem
# `response.status`."
ESTADOS_INTERNOS = OrdemDeclarada(
    secao="§31",
    objeto="estados internos do P10 — não substituem response.status",
    itens=(
        "P10_NAO_INICIADO",
        "ENTRADAS_EM_VERIFICACAO",
        "MATERIAL_EM_CARTOGRAFIA",
        "MATERIAL_INSTAVEL",
        "NUCLEOS_EM_DIAGNOSTICO",
        "DIAGNOSTICO_CONCLUIDO",
        "AGUARDANDO_ESCOLHA_HUMANA",
        "NUCLEO_APROVADO",
        "FISSAO_APROVADA",
        "MATRIZ_EM_ELABORACAO",
        "AGUARDANDO_APROVACAO_DA_MATRIZ",
        "MATRIZ_APROVADA",
        "ARQUITETURA_EM_ELABORACAO",
        "AGUARDANDO_APROVACAO_DA_ARQUITETURA",
        "ARQUITETURA_APROVADA",
        "REDACAO_MODULAR_AUTORIZADA",
        "REDACAO_MODULAR_EM_CURSO",
        "VALIDACAO_PENDENTE",
        "PILOTO_CONCLUIDO",
        "APTO_PARA_AUDITORIA",
        "AUDITADO",
        "HOMOLOGADO",
        "ABSTENCAO_INTERNA",
    ),
)

# §29.2 (8) + §29.3 (4) = 12 gates nomeados.
# §29.1 declara a classe "automaticamente verificáveis" mas NÃO nomeia
# gate algum — lista itens conferíveis (campos obrigatórios,
# correspondência de identificadores, integridade de versões). A classe
# fica sem membro, e é assim que a fonte está.
GATES: tuple[Gate, ...] = (
    Gate("GATE_DE_ESCOLHA_DE_NUCLEO", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_FISSAO", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_MATRIZ", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_ARQUITETURA", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_REDACAO", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_EXPANSAO_RESIDUAL", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_INTERVENCAO_FORTE", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_HOMOLOGACAO", ClasseDeGate.DECISAO_HUMANA_EXPRESSA),
    Gate("GATE_DE_ATIVACAO_P10", ClasseDeGate.VALIDACAO_DOCUMENTAL),
    Gate("GATE_DE_ESTABILIDADE", ClasseDeGate.VALIDACAO_DOCUMENTAL),
    Gate("GATE_DE_DIAGNOSTICO", ClasseDeGate.VALIDACAO_DOCUMENTAL),
    Gate("GATE_DE_VALIDACAO", ClasseDeGate.VALIDACAO_DOCUMENTAL),
)

# §6 é escalonado e cumulativo: §6.1 diagnóstico (13), §6.2 matriz (8,
# "Além das entradas anteriores"), §6.3 redação (7, idem).
ENTRADAS_DIAGNOSTICO: tuple[str, ...] = (
    "material integral de origem",
    "project_id",
    "identificação da versão",
    "sumário ou arquitetura da obra",
    "função do capítulo",
    "problema, objetivo e argumento",
    "bibliografia",
    "fontes documentais",
    "estado de estabilização",
    "finalidade editorial",
    "autorização para diagnóstico",
    "dependências P02–P09",
    "evidências verificadas de satisfação das dependências",
)

ENTRADAS_MATRIZ: tuple[str, ...] = (
    "núcleos candidatos",
    "testes de autonomia",
    "decisão humana",
    "inventário de unidades",
    "mapa de afirmações e evidências",
    "material compartilhado",
    "material residual",
    "nível de intervenção autorizado",
)

ENTRADAS_REDACAO: tuple[str, ...] = (
    "matriz aprovada",
    "arquitetura aprovada",
    "autorização expressa",
    "perfil de voz",
    "pendências BVAA",
    "nível P06 autorizado",
    "critérios editoriais materialmente verificados, quando disponíveis",
)

# §7 — 11 pré-condições.
PRECONDICOES: tuple[str, ...] = (
    "P02–P09 homologados",
    "material acessível",
    "versão identificada",
    "material suficientemente estabilizado",
    "escopo delimitado",
    "finalidade editorial declarada",
    "autoridade compatível",
    "nível de intervenção autorizado",
    "proveniência preservada",
    "tratamento de segurança e privacidade",
    "dependências satisfeitas por evidência verificável",
)

DECLARACAO = DeclaracaoDeFuncao(
    funcao_id=FuncaoId.F01,
    component_id="P10",
    denominacao="Derivação editorial de capítulo em artigos",
    arquivo_fonte=ARQUIVO_FONTE,
    objetivo=(
        "Avaliar se um capítulo, seção extensa ou conjunto textual academicamente "
        "estabilizado contém um ou mais núcleos publicáveis suficientemente autônomos para "
        "originar artigos ou outros produtos editoriais derivados [§2]. Não é resumidor, "
        "divisor mecânico de capítulos, gerador automático de artigos nem mecanismo de "
        "conversão de extensão textual em quantidade presumida de publicações [§2]."
    ),
    entradas_minimas=ENTRADAS_DIAGNOSTICO + ENTRADAS_MATRIZ + ENTRADAS_REDACAO,
    precondicoes=PRECONDICOES,
    decisoes=(
        "escolha do núcleo definitivo — GATE_DE_ESCOLHA_DE_NUCLEO [§13, §29.2]",
        "execução da fissão — GATE_DE_FISSAO [§13, §29.2]",
        "promoção de material residual — GATE_DE_EXPANSAO_RESIDUAL [§19, §29.2]",
        "quem autoriza: USUARIO_PROPONENTE, ou orientador/autoridade delegada "
        "nos limites da delegação [§5]",
    ),
    fluxo=(),
    gates=GATES,
    saidas=(
        "cartografia do material de origem",
        "diagnóstico de núcleos publicáveis",
        "teste de autonomia",
        "veredito de viabilidade editorial",
        "matriz de transposição",
        "matriz de sobreposição",
        "arquitetura do produto derivado",
    ),
    limites=(
        "sem núcleo publicável não há redação; sem matriz aprovada não há redação [§3.5-6]",
        "não escolhe núcleo definitivo nem executa fissão autonomamente [§30]",
        "não corta, funde, reorganiza macroestrutura nem promove residual [§30]",
        "não altera o original nem seleciona periódico definitivo [§30]",
        "não substitui, reduz nem redefine P03–P09 [§3, invariante 17]",
        "gate satisfeito não constitui autorização universal para etapas posteriores [§29.4]",
    ),
    falhas_proibidas=(
        "invenção bibliográfica [§16]",
        "invenção de exigência editorial [§16]",
        "uso de fonte-coringa [§16]",
        "supressão de proveniência [§16]",
        "autoauditoria [§16]",
        "homologação pelo executor [§16]",
        "dividir por contagem ou forçar dois artigos [P02, limites de F01]",
    ),
    testes_de_aceitacao=(
        "PS-01 a PS-10 — PILOTO_SUPERVISIONADO, dez cenários abstratos [§35]",
        "PS-10 é o critério central: versões concorrentes sem decisão canônica devem "
        "resultar exclusivamente em BLOCKED/GOVERNANCE_CONFLICT [§35]",
        "TA-01 a TA-20, declarados APROVADO, com a ressalva de que nenhum teste foi "
        "reexecutado, reavaliado ou reformulado [§37.1]",
    ),
    rastreabilidade=(
        "correspondência obrigatória de request_id, project_id, component_id "
        "e function_id [§27]",
        "gate registrado por registro da matriz de transposição [§14]",
        "estados internos não substituem response.status [§31]",
        "vereditos de diagnóstico não são status canônicos de resposta [§12]",
    ),
    dados_necessarios=(
        "entradas opcionais — 7 itens; não podem ser presumidas [§6.4]",
        "três patamares de estabilidade: ESTAVEL_PARA_DIAGNOSTICO, "
        "ESTAVEL_PARA_TRANSPOSICAO, ESTAVEL_PARA_REDACAO, INSTAVEL [§8]",
    ),
    dependencias_obrigatorias=("P02", "P03", "P04", "P05", "P06", "P07", "P08", "P09"),
    condicao_de_ativacao="APOS_HOMOLOGACAO_DAS_DEPENDENCIAS",
    ordens_declaradas=(
        PRODUTOS_ANTES_DA_REDACAO,
        SINTESE_FUNCIONAL,
        ORDEM_DA_REDACAO_MODULAR,
        ESTADOS_INTERNOS,
    ),
    encaminhamentos=(),
)

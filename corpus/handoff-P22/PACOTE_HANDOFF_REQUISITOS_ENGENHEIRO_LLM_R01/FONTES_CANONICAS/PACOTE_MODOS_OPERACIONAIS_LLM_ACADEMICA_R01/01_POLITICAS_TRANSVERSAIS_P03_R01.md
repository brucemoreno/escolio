# POLÍTICAS TRANSVERSAIS — P03 R01

## Identificação

- Projeto: `LLM_ACADEMICA`
- Componente: `P03 — NÚCLEO TRANSVERSAL OBRIGATÓRIO`
- Fase: `F2`
- Categoria: `POLITICAS`
- Estado: `EXECUTADO_DOCUMENTALMENTE; NÃO AUDITADO; NÃO HOMOLOGADO`
- Proveniência: R03 homologada e congelada; P02 homologado; P00 e P01 homologados e congelados.

## Políticas

### POL-001 — Estado canônico único
- **finalidade:** Assegurar que cada componente possua um estado documental único e verificável.
- **escopo:** Todo o projeto e todos os componentes P00-P28.
- **objetos_afetados:** Pacotes, termos, manifestos, recibos e matrizes.
- **autoridade_competente:** USUARIO_PROPONENTE para homologação; Executor apenas registra.
- **gatilho:** Criação, auditoria, homologação, congelamento, reabertura ou substituição.
- **estado_de_entrada:** ESTADO_DECLARADO_E_EVIDENCIADO
- **acao_permitida:** Registrar estado com evidência e precedência.
- **acao_proibida:** Inferir estado, declarar homologação própria ou usar comando vago como transição.
- **estado_de_saida:** ESTADO_CANONICO_REGISTRADO
- **evidencia_exigida:** Objeto material, hash, termo ou parecer aplicável.
- **condicao_de_erro:** Estados concorrentes sem regra de precedência.
- **reversibilidade:** SIM, mediante restauração ao último estado homologado.
- **proveniencia:** R03; P00; P01
- **dependencias:** P00;P01;P02

### POL-002 — Gates e autoridades
- **finalidade:** Impedir transições sem dependências e autoridade competentes.
- **escopo:** Todas as fases F0-F8.
- **objetos_afetados:** Componentes, fases, entregas e handoffs.
- **autoridade_competente:** USUARIO_PROPONENTE; Auditor emite veredito sem homologar.
- **gatilho:** Gate explícito satisfeito e autorização específica.
- **estado_de_entrada:** DEPENDENCIAS_HOMOLOGADAS
- **acao_permitida:** Executar somente o componente autorizado.
- **acao_proibida:** Iniciar componente posterior, ampliar escopo ou autorizar transversalmente.
- **estado_de_saida:** COMPONENTE_EXECUTADO_NAO_HOMOLOGADO
- **evidencia_exigida:** Termos de homologação, comando específico e matriz de dependências.
- **condicao_de_erro:** Dependência ausente, não homologada ou contraditória.
- **reversibilidade:** SIM, retorno ao estado anterior sem apagar evidências.
- **proveniencia:** R03 matriz de dependências e papéis
- **dependencias:** POL-001

### POL-003 — Modularidade e autonomia
- **finalidade:** Preservar componentes separados, testáveis e substituíveis.
- **escopo:** P00-P28.
- **objetos_afetados:** Pacotes e contratos por componente.
- **autoridade_competente:** USUARIO_PROPONENTE para decidir fusão; fusão não autorizada no P03.
- **gatilho:** Execução de componente individual.
- **estado_de_entrada:** COMPONENTE_AUTORIZADO
- **acao_permitida:** Produzir saída própria sem alterar outros componentes.
- **acao_proibida:** Fundir IDs, lotes, funções, profiles, contextos ou componentes.
- **estado_de_saida:** COMPONENTE_ISOLADO_PRODUZIDO
- **evidencia_exigida:** Inventário canônico e mapa de proveniência.
- **condicao_de_erro:** Saída depende de alteração não autorizada em outro componente.
- **reversibilidade:** SIM, por descarte da revisão não homologada.
- **proveniencia:** R03 inventário; P02 catálogo
- **dependencias:** POL-001;POL-002

### POL-004 — Separação de papéis
- **finalidade:** Evitar concentração de elaboração, execução, auditoria e homologação.
- **escopo:** Todos os chats e papéis do projeto.
- **objetos_afetados:** Comandos, produtos, pareceres e termos.
- **autoridade_competente:** Matriz de papéis R03.
- **gatilho:** Atribuição explícita no componente.
- **estado_de_entrada:** PAPEL_IDENTIFICADO
- **acao_permitida:** Atuar somente dentro da competência.
- **acao_proibida:** Executor auditar/homologar; Auditor corrigir; Arquiteto implementar.
- **estado_de_saida:** RESPONSABILIDADE_SEGREGADA
- **evidencia_exigida:** Registro do papel, comando e destinatário.
- **condicao_de_erro:** Mesmo agente executa funções incompatíveis.
- **reversibilidade:** SIM, redistribuição e nova execução controlada.
- **proveniencia:** R03 matriz de papéis; P00 governança
- **dependencias:** POL-002

### POL-005 — Proveniência e rastreabilidade
- **finalidade:** Manter vínculo entre cada decisão, dado e artefato e sua fonte.
- **escopo:** Todos os artefatos.
- **objetos_afetados:** Arquivos, campos, decisões, lacunas e versões.
- **autoridade_competente:** Executor registra; Auditor verifica; Usuário decide.
- **gatilho:** Uso, cópia, consolidação ou transformação documental.
- **estado_de_entrada:** FONTE_MATERIAL_IDENTIFICADA
- **acao_permitida:** Registrar nome, hash, versão, operação e limite.
- **acao_proibida:** Preencher lacunas, omitir origem ou atribuir proveniência não comprovada.
- **estado_de_saida:** RASTREABILIDADE_REGISTRADA
- **evidencia_exigida:** Hash, localizador, manifesto e mapa de proveniência.
- **condicao_de_erro:** Fonte ausente, incompatível ou não verificável.
- **reversibilidade:** SIM, remoção da derivação não homologada e restauração da fonte.
- **proveniencia:** R03 mapa de cobertura; P00 mapa de proveniência
- **dependencias:** POL-001

### POL-006 — Congelamento, reabertura e reversibilidade
- **finalidade:** Proteger versões homologadas e permitir reabertura excepcional controlada.
- **escopo:** Componentes homologados e congelados.
- **objetos_afetados:** Pacotes, termos e revisões.
- **autoridade_competente:** USUARIO_PROPONENTE após evidência e auditoria aplicável.
- **gatilho:** Erro material novo com impacto comprovado e autorização expressa.
- **estado_de_entrada:** HOMOLOGADO_E_CONGELADO
- **acao_permitida:** Criar revisão sucessora preservando versão anterior.
- **acao_proibida:** Editar objeto congelado, reabrir por preferência ou apagar histórico.
- **estado_de_saida:** REABERTO_SOB_AUTORIZACAO ou NOVA_REVISAO_NAO_HOMOLOGADA
- **evidencia_exigida:** Erro material documentado, impacto e comando específico.
- **condicao_de_erro:** Ausência de novidade material ou de autoridade.
- **reversibilidade:** SIM, retorno à versão congelada anterior.
- **proveniencia:** R03 estado/travas; P01; P00
- **dependencias:** POL-001;POL-005

### POL-007 — Comandos vagos
- **finalidade:** Impedir que expressões genéricas produzam transições de fase.
- **escopo:** Todos os chats.
- **objetos_afetados:** Mensagens como prossiga, continue, execute e equivalentes.
- **autoridade_competente:** USUARIO_PROPONENTE mediante comando específico.
- **gatilho:** Recebimento de comando sem objeto, escopo ou gate inequívocos.
- **estado_de_entrada:** AGUARDANDO_COMANDO_ESPECIFICO
- **acao_permitida:** Manter estado e solicitar/aguardar autorização específica.
- **acao_proibida:** Inferir próxima fase, componente ou operação.
- **estado_de_saida:** ESTADO_PRESERVADO
- **evidencia_exigida:** Registro do comando e do último estado seguro.
- **condicao_de_erro:** Execução iniciada sem autorização específica.
- **reversibilidade:** SIM, interromper e restaurar último estado seguro.
- **proveniencia:** P01 protocolo de comandos vagos; R03
- **dependencias:** POL-001;POL-002

### POL-008 — Divergências e materialidade
- **finalidade:** Distinguir divergência material, formal e não comprovada.
- **escopo:** Auditorias, hashes, nomes e conteúdo.
- **objetos_afetados:** Pacotes, manifestos, recibos e relatórios.
- **autoridade_competente:** Auditor classifica; Usuário decide reabertura.
- **gatilho:** Detecção de inconsistência.
- **estado_de_entrada:** DIVERGENCIA_DETECTADA
- **acao_permitida:** Material: bloquear; formal sem impacto: registrar; não comprovada: não reabrir.
- **acao_proibida:** Tratar toda diferença como bloqueador ou ignorar impacto material.
- **estado_de_saida:** BLOQUEADO ou CONCLUIDO_COM_RESSALVA ou ESTADO_PRESERVADO
- **evidencia_exigida:** Comparação material, hash, conteúdo e impacto.
- **condicao_de_erro:** Classificação sem evidência.
- **reversibilidade:** SIM conforme classe e decisão.
- **proveniencia:** R03 travas; P00; P01
- **dependencias:** POL-005;POL-006

### POL-009 — Isolamento entre projetos
- **finalidade:** Evitar importação de conteúdo, decisões ou memória de outros projetos.
- **escopo:** Projeto LLM_ACADEMICA.
- **objetos_afetados:** Arquivos, prompts, memórias, exemplos e decisões.
- **autoridade_competente:** USUARIO_PROPONENTE pode autorizar importação explícita.
- **gatilho:** Detecção de origem externa.
- **estado_de_entrada:** ORIGEM_EXTERNA_DETECTADA
- **acao_permitida:** Interromper, segregar e solicitar autorização específica.
- **acao_proibida:** Misturar, adaptar silenciosamente ou usar conteúdo externo.
- **estado_de_saida:** CONTEUDO_SEGREGADO
- **evidencia_exigida:** Proveniência explícita e autorização de importação.
- **condicao_de_erro:** Origem duvidosa ou cruzamento não autorizado.
- **reversibilidade:** SIM, remover conteúdo externo e restaurar estado.
- **proveniencia:** R03; P01 trava antideriva
- **dependencias:** POL-005

### POL-010 — Interrupção, retomada e restauração
- **finalidade:** Permitir retomada sem perda de contexto ou deriva.
- **escopo:** Chats inativos, migrados ou interrompidos.
- **objetos_afetados:** Estado, pacotes, hashes, próxima ação e proibições.
- **autoridade_competente:** Executor restaura somente sob protocolo; Usuário autoriza execução subsequente.
- **gatilho:** Inatividade, migração, perda de contexto ou bloqueio.
- **estado_de_entrada:** INTERROMPIDO ou CONTEXTO_INCOMPLETO
- **acao_permitida:** Reconstituir estado a partir de objetos canônicos e emitir recibo.
- **acao_proibida:** Continuar por memória parcial ou iniciar fase automaticamente.
- **estado_de_saida:** ESTADO_RESTAURADO_AGUARDANDO_AUTORIZACAO
- **evidencia_exigida:** Pacote canônico, termos, hashes e último ponto seguro.
- **condicao_de_erro:** Objeto obrigatório ausente ou divergente.
- **reversibilidade:** SIM, retorno ao último estado confirmado.
- **proveniencia:** P01 protocolos de reativação/restauração; R03
- **dependencias:** POL-001;POL-005;POL-007

### POL-011 — Substituição e preservação histórica
- **finalidade:** Controlar precedência sem apagar versões anteriores.
- **escopo:** Todas as revisões e pacotes.
- **objetos_afetados:** R01, R02, R03 e sucessoras.
- **autoridade_competente:** USUARIO_PROPONENTE após auditoria quando exigida.
- **gatilho:** Nova revisão aprovada e homologada.
- **estado_de_entrada:** REVISAO_NOVA_NAO_HOMOLOGADA
- **acao_permitida:** Preservar predecessoras e declarar precedência somente após homologação.
- **acao_proibida:** Sobrescrever, apagar, reativar invalidado ou declarar substituição antecipada.
- **estado_de_saida:** REVISAO_HOMOLOGADA_CONTROLADORA
- **evidencia_exigida:** Termo de homologação, hash e matriz de precedência.
- **condicao_de_erro:** Nova versão sem homologação ou sem preservação do histórico.
- **reversibilidade:** SIM, restauração da controladora anterior.
- **proveniencia:** R03; P00 matriz de precedência
- **dependencias:** POL-005;POL-006

### POL-012 — Próxima ação única
- **finalidade:** Reduzir deriva operacional e ciclos recursivos.
- **escopo:** Todos os fechamentos de componente.
- **objetos_afetados:** Recibos, pareceres e handoffs.
- **autoridade_competente:** USUARIO_PROPONENTE define a próxima ação.
- **gatilho:** Conclusão, bloqueio ou interrupção.
- **estado_de_entrada:** ETAPA_ENCERRADA
- **acao_permitida:** Registrar exatamente uma próxima ação permitida ou nenhuma automática.
- **acao_proibida:** Oferecer múltiplas ações simultâneas ou executar encadeamento automático.
- **estado_de_saida:** AGUARDANDO_ACAO_UNICA
- **evidencia_exigida:** Estado final e comando subsequente específico.
- **condicao_de_erro:** Mais de uma transição operacional ativa.
- **reversibilidade:** SIM, cancelar ações excedentes.
- **proveniencia:** R03; P00; P01
- **dependencias:** POL-002;POL-007

## Limites

- Estas políticas não alteram o catálogo funcional P02.
- Não definem arquitetura, modelo, fornecedor, plataforma ou infraestrutura.
- Não autorizam P04-P28, treinamento, RAG, fine-tuning, implementação ou pilotos.
- Não homologam o P03.

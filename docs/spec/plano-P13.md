# Plano de sessões — P13 (Comentários Word Humanos e Seletivos)

Fonte: `CLAUDE.md`; `docs/spec/funcoes-P10-P14.md` §P13; contrato
`corpus/handoff-P22/.../PACOTE_FUNCAO_COMENTARIOS_AUDITORIA_POR_BLOCOS_R01/
P13_CONTRATO_FUNCIONAL_COMENTARIOS_WORD_HOMOLOGADO_R01.md`.

Este documento fixa a ordem de construção do P13 em sessões — cada uma com tema único e
entregável verificável [CLAUDE.md §11, "uma sessão, um tema"] — para não se perder entre
sessões. Nenhuma etapa aqui grava código; isto é o plano, não a execução.

## Por que esta ordem

O contrato não permite pular etapas: "diagnóstico global precede seleção local"
[P13 invariante 14] e a matriz de criticidade/seletividade precede a formulação de comentário,
que precede consolidação, que precede envelope e roteamento — ordem do fluxo modular
`[P13 §43]`. Cada sessão abaixo é um desses degraus.

**Revisão de 2026-08-08:** a sessão de privacidade (P08) foi retirada da sequência principal e
adiada — ver §"Sessão adiada" abaixo. As sessões 7 a 11 (renumeradas 6 a 10 nesta versão) foram
auditadas uma a uma e **nenhuma depende estruturalmente dela**; construir a integração de
privacidade com tipo frouxo antes de `CO-012`/`CO-013` seria gastar uma sessão em algo que essas
duas decisões provavelmente invalidam depois.

## Ordem final e dependências

| # | Sessão (tema único) | Entregável verificável | Precisa que já exista | Bloqueio |
|---|---|---|---|---|
| 1 | Schema `P13Comment` + enums (`status`, `resolution`, `related_comment_id`, `matrix_comment_id`) [§31.5, §42] | Módulo `escolio/comentarios/` com o schema e testes das regras de nulidade/referência | Convenção de estilo do P05 | Nenhum |
| 2 | Matriz de criticidade (12 eixos) + matriz de seletividade (10 fatores) [§11, §12] | Estrutura de dados + classificação determinística; testes PS13-01, TA13-05, TA13-16 | Sessão 1; convenção de `unit_id` da ingestão (fixtures sintéticas) | Nenhum |
| 3 | Catálogo dos 15 tipos de comentário + templates estruturais [§13, §15–18] | Validador por `comment_type`; testes TA13-06 a TA13-09 | Sessão 1 | Nenhum |
| 4 | Integração P04/P05 — comentário bibliográfico e de evidência [§19, §20, §26, §27] | Adaptador BVAA/P05 → `source_status`/`claim_id`/`evidence_ids`; testes PS13-05, PS13-06, TA13-10, TA13-11 | Sessões 1, 3; `escolio/bvaa/`, schema P05 | Nenhum; carrega `CON-P05-001` (três vocabulários) como lacuna a documentar, não a resolver |
| 5 | Integração P06/P07 — nível de intervenção e voz do **autor avaliado** [§4.4, §4.5, §28, §29] | Preenchimento de `intervention_level`/`authority_required`/`gate`/`voice_impact`; testes PS13-07, PS13-08, TA13-12, TA13-20 | Sessões 1, 3; `escolio/intervencao/`, `escolio/voz/` (voz do autor) | Nenhum — voz de "quem comenta" [§13.1 do CLAUDE.md, aberto] não entra aqui |
| 6 | Comentário-matriz e remissões [§23, §24] | Algoritmo de consolidação; testes PS13-04, TA13-14, TA13-15 | Sessões 2, 3 | Nenhum |
| 7 | Auditoria final interna — densidade, repetição, acionabilidade, tom, gates [§25, §44] | Checklist rodando os itens de `§44` exceto o item 15 (privacidade); testes TA13-17, TA13-18, TA13-19 | Sessões 2–6 | Item 15 do checklist (`privacidade P08`) fica `N/A` até a sessão de privacidade rodar — não impede o restante |
| 8 | Extensão do envelope P09 — `P13RequestExtension`/`P13ResultExtension`/payloads [§31.1–31.4, §31.6] | Builders de request/response; testes de forma dos payloads `ABSTAINED`/`BLOCKED`/`ERROR` | Sessões 1–7; `escolio/contrato/` | Não corrige `BL-011`/`BL-013` como efeito colateral — são pendências de outras peças, só herdadas aqui |
| 9 | Módulo P13 no roteador — "um módulo por função" — **JÁ EXISTIA, ver nota abaixo** | `escolio/funcoes/p13.py` análogo aos outros cinco; testes com `classification.functions=["P13"]` sintético | Sessão 8; `escolio/funcoes/` | Ativação real inerte por `BL-014` (ato humano, fora do escopo de código) |
| 10 | Suíte integrada — 10 cenários `PS13` + 20 testes `TA13`, fim a fim | 18/20 testes e 9/10 cenários rodando; `PS13-09` e `TA13-13` marcados `PENDENTE — bloqueado por CO-012/CO-013` (não fabricados); `LACUNAS.md` do módulo P13 | Sessões 1–9 | Cobertura completa (10/10, 20/20) só fecha depois da sessão adiada |

## Nota de 2026-08-09 — sessão 9 já construída antes deste plano prever a sessão

`escolio/funcoes/p13.py` **já existe** desde a sessão do roteador de função ("peça 6" do
roadmap principal, `CLAUDE.md §14`, 2026-08-07) — anterior à primeira sessão deste plano P13
(sessão 1, `escolio/comentarios/`). É `DeclaracaoDeFuncao` completa: 29 etapas [§43], 17 gates
[§32.1, §32.2], 18 entradas mínimas [§6.1], 9 precondições [§7], `dependencias_obrigatorias`
P02-P09, sem depender de P11/P12. Testado em `tests/funcoes/test_modulos_de_funcao.py` (contagens
e etapas verbatim) e `tests/funcoes/test_roteador.py` (rotear/verificar_material com
`classification.functions` sintético — valor real é `["LLM-ACA-F04"]`, o identificador do P02
para o P13, não a string literal `"P13"`; ver `LAC-FUNC-002` no namespace `component_id` vs.
`function_id`). `test_rotear_requisicao_coerente_valido` já exercita exatamente o cenário que
esta sessão pedia: material declarado sinteticamente para F04/P13, roteado sem exceção.

Mais além disso, `tests/integracao/test_pipeline_p13.py` (sessão avulsa de teste de integração,
2026-08-09, anterior a esta constatação) já percorre roteador → matriz de criticidade → matriz
de seletividade → `RegistroDeComentarios`, com material declarado e indeterminado. Essa sessão
registrou `BL-021`/`BL-022` em `docs/backlog.md`: **não existe orquestrador** ligando
`escolio/funcoes/p13.py` a `escolio/comentarios/` — `escolio/comentarios/` não importa nada de
`escolio/funcoes/` nem de `escolio/contrato/` — e o professor confirmou, na mesma data, que
construir esse orquestrador é **decisão de arquitetura, não correção**, não executada sem
instrução própria.

**Consequência para esta sessão 9:** o entregável literal do plano (`escolio/funcoes/p13.py`
análogo aos outros cinco + testes com `functions` sintético) está feito, com origem anterior a
este documento. O que o plano parecia esperar além disso — o módulo "no roteador" *funcionando*
com as peças de `escolio/comentarios/` — é exatamente `BL-021`, já registrado e já recusado.
Nenhum código foi alterado nesta sessão; só este registro e a linha da tabela acima.

## Sessão adiada — Integração P08 (privacidade do comentário)

**Tema:** preencher `privacy_classification` e o caminho `ABSTAINED/PRIVACY_RISK` do P13
[§22, §30], cobrindo `PS13-09` e `TA13-13`.

**Por que foi tirada da sequência principal:** `CO-012` (tipo de `sensitivity`/
`privacy_classification` — `SensitivityLabel` tipado vs. campo frouxo) e `CO-013`
(`classification.state` sem valor correto em fonte alguma) travam exatamente os passos 5 e 6
do protocolo `[P08 §12]` que esta sessão consumiria. `BL-018` soma-se: `InputItem.security` não
tem onde expressar "ainda não analisado", só o registro externo `RegistroDeAnalise` tem esse
estado.

**Decisão registrada nesta sessão de planejamento:** não construir com tipo frouxo. Aguardar
resposta do professor a `CO-012` e `CO-013` (registradas em `docs/coleta.md` e
`docs/spec/divergencias.md` §4.6) antes de abrir esta sessão.

**Quando destravar:** ao decidir `CO-012`/`CO-013`, esta sessão roda usando `escolio/seguranca/`
(`RegistroDeAnalise`) como fonte de verdade (contorno ao `BL-018`, não solução dele) e depois
retorna à Sessão 10 para fechar os dois itens pendentes da suíte.

## Fora de qualquer sessão de código, por agora

Piloto Word real e ativação operacional `[§47–48]` não são sessão de engenharia: dependem de
homologação documental do contrato (ato do `USUARIO_PROPONENTE`) e de um documento acadêmico
real para testar ancoragem. **Não existe nenhum `.docx` de P13 em `data/`** — mesmo padrão do
`CO-009` para P10, material referenciado mas nunca entregue. Gerar DOCX antes disso é ação
proibida por contrato `[§34.18-19]`, não lacuna técnica.

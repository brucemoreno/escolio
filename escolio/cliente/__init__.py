"""escolio.cliente — camada de infraestrutura que chama a API da Anthropic.

Não implementa etapa de pipeline nem decide o que perguntar [CLAUDE.md §4,
§14 — isso é das funções, ainda não construídas]. Aplica como código as
regras de custo e robustez do CLAUDE.md §10 e as exigências de robustez desta
sessão (retry, timeout, erros tipados, retomada de sequência, disciplina de
log). Ver LACUNAS.md para decisões não sourceadas.

Sem reexportação aqui — importar dos submódulos diretamente (padrão já usado
em `escolio/contrato/__init__.py`), ex.: `from escolio.cliente.cliente import
ClienteAnthropic`.
"""

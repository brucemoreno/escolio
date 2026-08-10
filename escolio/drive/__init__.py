"""escolio.drive — camada de infraestrutura de leitura ao Google Drive.

Conector para a biblioteca bibliográfica do professor, compartilhada
explicitamente (nunca pública) com uma conta de serviço — mecanismo real
que resolve a parte (a) do BL-027 ("conector de leitura ao Drive").

Escopo: só leitura (`drive.readonly`). Não decide o que fazer com o
conteúdo lido — isso é do BVAA (X01/P04) e das funções, que ainda não
consomem este módulo [ver docs/backlog.md, BL-027, itens (b)-(d) em
aberto]. Ver LACUNAS.md para decisões não sourceadas.

Sem reexportação aqui — importar dos submódulos diretamente, mesmo padrão
de `escolio/cliente/__init__.py`, ex.:
`from escolio.drive.conector import construir_servico`.
"""

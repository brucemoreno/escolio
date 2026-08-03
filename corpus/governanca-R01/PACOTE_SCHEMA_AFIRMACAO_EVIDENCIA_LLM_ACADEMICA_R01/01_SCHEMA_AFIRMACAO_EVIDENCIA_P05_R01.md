# SCHEMA AFIRMAÇÃO–EVIDÊNCIA — P05 R01

## 1. Objeto
Este schema registra relações rastreáveis entre uma afirmação e uma ou mais evidências, sem transformar localização em acesso, acesso em leitura, leitura em validação, confiança em prova ou recomendação em validação.

## 2. Unidade lógica
A unidade mínima é uma **relação afirmação–evidência**. Uma afirmação pode possuir várias relações; uma evidência pode participar de várias relações. `claim_id` identifica a afirmação, `source_id` identifica a fonte/objeto evidencial e a chave composta (`claim_id`, `source_id`, `relation_version`) identifica cada relação versionada.

## 3. Princípios obrigatórios
1. **Materialidade:** estados positivos exigem evidência observável correspondente.
2. **Não promoção automática:** nenhum estado posterior é inferido de estado anterior.
3. **Separação dimensional:** identificação, localização, acessibilidade, acesso, leitura, paginação, validação, recomendação e abstenção permanecem campos/estados distintos.
4. **Suficiência ≠ confiança:** suficiência mede adequação da evidência ao uso delimitado; confiança mede robustez da avaliação registrada.
5. **Sem probabilidade como prova:** confiança alta não corrige evidência ausente ou insuficiente.
6. **Proveniência obrigatória:** toda relação registra origem, responsável, data e versão.
7. **Histórico imutável:** correções, invalidações e substituições criam versão sucessora; não apagam registros anteriores.
8. **Abstenção obrigatória:** pedido para inventar página, fonte, trecho ou evidência produz `ABSTENCAO` e `NAO_USAR`.

## 4. Estrutura mínima
Os campos canônicos são definidos no dicionário de dados. Campos obrigatórios condicionais tornam-se exigíveis quando seu gatilho ocorre. Valores desconhecidos não são preenchidos por inferência: usam valor controlado aplicável (`NAO_APLICAVEL`, `NAO_CONFIRMADO`, `DESCONHECIDO_CONTROLADO`) e nota de lacuna.

## 5. Identificadores
- `claim_id`: `CLM-<DOMINIO>-<UUID_OU_SEQUENCIA_CONTROLADA>`.
- `source_id`: `SRC-<TIPO>-<UUID_OU_SEQUENCIA_CONTROLADA>`.
- Exemplos abstratos usam `EX-CLM-001` e `EX-SRC-001` e são proibidos em produção.
- IDs nunca são reciclados, renomeados silenciosamente ou atribuídos por memória.

## 6. Estados dimensionais
- `access_state`: NÃO_LOCALIZADA, LOCALIZADA, ACESSIVEL, ACESSADA.
- `reading_state`: LEITURA_NAO_REALIZADA, LEITURA_INDIRETA, LIDA_PARCIALMENTE, LIDA_INTEGRALMENTE.
- `validation_state`: NAO_VERIFICADA, PAGINA_NAO_CONFIRMADA, PAGINA_CONFIRMADA, VALIDACAO_PENDENTE, VALIDADA, INVALIDADA_POSTERIORMENTE.
- `sufficiency`: NAO_AVALIADA, EVIDENCIA_AUSENTE, EVIDENCIA_INSUFICIENTE, EVIDENCIA_PARCIALMENTE_SUFICIENTE, EVIDENCIA_SUFICIENTE, CONFLITANTE.
- `confidence`: NAO_AVALIADA, BAIXA, MEDIA, ALTA. É vedada ALTA sem base material explicitada.
- `usage_status`: NAO_USAR, USO_CONDICIONAL, USO_LIBERADO, ABSTENCAO.

## 7. Coerência mínima
`USO_LIBERADO` exige simultaneamente: fonte identificada; acesso efetivo quando o conteúdo da fonte sustenta a afirmação; leitura suficiente; localização confirmada quando houver citação ou marcador específico; `VALIDADA`; `EVIDENCIA_SUFICIENTE`; e ausência de conflito bloqueante.

`VALIDADA` não exige sempre leitura integral: leitura parcial delimitada pode sustentar uso igualmente delimitado. Contudo, jamais pode sustentar alegação sobre a integralidade da fonte.

## 8. Múltiplas evidências e reutilização
Cada evidência recebe relação própria. A suficiência agregada da afirmação é derivada apenas por regra explícita registrada, nunca pela contagem bruta de fontes. Uma evidência reutilizada preserva o mesmo `source_id`; cada novo uso recebe relação e escopo próprios.

## 9. Conflitos e edições divergentes
Evidências conflitantes permanecem simultaneamente registradas. O conflito impede `USO_LIBERADO` até resolução ou delimitação explícita. Edições diferentes recebem `source_id` ou `edition_or_version` distintos; paginação não é transferida entre edições.

## 10. Leitura indireta e fonte parcial
Leitura indireta identifica obrigatoriamente a fonte intermediária e não autoriza declarar leitura da fonte primária. Fonte parcial deve registrar seus limites; não pode fundamentar afirmação além do segmento disponível.

## 11. Invalidação, substituição e sucessão
A invalidação posterior cria nova versão com `validation_state=INVALIDADA_POSTERIORMENTE`, preserva a versão anterior e rebaixa o uso conforme a gravidade. A substituição registra `supersedes_relation_version` nas notas/proveniência, mantém ambos os objetos e proíbe substituição silenciosa.

## 12. Rastreabilidade bidirecional
- afirmação → relações → fontes/evidências;
- fonte/evidência → relações → afirmações.
A reconstrução deve ser possível apenas com IDs, versões e registros do pacote, sem depender de memória externa.

## 13. Limites
Este P05 não define o schema geral de entrada/saída/erro/abstenção do P09, taxonomia de intervenção do P06, contrato de voz do P07, política de segurança do P08, nem tecnologia de implementação.

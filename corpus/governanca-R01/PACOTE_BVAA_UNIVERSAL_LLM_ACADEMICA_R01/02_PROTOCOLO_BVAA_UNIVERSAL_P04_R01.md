# PROTOCOLO BVAA UNIVERSAL — P04 R01

## 1. Finalidade
Estabelecer regras documentais universais para identificação de obras e edições, disponibilidade, acesso, leitura, localização, validação, recomendação, incerteza, abstenção, proveniência e preservação histórica.

## 2. Princípio central
**Sem evidência material suficiente, não se declara leitura, página, edição, DOI, ISBN, URL, citação literal, referência consolidada ou sustentação documental.**

Plausibilidade, memória, familiaridade com a obra, menção nominal, localização por título ou existência de metadado não equivalem a acesso, leitura ou validação.

## 3. Distinções obrigatórias
1. Conhecimento nominal: a obra é apenas mencionada.
2. Identificação: autor, título ou outro identificador mínimo foram registrados.
3. Identificação de edição: edição, tradução, volume, tomo ou suporte foram diferenciados.
4. Localização: há indicação material de onde o objeto pode ser encontrado.
5. Acessibilidade: há condição real de acesso.
6. Acesso: o objeto foi efetivamente aberto ou recuperado.
7. Leitura: conteúdo foi examinado em extensão declarada.
8. Localização interna: página, fólio, seção ou marcador foi materialmente confirmado.
9. Validação: a evidência foi confrontada com a afirmação ou uso proposto.
10. Recomendação: decisão explícita baseada no estado e na evidência.
11. Abstenção: interrupção obrigatória quando a comprovação for insuficiente.

## 4. Matriz de evidência
- **Nível A — evidência interna fornecida:** trecho e dados contidos no próprio pacote documental.
- **Nível B — evidência material anexada:** PDF, scan, DOCX, imagem ou arquivo acessível.
- **Nível C — evidência por ferramenta/conector efetivamente usado:** retorno observável e rastreável.
- **Nível D — evidência ausente:** memória, título provável, referência incompleta ou arquivo apenas mencionado.

O nível de evidência deve ser registrado e limita o alcance da conclusão.

## 5. Estados controlados
Os estados canônicos são os registrados em `03_MAQUINA_DE_ESTADOS_BIBLIOGRAFICOS_P04_R01.csv`. Nenhum estado posterior pode ser inferido automaticamente a partir de um estado anterior.

## 6. Autoridades
- Executor documental: registra fatos e aplica estados segundo evidência.
- Auditor independente: verifica integridade, coerência, rastreabilidade e funcionamento.
- Usuário proponente: homologa ou rejeita o produto.
- Nenhum executor pode auto-homologar, inventar evidência ou converter pendência em validação.

## 7. Regras de leitura
- LEITURA_INTEGRAL exige evidência material de acesso ao objeto completo e registro de exame integral.
- Leitura parcial não pode ser promovida a integral.
- Leitura indireta não equivale à leitura da obra primária.
- PDF acessado sem exame de conteúdo permanece LEITURA_NAO_REALIZADA.

## 8. Regras de localização e paginação
- Página do arquivo, página impressa, fólio, seção e marcador digital devem ser distinguidos.
- Citação literal exige confronto com o suporte material.
- Divergência de edição, tradução, volume, tomo ou paginação bloqueia confirmação automática.
- É proibido inventar DOI, ISBN, URL, edição, página ou metadado.

## 9. Regras de validação
VALIDADA exige:
1. objeto e edição identificados;
2. acesso material comprovado;
3. leitura suficiente para o uso;
4. localização interna confirmada quando necessária;
5. correspondência entre evidência e afirmação;
6. proveniência registrada.

## 10. Regras de recomendação
- Conhecimento nominal não autoriza recomendação.
- Localização sem acesso autoriza apenas recomendação condicional para obtenção.
- Leitura parcial pode sustentar recomendação limitada ao trecho examinado.
- RECOMENDADA exige validação compatível com a finalidade declarada.
- Fonte-coringa, extrapolação de escopo e concentração bibliográfica devem ser sinalizadas.

## 11. Política de abstenção
ABSTENCAO_BIBLIOGRAFICA é obrigatória quando:
- obra ou edição não podem ser identificadas;
- acesso não foi comprovado;
- leitura alegada não pode ser demonstrada;
- página, citação ou metadado divergem;
- fonte secundária é usada como prova de leitura primária;
- evidência não sustenta a afirmação;
- o comando exige invenção.

## 12. Atualização e preservação histórica
Nova edição, novo arquivo, nova localização ou nova evidência não apagam estados anteriores. A substituição deve registrar:
- versão anterior;
- versão nova;
- motivo;
- evidência;
- autoridade;
- data ou marco documental;
- reversibilidade.

## 13. Limites do P04
Este protocolo não cria o schema afirmação–evidência do P05, a taxonomia de intervenção do P06, o contrato de voz do P07 nem a política de segurança do P08. Não escolhe tecnologia, arquitetura, banco, indexador, API, fornecedor ou plataforma.

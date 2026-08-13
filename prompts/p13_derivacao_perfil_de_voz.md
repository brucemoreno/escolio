# P13 — Etapa 13: derivação de perfil de voz candidato a partir de amostras autorais [P07]

Fonte: `01_CONTRATO_UNIVERSAL_DE_VOZ_AUTORAL_P07_R01.md` (Gates: "perfil derivado exige
múltiplas amostras e proveniência"; "perfil insuficiente conduz à abstenção, pedido de amostras
ou perfil neutro"), `03_DICIONARIO_DE_DIMENSOES_DE_VOZ_P07_R01.csv` (30 dimensões, VOZ-D01...D30,
26 obrigatórias).

Decisão do professor (`USUARIO_PROPONENTE`): em vez de o professor preencher manualmente as 30
dimensões do perfil P07, você propõe um **candidato**, dimensão por dimensão, com evidência real
e confiança — o professor calibra depois, de preferência só nos pontos incertos. Você não
homologa nada; produz um rascunho rastreável.

Você recebe, no bloco `system`, as amostras autorais fornecidas (texto + proveniência). Quais
documentos contam como amostra **não é decisão sua** — foi decidido por quem montou esta chamada,
antes de você ser chamado.

## O que fazer, para cada uma das 30 dimensões (VOZ-D01...D30)

Avalie **todas as 30**, sem pular nenhuma. Para cada dimensão, você tem exatamente duas saídas
possíveis — nunca as duas ao mesmo tempo, e nunca nenhuma:

1. **Evidência suficiente** (`dimensoes_com_evidencia`): você consegue apontar, nas amostras, o
   padrão que sustenta um valor para esta dimensão. Registre:
   - `valor`: a caracterização da dimensão, em prosa concisa — nunca um número inventado onde a
     fonte não define limiar (ex.: "ritmo" e "cadência" não têm limiar quantitativo definido em
     nenhuma fonte — descreva o padrão observado, não force uma métrica).
   - `evidencia`: pelo menos um trecho real, citando `amostra_id`, que sustenta o valor. Nunca
     declare evidência sem poder apontar onde nas amostras ela está.
   - `confianca`: `BAIXA`, `MEDIA` ou `ALTA`. Use `BAIXA` sempre que o padrão for inconsistente
     entre as amostras ou dependa de poucos trechos — isso preserva a calibração humana em vez de
     forçar uma conclusão categórica.
2. **Evidência insuficiente** (`dimensoes_sem_evidencia_suficiente`): as amostras não trazem
   material suficiente para sustentar um valor com confiança mínima. Registre `motivo` explicando
   o que faltou (ex.: "nenhuma amostra contém nota de rodapé — sem base para avaliar
   VOZ-D11/transições em aparato crítico"). **Nunca invente um valor para preencher a lacuna** —
   é preferível declarar ausência de evidência do que produzir uma dimensão plausível, mas sem
   base real.

Toda dimensão (as 30) precisa aparecer em exatamente uma das duas listas. Não omita nenhuma.

## Disciplina

- Distinga fato observado de inferência, mesma regra da detecção de fidelidade: se você só tem
  inferência fraca, registre `confianca=BAIXA` ou declare a dimensão sem evidência suficiente —
  não eleve a confiança para simular certeza que as amostras não sustentam.
- Não avalie a qualidade do texto avaliado (isto não é revisão de conteúdo) — só descreva o
  padrão de voz que as amostras exibem.
- Não compare amostras entre si para decidir se conflitam — essa comparação (`amostras_
  conflitantes`) é feita por quem opera a etapa, fora desta chamada.
- Registre tudo pela ferramenta fornecida. Não produza texto fora dela.

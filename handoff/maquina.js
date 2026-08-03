'use strict';

/**
 * Máquina de estados documental do P03 (Núcleo transversal obrigatório).
 *
 * Fonte literal e única: P03/02_MAQUINA_DE_ESTADOS_DOCUMENTAL_P03_R01.csv
 * (corpus/governanca-R01/PACOTE_NUCLEO_TRANSVERSAL_LLM_ACADEMICA_R01/).
 *
 * Regra de leitura da fonte: a coluna "saida" de cada linha do CSV lista um
 * ou dois estados de destino separados por " ou ". Cada linha do CSV vira,
 * no código, uma ou duas transições (origem -> destino), preservando
 * evento, autoridade e erro_bloqueante originais.
 *
 * Lacunas conhecidas da fonte (estados sem saída codificada, estado sem
 * transição de entrada): ver handoff/LACUNAS.md. Não inferidas nem
 * corrigidas aqui.
 */

// Transcrição literal das 10 linhas do CSV fonte. Cada objeto corresponde a
// uma linha: origem, saida (pode conter " ou "), evento, autoridade,
// erro_bloqueante, reversivel.
const LINHAS_CSV = [
  {
    origem: 'NAO_INICIADO',
    saida: 'AUTORIZADO_PARA_EXECUCAO',
    evento: 'Comando específico após gate.',
    autoridade: 'USUARIO_PROPONENTE',
    erroBloqueante: 'Gate ou dependência ausente',
    reversivel: 'SIM',
  },
  {
    origem: 'AUTORIZADO_PARA_EXECUCAO',
    saida: 'EM_EXECUCAO_DOCUMENTAL',
    evento: 'Executor inicia comando único.',
    autoridade: 'CHAT_EXECUTOR_DOCUMENTAL',
    erroBloqueante: 'Escopo ambíguo ou entrada material ausente',
    reversivel: 'SIM',
  },
  {
    origem: 'EM_EXECUCAO_DOCUMENTAL',
    saida: 'EXECUTADO_NAO_AUDITADO',
    evento: 'Conclusão dos arquivos e testes.',
    autoridade: 'CHAT_EXECUTOR_DOCUMENTAL',
    erroBloqueante: 'Teste documental falho',
    reversivel: 'SIM',
  },
  {
    origem: 'EXECUTADO_NAO_AUDITADO',
    saida: 'EM_AUDITORIA',
    evento: 'Comando de auditoria independente.',
    autoridade: 'USUARIO_PROPONENTE/CHAT_AUDITOR_INDEPENDENTE',
    erroBloqueante: 'Produto incompleto',
    reversivel: 'SIM',
  },
  {
    origem: 'EM_AUDITORIA',
    saida: 'APROVADO_PARA_DECISAO_AUTORAL ou REPROVADO_PARA_CORRECAO',
    evento: 'Veredito.',
    autoridade: 'CHAT_AUDITOR_INDEPENDENTE',
    erroBloqueante: 'Auditor corrige ou amplia escopo',
    reversivel: 'SIM',
  },
  {
    origem: 'REPROVADO_PARA_CORRECAO',
    saida: 'AUTORIZADO_PARA_CORRECAO',
    evento: 'Comando autoral de correção local.',
    autoridade: 'USUARIO_PROPONENTE',
    erroBloqueante: 'Correção sem comando',
    reversivel: 'SIM',
  },
  {
    origem: 'APROVADO_PARA_DECISAO_AUTORAL',
    saida: 'HOMOLOGADO_E_CONGELADO ou AGUARDANDO_DECISAO',
    evento: 'Decisão autoral.',
    autoridade: 'USUARIO_PROPONENTE',
    erroBloqueante: 'Auto-homologação',
    reversivel: 'SIM',
  },
  {
    origem: 'HOMOLOGADO_E_CONGELADO',
    saida: 'PERMANECE_CONGELADO ou REABERTO_SOB_AUTORIZACAO',
    evento: 'Uso como dependência ou reabertura excepcional.',
    autoridade: 'USUARIO_PROPONENTE',
    erroBloqueante: 'Alteração direta',
    reversivel: 'SIM_PARA_VERSAO_ANTERIOR',
  },
  {
    origem: 'INTERROMPIDO_BLOQUEADO',
    saida: 'ESTADO_RESTAURADO',
    evento: 'Correção da entrada e autorização de retomada.',
    autoridade: 'USUARIO_PROPONENTE',
    erroBloqueante: 'Retomada automática',
    reversivel: 'SIM',
  },
  {
    origem: 'ESTADO_RESTAURADO',
    saida: 'AUTORIZADO_PARA_EXECUCAO ou AGUARDANDO_COMANDO',
    evento: 'Novo comando específico.',
    autoridade: 'USUARIO_PROPONENTE',
    erroBloqueante: 'Contexto incompleto',
    reversivel: 'SIM',
  },
];

function construirTransicoes() {
  const transicoes = [];
  for (const linha of LINHAS_CSV) {
    const destinos = linha.saida.split(' ou ').map((d) => d.trim());
    for (const destino of destinos) {
      transicoes.push({
        origem: linha.origem,
        destino,
        evento: linha.evento,
        autoridade: linha.autoridade,
        erroBloqueante: linha.erroBloqueante,
        reversivel: linha.reversivel,
      });
    }
  }
  return transicoes;
}

const TRANSICOES = construirTransicoes();

const TRANSICOES_POR_ORIGEM = new Map();
for (const t of TRANSICOES) {
  if (!TRANSICOES_POR_ORIGEM.has(t.origem)) {
    TRANSICOES_POR_ORIGEM.set(t.origem, []);
  }
  TRANSICOES_POR_ORIGEM.get(t.origem).push(t);
}

// Estados que têm linha própria no CSV (logo, podem ter transição de saída).
const ESTADOS_COM_LINHA_PROPRIA = new Set(LINHAS_CSV.map((l) => l.origem));

// Todos os estados citados na fonte, como origem ou como destino.
const ESTADOS = Array.from(
  new Set([...TRANSICOES.map((t) => t.origem), ...TRANSICOES.map((t) => t.destino)])
).sort();

const ESTADOS_SET = new Set(ESTADOS);

// Estados citados só como destino — terminais por ausência de definição na fonte.
const ESTADOS_TERMINAIS_SEM_SAIDA_DEFINIDA = ESTADOS.filter(
  (e) => !ESTADOS_COM_LINHA_PROPRIA.has(e)
);

class TransicaoInvalida extends Error {}

/**
 * Valida e retorna a transição correspondente a origem -> destino.
 *
 * Aceita SOMENTE as transições listadas na máquina de estados documental
 * do P03. Não infere, não completa e não corrige transições ausentes na
 * fonte.
 */
function transicionar(estadoOrigem, estadoDestino) {
  if (!ESTADOS_SET.has(estadoOrigem)) {
    throw new TransicaoInvalida(
      `Estado de origem '${estadoOrigem}' não existe na máquina de estados ` +
        `documental do P03 [P03/02_MAQUINA_DE_ESTADOS_DOCUMENTAL_P03_R01.csv].`
    );
  }

  const candidatas = TRANSICOES_POR_ORIGEM.get(estadoOrigem) || [];
  for (const transicao of candidatas) {
    if (transicao.destino === estadoDestino) {
      return transicao;
    }
  }

  if (!ESTADOS_COM_LINHA_PROPRIA.has(estadoOrigem)) {
    throw new TransicaoInvalida(
      `Transição de '${estadoOrigem}' para '${estadoDestino}' é inválida: ` +
        `'${estadoOrigem}' não possui linha própria na máquina de estados ` +
        `documental do P03 — é citado somente como destino de outra ` +
        `transição, sem saída definida na fonte ` +
        `[P03/02_MAQUINA_DE_ESTADOS_DOCUMENTAL_P03_R01.csv].`
    );
  }

  const destinosValidos = candidatas.map((t) => t.destino).join(', ');
  throw new TransicaoInvalida(
    `Transição de '${estadoOrigem}' para '${estadoDestino}' é inválida ` +
      `segundo a máquina de estados documental do P03 ` +
      `[P03/02_MAQUINA_DE_ESTADOS_DOCUMENTAL_P03_R01.csv]. ` +
      `Destinos permitidos a partir de '${estadoOrigem}': ${destinosValidos}.`
  );
}

module.exports = {
  TRANSICOES,
  ESTADOS,
  ESTADOS_COM_LINHA_PROPRIA,
  ESTADOS_TERMINAIS_SEM_SAIDA_DEFINIDA,
  TransicaoInvalida,
  transicionar,
};

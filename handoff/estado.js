'use strict';

/**
 * Estado canônico documental: leitura, escrita e transição de estado.json.
 *
 * Campos de estado.json, conforme escopo do handoff Fase 1:
 * - componenteAtual: id do componente em foco (ex.: "P03"), ou null.
 * - estadoPorComponente: mapa {P00..P28: estado da máquina documental do P03}.
 * - papelDaVez: autoridade/papel habilitado a agir agora
 *   (USUARIO_PROPONENTE, CHAT_EXECUTOR_DOCUMENTAL, CHAT_AUDITOR_INDEPENDENTE,
 *   ou combinação "A/B" como na fonte do P03).
 * - proximaAcaoUnica: string com exatamente uma próxima ação permitida, ou
 *   null (POL-012: "Registrar exatamente uma próxima ação permitida ou
 *   nenhuma automática" [P03/01_POLITICAS_TRANSVERSAIS_P03_R01.md]).
 * - hashesCanonicos: mapa {identificador_do_objeto: hash}.
 * - pendencias: lista de strings descrevendo pendências abertas.
 *
 * Os 29 componentes (P00-P28) do inventário canônico
 * [P00/04_INVENTARIO_CANONICO_DE_COMPONENTES_R03.csv] são os únicos
 * identificadores válidos de componente.
 */

const fs = require('fs');

const { ESTADOS, transicionar } = require('./maquina');

const COMPONENTES = Array.from({ length: 29 }, (_, n) => `P${String(n).padStart(2, '0')}`); // P00..P28
const COMPONENTES_SET = new Set(COMPONENTES);
const ESTADOS_SET = new Set(ESTADOS);

class EstadoInvalido extends Error {}

/** Retorna o estado.json inicial: todos os componentes NAO_INICIADO. */
function estadoInicial() {
  const estadoPorComponente = {};
  for (const c of COMPONENTES) {
    estadoPorComponente[c] = 'NAO_INICIADO';
  }
  return {
    componenteAtual: null,
    estadoPorComponente,
    papelDaVez: 'USUARIO_PROPONENTE',
    proximaAcaoUnica: null,
    hashesCanonicos: {},
    pendencias: [],
  };
}

const CAMPOS_OBRIGATORIOS = [
  'componenteAtual',
  'estadoPorComponente',
  'papelDaVez',
  'proximaAcaoUnica',
  'hashesCanonicos',
  'pendencias',
];

/** Valida a estrutura mínima de um objeto de estado.json. */
function validarEstado(estado) {
  const faltantes = CAMPOS_OBRIGATORIOS.filter((campo) => !(campo in estado));
  if (faltantes.length > 0) {
    throw new EstadoInvalido(`Campos ausentes em estado.json: ${faltantes.join(', ')}`);
  }

  if (estado.componenteAtual !== null && !COMPONENTES_SET.has(estado.componenteAtual)) {
    throw new EstadoInvalido(
      `componenteAtual '${estado.componenteAtual}' não está no inventário canônico P00-P28.`
    );
  }

  for (const [componente, estadoComponente] of Object.entries(estado.estadoPorComponente)) {
    if (!COMPONENTES_SET.has(componente)) {
      throw new EstadoInvalido(`Componente '${componente}' não está no inventário canônico P00-P28.`);
    }
    if (!ESTADOS_SET.has(estadoComponente)) {
      throw new EstadoInvalido(
        `Estado '${estadoComponente}' do componente '${componente}' não existe na ` +
          `máquina de estados documental do P03.`
      );
    }
  }
}

function carregarEstado(caminho) {
  const estado = JSON.parse(fs.readFileSync(caminho, 'utf8'));
  validarEstado(estado);
  return estado;
}

function salvarEstado(estado, caminho) {
  validarEstado(estado);
  fs.writeFileSync(caminho, JSON.stringify(estado, null, 2) + '\n', 'utf8');
}

/**
 * Aplica, sobre estado.json, a transição documental do P03 para um
 * componente específico. Retorna um novo objeto de estado (não muta o
 * argumento recebido). Lança TransicaoInvalida (de maquina.js) se a
 * transição não estiver na máquina de estados documental do P03, ou
 * EstadoInvalido se o componente não existir no inventário canônico.
 */
function transicionarComponente(estado, componente, estadoDestino) {
  if (!COMPONENTES_SET.has(componente)) {
    throw new EstadoInvalido(`Componente '${componente}' não está no inventário canônico P00-P28.`);
  }

  const estadoOrigem = estado.estadoPorComponente[componente];
  transicionar(estadoOrigem, estadoDestino); // lança TransicaoInvalida se ilegal

  const novoEstado = JSON.parse(JSON.stringify(estado));
  novoEstado.estadoPorComponente[componente] = estadoDestino;
  return novoEstado;
}

module.exports = {
  COMPONENTES,
  EstadoInvalido,
  estadoInicial,
  validarEstado,
  carregarEstado,
  salvarEstado,
  transicionarComponente,
};

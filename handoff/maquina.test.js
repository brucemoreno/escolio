'use strict';

/**
 * Testes da máquina de estados documental do P03.
 *
 * Cobre cada uma das 14 transições válidas (10 linhas do CSV fonte, quatro
 * das quais bifurcam em "X ou Y") e uma amostra de transições inválidas:
 * estado inexistente, transição fora da tabela, e transição a partir de um
 * estado sem linha própria (só citado como destino na fonte).
 */

const assert = require('node:assert/strict');
const { test } = require('node:test');

const maquina = require('./maquina');
const { TransicaoInvalida, transicionar } = maquina;

const TRANSICOES_VALIDAS = [
  ['NAO_INICIADO', 'AUTORIZADO_PARA_EXECUCAO'],
  ['AUTORIZADO_PARA_EXECUCAO', 'EM_EXECUCAO_DOCUMENTAL'],
  ['EM_EXECUCAO_DOCUMENTAL', 'EXECUTADO_NAO_AUDITADO'],
  ['EXECUTADO_NAO_AUDITADO', 'EM_AUDITORIA'],
  ['EM_AUDITORIA', 'APROVADO_PARA_DECISAO_AUTORAL'],
  ['EM_AUDITORIA', 'REPROVADO_PARA_CORRECAO'],
  ['REPROVADO_PARA_CORRECAO', 'AUTORIZADO_PARA_CORRECAO'],
  ['APROVADO_PARA_DECISAO_AUTORAL', 'HOMOLOGADO_E_CONGELADO'],
  ['APROVADO_PARA_DECISAO_AUTORAL', 'AGUARDANDO_DECISAO'],
  ['HOMOLOGADO_E_CONGELADO', 'PERMANECE_CONGELADO'],
  ['HOMOLOGADO_E_CONGELADO', 'REABERTO_SOB_AUTORIZACAO'],
  ['INTERROMPIDO_BLOQUEADO', 'ESTADO_RESTAURADO'],
  ['ESTADO_RESTAURADO', 'AUTORIZADO_PARA_EXECUCAO'],
  ['ESTADO_RESTAURADO', 'AGUARDANDO_COMANDO'],
];

test('número de transições válidas bate com a fonte (14 pares)', () => {
  assert.equal(maquina.TRANSICOES.length, 14);
  assert.equal(TRANSICOES_VALIDAS.length, 14);
});

for (const [origem, destino] of TRANSICOES_VALIDAS) {
  test(`transição válida: ${origem} -> ${destino}`, () => {
    const t = transicionar(origem, destino);
    assert.equal(t.origem, origem);
    assert.equal(t.destino, destino);
    assert.ok(t.evento);
    assert.ok(t.autoridade);
  });
}

test('transição válida carrega autoridade e erro bloqueante literais', () => {
  const t = transicionar('NAO_INICIADO', 'AUTORIZADO_PARA_EXECUCAO');
  assert.equal(t.autoridade, 'USUARIO_PROPONENTE');
  assert.equal(t.erroBloqueante, 'Gate ou dependência ausente');
  assert.equal(t.reversivel, 'SIM');
});

test('congelamento é reversível apenas para versão anterior', () => {
  const t = transicionar('HOMOLOGADO_E_CONGELADO', 'PERMANECE_CONGELADO');
  assert.equal(t.reversivel, 'SIM_PARA_VERSAO_ANTERIOR');
});

const TRANSICOES_INVALIDAS_FORA_DA_TABELA = [
  ['NAO_INICIADO', 'EM_EXECUCAO_DOCUMENTAL'], // pula etapa
  ['NAO_INICIADO', 'HOMOLOGADO_E_CONGELADO'], // salto arbitrário
  ['EM_EXECUCAO_DOCUMENTAL', 'NAO_INICIADO'], // retrocesso não previsto
  ['EM_AUDITORIA', 'HOMOLOGADO_E_CONGELADO'], // pula decisão autoral
  ['HOMOLOGADO_E_CONGELADO', 'EM_EXECUCAO_DOCUMENTAL'], // alteração direta
];

for (const [origem, destino] of TRANSICOES_INVALIDAS_FORA_DA_TABELA) {
  test(`transição inválida fora da tabela: ${origem} -> ${destino}`, () => {
    assert.throws(
      () => transicionar(origem, destino),
      (err) => {
        assert.ok(err instanceof TransicaoInvalida);
        assert.match(err.message, new RegExp(origem));
        assert.match(err.message, new RegExp(destino));
        return true;
      }
    );
  });
}

const ESTADOS_SO_DESTINO = [
  'AUTORIZADO_PARA_CORRECAO',
  'AGUARDANDO_DECISAO',
  'PERMANECE_CONGELADO',
  'REABERTO_SOB_AUTORIZACAO',
  'AGUARDANDO_COMANDO',
];

for (const origem of ESTADOS_SO_DESTINO) {
  test(`estado só-destino sem saída definida: ${origem}`, () => {
    assert.throws(
      () => transicionar(origem, 'NAO_INICIADO'),
      (err) => {
        assert.ok(err instanceof TransicaoInvalida);
        assert.match(err.message, new RegExp(origem));
        assert.match(err.message, /não possui linha própria/);
        return true;
      }
    );
  });
}

test('estado de origem inexistente', () => {
  assert.throws(
    () => transicionar('ESTADO_QUE_NAO_EXISTE', 'NAO_INICIADO'),
    (err) => {
      assert.ok(err instanceof TransicaoInvalida);
      assert.match(err.message, /ESTADO_QUE_NAO_EXISTE/);
      return true;
    }
  );
});

test('destino válido na máquina, mas não alcançável a partir da origem informada', () => {
  // REPROVADO_PARA_CORRECAO só chega em AUTORIZADO_PARA_CORRECAO, não em
  // HOMOLOGADO_E_CONGELADO.
  assert.throws(
    () => transicionar('REPROVADO_PARA_CORRECAO', 'HOMOLOGADO_E_CONGELADO'),
    (err) => {
      assert.ok(err instanceof TransicaoInvalida);
      assert.match(err.message, /REPROVADO_PARA_CORRECAO/);
      assert.match(err.message, /HOMOLOGADO_E_CONGELADO/);
      return true;
    }
  );
});

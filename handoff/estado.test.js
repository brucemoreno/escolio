'use strict';

/** Testes de estado.json: modelo, validação e transição por componente. */

const assert = require('node:assert/strict');
const { test } = require('node:test');

const {
  COMPONENTES,
  EstadoInvalido,
  estadoInicial,
  validarEstado,
  transicionarComponente,
} = require('./estado');
const { TransicaoInvalida } = require('./maquina');

test('COMPONENTES cobre P00 a P28', () => {
  assert.equal(COMPONENTES[0], 'P00');
  assert.equal(COMPONENTES[COMPONENTES.length - 1], 'P28');
  assert.equal(COMPONENTES.length, 29);
});

test('estado inicial é válido e todos os componentes começam NAO_INICIADO', () => {
  const estado = estadoInicial();
  validarEstado(estado);
  assert.ok(Object.values(estado.estadoPorComponente).every((v) => v === 'NAO_INICIADO'));
  assert.equal(estado.componenteAtual, null);
  assert.equal(estado.proximaAcaoUnica, null);
  assert.deepEqual(estado.pendencias, []);
});

test('estado inicial é serializável em JSON sem perda', () => {
  const estado = estadoInicial();
  const texto = JSON.stringify(estado);
  assert.deepEqual(JSON.parse(texto), estado);
});

test('validarEstado rejeita campo ausente', () => {
  const estado = estadoInicial();
  delete estado.pendencias;
  assert.throws(() => validarEstado(estado), EstadoInvalido);
});

test('validarEstado rejeita componente fora do inventário', () => {
  const estado = estadoInicial();
  estado.estadoPorComponente.P29 = 'NAO_INICIADO';
  assert.throws(() => validarEstado(estado), EstadoInvalido);
});

test('validarEstado rejeita estado documental desconhecido', () => {
  const estado = estadoInicial();
  estado.estadoPorComponente.P03 = 'ESTADO_INVENTADO';
  assert.throws(() => validarEstado(estado), EstadoInvalido);
});

test('transicionarComponente aplica transição válida e não muta o original', () => {
  const estado = estadoInicial();
  const novoEstado = transicionarComponente(estado, 'P03', 'AUTORIZADO_PARA_EXECUCAO');
  assert.equal(novoEstado.estadoPorComponente.P03, 'AUTORIZADO_PARA_EXECUCAO');
  assert.equal(estado.estadoPorComponente.P03, 'NAO_INICIADO');
});

test('transicionarComponente rejeita transição inválida', () => {
  const estado = estadoInicial();
  assert.throws(
    () => transicionarComponente(estado, 'P03', 'HOMOLOGADO_E_CONGELADO'),
    TransicaoInvalida
  );
});

test('transicionarComponente rejeita componente fora do inventário', () => {
  const estado = estadoInicial();
  assert.throws(
    () => transicionarComponente(estado, 'P29', 'AUTORIZADO_PARA_EXECUCAO'),
    EstadoInvalido
  );
});

'use strict';

/** Gera o estado.json inicial na pasta corrente do script. */

const path = require('path');

const { estadoInicial, salvarEstado } = require('./estado');

const caminho = path.join(__dirname, 'estado.json');
salvarEstado(estadoInicial(), caminho);
console.log(`estado.json gerado em ${caminho}`);

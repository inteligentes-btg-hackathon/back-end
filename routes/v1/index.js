const express = require('express');
const RouterV1 = express.Router();

const MockupRouter = require('./mockup.route');

RouterV1.use('/mockup', MockupRouter);

module.exports = RouterV1;

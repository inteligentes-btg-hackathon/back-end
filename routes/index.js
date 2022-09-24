const express = require('express');
const Router = express.Router();

const V1Router = require('./v1');

Router.use('/v1', V1Router);

module.exports = Router;

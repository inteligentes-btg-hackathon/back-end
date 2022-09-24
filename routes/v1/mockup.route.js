const express = require('express');
const MockupRouter = express.Router();

MockupRouter.get('/', (req, res) => {
	res.send('Hello from mockup route');
});

module.exports = MockupRouter;

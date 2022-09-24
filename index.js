const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');
const app = express();
const router = require('./routes');

dotenv.config();

app.use(express.json());
app.use(cors());

app.use('/api', router);

const server = app.listen(process.env.SERVER_PORT || 3232, () => {
	console.log(`Server Running on http://localhost:${server.address().port}`);
});

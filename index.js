const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');
const app = express();
const router = require('./routes');

const { Client, Bank, VariableIncome, FixedIncome } = require('./repositories');

//Client.create({ customerId: '17767719740' });
//Bank.create({
//	brand: 'BTG Pactual',
//	cnpj: '30306294000145',
//	clients: ['17767719740'],
//});
//VariableIncome.create({
//	customerId: '17767719740',
//	bankId: 6,
//	name: 'DISB34',
//	type: 'BDR',
//	exempt: true,
//	minimalValue: 100,
//	maturity: '2022-09-24',
//	date: '2021-09-01',
//	createdAt: new Date(),
//	updatedAt: new Date(),
//});
//FixedIncome.create({
//	customerId: '17767719740',
//	bankId: 6,
//	name: 'Tesouro IPCA+26',
//	type: 'Título público',
//	exempt: true,
//	interestRate: 0.5,
//	minimalValue: 100,
//	maturity: '2022-09-24',
//	date: '2021-09-01',
//});
Client.getInvestmentsByCustomerId('17767719740').then((data) => {
	console.log(data.dataValues);
});

dotenv.config();

app.use(express.json());
app.use(cors());

app.use('/api', router);

const server = app.listen(process.env.SERVER_PORT || 3232, () => {
	console.log(`Server Running on http://localhost:${server.address().port}`);
});

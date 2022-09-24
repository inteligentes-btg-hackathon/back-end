const { Client, VariableIncome, FixedIncome } = require('../models');

class ClientRepository {
	async create(client) {
		return Client.create(client);
	}

	async findAll() {
		return Client.findAll();
	}

	async findById(id) {
		return Client.findByPk(id);
	}

	async update(id, client) {
		return Client.update(client, { where: { id } });
	}

	async delete(id) {
		return Client.destroy({ where: { id } });
	}

	async getInvestmentsByCustomerId(customerId) {
		return Client.findByPk(customerId, {
			include: [
				{
					model: VariableIncome,
				},
				{
					model: FixedIncome,
				},
			],
		});
	}
}

module.exports = new ClientRepository();

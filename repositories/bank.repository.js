const { Bank } = require('../models');

class BankRepository {
	async create(bank) {
		return Bank.create(bank);
	}

	async findAll() {
		return Bank.findAll();
	}

	async findById(id) {
		return Bank.findByPk(id);
	}

	async update(id, bank) {
		return Bank.update(bank, { where: { id } });
	}

	async delete(id) {
		return Bank.destroy({ where: { id } });
	}
}

module.exports = new BankRepository();

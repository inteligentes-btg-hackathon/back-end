const { FixedIncome } = require('../models');

class FixedIncomeRepository {
	async create(fixedIncome) {
		return FixedIncome.create(fixedIncome);
	}

	async findAll() {
		return FixedIncome.findAll();
	}

	async findById(id) {
		return FixedIncome.findByPk(id);
	}

	async update(id, fixedIncome) {
		return FixedIncome.update(fixedIncome, { where: { id } });
	}

	async delete(id) {
		return FixedIncome.destroy({ where: { id } });
	}
}

module.exports = new FixedIncomeRepository();

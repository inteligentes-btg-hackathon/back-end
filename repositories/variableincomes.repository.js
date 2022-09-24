const { VariableIncome } = require('../models');

class VariableIncomeRepository {
	async create(variableIncome) {
		return VariableIncome.create(variableIncome);
	}

	async findAll() {
		return VariableIncome.findAll();
	}

	async findById(id) {
		return VariableIncome.findByPk(id);
	}

	async update(id, variableIncome) {
		return VariableIncome.update(variableIncome, { where: { id } });
	}

	async delete(id) {
		return VariableIncome.destroy({ where: { id } });
	}
}

module.exports = new VariableIncomeRepository();

'use strict';
const { Model } = require('sequelize');
module.exports = (sequelize, DataTypes) => {
	class Bank extends Model {
		static associate(models) {
			Bank.hasMany(models.Client, { foreignKey: 'clients' });
			Bank.belongsTo(models.FixedIncomes, { foreignKey: 'bankId' });
			Bank.belongsTo(models.VariableIncomes, { foreignKey: 'bankId' });
		}
	}
	Bank.init(
		{
			brand: DataTypes.STRING,
			cnpj: DataTypes.STRING,
			clients: DataTypes.ARRAY(DataTypes.STRING),
		},
		{
			sequelize,
			modelName: 'Bank',
		}
	);
	return Bank;
};

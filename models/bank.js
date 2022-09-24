'use strict';
const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
	class Bank extends Model {
		static associate(models) {
			// TODO: Associate the Bank model with the fixed and variable incomes models.
			Bank.hasMany(models.Client, { foreignKey: 'customerId' });
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

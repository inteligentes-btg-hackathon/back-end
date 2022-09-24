'use strict';
const { Model } = require('sequelize');
module.exports = (sequelize, DataTypes) => {
	class VariableIncomes extends Model {
		static associate(models) {
			VariableIncomes.hasOne(models.Banks, {
				foreignKey: 'bankId',
				as: 'id',
			});
			VariableIncomes.hasOne(models.ProductsClient, {
				foreignKey: 'productsVariableIncomes',
				as: 'id',
			});
		}
	}
	VariableIncomes.init(
		{
			customerId: {
				allowNull: false,
				autoIncrement: false,
				primaryKey: true,
				type: DataTypes.STRING,
			},
			bankId: DataTypes.INTEGER,
			name: DataTypes.STRING,
			type: DataTypes.STRING,
			exempt: DataTypes.BOOLEAN,
			minimalValue: DataTypes.INTEGER,
			maturity: DataTypes.STRING,
			date: DataTypes.DATEONLY,
		},
		{
			sequelize,
			modelName: 'VariableIncomes',
		}
	);
	return VariableIncomes;
};

'use strict';
const { Model } = require('sequelize');
module.exports = (sequelize, DataTypes) => {
	class FixedIncomes extends Model {
		static associate(models) {
			FixedIncomes.hasOne(models.Banks, {
				foreignKey: 'bankId',
				as: 'id',
			});
			FixedIncomes.hasOne(models.ProductsClient, {
				foreignKey: 'productsFixedIncomes',
				as: 'id',
			});
		}
	}
	FixedIncomes.init(
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
			interestRate: DataTypes.FLOAT,
			minimalValue: DataTypes.FLOAT,
			maturity: DataTypes.DATEONLY,
			date: DataTypes.DATEONLY,
		},
		{
			sequelize,
			modelName: 'FixedIncomes',
		}
	);
	return FixedIncomes;
};

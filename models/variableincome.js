'use strict';
const { Model } = require('sequelize');
module.exports = (sequelize, DataTypes) => {
	class VariableIncome extends Model {
		static associate(models) {
			VariableIncome.hasOne(models.Client, { foreignKey: 'customerId' });
		}
	}
	VariableIncome.init(
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
			modelName: 'VariableIncome',
		}
	);
	return VariableIncome;
};

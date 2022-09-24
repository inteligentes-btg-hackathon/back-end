'use strict';
const { Model } = require('sequelize');
module.exports = (sequelize, DataTypes) => {
	class FixedIncome extends Model {
		static associate(models) {
			FixedIncome.hasOne(models.Client, { foreignKey: 'customerId' });
		}
	}
	FixedIncome.init(
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
			modelName: 'FixedIncome',
		}
	);
	return FixedIncome;
};

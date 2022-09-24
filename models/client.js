'use strict';
const { Model } = require('sequelize');
module.exports = (sequelize, DataTypes) => {
	class Client extends Model {
		static associate(models) {
			Client.belongsTo(models.Bank, { foreignKey: 'customerId' });
			Client.belongsTo(models.FixedIncome, { foreignKey: 'customerId' });
			Client.belongsTo(models.VariableIncome, { foreignKey: 'customerId' });
		}
	}
	Client.init(
		{
			customerId: { type: DataTypes.STRING, primaryKey: true, allowNull: false, autoIncrement: false },
		},
		{
			sequelize,
			modelName: 'Client',
		}
	);
	return Client;
};

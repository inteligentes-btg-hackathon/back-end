'use strict';
const { Model } = require('sequelize');
module.exports = (sequelize, DataTypes) => {
	class Client extends Model {
		static associate(models) {
			Client.belongsTo(models.Bank, { foreignKey: 'clients' });
			Client.belongsTo(models.ProductsClient, { foreignKey: 'customerId' });
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

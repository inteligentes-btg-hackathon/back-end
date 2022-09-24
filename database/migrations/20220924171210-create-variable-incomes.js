'use strict';
module.exports = {
	async up(queryInterface, Sequelize) {
		await queryInterface.createTable('VariableIncomes', {
			id: {
				allowNull: false,
				autoIncrement: true,
				primaryKey: true,
				type: Sequelize.INTEGER,
			},
			customerId: {
				type: Sequelize.STRING,
			},
			bankId: {
				type: Sequelize.INTEGER,
			},
			name: {
				type: Sequelize.STRING,
			},
			type: {
				type: Sequelize.STRING,
			},
			exempt: {
				type: Sequelize.BOOLEAN,
			},
			minimalValue: {
				type: Sequelize.FLOAT,
			},
			maturity: {
				type: Sequelize.DATEONLY,
			},
			date: {
				type: Sequelize.DATEONLY,
			},
			createdAt: {
				allowNull: false,
				type: Sequelize.DATE,
			},
			updatedAt: {
				allowNull: false,
				type: Sequelize.DATE,
			},
		});
	},
	async down(queryInterface, Sequelize) {
		await queryInterface.dropTable('VariableIncomes');
	},
};

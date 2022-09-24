'use strict';
module.exports = {
	async up(queryInterface, Sequelize) {
		await queryInterface.createTable('Banks', {
			id: {
				allowNull: false,
				autoIncrement: true,
				primaryKey: true,
				type: Sequelize.INTEGER,
			},
			brand: {
				type: Sequelize.STRING,
			},
			cnpj: {
				type: Sequelize.STRING,
			},
			clients: {
				type: Sequelize.ARRAY(Sequelize.STRING),
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
		await queryInterface.dropTable('Banks');
	},
};
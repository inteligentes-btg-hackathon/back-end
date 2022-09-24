'use strict';

module.exports = {
	async up(queryInterface, Sequelize) {
		return queryInterface.bulkInsert('Clients', [
			{
				customerId: '05096197034',
				createdAt: new Date(),
				updatedAt: new Date(),
			},
			{
				customerId: '05639615036',
				createdAt: new Date(),
				updatedAt: new Date(),
			},
			{
				customerId: '04067913095',
				createdAt: new Date(),
				updatedAt: new Date(),
			},
		]);
	},

	async down(queryInterface, Sequelize) {
		return queryInterface.bulkDelete('Clients', null, {});
	},
};

'use strict';

module.exports = {
	async up(queryInterface, Sequelize) {
		return queryInterface.bulkInsert('Banks', [
			{
				brand: 'BTG Pactual',
				cnpj: '30306294000145',
				clients: ['05096197034', '05639615036'],
				createdAt: new Date(),
				updatedAt: new Date(),
			},
			{
				brand: 'Itaú',
				cnpj: ' 60701190000104',
				clients: ['04067913095'],
				createdAt: new Date(),
				updatedAt: new Date(),
			},
		]);
	},

	async down(queryInterface, Sequelize) {
		return queryInterface.bulkDelete('Banks', null, {});
	},
};

'use strict';

module.exports = {
	async up(queryInterface, Sequelize) {
		return queryInterface.bulkInsert('VariableIncomes', [
			{
				customerId: '05096197034',
				bankId: 0,
				name: 'DISB34',
				type: 'BDR',
				exempt: true,
				minimalValue: 100,
				maturity: '2022-09-24',
				date: '2021-09-01',
				createdAt: new Date(),
				updatedAt: new Date(),
			},

			{
				customerId: '05639615036',
				bankId: 0,
				name: 'DISB34',
				type: 'BDR',
				exempt: true,
				minimalValue: 100,
				maturity: '2022-09-24',
				date: '2021-09-01',
				createdAt: new Date(),
				updatedAt: new Date(),
			},

			{
				customerId: '05096197034',
				bankId: 1,
				name: 'FII XP',
				type: 'FII',
				exempt: true,
				minimalValue: 100,
				maturity: '2022-09-24',
				date: '2021-10-01',
				createdAt: new Date(),
				updatedAt: new Date(),
			},
		]);
	},

	async down(queryInterface, Sequelize) {
		return queryInterface.bulkDelete('VariableIncomes', null, {});
	},
};

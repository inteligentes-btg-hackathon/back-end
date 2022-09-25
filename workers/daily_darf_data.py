from services import TaxCalculator
from repositories import ClientRepository


class Tasks:
    def calculate_tax():
        current_year_month = datetime.datetime.now().strftime("%Y-%m")
        clients = ClientRepository.get_investments(
            None, current_year_month, None)

        TaxCalculator.taxes()

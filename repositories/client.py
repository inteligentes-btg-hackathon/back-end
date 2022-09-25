from database import db, QueryConstructor
from models import Client, Bank, Investment, ProfitLoss
import datetime
from services import TaxCalculator


class ClientRepository:
    def get_all():
        query = QueryConstructor(Client)
        query.select().execute()

        clients = query.results
        for (i, client) in enumerate(clients):
            # Get the banks of each client
            query_banks = QueryConstructor(Bank)
            query_banks.select().where_in_array(
                "id", client["banks_ids"]).execute()
            clients[i]["banks"] = query_banks.results
            del clients[i]["banks_ids"]

            query_investments = QueryConstructor(Investment)
            query_investments.select().where_in_array(
                "id", client["investments_ids"]).execute()

            clients[i]["investments"] = query_investments.results
            del clients[i]["investments_ids"]
        return clients

    def get_investments(customer_id: str, date: str = None, avaliable=True):
        query_client = QueryConstructor(Client)
        query_client.select()

        if (customer_id != None):
            query_client.where("customer_id", '=', customer_id)

        query_client.execute()

        if len(query_client.results) == 0:
            return None

        client = query_client.results[0]
        query_investments = QueryConstructor(Investment)
        query_investments.select().where_in_array(
            "id", client["investments_ids"])

        if (avaliable != None):
            if not avaliable:
                query_investments.is_null("sell_date")
            else:
                query_investments.is_not_null("sell_date")

        if date:
            if(avaliable):
                query_investments.and_("to_char(buy_date, 'YYYY-MM')",
                                       "=", date)
            else:
                query_investments.and_("to_char(sell_date, 'YYYY-MM')",
                                       "=", date)

        query_investments.execute()

        return query_investments.results

    def get_profit_loss(customer_id: str, date: str = None):
        query_profit_loss = QueryConstructor(ProfitLoss)
        query_profit_loss.select().where("customer_id", "=", customer_id)

        if date:
            query_profit_loss.and_("to_char(date, 'YYYY-MM')", "=", date)

        query_profit_loss.execute()

        return query_profit_loss.results

    def calculate_tax(customer_id: str, date: str = None):
        yesterday = datetime.datetime.strptime(
            date, "%Y-%m") - datetime.timedelta(days=1)
        yesterday = yesterday.strftime("%Y-%m")

        investments_yesterday = ClientRepository.get_investments(
            customer_id, yesterday, None)
        investments_today = []

        for investment in ClientRepository.get_investments(customer_id, None, None):
            if investment.get("sell_date", False) and investment["sell_date"].strftime("%Y-%m") == date:
                investments_today.append(investment)
        print("investments_today:", investments_today)
        print("investments_yesterday:", investments_yesterday)

        taxes = TaxCalculator.taxes(
            investments_today, investments_yesterday, date)

        return {
            "taxes": taxes
        }

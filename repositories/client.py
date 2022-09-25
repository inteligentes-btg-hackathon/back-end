from database import db, QueryConstructor
from models import Client, Bank, Investment
import datetime


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
            query_client.where("id", customer_id)

        query_client.execute()

        if len(query.results) == 0:
            return None

        client = query.results[0]
        query_investments = QueryConstructor(Investment)
        query_investments.select().where_in_array(
            "id", client["investments_ids"])

        if (avaliable != None):
            query_investments.and_(
                "sell_date", "=" if avaliable else "!=", None)

        if date:
            date = datetime.datetime.strptime(date, "%Y-%m")
            query_investments.and_("to_char(buy_date, 'YYYY-MM')",
                                   "=", date.strftime("%Y-%m"))

        query_investments.execute()

        return query_investments.results

from database import db, QueryConstructor
from models import Client, Bank, Investment


class Client:
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

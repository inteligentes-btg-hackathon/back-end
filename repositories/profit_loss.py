from database import db, QueryConstructor
from models import ProfitLoss


class ProfitLossRepository:
    def create(profit_loss: dict) -> dict:
        query = QueryConstructor(ProfitLoss)
        query.insert(profit_loss)
        return query.results

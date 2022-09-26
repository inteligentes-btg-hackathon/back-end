from pydantic import BaseModel
from datetime import date


class Investment(BaseModel):
    __table__ = "investments"
    id: int
    bank_id: int
    name: str
    itype: str
    exempt: bool
    sell_date: date
    buy_date: date
    price: float
    rate: float
    buy_price: float
    sell_price: float

    def headers() -> list:
        return [
            "id",
            "bank_id",
            "name",
            "itype",
            "exempt",
            "sell_date",
            "buy_date",
            "price",
            "rate",
            "buy_price",
            "sell_price"
        ]

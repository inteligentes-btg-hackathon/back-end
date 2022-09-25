from pydantic import BaseModel
from datetime import date


class Investment(BaseModel):
    __table__ = "investments"

    bank_id: int
    name: str
    itype: str
    exempt: bool
    minimal_value: float
    sell_date: date
    date: date
    price: float
    rate: float

    def headers() -> list:
        return [
            "bank_id",
            "name",
            "itype",
            "exempt",
            "minimal_value",
            "sell_date",
            "buy_date",
            "price",
            "rate",
        ]

from pydantic import BaseModel
from datetime import date


class Investment(BaseModel):
    __table__ = "investments"

    customer_id: str
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
            "customer_id",
            "bank_id",
            "name",
            "itype",
            "exempt",
            "minimal_value",
            "sell_date",
            "date",
            "price",
            "rate",
        ]

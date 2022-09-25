from pydantic import BaseModel
from datetime import date


class Investment(BaseModel):
    __table__ = "investments"

    bank_id: int
    name: str
    itype: str
    exempt: bool
    interest_rate: float
    minimal_value: float
    maturity: date
    date: date
    price: float
    rate: float

    def headers() -> list:
        return [
            "bank_id",
            "name",
            "itype",
            "exempt",
            "interest_rate",
            "minimal_value",
            "maturity",
            "date",
            "price",
            "rate",
        ]

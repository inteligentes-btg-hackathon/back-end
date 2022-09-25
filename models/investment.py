from pydantic import BaseModel
from datetime import date


class Investment(BaseModel):
    __table__ = "investments"

    customer_id: int
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

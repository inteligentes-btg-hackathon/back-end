from pydantic import BaseModel
from datetime import date

class VariableIncome(BaseModel):
    
    customer_id: int
    bank_id: int
    name: str
    type: str
    exempt: bool
    interest_rate: float
    maturity: date
    date: date
    price: float
    rate: float
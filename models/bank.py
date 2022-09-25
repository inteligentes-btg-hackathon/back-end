from pydantic import BaseModel


class Bank(BaseModel):
    __table__ = "banks"

    bank_id: int
    brand: str
    cnpj: str

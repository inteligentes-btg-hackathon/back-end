from pydantic import BaseModel


class Client(BaseModel):
    bank_id: int
    brand: str
    cnpj: str
    clients: list[str]

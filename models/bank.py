from pydantic import BaseModel


class Bank(BaseModel):
    __table__ = "banks"

    id: int
    brand: str
    cnpj: str

    def headers() -> list:
        return [
            "bank_id",
            "brand",
            "cnpj",
        ]

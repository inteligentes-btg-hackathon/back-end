from pydantic import BaseModel


class Client(BaseModel):
    __table__ = "clients"

    customer_id: str
    banks_ids: list[str]
    investments: list[str]

    def headers():
        return [
            "customer_id",
            "banks_ids",
            "investments",
        ]

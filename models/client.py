from pydantic import BaseModel


class Client(BaseModel):
    __table__ = "clients"

    customer_id: str
    banks_ids: list[str]
    investments_ids: list[str]

    def headers() -> list:
        return [
            "customer_id",
            "banks_ids",
            "investments_ids",
        ]

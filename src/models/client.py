from pydantic import BaseModel


class Client(BaseModel):
    customer_id: str
    investments: list[str]

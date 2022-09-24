from pydantic import BaseModel
# https://www.w3schools.com/python/python_datatypes.asp
# https://fastapi.tiangolo.com/tutorial/response-model/#__tabbed_1_3


class Client(BaseModel):
    customer_id: str
    investments: list[str]

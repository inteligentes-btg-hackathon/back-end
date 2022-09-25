from pydantic import BaseModel
from datetime import date


class profit_loss(BaseModel):

    __table__ = "profit_loss"
    customer_id : str
    day_trade_profit :float
    swing_trade_profit :float
    cripto_profit :float
    fii_profit :float
    day_trade_accumulated_loss :float
    swing_trade_accumulated_loss :float
    fii_accumulated_loss :float
    cripto_accumulated_loss :float
    date: date
    taxes: float

    def headers() -> list:
        return [
            "customer_id",
            "day_trade_profit",
            "swing_trade_profit",
            "cripto_profit",
            "fii_profit",
            "day_trade_accumulated_loss",
            "swing_trade_accumulated_loss",
            "fii_accumulated_loss",
            "cripto_accumulated_loss",
            "date",
            "taxes"
        ]

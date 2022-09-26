from pydantic import BaseModel
import datetime


class ProfitLoss(BaseModel):
    __table__ = "profit_loss"

    customer_id: str
    day_trade_profit: float
    swing_trade_profit: float
    cripto_profit: float
    fii_profit: float
    day_trade_accumulated_loss: float
    swing_trade_accumulated_loss: float
    fii_accumulated_loss: float
    cripto_accumulated_loss: float
    accumulated_loss: list[int]
    generate_date: datetime.date
    taxes: float
    paid: bool

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
            "accumulated_loss",
            "generate_date",
            "taxes",
            "paid"
        ]

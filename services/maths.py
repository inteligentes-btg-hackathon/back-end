import datetime
import math
from datetime import datetime


class TaxCalculator:
    def get_cripto_price(value: float):
        CRIPTO_PRICES = [
            {
                "range": range(0, 35001),
                "result": 0.15,
            },
            {
                "range": range(35001, 5000001),
                "result": 0.15,
            },
            {
                "range": range(5000001, 100000001),
                "result": 0.175,
            },
            {
                "range": range(100000001, 300000001),
                "result": 0.2,
            },
            {
                "else": 0.225,
            }
        ]

        for cripto_price in CRIPTO_PRICES:
            if (cripto_price.get("else", None)):
                return cripto_price["else"]
            if value in cripto_price["range"]:
                return cripto_price["result"]

    def taxes(investments_this_month_sold, investments_last_month, current_date, last_taxes={"day_trade_accumulated_loss": 0, "swing_accumulated_loss": 0, "fii_loss": 0, "cripto_accumulated_loss": 0}):
        investments = {}

        taxes = {}
        cripto_sum = 0
        stocks_sum = 0
        day_trade_profit = 0
        swing_trade_profit = 0
        cripto_profit = 0
        fii_profit = 0
        sum_taxes = 0

        for (i, investment_this_month) in enumerate(investments_last_month):
            if investment_this_month["name"] == investment_this_month["name"]:
                index = i
                break

            investments["name"] = {
                "name": investment_this_month["name"],
                "bank_id": investment_this_month["bank_id"],
                "type": investment_this_month["type"],
                "rate": investment_this_month["rate"],
                "buy_date": investment_this_month["date"],
                "sell_date": investment_this_month["sell_date"],
                "exempt": False,
                "profit": investment_this_month["price"] - list(investments_last_month)[index]["price"]
            }

        for item in investments:
            if item["type"] == "criptoativo":
                cripto_sum += item["profit"]
            elif item["type"] == "ação" and (item["sell_date"]-item["buy_date"]).days < 1:
                stocks_sum += item["profit"]
        if stocks_sum <= 20000:
            stock_exempt = True
        if cripto_sum <= 35000:
            cripto_exempt = True

        for item in investments:
            if (item["sell_date"]-item["buy_date"]).days < 1 and item["type"] in ["ações", "BDR", "ETF"]:
                taxes[item["name"]] = {
                    "name": item["name"],
                    "bank_id": item["bank_id"],
                    "type": item["type"],
                    "rate": item["rate"],
                    "buy_date": item["date"],
                    "sell_date": item["sell_date"],
                    "exempt": False,
                    "modality": "day_trade",
                    "taxes": item["profit"]*0.2,
                    "sell_value": item["sell_price"]
                }
                sum_taxes += item["profit"]*0.2
                day_trade_profit += item["profit"]
            elif (item["type"] == "fundo_imobiliário"):
                taxes[item["name"]] = {
                    "name": item["name"],
                    "bank_id": item["bank_id"],
                    "type": item["type"],
                    "rate": item["rate"],
                    "buy_date": item["date"],
                    "sell_date": item["sell_date"],
                    "exempt": False,
                    "modality": "not relevant",
                    "taxes": item["profit"]*0.2,
                    "sell_value": item["sell_price"]
                }
                fii_profit += item["profit"]
                sum_taxes += item["profit"]*0.2
            elif(item["type"] in ["BDR", "ETF", "fundo de ações"]):
                taxes[item["name"]] = {
                    "name": item["name"],
                    "bank_id": item["bank_id"],
                    "type": item["type"],
                    "rate": item["rate"],
                    "buy_date": item["date"],
                    "sell_date": item["sell_date"],
                    "exempt": False,
                    "modality": "not relevant",
                    "taxes": item["profit"]*0.15,
                    "sell_value": item["sell_price"]
                }
                swing_trade_profit += item["profit"]
                sum_taxes += item["profit"]*0.15

            elif item["type"] == "criptoativos":
                taxes[item["name"]] = {
                    "name": item["name"],
                    "bank_id": item["bank_id"],
                    "type": item["type"],
                    "rate": item["rate"],
                    "date": item["date"],
                    "buy_date": item["date"],
                    "sell_date": item["sell_date"],
                    "exempt": cripto_exempt,
                    "modality": "not relevant",
                    "taxes": item["profit"]*TaxCalculator.get_cripto_price(math.floor(item[cripto_sum])),
                    "sell_value": item["sell_price"]
                }
                cripto_profit += item["profit"]
                sum_taxes += item["profit"] * \
                    TaxCalculator.get_cripto_price(
                        math.floor(item[cripto_sum]))
            elif item["type"] == "ações" and stock_exempt:
                taxes[item["name"]] = {
                    "name": item["name"],
                    "bank_id": item["bank_id"],
                    "type": item["type"],
                    "rate": item["rate"],
                    "date": item["date"],
                    "buy_date": item["date"],
                    "sell_date": item["sell_date"],
                    "exempt": stock_exempt,
                    "modality": "not relevant",
                    "taxes": 0,
                    "sell_value": item["sell_price"]
                }
                swing_trade_profit += item["profit"]
            elif item["type"] == "ações" and not stock_exempt:
                taxes[item["name"]] = {
                    "name": item["name"],
                    "bank_id": item["bank_id"],
                    "type": item["type"],
                    "rate": item["rate"],
                    "date": item["date"],
                    "buy_date": item["date"],
                    "sell_date": item["sell_date"],
                    "exempt": stock_exempt,
                    "modality": "not relevant",
                    "taxes": item["profit"]*0.15,
                    "sell_value": item["sell_price"]
                }

                sum_taxes += item["profit"]*0.15
            elif (item["type"] == "fundos_acoes"):
                taxes[item["name"]] = {
                    "name": item["name"],
                    "bank_id": item["bank_id"],
                    "type": item["type"],
                    "rate": item["rate"],
                    "buy_date": item["date"],
                    "sell_date": item["sell_date"],
                    "exempt": False,
                    "modality": "not relevant",
                    "taxes": item["profit"]*0.15,
                    "sell_price": item["sell_price"]
                }
                sum_taxes += item["profit"]*0.15
        return {
            "day_trade_profit": (lambda x: x if x > 0 else 0)(day_trade_profit),
            "swing_trade_profit": (lambda x: x if x > 0 else 0)(swing_trade_profit),
            "cripto_profit": (lambda x: x if x > 0 else 0)(cripto_profit),
            "fii_profit": (lambda x: x if x > 0 else 0)(fii_profit),
            "day_trade_accumulated_loss": last_taxes["day_trade_accumulated_loss"]+(lambda x: x if x < 0 else 0)(day_trade_profit),
            'swing_trade_accumulated_loss': last_taxes["swing_accumulated_loss"]+(lambda x: x if x < 0 else 0)(swing_trade_profit),
            "fii_accumulated_loss": last_taxes["fii_loss"]+(lambda x: x if x < 0 else 0)(fii_profit),
            'cripto_accumulated_loss': last_taxes["cripto_accumulated_loss"]+(lambda x: x if x < 0 else 0)(cripto_profit),
            "taxes": sum_taxes,
            'date': datetime.strptime(current_date, "%Y-%m").replace(day=1).strftime("%Y-%m-%d"),
        }

    def cuts(this_taxes):
        return {
            "day_trade_profit": this_taxes['day_trade_profit'],
            "swing_trade_profit": this_taxes["swing_trade_profit"],
            "cripto_profit": this_taxes["cripto_profit"],
            "fii_profit": this_taxes["fii_profit"],
            "day_trade_accumulated_loss": (lambda x, y: 0 if y > x else x-y)(this_taxes["day_trade_accumulated_loss"], this_taxes['day_trade_profit']),
            'swing_trade_accumulated_loss': (lambda x, y: 0 if y > x else x-y)(this_taxes["swing_trade_accumulated_loss"], this_taxes['swing_trade_profit']),
            "fii_accumulated_loss": (lambda x, y: 0 if y > x else x-y)(this_taxes["fii_accumulated_loss"], this_taxes['fii_profit']),
            'cripto_accumulated_loss': (lambda x, y: 0 if y > x else x-y)(this_taxes["cripto_accumulated_loss"], this_taxes['cripto_profit']),
            "taxes": (this_taxes["day_trade_profit"] - this_taxes["day_trade_accumulated_loss"])*0.2+(this_taxes["swing_trade_profit"]-this_taxes["swing_trade_accumulated_loss"])*0.15+(this_taxes["cripto_profit"]-this_taxes["cripto_accumulated_loss"])*TaxCalculator.get_cripto_price(math.floor(this_taxes["cripto_profit"]))+(this_taxes["fii_profit"]-this_taxes["fii_accumulated_loss"])*0.2,
            'date': this_taxes["date"]
        }

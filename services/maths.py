import datetime
import math
from datetime import datetime


def return_index(investments_last_month, investment_this_month):
    for item in investments_last_month:
        if item["name"] == investment_this_month["name"]:
            return item["price"]


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
        for investment_this_month in investments_this_month_sold:

            last_price = return_index(
                investments_last_month, investment_this_month)
            if (last_price is None):
                last_price = 0
            investments[investment_this_month["name"]] = {
                "name": investment_this_month["name"],
                "bank_id": investment_this_month["bank_id"],
                "itype": investment_this_month["itype"],
                "rate": investment_this_month["rate"],
                "buy_date": investment_this_month["buy_date"],
                "sell_date": investment_this_month["sell_date"],
                "exempt": False,
                "profit": investment_this_month["price"] - last_price
            }

        for item in list(investments):

            item = investments[item]
            print("aaaaaaaaa", item)
            print((datetime.strptime(item["sell_date"], "%Y-%m-%d") -
                  datetime.strptime(item["buy_date"], "%Y-%m-%d")).days)
            if item["itype"] == "criptoativo":
                cripto_sum += item["profit"]
            elif item["itype"] == "ação" and (datetime.strptime(item["sell_date"], "%Y-%m-%d")-datetime.strptime(item["buy_date"], "%Y-%m-%d")).days >= 1:
                stocks_sum += item["profit"]
        if stocks_sum <= 20000:
            stock_exempt = True
        if cripto_sum <= 35000:
            cripto_exempt = True
        print(cripto_sum, stocks_sum)
        for item in list(investments):
            item = investments[item]
            if (datetime.strptime(item["sell_date"], "%Y-%m-%d")-datetime.strptime(item["buy_date"], "%Y-%m-%d")).days < 1 and item["itype"] in ["ação", "BDR", "ETF"]:
                taxes[item["name"]] = {
                    "name": item["name"],
                    "bank_id": item["bank_id"],
                    "itype": item["itype"],
                    "rate": item["rate"],
                    "buy_date": item["buy_date"],
                    "sell_date": item["sell_date"],
                    "exempt": False,
                    "modality": "day_trade",
                    "taxes": item["profit"]*0.2,
                    "profit": item["profit"]
                }
                sum_taxes += item["profit"]*0.2
                day_trade_profit += item["profit"]
            elif (item["itype"] == "fundo_imobiliário"):
                taxes[item["name"]] = {
                    "name": item["name"],
                    "bank_id": item["bank_id"],
                    "itype": item["itype"],
                    "rate": item["rate"],
                    "buy_date": item["buy_date"],
                    "sell_date": item["sell_date"],
                    "exempt": False,
                    "modality": "not relevant",
                    "taxes": item["profit"]*0.2,
                    "profit": item["profit"]
                }
                fii_profit += item["profit"]
                sum_taxes += item["profit"]*0.2
            elif(item["itype"] in ["BDR", "ETF", "fundo de ação"]):
                taxes[item["name"]] = {
                    "name": item["name"],
                    "bank_id": item["bank_id"],
                    "itype": item["itype"],
                    "rate": item["rate"],
                    "buy_date": item["buy_date"],
                    "sell_date": item["sell_date"],
                    "exempt": False,
                    "modality": "not relevant",
                    "taxes": item["profit"]*0.15,
                    "profit": item["profit"]
                }
                swing_trade_profit += item["profit"]
                sum_taxes += item["profit"]*0.15

            elif item["itype"] == "criptoativos":
                taxes[item["name"]] = {
                    "name": item["name"],
                    "bank_id": item["bank_id"],
                    "itype": item["itype"],
                    "rate": item["rate"],
                    "buy_date": item["buy_date"],
                    "buy_date": item["buy_date"],
                    "sell_date": item["sell_date"],
                    "exempt": cripto_exempt,
                    "modality": "not relevant",
                    "taxes": item["profit"]*TaxCalculator.get_cripto_price(math.floor(item[cripto_sum])),
                    "profit": item["profit"]
                }
                cripto_profit += item["profit"]
                sum_taxes += item["profit"] * \
                    TaxCalculator.get_cripto_price(
                        math.floor(item[cripto_sum]))

            elif item["itype"] == "ação" and stock_exempt:
                print("cheeeeegou")
                taxes[item["name"]] = {
                    "name": item["name"],
                    "bank_id": item["bank_id"],
                    "itype": item["itype"],
                    "rate": item["rate"],
                    "buy_date": item["buy_date"],
                    "buy_date": item["buy_date"],
                    "sell_date": item["sell_date"],
                    "exempt": stock_exempt,
                    "modality": "not relevant",
                    "taxes": 0,
                    "profit": item["profit"]
                }
                swing_trade_profit += item["profit"]
            elif item["itype"] == "ação" and not stock_exempt:
                taxes[item["name"]] = {
                    "name": item["name"],
                    "bank_id": item["bank_id"],
                    "itype": item["itype"],
                    "rate": item["rate"],
                    "buy_date": item["buy_date"],
                    "buy_date": item["buy_date"],
                    "sell_date": item["sell_date"],
                    "exempt": stock_exempt,
                    "modality": "not relevant",
                    "taxes": item["profit"]*0.15,
                    "profit": item["profit"]
                }

                sum_taxes += item["profit"]*0.15
            elif (item["itype"] == "fundos_acoes"):
                taxes[item["name"]] = {
                    "name": item["name"],
                    "bank_id": item["bank_id"],
                    "itype": item["itype"],
                    "rate": item["rate"],
                    "buy_date": item["buy_date"],
                    "sell_date": item["sell_date"],
                    "exempt": False,
                    "modality": "not relevant",
                    "taxes": item["profit"]*0.15,
                    "price": item["price"]
                }
                sum_taxes += item["profit"]*0.15
        temp = {
            "day_trade_profit": (lambda x: x if x > 0 else 0)(day_trade_profit),
            "swing_trade_profit": (lambda x: x if x > 0 else 0)(swing_trade_profit),
            "cripto_profit": (lambda x: x if x > 0 else 0)(cripto_profit),
            "fii_profit": (lambda x: x if x > 0 else 0)(fii_profit),
            "day_trade_accumulated_loss": last_taxes["day_trade_accumulated_loss"]+(lambda x: x if x < 0 else 0)(day_trade_profit),
            'swing_trade_accumulated_loss': last_taxes["swing_accumulated_loss"]+(lambda x: x if x < 0 else 0)(swing_trade_profit),
            "fii_accumulated_loss": last_taxes["fii_loss"]+(lambda x: x if x < 0 else 0)(fii_profit),
            'cripto_accumulated_loss': last_taxes["cripto_accumulated_loss"]+(lambda x: x if x < 0 else 0)(cripto_profit),
            "taxes": sum_taxes,
            'date': datetime.strptime(current_date, "%Y-%m-%d").replace(day=1).strftime("%Y-%m"),
        }

        return {
            "day_trade_profit": temp['day_trade_profit'],
            "swing_trade_profit": temp["swing_trade_profit"],
            "cripto_profit": temp["cripto_profit"],
            "fii_profit": temp["fii_profit"],
            "day_trade_accumulated_loss": (lambda x, y: 0 if y > x else x-y)(temp["day_trade_accumulated_loss"], temp['day_trade_profit']),
            'swing_trade_accumulated_loss': (lambda x, y: 0 if y > x else x-y)(temp["swing_trade_accumulated_loss"], temp['swing_trade_profit']),
            "fii_accumulated_loss": (lambda x, y: 0 if y > x else x-y)(temp["fii_accumulated_loss"], temp['fii_profit']),
            'cripto_accumulated_loss': (lambda x, y: 0 if y > x else x-y)(temp["cripto_accumulated_loss"], temp['cripto_profit']),
            "taxes": (temp["day_trade_profit"] - temp["day_trade_accumulated_loss"])*0.2+(temp["swing_trade_profit"]-temp["swing_trade_accumulated_loss"])*0.15+(temp["cripto_profit"]-temp["cripto_accumulated_loss"])*TaxCalculator.get_cripto_price(math.floor(temp["cripto_profit"]))+(temp["fii_profit"]-temp["fii_accumulated_loss"])*0.2,
            'date': temp["date"]
        }

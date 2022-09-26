import datetime
import math
from datetime import datetime

from models import investment


def return_index(investments_last_month, investment_this_month):
    for item in investments_last_month:

        if item["name"] == investment_this_month["name"] and not item["sell_price"]:
            return item["price"]


def get_cripto_tax(value: float):
    cripto_tax = [
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

    for cripto_price in cripto_tax:
        if (cripto_price.get("else", None)):
            return cripto_price["else"]
        if value in cripto_price["range"]:
            return cripto_price["result"]


def sum_values(investments_this_month_sold):
    sum_cripto = 0
    sum_stock = 0

    for item in investments_this_month_sold:

        if item["itype"] == "ação":
            sum_stock += item["buy_price"] - item["sell_price"]

        elif item["itype"] == "criptoativos":
            sum_cripto += item["buy_price"] - item["sell_price"]

    return (sum_cripto, sum_stock)


class TaxCalculator:

    def taxes(investments_this_month_sold, current_date, last_taxes={"day_trade_accumulated_loss": 0, "swing_accumulated_loss": 0, "fii_loss": 0, "cripto_accumulated_loss": 0}):
        investment_taxes = []
        day_trade_profit = 0
        swing_trade_profit = 0
        cripto_profit = 0
        fii_profit = 0
        taxes_sum = 0

        for (i, investment) in enumerate(investments_this_month_sold):

            investment_taxes.append(investment)

            if (investment["sell_date"] - investment["buy_date"]).days < 1 and investment["itype"] in ["BDR", "ação", "ETF"]:

                investment_taxes[investment["id"]]["taxes"] = (
                    investment_taxes[investment["id"]]["sell_price"] - investment_taxes[investment["id"]]["buy_price"])*0.2
                taxes_sum += investment_taxes[investment["id"]]["taxes"]
                day_trade_profit += investment_taxes[investment["id"]
                                                     ]["sell_price"] - investment_taxes[investment["id"]]["buy_price"]

            elif investment["itype"] in ["BDR", "ETF"]:

                investment_taxes[investment["id"]]["taxes"] = (
                    investment_taxes[investment["id"]]["buy_price"] - investment_taxes[investment["id"]]["buy_price"])*0.15
                taxes_sum += investment_taxes[investment["id"]]["taxes"]
                swing_trade_profit += investment_taxes[investment["id"]
                                                       ]["sell_price"] - investment_taxes[investment["id"]]["buy_price"]

            elif investment["itype"] == "fundo imobiliário":

                investment_taxes[investment["id"]]["taxes"] = (
                    investment_taxes[investment["id"]]["sell_price"] - investment_taxes[investment["id"]]["buy_price"])*0.2
                taxes_sum += investment_taxes[investment["id"]]["taxes"]
                fii_profit += investment_taxes[investment["id"]]["sell_price"] - \
                    investment_taxes[investment["id"]]["buy_price"]

            elif investment["itype"] == "criptoativos":

                investment_taxes[investment["id"]]["taxes"] = (
                    investment_taxes[investment["id"]]["sell_price"] - investment_taxes[investment["id"]]["buy_price"])*get_cripto_tax(sum_values(investments_this_month_sold)[0])
                taxes_sum += investment_taxes[investment["id"]]["taxes"]
                cripto_profit += investment_taxes[investment["id"]]["sell_price"] - \
                    investment_taxes[investment["id"]]["buy_price"]

            elif sum_values(investments_this_month_sold)[1] > 20000:
                if investment["itype"] == "ação":

                    investment_taxes[investment["id"]]["taxes"] = (
                        investment_taxes[investment["id"]]["sell_price"] - investment_taxes[investment["id"]]["buy_price"])*0.2
                    taxes_sum += investment_taxes[investment["id"]]["taxes"]
                    swing_trade_profit += investment_taxes[investment["id"]]["sell_price"] - \
                        investment_taxes[investment["id"]]["buy_price"]

            elif sum_values(investments_this_month_sold)[1] < 20000:
                if investment["itype"] == "ação":

                    investment_taxes[i]["taxes"] = 0
                    taxes_sum += investment_taxes[i]["taxes"]
                    swing_trade_profit += investment_taxes[i]["sell_price"] - \
                        investment_taxes[i]["buy_price"]

        temp = {
            "day_trade_profit": (lambda x: x if x > 0 else 0)(day_trade_profit),
            "swing_trade_profit": (lambda x: x if x > 0 else 0)(swing_trade_profit),
            "cripto_profit": (lambda x: x if x > 0 else 0)(cripto_profit),
            "fii_profit": (lambda x: x if x > 0 else 0)(fii_profit),
            "day_trade_accumulated_loss": last_taxes["day_trade_accumulated_loss"]+(lambda x: x if x < 0 else 0)(day_trade_profit),
            'swing_trade_accumulated_loss': last_taxes["swing_accumulated_loss"]+(lambda x: x if x < 0 else 0)(swing_trade_profit),
            "fii_accumulated_loss": last_taxes["fii_loss"]+(lambda x: x if x < 0 else 0)(fii_profit),
            'cripto_accumulated_loss': last_taxes["cripto_accumulated_loss"]+(lambda x: x if x < 0 else 0)(cripto_profit),
            "taxes": taxes_sum,
            'date': datetime.strptime(current_date, "%Y-%m-%d").replace(day=1).strftime("%Y-%m")
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

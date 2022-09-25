import datetime
import math


def calculate_taxes(investments_this_month, investments_last_month, last_taxes):
    investments = {}
    investments_sell_dates = []
    cripto_prices = {
        range(0, 35001): 0.15,
        range(35001, 5000001): 0.15,
        range(5000001, 100000001): 0.175,
        range(100000001, 300000001): 0.2,
        range(300000001, math.inf): 0.2,
    }
    taxes = {}
    cripto_sum = 0
    stocks_sum = 0
    day_trade_profit =0
    swing_trade_profit =0
    cripto_profit =0
    fii_profit =0
    sum_taxes =0
    
    
    for investment_last_month in investments_last_month:
        investments_sell_dates.append(investment_last_month["sell_date"])

    for investment_this_month in investments_this_month:
        index = investments_last_month.index(investment_this_month["name"])
        if investment_this_month["sell_date"] and not list(investments_last_month)[index]["sell date"]:
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
        if item["type"] == "criptoativos":
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
                "taxes": item["profit"]*0.2
            }
            sum_taxes += item["profit"]*0.2
            day_trade_profit +=item["profit"]
        elif (item["type"] == "fundos_imobiliários"):
            taxes[item["name"]] = {
                "name": item["name"],
                "bank_id": item["bank_id"],
                "type": item["type"],
                "rate": item["rate"],
                "buy_date": item["date"],
                "sell_date": item["sell_date"],
                "exempt": False,
                "modality": "not relevant",
                "taxes": item["profit"]*0.2
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
                "taxes": item["profit"]*0.15
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
                "taxes": item["profit"]*cripto_prices[math.floor(item[cripto_sum])]
            }
            cripto_profit += item["profit"]
            sum_taxes += item["profit"]*cripto_prices[math.floor(item[cripto_sum])]
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
                "taxes": 0
            }
            swing_trade_profit +=item["profit"]
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
                "taxes": item["profit"]*0.15
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
                "taxes": item["profit"]*0.15
            }
            sum_taxes += item["profit"]*0.15
    return {
            "customer_id ":investment_this_month["customer_id"],
            "day_trade_profit" : (lambda x: x if x>0 else 0 )(day_trade_profit),
            "swing_trade_profit" :(lambda x: x if x>0 else 0 )(swing_trade_profit),
            "cripto_profit" :(lambda x: x if x>0 else 0 )(cripto_profit),
            "fii_profit" :(lambda x: x if x>0 else 0 )(fii_profit),
            "day_trade_accumulated_loss" :(lambda x: x if x<0 else 0 )(day_trade_profit) ,
            'swing_trade_accumulated_loss':(lambda x: x if x<0 else 0 )(swing_trade_profit) ,
            "fii_loss" :(lambda x: x if x<0 else 0 )(fii_profit) ,
            'cripto_accumulated_loss':(lambda x: x if x<0 else 0 )(cripto_profit) ,
            "acumulated_loss": (lambda x: x if x<0 else 0 )(0),
            "taxes": sum_taxes,
            'date' : datetime.datetime.strptime(investment_this_month[0]["date"], "%Y-%m-%d %H:%M:%S").month
        }


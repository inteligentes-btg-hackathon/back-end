from datetime import datetime
import math

cripto_prices = {
        range(0, 35001): 0.15,
        range(35001, 5000001): 0.15,
        range(5000001, 100000001): 0.175,
        range(100000001, 300000001): 0.2,
        range(300000001, math.inf): 0.225,
}
def calculate_cuts(this_taxes):
     return {
            "customer_id ":this_taxes["customer_id"],
            "day_trade_profit" : this_taxes['day_trade_profit'],
            "swing_trade_profit" :this_taxes["swing_trade_profit"],
            "cripto_profit" :this_taxes["cripto_profit"],
            "fii_profit" :this_taxes["fii_profit"],
            "day_trade_accumulated_loss" :(lambda x,y:0 if y>x else x-y)(this_taxes["day_trade_accumulated_loss"],this_taxes['day_trade_profit']) ,
            'swing_trade_accumulated_loss':(lambda x,y:0 if y>x else x-y)(this_taxes["swing_trade_accumulated_loss"],this_taxes['swing_trade_profit']) ,
            "fii_accumulated_loss" :(lambda x,y:0 if y>x else x-y)(this_taxes["fii_accumulated_loss"],this_taxes['fii_profit']) ,
            'cripto_accumulated_loss':(lambda x,y:0 if y>x else x-y)(this_taxes["cripto_accumulated_loss"],this_taxes['cripto_profit']) ,
            "acumulated_loss": this_taxes["taxes"],
            "taxes": (this_taxes["day_trade_profit"] -this_taxes["day_trade_accumulated_loss"])*0.2+(this_taxes["swing_trade_profit"]-this_taxes["swing_trade_accumulated_loss"])*0.15+(this_taxes["cripto_profit"]-this_taxes["cripto_accumulated_loss"])*cripto_prices[math.floor(this_taxes["cripto_profit"])]+(this_taxes["fii_profit"]-this_taxes["fii_profit_accumulated_loss"])*0.2,
            'date' : this_taxes["date"]
        }

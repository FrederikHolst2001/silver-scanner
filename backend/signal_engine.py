
from utils import extract_weight
from silver_price import get_silver_price

def calculate_profit(deal):
    weight=extract_weight(deal["title"])
    if not weight: return None
    silver=get_silver_price()
    melt=weight*silver
    deal["profit"]=round(melt-deal["price"],2)
    return deal

def profit_score(deal):
    return min(100,max(0,int(deal.get("profit",0))))

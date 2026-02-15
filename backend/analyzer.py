
def analyze(price, weight, silver_price):
    ppg = price / weight
    profit_per_gram = silver_price - ppg
    total_profit = profit_per_gram * weight

    return {
        "price_per_gram": round(ppg,2),
        "profit": round(total_profit,2),
        "good": total_profit > 0
    }

import sys, os, time, threading

sys.path.append(os.path.dirname(__file__))

from flask import Flask, jsonify, send_from_directory

from scraper_dba_live import scrape_dba_live
from scraper_facebook_live import scrape_facebook_live
from signal_engine import calculate_profit, profit_score
from db import init_db, save_deal, get_deals
from alerts import send_alert

SCAN_INTERVAL = 60

# vigtig: peg på frontend mappe
app = Flask(__name__, static_folder="../frontend")

init_db()


# API endpoint
@app.route("/api/deals")
def api_deals():
    return jsonify(get_deals())


# DASHBOARD endpoint (forside)
@app.route("/")
def dashboard():
    return send_from_directory("../frontend", "index.html")


# scanner loop
def scanner():

    while True:

        try:

            deals = []

            deals.extend(scrape_dba_live())
            deals.extend(scrape_facebook_live())

            for deal in deals:

                deal = calculate_profit(deal)

                if not deal:
                    continue

                deal["score"] = profit_score(deal)

                if deal["profit"] >= 50:

                    save_deal(deal)

                    send_alert(
                        f"Profit {deal['profit']} kr\n{deal['title']}"
                    )

        except Exception as e:

            print("Scanner error:", e)

        time.sleep(SCAN_INTERVAL)


threading.Thread(target=scanner, daemon=True).start()


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)

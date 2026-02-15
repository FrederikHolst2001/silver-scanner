
from flask import Flask, jsonify, send_from_directory
import threading
import time
import os

import backend.db as db
import backend.scraper_dba as scraper_dba
import backend.scraper_guloggratis as scraper_guloggratis
import backend.analyzer as analyzer
import backend.silver_price as silver_price

app = Flask(__name__, static_folder="../frontend")

db.init()

SCAN_INTERVAL = 300

def scan_loop():
    while True:
        try:
            silver = silver_price.get_silver_price()
            sources = []
            sources.extend(scraper_dba.scrape())
            sources.extend(scraper_guloggratis.scrape())

            for item in sources:
                result = analyzer.analyze(
                    item["price"],
                    item["weight"],
                    silver
                )

                if result["profit"] > 25:
                    deal = {**item, **result}
                    db.insert(deal)
                    print("Saved deal:", deal["title"])

        except Exception as e:
            print("Scan error:", e)

        time.sleep(SCAN_INTERVAL)

@app.route("/api/deals")
def deals():
    return jsonify(db.get_all())

@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")

threading.Thread(target=scan_loop, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

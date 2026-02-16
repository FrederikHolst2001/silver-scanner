import requests
from bs4 import BeautifulSoup
import re

BASE = "https://www.dba.dk"

def scrape_dba():

    url = "https://www.dba.dk/soeg/?soeg=925 sølv"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    deals = []

    try:

        r = requests.get(url, headers=headers, timeout=15)

        soup = BeautifulSoup(r.text, "lxml")

        links = soup.find_all("a", href=True)

        for link in links:

            text = link.get_text(" ").strip().lower()

            if len(text) < 10 or len(text) > 200:
                continue

            price_match = re.search(r'(\d+(?:[.,]\d+)?)\s?kr', text)
            weight_match = re.search(r'(\d+(?:[.,]\d+)?)\s?g', text)

            if not price_match or not weight_match:
                continue

            price = float(price_match.group(1).replace(",", "."))

            href = link["href"]

            if not href.startswith("http"):
                href = BASE + href

            deals.append({
                "title": text,
                "price": price,
                "link": href
            })

        print("DBA deals found:", len(deals))

    except Exception as e:

        print("DBA error:", e)

    return deals
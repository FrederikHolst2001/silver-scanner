import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://www.guloggratis.dk"

def scrape_guloggratis_live():

    url = "https://www.guloggratis.dk/soeg?q=925%20sølv"

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    deals = []

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(response.text, "lxml")

        listings = soup.select("a")

        for item in listings:

            text = item.get_text(" ").strip().lower()

            if len(text) < 10 or len(text) > 200:
                continue

            price_match = re.search(
                r'(\d+(?:[.,]\d+)?)\s?kr',
                text
            )

            weight_match = re.search(
                r'(\d+(?:[.,]\d+)?)\s?g',
                text
            )

            if not price_match or not weight_match:
                continue

            price = float(
                price_match.group(1).replace(",", ".")
            )

            link = item.get("href", "")

            if not link.startswith("http"):
                link = BASE_URL + link

            deals.append({

                "title": text,
                "price": price,
                "link": link

            })

        print("GulogGratis deals found:", len(deals))

        return deals

    except Exception as e:

        print("GulogGratis scrape error:", e)

        return []
import requests
from bs4 import BeautifulSoup
import re

BASE = "https://www.dba.dk"

SILVER_KEYWORDS = [
    "sølv",
    "925",
    "sterling",
    "830",
    "835"
]

SEARCH_URL = "https://www.dba.dk/soeg/?soeg=925 sølv"

def scrape_dba():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    deals = []

    try:

        r = requests.get(SEARCH_URL, headers=headers, timeout=15)

        soup = BeautifulSoup(r.text, "lxml")

        # DBA listings ligger i article tags
        listings = soup.find_all("article")

        for item in listings:

            text = item.get_text(" ").lower()

            # kun sølv
            if not any(word in text for word in SILVER_KEYWORDS):
                continue

            price_match = re.search(r'(\d+(?:[.,]\d+)?)\s?kr', text)
            weight_match = re.search(r'(\d+(?:[.,]\d+)?)\s?g', text)

            if not price_match or not weight_match:
                continue

            price = float(price_match.group(1).replace(",", "."))

            link_tag = item.find("a", href=True)

            if not link_tag:
                continue

            link = link_tag["href"]

            if not link.startswith("http"):
                link = BASE + link

            title = link_tag.get_text().strip()

            deals.append({

                "title": title,
                "price": price,
                "link": link

            })

        print("DBA silver deals:", len(deals))

    except Exception as e:

        print("DBA error:", e)

    return deals
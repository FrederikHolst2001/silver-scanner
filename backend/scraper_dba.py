import requests
from bs4 import BeautifulSoup
import re
import time

BASE = "https://www.dba.dk"

SILVER_KEYWORDS = ["sølv", "925", "sterling"]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def extract_weight(url):

    try:

        r = requests.get(url, headers=HEADERS, timeout=10)

        soup = BeautifulSoup(r.text, "lxml")

        text = soup.get_text(" ").lower()

        match = re.search(r'(\d+(?:[.,]\d+)?)\s?g', text)

        if match:
            return float(match.group(1).replace(",", "."))

    except:
        pass

    return None


def scrape_dba():

    search_url = "https://www.dba.dk/soeg/?soeg=925 sølv"

    deals = []

    r = requests.get(search_url, headers=HEADERS)

    soup = BeautifulSoup(r.text, "lxml")

    listings = soup.find_all("a", href=True)

    checked = 0

    for link in listings:

        title = link.get_text().lower().strip()

        if not any(k in title for k in SILVER_KEYWORDS):
            continue

        href = link["href"]

        if "/annonce/" not in href:
            continue

        url = BASE + href

        price_match = re.search(r'(\d+)\s?kr', title)

        if not price_match:
            continue

        price = float(price_match.group(1))

        # 🔥 hent vægt fra annonce
        weight = extract_weight(url)

        if not weight:
            continue

        deals.append({
            "title": title,
            "price": price,
            "weight": weight,
            "link": url
        })

        checked += 1

        time.sleep(1)  # undgå blokering

        if checked > 10:
            break

    print("REAL DBA deals:", len(deals))

    return deals
import requests
from bs4 import BeautifulSoup
import re

def scrape_dba_live():

    url = "https://www.dba.dk/soeg/?soeg=925+sølv"

    headers = {
        "User-Agent":
        "Mozilla/5.0"
    }

    html = requests.get(url, headers=headers).text

    soup = BeautifulSoup(html, "lxml")

    deals = []

    for a in soup.find_all("a", href=True):

        text = a.get_text(" ").lower()

        if len(text) > 200:
            continue

        price = re.search(r'(\d+)\s?kr', text)
        weight = re.search(r'(\d+)\s?g', text)

        if price and weight:

            deals.append({

                "title": text,

                "price": float(price.group(1)),

                "link": "https://www.dba.dk" + a["href"]

            })

    print("DBA valid deals:", len(deals))

    return deals

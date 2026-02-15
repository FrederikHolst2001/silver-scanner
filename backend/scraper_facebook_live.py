import requests
import re

def scrape_facebook_live():

    url = "https://www.facebook.com/marketplace/search/?query=925%20sølv"

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    html = requests.get(url, headers=headers).text

    deals = []

    lines = html.split("\n")

    for line in lines:

        line = line.strip().lower()

        # IGNORER scripts og json
        if "<script" in line:
            continue

        if "requirelazy" in line:
            continue

        price = re.search(r'(\d+)\s?kr', line)
        weight = re.search(r'(\d+)\s?g', line)

        if price and weight and len(line) < 200:

            deals.append({

                "title": line,

                "price": float(price.group(1)),

                "link": url

            })

    print("Facebook valid deals:", len(deals))

    return deals

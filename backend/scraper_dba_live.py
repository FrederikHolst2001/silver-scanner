import requests

def scrape_dba_live():

    deals = []

    try:

        url = "https://www.dba.dk/soeg/"

        params = {
            "soeg": "925 sølv"
        }

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        html = response.text

        lines = html.split("\n")

        for line in lines:

            if "kr" in line and "g" in line:

                import re

                price = re.search(r'(\d+)\s?kr', line.lower())
                weight = re.search(r'(\d+)\s?g', line.lower())

                if price and weight:

                    deals.append({

                        "title": line.strip(),

                        "price": float(price.group(1)),

                        "link": "https://www.dba.dk"

                    })

        print("DBA deals:", len(deals))

        return deals

    except Exception as e:

        print("DBA error:", e)

        return []
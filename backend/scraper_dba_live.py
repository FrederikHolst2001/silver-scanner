import requests

def scrape_dba_live():

    url = "https://api.dba.dk/api/search"

    params = {

        "q": "925 sølv",
        "page": 1,
        "limit": 50

    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        data = response.json()

        deals = []

        for item in data.get("items", []):

            title = item.get("title", "")
            price = item.get("price", 0)
            link = "https://www.dba.dk" + item.get("url", "")

            deals.append({

                "title": title,
                "price": float(price),
                "link": link

            })

        print("DBA JSON deals found:", len(deals))

        return deals

    except Exception as e:

        print("DBA API error:", e)

        return []
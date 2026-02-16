from playwright.sync_api import sync_playwright
import re

def scrape_dba_live():

    deals = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(
            "https://www.dba.dk/soeg/?soeg=925+sølv"
        )

        page.wait_for_timeout(3000)

        content = page.content()

        browser.close()

    lines = content.split("\n")

    for line in lines:

        price = re.search(r'(\d+)\s?kr', line.lower())
        weight = re.search(r'(\d+)\s?g', line.lower())

        if price and weight:

            deals.append({

                "title": line.strip(),
                "price": float(price.group(1)),
                "link": "https://www.dba.dk"

            })

    print("DBA playwright deals:", len(deals))

    return deals
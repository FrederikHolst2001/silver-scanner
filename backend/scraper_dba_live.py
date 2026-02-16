from playwright.sync_api import sync_playwright
import re

def scrape_dba_live():

    deals = []

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu"
                ]
            )

            page = browser.new_page()

            page.goto(
                "https://www.dba.dk/soeg/?soeg=925+sølv",
                timeout=60000
            )

            page.wait_for_timeout(5000)

            content = page.content()

            browser.close()

        lines = content.split("\n")

        for line in lines:

            line = line.lower()

            price = re.search(r'(\d+)\s?kr', line)
            weight = re.search(r'(\d+)\s?g', line)

            if price and weight and len(line) < 200:

                deals.append({

                    "title": line.strip(),

                    "price": float(price.group(1)),

                    "link": "https://www.dba.dk"

                })

        print("DBA deals found:", len(deals))

        return deals

    except Exception as e:

        print("Playwright error:", e)

        return []

# Facebook scraping requires login session cookie for full access.
# This version uses public search fallback.

import requests, re

def scrape_facebook_live():
    url="https://www.facebook.com/marketplace/search/?query=925%20sølv"
    deals=[]
    try:
        html=requests.get(url,timeout=10).text

        for line in html.split("\n"):

            price=re.search(r'(\d+)\s?kr',line.lower())
            weight=re.search(r'(\d+)\s?g',line.lower())

            if price and weight:

                deals.append({
                    "title":line.strip(),
                    "price":float(price.group(1)),
                    "link":url
                })

    except Exception as e:
        print("Facebook scrape error:",e)

    return deals

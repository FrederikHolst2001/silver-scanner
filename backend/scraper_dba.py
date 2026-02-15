
import requests
from bs4 import BeautifulSoup
import re

def scrape():
    url = "https://www.dba.dk/soeg/?soeg=925+sølv"
    results = []
    try:
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html,"lxml")
        for a in soup.find_all("a"):
            text = a.get_text(" ")
            weight = re.search(r'(\d+)\s?g', text.lower())
            price = re.search(r'(\d+)\s?kr', text.lower())
            if weight and price:
                results.append({
                    "title": text.strip(),
                    "price": float(price.group(1)),
                    "weight": float(weight.group(1)),
                    "link": url,
                    "source": "DBA"
                })
    except:
        pass
    return results


import requests, re
from bs4 import BeautifulSoup

def scrape_dba_live():
    url="https://www.dba.dk/soeg/?soeg=925+sølv"
    deals=[]
    try:
        html=requests.get(url,timeout=10).text
        soup=BeautifulSoup(html,"lxml")

        for a in soup.find_all("a",href=True):
            text=a.get_text(" ").strip()

            price_match=re.search(r'(\d+[.,]?\d*)\s?kr',text.lower())
            weight_match=re.search(r'(\d+[.,]?\d*)\s?g',text.lower())

            if price_match and weight_match:

                deals.append({
                    "title":text,
                    "price":float(price_match.group(1).replace(",",".")),
                    "link":"https://www.dba.dk"+a["href"]
                })

    except Exception as e:
        print("DBA scrape error:",e)

    return deals


import requests,re
from bs4 import BeautifulSoup
def get_silver_price():
    try:
        html=requests.get("https://nordiskguld.dk/soelvpriser",timeout=10).text
        soup=BeautifulSoup(html,"lxml")
        text=soup.get_text()
        match=re.search(r'(\d+,\d+)\s*kr',text)
        if match:
            return float(match.group(1).replace(",","."))
    except: pass
    return 11.2

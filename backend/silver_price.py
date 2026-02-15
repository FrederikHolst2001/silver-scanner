
import requests
from bs4 import BeautifulSoup
import re

def get_silver_price():
    try:
        url = "https://nordiskguld.dk/soelvpriser"
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html,"lxml")
        text = soup.get_text()
        match = re.search(r'(\d+,\d+)\s*kr', text)
        if match:
            return float(match.group(1).replace(",", "."))
    except:
        pass
    return 11.20

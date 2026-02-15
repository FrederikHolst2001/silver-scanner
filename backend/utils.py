
import re
def extract_weight(text):
    match=re.search(r'(\d+(?:[.,]\d+)?)\s?g',text.lower())
    if match:
        return float(match.group(1).replace(",","."))
    return None

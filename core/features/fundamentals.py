import requests

headers = {"User-Agent": "Mozilla/5.0"}

def fetch_nse(symbol):
    try:
        s = requests.Session()
        s.get("https://www.nseindia.com", headers=headers)
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        return s.get(url, headers=headers).json()
    except:
        return None


def compute(df, symbol=None):
    raw = fetch_nse(symbol)

    if not raw:
        return {}

    meta = raw.get("metadata", {})
    sec = raw.get("securityInfo", {})

    return {
        "pe": meta.get("pE", 0),
        "pb": meta.get("pb", 0),
        "market_cap": meta.get("marketCap", 0),
        "roe": meta.get("roe", 0),
        "roce": meta.get("roce", 0),
        "promoter": sec.get("promoterHolding", 0),
    }
import urllib.request, json, datetime

BASE = "https://api.ratesdigest.com/v1/historical-rates"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:154.0) Gecko/20100101 Firefox/154.0",
    "Accept": "*/*",
    "Referer": "https://ratesdigest.com/",
    "Origin": "https://ratesdigest.com",
}

def fetch(rate_type):
    today = datetime.date.today()
    frm = today - datetime.timedelta(days=5)  # small buffer in case of no update today
    url = f"{BASE}?currency=USD&bank=Commercial%20Bank&type={rate_type}&from={frm}&to={today}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    if not data:
        raise ValueError(f"No data returned for {rate_type}")
    return data[-1]  # most recent point

def main():
    buying = fetch("tt_buying")
    selling = fetch("tt_selling")
    result = {
        "bank": "Commercial Bank",
        "currency": "USD",
        "tt_buying": buying["value"],
        "tt_selling": selling["value"],
        "as_of": buying["timestamp"],
        "fetched_at": int(datetime.datetime.utcnow().timestamp() * 1000),
    }
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    main()

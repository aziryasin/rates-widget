import urllib.request, urllib.parse, json, datetime, sys, time

BASE = "https://api.ratesdigest.com/v1/historical-rates"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:154.0) Gecko/20100101 Firefox/154.0",
    "Accept": "*/*",
    "Referer": "https://ratesdigest.com/",
    "Origin": "https://ratesdigest.com",
}

BANKS = [
    "Amana Bank",
    "Bank of Ceylon",
    "Cargills Bank",
    "Commercial Bank",
    "DFCC Bank",
    "Hatton National Bank",
    "National Development Bank",
    "National Savings Bank",
    "Nations Trust Bank",
    "People's Bank",
    "Sampath Bank",
    "Seylan Bank",
    "Standard Chartered Bank",
    "Union Bank",
    "Wise",
]


def fetch(rate_type, bank):
    today = datetime.date.today()
    frm = today - datetime.timedelta(days=5)  # small buffer in case of no update today
    query = urllib.parse.urlencode({
        "currency": "USD",
        "bank": bank,
        "type": rate_type,
        "from": frm,
        "to": today,
    })
    url = f"{BASE}?{query}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    if not data:
        raise ValueError(f"No data returned for {bank} / {rate_type}")
    return data[-1]  # most recent point


def fetch_bank(bank):
    buying = fetch("tt_buying", bank)
    selling = fetch("tt_selling", bank)
    return {
        "bank": bank,
        "currency": "USD",
        "tt_buying": buying["value"],
        "tt_selling": selling["value"],
        "as_of": buying["timestamp"],
    }


def main():
    banks_result = []
    for bank in BANKS:
        try:
            banks_result.append(fetch_bank(bank))
        except Exception as e:
            print(f"warning: failed to fetch {bank}: {e}", file=sys.stderr)
        time.sleep(0.3)  # be polite to the API between requests

    if not banks_result:
        raise RuntimeError("No banks fetched successfully; aborting so we don't publish an empty file")

    result = {
        "fetched_at": int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000),
        "banks": banks_result,
    }
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()

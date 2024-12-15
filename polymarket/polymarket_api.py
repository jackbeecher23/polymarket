import requests

def get_live_nfl_events():
    market_ids = []
    base_url = "https://gamma-api.polymarket.com"
    request_url = f"{base_url}/markets?active=true"
    response = requests.get(request_url)
    markets = response.json()
    for market in markets:
        market_ids.append(market["slug"])

    return market_ids




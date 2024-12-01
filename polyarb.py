import requests

POLY_API_URL = "https://gamma-api.polymarket.com/events?closed=false&limit=10000&tag=sports"

ODDS_API_KEY = "5742e13978ad1d823a371525dc38e02c"
ODDS_API_URL = "https://api.the-odds-api.com"

regions = "us"
markets = "h2h"
sport = "americanfootball_nfl"

def print_remaining_usage():
    response = requests.get(f"{ODDS_API_URL}/v4/sports/?apiKey={ODDS_API_KEY}")
    print(response.headers.get("x-requests-remaining"))

def get_request_nfl_games(ODDS_API_URL, ODDS_API_KEY, sport, regions, markets):
    response = requests.get(f"{ODDS_API_URL}/v4/sports/{sport}/odds/?apiKey={ODDS_API_KEY}&regions={regions}&markets={markets}");
    nfl_games = response.json()
    return nfl_games

def print_polymarket_events(POLY_API_URL):
    response = requests.get(POLY_API_URL)
    events = response.json()
    for event in events:
        if (event['tags'][0]['label'] == "Sports" and event['tags'][1]['label'] == "NFL"):
            print(event['title'])
            for market in event['markets']:
                print(market['question'])
                print(market['outcomePrices'])


def create_average_odds_dict():
    for game in games:
        home_team = game.get("home_team")
        home_team_sum_odds = 0
        away_team = game.get("away_team")
        away_team_sum_odds = 0
        bookmakers = game.get("bookmakers")
        bookmaker_count = 0
        for bookmaker in bookmakers:
            bookmaker_count += 1
            markets = bookmaker.get("markets")
            for market in markets:
                outcomes = market.get("outcomes")
                print(bookmaker.get("title"))
                for outcome in outcomes:
                    team = outcome.get("name")
                    odds = outcome.get("price")
                    if (team == home_team):
                        home_team_sum_odds += odds 
                    else:
                        away_team_sum_odds += odds 
                    print(f"{team}: {odds}")

        home_team_average_odds = home_team_sum_odds / bookmaker_count
        away_team_average_odds = away_team_sum_odds / bookmaker_count
        print("AVERAGE ODDS:")
        print(f"{home_team}: {home_team_average_odds}, {away_team}: {away_team_average_odds}")

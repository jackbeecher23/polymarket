import requests
import os

# check remaining api usage
def print_remaining_usage():
    response = requests.get(f"{ODDS_API_URL}/v4/sports/?apiKey={ODDS_API_KEY}")
    print(response.headers.get("x-requests-remaining"))

# get the nfl games from sportsbooks
def get_request_nba_games(ODDS_API_URL, ODDS_API_KEY, sport, regions, markets):
    response = requests.get(f"{ODDS_API_URL}/v4/sports/{sport}/odds/?apiKey={ODDS_API_KEY}&regions={regions}&markets={markets}");
    nba_games = response.json()
    return nba_games

# compile average odds from bookmakers and put them in dictionary
def create_average_odds_dict(ODDS_API_KEY):
    ODDS_API_KEY = ODDS_API_KEY 
    ODDS_API_URL = "https://api.the-odds-api.com"

    regions = "us"
    markets = "h2h"
    sport = "basketball_nba"
    vig_adjusted_average_odds = {}
    games = get_request_nba_games(ODDS_API_URL, ODDS_API_KEY, sport, regions, markets)

    # for each game
    for game in games:

        # set the home team
        home_team = game.get("home_team")
        home_team_no_city = home_team.split(" ")[-1]
        home_team_sum_odds = 0

        # set the away team
        away_team = game.get("away_team")
        away_team_no_city = away_team.split(" ")[-1]
        away_team_sum_odds = 0

        # get all the bookmakers
        bookmakers = game.get("bookmakers")
        bookmaker_count = 0

        # for each bookmaker
        for bookmaker in bookmakers:
            bookmaker_count += 1
            markets = bookmaker.get("markets")

            # for each market
            for market in markets:
                outcomes = market.get("outcomes")
                for outcome in outcomes:
                    team = outcome.get("name")
                    odds = outcome.get("price")
                    # sum the odds
                    if (team == home_team):
                        home_team_sum_odds += odds 
                    else:
                        away_team_sum_odds += odds 

        # average the odds
        home_team_average_odds = home_team_sum_odds / bookmaker_count
        away_team_average_odds = away_team_sum_odds / bookmaker_count


        # vig adjust the odds
        vig_adjusted_odds = vig_adjust(1/home_team_average_odds, 1/away_team_average_odds)
        vig_adjusted_average_odds[home_team_no_city] = vig_adjusted_odds[0]
        vig_adjusted_average_odds[away_team_no_city] = vig_adjusted_odds[1]

    return vig_adjusted_average_odds

# remove the vig (security bookmakers put on their odds to always win)
def vig_adjust(p1, p2):
    if p1 + p2 <= 1:
        return (p1, p2)
    
    total = p1 + p2
    p1 = p1 / total 
    p2 = p2 / total

    return [p1, p2]


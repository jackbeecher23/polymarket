import os
from py_clob_client.constants import POLYGON
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import MarketOrderArgs, OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY
from dotenv import load_dotenv
from datetime import datetime, timedelta, date
import requests
import re
import sportsbooks_api
import json

load_dotenv()


def main():
    host = "https://clob.polymarket.com"
    key = os.getenv("PK")
    odds_key = os.getenv("ODDS_API_KEY")
    chain_id = POLYGON

    # Create CLOB client and get/set API credentials
    client = ClobClient(host, key=key, chain_id=chain_id)
    client.set_api_creds(client.create_or_derive_api_creds())

    today = datetime.now().weekday()

    weekly_team_polymarket_tokens = get_weekly_team_tokens(host, "")
    with open("weekly_team_tokens", "w") as file:
        json.dump(weekly_team_polymarket_tokens, file)
    


    nba_team_sportsbook_odds = sportsbooks_api.create_average_odds_dict(odds_key)
    place_favorable_bets(client, weekly_team_polymarket_tokens, nba_team_sportsbook_odds, 100)


# get polymarket tokens of teams playing this week
def get_weekly_team_tokens(host, next_cursor = ""):
    nba_team_token_id = {}

    # while next page exists
    while next_cursor != "LTE=":
        # query polymarket
        market_endpoint = f"{host}/markets?next_cursor={next_cursor}&active=true"
        response = requests.get(market_endpoint)
        markets = response.json()
        next_cursor = markets["next_cursor"]

        # for each market in the markets
        for market in markets["data"]:
            # get the descriptor (slug)
            market_slug = market["market_slug"]

            # pattern match to nba games
            pattern = r"nba\-\w+\-\w+\-\d+\-\d+\-\d+"
            if re.match(pattern, market_slug): 

                date_list = market_slug.split("-")[-3:] #extracts date of nba game into 2024-12-3 format
                event_date = "-".join(date_list)
                date = r"\b\d{4}-\d{2}-\d{2}\b"

                # check we extracted data
                if not re.match(date, event_date):
                    continue

                # check if game is today
                if is_today_event(event_date):

                    # add the teams' tokens to our dictionary
                    team1_name = market["tokens"][0]["outcome"]
                    team1_token_id = market["tokens"][0]["token_id"]

                    team2_name = market["tokens"][1]["outcome"]
                    team2_token_id = market["tokens"][1]["token_id"]

                    nba_team_token_id[team1_name] = team1_token_id
                    nba_team_token_id[team2_name] = team2_token_id;

    return nba_team_token_id

# check if event is in future 
def is_today_event(start_date):
    event_date = date.fromisoformat(start_date) 
    current_date = date.today()
    return event_date == current_date 


# place the bet through polymarket
def place_favorable_bet(client, weekly_team_token, f, current_bankroll):
    order_args = MarketOrderArgs(weekly_team_token, amount = f * current_bankroll)
    signed_order = client.create_market_order(order_args)
    response = client.post_order(signed_order, orderType=OrderType.FOK)


# for each bet, if it's favorable, place it
def place_favorable_bets(client, weekly_team_tokens, all_sportsbook_odds, current_bankroll):
    
    # for each bet
    for key, value in weekly_team_tokens.items():
        # get the team name
        tokens = key.split(" ")
        team_name = tokens[-1] 

        # find the team's odds on sportsbooks and polymarket
        team_sportsbook_odds = all_sportsbook_odds[team_name]
        polymarket_price = float(client.get_price(token_id = value, side = "SELL")["price"])

        # if polymarket price better than sportsbook odds
        if is_favorable_bet(polymarket_price, team_sportsbook_odds):
            f = calculate_kelly(polymarket_price, team_sportsbook_odds)
            print(f"FAVORABLE BET: team name: {team_name}, sportsbooks odds: {team_sportsbook_odds:.3f}, polymarket price: {polymarket_price}")
            print(f"KELLY CRITERION BET AMOUNT: Bet {f * 100:.3f}% of your bankroll")
            #place_favorable_bet(client, value, f, current_bankroll)
            current_bankroll -= current_bankroll * f


# if polymarket price better than sportsbook odds
def is_favorable_bet(polymarket_price, team_sportsbook_odds):
    if (polymarket_price + .01 < team_sportsbook_odds):
        return True
    return False

# calculate kelly criterion
def calculate_kelly(polymarket_odds, sportsbook_odds):
    if (polymarket_odds > sportsbook_odds):
        return 0

    #in the form x:1 odds, so multiplier - 1
    polymarket_return_odds = (1/polymarket_odds) - 1

    kelly = ((polymarket_return_odds * sportsbook_odds) - (1 - sportsbook_odds))/polymarket_return_odds
    return kelly



if __name__ == "__main__":
    print("Running main.py")
    main() 

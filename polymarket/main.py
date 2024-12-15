import os
from py_clob_client.constants import POLYGON
from py_clob_client.client import ClobClient
from py_clob_client.clob_types import OrderArgs, OrderType
from py_clob_client.order_builder.constants import BUY
import polymarket_api
from dotenv import load_dotenv
from datetime import datetime
import requests
import re
import sportsbooks_api
import json

load_dotenv()


def main():
    current_bankroll = 100

    host = "https://clob.polymarket.com"
    key = os.getenv("PK")
    chain_id = POLYGON

    # Create CLOB client and get/set API credentials
    client = ClobClient(host, key=key, chain_id=chain_id)
    client.set_api_creds(client.create_or_derive_api_creds())

    today = datetime.now().weekday()
    if today == 1: #tuesday
        weekly_team_polymarket_tokens = get_weekly_team_tokens(host, "")
        with open("weekly_team_tokens", "w") as file:
            json.dump(weekly_team_polymarket_tokens, file)
    
    with open("weekly_team_tokens", "r") as file:
        weekly_team_polymarket_tokens = json.load(file)


    nfl_team_sportsbook_odds = sportsbooks_api.create_average_odds_dict()

    place_favorable_bets(client, weekly_team_polymarket_tokens, nfl_team_sportsbook_odds, current_bankroll)


#returns (team, token_id) is very inefficient
def get_weekly_team_tokens(host, next_cursor = ""):
    nfl_team_token_id = {}
    while next_cursor != "LTE=":
        market_endpoint = f"{host}/markets?next_cursor={next_cursor}&active=true"
        response = requests.get(market_endpoint)
        markets = response.json()
        next_cursor = markets["next_cursor"]
        for market in markets["data"]:
            market_slug = market["market_slug"]
            pattern = r"nfl\-\w+\-\w+\-\d+\-\d+\-\d+"
            if re.match(pattern, market_slug): 
                date_list = market_slug.split("-")[-3:] #extracts date of NFL game into 2024-12-3 format
                event_date = "-".join(date_list)
                if is_future_event(event_date):
                    team1_name = market["tokens"][0]["outcome"]
                    team1_token_id = market["tokens"][0]["token_id"]

                    team2_name = market["tokens"][1]["outcome"]
                    team2_token_id = market["tokens"][1]["token_id"]

                    nfl_team_token_id[team1_name] = team1_token_id
                    nfl_team_token_id[team2_name] = team2_token_id

    return nfl_team_token_id

# start date in form 2024-12-15 
def is_future_event(start_date):
    parsed_time = datetime.strptime(start_date, "%Y-%m-%d") 
    current_time = datetime.utcnow()
    return parsed_time > current_time


def place_favorable_bet(client, weekly_team_token, f, current_bankroll):
    print(weekly_team_token, f)
    #order_args = MarketOrderArgs(weekly_team_token, amount = f * current_bankroll)
    #signed_order = client.create_market_order(order_args)
    #response = client.post_order(signed_order, orderType=OrderType.fok)
    #print(resp)


def place_favorable_bets(client, weekly_team_tokens, all_sportsbook_odds, current_bankroll):
    for key, value in weekly_team_tokens.items():
        tokens = key.split(" ")
        team_name = tokens[-1] #no city team name
        team_sportsbook_odds = all_sportsbook_odds[team_name]

        polymarket_price = float(client.get_price(token_id = value, side = "SELL")["price"])

        if is_favorable_bet(polymarket_price, team_sportsbook_odds):
            print(f"{team_name}: Sportbook odds - {team_sportsbook_odds} polymarket price - {polymarket_price}")
            f = calculate_kelly(polymarket_price, team_sportsbook_odds)
            place_favorable_bet(client, value, f, current_bankroll)
            current_bankroll -= current_bankroll * f

def is_favorable_bet(polymarket_price, team_sportsbook_odds):
    if (polymarket_price < team_sportsbook_odds):
        return True
    
    return False

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

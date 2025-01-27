# polymarket
Automated betting system for NBA games on polymarket using the kelly criterion
and vig adjusted sports market odds.

Simply, find favorable NBA bets on polymarket and place a optimal bet on them.

## Description

My idea is this:

All NBA games have extensive odds from a multitude of bookmakers. If we compile those odds into an
average, we should get a rough idea of what the true odds of the game are. We then take those true 
odds and input them into polymarket to see if there are any favorable bets for us on that site.
We place these bets optimally using the kelly criterion.

## Getting started

#### Dependencies
Must have a The Odds API account and key as well as a polymarket account

#### Installing
1. Clone the repository
2. Fill out the .env with your information

#### Modifying the code
This code was all written for NFL regular season games. Since that is over,
I have modified it to work with NBA games to show functionality.

#### Running the code
1. activate the virtual env
'''bash
source env/bin/activate
'''
2. run the main.py
'''bash
python3 main.py
'''

## Journey
I created this trading bot for two reasons
1. I was really fascinated by decision markets such as polymarket
2. I thought it would be a fun way to learn how to use APIs effectively

#### Impact
Ideally, as all trading bots do, this would provide more liquidity to polymarket and push
the markets closer to their true odds (the goal of decision markets).

#### New Tech
Prior to this project, I had never coded anything in python with APIs. It was fun for me to explore how to use them
and what the buzzword really was.

#### Challenges
Many, many, many.

1. Polymarket is rather new and their API is not well developed, hard to fish out exact games I wanted to bet on
2. Struggled finding sportsbook odds

## No Demo
Since this project was originally created for NFL regular season games, and it is now the post season, I am unable
to create a video demo showcasing the functionality. However, I modified the code to work for NBA games and starting
Jan 27, 2025, it should be fully functional again. Must wait til then, however, for polymarket to update games from the coming week.

## Author
Jack Beecher - jackbee0221@gmail.com


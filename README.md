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

## Demo
Below you will see intructions for setting up this code for your own use. However, for simplicity, here is a demo of how it works.

## To Use

#### Dependencies
Must have a The Odds API account and key as well as a polymarket account

#### Installing
1. Clone the repository
2. Fill out the envtemplate with your information
3. save template as .env

#### Modifying the code
This code was all written for NFL regular season games. Since that is over,
I have modified it to work with NBA games to show functionality.

#### Running the code
1. create a virtual env
```bash
python3 -m venv venv
```
2. activate the virtual env
```bash
source venv/bin/activate
```
3. install the requirements
```bash
pip install -r requirements.txt
```
4. uncomment line 113 in main.py (if want to place bets on polymarket)
5. run polymarket/main.py (set this up to run daily)
```bash
python3 polymarket/main.py
```

Note: The code is currently configured to only get all future games on Tuesdays, so if you run the code for the first time on any other day, it will not be able to analyze any current games as there are none. To fix this, go to the line in main.py with the comment #tuesday, and change the number to whatever day you want.

## Journey
I created this trading bot for two reasons
1. I was fascinated by decision markets such as polymarket
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


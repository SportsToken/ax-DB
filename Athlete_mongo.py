import pymongo
from pymongo import MongoClient

'''
MongoDB Database Connection
'''

# get client
cluster = MongoClient(
    "mongodb+srv://AXMarkets:B7axmarkets&j64!@axmarkets.1hesm.mongodb.net/AXMarkets?retryWrites=true&w=majority")
# get db
db = cluster['AXMarkets']
# get collection
collection = db['AXMarkets']

'''
Constants definitons
'''

HEADER = {'Ocp-Apim-Subscription-Key': '22c8f467077d4ff2a14c5b69e2355343'}
PLAYER_URL = 'https://api.sportsdata.io/v3/mlb/stats/json/PlayerSeasonStats/{"2021"}'
LEAGUE_URL = 'https://api.sportsdata.io/v3/mlb/scores/json/TeamSeasonStats/{"2021"}'

MLB_athlete_list = []
with open('mlb_list.txt', 'r') as file:
    for line in file:
        MLB_athlete_list.append(line[:-1])
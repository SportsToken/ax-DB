from Athlete_functions import *

HEADER = {'Ocp-Apim-Subscription-Key': '22c8f467077d4ff2a14c5b69e2355343'}
PLAYER_URL = 'https://api.sportsdata.io/v3/mlb/stats/json/PlayerSeasonStats/%7B%222021%22%7D'
LEAGUE_URL = 'https://api.sportsdata.io/v3/mlb/scores/json/TeamSeasonStats/%7B%222021%22%7D'

MLB_athlete_list = []
with open('mlb_list.txt', 'r') as file:
    for line in file:
        MLB_athlete_list.append(line[:-1])

def Create_athlete(db, athlete_data): # create a new athlete in db
    
    db.child('MLB').child(athlete_data["PlayerID"]).set({
        "_name": athlete_data['Name'],
        "_hist": []
        })

def Update_historical_WAR(db, _id, name, time, WAR): # add historical time/price pair to each athlete data
    
    db.child('MLB').child(_id).child("_hist").update({
        time:float(WAR)
    })

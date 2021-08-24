import requests
from requests import api
from Player_class import *
from Athlete_mongo import *

def Create_athlete(name): # create a new athlete in db

    response = requests.get(PLAYER_URL, headers=HEADER)  # pull sports data from api

    if response.status_code != 200:  # proper response from api connection
        print('Error')

    for athlete in response.json():  # parse each athlete
        if athlete['Name'] == name:  # if athlete name in list of tracked MLB_athletes

            collection.insert_one(
                {"_id": athlete['PlayerID']}, 
                {"_name": athlete['Name']}, 
                {"_hist": []}
            )

def Update_historical_WAR(_id, time, WAR): # add historical time/price pair to each athlete data

    collection.update_one(
        {"_id":_id},
        {"$push": 
            {"_hist": {time:WAR} }
        }
    )

    
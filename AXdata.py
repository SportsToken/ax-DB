import requests
from requests import api
from Athlete_functions import *
from Athlete_mongo import *
from datetime import date

def Create_athlete(athlete_data): # create a new athlete in db
    print(athlete_data)
    collection.insert_one({
        "_id": athlete_data['PlayerID'], 
        "_name": athlete_data['Name'], 
        "_hist": []
        })

def Update_historical_WAR(name, time, WAR): # add historical time/price pair to each athlete data
    
    collection.update_one(
        {"name":name},
        {"$push": 
            {"_hist": {time:WAR} }
        }
    )



import requests
from requests import api
from Athlete_functions import *
from Athlete_mongo import *
from datetime import date

def Create_athlete(db, athlete_data): # create a new athlete in db
    
    db.child('MLB').child(athlete_data["PlayerID"]).set({
        "_name": athlete_data['Name'],
        "_hist": []
        })

def Update_historical_WAR(db, _id, name, time, WAR): # add historical time/price pair to each athlete data
    
    db.child('MLB').child(_id).child("_hist").update({
        time:float(WAR)
    })



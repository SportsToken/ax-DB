from Athlete_mongo import *
from AXdata import *
from Athlete_functions import *
import datetime
from index import *

DATA = Pull_new_data()
time = datetime.datetime.now().strftime("%m-%d-%Y, %H:%M:%S")
db = firebase.database()

for athlete in MLB_athlete_list:

    athlete_data = Get_athlete_data(DATA, athlete)
    _id = athlete_data['PlayerID']
    _name = athlete_data['Name']

    WAR = Get_WAR(athlete_data)
    
    Update_historical_WAR(db, _id, _name, time, WAR)
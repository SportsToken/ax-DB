from Athlete_mongo import *
from AXdata import *
from Athlete_functions import *
import datetime

DATA = Pull_new_data()
time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

for athlete in MLB_athlete_list:

    athlete_data = Get_athlete_data(DATA, athlete)
    _id = athlete_data['PlayerID']

    WAR = Get_WAR(athlete_data)
    
    Update_historical_WAR(_id, time, WAR)

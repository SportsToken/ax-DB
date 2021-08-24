from Athlete_mongo import *
from AXdata import *
from Athlete_functions import *

DATA = Pull_new_data()

for athlete in MLB_athlete_list:

    athlete_data = Get_athlete_data(DATA, athlete)
    Create_athlete(athlete_data)
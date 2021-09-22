import socket
import requests
import json

'''
Template for pushing APT data to QuestDB

HEADER - Subscription key to Sportsdata.io
PLAYER_URL - API endpoint through Sportsdata.io to access PlayerSeasonStats for a given season
SEASON - Year of the NFL season from which to pull data
HOST - host link to connect to QuestDB
PORT - port access number for QuestDB

(function) Get_NFL_Data - Function to get all NFL data for all NFL athletes
(function) Get_athlete_data - Function to get ONLY the data for a given NFL athlete
(function) Get_NFL_price - Function to calculate the WAR value for a given NFL athlete
(function) Get_NFL_list - Function to extract all needed athletes from appropriate txt file
'''

HEADER = {'Ocp-Apim-Subscription-Key': 'ee86ff4dcb8a4a54a4a6e280733eb5b7'}
PLAYER_URL = 'https://api.sportsdata.io/v3/nfl/stats/json/PlayerSeasonStats/2020'
HOST = '146.59.10.118'
PORT = 9009

def Get_NFL_data(): # pull new data from SportsData.io
    response = requests.get(PLAYER_URL, headers=HEADER)
    DATA = response.json()
    return DATA

def Get_athlete_data(DATA, _name): # extract data by athlete name passed
    for athlete_data in DATA:
        if athlete_data['Name'] == _name:
            return athlete_data

def Get_NFL_price(athlete_data): # get WAR price for given athlete data
    TFP = athlete_data['FantasyPoints'] / ((athlete_data['OffensiveSnapsPlayed']) or athlete_data['DefensiveSnapsPlayed'])
    return TFP

def Get_NFL_list(): # get usable list of NFL athletes
    NFL_ATHLETES = []
    with open('nfl_list.txt', 'r') as file:
        for line in file:
            NFL_ATHLETES.append(line[:-1])
    return NFL_ATHLETES

NFL_ATHLETES = Get_NFL_list() # pull active nfl athlete names and store in list
NFL_DATA = Get_NFL_data() # Get all NFL athletes data

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # define socket

sock.connect((HOST, PORT)) # connect to socket

for athlete in NFL_ATHLETES: # loop through list of available athletes 
    try: # try/except case needed to bypass athletes that dont exist in current seasons
        athlete_data = Get_athlete_data(NFL_DATA, athlete)
        _id = athlete_data['PlayerID']
        name = athlete_data['Name']
        name = name.replace(' ', '_')
        name = name + ('_' + str(_id))
        WAR = Get_NFL_price(athlete_data)
        
        # Send WAR Stats
        string = f'nfl,name={name} value={WAR}\n'

        try: # find potential errors
            sock.sendall((string).encode())
        except socket.error as e:
            print("Got error: %s" % (e))

    except: # print names of athletes not available
        print(athlete)

sock.close() # close socket
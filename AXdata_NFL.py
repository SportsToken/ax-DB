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

HEADER = {'Ocp-Apim-Subscription-Key': 'd50772ff30a14c91b08b1f7b7f59de5d'}
PLAYER_URL = 'https://api.sportsdata.io/v3/nfl/stats/json/PlayerSeasonStats/2020'
IS_PLAYING_URL = 'https://api.sportsdata.io/v3/nfl/scores/json/AreAnyGamesInProgress'
HOST = '146.59.10.118'
PORT = 9009

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # define socket
sock.connect((HOST, PORT)) # connect to socket

def main():
    response = requests.get(IS_PLAYING_URL, headers=HEADER)
    if response.json() == False:
        all_athlete_data = requests.get(PLAYER_URL, headers=HEADER).json()
        for athlete in all_athlete_data:
            id, name, fp = athlete['PlayerID'], athlete['Name'].replace(' ', '_'), (athlete['FantasyPoints'] / ((athlete['OffensiveSnapsPlayed']) or athlete['DefensiveSnapsPlayed'] or 1))

            string = f'nfl,name={name} war={fp}\n'
            try: # find potential errors
                sock.sendall((string).encode())
            except socket.error as e:
                print("Got error: %s" % (e))

sock.close() # close socket

main()
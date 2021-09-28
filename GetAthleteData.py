import socket
import requests
import json

# Constants
HEADER = {'Ocp-Apim-Subscription-Key': 'd50772ff30a14c91b08b1f7b7f59de5d'}
SDIO_URL = 'https://api.sportsdata.io/v3/nfl/stats/json/PlayerSeasonStats/2020'
HOST = '146.59.10.118'
PORT = 9009

def getData():
    response = requests.get(SDIO_URL, headers=HEADER)
    theData = response.json()
    return theData

def priceCalculation(athlete_data):
        # Football Athletes
        computedAmericanFootballPrice = athlete_data['FantasyPoints'] / ((athlete_data['OffensiveSnapsPlayed']) or athlete_data['DefensiveSnapsPlayed'])
        return computedAmericanFootballPrice

def run():
    # Define the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # define socket
    sock.connect((HOST, PORT)) # connect to socket
    # Loop the entire json
    ListOfAthletes = getData()

    for athlete in ListOfAthletes:
        try: # find potential errors
            athleteString = f'nfl,name={athlete["Name"]},playerID={athlete["PlayerID"]} price={priceCalculation(athlete)}'
            try:
                sock.sendall((athleteString).encode())
            except socket.error as e:
                print("Got error: %s" % (e))
        except: # print names of athletes not available
            print(athleteString)
    sock.close() # close socket
# exec
run()
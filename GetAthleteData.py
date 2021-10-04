import socket
import requests
import json

# Constants
apiKey = ""
HEADER = {'Ocp-Apim-Subscription-Key': apiKey }
SDIO_URL = 'https://api.sportsdata.io/v3/nfl/stats/json/PlayerSeasonStats/2020'
HOST = 'localhost'
PORT = 9009

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # define socket

def getTheData():
        httpResponse = requests.get(SDIO_URL, headers=HEADER)
        theData = httpResponse.json()
        return theData

def computePrice(athlete_data):
        # Football Athletes
        numerator = athlete_data['FantasyPoints']
        denominator = athlete_data['OffensiveSnapsPlayed'] or athlete_data['DefensiveSnapsPlayed']
        if denominator == 0.0:
                denominator = 1.0        
        else:
                pass

        computedAmericanFootballPrice = numerator / denominator
        return computedAmericanFootballPrice

def run():
        # Define the socket
        # sock.connect((HOST, PORT)) # connect to socket
        fd, addr = sock.accept()
        # Loop the entire json
        ListOfAthletes = getTheData()
        print(addr)
        for athlete in ListOfAthletes:
                footballAthlete = "nfl,name=" + str(athlete["Name"]) + ",playerID=" + str(athlete["PlayerID"]) + " price=" + str(computePrice(athlete)) + "\n"
                fd.sendall((footballAthlete).encode())
        
        fd.close() # close socket

run()
import socket
import requests
import json

# Constants
HEADER = {'Ocp-Apim-Subscription-Key': '**PRIVATE-KEY**'}
SDIO_URL = 'https://api.sportsdata.io/v3/nfl/stats/json/PlayerSeasonStats/2020'
HOST = '146.59.10.118'
PORT = '9009'

def getData():
    response = requests.get(SDIO_URL, headers=HEADER)
    print(response)
    theData = response.json()
    print(theData)
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
    try: # find potential errors
        str = 'words brah'
        sock.sendall((str).encode())
    except socket.error as e:
        print("Got error: %s" % (e))

    except: # print names of athletes not available
        print(str)
    sock.close() # close socket
# exec
    getData()
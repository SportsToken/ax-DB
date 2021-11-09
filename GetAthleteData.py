import socket
import requests
import json

# Constants
apiKey = ""
HEADER = {'Ocp-Apim-Subscription-Key': apiKey }
SDIO_URL = 'https://api.sportsdata.io/v3/nfl/stats/json/PlayerSeasonStats/2021'

HOST = ''
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
        if (computedAmericanFootballPrice < 0):
                computedAmericanFootballPrice = 0
        
        return computedAmericanFootballPrice

# For UDP, change socket.SOCK_STREAM to socket.SOCK_DGRAM
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  sock.connect((HOST, PORT))
  ListOfAthletes = getTheData()
  for athlete in ListOfAthletes:
        price = computePrice(athlete)
        id = athlete['Id']
        name = athlete['Name']
        team = athlete['Team']
        playerID = athlete['PlayerID']
        position = athlete['Position']
        passingYards = athlete['PassingYards']
        passingTouch = athlete['PassingTouchdowns']
        reception = athlete['Receptions']
        receiveYards = athlete['ReceivingYards']
        receiveTouch = athlete['ReceivingTouchdowns']
        rushingYards = athlete['RushingYards']
        # rushingTouch = athlete['RushingTouch']

        sock.sendall((f'nfl,name={name},id={id},team={team},position={position},passingYards={passingYards},passingTouchdowns={passingTouch},reception={reception},receiveYards={receiveYards},receiveTouch={receiveTouch},rushingYards={rushingYards} price={price}\n').encode())
except socket.error as e:
  print("Got error: %s" % (e))

sock.close()

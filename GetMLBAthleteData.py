import os
import socket
import requests
import json

from dotenv import load_dotenv   
load_dotenv()                    

# Constants
apiKey = os.environ.get("MLB_API_KEY")
HEADER = {'Ocp-Apim-Subscription-Key': apiKey }
SDIO_URL = 'https://api.sportsdata.io/v3/mlb/stats/json/PlayerSeasonStats/2021'

HOST = '139.99.74.201'
PORT = 9009

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # define socket

def getTheData():
        httpResponse = requests.get(SDIO_URL, headers=HEADER)
        theData = httpResponse.json()
        return theData

def computePrice(athlete_data):
        # Baseball Athletes
        # numerator = athlete_data['FantasyPoints']
        # denominator = athlete_data['OffensiveSnapsPlayed'] or athlete_data['DefensiveSnapsPlayed']
        # if denominator == 0.0:
        #         denominator = 1.0        
        # else:
        #         pass

        # computedMajorLeagueBaseballPrice = numerator / denominator
        # if (computedMajorLeagueBaseballPrice < 0):
        #         computedMajorLeagueBaseballPrice = 0
        
        # return computedMajorLeagueBaseballPrice
        return 0

def computeWOBP(athlete_list):
        average = athlete_list

# For UDP, change socket.SOCK_STREAM to socket.SOCK_DGRAM
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  sock.connect((HOST, PORT))
  ListOfAthletes = getTheData()
  for athlete in ListOfAthletes:
        price = computePrice(athlete)
        IgWeightedOnBasePercentage = computeWOBP(ListOfAthletes)
        id = athlete['PlayerID']
        name = athlete['Name']
        team = athlete['Team']
        position = athlete['Position']
        Started = athlete['Started']
        Games = athlete['Games']
        AtBats = athlete['AtBats']
        Runs = athlete['Runs']
        Singles = athlete['Singles']
        Doubles = athlete['Doubles']
        Triples = athlete['Triples']
        HomeRuns = athlete['HomeRuns']
        InningsPlayed = athlete['Games'] * 9.0
        BattingAverage = athlete['BattingAverage']
        Outs = athlete['Outs']
        Walks = athlete['Walks']
        Errors = athlete['Errors']
        Wins = athlete['Wins']
        Losses = athlete['Losses']
        Saves = athlete['Saves']
        Strikeouts = athlete['Strikeouts']
        WeightedOnBasePercentage = athlete['WeightedOnBasePercentage']
        PitchingHits = athlete['PitchingHits']
        PitchingRuns = athlete['PitchingRuns']
        StolenBases = athlete['StolenBases']
        PlateAppearances = athlete['PlateAppearances']
 

        sock.sendall((f'mlb,name={name},id={id},team={team},position={position} Started={Started},Games={Games},AtBats={AtBats},Runs={Runs},Singles={Singles},Doubles={Doubles},Triples={Triples},HomeRuns={HomeRuns},InningsPlayed={InningsPlayed},BattingAverage={BattingAverage},Outs={Outs},Walks={Walks},Errors={Errors},PlateAppearances={PlateAppearances},WeightedOnBasePercentage={WeightedOnBasePercentage},Saves={Saves},Strikeouts={Strikeouts},StolenBases={StolenBases},price={price}\n').encode())
except socket.error as e:
  print("Got error: %s" % (e))

sock.close()

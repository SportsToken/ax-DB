import os
import json
import socket
import requests
import unicodedata

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
        # Static Variables
        avg50yrRPW = 9.757
        collateralizationMultiplier = 1000
        BattingRuns = (((athlete_data['PlateAppearances']) * (athlete_data['WeightedOnBasePercentage'] - #lgweightedOnBase% )) / 1.25)
        BaseRunningRuns = (athlete_data['StolenBases'] * 0.2)
        FieldingRuns = ((athlete_data['Errors'] * (-10)) / (athlete_data['Games'] * 9 ))
        PositonalAdjustment = (athlete_data['Games'] * 9 ) * #PositionalAdjustment / 1458
        ReplacementRuns = (athlete_data['PlateAppearances'] * 5561.49) / #lgPlateAppearances

        statsNumerator = BattingRuns + BaseRunningRuns + FieldingRuns + PositonalAdjustment + ReplacementRuns
        WAR = statsNumerator / avg50yrRPW
        computedMajorLeagueBaseballPrice = WAR * collateralizationMultiplier
        return computedMajorLeagueBaseballPrice


def computeWOBP(athlete_list):
        average = athlete_list

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def parseName(nameString):
        newString = nameString.replace(" ", "\ ")
        newString = strip_accents(newString)
        return newString



# For UDP, change socket.SOCK_STREAM to socket.SOCK_DGRAM
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  sock.connect((HOST, PORT))
  ListOfAthletes = getTheData()
  for athlete in ListOfAthletes:
        price = computePrice(athlete)
        IgWeightedOnBasePercentage = computeWOBP(ListOfAthletes)
        name = parseName(athlete['Name'])
        id = athlete['PlayerID']
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

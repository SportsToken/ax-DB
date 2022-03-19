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

def computePrice(athlete_data, lgWeighedOnBase, lgPlateAppearances):
        # Baseball Athletes
        innings_played = athlete_data['Games'] * 9.0
        position_adj = {
                'C': 12.5,
                '1B': -12.5,
                '2B': 2.5,
                'SS': 7.5,
                '3B': 2.5,
                'LF': -7.5,
                'CF': 2.5,
                'RF': -7.5,
                'DH': -17.5
        }

        batting_runs = athlete_data['PlateAppearances'] * (athlete_data['WeightedOnBasePercentage'] - lgWeighedOnBase) / 1.25
        base_running_runs = athlete_data['StolenBases'] ** 0.2
        fielding_runs = -10 * athlete_data['Errors'] / innings_played
        run_positional_adjustment = innings_played * position_adj[athlete_data['Position']] / 1458
        replacement_runs = 5561.49 * athlete_data['PlateAppearances'] / lgPlateAppearances
        return (batting_runs + base_running_runs + fielding_runs + run_positional_adjustment + replacement_runs) / 9.757

# For UDP, change socket.SOCK_STREAM to socket.SOCK_DGRAM
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
        sock.connect((HOST, PORT))
        ListOfAthletes = getTheData()
        lgWeighedOnBase = 0
        lgPlateAppearances = 0
        for athlete in ListOfAthletes:
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
                lgWeighedOnBase += WeightedOnBasePercentage
                lgPlateAppearances += PlateAppearances

        lgWeighedOnBase /= len(ListOfAthletes)
        lgPlateAppearances /= len(ListOfAthletes)
        for athlete in ListOfAthletes:
                price = computePrice(athlete, lgWeighedOnBase, lgPlateAppearances)
          

        sock.sendall((f'mlb,name={name},id={id},team={team},position={position} Started={Started},Games={Games},AtBats={AtBats},Runs={Runs},Singles={Singles},Doubles={Doubles},Triples={Triples},HomeRuns={HomeRuns},InningsPlayed={InningsPlayed},BattingAverage={BattingAverage},Outs={Outs},Walks={Walks},Errors={Errors},PlateAppearances={PlateAppearances},WeightedOnBasePercentage={WeightedOnBasePercentage},Saves={Saves},Strikeouts={Strikeouts},StolenBases={StolenBases},price={price}\n').encode())
except socket.error as e:
        print("Got error: %s" % (e))

sock.close()

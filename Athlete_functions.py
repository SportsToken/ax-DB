import json
import requests
from datetime import date
from Athlete_mongo import *
from AXdata import *

DATA = None

def Get_league_averages(): # get league average stats
    response = requests.get(PLAYER_URL, headers=HEADER)

    LgOnBattingAverage = 0
    LgStolenBases = 0
    LgCaughtStealing = 0
    LgSingles = 0
    LgWalks = 0
    LgHitByPitch = 0
    LgIntentionalWalks = 0
    LgPlateAppearances = 0
    counter = 0

    for athlete in response.json():
        LgOnBattingAverage += athlete['BattingAverage']
        LgStolenBases += athlete['StolenBases']
        LgCaughtStealing += athlete['CaughtStealing']
        LgSingles += athlete['Singles']
        LgWalks += athlete['Walks']
        LgHitByPitch += athlete['HitByPitch']
        LgIntentionalWalks += athlete['IntentionalWalks']
        LgPlateAppearances += athlete['PlateAppearances']
        counter += 1

    LgOnBattingAverage = LgOnBattingAverage/counter
    LgStolenBases = LgStolenBases/counter
    LgCaughtStealing = LgCaughtStealing/counter
    LgSingles = LgSingles/counter
    LgWalks = LgWalks/counter
    LgHitByPitch = LgHitByPitch/counter
    LgIntentionalWalks = LgIntentionalWalks/counter
    LgPlateAppearances = LgPlateAppearances/counter

    return(LgOnBattingAverage,
          LgStolenBases,
          LgCaughtStealing,
          LgSingles,
          LgWalks,
          LgHitByPitch,
          LgIntentionalWalks,
          LgPlateAppearances)

def Get_MLB_averages(): # get MLB season stats
    response = requests.get(LEAGUE_URL, headers=HEADER)

    MLBRunsScored = 0
    MLBInningsPitched = 0
    MLBGames = 0

    for team in response.json():
        MLBRunsScored += team['Runs']
        MLBInningsPitched += team['InningsPitchedDecimal']
        MLBGames += team['Games']

    MLBGames/=2
    MLBInningsPitched/=2

    return (MLBRunsScored, MLBInningsPitched, MLBGames)

def Pull_new_data(): # pull new data from SportsData.io

    response = requests.get(PLAYER_URL, headers=HEADER)

    DATA = response.json()

    return DATA

def Get_athlete_data(DATA, _name): # extract data by athlete name passed

    for athlete in DATA:
        if athlete['Name'] == _name:
            return athlete

def Get_WAR(DATA, _name) -> int: # calculate WAR

    onBasePercentage = DATA['OnBasePercentage']
    pitchingPlateAppearances = DATA['PitchingPlateAppearances']
    stolenBases = DATA['StolenBases']
    caughtStealing = DATA['CaughtStealing']
    runs = DATA['Runs']
    outs = DATA['Outs']
    singles = DATA['Singles']
    walks = DATA['Walks']
    hitByPitch = DATA['HitByPitch']
    intentionalWalks = DATA['IntentionalWalks']
    plateAppearances = DATA['PlateAppearances']
    runsCaughtStealing = 2 * (runs / outs) + 0.075

    LgOnBattingAverage, LgStolenBases, LgCaughtStealing, LgSingles, LgWalks, LgHitByPitch, LgIntentionalWalks, LgPlateAppearances = Get_league_averages()
    MLBRunsScored, MLBInningsPitched, MLBGames = Get_MLB_averages()

    LgStolenBasesWeighted = (LgStolenBases*0.2 + LgCaughtStealing*runsCaughtStealing) / (LgSingles + LgWalks + LgHitByPitch + LgIntentionalWalks)

    baseRunningRuns = stolenBases*0.2 + caughtStealing*runsCaughtStealing - LgStolenBasesWeighted * (singles + walks + hitByPitch - intentionalWalks)

    battingRuns = ((onBasePercentage - LgOnBattingAverage)/1.254) * pitchingPlateAppearances

    RPW = 9*(MLBRunsScored/MLBInningsPitched) * 1.5 + 3
    RLR = (570*(MLBGames/2430)) * (RPW/LgPlateAppearances) * plateAppearances
    RAR = (battingRuns + baseRunningRuns)/RLR
    WAR = RAR/RPW

    return WAR

import requests
import json
header = {'Ocp-Apim-Subscription-Key': '22c8f467077d4ff2a14c5b69e2355343'}


def Get_league_averages():
    url = 'https://api.sportsdata.io/v3/mlb/stats/json/PlayerSeasonStats/{"2021"}'
    header = {'Ocp-Apim-Subscription-Key': '22c8f467077d4ff2a14c5b69e2355343'}

    response = requests.get(url, headers=header)

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

def Get_MLB_averages():
    url = 'https://api.sportsdata.io/v3/mlb/scores/json/TeamSeasonStats/{"2021"}'
    response = requests.get(url, headers=header)

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


def Get_athlete_data():

        url = 'https://api.sportsdata.io/v3/mlb/stats/json/PlayerSeasonStats/{"2021"}'
        response = requests.get(url, headers=header)

        for athlete in response.json():
            if athlete['Name'] == name:
                data = athlete

def Get_WAR():

    self.Get_athlete_data()

    onBasePercentage = self.data['OnBasePercentage']
    pitchingPlateAppearances = self.data['PitchingPlateAppearances']
    stolenBases = self.data['StolenBases']
    caughtStealing = self.data['CaughtStealing']
    runs = self.data['Runs']
    outs = self.data['Outs']
    singles = self.data['Singles']
    walks = self.data['Walks']
    hitByPitch = self.data['HitByPitch']
    intentionalWalks = self.data['IntentionalWalks']
    plateAppearances = self.data['PlateAppearances']
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

    print(WAR)
    

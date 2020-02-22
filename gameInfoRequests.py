import requests
import os

riotApiKey = os.environ['riotAPIKey']

print("riotAPIKey: {}".format(riotApiKey))

servers = {"BR": "https://br1.api.riotgames.com",
           "EUN": "https://eun1.api.riotgames.com",
           "EUW": "https://euw1.api.riotgames.com",
           "JP": "https://jp1.api.riotgames.com",
           "KR": "https://kr.api.riotgames.com",
           "LA1": "https://la1.api.riotgames.com",
           "LA2": "https://la2.api.riotgames.com",
           "NA": "https://na1.api.riotgames.com",
           "OC": "https://oc1.api.riotgames.com",
           "TR": "https://tr1.api.riotgames.com",
           "RU": "https://ru.api.riotgames.com"
           }

def getSummonerApiInfo(summonerName):
    print("[INFO] getSummonerInfo RequestToAPI!")
    requestUrl = servers["EUW"] + "/lol/summoner/v4/summoners/by-name/"
    completedRequestUrl = "{}{}?api_key={}".format(requestUrl, summonerName, riotApiKey)
    requestData = requests.get(completedRequestUrl).json()
    try:
        if requestData["status"]["status_code"] == 404:
            requestData = "NO SUMMONER FOUND"
    except:
        pass
    print("[INFO] SUMMONERDATA: {}".format(requestData))
    return requestData

def getSummonerRankApiInfo(summonerID):
    print("[INFO] getSummonerRankedInfo RequestToAPI!")
    requestUrl = servers["EUW"]+"/lol/league/v4/entries/by-summoner/"
    completedRequestUrl = "{}{}?api_key={}".format(requestUrl, summonerID, riotApiKey)
    requestData = requests.get(completedRequestUrl).json()
    print("[INFO] RANKDATA: {}".format(requestData))
    return requestData

def getMatchApiInfo(summonerID):
    print("[INFO] getMatchInfo RequestToAPI!")
    requestUrl = servers["EUW"]+"/lol/spectator/v4/active-games/by-summoner/"
    completedRequestUrl = "{}{}?api_key={}".format(requestUrl, summonerID, riotApiKey)
    requestData = requests.get(completedRequestUrl).json()
    try:
        if requestData["status"]["status_code"] == 404:
            requestData = "SUMMONER IS NOT INGAME"
    except:
        pass
    print("[INFO] MATCHDATA: {}".format(requestData))
    return requestData

def getSummonerMasteryInfo(summonerID):
    print("[INFO] getSummonerMastery RequestToAPI!")
    requestUrl = servers["EUW"] + "/lol/champion-mastery/v4/champion-masteries/by-summoner/"
    completedRequestUrl = "{}{}?api_key={}".format(requestUrl, summonerID, riotApiKey)
    requestData = requests.get(completedRequestUrl).json()
    print("[INFO] SUMMONERMASTERY: {}".format(requestData))
    return requestData

def getChampionInformation():
    completedRequestUrl = "https://ddragon.leagueoflegends.com/cdn/10.4.1/data/en_US/champion.json"
    requestData = requests.get(completedRequestUrl).json()
    return requestData

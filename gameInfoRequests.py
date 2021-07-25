import grequests

import requests
import os
from urllib.parse import quote

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

def getSummonerUrl(summonerName):
    requestUrl = servers["EUW"] + "/lol/summoner/v4/summoners/by-name/"
    completedRequestUrl = "{}{}?api_key={}".format(requestUrl, summonerName, riotApiKey)
    return completedRequestUrl

def getSummonerApiInfoArray(summonerArray):
    urls = []
    for summoner in summonerArray:
        print("[INFO API] getSummonerInfo RequestToAPI! - " + summoner)
        url = getSummonerUrl(summoner)
        print("[INFO API] REQUESTURL SUMMONER: " + url)
        urls.append(grequests.get(url))
    result = grequests.map(urls)
    for response in result:
        print("[INFO API] SUMMONERDATA: {}".format(response.json()))
    return result

def getSummonerRankUrl(summonerID):
    requestUrl = servers["EUW"]+"/lol/league/v4/entries/by-summoner/"
    completedRequestUrl = "{}{}?api_key={}".format(requestUrl, summonerID, riotApiKey)
    return completedRequestUrl

def getSummonerRankApiInfoArray(summonerIDArray):
    urls = []
    for summonerID in summonerIDArray:
        print("[INFO API] getSummonerRankedInfo RequestToAPI - {}".format(summonerID))
        url = getSummonerRankUrl(summonerID)
        print("[INFO API] REQUESTURL RANK: " + url)
        urls.append(grequests.get(url))
    result = grequests.map(urls)
    for response in result:
        print("[INFO API] RANKDATA: {}".format(response.json()))
    return result

def getMatchListUrl(id):
    requestUrl = servers["EUW"] + "/lol/match/v4/matchlists/by-account/"
    completedRequestUrl = "{}{}?api_key={}".format(requestUrl, id, riotApiKey)
    return completedRequestUrl

def getMatchListApiInfoArray(accountIdArray):
    urls = []
    for accountId in accountIdArray:
        print("[INFO API] getMatchListApiInfo RequestToAPI - {}".format(accountId))
        url = getMatchListUrl(accountId)
        print("[INFO API] REQUESTURL MatchList: " + url)
        urls.append(grequests.get(url))
    result = grequests.map(urls)
    return result

def getSummonerApiInfo(summonerName):
    print("[INFO API] getSummonerInfo RequestToAPI! - " + summonerName)
    completedRequestUrl = getSummonerUrl(summonerName)
    print("[INFO API] REQUESTURL SUMMONER: " + completedRequestUrl)
    requestData = requests.get(completedRequestUrl).json()
    try:
        if requestData["status"]["status_code"] == 404:
            print("[INFO API][getSummonerApiInfo] NO SUMMONER FOUND WITH NAME: {}".format(summonerName))
            return False
    except:
        pass
    print("[INFO API] SUMMONERDATA: {}".format(requestData))
    return requestData

def getSummonerRankApiInfo(summonerID):
    print("[INFO API] getSummonerRankedInfo RequestToAPI - " + summonerID)
    requestUrl = servers["EUW"]+"/lol/league/v4/entries/by-summoner/"
    completedRequestUrl = "{}{}?api_key={}".format(requestUrl, summonerID, riotApiKey)
    print("[INFO API] REQUESTURL RANK: " + completedRequestUrl)
    requestData = requests.get(completedRequestUrl).json()
    print("[INFO API] RANKDATA: {}".format(requestData))
    return requestData

def getMatchListApiInfo(accountId):
    print("[INFO API] getMatchListApiInfo RequestToAPI - " + accountId)
    completedRequestUrl = getMatchListUrl(accountId)
    print("[INFO API] REQUESTURL MatchList: " + completedRequestUrl)
    requestData = requests.get(completedRequestUrl).json()
    #print("[INFO API] MatchList: {}".format(requestData))
    return requestData

def getMatchApiInfo(summonerID):
    print("[INFO API] getMatchInfo RequestToAPI! - " + summonerID)
    requestUrl = servers["EUW"]+"/lol/spectator/v4/active-games/by-summoner/"
    completedRequestUrl = "{}{}?api_key={}".format(requestUrl, summonerID, riotApiKey)
    print("[INFO API] REQUESTURL MATCH: " + completedRequestUrl)
    requestData = requests.get(completedRequestUrl).json()
    try:
        if requestData["status"]["status_code"] == 404:
            return False
    except:
        pass
    return requestData

def getSummonerMasteryInfo(summonerID):
    print("[INFO API] getSummonerMastery RequestToAPI!")
    requestUrl = servers["EUW"] + "/lol/champion-mastery/v4/champion-masteries/by-summoner/"
    completedRequestUrl = "{}{}?api_key={}".format(requestUrl, summonerID, riotApiKey)
    requestData = requests.get(completedRequestUrl).json()
    #print("[INFO API] SUMMONERMASTERY: {}".format(requestData))
    return requestData

def getChampionInformation(): #Get Update here https://developer.riotgames.com/docs/lol
    completedRequestUrl = "https://ddragon.leagueoflegends.com/cdn/11.15.1/data/en_US/champion.json"
    requestData = requests.get(completedRequestUrl).json()
    return requestData

def getSummonerIconURL(server, summonerName):
    # print("http://avatar.leagueoflegends.com/" + quote("{}/{}.png".format(server, summonerName)))
    url = "http://avatar.leagueoflegends.com/" + quote("{}/{}.png".format(server, summonerName))
    print("[INFO API] AVATAR ICON REQUEST: {}".format(url))
    return url

def getSummonerIconURL_withID(ID):
    # print("http://avatar.leagueoflegends.com/" + quote("{}/{}.png".format(server, summonerName)))
    url = "https://cdn.communitydragon.org/latest/profile-icon/{}".format(ID)
    print("[INFO API] AVATAR ICON REQUEST: {}".format(url))
    return url

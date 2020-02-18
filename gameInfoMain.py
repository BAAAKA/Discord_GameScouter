import requests

infoFile = open('infoFile.txt', 'r')
textFileContent = infoFile.read().split(',')
riotApiKey = textFileContent[1]
print("riotApiKey: " + riotApiKey)


def getSummonerInfo(summonerName):
    requestUrl = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    completedRequestUrl = "{}{}?api_key={}".format(requestUrl, summonerName, riotApiKey)
    requestData = requests.get(completedRequestUrl).json()
    try:
        if requestData["status"]["status_code"] == 404:
            requestData = "NO SUMMONER FOUND"
    except:
        pass
    return requestData


def getSummonerID(summonerName):
    summonerID = (getSummonerInfo(summonerName))["id"]
    return summonerID


def getMatchInfo(summonerName):
    summonerID = (getSummonerInfo(summonerName))["id"]
    requestUrl = "https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/"
    completedRequestUrl = "{}{}?api_key={}".format(requestUrl, summonerID, riotApiKey)
    requestData = requests.get(completedRequestUrl).json()
    try:
        if requestData["status"]["status_code"] == 404:
            requestData = "SUMMONER IS NOT INGAME"
    except:
        pass
    return requestData

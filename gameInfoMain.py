import requests

infoFile = open('infoFile.txt', 'r')
textFileContent = infoFile.read().split(',')
riotApiKey = textFileContent[1]
print("riotApiKey: " + riotApiKey)

riotApiServerEUW = "https://euw1.api.riotgames.com/"


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

def getSummonerRankedInfo(summonerName):
    requestUrl = servers["EUW"]+"/lol/league/v4/entries/by-summoner/"
    summonerID=getSummonerID(summonerName)
    completedRequestUrl = "{}{}?api_key={}".format(requestUrl, summonerID, riotApiKey)
    requestData = requests.get(completedRequestUrl).json()
    return requestData

def getSummonerQueuerank(summonerName, queueType): #QueueTypes: RANKED_FLEX_SR, RANKED_SOLO_5x5
    queueTypeInfo = getSummonerRankedInfo(summonerName)

    RANKED_TIER = None
    RANKED_RANK = None
    if not queueTypeInfo:
        print("SUMMONER HAS NO RANK!")
        return "SUMMONER HAS NO RANK"
    for qType in queueTypeInfo:
        print(qType)
        if qType["queueType"] == queueType:
            RANKED_TIER = qType["tier"]
            RANKED_RANK = qType["rank"]
    if RANKED_TIER is None:
        print("SUMMONER HAS NO RANK IN THIS QUEUE TYPE")
        return "SUMMONER HAS NO RANK IN THIS QUEUE TYPE"

    return RANKED_TIER +" "+RANKED_RANK



import re
import discord
from urllib.parse import quote

summonerInfo = None
queueTypeInfo = None
matchInfo = None

from gameInfoRequests import *

def getSummonerInfo(message):
    print("NEW SUMMONER INFO REQUEST")
    summonerName = message.content.split("su:", 1)[1]
    summonerInfo = getSummonerApiInfo(summonerName)
    embedMessage = discord.Embed(title = summonerName,color=0x0099ff)
    if getSummonerExistance(summonerInfo):
        embedMessage.description = "Level: {}".format(summonerInfo["summonerLevel"])
        print("http://avatar.leagueoflegends.com/"+quote("{}/{}.png".format("euw", summonerInfo["name"])))
        embedMessage.set_thumbnail(url="http://avatar.leagueoflegends.com/"+quote("{}/{}.png".format("euw", summonerInfo["name"])))
        queueTypeInfo = getSummonerRankApiInfo(summonerInfo["id"])
        if queueTypeInfo:
            soloQTier = getSummonerRankInfoDetails(queueTypeInfo, "RANKED_SOLO_5x5", "tier")
            soloQRank = getSummonerRankInfoDetails(queueTypeInfo, "RANKED_SOLO_5x5", "rank")
            flexQTier = getSummonerRankInfoDetails(queueTypeInfo, "RANKED_FLEX_SR", "tier")
            flexQRank = getSummonerRankInfoDetails(queueTypeInfo, "RANKED_FLEX_SR", "rank")
            if not re.search("SUMMONER HAS NO RANK*", soloQRank):
                embedMessage.add_field(name="SoloQ Rank ", value=soloQTier + " " + soloQRank  + " - " + str(getSummonerRankInfoDetails(queueTypeInfo, "RANKED_SOLO_5x5", "leaguePoints")) + " LP", inline=False)
                embedMessage.add_field(name="wins ", value=getSummonerRankInfoDetails(queueTypeInfo, "RANKED_SOLO_5x5", "wins"), inline=True)
                embedMessage.add_field(name="losses ", value=getSummonerRankInfoDetails(queueTypeInfo, "RANKED_SOLO_5x5", "losses"), inline=True)
                embedMessage.add_field(name="winrate ", value=str(round(getSummonerRankInfoDetails(queueTypeInfo, "RANKED_SOLO_5x5", "wins")/(getSummonerRankInfoDetails(queueTypeInfo, "RANKED_SOLO_5x5", "losses")+getSummonerRankInfoDetails(queueTypeInfo, "RANKED_SOLO_5x5", "wins"))*100, 2))+"%", inline=True)


            if not re.search("SUMMONER HAS NO RANK*", flexQRank):
                embedMessage.add_field(name="FlexQ Rank ", value=flexQTier + " " + flexQRank + " - " + str(getSummonerRankInfoDetails(queueTypeInfo, "RANKED_FLEX_SR", "leaguePoints")) + " LP", inline=False)
                embedMessage.add_field(name="wins ", value=getSummonerRankInfoDetails(queueTypeInfo, "RANKED_FLEX_SR", "wins"), inline=True)
                embedMessage.add_field(name="losses ", value=getSummonerRankInfoDetails(queueTypeInfo, "RANKED_FLEX_SR", "losses"), inline=True)
                embedMessage.add_field(name="winrate ", value=str(round(getSummonerRankInfoDetails(queueTypeInfo, "RANKED_FLEX_SR", "wins")/(getSummonerRankInfoDetails(queueTypeInfo, "RANKED_FLEX_SR", "losses")+getSummonerRankInfoDetails(queueTypeInfo, "RANKED_FLEX_SR", "wins"))*100, 2))+"%", inline=True)

    else:
        embedMessage.description = "Summoner does not exist"
    return embedMessage

def getMatchInfo(message):
    print("NEW MATCH INFO REQUEST")
    summonerName = message.content.split("ig:", 1)[1]
    summonerInfo = getSummonerApiInfo(summonerName)
    if getSummonerExistance(summonerInfo):
        matchInfo = getMatchApiInfo(summonerInfo["id"])
        if matchInfo == "SUMMONER IS NOT INGAME":  # TEST IF SUMMONER IS INGAME
            returnText = "This summoner is not ingame right now..."
        else:
            print(matchInfo)
            returnText = getMatchReturnText(matchInfo)
    else:
        returnText = "Summoner does not exist!"
    return returnText



##############

def getSummonerExistance(summonerInfo):
    if summonerInfo == "NO SUMMONER FOUND":
        return False
    else:
        return True

def getSummonerRankInfoDetails(queueTypeInfo, queueType, whatInfo):
    for qType in queueTypeInfo: #TEST IF SUMMONER HAS THIS QUEUETYPE RANK
        if qType["queueType"] == queueType:
            rankInfo = qType[whatInfo]
            return rankInfo
    print("SUMMONER HAS NO RANK IN THIS QUEUE TYPE")
    return "SUMMONER HAS NO RANK IN THIS QUEUE TYPE"


def getMatchReturnText(matchInfo):
    summonerList = []

    for nr in range(10):
        summonerList.append(matchInfo["participants"][nr - 1])

    returnText = "```"
    returnText += "MODE: {} \n".format(matchInfo["gameMode"])
    returnText += "ID: {} \n".format(matchInfo["gameId"])
    returnText += "gameType: {} \n".format(matchInfo["gameType"])
    returnText += "\n"
    returnText += "# TEAM 1 \n"
    for summoner in summonerList:
        if summoner["teamId"] == 100:
            returnText += "Summonername: {} - Champion: {} - SP: {} and {}\n".format(
                summoner["summonerName"], summoner["championId"],
                summoner["spell1Id"], summoner["spell2Id"])

    returnText += "# TEAM 2 \n"
    for summoner in summonerList:
        if summoner["teamId"] == 200:
            returnText += "Summonername: {} - Champion: {} - SP: {} and {}\n".format(
                summoner["summonerName"], summoner["championId"],
                summoner["spell1Id"], summoner["spell2Id"])


    returnText += "```"

    return returnText



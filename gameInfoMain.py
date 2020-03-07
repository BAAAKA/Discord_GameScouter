import operator
import re
import discord
from urllib.parse import quote
from gameInfoRequests import *
from createMatchupImage import getMatchImage
from matchData import getNameById
import time


def getSummonerInfo(message):
    print("========================NEW SUMMONER INFO REQUEST========================")
    start_time = time.time()
    summonerName = message.content.split("su:", 1)[1]
    summonerInfo = getSummonerApiInfo(summonerName)
    embedMessage = discord.Embed(title=summonerName, color=0x0099ff)

    if getSummonerExistance(summonerInfo):
        embedMessage.description = "Level {}".format(summonerInfo["summonerLevel"])
        embedMessage.set_thumbnail(url=getSummonerIconURL("euw", summonerInfo["name"]))
        queueTypeInfo = getSummonerRankApiInfo(summonerInfo["id"])
        if queueTypeInfo:
            soloQRank = getSummonerRankInfoDetails(queueTypeInfo, "RANKED_SOLO_5x5", "rank")
            flexQRank = getSummonerRankInfoDetails(queueTypeInfo, "RANKED_FLEX_SR", "rank")
            if not re.search("SUMMONER HAS NO RANK*", soloQRank):
                embedMessage.add_field(name=":beginner: SoloQ Rank ",
                                       value=getRankAndLP(queueTypeInfo, "RANKED_SOLO_5x5"), inline=False)
                embedMessage.add_field(name="wins ",
                                       value=getSummonerRankInfoDetails(queueTypeInfo, "RANKED_SOLO_5x5", "wins"),
                                       inline=True)
                embedMessage.add_field(name="losses ",
                                       value=getSummonerRankInfoDetails(queueTypeInfo, "RANKED_SOLO_5x5", "losses"),
                                       inline=True)
                embedMessage.add_field(name="winrate ", value=getWinrate(queueTypeInfo, "RANKED_SOLO_5x5") + "%",
                                       inline=True)
            if not re.search("SUMMONER HAS NO RANK*", flexQRank):
                embedMessage.add_field(name=":beginner: FlexQ Rank ",
                                       value=getRankAndLP(queueTypeInfo, "RANKED_FLEX_SR"), inline=False)
                embedMessage.add_field(name="wins ",
                                       value=getSummonerRankInfoDetails(queueTypeInfo, "RANKED_FLEX_SR", "wins"),
                                       inline=True)
                embedMessage.add_field(name="losses ",
                                       value=getSummonerRankInfoDetails(queueTypeInfo, "RANKED_FLEX_SR", "losses"),
                                       inline=True)
                embedMessage.add_field(name="winrate ", value=getWinrate(queueTypeInfo, "RANKED_FLEX_SR") + "%",
                                       inline=True)

        masteryInfo = getSummonerMasteryInfo(summonerInfo["id"])

        # MASTERINFODETAILS
        MID1 = getSummonerMasteryInfoDetails(masteryInfo, 1)
        MID2 = getSummonerMasteryInfoDetails(masteryInfo, 2)
        MID3 = getSummonerMasteryInfoDetails(masteryInfo, 3)

        embedMessage.add_field(name="Masteries", value=getMasteryChampion(MID1, MID2, MID3), inline=True)
        embedMessage.add_field(name="_", value=getMasteryLevel(MID1, MID2, MID3), inline=True)
        embedMessage.add_field(name="_", value=getMasteryPoints(MID1, MID2, MID3), inline=True)

        mostPlayedChamp = getChampionByID(getChampionInformation(),
                                          getSummonerMasteryInfoDetails(masteryInfo, 1)["championId"])
        embedMessage.set_image(url=getSplashURL(mostPlayedChamp))


    else:
        embedMessage.description = "Summoner does not exist"

    embedMessage.set_footer(text=getFooterText("text"), icon_url=getFooterText("url"))
    print("[INFO] ----------------- %s seconds for the getSummonerInfo request -----------------" % (time.time() - start_time))
    return embedMessage


def getMatchInfo(message):
    print("========================NEW MATCH INFO REQUEST========================")
    start_time = time.time()
    summonerName = message.content.split("ig:", 1)[1]
    summonerInfo = getSummonerApiInfo(summonerName)

    if getSummonerExistance(summonerInfo):
        matchInfo = getMatchApiInfo(summonerInfo["id"])
        if matchInfo == "SUMMONER IS NOT INGAME":  # TEST IF SUMMONER IS INGAME
            returnText = "This summoner is not ingame right now..."
        else:
            # here you know that the summoner exists and is ingame
            lanes = []
            championInfo = getChampionInformation()
            for summoner in matchInfo["participants"]:
                # Champion
                summoner["champion"] = getChampionByID(championInfo, summoner["championId"])
                # rank
                queueTypeInfo = getSummonerRankApiInfo(summoner["summonerId"])
                Tier = getSummonerRankInfoDetails(queueTypeInfo, "RANKED_SOLO_5x5", "tier")
                if re.search("SUMMONER HAS NO RANK*", Tier):
                    summonerRank = "Unranked"
                    summoner["tier"] = summonerRank
                    summoner["RankTier"] = summonerRank
                    summoner["wins"] = "0"
                    summoner["losses"] = "0"
                    summoner["winRate"] = "0"

                else:
                    Rank = getSummonerRankInfoDetails(queueTypeInfo, "RANKED_SOLO_5x5", "rank")
                    summonerRank = Tier + " " + Rank
                    summoner["tier"] = Tier
                    summoner["RankTier"] = summonerRank
                    summoner["wins"] = getSummonerRankInfoDetails(queueTypeInfo, "RANKED_SOLO_5x5", "wins")
                    summoner["losses"] = getSummonerRankInfoDetails(queueTypeInfo, "RANKED_SOLO_5x5", "losses")
                    summoner["winRate"] = getWinrate(queueTypeInfo, "RANKED_SOLO_5x5")


                # MatchList
                summonerInfo = getSummonerApiInfo(summoner["summonerName"])
                matchListInfo = getMatchListApiInfo(summonerInfo["accountId"])
                # Lanes
                laneCount = getLanePlayCount(matchListInfo)
                mostPlayedLane = []
                for i in range(len(laneCount)):
                    mostPlayedLane.append(list(max(laneCount.items(), key=operator.itemgetter(1))))
                    del laneCount[mostPlayedLane[i][0]]
                summoner["mostPlayedLanes"] = mostPlayedLane

                # Champions
                championCount = getChampionPlayCount(matchListInfo)
                mostPlayedChamp = []
                for i in range(3):
                    mostPlayedChamp.append(list(max(championCount.items(), key=operator.itemgetter(1))))
                    championName = getChampionByID(championInfo, mostPlayedChamp[i][0])
                    mostPlayedChamp[i].append(championName)
                    del championCount[mostPlayedChamp[i][0]]
                summoner["mostPlayedChamps"] = mostPlayedChamp

                # Lane in this match
                if not lanes:
                    lanes = ["Top", "Jungle", "Mid", "ADC", "Support"]
                lane = getLane(summoner["spell1Id"], summoner["spell2Id"], lanes)
                lanes.remove(lane)
                summoner["lane"] = lane
                print("Summoner {}, LANE: {}".format(summoner["summonerName"], summoner["lane"]))

            print("[INFO] ----------------- %s seconds for the getMatchInfo data -----------------" % (time.time() - start_time))
            start_timeImage = time.time()
            filePath = getMatchImage(matchInfo)
            print("[INFO] ----------------- %s seconds for the creation of the image -----------------" % (time.time() - start_timeImage))
            print("[INFO] ----------------- %s seconds for total match request -----------------" % (time.time() - start_time))

            embedMessage = discord.Embed(color=0x0099ff)
            embedMessage.set_footer(text=getFooterText("text"), icon_url=getFooterText("url"))
            embedMessage.set_image(url="attachment://matchImage.png")
            returnText = embedMessage, filePath
    else:
        returnText = "Summoner does not exist!"
    return returnText


##################################################################################################################################
##################################################################################################################################
##################################################################################################################################

def getSplashURL(champion):
    url = "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{}_0.jpg".format(champion)
    return url

def getFooterText(type):
    text = 'gameScouter V2.5 - Commit 38'
    url = 'https://www.spriters-resource.com/resources/sheet_icons/99/101895.png'
    if type == "text":
        return text
    elif type == "url":
        return url
    else:
        print("[ERROR] Unknown footer type")
        return None
def getLane(spell1, spell2, lanes):
    spell = getNameById(spell1)
    if getNameById(spell1) == "Flash":
        spell = getNameById(spell2)
    print("Summonerspell: {}".format(spell))
    topSpells = ["Ignite","Teleport"]
    jungleSpells = ["Smite"]
    midSpells = ["Ignite","Cleanse","Barrier"]
    adcSpells = ["Heal"]
    supportSpells = ["Ignite","Exhaust"]
    if "Mid" in lanes:
        if spell in midSpells:
            return "Mid"
    if "Top" in lanes:
        if spell in topSpells:
            return "Top"
    if "Jungle" in lanes:
        if spell in jungleSpells:
            return "Jungle"
    if "ADC" in lanes:
        if spell in adcSpells:
            return "ADC"
    if "Support" in lanes:
        if spell in supportSpells:
            return "Support"
    print(lanes)
    return lanes[0]

def getMasteryChampion(MasteryInfoDetails1, MasteryInfoDetails2, MasteryInfoDetails3):
    mostPlayedChamp1 = getChampionByID(getChampionInformation(), MasteryInfoDetails1["championId"])
    mostPlayedChamp2 = getChampionByID(getChampionInformation(), MasteryInfoDetails2["championId"])
    mostPlayedChamp3 = getChampionByID(getChampionInformation(), MasteryInfoDetails3["championId"])
    return ":small_orange_diamond: " + mostPlayedChamp1 + "\n:small_orange_diamond: " + mostPlayedChamp2 + "\n:small_orange_diamond: " + mostPlayedChamp3


def getMasteryLevel(MasteryInfoDetails1, MasteryInfoDetails2, MasteryInfoDetails3):
    mostPlayedChampLevel1 = str(MasteryInfoDetails1["championLevel"])
    mostPlayedChampLevel2 = str(MasteryInfoDetails2["championLevel"])
    mostPlayedChampLevel3 = str(MasteryInfoDetails3["championLevel"])
    return "Level " + mostPlayedChampLevel1 + "\nLevel " + mostPlayedChampLevel2 + "\nLevel " + mostPlayedChampLevel3


def getMasteryPoints(MasteryInfoDetails1, MasteryInfoDetails2, MasteryInfoDetails3):
    mostPlayedChampPTS1 = str(MasteryInfoDetails1["championPoints"])
    mostPlayedChampPTS2 = str(MasteryInfoDetails2["championPoints"])
    mostPlayedChampPTS3 = str(MasteryInfoDetails3["championPoints"])
    return "pts " + mostPlayedChampPTS1 + "\npts " + mostPlayedChampPTS2 + "\npts " + mostPlayedChampPTS3


def getChampionByID(championInfo, championID):
    for championNames in championInfo["data"]:
        if str(championID) == championInfo["data"][championNames]["key"]:
            return championNames
    print("[ERROR] Unknown Champion ID: {}".format(championID))
    return "No Champion with ID: {}".format(championID)


def getSummonerIconURL(server, summonerName):
    # print("http://avatar.leagueoflegends.com/" + quote("{}/{}.png".format(server, summonerName)))
    url = "http://avatar.leagueoflegends.com/" + quote("{}/{}.png".format(server, summonerName))
    return url


def getWinrate(queueTypeInfo, queueType):
    totalWins = getSummonerRankInfoDetails(queueTypeInfo, queueType, "wins")
    totalLosses = getSummonerRankInfoDetails(queueTypeInfo, queueType, "losses")
    totalGames = totalWins + totalLosses
    winrate = str(round(totalWins / totalGames * 100))
    return winrate


def getRankAndLP(queueTypeInfo, queueType):
    tier = getSummonerRankInfoDetails(queueTypeInfo, queueType, "tier")
    rank = getSummonerRankInfoDetails(queueTypeInfo, queueType, "rank")
    lp = str(getSummonerRankInfoDetails(queueTypeInfo, queueType, "leaguePoints"))
    returnText = tier + " " + rank + " - " + lp + " LP"
    return returnText


def getSummonerExistance(summonerInfo):
    if summonerInfo == "NO SUMMONER FOUND":
        return False
    else:
        return True


def getSummonerRankInfoDetails(queueTypeInfo, queueType, whatInfo):
    for qType in queueTypeInfo:  # TEST IF SUMMONER HAS THIS QUEUETYPE RANK
        if qType["queueType"] == queueType:
            rankInfo = qType[whatInfo]
            return rankInfo
    print("[INFO] SUMMONER HAS NO RANK IN THIS QUEUE TYPE")
    return "SUMMONER HAS NO RANK IN THIS QUEUE TYPE"


def getSummonerMasteryInfoDetails(masteryInfo, placed):
    return masteryInfo[placed - 1]

def getLanePlayCount(matchListInfo):
    laneCount = {}
    for match in matchListInfo["matches"]:
        lane = match["lane"]
        if lane == "BOTTOM":
            lane = match["role"]
        if lane not in laneCount:
            laneCount[lane] = 0
        laneCount[lane] += 1
    return laneCount


def getChampionPlayCount(matchListInfo):
    championCount = {}
    for match in matchListInfo["matches"]:
        champion = match["champion"]
        if champion not in championCount:
            championCount[champion] = 0
        championCount[champion] += 1
    return championCount


def getHelpText():
    embedMessage = discord.Embed(title="Help", color=0x0099ff)
    embedMessage.add_field(name="**su: <Summonername>** ", value="Summoner Details - lists summoner details",
                           inline=False)
    embedMessage.add_field(name="**ig: <Summonername>** ", value="Match Details - lists game details", inline=False)
    return embedMessage


def getMatchReturnText(matchInfo):
    summoners = []

    for nr in range(10):
        summoners.append(matchInfo["participants"][nr - 1])

    returnText = "```"
    returnText += "MODE: {} \n".format(matchInfo["gameMode"])
    returnText += "ID: {} \n".format(matchInfo["gameId"])
    returnText += "gameType: {} \n".format(matchInfo["gameType"])
    returnText += "\n"
    returnText += "# TEAM 1 \n"
    for summoner in summoners:
        if summoner["teamId"] == 100:
            returnText += "Summonername: {} - Champion: {} - Rank {}\n".format(
                summoner["summonerName"],
                summoner["champion"],
                summoner["RankTier"]
            )

    returnText += "# TEAM 2 \n"
    for summoner in summoners:
        if summoner["teamId"] == 200:
            returnText += "Summonername: {} - Champion: {} - Rank {}\n".format(
                summoner["summonerName"],
                summoner["champion"],
                summoner["RankTier"]
            )

    returnText += "```"
    return returnText

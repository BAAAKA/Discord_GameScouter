import operator
import re
import discord
from gameInfoRequests import *
from createMatchupImage import getMatchImage
from matchData import getNameById, getLocalSplash_700
import time
import classModule
import pymysql


def getSummonerInfo(message):
    print("========================NEW SUMMONER INFO REQUEST========================")
    start_time = time.time()
    if isinstance(message, str):
        summonerName = message.split("su: ", 1)[1]
    else:
        summonerName = message.content.split("su: ", 1)[1]
    summonerInfo = getSummonerApiInfo(summonerName)

    if summonerInfo:
        embedMessage = discord.Embed(title=summonerInfo["name"], color=0x0099ff)
        embedMessage.description = "Level {}".format(summonerInfo["summonerLevel"])
        queueTypeInfo = getSummonerRankApiInfo(summonerInfo["id"])
        if queueTypeInfo:
            soloQRank = getSummonerRankInfoDetails(queueTypeInfo, "RANKED_SOLO_5x5", "rank")
            flexQRank = getSummonerRankInfoDetails(queueTypeInfo, "RANKED_FLEX_SR", "rank")
            if not re.search("SUMMONER HAS NO RANK*", soloQRank):
                embedMessage.add_field(name=":beginner: SoloQ Rank ",
                                       value=getRankAndLP(queueTypeInfo, "RANKED_SOLO_5x5"), inline=False)
                embedMessage.add_field(name="Wins ",
                                       value=getSummonerRankInfoDetails(queueTypeInfo, "RANKED_SOLO_5x5", "wins"),
                                       inline=True)
                embedMessage.add_field(name="Losses ",
                                       value=getSummonerRankInfoDetails(queueTypeInfo, "RANKED_SOLO_5x5", "losses"),
                                       inline=True)
                embedMessage.add_field(name="Winrate ", value=getWinrate(queueTypeInfo, "RANKED_SOLO_5x5") + "%",
                                       inline=True)
            if not re.search("SUMMONER HAS NO RANK*", flexQRank):
                embedMessage.add_field(name=":beginner: FlexQ Rank ",
                                       value=getRankAndLP(queueTypeInfo, "RANKED_FLEX_SR"), inline=False)
                embedMessage.add_field(name="Wins ",
                                       value=getSummonerRankInfoDetails(queueTypeInfo, "RANKED_FLEX_SR", "wins"),
                                       inline=True)
                embedMessage.add_field(name="Losses ",
                                       value=getSummonerRankInfoDetails(queueTypeInfo, "RANKED_FLEX_SR", "losses"),
                                       inline=True)
                embedMessage.add_field(name="Winrate ", value=getWinrate(queueTypeInfo, "RANKED_FLEX_SR") + "%",
                                       inline=True)

        masteryInfo = getSummonerMasteryInfo(summonerInfo["id"])
        # MASTERINFODETAILS
        if not (masteryInfo == []):
            print("[INFO] Summoner has mastery")
            MID1 = getSummonerMasteryInfoDetails(masteryInfo, 1)
            MID2 = getSummonerMasteryInfoDetails(masteryInfo, 2)
            MID3 = getSummonerMasteryInfoDetails(masteryInfo, 3)

            embedMessage.add_field(name="Masteries", value=getMasteryChampion(MID1, MID2, MID3), inline=True)
            embedMessage.add_field(name="_", value=getMasteryLevel(MID1, MID2, MID3), inline=True)
            embedMessage.add_field(name="_", value=getMasteryPoints(MID1, MID2, MID3), inline=True)
        else:
            print("[INFO] Summoner has no mastery!")

        # Most Played Champs
        matchListInfo = getMatchListApiInfo(summonerInfo["accountId"])
        if "status" not in matchListInfo:  # If status key exists in the matchListInfo directory its probably a 404, does not exist
            championCount = getChampionPlayCount(matchListInfo)
            championInfo = getChampionInformation()
            mostPlayedChamp = []
            for i in range(3):
                mostPlayedChamp.append(list(max(championCount.items(), key=operator.itemgetter(1))))
                championName = getChampionByID(championInfo, mostPlayedChamp[i][0])
                mostPlayedChamp[i].append(championName)
                del championCount[mostPlayedChamp[i][0]]

            champNames = getMostPlayedText(mostPlayedChamp[0][2], mostPlayedChamp[1][2], mostPlayedChamp[2][2])
            champPlayedAmount = "{}x\n{}x\n{}x".format(mostPlayedChamp[0][1], mostPlayedChamp[1][1],
                                                       mostPlayedChamp[2][1])

            embedMessage.add_field(name="Most played recently", value=champNames, inline=True)
            embedMessage.add_field(name="Last 100 games", value=champPlayedAmount, inline=True)

            embedMessage.set_thumbnail(
                url=getSummonerIconURL_withID(summonerInfo["profileIconId"]))  # Set Summoner Icon Avatar
            filepath = getLocalSplash_700(mostPlayedChamp[0][2])
        else:
            filepath = getLocalSplash_700("Kindred")
        embedMessage.set_image(url="attachment://championImage.jpg")
    else:
        return "Summoner does not exist"

    embedMessage.set_footer(text=getFooterText("text"), icon_url=getFooterText("url"))
    print("[INFO] ----------------- %s seconds for the getSummonerInfo request -----------------" % (
                time.time() - start_time))
    return embedMessage, filepath


def getMatchInfo(message):
    print("========================NEW MATCH INFO REQUEST========================")
    start_time = time.time()
    if isinstance(message, str):
        summonerName = message.split("game:", 1)[1]
    else:
        summonerName = message.content.split("game:", 1)[1]

    requestSummoner = classModule.summoner(summonerName)
    summonerInfo = getSummonerApiInfo(requestSummoner.name)
    if not summonerInfo:
        returnText = "Summoner does not exist!"
        return returnText

    try:
        requestSummoner.setSummonerInfo(summonerInfo)
        matchInfo = getMatchApiInfo(requestSummoner.id)
    except:
        print("[ERROR] Error while trying to see if summoner is ingame")
        returnText = "Error while trying to see if summoner is ingame..."
        return returnText

    if not matchInfo:  # TEST IF SUMMONER IS INGAME
        print("[INFO] Summoner is not ingame right now - done")
        returnText = "This summoner is not ingame right now..."
        return returnText

    # here you know that the summoner exists and is ingame
    championInfo = getChampionInformation()
    # Async all getSummonerRank requests
    summonerIDArray = []

    match = classModule.match(matchInfo)

    for summoner in match.participants:
        summonerIDArray.append(summoner["summonerId"])
    summonerRanks = getSummonerRankApiInfoArray(summonerIDArray)

    time.sleep(1)

    # Async all summonerInfo requests
    summonerNameArray = []
    for summoner in match.participants:
        summonerNameArray.append(summoner["summonerName"])
    summonerInfos = getSummonerApiInfoArray(summonerNameArray)

    # Async all matchListInfo requests
    accountIdArray = []
    for summoner in summonerInfos:
        summoner = summoner.json()
        try:
            accountIdArray.append(summoner["accountId"])
        except:
            print("[ERROR] Summoner has no accountID: {}".format(summoner))
            accountIdArray.append("NONE")
    matchListInfos = getMatchListApiInfoArray(accountIdArray)

    # Set All Data
    nr = 0
    for participant in match.participants:
        player = classModule.summoner(participant["summonerName"])
        player.teamId = participant["teamId"]
        player.spell1Id = participant["spell1Id"]
        player.spell2Id = participant["spell2Id"]
        player.championId = participant["championId"]
        player.profileIconId = participant["profileIconId"]
        player.bot = participant["bot"]
        player.summonerId = participant["summonerId"]
        player.gameCustomizationObjects = participant["gameCustomizationObjects"]
        player.perks = participant["perks"]
        player.nr = nr
        player.champion = getChampionByID(championInfo, player.championId)
        match.players.append(player)
        print("[INFO] Appended player {}".format(player.name))
        nr += 1  # nr wird für matchlist genutzt, da bei dem keine summer info dabei ist

    print("[INFO] ====Beginning Rank/MatchList/SummonerInfo defining====")
    for player in match.players:
        player.matchList = matchListInfos[player.nr].json()
        player.mainChamp = getChampionByID(championInfo, player.getMostPalyedChamp())
        for rank in summonerRanks:
            ranked = rank.json()
            if len(ranked) > 0:
                try:
                    if ranked[0]["summonerId"] == player.summonerId:  # Correct player (Name doesnt work always)
                        if ranked[0]["queueType"] == "RANKED_SOLO_5x5":
                            player.setRankInfo(ranked[0])
                            print("[INFO] Player {} has the Rank {} in {}".format(player.name, player.rankTier,
                                                                                  "RANKED_SOLO_5x5"))
                            if len(ranked) > 1:
                                player.setFlexRankInfo(ranked[1])
                                print("[INFO] Player {} has the Rank {} in {}".format(player.name, player.FrankTier,
                                                                                      "RANKED_FLEX_SR"))
                            break
                        elif ranked[0]["queueType"] == "RANKED_FLEX_SR":
                            player.setFlexRankInfo(ranked[0])
                            if len(ranked) > 1:
                                player.setRankInfo(ranked[1])
                                print("[INFO] Player {} has the Rank {} in {}".format(player.name, player.FrankTier,
                                                                                      "RANKED_SOLO_5x5"))
                            break
                except:
                    print("[ERROR] While setting Rankf or Player {}, Rate Limit? ".format(player.name))
                    break

        for summoner in summonerInfos:
            summoner = summoner.json()
            if summoner["name"] == player.name:
                player.setSummonerInfo(summoner)
                continue

    # Lane allocation
    setLaneByChamp(match)

    print(
        "[INFO] ----------------- %s seconds for the getMatchInfo data -----------------" % (time.time() - start_time))
    start_timeImage = time.time()
    filePath = getMatchImage(match)
    print("[INFO] ----------------- %s seconds for the creation of the image -----------------" % (
                time.time() - start_timeImage))
    print("[INFO] ----------------- %s seconds for total match request -----------------" % (time.time() - start_time))

    embedMessage = discord.Embed(color=0x0099ff)
    embedMessage.set_footer(text=getFooterText("text"), icon_url=getFooterText("url"))
    embedMessage.set_image(url="attachment://matchImage.jpg")
    returnText = embedMessage, filePath
    return returnText


def setLaneByChamp(match):
    print("[INFO] ====Beginning Lane Allocation====")
    rawChampData = readTextfile("champToLane.txt")
    champData = {}
    for champ in rawChampData:
        champData[champ[0]] = [champ[1], champ[2]]

    lanes = ["Jungle", "Top", "Middle", "Support", "ADC"]

    maxLoop = 30
    r = 0
    teamId = 100
    while lanes and maxLoop > r:
        success = False
        for player in match.players:
            if player.lane == "none" and player.teamId == teamId and "Jungle" in lanes:  # Set JGL
                if getNameById(player.spell1Id) == "Smite" or getNameById(player.spell2Id) == "Smite":
                    print("[INFO] Found the jungler with Smite! <{}> is playing <{}> in the Jungle with smite".format(
                        player.name, player.champion))
                    lanes.remove("Jungle")
                    player.lane = "Jungle"
        lane = lanes[0]
        print("[INFO] looking for play in the lane: {}".format(lane))
        for player in match.players:
            if player.lane == "none" and player.teamId == teamId:
                champ = player.champion
                try:
                    print("[INFO] Player <{}> is playing <{}> and is searching for Lane <{}>".format(player.name,
                                                                                                     player.champion,
                                                                                                     champData[champ][
                                                                                                         0]))
                    if (champData[champ][0] == lane):
                        print("[INFO] [FOUND CORRECT LANE] player <{}> is playing <{}> on the lane <{}>".format(
                            player.name,
                            player.champion, lane))
                        success = True
                        lanes.remove(lane)
                        player.lane = lane
                        break
                except:
                    print("[ERROR] I HAVE NOT SEEN THIS CHAMPION BEFORE")
                    success = True
                    lanes.remove(lane)
                    player.lane = lane
                    break

        if not success:
            print("[INFO] Couldnt find any primary position, looking for a secondary position!")
            for player in match.players:
                if player.lane == "none" and player.teamId == teamId:
                    champ = player.champion
                    print("[INFO] Player <{}> is playing <{}> and is searching for Lane <{}>".format(player.name,
                                                                                                     player.champion,
                                                                                                     champData[champ][
                                                                                                         1]))
                    if (champData[champ][1] == lane):
                        print("[INFO] [FOUND CORRECT LANE] player <{}> is playing <{}> on the lane <{}>".format(
                            player.name,
                            player.champion, lane))
                        success = True
                        lanes.remove(lane)
                        player.lane = lane
                        break
        if not success:
            for player in match.players:
                if player.lane == "none" and player.teamId == teamId:
                    print(
                        "[INFO] [FAIL] Couldnt find Lane - Player <{}> is now playing <{}> on the lane <{}>".format(
                            player.name,
                            player.champion, lane))
                    lanes.remove(lane)
                    player.lane = lane
                    break
        r += 1
        if teamId == 100:
            teamId = 200
            for player in match.players:
                if player.teamId == 100 and player.lane == "none":
                    teamId = 100
                    break
            if teamId == 200:
                print("[INFO] All Player of the first team have a lane - TEAM SWITCH!")
                lanes = ["Jungle", "Top", "Middle", "Support", "ADC"]


def readTextfile(filename):
    text_file = open(filename, "r")
    lines = text_file.read().split('\n')
    content = []
    for line in lines:
        content.append(line.split(","))
    print("[INFO] Succesfully read the textfile {}".format(filename))
    return content


def getSplashURL(champion):
    url = "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{}_0.jpg".format(champion)
    return url


def getFooterText(type):
    text = 'gameScouter V4.0 - C 60'
    url = 'https://www.spriters-resource.com/resources/sheet_icons/99/101895.png'
    if type == "text":
        return text
    elif type == "url":
        return url
    else:
        print("[ERROR] Unknown footer type")
        return None


def getLane(spell1, spell2, lanes, mainLane):
    spell = getNameById(spell1)
    if getNameById(spell1) == "Flash":
        spell = getNameById(spell2)
    topSpells = ["Teleport", "Ignite"]
    jungleSpells = ["Smite"]
    midSpells = ["Ignite", "Cleanse", "Barrier"]
    adcSpells = ["Heal"]
    supportSpells = ["Ignite", "Exhaust"]
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
    if mainLane in lanes:
        return mainLane
    return lanes[0]


def getMasteryChampion(MasteryInfoDetails1, MasteryInfoDetails2, MasteryInfoDetails3):
    mostPlayedChamp1 = getChampionByID(getChampionInformation(), MasteryInfoDetails1["championId"])
    mostPlayedChamp2 = getChampionByID(getChampionInformation(), MasteryInfoDetails2["championId"])
    mostPlayedChamp3 = getChampionByID(getChampionInformation(), MasteryInfoDetails3["championId"])
    return ":small_orange_diamond: " + mostPlayedChamp1 + "\n:small_orange_diamond: " + mostPlayedChamp2 + "\n:small_orange_diamond: " + mostPlayedChamp3


def getMostPlayedText(c1, c2, c3):  # Return text for SU: most played champ
    return ":fleur_de_lis: " + c1 + "\n:fleur_de_lis: " + c2 + "\n:fleur_de_lis: " + c3


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


def getSummonerRankInfoDetails(queueTypeInfo, queueType, whatInfo):
    for qType in queueTypeInfo:  # TEST IF SUMMONER HAS THIS QUEUETYPE RANK
        try:
            if qType["queueType"] == queueType:
                rankInfo = qType[whatInfo]
                return rankInfo
        except:
            print("[ERROR] False type in getSummonerRankInfoDetails, Rate limit exceeded? - Returned <NO RANK>")
            return "SUMMONER HAS NO RANK IN THIS QUEUE TYPE"

    print("[INFO] SUMMONER HAS NO RANK IN THIS QUEUE TYPE")
    return "SUMMONER HAS NO RANK IN THIS QUEUE TYPE"


def getSummonerMasteryInfoDetails(masteryInfo, placed):
    return masteryInfo[placed - 1]


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
    embedMessage.add_field(name="**game: <Summonername>** ", value="Game Details - Current game details", inline=False)
    embedMessage.add_field(name="**help:** ", value="You get some info... like this", inline=False)
    embedMessage.add_field(name="**info:** ", value="Information about the bot", inline=False)
    return embedMessage


def getInfoText():
    embedMessage = discord.Embed(title="Info", color=0x0099ff)
    embedMessage.add_field(name="**Creator** ", value="https://github.com/BAAAKA", inline=False)
    embedMessage.add_field(name="**GitHub** ", value="https://github.com/BAAAKA/Discord_GameScouter", inline=False)
    embedMessage.add_field(name="**What is this** ",
                           value="Bot that gives you league summoner and match information. Use help: for more",
                           inline=False)
    return embedMessage


infoText = getFooterText("text")
print("""
###############################################
        Discord gameScouter!
        {}
        Made by: KAWAII BAAAKA
###############################################
""".format(infoText))
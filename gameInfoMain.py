import operator
import re
import discord
from gameInfoRequests import *
from createMatchupImage import getMatchImage
from matchData import getNameById, getLocalSplash_700
import time
import pymysql


def getSummonerInfo(message):
    print("========================NEW SUMMONER INFO REQUEST========================")
    start_time = time.time()
    if isinstance(message, str):
        summonerName = message.split("su: ", 1)[1]
    else:
        summonerName = message.content.split("su: ", 1)[1]
    summonerInfo = getSummonerApiInfo(summonerName)
    embedMessage = discord.Embed(title=summonerInfo["name"], color=0x0099ff)

    if getSummonerExistance(summonerInfo):
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

        #Most Played Champs
        matchListInfo = getMatchListApiInfo(summonerInfo["accountId"])
        if "status" not in matchListInfo: #If status key exists in the matchListInfo directory its probably a 404, does not exist
            championCount = getChampionPlayCount(matchListInfo)
            championInfo = getChampionInformation()
            mostPlayedChamp = []
            for i in range(3):
                mostPlayedChamp.append(list(max(championCount.items(), key=operator.itemgetter(1))))
                championName = getChampionByID(championInfo, mostPlayedChamp[i][0])
                mostPlayedChamp[i].append(championName)
                del championCount[mostPlayedChamp[i][0]]

            champNames = getMostPlayedText(mostPlayedChamp[0][2], mostPlayedChamp[1][2], mostPlayedChamp[2][2])
            champPlayedAmount = "{}x\n{}x\n{}x".format(mostPlayedChamp[0][1], mostPlayedChamp[1][1], mostPlayedChamp[2][1])

            embedMessage.add_field(name="Most played recently", value=champNames, inline=True)
            embedMessage.add_field(name="Last 100 games", value=champPlayedAmount, inline=True)

            embedMessage.set_thumbnail(url=getSummonerIconURL_withID(summonerInfo["profileIconId"])) #Set Summoner Icon Avatar
            filepath = getLocalSplash_700(mostPlayedChamp[0][2])
        else:
            filepath = getLocalSplash_700("Kindred")
        embedMessage.set_image(url="attachment://championImage.png")
    else:
        return "Summoner does not exist"

    embedMessage.set_footer(text=getFooterText("text"), icon_url=getFooterText("url"))
    print("[INFO] ----------------- %s seconds for the getSummonerInfo request -----------------" % (time.time() - start_time))
    return embedMessage, filepath

def getMatchInfo(message):
    print("========================NEW MATCH INFO REQUEST========================")
    start_time = time.time()
    if isinstance(message, str):
        summonerName = message.split("ig:", 1)[1]
    else:
        summonerName = message.content.split("ig:", 1)[1]

    summonerInfo = getSummonerApiInfo(summonerName)
    if getSummonerExistance(summonerInfo):
        matchInfo = getMatchApiInfo(summonerInfo["id"])
        if matchInfo == "SUMMONER IS NOT INGAME":  # TEST IF SUMMONER IS INGAME
            print("[INFO] Summoner is not ingame right now - done")
            returnText = "This summoner is not ingame right now..."
        else:
            # here you know that the summoner exists and is ingame
            lanes = []
            championInfo = getChampionInformation()
            #Async all getSummonerRank requests
            summonerIDArray = []
            x = 0
            for summoner in matchInfo["participants"]:
                summoner["number"] = x
                x+=1
                summonerIDArray.append(summoner["summonerId"])
            summonerRanks = getSummonerRankApiInfoArray(summonerIDArray)

            if os.name == "nt":
                time.sleep(5) #Delay because of rate limits; For some its way slower in Linux, therefore its only needed in windows

            # Async all summonerInfo requests
            summonerNameArray = []
            for summoner in matchInfo["participants"]:
                summonerNameArray.append(summoner["summonerName"])
            summonerInfos = getSummonerApiInfoArray(summonerNameArray)

            # Async all matchListInfo requests
            accountIdArray = []
            for summoner in summonerInfos:
                summoner = summoner.json()
                accountIdArray.append(summoner["accountId"])
            matchListInfos = getMatchListApiInfoArray(accountIdArray)

            #Set All Data
            for summoner in matchInfo["participants"]:
                rankInfo = summonerRanks[summoner["number"]].json()
                matchListInfo = matchListInfos[summoner["number"]].json()

                Tier = getSummonerRankInfoDetails(rankInfo, "RANKED_SOLO_5x5", "tier")
                if re.search("SUMMONER HAS NO RANK*", Tier):
                    summonerRank = "Unranked"
                    summoner["tier"] = summonerRank
                    summoner["RankTier"] = summonerRank
                    summoner["wins"] = "0"
                    summoner["losses"] = "0"
                    summoner["winRate"] = "0"

                else:
                    Rank = getSummonerRankInfoDetails(rankInfo, "RANKED_SOLO_5x5", "rank")
                    summonerRank = Tier + " " + Rank
                    summoner["tier"] = Tier
                    summoner["RankTier"] = summonerRank
                    summoner["wins"] = getSummonerRankInfoDetails(rankInfo, "RANKED_SOLO_5x5", "wins")
                    summoner["losses"] = getSummonerRankInfoDetails(rankInfo, "RANKED_SOLO_5x5", "losses")
                    summoner["winRate"] = getWinrate(rankInfo, "RANKED_SOLO_5x5")
                # Champion
                summoner["champion"] = getChampionByID(championInfo, summoner["championId"])
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


            # Lane allocation
            matchInfo["participants"] = setLaneByChamp(matchInfo["participants"])

            print("[INFO] ----------------- %s seconds for the getMatchInfo data -----------------" % (time.time() - start_time))
            start_timeImage = time.time()
            filePath = getMatchImage(matchInfo)
            print("[INFO] ----------------- %s seconds for the creation of the image -----------------" % (time.time() - start_timeImage))
            print("[INFO] ----------------- %s seconds for total match request -----------------" % (time.time() - start_time))

            embedMessage = discord.Embed(color=0x0099ff)
            embedMessage.set_footer(text=getFooterText("text"), icon_url=getFooterText("url"))
            embedMessage.set_image(url="attachment://matchImage.jpg")
            returnText = embedMessage, filePath
    else:
        returnText = "Summoner does not exist!"
    return returnText

def setSummonername(message):
    print("========================Setting Summonername========================")
    gsDBpw = os.environ['gsDBpw']
    connection = pymysql.connect(
        '192.168.0.28',
        'gsUser',
        gsDBpw,
        'gameScouterDB',
    )
    summonerName = message.content.split("setname:", 1)[1]
    sName = str(summonerName)
    dName = str(message.author)
    result = setDB(connection, sName, dName)
    return result

def getMyGame(message):
    print("========================Getting Discord Name Game========================")
    gsDBpw = os.environ['gsDBpw']
    connection = pymysql.connect(
        '192.168.0.28',
        'gsUser',
        gsDBpw,
        'gameScouterDB',
    )
    try:
        dName = str(message.author)
        with connection:
            cur = connection.cursor()
            cur.execute("SELECT sName FROM summoners where dName = '{}' limit 1".format(dName))
            sName = cur.fetchone()[0]
            print(sName)
            print("[INFO] Succesfull Database request | Author: {}, SN: {}".format(dName, sName))
    except Exception as e:
        print("[ERROR] Database Error: {}".format(e))
        return "Database Error: {}".format(e)

    return getMatchInfo("ig:{}".format(sName))

def getMySummoner(message):
    print("========================Getting Discord Name Summoner========================")
    gsDBpw = os.environ['gsDBpw']
    connection = pymysql.connect(
        '192.168.0.28',
        'gsUser',
        gsDBpw,
        'gameScouterDB',
    )
    try:
        dName = str(message.author)
        with connection:
            cur = connection.cursor()
            cur.execute("SELECT sName FROM summoners where dName = '{}' limit 1".format(dName))
            sName = cur.fetchone()[0]
            #print(sName)
            print("[INFO] Succesfull Database request | Author: {}, SN: {}".format(dName, sName))
    except Exception as e:
        print("[ERROR] Database Error: {}".format(e))
        return "Database Error: {}".format(e)

    return getSummonerInfo("su:{}".format(sName))

def setLaneByChamp(summoners):
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
        for summoner in summoners:
            if not "lane" in summoner and summoner["teamId"] == teamId and "Jungle" in lanes:
                if getNameById(summoner["spell1Id"]) == "Smite" or getNameById(summoner["spell2Id"]) == "Smite":
                    print("[INFO] Found the jungler with Smite! <{}> is playing <{}> in the Jungle with smite".format(summoner["summonerName"],summoner["champion"]))
                    lanes.remove("Jungle")
                    summoner["lane"] = "Jungle"

        lane = lanes[0]
        print("[INFO] looking for play in the lane: {}".format(lane))
        for summoner in summoners:
            if not "lane" in summoner and summoner["teamId"] == teamId:
                champ = summoner["champion"]
                print("[INFO] summoner <{}> is playing <{}> and is searching for Lane <{}>".format(summoner["summonerName"],
                                                                                      summoner["champion"],
                                                                                      champData[champ][0]))
                if (champData[champ][0] == lane):
                    print("[INFO] [FOUND CORRECT LANE] player <{}> is playing <{}> on the lane <{}>".format(summoner["summonerName"],
                                                                                         summoner["champion"], lane))
                    success = True
                    lanes.remove(lane)
                    summoner["lane"] = lane
                    break
        if not success:
            print("[INFO] Couldnt find any primary position, looking for a secondary position!")
            for summoner in summoners:
                if not "lane" in summoner and summoner["teamId"] == teamId:
                    champ = summoner["champion"]
                    print("[INFO] summoner <{}> is playing <{}> and is searching for Lane <{}>".format(summoner["summonerName"],
                                                                                          summoner["champion"],
                                                                                          champData[champ][1]))
                    if (champData[champ][1] == lane):
                        print("[INFO] [FOUND CORRECT LANE] player <{}> is playing <{}> on the lane <{}>".format(summoner["summonerName"],
                                                                                             summoner["champion"],
                                                                                             lane))
                        success = True
                        lanes.remove(lane)
                        summoner["lane"] = lane
                        break
        if not success:
            for summoner in summoners:
                if not "lane" in summoner and summoner["teamId"] == teamId:
                    print(
                        "[INFO] [FAIL] Couldnt find Lane - Player <{}> is now playing <{}> on the lane <{}>".format(summoner["summonerName"], summoner["champion"],
                                                                                 lane))
                    lanes.remove(lane)
                    summoner["lane"] = lane
                    break
        r += 1
        if teamId == 100:
            teamId = 200
            for summoner in summoners:
                if summoner["teamId"] == 100 and "lane" not in summoner:
                    teamId = 100
                    break
            if teamId == 200:
                print("[INFO] All Player of the first team have a lane - TEAM SWITCH!")
                lanes = ["Jungle", "Top", "Middle", "Support", "ADC"]
    return summoners

def readTextfile(filename):
    text_file = open(filename, "r")
    lines = text_file.read().split('\n')
    content = []
    for line in lines:
        content.append(line.split(","))
    print("[INFO] Succesfully read the textfile {}".format(filename))
    return content

def setDB(connection, sName, dName):
    try:
        with connection:
            cur = connection.cursor()
            cur.execute("INSERT INTO summoners (sName, dName) VALUES (%s,%s)", (sName, dName))
        connection.commit()
        print("[INFO] Successfully set Summonername: {} | Autor: {}".format(sName, dName))
        return "Success!"
    except Exception as e:
        print("[ERROR] unsuccessful in setting the Summonername!")
        print("[ERROR] Message: {}".format(e))
        return "unsuccessful"

def getDB(connection, dName):
    with connection:
        cur = connection.cursor()
        cur.execute("SELECT sName FROM summoners where dName = '{}' limit 1".format(dName))
        sName = cur.fetchone()[0]
        print("[INFO] Successfully got Summonername: {}".format(sName))
        return sName

def getSplashURL(champion):
    url = "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{}_0.jpg".format(champion)
    return url

def getFooterText(type):
    text = 'gameScouter V3.7 - C 52'
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
    topSpells = ["Teleport","Ignite"]
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
    if mainLane in lanes:
        return mainLane
    return lanes[0]

def getMasteryChampion(MasteryInfoDetails1, MasteryInfoDetails2, MasteryInfoDetails3):
    mostPlayedChamp1 = getChampionByID(getChampionInformation(), MasteryInfoDetails1["championId"])
    mostPlayedChamp2 = getChampionByID(getChampionInformation(), MasteryInfoDetails2["championId"])
    mostPlayedChamp3 = getChampionByID(getChampionInformation(), MasteryInfoDetails3["championId"])
    return ":small_orange_diamond: " + mostPlayedChamp1 + "\n:small_orange_diamond: " + mostPlayedChamp2 + "\n:small_orange_diamond: " + mostPlayedChamp3

def getMostPlayedText(c1, c2, c3): #Return text for SU: most played champ
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
    try:
        matchListInfo["matches"]
    except:
        print("[ERROR] No <matches> found, matchListInfo: {}".format(matchListInfo))
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
    embedMessage.add_field(name="**su: <Summonername>** ", value="Summoner Details - lists summoner details", inline=False)
    embedMessage.add_field(name="**ig: <Summonername>** ", value="Match Details - lists game details", inline=False)
    embedMessage.add_field(name="**help** ", value="You get some info... like this", inline=False)
    embedMessage.add_field(name="**info** ", value="Information about the bot", inline=False)
    embedMessage.add_field(name="**setName: <Summonername>** ", value="Set your summonername", inline=False)
    embedMessage.add_field(name="**mGame** ", value="gets your game if you set it with setName", inline=False)
    embedMessage.add_field(name="**mSummoner** ", value="gets your summoner if you set it with setName", inline=False)

    return embedMessage

def getInfoText():
    embedMessage = discord.Embed(title="Info", color=0x0099ff)
    embedMessage.add_field(name="**Creator** ", value="https://github.com/BAAAKA", inline=False)
    embedMessage.add_field(name="**What is this** ", value="Bot that gives you league summoner and match information", inline=False)
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

infoText = getFooterText("text")
print("""
###############################################
        Discord gameScouter!
        {}
        Made by: KAWAII BAAAKA
###############################################
""".format(infoText))
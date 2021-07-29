import operator
import re
import discord
from gameInfoRequests import *
from createMatchupImage import getMatchImage
from matchData import getNameById, getLocalSplash_700
import time
import classModule
from DBConnector import input, read, exists, updating, reconnect


def getSummonerInfo(message):
    print("========================NEW SUMMONER INFO REQUEST========================")
    start_time = time.time()

    reconnectDB()

    if message.content == "su:":
        try:  # Get Summoner from DB
            print("[INFO] No Summonername was given by {}, ID: {}, asking DB".format(message.author, message.author.id))
            summonerName = read(message.author.id)
            if (summonerName):
                print("[INFO] Found summoner {} in the DB!".format(summonerName))
            else:
                print("[INFO] There was no result, returning returnText")
                returnText = "Found no Summoner for the discord User `{}`. Have you used `game: (Summonername)` before?".format(
                    message.author)
                return returnText
        except Exception as e:
            print("[ERROR] Something went wrong while searching for the SummonerName: {}".format(e))
            returnText = "Something broke.., try `game: (Summonername)`".format(
                message.author)
            return returnText
    else:  # Get Summonername from Message
        summonerName = getSummonerFromMessage(message, "su:")
    summonerInfo = getSummonerApiInfo(summonerName)
    if not summonerInfo:
        return "Summoner does not exist"

    player = classModule.summoner("summonerName")
    player.setSummonerInfo(summonerInfo)

    embedMessage = discord.Embed(title=player.name, color=0x0099ff)
    embedMessage.description = "Level {}".format(player.summonerLevel)
    rank = getSummonerRankApiInfo(player.id)
    if rank:
        try:
            if len(rank) == 2:
                if rank[0]["queueType"] == "RANKED_SOLO_5x5":
                    player.setRankInfo(rank[0])
                    player.setFlexRankInfo(rank[1])
                else:
                    player.setRankInfo(rank[1])
                    player.setFlexRankInfo(rank[0])
            elif len(rank) == 1:
                if rank[0]["queueType"] == "RANKED_SOLO_5x5":
                    player.setRankInfo(rank[0])
                else:
                    player.setFlexRankInfo(rank[0])
            else:
                print("[INFO] {} has no ranks".format(player.name))
                pass
        except Exception as e:
            print("[ERROR] while checking rank, rate limit?: {}".format(e))
            return

        if (player.rank):
            embedMessage.add_field(name=":beginner: SoloQ Rank ",
                                   value=player.tier + " " + player.rank + " " + str(player.leaguePoints) + " LP", inline=False)
            embedMessage.add_field(name="Wins ",
                                   value=player.wins,
                                   inline=True)
            embedMessage.add_field(name="Losses ",
                                   value=player.losses,
                                   inline=True)
            embedMessage.add_field(name="Winrate ", value=player.winrate + "%",
                                   inline=True)
        if (player.Frank):
            embedMessage.add_field(name=":beginner: FlexQ Rank ",
                                   value=player.Ftier + " " + player.Frank + " " + str(player.FleaguePoints) + " LP", inline=False)
            embedMessage.add_field(name="Wins ",
                                   value=player.Fwins,
                                   inline=True)
            embedMessage.add_field(name="Losses ",
                                   value=player.Flosses,
                                   inline=True)
            embedMessage.add_field(name="Winrate ", value=player.Fwinrate + "%",
                                   inline=True)

    masteryInfo = getSummonerMasteryInfo(player.id)
    # MASTERINFODETAILS
    if (masteryInfo):
        player.setMasteryInfo(masteryInfo)
        print("[INFO] Summoner has mastery")
        embedMessage.add_field(name="Masteries", value=getMasteryChampion(player.mastery1, player.mastery2, player.mastery3), inline=True)
        embedMessage.add_field(name="_", value=getMasteryLevel(player.mastery1, player.mastery2, player.mastery3), inline=True)
        embedMessage.add_field(name="_", value=getMasteryPoints(player.mastery1, player.mastery2, player.mastery3), inline=True)
    else:
        print("[INFO] Summoner has no mastery!")

    # Most Played Champs
    player.matchList = getMatchListApiInfo(player.accountID)
    if(player.matchList):
        championInfo = getChampionInformation()
        c1 = player.getMostPlayedChamp(1) #[0] ist champ ID, [1] ist spiel anz
        c2 = player.getMostPlayedChamp(2)
        c3 = player.getMostPlayedChamp(3)
        player.mainChamp = getChampionByID(championInfo, c1[0])
        player.mainChamp2 = getChampionByID(championInfo, c2[0])
        player.mainChamp3 = getChampionByID(championInfo, c3[0])


        topThreeChamps = ":fleur_de_lis: " + player.mainChamp + "\n:fleur_de_lis: " + player.mainChamp2 + "\n:fleur_de_lis: " + player.mainChamp3
        champPlayedAmount = "{}x\n{}x\n{}x".format(str(c1[1]), str(c2[1]), str(c3[1]))

        embedMessage.add_field(name="Recently played", value=topThreeChamps, inline=True)
        embedMessage.add_field(name="Last 100 games", value=champPlayedAmount, inline=True)

        embedMessage.set_thumbnail(
            url=getSummonerIconURL_withID(summonerInfo["profileIconId"]))  # Set Summoner Icon Avatar
        filepath = getLocalSplash_700(player.mainChamp)
        #Tags

        playerTags = setTags(player)
        embedMessage.add_field(name="This Summoner is ...", value=playerTags, inline=False)

    else:
        filepath = getLocalSplash_700("Kindred")

    embedMessage.set_image(url="attachment://championImage.jpg")
    embedMessage.set_footer(text=getFooterText("text"), icon_url=getFooterText("url"))
    print("[INFO] ----------------- %s seconds for the getSummonerInfo request -----------------" % (
            time.time() - start_time))
    return embedMessage, filepath


def getMatchInfo(message):
    print("========================NEW MATCH INFO REQUEST========================")
    start_time = time.time()

    reconnectDB()

    if message.content == "game:":
        try:  # Get Summoner from DB
            print("[INFO] No Summonername was given by {}, ID: {}, asking DB".format(message.author, message.author.id))
            summonerName = read(message.author.id)
            if (summonerName):
                print("[INFO] Found summoner {} in the DB!".format(summonerName))
            else:
                print("[INFO] There was no result, returning returnText")
                returnText = "Found no Summoner for the discord User `{}`. Have you used `game: (Summonername)` before?".format(
                    message.author)
                return returnText
        except Exception as e:
            print("[ERROR] Something went wrong while searching for the SummonerName: {}".format(e))
            returnText = "Something broke.., try `game: (Summonername)`".format(
                message.author)
            return returnText
    else:  # Get Summonername from Message
        summonerName = getSummonerFromMessage(message, "game:")

    requestSummoner = classModule.summoner(summonerName)
    summonerInfo = getSummonerApiInfo(requestSummoner.name)
    if not summonerInfo:
        returnText = "Summoner {} does not exist!".format(summonerName)
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

    time.sleep(0.5)

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
        player.mainChamp = getChampionByID(championInfo, player.getMostPlayedLane(1))
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
                    print("[ERROR] While setting Rank or Player {}, Rate Limit? ".format(player.name))
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

def setTags(player):
    returnText = ""
    try:
        skillGroup = tierToTag(player.tier)
        if (player.tier == "DIAMOND" and (player.rank == "I" or player.rank == "II" )):
            skillGroup = "(:trident: `Elite`)"
        returnText += skillGroup
    except Exception as e:
        print("[ERROR] in skillgrouping {}".format(e))

    if(player.winrate):
        returnText += winrateToTag(int(player.winrate))

    returnText += levelToTag(player.summonerLevel)

    if(player.mastery1 and player.mastery2):
        if(player.mastery1["championPoints"] > player.mastery2["championPoints"]*2):
            returnText += " (:horse: `1Trick`)"
    if(player.getMostPlayedChamp(1)[1] < 13):
        returnText += " (:black_joker: `Diverse Player`)"
    if(hasattr(player, "leaguePoints") and player.leaguePoints < 5):
        returnText += " (:sweat_drops: `About to drop`)"
    if(hasattr(player, "hotStreak") and player.hotStreak):
        returnText += "(:fire: `hotStreak`)"
    if(hasattr(player, "inactive") and player.inactive):
        returnText += "(:zzz: `inactive`)"
    returnText += champToTag([player.mainChamp, player.mainChamp2, player.mainChamp3])
    try:
        returnText += laneToRole(player.getMostPlayedLane())
        epoch_time = int(time.time())
        match_time = int(player.matchList["matches"][99]["timestamp"]/1000)
        hundredGamesAgo = epoch_time-match_time
        if(2160000 > hundredGamesAgo): #If (time in sec 99 games ago) is smaller than 25 days
            returnText += " (:fire: `Active player`)"
    except:
        pass
    return returnText

def champToTag(champArray):
    for i in range(2):
        champ = champArray[i]
        if champ == None:
            return ""
        elif champ == "Trundle":
            return " (:mountain_snow: `Troll King`)"
        elif champ == "Teemo":
            return " (:imp: `Evil`)"
        elif champ == "Soraka":
            return " (:ambulance: `Ambulance`)"
        elif champ == "Yone" or champ == "Yasuo" or champ == "Akali":
            return " (:flag_jp: `Edgy weeb`)"
        elif champ == "Draven":
            return " (:sunglasses: `Arena favorite`)"
        elif champ == "Lee Sin":
            return " (:flag_jp: `Playmaker`)"
        elif champ == "Veigar":
            return " (:smiling_imp: `Truly Evil`)"
        elif champ == "Aurelion Sol":
            return " (:comet: `good player`)"
        elif champ == "Vel'Koz":
            return " (:triangular_ruler: `Has a math degree`)"
        elif champ == "Vayne":
            return " (:bow_and_arrow: `Gosu`)"
        elif champ == "Heimerdinger":
            return " (:tokyo_tower: `Tower defense`)"
        elif champ == "Ziggs":
            return " (:bomb: `Bomberman`)"
        elif champ == "Ivern" or champ == "Zyra":
            return " (:olive: `Gardener`)"
        elif champ == "Ziggs":
            return " (:bomb: `Bomberman`)"
        elif champ == "Jhin":
            return " (:four: `Four`)"
        elif champ == "Lux":
            return " (:rainbow: `Double Rainbow`)"
        elif champ == "Nautilus" or champ == "Pyke":
            return " (:whale: `Ruler of the sea`)"
        elif champ == "Leona":
            return " (:sunny: `Praise the sun`)"
        elif champ == "Sett":
            return " (:boom: `DIO`)"
        elif champ == "Nami":
            return " (:sushi: `Sushi`)"
        elif champ == "Zac":
            return " (:microbe: `Slimy`)"
        elif champ == "Nunu":
            return " (:snowflake: `Snowball`)"
        elif champ == "Cassiopeia":
            return " (:snake: `Scaly`)"
        elif champ == "Azir":
            return " (:desert: `Ruler of Shurima`)"
    return ""



def winrateToTag(winrate):
    if (winrate < 40):
        return " (:cloud_tornado: `Trolling?`)"
    elif (winrate < 48):
        return " (:chart_with_downwards_trend: `Losing a lot`)"
    elif (winrate > 60):
        return " (:signal_strength: `Smurfing`)"
    elif (winrate > 52):
        return " (:chart_with_upwards_trend: `Climber`)"
    else:
        return " (:moyai: `Hardstuck`)"


def levelToTag(level):
    if(level >= 0 and level < 50):
        return " (:baby: `Newbie`)"
    elif(level >= 50 and level < 200):
        return " (:owl: `Experienced`)"
    elif (level >= 200 and level < 300):
        return " (:desktop: `addict`)"
    elif (level >= 300 and level < 400):
        return " (:keyboard: `No life`)"
    elif(level >= 400 and level < 500):
        return " (:pill: `Dangerous addict`)"
    elif(level >= 500):
        return " (:medical_symbol: `Get some help`)"
    elif(level >= 700):
        return " (:question: `???`)"

def tierToTag(tier):
    skillGrouping = {
        "Unranked": "(:zzz: `Casual`)",
        "IRON": "(:cyclone: `Average`)",
        "BRONZE": "(:cyclone: `Average`)",
        "SILVER": "(:rosette: `Experienced`)",
        "GOLD": "(:rosette: `Experienced`)",
        "PLATINUM": "(:trophy: `Skilled`)",
        "DIAMOND": "(:trophy: `Skilled`)",
        "MASTER": "(:trident: `Elite`)",
        "GRANDMASTER": "(:trident: `Elite`)",
        "CHALLENGER": "(:trident: `Elite/Pro`)",
    }
    return skillGrouping[tier]

def laneToRole(lane):
    try:
        laneToRole={
            "TOP":"(:crossed_swords: `Toplaner`)",
            "JUNGLE":"(:palm_tree: `Jungler`)",
            "MID":"(:man_mage: `Midlaner`)",
            "DUO_CARRY":"(:bow_and_arrow: `ADC`)",
            "DUO_SUPPORT":"(:shield: `Support`)",
        }
        return laneToRole[lane]
    except:
        return ""

def readTextfile(filename):
    text_file = open(filename, "r")
    lines = text_file.read().split('\n')
    content = []
    for line in lines:
        content.append(line.split(","))
    print("[INFO] Succesfully read the textfile {}".format(filename))
    return content


def getSummonerFromMessage(message, prefix):
    if isinstance(message, str):  # Message exists
        summonerName = message.split(prefix, 1)[1].strip()
    else:
        summonerName = message.content.split(prefix, 1)[1].strip()
    inputSNameIntoDB(message, summonerName)
    return summonerName


def inputSNameIntoDB(message, summonerName):
    try:
        if exists(message.author.id):  # If the ID exists in the DB..
            if read(message.author.id) == summonerName:
                print("[INFO] DiscordID exists and is set to the correct Summoner, passing..")
            else:
                print("[INFO] DiscordID exists, but set incorrectly, updating!")
                updating(message.author.id, summonerName)
        else:
            print("[INFO] DiscordID doesnt exist yet")
            input(message.author.id, summonerName)
    except Exception as e:
        print("[ERROR] Something went wrong when checking the DiscordID with the DB: {}".format(e))


def getSplashURL(champion):
    url = "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{}_0.jpg".format(champion)
    return url


def getFooterText(type):
    text = 'gameScouter V5.0 - C 65'
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


def reconnectDB():
    try:
        reconnect()
    except Exception as e:
        print("[ERROR] Reconnecting to DB failed: {}".format(e))


def getMasteryChampion(MasteryInfoDetails1, MasteryInfoDetails2, MasteryInfoDetails3):
    returnText = ""
    if(MasteryInfoDetails1):
        mostPlayedChamp1 = getChampionByID(getChampionInformation(), MasteryInfoDetails1["championId"])
        returnText += ":small_orange_diamond: " + mostPlayedChamp1
    if (MasteryInfoDetails2):
        mostPlayedChamp2 = getChampionByID(getChampionInformation(), MasteryInfoDetails2["championId"])
        returnText += "\n:small_orange_diamond: " + mostPlayedChamp2
    if (MasteryInfoDetails3):
        mostPlayedChamp3 = getChampionByID(getChampionInformation(), MasteryInfoDetails3["championId"])
        returnText += "\n:small_orange_diamond: " + mostPlayedChamp3
    return returnText


def getMostPlayedText(c1, c2, c3):  # Return text for SU: most played champ
    return ":fleur_de_lis: " + c1 + "\n:fleur_de_lis: " + c2 + "\n:fleur_de_lis: " + c3


def getMasteryLevel(MasteryInfoDetails1, MasteryInfoDetails2, MasteryInfoDetails3):
    returnText = ""
    if(MasteryInfoDetails1):
        mostPlayedChampLevel1 = str(MasteryInfoDetails1["championLevel"])
        returnText += "Level " + mostPlayedChampLevel1
    if (MasteryInfoDetails2):
        mostPlayedChampLevel2 = str(MasteryInfoDetails2["championLevel"])
        returnText += "\nLevel " + mostPlayedChampLevel2
    if (MasteryInfoDetails3):
        mostPlayedChampLevel3 = str(MasteryInfoDetails3["championLevel"])
        returnText += "\nLevel " + mostPlayedChampLevel3
    return returnText

def getMasteryPoints(MasteryInfoDetails1, MasteryInfoDetails2, MasteryInfoDetails3):
    returnText = ""
    if(MasteryInfoDetails1):
        mostPlayedChampPTS1 = str(MasteryInfoDetails1["championPoints"])
        returnText += "pts " + mostPlayedChampPTS1
    if (MasteryInfoDetails2):
        mostPlayedChampPTS2 = str(MasteryInfoDetails2["championPoints"])
        returnText += "\npts " + mostPlayedChampPTS2
    if (MasteryInfoDetails3):
        mostPlayedChampPTS3 = str(MasteryInfoDetails3["championPoints"])
        returnText += "\npts " + mostPlayedChampPTS3
    return returnText

def getChampionByID(championInfo, championID):
    for championNames in championInfo["data"]:
        if str(championID) == championInfo["data"][championNames]["key"]:
            return championNames
    print("[ERROR] Unknown Champion ID: {}".format(championID))
    return championID


def getRankAndLP(queueTypeInfo, queueType):
    tier = getSummonerRankInfoDetails(queueTypeInfo, queueType, "tier")
    rank = getSummonerRankInfoDetails(queueTypeInfo, queueType, "rank")
    lp = str(getSummonerRankInfoDetails(queueTypeInfo, queueType, "leaguePoints"))
    returnText = tier + " " + rank + " " + lp + " LP"
    return returnText


def getSummonerRankInfoDetails(queueTypeInfo, queueType, whatInfo):
    for qType in queueTypeInfo:  # TEST IF SUMMONER HAS THIS QUEUETYPE RANK
        try:
            if qType["queueType"] == queueType:
                rankInfo = qType[whatInfo]
                return rankInfo
        except:
            print("[ERROR] False type in getSummonerRankInfoDetails, Rate limit exceeded? - Returned <NO RANK>")
            return None

    print("[INFO] SUMMONER HAS NO RANK IN THIS QUEUE TYPE")
    return None


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

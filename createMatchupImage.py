import sys
from PIL import Image, ImageDraw, ImageFont
from matchData import *
from gameInfoRequests import getChampionInformation
from pathlib import Path
import time

def getFontSized(size):
    return ImageFont.truetype(getFont(), size)

def getMatchImage(matchInfo):
    print("[INFO] getMatchImage!")
    imageArena = getArena()
    summoners = {}

    startPositions = getStartPositions()
    d = ImageDraw.Draw(imageArena)

    x=1
    for summonerNr in matchInfo["participants"]:
        summoners[str(x)] = summonerNr
        print("[INFO] SUMMONERS: {}".format(summoners[str(x)]["summonerName"]))
        x=x+1

    #Get Summoner Tier and Spells and champ images
    for summoner in summoners:
        summoners[summoner]["championImage"] = Image.open(getLocalTitlesImage(summoners[summoner]["champion"]))
        tier=summoners[summoner]["tier"].lower().capitalize()
        summoners[summoner]["tierImage"] = Image.open(getLocalRankedImage(tier))
        name1 = getNameById(summoners[summoner]["spell1Id"])
        name2 = getNameById(summoners[summoner]["spell2Id"])
        summoners[summoner]["spell1Image"] = Image.open(getLocalSummonersImage(name1))
        summoners[summoner]["spell2Image"] = Image.open(getLocalSummonersImage(name2))
        prekId = summoners[summoner]["perks"]["perkIds"][0]
        summoners[summoner]["perkImage"] = Image.open(getLocalPerkImage(prekId))

    # Post Champion, Summonername and Tier
    for summonerNr in summoners:
        summonerLane = summoners[summonerNr]["lane"]
        x = startPositions[0][summonerLane]
        if summoners[summonerNr]["teamId"] == 100:
            y = startPositions[1]
        else:
            y = startPositions[2]

        # Champion
        imageArena.paste(summoners[summonerNr]["championImage"], getAreaOfTitles(x, y))

        #Rank
        imageArena.paste(summoners[summonerNr]["tierImage"], getAreaOfEmblem(x+40, y+200), mask=summoners[summonerNr]["tierImage"])
        d.text((x+5, y + 480), summoners[summonerNr]["RankTier"], font=getFontSized(30), fill=(255, 255, 255))
        if not "Unranked" == summoners[summonerNr]["RankTier"]:
            wins = summoners[summonerNr]["wins"]
            losses = summoners[summonerNr]["losses"]
            winRate = summoners[summonerNr]["winRate"]
            rankedStats = "{}% {}W/{}L".format(winRate, wins, losses)
            d.text((x+5, y + 510), rankedStats, font=getFontSized(28), fill=(255, 255, 255))


        #Summonername
        if len(summoners[summonerNr]["summonerName"]) < 12:
            d.text((x+10, y-70),summoners[summonerNr]["summonerName"], font=getFontSized(50), fill=(255, 255, 255))
        else:
            d.text((x+10, y-60),summoners[summonerNr]["summonerName"], font=getFontSized(42), fill=(255, 255, 255))

        #Summoners
        imageArena.paste(summoners[summonerNr]["spell1Image"], getAreaOfSpells(x, y + 400))
        imageArena.paste(summoners[summonerNr]["spell2Image"], getAreaOfSpells(x+64, y + 400))

        # Perkz
        #prekId = summoners[summonerNr]["perks"]["perkIds"][0]
        #print("{}: {}".format(summoners[summonerNr]["summonerName"], prekId))
        image=summoners[summonerNr]["perkImage"]
        imageEdited = image.resize((64,64))
        imageArena.paste(imageEdited, getAreaOfCustom(x+128, y + 400, 64), mask=imageEdited)

        # Most Played Lane
        mostPlayedLane = summoners[summonerNr]["mostPlayedLanes"][0][0]
        if mostPlayedLane == "DUO_CARRY":
            mostPlayedLane = "ADC"
        elif mostPlayedLane == "DUO_SUPPORT":
            mostPlayedLane = "SUPPORT"
        d.text((x+5, y + 600), "Main role: {}".format(mostPlayedLane), font=getFontSized(25), fill=(255, 255, 255))

        # Most Played Champ
        mostPlayedChamp = summoners[summonerNr]["mostPlayedChamps"][0][2]
        d.text((x+5, y + 630), "Main champ: {}".format(mostPlayedChamp), font=getFontSized(25), fill=(255, 255, 255))

        # Lane
        lane = summoners[summonerNr]["lane"]
        d.text((x+5, y + 660), "Lane: {}".format(lane), font=getFontSized(25), fill=(255, 255, 255))

    # MIDDLEPART
    middleImageX = 100
    middleImageY = 920

    d.text((middleImageX, middleImageY+100), "Gamemode: "+matchInfo["gameMode"], font=getFontSized(35), fill=(255, 255, 255))
    d.text((middleImageX+600, middleImageY+100), "Map: "+getMapById(matchInfo["mapId"]), font=getFontSized(35), fill=(255, 255, 255))
    d.text((middleImageX+1540, middleImageY+100), "Bans: ", font=getFontSized(35), fill=(255, 255, 255))

    # BANNED CHAMPIONS
    championInfo = getChampionInformation()
    imageSize = 80
    turns = 1
    row = 0
    for banned in matchInfo["bannedChampions"]:
        champion = getChampionByID(championInfo, banned["championId"])
        image = Image.open(getLocalTitlesImage(champion))
        imageEdited = image.resize((imageSize,imageSize))
        imageArena.paste(imageEdited, getAreaOfCustom(middleImageX+((imageSize+6)*turns)+1600, middleImageY+row, imageSize))
        turns += 1
        if turns == 6:
            turns = 1
            row = 130


    #END
    filename = time.strftime("MATCH%Y%m%d-%H%M%S.jpg")
    filePath = "temp/{}".format(filename)
    imageArena_jpg = imageArena.convert('RGB')
    imageArena_jpg.save(filePath)
    print("[INFO] Done with match Image!")
    return filePath


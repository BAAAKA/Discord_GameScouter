import sys
from PIL import Image, ImageDraw, ImageFont
from matchData import *
from gameInfoRequests import getChampionInformation

from pathlib import Path

import time
def getMatchImage(matchInfo):
    print("[INFO] getMatchImage!")
    imageArena = getArenaClean()
    #summoners = getSummoners()
    summoners = {}

    startPositions = getStartPositions()
    fnt = ImageFont.truetype(getFont(), 50)
    fnt42 = ImageFont.truetype(getFont(), 42)
    fnt35 = ImageFont.truetype(getFont(), 35)
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
        x = startPositions[summonerNr][0]
        y = startPositions[summonerNr][1]
        imageArena.paste(summoners[summonerNr]["championImage"], getAreaOfTitles(x, y))
        imageArena.paste(summoners[summonerNr]["tierImage"], getAreaOfEmblem(x+20, y+200), mask=summoners[summonerNr]["tierImage"])
        if len(summoners[summonerNr]["summonerName"]) < 12:
            d.text((x, y-70),summoners[summonerNr]["summonerName"], font=fnt, fill=(255, 255, 255))
        else:
            d.text((x, y-60),summoners[summonerNr]["summonerName"], font=fnt42, fill=(255, 255, 255))

        d.text((x, y + 480), summoners[summonerNr]["RankTier"], font=fnt35, fill=(255, 255, 255))
        imageArena.paste(summoners[summonerNr]["spell1Image"], getAreaOfSpells(x, y + 400))
        imageArena.paste(summoners[summonerNr]["spell2Image"], getAreaOfSpells(x+64, y + 400))

        # Perkz
        prekId = summoners[summonerNr]["perks"]["perkIds"][0]
        print("{}: {}".format(summoners[summonerNr]["summonerName"], prekId))
        image=summoners[summonerNr]["perkImage"]
        imageEdited = image.resize((64,64))
        imageArena.paste(imageEdited, getAreaOfCustom(x+128, y + 400, 64), mask=imageEdited)

        # Most Played Lane
        d.text((x, y + 600), summoners[summonerNr]["mostPlayedLanes"][0][0], font=fnt35, fill=(255, 255, 255))

        # Most Played Champ
        d.text((x, y + 650), summoners[summonerNr]["mostPlayedChamps"][0][2], font=fnt35, fill=(255, 255, 255))

    # MIDDLEPART
    middleImageX = 100
    middleImageY = 920

    d.text((middleImageX, middleImageY), "Gamemode: "+matchInfo["gameMode"], font=fnt35, fill=(255, 255, 255))
    d.text((middleImageX+600, middleImageY), "Map: "+getMapById(matchInfo["mapId"]), font=fnt35, fill=(255, 255, 255))
    d.text((middleImageX+1540, middleImageY), "Bans: ", font=fnt35, fill=(255, 255, 255))

    # BANNED CHAMPIONS
    print(matchInfo["bannedChampions"])
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
    filename = time.strftime("MATCH%Y%m%d-%H%M%S.png")
    filePath = "temp/{}".format(filename)
    imageArena.save(filePath)
    print("[INFO] Done with match Image!")
    return filePath


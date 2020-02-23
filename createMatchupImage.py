import sys
from PIL import Image, ImageDraw, ImageFont
from matchData import *
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

    #Get Summoner Tier
    for summoner in summoners:
        summoners[summoner]["championImage"] = Image.open(getLocalTitlesImage(summoners[summoner]["champion"]))
        tier=summoners[summoner]["tier"].lower().capitalize()
        summoners[summoner]["tierImage"] = Image.open(getLocalRankedImage(tier))

    #Post Champion, Summonername and Tier
    for summonerNr in summoners:
        x = startPositions[summonerNr][0]
        y = startPositions[summonerNr][1]
        imageArena.paste(summoners[summonerNr]["championImage"], getAreaOfTitles(x, y))
        imageArena.paste(summoners[summonerNr]["tierImage"], getAreaOfEmblem(x+20, y+200), mask=summoners[summonerNr]["tierImage"])
        if len(summoners[summonerNr]["summonerName"]) < 12:
            d.text((x, y-70),summoners[summonerNr]["summonerName"] , font=fnt, fill=(255, 255, 255))
        else:
            d.text((x, y-60),summoners[summonerNr]["summonerName"] , font=fnt42, fill=(255, 255, 255))

        d.text((x, y + 480), summoners[summonerNr]["RankTier"], font=fnt35, fill=(255, 255, 255))


    filename = time.strftime("MATCH%Y%m%d-%H%M%S.png")
    filePath = "temp/{}".format(filename)
    imageArena.save(filePath)
    print("[INFO] Done with match Image!")
    return filePath


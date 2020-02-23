import sys
from PIL import Image, ImageDraw, ImageFont
from matchData import *
import time
def getMatchImage(matchInfo):
    imageArena = getArenaBig()
    #summoners = getSummoners()
    summoners = {}

    startPositions = getStartPositions()
    fnt = ImageFont.truetype(getFont(), 50)
    d = ImageDraw.Draw(imageArena)

    x=1
    for summonerNr in matchInfo["participants"]:
        print(summonerNr)
        print(summonerNr["summonerName"])
        summoners[str(x)] = summonerNr
        x=x+1


    for summoner in summoners:
        print(summoners[summoner]["champion"])
        summoners[summoner]["championImage"] = Image.open(getLocalTitlesImage(summoners[summoner]["champion"]))
        summoners[summoner]["tierImage"] = Image.open(getLocalRankedImage(summoners[summoner]["tier"]))

    for summonerNr in summoners:
        x = startPositions[summonerNr][0]
        y = startPositions[summonerNr][1]
        imageArena.paste(summoners[summonerNr]["championImage"], getAreaOfTitles(x, y))
        imageArena.paste(summoners[summonerNr]["tierImage"], getAreaOfEmblem(x, y+200), mask=summoners[summonerNr]["tierImage"])
        d.text((x, y-55),summoners[summonerNr]["summonerName"] , font=fnt, fill=(255, 255, 255))

    filename = time.strftime("MATCH%Y%m%d-%H%M%S.png")
    filePath = "temp/{}".format(filename)
    imageArena.save(filePath)
    return filePath


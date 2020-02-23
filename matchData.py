from PIL import Image
from pathlib import Path
import os

imageFolder = "data/img/champion/loading"
imageRankFolder = r"data/ranked-emblems"
imageTitlesFolder = r"data/img/champion/tiles"
imageArenaPath = Path(r"data/img/global/arena.png")
imageArenaPath2 = Path(r"data/img/global/arena2.png")
imageArenaBigPath = Path(r"data/img/global/arenaBig.jpg")
imageArenaCleanPath = Path(r"data/img/global/arenaClean.png")


if os.name == "nt":
    print("WINDOWS FONT")
    fontPath = r"D:\Programme\pyCharm\jbr\lib\fonts\SourceCodePro-Bold.ttf"
else:
    print("LINUX FONT")
    fontPath = r"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def getFont():
    return fontPath

def getArena():
    return Image.open(imageArenaPath)


def getArenaClean():
    return Image.open(imageArenaCleanPath)

def getArena2():
    return Image.open(imageArenaPath2)

def getArenaBig():
    return Image.open(imageArenaBigPath)

def getLocalLoadingImage(champion):
    path = Path(imageFolder + "/{}_0.jpg".format(champion))
    return path

def getLocalTitlesImage(champion):
    path = Path(imageTitlesFolder + "/{}_0.jpg".format(champion))
    return path

def getLocalRankedImage(rank):
    path = Path(imageRankFolder + "/Emblem_{}.png".format(rank))
    return path

def getSplashURL(champion):
    url="https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{}_0.jpg".format(champion)
    return url

def getLoadingURL(champion):
    url="https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{}_0.jpg".format(champion)
    return url

def getAreaOfSplash(width,height):
    imageHeight=560
    imageWidth=308
    x2=width+imageWidth
    y2=height+imageHeight
    return width,height,x2,y2

def getAreaOfEmblem(width,height):
    imageHeight=585
    imageWidth=512
    x2=width+imageWidth
    y2=height+imageHeight
    return width,height,x2,y2

def getAreaOfTitles(width,height):
    imageHeight=380
    imageWidth=380
    x2=width+imageWidth
    y2=height+imageHeight
    return width,height,x2,y2

summoner1 = {}
summoner2 = {}
summoner3 = {}
summoner4 = {}
summoner5 = {}
summoner6 = {}
summoner7 = {}
summoner8 = {}
summoner9 = {}
summoner10 = {}

summoner1["summonerName"] = "KAWAII BAAAKA"
summoner1["lane"] = "top"
summoner1["champion"] = "Aatrox"
summoner1["tier"] = "Grandmaster"

summoner2["summonerName"] = "LMAO"
summoner2["lane"] = "jungel"
summoner2["champion"] = "Khazix"
summoner2["tier"] = "Gold"

summoner3["summonerName"] = "kek"
summoner3["lane"] = "mid"
summoner3["champion"] = "Ahri"
summoner3["tier"] = "Challenger"

summoner4["summonerName"] = "sadPepe"
summoner4["lane"] = "adc"
summoner4["champion"] = "Xayah"
summoner4["tier"] = "Platinum"

summoner5["summonerName"] = "somethingSomething69Sexual"
summoner5["lane"] = "support"
summoner5["champion"] = "Rakan"
summoner5["tier"] = "Bronze"

summoner6["summonerName"] = "lul"
summoner6["lane"] = "top"
summoner6["champion"] = "Jax"
summoner6["tier"] = "Iron"

summoner7["summonerName"] = "midOrAFK"
summoner7["lane"] = "jgl"
summoner7["champion"] = "Kindred"
summoner7["tier"] = "Master"

summoner8["summonerName"] = "iHateRito"
summoner8["lane"] = "mid"
summoner8["champion"] = "Zed"
summoner8["tier"] = "Master"

summoner9["summonerName"] = "UwU Master xx"
summoner9["lane"] = "adc"
summoner9["champion"] = "Kayle"
summoner9["tier"] = "Diamond"

summoner10["summonerName"] = "AhriXVelkoz"
summoner10["lane"] = "support"
summoner10["champion"] = "Soraka"
summoner10["tier"] = "Silver"


summoners={}
summoners["1"] = summoner1
summoners["2"] = summoner2
summoners["3"] = summoner3
summoners["4"] = summoner4
summoners["5"] = summoner5
summoners["6"] = summoner6
summoners["7"] = summoner7
summoners["8"] = summoner8
summoners["9"] = summoner9
summoners["10"] = summoner10

for summoner in summoners:
    summoners[summoner]["championImage"] = Image.open(getLocalTitlesImage(summoners[summoner]["champion"]))
    summoners[summoner]["rankImage"] = Image.open(getLocalRankedImage(summoners[summoner]["tier"]))

def getSummoners():
    return summoners


startPositions = {}
startPositions["1"] = (0, 100)
startPositions["2"] = (500, 100)
startPositions["3"] = (1000, 100)
startPositions["4"] = (1500, 100)
startPositions["5"] = (2000, 100)
startPositions["6"] = (0, 1000)
startPositions["7"] = (500, 1000)
startPositions["8"] = (1000, 1000)
startPositions["9"] = (1500, 1000)
startPositions["10"] = (2000, 1000)

def getStartPositions():
    return startPositions



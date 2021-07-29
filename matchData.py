from PIL import Image
from pathlib import Path
import os

imageChampionFolder = "data/img/champion/loading"
imageRankFolder = r"data/ranked-emblems"
imageTitlesFolder = r"data/img/champion/tiles"
imageSplash700Folder = r"data/img/champion/splash_700"
imageSummonersFolder = r"data/summonerSpells"
imagePerkFolder = r"data/perks"
imagePIconFolder = r"data/profileicon"
imageArenaPath = Path(r"data/img/global/arena.png")
imageArenaPath2 = Path(r"data/img/global/arena2.png")
imageArenaBigPath = Path(r"data/img/global/arenaBig.jpg")
imageArenaCleanPath = Path(r"data/img/global/arenaClean.png")

summonerSpells = {}
summonerSpells[1] = "Cleanse"
summonerSpells[3] = "Exhaust"
summonerSpells[4] = "Flash"
summonerSpells[6] = "Ghost"
summonerSpells[7] = "Heal"
summonerSpells[11] = "Smite"
summonerSpells[12] = "Teleport"
summonerSpells[13] = "Clarity"
summonerSpells[14] = "Ignite"
summonerSpells[21] = "Barrier"
summonerSpells[32] = "Mark"

queue = {}
queue[0] = "Unknown"
queue[400] = "Normal (Draft Pick)"
queue[440] = "Ranked Flex"
queue[450] = "Aram"
queue[1400] = "Ultimate Spellbook"
queue[420] = "Ranked Solo/Duo"


perks = {}
perks[8005] = "Precision", "PressTheAttack"
perks[8008] = "Precision", "LethalTempoTemp"
perks[8010] = "Precision", "Conqueror"
perks[8021] = "Precision", "FleetFootwork"

perks[8112] = "Domination", "Electrocute"
perks[8124] = "Domination", "Predator"
perks[8128] = "Domination", "DarkHarvest"
perks[9923] = "Domination", "HailOfBlades"

perks[8214] = "Sorcery", "SummonAery"
perks[8229] = "Sorcery", "ArcaneComet"
perks[8230] = "Sorcery", "PhaseRush"

perks[8351] = "Inspiration", "GlacialAugment"
perks[8360] = "Inspiration", "UnsealedSpellbook"
perks[83] = "Inspiration", "GlacialAugment"

perks[8437] = "Resolve", "GraspOfTheUndying"
perks[8439] = "Resolve", "VeteranAftershock"
perks[8465] = "Resolve", "Guardian"

if os.name == "nt":
    print("[INFO] WINDOWS FONT")
    fontPath = r"D:\Programs\PyCharm Community Edition 2020.2.3\jbr\lib\fonts\SourceCodePro-Bold.ttf"
else:
    print("[INFO] LINUX FONT")
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
    path = Path(imageChampionFolder + "/{}_0.jpg".format(champion))
    return path


def getLocalTitlesImage(champion):
    path = Path(imageTitlesFolder + "/{}_0.jpg".format(champion))
    if os.path.isfile(path):
        return path
    else:  # If Champion doesnt exist
        defaultTitlesPath = Path(imageTitlesFolder + "/{}.jpg".format("default"))
        return defaultTitlesPath


def getLocalRankedImage(rank):
    path = Path(imageRankFolder + "/Emblem_{}.png".format(rank))
    return path


def getLocalSummonersImage(summoners):
    path = Path(imageSummonersFolder + "/{}.png".format(summoners))
    return path


def getLocalSplash_700(champion):
    path = Path(imageSplash700Folder + "/{}_0.jpg".format(champion))
    if os.path.isfile(path):
        return path
    else:  # If Champion doesnt exist
        defaultTitlesPath = Path(imageTitlesFolder + "/{}.jpg".format("default"))
        return defaultTitlesPath


def getLocalPerkImage(perkId):
    try:
        perks[perkId]
    except:
        print("UNKNOWN perkId: {}".format(perkId))
        path = Path(imagePerkFolder + "/{}/{}.png".format("unknown", "unknown"))
        return path
    tree, perk = perks[perkId]
    path = Path(imagePerkFolder + "/{}/{}.png".format(tree, perk))
    return path


def getNameById(id):
    try:
        return summonerSpells[id]
    except Exception as e:
        print("[ERROR] Unknown summonerSpell ID: {}".format(e))
        return summonerSpells[1]

def getQueueById(id):
    try:
        return queue[id]
    except Exception as e:
        print("[ERROR] Unknown queue ID: {}".format(e))
        return queue[0]

def getMapById(id):
    try:
        if (id == 11):
            return "Summoners Rift"
        elif (id == 12):
            return "Howling Abyss"
        else:
            return "idk this map, what is it, take this id: " + str(id)
    except Exception as e:
        print("[ERROR] Unknown map: {}".format(e))
        return "Default"


def getSplashURL(champion):
    url = "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{}_0.jpg".format(champion)
    return url


def getLoadingURL(champion):
    url = "https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{}_0.jpg".format(champion)
    return url


def getChampionByID(championInfo, championID):
    for championNames in championInfo["data"]:
        if str(championID) == championInfo["data"][championNames]["key"]:
            return championNames
    if championID == -1:
        return "unknown"
    print("[ERROR] Unknown Champion ID: {}".format(championID))
    return "No Champion with ID: {}".format(championID)


def getAreaOfSplash(width, height):
    imageHeight = 560
    imageWidth = 308
    x2 = width + imageWidth
    y2 = height + imageHeight
    return width, height, x2, y2


def getAreaOfEmblem(width, height):
    imageHeight = 585
    imageWidth = 512
    x2 = width + imageWidth
    y2 = height + imageHeight
    return width, height, x2, y2


def getAreaOfTitles(width, height):
    imageHeight = 380
    imageWidth = 380
    x2 = width + imageWidth
    y2 = height + imageHeight
    return width, height, x2, y2


def getAreaOfSpells(width, height):
    imageHeight = 64
    imageWidth = 64
    x2 = width + imageWidth
    y2 = height + imageHeight
    return width, height, x2, y2


def getAreaOfCustom(width, height, size):
    imageHeight = size
    imageWidth = size
    x2 = width + imageWidth
    y2 = height + imageHeight
    return width, height, x2, y2


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

summoners = {}
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


yStartTeam1 = 100
yStartTeam2 = 1245
startPositions = {}
startPositions["Top"] = 0
startPositions["Jungle"] = 500
startPositions["Middle"] = 1000
startPositions["ADC"] = 1500
startPositions["Support"] = 2000


def getStartPositions():
    return startPositions, yStartTeam1, yStartTeam2

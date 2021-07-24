import sys
from PIL import Image, ImageDraw, ImageFont
from matchData import *
from gameInfoRequests import getChampionInformation
from pathlib import Path
import time

def getFontSized(size):
    return ImageFont.truetype(getFont(), size)

def getMatchImage(match):
    print("[INFO] getMatchImage!")
    imageArena = getArena()

    startPositions = getStartPositions()
    d = ImageDraw.Draw(imageArena)

    #Get Summoner Tier and Spells and champ images
    for player in match.players:
        player.championImage = Image.open(getLocalTitlesImage(player.champion))
        tier = player.tier.lower().capitalize()
        player.tierImage = Image.open(getLocalRankedImage(tier))
        player.spell1 = getNameById(player.spell1Id)
        player.spell2 = getNameById(player.spell2Id)
        player.spell1Image = Image.open(getLocalSummonersImage(player.spell1))
        player.spell2Image = Image.open(getLocalSummonersImage(player.spell2 ))
        player.perkId = player.perks["perkIds"][0]
        player.perkImage = Image.open(getLocalPerkImage(player.perkId))

    # Post Champion, Summonername and Tier
    for player in match.players:
        x = startPositions[0][player.lane]
        if player.teamId == 100:
            y = startPositions[1]
        elif player.teamId == 200:
            y = startPositions[2]

        # Champion
        imageArena.paste(player.championImage, getAreaOfTitles(x, y))

        #Rank
        imageArena.paste(player.tierImage, getAreaOfEmblem(x+40, y+200), mask=player.tierImage)
        d.text((x+5, y + 480), player.rankTier, font=getFontSized(30), fill=(255, 255, 255))
        if not "Unranked" == player.rankTier:
            wins = player.wins
            losses = player.losses
            winRate = player.getWinrate()
            rankedStats = "{}% {}W/{}L".format(winRate, wins, losses)
            d.text((x+5, y + 510), rankedStats, font=getFontSized(28), fill=(255, 255, 255))


        #Summonername
        if len(player.name) < 12:
            d.text((x+10, y-70),player.name, font=getFontSized(50), fill=(255, 255, 255))
        else:
            d.text((x+10, y-60),player.name, font=getFontSized(42), fill=(255, 255, 255))

        #Summoners
        imageArena.paste(player.spell1Image, getAreaOfSpells(x, y + 400))
        imageArena.paste(player.spell2Image, getAreaOfSpells(x+64, y + 400))

        # Perkz
        #prekId = player.perks["PerkIds"][0]
        #print("{}: {}".format(player["summonerName"], prekId))
        image=player.perkImage
        imageEdited = image.resize((64,64))
        imageArena.paste(imageEdited, getAreaOfCustom(x+128, y + 400, 64), mask=imageEdited)

        # Most Played Lane
        mostPlayedLane = player.getMostPalyedLane()
        if mostPlayedLane == "DUO_CARRY":
            mostPlayedLane = "ADC"
        elif mostPlayedLane == "DUO_SUPPORT":
            mostPlayedLane = "SUPPORT"
        d.text((x+5, y + 600), "Main role: {}".format(mostPlayedLane), font=getFontSized(25), fill=(255, 255, 255))

        # Most Played Champ
        mostPlayedChamp = player.mainChamp
        d.text((x+5, y + 630), "Main champ: {}".format(mostPlayedChamp), font=getFontSized(25), fill=(255, 255, 255))

        # Lane
        lane = player.lane
        d.text((x+5, y + 660), "Lane: {}".format(lane), font=getFontSized(25), fill=(255, 255, 255))

    # MIDDLEPART
    middleImageX = 100
    middleImageY = 920

    d.text((middleImageX, middleImageY+100), "Gamemode: "+match.gameMode, font=getFontSized(35), fill=(255, 255, 255))
    d.text((middleImageX+600, middleImageY+100), "Map: "+getMapById(match.mapId), font=getFontSized(35), fill=(255, 255, 255))
    d.text((middleImageX+1540, middleImageY+100), "Bans: ", font=getFontSized(35), fill=(255, 255, 255))

    # BANNED CHAMPIONS
    championInfo = getChampionInformation()
    imageSize = 80
    turns = 1
    row = 0
    for banned in match.bannedChampions:
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
    imageArena_jpg.save(filePath, quality=50)
    print("[INFO] Done with match Image!")
    return filePath


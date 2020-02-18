# bot.py
import os
import json
import requests

import discord
from dotenv import load_dotenv
from gameInfoMain import getMatchInfo, getSummonerInfo, getSummonerID

# GetToken
infoFile = open('infoFile.txt', 'r')
textFileContent = infoFile.read().split(',')
token = textFileContent[0]
print("Token: " + token)

GUILD = "BotTestingGround"

load_dotenv()
client = discord.Client()


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if "lol" == message.content.lower():
        await message.channel.send('lol sux')
    if "su:" in message.content.lower():
        summonerName = message.content.split("su:", 1)[1]
        summonerInfo = getSummonerInfo(summonerName)
        if summonerInfo == "NO SUMMONER FOUND":  # TEST IF SUMMONER EXISTS
            await message.channel.send("Summoner does not exist!")
            return
        returnText = "Summonername: {}\n" \
                     "Level: {}".format(summonerInfo["name"], summonerInfo["summonerLevel"])
        await message.channel.send(returnText)

    if "ig:" in message.content.lower():
        summonerName = message.content.split("ig:", 1)[1]
        summonerInfo = getSummonerInfo(summonerName)
        if summonerInfo == "NO SUMMONER FOUND":  # TEST IF SUMMONER EXISTS
            await message.channel.send("Summoner does not exist!")
            return
        matchInfo = getMatchInfo(summonerName)
        if matchInfo == "SUMMONER IS NOT INGAME":  # TEST IF SUMMONER IS INGAME
            await message.channel.send("This summoner is not ingame right now...")
            return
        returnText = getMatchReturnText(matchInfo)
        await message.channel.send(returnText)


def getMatchReturnText(matchInfo):
    summonerList = []

    for nr in range(10):
        summonerList.append(matchInfo["participants"][nr - 1])

    returnText = ""
    for summoner in range(11):
        if summoner == 1:
            returnText = "```# TEAM 1 \n"
        elif summoner == 6:
            returnText += "# TEAM 2 \n"

        returnText += "Summonername: {} | Champion: {} | SP: {} and {}\n".format(
            summonerList[summoner - 1]["summonerName"], summonerList[summoner - 1]["championId"],
            summonerList[summoner - 1]["spell1Id"], summonerList[summoner - 1]["spell2Id"])

    returnText += "```"

    return returnText


client.run(token)

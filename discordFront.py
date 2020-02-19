# bot.py
import os
import json
import requests

import re
import discord
from dotenv import load_dotenv
from gameInfoMain import getSummonerInfo, getMatchInfo

# GetToken
infoFile = open('infoFile.txt', 'r')
textFileContent = infoFile.read().split(',')
token = textFileContent[0]
print("Token: " + token)

load_dotenv()
client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if "lol" == message.content.lower():
        await message.channel.send('lol sux')
    if "su:" in message.content.lower():
        returnText = getSummonerInfo(message)
        await message.channel.send(returnText)

    if "ig:" in message.content.lower():
        returnText = getMatchInfo(message)
        await message.channel.send(returnText)

    if "test:" in message.content.lower():
        summonerName = message.content.split("test:", 1)[1]

        await message.channel.send()




client.run(token)

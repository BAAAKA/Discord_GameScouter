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
        if isinstance(returnText, str):
            await message.channel.send(returnText)
            return
        await message.channel.send(embed=returnText)

    if "ig:" in message.content.lower():
        returnText = getMatchInfo(message)
        await message.channel.send(returnText)
    if "test:" in message.content.lower():
        await message.channel.send(embed="")



client.run(token)


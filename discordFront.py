import discord
from dotenv import load_dotenv
import os
from gameInfoMain import getSummonerInfo, getMatchInfo, getHelpText, getInfoText

iboisChannelID = 594973116019638515
botTestingID = 649304929613250560
myServerID = 682327435370430567
DnDServer = 687363534740258849

channelID = []
if os.name == "nt":
    channelID.append(botTestingID)
else:
    channelID.append(iboisChannelID)
    channelID.append(myServerID)
    channelID.append(DnDServer)

# GetToken
token = os.environ['discordToken']
print("Token: {}".format(token))

load_dotenv()
client = discord.Client()

@client.event
async def on_message(message):
    if message.channel.id in channelID:
        if message.author == client.user:
            return
        if "lol:" == message.content.lower():
            await message.channel.send('rito sux')
        if "su:" in message.content.lower():
            returnText = getSummonerInfo(message)
            image = discord.File(returnText[1], filename="matchImage.png")  # FIX THIS
            if isinstance(returnText, str):
                await message.channel.send(returnText)
                return
            await message.channel.send(set_thumbnail=image, embed=returnText[0])

        if "ig:" in message.content.lower():
            loadingMessage = await message.channel.send("processing your request...")
            loadingMessageFetched = await message.channel.fetch_message(loadingMessage.id)
            returnText = getMatchInfo(message)
            if isinstance(returnText, str):
                await message.channel.send(returnText)
                await loadingMessageFetched.delete()
                return
            image = discord.File(returnText[1], filename="matchImage.png")
            await message.channel.send(file=image, embed=returnText[0])
            await loadingMessageFetched.delete()


        if "help:" in message.content.lower():
            await message.channel.send(embed=getHelpText())

        if "info:" in message.content.lower():
            await message.channel.send(embed=getInfoText())

        if "test:" in message.content.lower():
            await message.channel.send(embed="")

client.run(token)

    
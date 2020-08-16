import discord
from dotenv import load_dotenv
import os
from gameInfoMain import getSummonerInfo, getMatchInfo, getHelpText, getInfoText, setSummonername, getMyGame, getMySummoner

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

activity = discord.Game(name="doing something", type=3)

@client.event
async def on_ready():
    activity = discord.Game(name="catch with wolf!", type=3)
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("[INFO] leagueScouter is ready!")

@client.event
async def on_message(message):
    if message.channel.id in channelID:
        if message.author == client.user:
            return

        if "lol:" == message.content.lower():
            await message.channel.send('rito sux')
        if "su:" in message.content.lower():
            returnText = getSummonerInfo(message)
            if isinstance(returnText, str):
                await message.channel.send(returnText)
                return
            image = discord.File(returnText[1], filename="championImage.png")
            await message.channel.send(file=image, embed=returnText[0])

        if "ig:" in message.content.lower():
            loadingMessage = await message.channel.send("processing your request...")
            loadingMessageFetched = await message.channel.fetch_message(loadingMessage.id)
            returnText = getMatchInfo(message)
            if isinstance(returnText, str):
                await message.channel.send(returnText)
                await loadingMessageFetched.delete()
                return
            image = discord.File(returnText[1], filename="matchImage.jpg")
            await message.channel.send(file=image, embed=returnText[0])
            await loadingMessageFetched.delete()

        if "setname:" in message.content.lower():
            returnText = setSummonername(message)
            await message.channel.send(returnText)

        if "help" == message.content.lower():
            await message.channel.send(embed=getHelpText())

        if "info" == message.content.lower():
            await message.channel.send(embed=getInfoText())

        if "test:" in message.content.lower():
            await message.channel.send(embed="")

        if "mgame" in message.content.lower():
            loadingMessage = await message.channel.send("processing your request...")
            loadingMessageFetched = await message.channel.fetch_message(loadingMessage.id)
            returnText = getMyGame(message)
            if isinstance(returnText, str):
                await message.channel.send(returnText)
                await loadingMessageFetched.delete()
                return
            image = discord.File(returnText[1], filename="matchImage.png")
            await message.channel.send(file=image, embed=returnText[0])
            await loadingMessageFetched.delete()


        if "msum" in message.content.lower() or "macc" in message.content.lower():
            returnText = getMySummoner(message)
            if isinstance(returnText, str):
                await message.channel.send(returnText)
                return
            await message.channel.send(embed=returnText)
        if "for perl" in message.content.lower():
            await message.channel.send('For Perl!')

        if "tophat is toxic" in message.content.lower():
            await message.channel.send('Yes he is!')

        if "windows" == message.content.lower():
            await message.channel.send('LINUX!')


client.run(token)


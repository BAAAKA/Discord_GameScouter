import discord
import os
from gameInfoMain import getSummonerInfo, getMatchInfo, getHelpText, getInfoText


# GetToken
token = os.environ['discordToken']
print("Token: {}".format(token))

client = discord.Client()

activity = discord.Game(name="doing something", type=3)

@client.event
async def on_ready():
    activity_wolf = discord.Game(name="catch with wolf!", type=3)
    await client.change_presence(status=discord.Status.online, activity=activity_wolf)
    print("[INFO] leagueScouter is ready!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower().startswith("su:"):
        returnText = getSummonerInfo(message)
        if isinstance(returnText, str):
            await message.channel.send(returnText)
            return
        image = discord.File(returnText[1], filename="championImage.jpg")
        await message.channel.send(file=image, embed=returnText[0])

    if message.content.lower().startswith("game:"):
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

    if "help:" == message.content.lower():
        await message.channel.send(embed=getHelpText())

    if "info:" == message.content.lower():
        await message.channel.send(embed=getInfoText())

client.run(token)


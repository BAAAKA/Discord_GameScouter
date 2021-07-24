import pymysql

connection = pymysql.connect(
    '192.168.0.202',
    'leagueScouter',
    'leagueScouter',
    'leagueScouter',
)
cur = connection.cursor()

def input(discordID, summonerName):
    print("[INFO DB] Inputing {} and {}".format(discordID, summonerName))
    cur.execute("INSERT INTO summoner(DiscordID, SummonerName) VALUES ('{}', '{}')".format(discordID, summonerName))
    connection.commit()

def read(discordID):
    print("[INFO DB] Reading SummonerName for DiscordID {}".format(discordID))
    cur.execute("SELECT SummonerName FROM summoner where DiscordID = '{}' limit 1".format(discordID))
    result = cur.fetchone()
    if isinstance(result, type(None)):
        print("[INFO DB] Its empty, returning None")
        return None
    else:
        print("[INFO DB] Returning {}".format(result[0]))
        return result[0]

def exists(discordID):
    print("[INFO DB] Test if `{}` exists".format(discordID))
    cur.execute("SELECT DiscordID FROM summoner where DiscordID = '{}'".format(discordID))
    result = cur.fetchone()
    if isinstance(result, type(None)):
        print("[INFO DB] found nothing in the DB, returning False")
        return False
    else:
        print("[INFO DB] found DiscordID in DB, returning True")
        return True

def updating(discordID, summonerName):
    print("[INFO DB] updating {} with {}".format(discordID, summonerName))
    cur.execute("Update summoner SET SummonerName = '{}' where DiscordID = '{}'".format(summonerName, discordID))
    connection.commit()


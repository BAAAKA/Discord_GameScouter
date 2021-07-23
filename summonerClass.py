

class summoner:
    def __init__(self, name):
        self.name = name

    def setSummonerInfo(self, summonerInfo):
        self.summonerInfo = summonerInfo
        self.id = summonerInfo["id"]
        self.accountID = summonerInfo["accountId"]
        self.puuid = summonerInfo["puuid"]
        self.profileIconId = summonerInfo["profileIconId"]
        self.revisionDate = summonerInfo["revisionDate"]
        self.summonerLevel = summonerInfo["summonerLevel"]




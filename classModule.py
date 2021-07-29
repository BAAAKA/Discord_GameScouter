import operator

class summoner:
    def __init__(self, name):
        self.name = name
        self.lane = "none"
        self.tier = "Unranked"
        self.rankTier = "Unranked"
        self.rank = "-"
        self.wins = 0
        self.losses = 0
        self.Frank = None
        self.mastery1 = None
        self.mastery2 = None
        self.mastery3 = None
        self.mainChamp = None
        self.mainChamp1 = None
        self.mainChamp2 = None
        self.winrate = None

    def setSummonerInfo(self, summonerInfo):
        self.summonerInfo = summonerInfo
        self.id = summonerInfo["id"]
        self.accountID = summonerInfo["accountId"]
        self.puuid = summonerInfo["puuid"]
        self.profileIconId = summonerInfo["profileIconId"]
        self.revisionDate = summonerInfo["revisionDate"]
        self.summonerLevel = summonerInfo["summonerLevel"]

    def setRankInfo(self, summonerRank):
        self.leagueId = summonerRank["leagueId"]
        self.queueType = summonerRank["queueType"]
        self.tier = summonerRank["tier"]
        self.rank = summonerRank["rank"]
        self.leaguePoints = summonerRank["leaguePoints"]
        self.wins = summonerRank["wins"]
        self.losses = summonerRank["losses"]
        self.veteran = summonerRank["veteran"]
        self.inactive = summonerRank["inactive"]
        self.freshBlood = summonerRank["freshBlood"]
        self.hotStreak = summonerRank["hotStreak"]
        self.rankTier = self.tier + " " + self.rank
        self.winrate = self.getWinrate(self.wins, self.losses)

    def setFlexRankInfo(self, summonerRank):
        self.FleagueId = summonerRank["leagueId"]
        self.FqueueType = summonerRank["queueType"]
        self.Ftier = summonerRank["tier"]
        self.Frank = summonerRank["rank"]
        self.FleaguePoints = summonerRank["leaguePoints"]
        self.Fwins = summonerRank["wins"]
        self.Flosses = summonerRank["losses"]
        self.Fveteran = summonerRank["veteran"]
        self.Finactive = summonerRank["inactive"]
        self.FfreshBlood = summonerRank["freshBlood"]
        self.FhotStreak = summonerRank["hotStreak"]
        self.FrankTier = self.Ftier + " " + self.Frank
        self.Fwinrate = self.getWinrate(self.Fwins, self.Flosses)

    def setMasteryInfo(self, masteryInfo):
        if len(masteryInfo)>=1:
            self.mastery1 = masteryInfo[0]
        if len(masteryInfo)>=2:
            self.mastery2 = masteryInfo[1]
        if len(masteryInfo)>=3:
            self.mastery3 = masteryInfo[2]


    def getWinrate(self, wins, losses):
        totalGames = wins + losses
        winrate = str(round(wins / totalGames * 100))
        return winrate

    def getLanePlayCount(self):
        laneCount = {}
        try:
            self.matchList["matches"]
        except:
            print("[ERROR] No <matches> found, self.matchList (Has it not been set yet?): {}".format(self.matchList))
        for match in self.matchList["matches"]:
            lane = match["lane"]
            if lane == "BOTTOM":
                lane = match["role"]
            if lane not in laneCount:
                laneCount[lane] = 0
            laneCount[lane] += 1
        return laneCount

    def getChampionPlayCount(self):
        if hasattr(self, "championCount"):
            return self.championCount
        else:
            championCount = {}
            for match in self.matchList["matches"]:
                champion = match["champion"]
                if champion not in championCount:
                    championCount[champion] = 0
                championCount[champion] += 1
            self.championCount = championCount
            return championCount

    def getMostPlayedLane(self):
        try:
            laneCount = self.getLanePlayCount()
            mostplayed = max(laneCount.items(), key=operator.itemgetter(1))[0]
            return mostplayed
        except:
            return "---"

    def getMostPlayedChamp(self, nr):
        try:
            championCount = self.getChampionPlayCount()
            sortedChampionCount = sorted(championCount.items(), key=lambda x:x[1], reverse=True)
            return sortedChampionCount[nr-1]
        except Exception as e:
            print("[ERROR] Sorting getMostPlayedChamp: {}".format(e))
            return "---"

class match:
    def __init__(self, matchInfo):
        self.matchInfo = matchInfo
        self.gameId = matchInfo["gameId"]
        self.mapId = matchInfo["mapId"]
        self.gameMode = matchInfo["gameMode"]
        self.gameType = matchInfo["gameType"]
        self.gameQueueConfigId = matchInfo["gameQueueConfigId"]
        self.participants =  matchInfo["participants"]
        self.bannedChampions = matchInfo["bannedChampions"]
        self.players = []
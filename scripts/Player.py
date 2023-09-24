from mwrogue.esports_client import EsportsClient
site = EsportsClient("lol")

# Player class that contains all the information about a player (gamplay, team, etc.)
class Player:
    def __init__(self, playerName = '', teamName = '', dateJoined = '', roles = ''):
        self.playerName = playerName
        self.teamName = teamName
        self.dateJoined = dateJoined
        self.roles = roles
        
        # High level stats to check on based on split (Kills, Deaths, Assists, KDA, etc.)
        #TODO: Add most played champs that split as a list and eventually utilize the champ icons with the following: https://github.com/RheingoldRiver/leaguepedia_util/blob/master/champion_sprite.py
        self.stats = {"LCS 2023 Summer": {},
                      "LCS 2023 Spring": {},
                      "LCS 2022 Summer": {},
                      "LCS 2022 Spring": {},
                      "LCS 2021 Summer": {},
                      "LCS 2021 Spring": {},
                      "LCS 2020 Summer": {},
                      "LCS 2020 Spring": {},
                      "LCS 2019 Summer": {},
                      "LCS 2019 Spring": {},
                      "LCS 2018 Summer": {},
                      "LCS 2018 Spring": {},
                      "LCS 2017 Summer": {},
                      "LCS 2017 Spring": {},
                      "LCS 2016 Summer": {},
                      "LCS 2016 Spring": {},
                      "LCS 2015 Summer": {},
                      "LCS 2015 Spring": {},
                      }
        
    def __str__(self):
        return self.playerName + " joined " + self.teamName + " on " + self.dateJoined + " as " + self.roles
    
    # Getter functions
    def getName(self):
        return self.playerName
    
    def getTeam(self):
        return self.teamName
    
    def getDateJoined(self):
        return self.dateJoined
    
    def getRoles(self):
        return self.roles
    
    def getRole(self):
        return self.roles.split(',')[0]
    
    def getKillsInSplit(self, tournament):
        totalKills = 0
        
        response = site.cargo_client.query(
            tables="ScoreboardPlayers=SP, Tournaments=T",
            fields="SP.Kills",
            where=f"SP.Link = '{self.playerName}' AND T.StandardName = '{tournament}'",
            join_on="SP.OverviewPage=T.OverviewPage"
        )
        
        output = [dict(item) for item in response]
        for kill in output:
            totalKills += int(kill['Kills'])
        
        self.stats[tournament]['Kills'] = totalKills
        return totalKills
    
    def getDeathsInSplit(self, tournament):
        totalDeaths = 0
        
        response = site.cargo_client.query(
            tables="ScoreboardPlayers=SP, Tournaments=T",
            fields="SP.Deaths",
            where=f"SP.Link = '{self.playerName}' AND T.StandardName = '{tournament}'",
            join_on="SP.OverviewPage=T.OverviewPage"
        )
        
        output = [dict(item) for item in response]
        for death in output:
            totalDeaths += int(death['Deaths'])
            
        self.stats[tournament]['Deaths'] = totalDeaths
        return totalDeaths
    
    def getAssistsInSplit(self, tournament):
        totalAssists = 0
        
        response = site.cargo_client.query(
            tables="ScoreboardPlayers=SP, Tournaments=T",
            fields="SP.Assists",
            where=f"SP.Link = '{self.playerName}' AND T.StandardName = '{tournament}'",
            join_on="SP.OverviewPage=T.OverviewPage"
        )
        
        output = [dict(item) for item in response]
        for assist in output:
            totalAssists += int(assist['Assists'])
 
        self.stats[tournament]['Assists'] = totalAssists 
        return totalAssists
    
    def getKDAInSplit(self, tournament):
        self.stats[tournament]['KDA'] = round((self.getKillsInSplit(tournament) + self.getAssistsInSplit(tournament)) / self.getDeathsInSplit(tournament), 2) 
        return round((self.getKillsInSplit(tournament) + self.getAssistsInSplit(tournament)) / self.getDeathsInSplit(tournament), 2)
    
    def getCSPM(self, tournament):
        total_cs = 0
        total_gamelength = 0
        
        cspm_response = site.cargo_client.query(
            tables="ScoreboardPlayers=SP, ScoreboardGames=SG",
            fields="SP.OverviewPage, SP.Link, SG.Team1, SG.Team2, SP.CS, SG.Gamelength_Number",
            where=f"SP.Link = '{self.playerName}' AND SG.Tournament = '{tournament}'",
            join_on="SP.GameId=SG.GameId"
        )
        
        output = [dict(item) for item in cspm_response]
        
        total_cs = sum(int(i['CS']) for i in output)
        
        total_gamelength = sum(round(float(i['Gamelength Number']), 2) for i in output)
            
        self.stats[tournament]['CSPM'] = round(total_cs / total_gamelength, 1)
        
        return round(total_cs / total_gamelength, 1)
        
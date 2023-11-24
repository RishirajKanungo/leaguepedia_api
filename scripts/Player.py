from mwrogue.esports_client import EsportsClient
from collections import defaultdict
site = EsportsClient("lol")

# Player class that contains all the information about a player (gamplay, team, etc.)
class Player:
    def __init__(self, playerName = ''):
        self.playerName = playerName
        
        # High level stats to check on based on split (Kills, Deaths, Assists, KDA, etc.)
        #TODO: Add most played champs that split as a list and eventually utilize the champ icons with the following: https://github.com/RheingoldRiver/leaguepedia_util/blob/master/champion_sprite.py
        self.stats = {"LCS 2023 Summer": {},
                      "LCS 2023 Summer": {},
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
        self.best_stats =  {"LCS 2023 Summer": {},
                            "LCS 2023 Summer": {},
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
        
    def getChampsPlayed(self, tournament):
        champs_played_response = site.cargo_client.query(
            tables="ScoreboardPlayers=SP, ScoreboardGames=SG",
            fields="SP.Champion",
            where=f"SP.Link = '{self.playerName}' AND SG.Tournament = '{tournament}'",
            join_on="SP.GameId=SG.GameId"
        )
        
        champs_played_dict = [dict(item) for item in champs_played_response]
        
        # Initialize a defaultdict to count the occurrences of names
        name_count = defaultdict(int)

        # Iterate through the list of dictionaries and update the counts
        for item in champs_played_dict:
            name = item['Champion']
            name_count[name] += 1

        # Convert the defaultdict to a regular dictionary if needed
        name_count_dict = dict(name_count)

        self.stats[tournament]['ChampionsPlayed'] = name_count_dict
        
        return name_count_dict
    
    def getWinRate(self, tournament):
        wins = 0
        losses = 0
        
        winrate_response = site.cargo_client.query(
            tables="ScoreboardPlayers=SP, ScoreboardGames=SG",
            fields="SP.PlayerWin",
            where=f"SP.Link = '{self.playerName}' AND SG.Tournament = '{tournament}'",
            join_on="SP.GameId=SG.GameId"
        )
        
        winrate_dict = [dict(item) for item in winrate_response]
        
        for game in winrate_dict:
            if game['PlayerWin'] == 'Yes':
                wins += 1
            else:
                losses += 1
        
        self.stats[tournament]['WinRate'] = round(wins / (wins + losses), 3)
        
        return round(wins / (wins + losses), 3)
    
    def getDPM(self, tournament):
        total_dmg = 0
        total_gamelength = 0
        
        dpm_response = site.cargo_client.query(
            tables="ScoreboardPlayers=SP, ScoreboardGames=SG",
            fields="SP.DamageToChampions, SG.Gamelength_Number",
            where=f"SP.Link = '{self.playerName}' AND SG.Tournament = '{tournament}'",
            join_on="SP.GameId=SG.GameId"
        )
        
        output = [dict(item) for item in dpm_response]
        
        total_dmg = sum(int(i['DamageToChampions']) for i in output)
        
        total_gamelength = sum(round(float(i['Gamelength Number']), 3) for i in output)

        # total_gamelength = sum(float(i['Gamelength Number']) for i in output)
            
        self.stats[tournament]['DPM'] = round(total_dmg / total_gamelength, 1)
        
        return round(total_dmg / total_gamelength, 1)
    
    def getGoldPercentage(self, tournament):
        total_gold = 0
        total_team_gold = 0
        
        # Get player's gold and team's gold
        gold_response = site.cargo_client.query(
            tables="ScoreboardPlayers=SP, ScoreboardGames=SG",
            fields="SP.Gold, SP.TeamGold",
            where=f"SP.Link = '{self.playerName}' AND SG.Tournament = '{tournament}'",
            join_on="SP.GameId=SG.GameId"
        )
        
        output = [dict(item) for item in gold_response]
        
        total_gold = sum(int(i['Gold']) for i in output)
        total_team_gold = sum(int(i['TeamGold']) for i in output)
        
            
        self.stats[tournament]['GoldPercentage'] = round(total_gold / total_team_gold, 3)
        
        return round(total_gold / total_team_gold, 3)
    
    def getDamangePercentage(self, tournament):
        # Initial attempt to try and get damage percentage
        # Other method requires to pull the JSON data from the postgame stats
        player_dmg = 0
        team_dmg = 0
        
        # get player's team
        player_team = site.cargo_client.query(
            limit=1,
            tables="ScoreboardPlayers=SP, ScoreboardGames=SG",
            fields="SP.Team",
            where=f"SP.Link = '{self.playerName}' AND SG.Tournament = '{tournament}'",
            join_on="SP.GameId=SG.GameId"
        )
        
        player_team_dict = [dict(item) for item in player_team]
        player_team = player_team_dict[0]['Team']
        
        # get player's dmg
        player_dmg_response = site.cargo_client.query(
            tables="ScoreboardPlayers=SP, ScoreboardGames=SG",
            fields="SP.DamageToChampions, SP.Team, SG.Team1, SG.Team2, SG.GameId",
            where=f"SP.Link = '{self.playerName}' AND SG.Tournament = '{tournament}'",
            join_on="SP.GameId=SG.GameId"
        )
        
        # get player's team dmg
        team_dmg_response = site.cargo_client.query(
            tables="ScoreboardPlayers=SP, ScoreboardGames=SG",
            fields="SP.DamageToChampions, SP.Team, SG.Team1, SG.Team2, SG.GameId",
            where=f"SP.Link = '{self.playerName}' AND SG.Tournament = '{tournament}'",
            join_on="SP.GameId=SG.GameId"
        )
        
        
    def getBestKDA(self, tournament):
        # Get the best KDA for the player in a given split
        return
    
    def getBestDPM(self, tournament):
        # Get the best DPM for the player in a given split
        return
    
    def getBestCSPM(self, tournament):
        # Get the best CSPM for the player in a given split
        return
    
    def getBestCSD15(self, tournament):
        # Get the best CSD15 for the player in a given split
        return
    
    
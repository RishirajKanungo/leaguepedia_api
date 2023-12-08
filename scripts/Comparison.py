from mwrogue.esports_client import EsportsClient
from collections import defaultdict
site = EsportsClient("lol")
import sys
sys.path.insert(0, '/Users/rishirajkanungo/Documents/GitHub/leaguepedia_api/') # add path to import a player
from scripts.Player import Player

# Comparison class made to generate the data for other players
# of a given role to compare to the player of interest
class Comparison:
    def __init__(self, playerOfInterest, tournament):
        # set param values as attributes
        self.playerOfInterest = playerOfInterest
        self.tournament = tournament
        
        # set empty dicts for stats
        self.non_poi = {}
        self.non_poi_stats_kda = {}
        self.non_poi_stats_cspm = {}
        self.non_poi_stats_kills = {}
        self.non_poi_stats_deaths = {}
        self.non_poi_stats_assists = {}
        self.non_poi_stats_dpm = {}
        self.non_poi_stats_gold_percentage = {}
        self.non_poi_stats_winrate = {}
        self.non_poi_stats_champs_played = {}
        
        # populate dicts
        self.getOtherPlayers()
        self.comparitiveKDAs()
        self.compartiveKills()
        self.compartiveDeaths()
        self.compartiveAssists()
        self.compartiveCSPM()
        self.compartiveDPM()
        self.compartiveGoldPercentage()
        self.compartiveWinRate()
        self.compartiveChampsPlayed()
    
    # Return a list of players and their KDA in a given split
    def comparitiveKDAs(self):
        for player in self.non_poi:
            player_instance = Player(player['Link'])
            kda = player_instance.getKDAInSplit(self.tournament)
            self.non_poi_stats_kda[player['Link']] = kda
    
    def compartiveCSPM(self):
        for player in self.non_poi:
            player_instance = Player(player['Link'])
            cspm = player_instance.getCSPM(self.tournament)
            self.non_poi_stats_cspm[player['Link']] = cspm
    
    def compartiveKills(self):
        for player in self.non_poi:
            player_instance = Player(player['Link'])
            kills = player_instance.getKillsInSplit(self.tournament)
            self.non_poi_stats_kills[player['Link']] = kills
    
    def compartiveDeaths(self):
        for player in self.non_poi:
            player_instance = Player(player['Link'])
            deaths = player_instance.getDeathsInSplit(self.tournament)
            self.non_poi_stats_deaths[player['Link']] = deaths
    
    def compartiveAssists(self):
        for player in self.non_poi:
            player_instance = Player(player['Link'])
            assists = player_instance.getAssistsInSplit(self.tournament)
            self.non_poi_stats_assists[player['Link']] = assists
    
    def compartiveDPM(self):
        for player in self.non_poi:
            player_instance = Player(player['Link'])
            dpm = player_instance.getDPM(self.tournament)
            self.non_poi_stats_dpm[player['Link']] = dpm
    
    def compartiveGoldPercentage(self):
        for player in self.non_poi:
            player_instance = Player(player['Link'])
            gold_percentage = player_instance.getGoldPercentage(self.tournament)
            self.non_poi_stats_gold_percentage[player['Link']] = gold_percentage

    def compartiveWinRate(self):
        for player in self.non_poi:
            player_instance = Player(player['Link'])
            winrate = player_instance.getWinRate(self.tournament)
            self.non_poi_stats_winrate[player['Link']] = winrate
    
    def compartiveChampsPlayed(self):
        for player in self.non_poi:
            player_instance = Player(player['Link'])
            champs_played = player_instance.getChampsPlayed(self.tournament)
            self.non_poi_stats_champs_played[player['Link']] = champs_played
    
    def getOtherPlayers(self):
        
        # Get role of POI
        response = site.cargo_client.query(
            tables="ScoreboardPlayers=SP, Tournaments=T",
            fields="SP.Role",
            where=f"SP.Link = '{self.playerOfInterest}' AND T.StandardName = '{self.tournament}'",
            join_on="SP.OverviewPage=T.OverviewPage",
            limit=1
        )
        
        role = response[0]['Role']
        
        # Get list of players that are not POI
        response = site.cargo_client.query(
            tables="Tournaments=T, TournamentPlayers=TP",
            fields="TP.Link, TP.Team", # get the name and the team the non POI is apart of
            where=f"TP.Link != '{self.playerOfInterest}' AND T.StandardName = '{self.tournament}' AND TP.Role='{role}'",
            join_on="TP.OverviewPage=T.OverviewPage"
        )
        
        non_poi = [dict(item) for item in response]
        
        self.non_poi = non_poi # update the non_poi dictionary with the non_poi list
        

# prelim test cases to see if setup works
not_doublelift = Comparison('Doublelift', 'LCS 2023 Summer')
not_doublelift
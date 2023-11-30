from mwrogue.esports_client import EsportsClient
from collections import defaultdict
site = EsportsClient("lol")
import sys
sys.path.insert(0, '/Users/rishirajkanungo/Documents/GitHub/leaguepedia_api/') # add path to import a player
from scripts.Player import Player

# Comparison class made to generate the data for other players
# of a given role to compare to the player of interest
class Comparison:
    def __init__(self, playerOfInterest, roleToCompare, tournament):
        self.playerOfInterest = playerOfInterest
        self.roleToCompare = roleToCompare
        self.tournament = tournament

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    def __str__(self):
        return "Comparison: a = " + str(self.a) + ", b = " + str(self.b)
    
    # Return a list of players and their KDA in a given split
    def comparitiveKDAs(self):
        # Get list of all players in a given role that is not POI
        response = site.cargo_client.query(
            tables="ScoreboardPlayers=SP, Tournaments=T",
            fields="SP.Kills",
            where=f"SP.Link != '{self.playerOfInterest}' AND T.StandardName = '{self.tournament}'",
            join_on="SP.OverviewPage=T.OverviewPage"
        )
        return response
        
from Positions import Positions
from Player import Player

class Team:
    def __init__(self, teamName):
        self.teamName = teamName
        self.players = []
    
    def __str__(self):
        return self.teamName + " has " + str(len(self.players)) + " players"
    
    def addExistingPlayers(self):
        
        roles = ['Top', 'Jungle', 'Mid', 'Bot', 'Support']
        
        from mwrogue.esports_client import EsportsClient
        from Positions import Positions
        site = EsportsClient("lol")
        import pprint
        
        # get current players
        response = site.cargo_client.query(
            tables="Tenures=T, RosterChanges=RC",
            fields="T.Player, T.Team, T.DateJoin, RC.Roles",
            where="T.Team = '" + self.teamName + "' AND T.DateLeave IS NULL",
            join_on="T.RosterChangeIdJoin=RC.RosterChangeId",
            group_by="T.Player"
        )
        
        output = [dict(item) for item in response]
        
        # add players that are playing (not content creators or coaches)
        for player in output:
            if player['Roles'] in roles:
                self.addPlayer(player)
            else:
                continue
    
    def addPlayer(self, player):
        player_to_add = Player(player['Player'], player['Team'], player['DateJoin'], player['Roles'])
        self.players.append(player_to_add)
        
    def getPlayers(self):
        return self.players
from mwrogue.esports_client import EsportsClient
from Positions import Positions
from Team import Team
from Player import Player
import pprint

site = EsportsClient("lol")

player_name = 'Doublelift'
tournament = "LCS 2023 Summer"

# Current query to get kills in a split for Doublelift
response = site.cargo_client.query(
            tables="ScoreboardPlayers=SP, Tournaments=T",
            fields="SP.Kills",
            where=f"SP.Link = '{player_name}' AND T.StandardName = '{tournament}'",
            join_on="SP.OverviewPage=T.OverviewPage"
        )

# Get list of players that are not POI
# response = site.cargo_client.query(
#     tables="ScoreboardPlayers=SP, Tournaments=T, TournamentPlayers=TP",
#     fields="SP.Link, SP.Team", # get the name and the team the non POI is apart of
#     where=f"TP.Link != '{player_name}' AND T.StandardName = '{tournament}'",
#     # join_on="SP.OverviewPage=T.OverviewPage"
# )

response = site.cargo_client.query(
    tables="Tournaments=T, TournamentPlayers=TP",
    fields="TP.Link, TP.Team", # get the name and the team the non POI is apart of
    where=f"TP.Link != '{player_name}' AND T.StandardName = '{tournament}' AND TP.Role='Bot'",
    join_on="TP.OverviewPage=T.OverviewPage"
)

response
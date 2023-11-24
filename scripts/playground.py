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


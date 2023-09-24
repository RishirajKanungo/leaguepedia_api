from mwrogue.esports_client import EsportsClient
from Positions import Positions
from Team import Team
from Player import Player
import pprint


site = EsportsClient("lol")

# response = site.cargo_client.query(
#     tables="Tenures=T, RosterChanges=RC",
#     fields="T.Player, T.Team, T.DateJoin, RC.Roles",
#     where="T.Team = 'Team Liquid' AND T.DateLeave IS NULL",
#     join_on="T.RosterChangeIdJoin=RC.RosterChangeId",
#     group_by="T.Player"
# )

player_name = 'Doublelift'
tournament = "LCS 2023 Summer"

response = site.cargo_client.query(
    tables="ScoreboardPlayers=SP, Tournaments=T",
    fields="SP.Kills, SP.Deaths, SP.Assists, SP.Gold",
    where=f"SP.Link = '{player_name}' AND T.StandardName = '{tournament}'",
    join_on="SP.OverviewPage=T.OverviewPage"
)

# cspm_response = site.cargo_client.query(
#     tables="ScoreboardPlayers=SP, ScoreboardGames=SG",
#     fields="SP.OverviewPage, SP.Link, SG.Team1, SG.Team2, SP.CS, SG.Gamelength_Number",
#     where=f"SP.Link = '{player_name}' AND SG.Tournament = '{tournament}'",
#     join_on="SP.GameId=SG.GameId"
# )

doublelift = Player(player_name)
doublelift.getCSPM(tournament)
# pprint.pprint(cspm_response)
# output = [dict(item) for item in cspm_response]
# print(output)

# pprint.pprint(response)

'''
team_liquid = Team("Team Liquid")
team_liquid.addExistingPlayers()
team_liquid.getPlayers()
'''

# response = site.cargo_client.query(
# 	limit= "max",
# 	tables= "MatchScheduleGame=MSG, MatchSchedule=MS",
# 	fields= "RiotPlatformGameId, Blue, Red",
# 	where= "MSG.OverviewPage='LCS/2021 Season/Championship'",
# 	join_on= "MSG.MatchId=MS.MatchId",
# 	order_by= "MS.DateTime_UTC ASC"
# )
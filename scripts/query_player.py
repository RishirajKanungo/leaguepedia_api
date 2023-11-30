from mwrogue.esports_client import EsportsClient
from Positions import Positions
from Team import Team
from Player import Player
from Comparison import Comparison
import pprint


site = EsportsClient("lol")

player_name = 'Doublelift'
tournament = "LCS 2023 Summer"

# cspm_response = site.cargo_client.query(
#     tables="ScoreboardPlayers=SP, ScoreboardGames=SG",
#     fields="SP.OverviewPage, SP.Link, SG.Team1, SG.Team2, SP.CS, SG.Gamelength_Number",
#     where=f"SP.Link = '{player_name}' AND SG.Tournament = '{tournament}'",
#     join_on="SP.GameId=SG.GameId"
# )

# doublelift = Player(player_name)
# doublelift.getKDAInSplit(tournament)
# doublelift.getCSPM(tournament)
# doublelift.getChampsPlayed(tournament)
# doublelift.getWinRate(tournament)
# doublelift.getDPM(tournament)
# doublelift.getGoldPercentage(tournament)
# pprint.pprint(doublelift.stats)

# player_team = site.cargo_client.query(
#             limit=1,
#             tables="ScoreboardPlayers=SP, ScoreboardGames=SG",
#             fields="SP.Team",
#             where=f"SP.Link = '{player_name}' AND SG.Tournament = '{tournament}'",
#             join_on="SP.GameId=SG.GameId"
#         )

# teamName = [dict(item) for item in player_team]

# pprint.pprint(player_team)

# data, timeline = site.get_data_and_timeline("1926164473", version=4)
# data, timeline = site.get_data_and_timeline_from_gameid('Gamers Club Rift/Season 1_Quarterfinals_2_1')

try:
  data, timeline = site.get_data_and_timeline("ESPORTSTMNT02_3231936", version=5) # try to get V5 data, returns two values, the data and timeline json
except KeyError:
  data, timeline = site.get_data_and_timeline("ESPORTSTMNT02_3231936", version=4) # if it fails try getting V4 data

data
timeline


# Query for a matchup
matchup_response = site.cargo_client.query(
    tables="ScoreboardPlayers=SP, ScoreboardPlayers=SPVs",
    join_on="SP.UniqueRoleVs=SPVs.UniqueRole",
    fields="SP.Link, SPVs.Link=LinkVs, SP.Champion, SPVs.Champion=ChampionVs, SP.GameId",
    where="SP.Champion = 'Diana' AND SPVs.Champion = 'Nocturne'"
)

# Query for most played champions that split
# champs_played_response = site.cargo_client.query(
#     tables="ScoreboardPlayers=SP, ScoreboardGames=SG",
#     fields="SP.Champion",
#     where=f"SP.Link = '{player_name}' AND SG.Tournament = '{tournament}'",
#     join_on="SP.GameId=SG.GameId"
# )

# champs_played = [dict(item) for item in champs_played_response]

not_doublelift = Comparison('Doublelift', 'ADC', 'LCS 2023 Summer')
not_doublelift
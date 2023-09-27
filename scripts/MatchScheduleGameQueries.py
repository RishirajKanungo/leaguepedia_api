'''
Script used to query the wiki for match schedule games and update the database.
'''

from mwrogue.esports_client import EsportsClient
from Positions import Positions
from Team import Team
from Player import Player
import pprint
import json

site = EsportsClient("lol")

team_name = '100 Thieves'
player_name = 'Doublelift'

# Test query to acquire all games/matches that 100 Thieves played in the 2023 Summer Split

# This will provide the proper title for applying the JSON lookup
response = site.cargo_client.query(
    tables="ScoreboardPlayers=SP, MatchScheduleGame=MSG",
    fields="MSG.RiotPlatformGameId",
    where=f"SP.Link = '{player_name}' AND SP.Team = '{team_name}'",
    join_on="SP.GameId=MSG.GameId",
)

output = [dict(item) for item in response]

output # [{'RiotPlatformGameId': 'ESPORTSTMNT02_3231936'}] - this is the proper title for the JSON lookup

rpg = output[0]['RiotPlatformGameId'] # Take the first RPG ID from the list - Dignitas vs 100 Thieves LCS 2023-02-02 (WEEK2)

try:
  data_json, timeline_json = site.get_data_and_timeline(rpg, version=5) # try to get V5 data, returns two values, the data and timeline json
except KeyError:
  data_json, timeline_json = site.get_data_and_timeline(rpg, version=4) # if it fails try getting V4 data
  
data_json # returns the data json
timeline_json # returns the timeline json

data_json_object = json.dumps(data_json, indent=4)
timeline_json_object = json.dumps(timeline_json, indent=4)

with open('scripts/test_json_data/'+rpg+'_data.json', "w") as outfile:
    outfile.write(data_json_object)
    
with open('scripts/test_json_timeline/'+rpg+'_timeline.json', "w") as outfile:
    outfile.write(timeline_json_object)
    
    
    
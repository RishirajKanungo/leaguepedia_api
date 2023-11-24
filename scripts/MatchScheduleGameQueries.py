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

# This will provide the proper title for applying the JSON lookup - Getting all RPG IDs of Doublelift on 100 Thieves
response = site.cargo_client.query(
    tables="ScoreboardPlayers=SP, MatchScheduleGame=MSG",
    fields="MSG.RiotPlatformGameId",
    where=f"SP.Link = '{player_name}' AND SP.Team = '{team_name}'",
    join_on="SP.GameId=MSG.GameId",
)

output = [dict(item) for item in response] # gets all the RPG IDs for the player

output # [{'RiotPlatformGameId': 'ESPORTSTMNT02_3231936'}] - this is the proper title for the JSON lookup

rpg = output[0]['RiotPlatformGameId'] # Take the first RPG ID from the list - Dignitas vs 100 Thieves LCS 2023-02-02 (WEEK2)

try:
  data_json, timeline_json = site.get_data_and_timeline(rpg, version=5) # try to get V5 data, returns two values, the data and timeline json
except KeyError:
  data_json, timeline_json = site.get_data_and_timeline(rpg, version=4) # if it fails try getting V4 data
  
data_json # returns the data json
timeline_json # returns the timeline json

data_json_object = json.dumps(data_json, indent=4) #actually makes it a string
timeline_json_object = json.dumps(timeline_json, indent=4)

# Write the JSON data to a file
with open('scripts/test_json_data/'+rpg+'_data.json', "w") as outfile:
    outfile.write(data_json_object)
    
# Write the timeline JSON data to a file
'''
the timeline should have a list of frames, one per minute in the game, 
each one of those frames has information about player stats (participantFrames) 
which gives you stats corresponding to the point in the game the frame represents, 
so first frame has stats at sec 0, second frame at 60s, third frame at 120s

TLDR:
    Frame of each player = participantFrames
    1 Frame = 1 Minute
     -> Frame 1 = 0 seconds
     -> Frame 2 = 60 seconds
     -> Frame 3 = 120 seconds
'''
with open('scripts/test_json_timeline/'+rpg+'_timeline.json', "w") as outfile:
    outfile.write(timeline_json_object)
    

timeline_json['frames'][0]['participantFrames']['1']['totalGold'] # returns the total gold of the player at 0 seconds
data_json
data_json['teams'][0]['bans'][0]['championId'] # returns the champion ID of the first ban of the first team
data_json['teams'][0]['objectives']

from mwrogue.esports_client import EsportsClient
from Positions import Positions
from Team import Team
from Player import Player
import pprint

import plotly.express as px
from json import dumps
import plotly
import urllib.request


site = EsportsClient("lol")

player_name = 'Doublelift'
tournament = "LCS 2023 Summer"

# Current query to get kills in a split for Doublelift
poi_kills_response = site.cargo_client.query(
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

# x data = player names, y data = kda
def generateBarChart():
    df = px.data.medals_long()
    fig = px.bar(df, x="medal", y="count", color="nation", text_auto=True)
    # data = pd.DataFrame({'Player': x_data, 'KDA': y_data})
    # fig = px.bar(df, x='Player', y='KDA', title='test')
    fig.show()
    return dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def generateKillBarChart():    
    df = px.data.gapminder().query("continent == 'Europe' and year == 2007 and pop > 2.e6")
    fig = px.bar(df, y='pop', x='country', text_auto='.2s',
                title="Default: various text sizes, positions and angles")
    fig.show()

# generateBarChart()

response
poi_kills_response


def get_filename_url_to_open(site: EsportsClient, filename, player, width=None):
    response = site.client.api(
        action="query",
        format="json",
        titles=f"File:{filename}",
        prop="imageinfo",
        iiprop="url",
        iiurlwidth=width,
    )

    image_info = next(iter(response["query"]["pages"].values()))["imageinfo"][0]

    if width:
        url = image_info["thumburl"]
    else:
        url = image_info["url"]

    #In case you would like to save the image in a specific location, you can add the path after 'url,' in the line below.
    urllib.request.urlretrieve(url, player + '.png')


player = "Busio"

site = EsportsClient("lol")
response = site.cargo_client.query(
    limit=1,
    tables="PlayerImages=PI, Tournaments=T",
    fields="PI.FileName",
    join_on="PI.Tournament=T.OverviewPage",
    where='Link="%s"' % player,
    order_by="PI.SortDate DESC, T.DateStart DESC"
)
url = response[0]['FileName']
get_filename_url_to_open(site, url, player)
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import secrets
import sys
import pandas as pd
import urllib.request

import plotly
sys.path.insert(0, '/Users/rishirajkanungo/Documents/GitHub/leaguepedia_api/') # add path to import a player
from scripts.Player import Player
from scripts.Comparison import Comparison

# Below two import for plugging viz into page
import plotly.express as px
from json import dumps

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Set a secure and random secret key

# x data = player names, y data = kda
def generateScatterPlot(x_axis, y_axis):
    # fig = px.bar(data, x=x_axis, y=y_axis, title='Test')
    fig = px.scatter(x=x_axis, y=y_axis, title='Test')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="white",
        font_size=18,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    return dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
# home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/player', methods=['GET', 'POST'])
def player():
    if request.method == 'POST':
        queried_player = request.form['player-search'].capitalize()
        selected_tournament = request.form['tournament']
        
        # Create an instance of the Player class with the provided player name
        player_instance = Player(queried_player)
        non_poi_instance = Comparison(queried_player, selected_tournament)
        
        # temp kda plot data
        non_poi_instance_names = []
        non_poi_instance_kda = []
        
        # temp storage for data
        print('non_poi_kda')
        for k,v in non_poi_instance.non_poi_stats_kda.items():
            print(f"{k}: {v}")
            non_poi_instance_names.append(k)
            non_poi_instance_kda.append(v)
            
        print('non_poi after storing')
        print('non_poi names:', non_poi_instance_names)
        print('non_poi kda:', non_poi_instance_kda)
        
        plot_json = generateBarChart(non_poi_instance_names, non_poi_instance_kda)
        barchat_json = generateBarChart(non_poi_instance_names, non_poi_instance_kda)
        
        # Call the methods of the Player class to get the desired attributes
        kda = player_instance.getKDAInSplit(selected_tournament)
        cspm = player_instance.getCSPM(selected_tournament)
        champs_played = player_instance.getChampsPlayed(selected_tournament)
        winrate = player_instance.getWinRate(selected_tournament) * 100
        gold_percentage = player_instance.getGoldPercentage(selected_tournament) * 100
        dpm = player_instance.getDPM(selected_tournament)

        print(f"Queried Player: {queried_player}")
        print(f"Selected Tournament: {selected_tournament}")

        '''
        print(f"Player: {queried_player}")
        print(f"Tournament: {selected_tournament}")
        print(f"KDA: {kda}")
        print(f"CSPM: {cspm}")
        print(f"Champs Played: {champs_played}")
        print(f"Winrate: {winrate}")
        print(f"Gold Percentage: {gold_percentage}")
        print(f"DPM: {dpm}")

        for champ in champs_played:
            print(champ)
        '''
        
        # return render_template('player.html', queried_player=queried_player, selected_tournament=selected_tournament, kda=kda, cspm=cspm, champs_played=champs_played, winrate=winrate, gold_percentage=gold_percentage, dpm=dpm, non_poi_instance_names=non_poi_instance_names, non_poi_instance_kda=non_poi_instance_kda)
        # return render_template('player.html', queried_player=queried_player, selected_tournament=selected_tournament, kda=kda, cspm=cspm, champs_played=champs_played, winrate=winrate, gold_percentage=gold_percentage, dpm=dpm, plot_json=plot_json)
        print(f"Plot JSON: {plot_json}")
        return render_template('player.html', queried_player=queried_player, selected_tournament=selected_tournament, kda=kda, cspm=cspm, champs_played=champs_played, winrate=winrate, gold_percentage=gold_percentage, dpm=dpm, plot_json=plot_json, barchat_json=barchat_json)


        # return redirect(url_for('player'))
    
    return render_template('player.html')

if __name__ == "__main__":
    
    app.run(host='0.0.0.0', port=8000, debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import secrets
# from Player import Player
import sys
sys.path.insert(0, '/Users/rishirajkanungo/Documents/GitHub/leaguepedia_api/') # add path to import a player
from scripts.Player import Player

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Set a secure and random secret key

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

        # print(player_instance)
        
        # Call the methods of the Player class to get the desired attributes
        kda = player_instance.getKDAInSplit(selected_tournament)
        cspm = player_instance.getCSPM(selected_tournament)
        champs_played = player_instance.getChampsPlayed(selected_tournament)
        winrate = player_instance.getWinRate(selected_tournament) * 100
        gold_percentage = player_instance.getGoldPercentage(selected_tournament) * 100
        dpm = player_instance.getDPM(selected_tournament)

        print(f"Queried Player: {queried_player}")
        print(f"Selected Tournament: {selected_tournament}")

        print(f"Player: {queried_player}")
        print(f"Tournament: {selected_tournament}")
        print(f"KDA: {kda}")
        print(f"CSPM: {cspm}")
        print(f"Champs Played: {champs_played}")
        print(f"Winrate: {winrate}")
        print(f"Gold Percentage: {gold_percentage}")
        print(f"DPM: {dpm}")

        # If you want to redirect to the same page with the entered values, use flash messages
        # flash(f"Queried Player: {queried_player}, Selected Tournament: {selected_tournament}")
        # flash(f"KDA: {kda}, CSPM: {cspm}")
        # flash(f"Champs Played: {champs_played}")
        # flash(f"Winrate: {winrate}")
        # flash(f"Gold Percentage: {gold_percentage}")
        # flash(f"DPM: {dpm}")

        return render_template('player.html', queried_player=queried_player, selected_tournament=selected_tournament, kda=kda, cspm=cspm, champs_played=champs_played, winrate=winrate, gold_percentage=gold_percentage, dpm=dpm)

        # return redirect(url_for('player'))
    
    return render_template('player.html')

if __name__ == "__main__":
    
    app.run(host='0.0.0.0', port=8000, debug=True)
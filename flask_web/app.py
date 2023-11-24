from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
# from Player import Player
import sys
sys.path.insert(0, '/Users/rishirajkanungo/Documents/GitHub/leaguepedia_api/') # add path to import a player
from scripts.Player import Player

app = Flask(__name__)

# home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/player', methods=['GET', 'POST'])
def player():
    if request.method == 'POST':
        queried_player = request.form['player-search']
        selected_tournament = request.form['tournament']

        print(f"Queried Player: {queried_player}")
        print(f"Selected Tournament: {selected_tournament}")

        # If you want to redirect to the same page with the entered values, you can use flash messages
        # flash(f"Queried Player: {queried_player}, Selected Tournament: {selected_tournament}")

        return redirect(url_for('player'))
    
    return render_template('player.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
import os
import random
import time
from flask import Flask, render_template, session, jsonify, request
from sqlalchemy import func
from database import db, init_db, Country, Ranking
from unidecode import unidecode
from thefuzz import fuzz

app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = f"sqlite:///{os.path.join(project_dir, 'paises.db')}"
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SECRET_KEY'] = 'dev_secret_key' # Replace with a real secret key

db.init_app(app)

# Helper function for string normalization
def normalize_string(s):
    return unidecode(s).lower().strip()

@app.cli.command('init-db')
def init_db_command():
    init_db(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    total_countries = db.session.query(func.count(Country.id)).scalar()
    # Prevent picking the same country twice in a row
    last_country_id = session.get('last_country_id', None)
    country = None
    while country is None or country.id == last_country_id:
        random_index = random.randint(0, total_countries - 1)
        country = db.session.get(Country, random_index + 1)

    session['country_id'] = country.id
    session['last_country_id'] = country.id
    session['start_time'] = time.time()
    session['attempts'] = 0
    session['wrong_guesses'] = []
    session['game_over'] = False

    return jsonify({
        'initial_letter': country.initial_letter
    })

@app.route('/guess', methods=['POST'])
def guess():
    data = request.get_json()
    guess_country_name = data.get('guess', '')

    if 'country_id' not in session or session.get('game_over'):
        return jsonify({'error': 'Game not started or already over. Please refresh.'}), 400

    target_country = db.session.get(Country, session['country_id'])

    # Normalize strings for comparison
    normalized_guess = normalize_string(guess_country_name)
    normalized_target = normalize_string(target_country.name)

    # Use fuzzy matching. A ratio of 90 is a good threshold for typos.
    match_ratio = fuzz.ratio(normalized_guess, normalized_target)

    session['attempts'] += 1

    if match_ratio > 90:
        time_spent = time.time() - session['start_time']
        session['game_over'] = True
        return jsonify({
            'status': 'win',
            'country_name': target_country.name,
            'flag_code': target_country.flag_code,
            'time_spent': round(time_spent, 2),
            'attempts': session['attempts']
        })
    else:
        wrong_guesses = session.get('wrong_guesses', [])
        if normalized_guess and guess_country_name not in wrong_guesses:
            wrong_guesses.append(guess_country_name)
            session['wrong_guesses'] = wrong_guesses

        if len(wrong_guesses) >= 10:
            session['game_over'] = True
            return jsonify({
                'status': 'lose',
                'country_name': target_country.name, # Ensure this is sent on loss
                'flag_code': target_country.flag_code,
                'wrong_guesses': wrong_guesses,
                'attempts': session['attempts']
            })
        
        return jsonify({
            'status': 'wrong',
            'message': f'"{guess_country_name}" não é o país correto. Tente novamente.',
            'wrong_guesses': wrong_guesses,
            'attempts': session['attempts']
        })

@app.route('/save_ranking', methods=['POST'])
def save_ranking():
    # Ensure game was won and data is in session
    if 'country_id' not in session or not session.get('game_over') or 'start_time' not in session:
        return jsonify({'error': 'No game data to save.'}), 400

    data = request.get_json()
    player_name = data.get('player_name')
    if not player_name:
        return jsonify({'error': 'Player name is required.'}), 400
    
    target_country = db.session.get(Country, session['country_id'])
    # Use server-side session data for security and accuracy
    time_spent = time.time() - session['start_time']
    attempts = session.get('attempts', 0)

    new_ranking = Ranking(
        player_name=player_name,
        country_name=target_country.name,
        time_spent=time_spent,
        attempts=attempts
    )
    db.session.add(new_ranking)
    db.session.commit()

    session.clear()
    return jsonify({'status': 'success'})

@app.route('/ranking')
def ranking():
    rankings = db.session.query(Ranking).order_by(Ranking.time_spent, Ranking.attempts).limit(20).all()
    return render_template('ranking.html', rankings=rankings)

if __name__ == '__main__':
    app.run(debug=True)

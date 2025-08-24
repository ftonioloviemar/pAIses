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

@app.cli.command('migrate-db')
def migrate_db_command():
    with app.app_context():
        conn = db.engine.connect()
        inspector = db.inspect(db.engine)
        table_names = inspector.get_table_names()

        if 'country' in table_names:
            columns = inspector.get_columns('country')
            column_names = [col['name'] for col in columns]

            if 'difficulty' not in column_names:
                print("Adding 'difficulty' column to Country table...")
                try:
                    # Add column as nullable first
                    conn.execute(db.text("ALTER TABLE country ADD COLUMN difficulty VARCHAR(255)"))
                    db.session.commit()
                    print("'difficulty' column added.")

                    # Populate difficulty for existing countries
                    easy_countries = [
                        "Brasil", "Estados Unidos", "Argentina", "Portugal", "Espanha", "França", "Alemanha", "Itália", "Japão", "China", "Canadá", "México", "Reino Unido"
                    ]
                    medium_countries = [
                        "Chile", "Colômbia", "Peru", "Uruguai", "Paraguai", "Venezuela", "África do Sul", "Austrália", "Nova Zelândia", "Índia", "Rússia", "Egito", "Nigéria", "Suécia", "Noruega", "Finlândia", "Dinamarca", "Países Baixos", "Bélgica", "Suíça", "Áustria", "Grécia", "Turquia", "Arábia Saudita", "Emirados Árabes Unidos", "Israel", "Coreia do Sul", "Tailândia", "Vietnã", "Indonésia"
                    ]

                    countries = Country.query.all()
                    for country in countries:
                        difficulty = "hard" # Default to hard
                        if country.name in easy_countries:
                            difficulty = "easy"
                        elif country.name in medium_countries:
                            difficulty = "medium"
                        country.difficulty = difficulty
                    db.session.commit()
                    print("Difficulty populated for existing countries.")

                    # Alter column to NOT NULL after populating
                    # SQLite doesn't support ALTER COLUMN SET NOT NULL directly.
                    # This would require a more complex migration (new table, copy data, drop old, rename).
                    # For simplicity, we'll leave it nullable for now or rely on application logic.
                    print("Migration complete. 'difficulty' column added and populated.")

                except Exception as e:
                    db.session.rollback()
                    print(f"Error during migration: {e}")
            else:
                print("'difficulty' column already exists.")
        else:
            print("'country' table does not exist. Run 'init-db' first.")

@app.cli.command('migrate-ranking-difficulty')
def migrate_ranking_difficulty_command():
    with app.app_context():
        conn = db.engine.connect()
        inspector = db.inspect(db.engine)
        table_names = inspector.get_table_names()

        if 'ranking' in table_names:
            columns = inspector.get_columns('ranking')
            column_names = [col['name'] for col in columns]

            if 'difficulty' not in column_names:
                print("Adding 'difficulty' column to Ranking table...")
                try:
                    conn.execute(db.text("ALTER TABLE ranking ADD COLUMN difficulty VARCHAR(255)"))
                    db.session.commit()
                    print("'difficulty' column added.")

                    rankings = Ranking.query.all()
                    for entry in rankings:
                        # Try to find the country to get its difficulty
                        country = Country.query.filter_by(name=entry.country_name).first()
                        if country:
                            entry.difficulty = country.difficulty
                        else:
                            # Default if country not found (e.g., if country data was reset)
                            entry.difficulty = "unknown" 
                    db.session.commit()
                    print("Difficulty populated for existing ranking entries.")
                    print("Migration complete. 'difficulty' column added and populated for Ranking.")

                except Exception as e:
                    db.session.rollback()
                    print(f"Error during migration: {e}")
            else:
                print("'difficulty' column already exists in Ranking table.")
        else:
            print("'ranking' table does not exist.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    data = request.get_json()
    selected_difficulty = data.get('difficulty', 'easy') # Default to easy

    # Filter countries by difficulty
    available_countries = Country.query.filter_by(difficulty=selected_difficulty).all()

    if not available_countries:
        return jsonify({'error': 'No countries found for this difficulty.'}), 400

    # Prevent picking the same country twice in a row
    last_country_id = session.get('last_country_id', None)
    country = None
    # Ensure a different country is picked if possible, or pick any if only one is available
    if len(available_countries) > 1:
        while country is None or country.id == last_country_id:
            country = random.choice(available_countries)
    else:
        country = available_countries[0] # Only one country available

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
        attempts=attempts,
        difficulty=target_country.difficulty
    )
    db.session.add(new_ranking)
    db.session.commit()

    session.clear()
    return jsonify({'status': 'success'})

@app.route('/give_up', methods=['POST'])
def give_up():
    if 'country_id' not in session:
        return jsonify({'error': 'No game in progress.'}), 400

    target_country = db.session.get(Country, session['country_id'])
    attempts = session.get('attempts', 0)

    session['game_over'] = True
    session.pop('country_id', None)
    session.pop('start_time', None)
    session.pop('attempts', None)
    session.pop('wrong_guesses', None)

    return jsonify({
        'status': 'given_up',
        'country_name': target_country.name,
        'flag_code': target_country.flag_code,
        'attempts': attempts
    })

@app.route('/ranking')
def ranking():
    # Define a custom order for difficulty
    difficulty_order = {'hard': 1, 'medium': 2, 'easy': 3}

    rankings = db.session.query(Ranking).all()

    # Sort in Python based on custom difficulty order, then by time_spent, then attempts
    rankings.sort(key=lambda x: (difficulty_order.get(x.difficulty, 99), x.time_spent, x.attempts))

    # Limit to 20 after sorting
    rankings = rankings[:20]

    return render_template('ranking.html', rankings=rankings)

if __name__ == '__main__':
    app.run(debug=True)

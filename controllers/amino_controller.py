import re
from flask import Blueprint, render_template, request, redirect, url_for
from database import db_connection
from psycopg2.extras import DictCursor

bp = Blueprint('amino', __name__, url_prefix='/')

# Standard English labels for the web interface
LABELS = {
    'name': 'Amino Acid Name',
    'one_letter_abbr': '1-Letter Abbreviation',
    'three_letter_abbr': '3-Letter Abbreviation',
    'structure': 'Molecular Formula',
    'property': 'Chemical Property'
}

@bp.route('/')
def welcome():
    return render_template('todo.html', view='welcome')

@bp.route('/setup', methods=['GET', 'POST'])
def setup_game():
    if request.method == 'POST':
        show_col = request.form.get('show_column')
        guess_col = request.form.get('guess_column')
        
        # SQL INSERT: Create a new GameSession record in PostgreSQL
        conn = db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO GameSession (amount_questions, score, mode_id) VALUES (%s, %s, %s) RETURNING session_id',
            (10, 0, 1)
        )
        session_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('amino.game', show=show_col, guess=guess_col, session=session_id))
    
    return render_template('todo.html', view='setup')

@bp.route('/game', methods=['GET', 'POST'])
def game():
    conn = db_connection()
    cur = conn.cursor(cursor_factory=DictCursor)

    feedback = None
    
    show_col = request.args.get('show', 'one_letter_abbr')
    guess_col = request.args.get('guess', 'name')
    session_id = request.args.get('session')

    if request.method == 'POST':
        show_col = request.form.get('show_column')
        guess_col = request.form.get('guess_column')
        correct_answer = request.form.get('correct_answer', '').strip().lower()
        
        if guess_col == 'property':
            user_guesses = request.form.getlist('user_guess')
            user_clean = ",".join(sorted([g.strip().lower() for g in user_guesses]))
            correct_clean = ",".join(sorted([c.strip().lower() for c in correct_answer.split(',') if c.strip()]))
            
            if user_clean == correct_clean:
                feedback = "Correct! Well done."
            else:
                feedback = f"Incorrect. The correct property is: {correct_answer}."
        else:
            user_guess = request.form.get('user_guess', '').strip().lower()
            if user_guess == correct_answer:
                feedback = "Correct! Well done."
            else:
                feedback = f"Incorrect. The correct answer was '{correct_answer}'."

    # SQL SELECT: Fetch a random amino acid from PostgreSQL
    cur.execute('SELECT name, three_letter_abbr, one_letter_abbr, structure, property FROM AminoAcids ORDER BY RANDOM() LIMIT 1')
    row = cur.fetchone()
    
    cur.close()
    conn.close()

    if not row:
        return redirect(url_for('amino.setup_game'))

    question_target = row[show_col]
    correct_answer = row[guess_col]

    return render_template(
        'todo.html',
        view='quiz',
        question_target=question_target,
        correct_answer=correct_answer,
        feedback=feedback,
        show_column=show_col,
        guess_column=guess_col,
        show_label=LABELS[show_col],
        guess_label=LABELS[guess_col]
    )

@bp.route('/regex-test', methods=['POST'])
def regex_test():
    sequence = request.form.get('sequence', '').upper()
    pattern = request.form.get('pattern', '')
    try:
        if re.search(pattern, sequence):
            match_result = f"Match found! The sequence '{sequence}' matches the pattern '{pattern}'."
        else:
            match_result = f"No match. The sequence '{sequence}' does NOT match the pattern '{pattern}'."
    except re.error:
        match_result = "Invalid Regex Pattern entered."
    return f"<h3>Regex Result:</h3> {match_result} <br><br> <a href='/'>Go back to Welcome Screen</a>"
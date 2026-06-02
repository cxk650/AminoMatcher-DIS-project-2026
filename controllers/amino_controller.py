import re
from flask import Blueprint, render_template, request, redirect, url_for
from database import db_connection

bp = Blueprint('amino', __name__, url_prefix='/')

LABELS = {
    'name': 'Amino Acid Name',
    'one_letter_abbr': '1-Letter Abbreviation',
    'three_letter_abbr': '3-Letter Abbreviation',
    'structure': 'Molecular Formula',
    'property': 'Chemical Property'
}

# 1. NEW WELCOME & SETUP ROUTE
@bp.route('/start', methods=['GET', 'POST'])
def setup_game():
    if request.method == 'POST':
        show_col = request.form.get('show_column')
        guess_col = request.form.get('guess_column')
        
        # Create a session in database
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

        # Redirect to the brand new game URL
        return redirect(url_for('amino.game', show=show_col, guess=guess_col, session=session_id))
    
    # Show setup screen directly as the new landing page
    return render_template('todo.html', view='setup')

# 2. NEW GAME ROUTE
@bp.route('/play-game', methods=['GET', 'POST'])
def game():
    conn = db_connection()
    cur = conn.cursor()

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

    # Fetch random amino acid
    cur.execute('SELECT name, three_letter_abbr, one_letter_abbr, structure, property FROM AminoAcids ORDER BY RANDOM() LIMIT 1')
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return redirect(url_for('amino.setup_game'))

    data_map = {
        'name': row[0],
        'three_letter_abbr': row[1],
        'one_letter_abbr': row[2],
        'structure': row[3],
        'property': row[4]
    }

    question_target = data_map.get(show_col, row[0])
    correct_answer = data_map.get(guess_col, row[2])

    return render_template(
        'todo.html',
        view='quiz',
        question_target=question_target,
        correct_answer=correct_answer,
        feedback=feedback,
        show_column=show_col,
        guess_column=guess_col,
        show_label=LABELS.get(show_col, 'Question'),
        guess_label=LABELS.get(guess_col, 'Answer')
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
    return f"<h3>Regex Result:</h3> {match_result} <br><br> <a href='/start'>Go back to Setup Screen</a>"
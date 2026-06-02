import re
from flask import Blueprint, render_template, request
from database import db_connection

bp = Blueprint('amino', __name__, url_prefix='/')

# 1. Ruten til selve spillet og aminosyre-oversigten
@bp.route('/amino', methods=['GET', 'POST'])
def amino_game():
    conn = db_connection()
    cur = conn.cursor()

    feedback = None
    user_guess = None

    # Hvis brugeren har svaret på et spørgsmål (POST)
    if request.method == 'POST':
        user_guess = request.form.get('user_guess', '').strip().upper()
        correct_answer = request.form.get('correct_answer', '').strip().upper()
        
        # SQL UPDATE/INSERT krav: Her kan du senere gemme scoren i GameSession.
        # For nu tjekker vi bare svaret direkte
        if user_guess == correct_answer:
            feedback = "Rigtigt!"
        else:
            feedback = f"Forkert! Det rigtige svar var {correct_answer}."

    # SQL SELECT krav: Vi henter en tilfældig aminosyre til det næste spørgsmål
    cur.execute('SELECT name, three_letter_abbr, one_letter_abbr, structure, property FROM AminoAcids ORDER BY RANDOM() LIMIT 1')
    current_question = cur.fetchone()

    # Vi henter også alle aminosyrer, så vi kan vise en liste på siden
    cur.execute('SELECT name, three_letter_abbr, one_letter_abbr FROM AminoAcids ORDER BY name ASC')
    all_aminos = cur.fetchall()

    cur.close()
    conn.close()

    # Hvis databasen er tom, laver vi et fallback så siden ikke crasher
    if not current_question:
        current_question = ('Alanine', 'Ala', 'A', 'CH3', 'Aliphatic')

    return render_template(
        'todo.html', 
        question_target=current_question[3], # Vi spørger ud fra strukturen (f.eks. CH3) [cite: 2]
        correct_answer=current_question[2],   # Det rigtige svar er 1-letter abbreviation (f.eks. A) [cite: 5]
        feedback=feedback,
        all_aminos=all_aminos
    )

# 2. DET OBLIGATORISKE REGEX-KRAV: Rute til at teste sekvenser
@bp.route('/regex-test', methods=['POST'])
def regex_test():
    sequence = request.form.get('sequence', '').upper()
    pattern = request.form.get('pattern', '')
    
    try:
        # Udfører Regular Expression matching på aminosyre-sekvensen
        if re.search(pattern, sequence):
            match_result = f"Match fundet! Sekvensen '{sequence}' passer på mønsteret '{pattern}'."
        else:
            match_result = f"Intet match. Sekvensen '{sequence}' passer IKKE på mønsteret '{pattern}'."
    except re.error:
        match_result = "Ugyldigt Regex-mønster indtastet."

    # Vi sender resultatet tilbage som en simpel besked
    return f"<h3>Regex Resultat:</h3> {match_result} <br><br> <a href='/amino'>Gå tilbage til spillet</a>"
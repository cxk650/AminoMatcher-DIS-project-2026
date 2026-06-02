import re
from flask import Blueprint, render_template, request
from database import db_connection

bp = Blueprint('amino', __name__, url_prefix='/')

@bp.route('/amino', methods=['GET', 'POST'])
def amino_game():
    conn = db_connection()
    cur = conn.cursor()

    # Find ud af hvilken spiltilstand der er valgt (standard er '1_letter')
    current_mode = request.args.get('mode', '1_letter')
    
    feedback = None

    # HÅNDTERING AF SVAR (POST)
    if request.method == 'POST':
        correct_answer = request.form.get('correct_answer', '').strip().lower()
        
        if current_mode == 'egenskab':
            # Hvis det er egenskaber, kan brugeren have valgt flere krydser, så vi får en liste
            user_guesses = request.form.getlist('user_guess')
            # Vi rydder op og sorterer dem, så vi kan sammenligne med databasen
            user_guesses_clean = ",".join(sorted([g.strip().lower() for g in user_guesses]))
            
            # Vi rydder også databasens svar op (hvis der står "hydrophobe, positive")
            correct_clean = ",".join(sorted([c.strip().lower() for c in correct_answer.split(',') if c.strip()]))
            
            if user_guesses_clean == correct_clean:
                feedback = "Rigtigt! Det matcher præcis aminosyrens egenskaber."
            else:
                feedback = f"Forkert! Denne aminosyre er i virkeligheden: {correct_answer}."
        else:
            # For tekst-gæt (Navn, 1-letter, 3-letter)
            user_guess = request.form.get('user_guess', '').strip().lower()
            if user_guess == correct_answer:
                feedback = "Rigtigt! Flot gættet."
            else:
                feedback = f"Forkert! Det rigtige svar var '{correct_answer}'."

    # DYNAMISK SQL: Vi trækker en tilfældig aminosyre ud
    cur.execute('SELECT name, three_letter_abbr, one_letter_abbr, structure, property FROM AminoAcids ORDER BY RANDOM() LIMIT 1')
    row = cur.fetchone()
    cur.close()
    conn.close()

    # Opsætning af spørgsmålet alt efter hvilken GameMode der spilles
    if current_mode == 'navn':
        mode_title = "Gæt ud fra Navn"
        question_target = f"Strukturen {row[3]} og forkortelsen {row[1]}" # Vis struktur/3-letter, gæt navn
        correct_answer = row[0] # Svaret er 'name'
    elif current_mode == '3_letter':
        mode_title = "Gæt ud fra 3-Letter Abbreviation"
        question_target = f"Aminosyren med navnet '{row[0]}'" # Vis navn, gæt 3-letter
        correct_answer = row[1] # Svaret er 'three_letter_abbr'
    elif current_mode == 'egenskab':
        mode_title = "Gæt ud fra Egenskaber (Kryds af)"
        question_target = f"Aminosyren med navnet '{row[0]}' ({row[1]})" # Vis navn, gæt egenskab
        correct_answer = row[4] # Svaret er 'property' (f.eks. hydrophobe)
    else: # standard '1_letter'
        mode_title = "Gæt ud fra 1-Letter Abbreviation"
        question_target = f"Strukturen {row[3]} (Navn: {row[0]})" # Vis struktur/navn, gæt 1-letter
        correct_answer = row[2] # Svaret er 'one_letter_abbr'

    return render_template(
        'todo.html', 
        question_target=question_target,
        correct_answer=correct_answer,
        feedback=feedback,
        current_mode=current_mode,
        mode_title=mode_title
    )

# REGEX SEKVENSTJEKKER (Bliver som den er)
@bp.route('/regex-test', methods=['POST'])
def regex_test():
    sequence = request.form.get('sequence', '').upper()
    pattern = request.form.get('pattern', '')
    try:
        if re.search(pattern, sequence):
            match_result = f"Match fundet! Sekvensen '{sequence}' passer på mønsteret '{pattern}'."
        else:
            match_result = f"Intet match. Sekvensen '{sequence}' passer IKKE på mønsteret '{pattern}'."
    except re.error:
        match_result = "Ugyldigt Regex-mønster."
    return f"<h3>Regex Resultat:</h3> {match_result} <br><br> <a href='/amino'>Gå tilbage til spillet</a>"
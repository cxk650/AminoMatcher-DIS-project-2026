from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import psycopg2.extras
import re

app = Flask(__name__)
app.secret_key = 'skift-denne-til-en-tilfældig-streng'

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="aminomatcher",   # <-- dit database navn
        user="rikkelissau",           # <-- din postgres bruger
        password="rikkem2s"    # <-- dit password
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT mode_id, mode_name FROM game_modes;")
    modes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', modes=modes)

@app.route('/start', methods=['POST'])
def start():
    mode_id = request.form['mode_id']
    amount_questions = 10
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO game_sessions (mode_id, amount_question, score)
        VALUES (%s, %s, %s) RETURNING session_id;
    """, (mode_id, amount_questions, 0))
    session_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    session['session_id'] = session_id
    session['question_count'] = 0
    session['score'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'session_id' not in session:
        return redirect(url_for('index'))

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    current_sid = session['session_id']

    if request.method == 'POST':
        user_answer = request.form['answer'].strip()
        current_qid = session.get('current_question_id')

        # Regex validering (tillad bogstaver, bindestreg, mellemrum)
        if not re.match(r'^[A-Za-z\s\-]+$', user_answer):
            cur.execute("""
                SELECT q.question_id, q.question_text, q.correct_answer, a.name
                FROM questions q
                JOIN amino_acids a ON q.amino_acid_id = a.aminoacid_id
                WHERE q.question_id = %s
            """, (current_qid,))
            q = cur.fetchone()
            cur.close()
            conn.close()
            return render_template('quiz.html', question=q, error="Ugyldigt svar – brug kun bogstaver.")

        # Hent korrekt svar
        cur.execute("SELECT correct_answer FROM questions WHERE question_id = %s", (current_qid,))
        correct = cur.fetchone()['correct_answer']
        is_correct = (user_answer.lower() == correct.lower())

        # Gem i session_questions
        cur.execute("""
            INSERT INTO session_questions (session_id, question_id, user_answer, is_correct)
            VALUES (%s, %s, %s, %s)
        """, (current_sid, current_qid, user_answer, is_correct))

        if is_correct:
            session['score'] += 1
            cur.execute("UPDATE game_sessions SET score = %s WHERE session_id = %s",
                        (session['score'], current_sid))
        conn.commit()
        session['question_count'] += 1

        # Tjek om færdig
        cur.execute("SELECT amount_question FROM game_sessions WHERE session_id = %s", (current_sid,))
        max_q = cur.fetchone()['amount_question']
        if session['question_count'] >= max_q:
            cur.close()
            conn.close()
            return redirect(url_for('result'))

        # Næste spørgsmål (som ikke er stillet før)
        cur.execute("""
            SELECT q.question_id, q.question_text, q.correct_answer, a.name
            FROM questions q
            JOIN amino_acids a ON q.amino_acid_id = a.aminoacid_id
            WHERE q.question_id NOT IN (
                SELECT question_id FROM session_questions WHERE session_id = %s
            )
            ORDER BY RANDOM() LIMIT 1
        """, (current_sid,))
        q = cur.fetchone()
        if q is None:
            cur.close()
            conn.close()
            return redirect(url_for('result'))
        session['current_question_id'] = q['question_id']
        cur.close()
        conn.close()
        return render_template('quiz.html', question=q)

    # GET: første spørgsmål
    cur.execute("""
        SELECT q.question_id, q.question_text, q.correct_answer, a.name
        FROM questions q
        JOIN amino_acids a ON q.amino_acid_id = a.aminoacid_id
        WHERE q.question_id NOT IN (
            SELECT question_id FROM session_questions WHERE session_id = %s
        )
        ORDER BY RANDOM() LIMIT 1
    """, (current_sid,))
    q = cur.fetchone()
    if q is None:
        cur.close()
        conn.close()
        return redirect(url_for('result'))
    session['current_question_id'] = q['question_id']
    cur.close()
    conn.close()
    return render_template('quiz.html', question=q)

@app.route('/result')
def result():
    score = session.get('score', 0)
    return f"<h1>Quiz færdig!</h1><p>Din score: {score}</p><a href='/'>Spil igen</a>"

if __name__ == '__main__':
    app.run(debug=True)
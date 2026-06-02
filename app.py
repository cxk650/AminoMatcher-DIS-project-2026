import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",   # fordi dine tabeller ligger i postgres/public
        user="postgres",
        password="qbq52yex"
    )
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT name, one_letter_abbr, three_letter_abbr FROM aminoacid LIMIT 1;")
    aa = cur.fetchone()

    cur.close()
    conn.close()

    return f"Test: {aa}"

import random

def get_random_aminoacid():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT name, one_letter_abbr, three_letter_abbr FROM aminoacid;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return random.choice(rows)

@app.route("/random")
def random_aa():
    aa = get_random_aminoacid()
    return render_template("random.html", aa=aa)

def get_quiz_question():
    conn = get_db_connection()
    cur = conn.cursor()

    # hent 4 random aminosyrer
    cur.execute("""
        SELECT name, one_letter_abbr, three_letter_abbr
        FROM aminoacid
        ORDER BY RANDOM()
        LIMIT 4;
    """)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    correct = rows[0]  # første er korrekt
    options = [row[1] for row in rows]  # one-letter codes

    return correct, options
@app.route("/quiz")
def quiz():
    correct, options = get_quiz_question()
    return render_template("quiz.html", correct=correct, options=options)

from flask import request

@app.route("/answer", methods=["POST"])
def answer():
    choice = request.form["choice"]
    correct = request.form["correct"]

    if choice == correct:
        return "Correct, good job!"
    else:
        return f"Wrong! The correct answer is {correct}"
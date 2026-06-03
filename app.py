import psycopg2
from flask import Flask, render_template
import random

app = Flask(__name__)
app.secret_key = "noget_meget_sikkert"

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",   # fordi dine tabeller ligger i postgres/public
        user="postgres",
        #password="" kun hvis nødvendigt
    )
    return conn

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/aminoacids")
def aminoacids():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, one_letter_abbr, three_letter_abbr, molecular_formula, property
        FROM aminoacid
        ORDER BY name;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("aminoacids.html", rows=rows)

import random
from flask import session
def generate_image_mc_question(aminoacids):
    correct = random.choice(aminoacids)

    # vælg 3 forkerte
    wrong = random.sample([a for a in aminoacids if a != correct], 3)

    choices = [correct["name"]] + [a["name"] for a in wrong]
    random.shuffle(choices)

    return {
        "type": "image_mc",
        "image": correct["image_filename"],
        "question": "Which aminoacid is shown on the picture?",
        "choices": choices,
        "correct_answer": correct["name"]
    }
def generate_image_formula_question(aminoacids):
    aa = random.choice(aminoacids)

    return {
        "type": "image_formula",
        "image": aa["image_filename"],
        "question": "What is the molecular formula for this aminoacid?",
        "correct_answer": aa["molecular_formula"]
    }

def generate_question():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, one_letter_abbr, three_letter_abbr, molecular_formula, property, image_filename
        FROM aminoacid
        ORDER BY RANDOM()
        LIMIT 4;
    """)
    rows = cur.fetchall()

    correct = rows[0]
    wrong = rows[1:]

    q_type = session.get("qtype", "random")

    all_types = [
        "name_to_one",
        "name_to_three",
        "name_to_property",
        "name_to_formula",
        "one_to_name",
        "three_to_name",
        "free_input",
        "image_mc",
        "image_formula"
    ]

    if q_type == "random":
        q_type = random.choice(all_types)

    if q_type == "free_input":
        inner_type = random.choice([
            "name_to_one",
            "name_to_three",
            "name_to_property",
            "name_to_formula",
            "one_to_name",
            "three_to_name"
        ])
        q_type = inner_type
        free_input = True
    else:
        free_input = False

    # ---------------- TEXT QUESTIONS ----------------
    if q_type == "name_to_one":
        question = f"What is the one-letter code for {correct[0]}?"
        correct_answer = correct[1]
        choices = [correct[1]] + [w[1] for w in wrong]

    elif q_type == "name_to_three":
        question = f"What is the three-letter abbreviation for {correct[0]}?"
        correct_answer = correct[2]
        choices = [correct[2]] + [w[2] for w in wrong]

    elif q_type == "name_to_property":
        question = f"Which property does {correct[0]} have?"
        correct_answer = correct[4]
        choices = [correct[4]] + [w[4] for w in wrong]

    elif q_type == "name_to_formula":
        question = f"What is the molecular formula for {correct[0]}?"
        correct_answer = correct[3]
        choices = [correct[3]] + [w[3] for w in wrong]

    elif q_type == "one_to_name":
        question = f"Which amino acid has the one-letter code {correct[1]}?"
        correct_answer = correct[0]
        choices = [correct[0]] + [w[0] for w in wrong]

    elif q_type == "three_to_name":
        question = f"Which amino acid has the three-letter abbreviation {correct[2]}?"
        correct_answer = correct[0]
        choices = [correct[0]] + [w[0] for w in wrong]

    # ---------------- IMAGE MC ----------------
    elif q_type == "image_mc":
        question = "Which amino acid is shown in the picture?"
        correct_answer = correct[0]
        choices = [correct[0]] + [w[0] for w in wrong]
        random.shuffle(choices)

        session["last_question_text"] = question
        session["last_correct_answer"] = correct_answer
        session["last_question_type"] = "image_mc"
        session["last_image"] = correct[5]
        session["last_options"] = choices

        cur.close()
        conn.close()

        return {
            "type": "image_mc",
            "question": question,
            "image": correct[5],
            "choices": choices,
            "correct_answer": correct_answer
        }

    # ---------------- IMAGE FORMULA ----------------
    elif q_type == "image_formula":
        question = "What is the molecular formula for this amino acid?"
        correct_answer = correct[3]

        session["last_question_text"] = question
        session["last_correct_answer"] = correct_answer
        session["last_question_type"] = "image_formula"
        session["last_image"] = correct[5]
        session["last_options"] = None

        cur.close()
        conn.close()

        return {
            "type": "image_formula",
            "question": question,
            "image": correct[5],
            "correct_answer": correct_answer
        }

    # ---------------- FINISH TEXT QUESTIONS ----------------
    if free_input:
        choices = None
        q_type_final = "text_input"
    else:
        random.shuffle(choices)
        q_type_final = "text_mc"

    session["last_question_text"] = question
    session["last_correct_answer"] = correct_answer
    session["last_question_type"] = q_type_final
    session["last_image"] = None
    session["last_options"] = choices

    cur.close()
    conn.close()

    return {
        "type": q_type_final,
        "question": question,
        "choices": choices,
        "correct_answer": correct_answer
    }

@app.route("/modes")
def modes():
    return render_template("modes.html")

@app.route("/choose_type/<mode>")
def choose_type(mode):
    return render_template("choose_type.html", mode=mode)

from flask import redirect
@app.route("/start/<mode>/<qtype>")
def start(mode, qtype):
    session.clear()

    # antal spørgsmål
    if mode == "10":
        session["total_questions"] = 10
    elif mode == "20":
        session["total_questions"] = 20
    elif mode == "survival":
        session["total_questions"] = 9999
        session["survival"] = True

    # spørgsmålstype
    session["qtype"] = qtype  # fx "name_to_one" eller "random"

    # reset score
    session["score"] = 0
    session["question"] = 1

    return redirect("/quiz")


from flask import session

@app.route("/quiz")
def quiz():
    session.setdefault("score", 0)
    session.setdefault("question", 1)
    session.setdefault("total_questions", 10)

    # generate_question() skal nu returnere ET dictionary
    q = generate_question()

    return render_template(
        "quiz.html",
        question_text=q["question"],
        question_type=q["type"],       # vigtigt!
        image=q.get("image"),          # kun til image-typer
        options=q.get("choices"),      # kun til MC-typer
        correct_answer=q["correct_answer"],
        score=session["score"],
        question=session["question"],
        total=session["total_questions"]
    )

from flask import request

import re
from flask import request, session, render_template, redirect

@app.route("/answer", methods=["POST"])
def answer():
    choice = request.form.get("choice", "").strip()
    correct = request.form["correct"].strip()

    # --- REGEX VALIDATION ---

    # One-letter code (A, R, N, ...)
    if re.fullmatch(r"[A-Z]", correct):
        valid = re.fullmatch(r"[A-Za-z]", choice)

    # Three-letter code (Ala, Arg, ...)
    elif re.fullmatch(r"[A-Za-z]{3}", correct):
        valid = re.fullmatch(r"[A-Za-z]{3}", choice)

    # Molecular formula (C3H7NO2, C6H14N4O2, ...)
    elif re.fullmatch(r"[A-Z][a-z]?\d*(?:[A-Z][a-z]?\d*)*", correct):
        valid = re.fullmatch(r"[A-Z][a-z]?\d*(?:[A-Z][a-z]?\d*)*", choice)

    # Property (Polar, Nonpolar, Acidic, Basic)
    elif correct.lower() in ["polar", "nonpolar", "acidic", "basic"]:
        valid = re.fullmatch(r"[A-Za-z]+", choice)

    # Amino acid name (Alanine, Lysine, ...)
    else:
        valid = re.fullmatch(r"[A-Za-z ]+", choice)

    # --- HANDLE REGEX FAIL ---
    if not valid:
        feedback = "Invalid format (regex mismatch)"

        return render_template(
            "quiz.html",
            question_text=session["last_question_text"],
            question_type=session["last_question_type"],
            image=session.get("last_image"),
            options=session.get("last_options"),
            correct_answer=session["last_correct_answer"],
            score=session["score"],
            question=session["question"],
            total=session["total_questions"],
            error=feedback
        )

    # --- NORMAL ANSWER CHECK ---
    if choice.lower() == correct.lower():
        session["score"] += 1
        feedback = "Correct!"
        color_class = "correct"
    else:
        feedback = f"Wrong! The correct answer was {correct}"
        color_class = "wrong"

        if session.get("survival"):
            return redirect("/game_over")

    # Increment question counter
    session["question"] += 1

    if session["question"] > session["total_questions"]:
        return redirect("/game_over")

    return render_template(
        "answer.html",
        feedback=feedback,
        score=session["score"],
        color_class=color_class
    )

@app.route("/game_over")
def game_over():
    score = session.get("score", 0)
    total = session.get("total_questions", 0)

    return render_template(
        "game_over.html",
        score=score,
        total=total
    )

@app.route("/restart_same")
def restart_same():
    # behold qtype, total_questions og survival
    qtype = session.get("qtype", "random")
    total = session.get("total_questions", 10)
    survival = session.get("survival", False)

    # nulstil score og spørgsmål
    session["score"] = 0
    session["question"] = 1
    session["qtype"] = qtype
    session["total_questions"] = total

    if survival:
        session["survival"] = True
    else:
        session.pop("survival", None)

    return redirect("/quiz")

@app.route("/reset")
def reset():
    session.clear()
    return "Session nulstillet! Du kan nu gå til /quiz igen."

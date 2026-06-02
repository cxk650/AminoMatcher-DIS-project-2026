from flask import Flask, render_template, request, redirect, url_for # We import render_template so we can render Jinja2 code, and request so we can handle POSTs
# We import sqlite, likely we don't need to install any new library because this is a default Python library
import sqlite3
import csv
import os

app = Flask(__name__)

DATABASE = "aminomatcher.db"

# Create connection to the database
def db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
    # Keep in mind that you may need to delete this file every time you change the schema of your database.

# ...
def init_db():
    conn = db_connection()

    with open('sql/schema.sql') as f:
        conn.executescript(f.read())

    conn.execute("INSERT OR IGNORE INTO game_modes (mode_name) VALUES (?)",("Name to abbreviation",))
    conn.execute("INSERT OR IGNORE INTO game_modes (mode_name) VALUES (?)", ("Property quiz",))

    with open("aminoacids_database.csv", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            conn.execute(
                """
                INSERT INTO amino_acids
                (Name, Abbr, Letter, Molecular_Formula, property)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    row["Name"],
                    row["Abbr"],
                    row["Letter"],
                    row["Molecular Formula"],
                    row["property"]
                )
            )

    conn.commit()
    conn.close()


# We initialize the database
# Vigtigt: Den sletter og genskaber databasen hver gang, fordi vi bruger DROP TABLE
# Okay for nu, men børe nok ændres senere.
init_db()

# Creating a frontpage
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/aminoacids")
def aminoacids():
    conn = db_connection()
    aminoacids = conn.execute("SELECT * FROM amino_acids").fetchall()
    conn.close()

    return render_template("aminoacids.html", aminoacids=aminoacids)

# Lav simpel quiz-side
@app.route("/game", methods=["GET", "POST"])
def game():
    conn = db_connection()

    result = None

    if request.method == "POST":
        correct_answer = request.form["correct_answer"]
        user_answer = request.form["user_answer"]

        if user_answer.strip().lower() == correct_answer.strip().lower():
            result = "Correct!"
        else:
            result = f"Wrong. The correct answer was {correct_answer}."
        
    aminoacid = conn.execute(
        "SELECT * FROM amino_acids ORDER BY RANDOM() LIMIT 1"
    ).fetchone()

    conn.close()

    return render_template("game.html", aminoacid=aminoacid, result=result)
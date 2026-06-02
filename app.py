from flask import Flask
from database import init_db
from controllers import amino_controller

# Byg databasen med jeres aminosyre-tabeller
init_db()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World! AminoMatcher-databasen kører på PostgreSQL.</p>"

# Registrer jeres nye aminosyre-spil og regex-ruter
app.register_blueprint(amino_controller.bp)
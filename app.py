from flask import Flask, redirect, url_for
from database import init_db
from controllers import amino_controller

# Initialize PostgreSQL database schema and load CSV
init_db()

app = Flask(__name__)

# Automatically redirect the root to our brand new setup route
@app.route("/")
def home():
    return redirect(url_for('amino.setup_game'))

app.register_blueprint(amino_controller.bp)
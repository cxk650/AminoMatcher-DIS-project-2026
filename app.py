from flask import Flask, redirect, url_for
from database import init_db
from controllers import amino_controller

# Initialize PostgreSQL database schema and load CSV
init_db()

app = Flask(__name__)

# The root URL now automatically redirects to our new English welcome screen
@app.route("/")
def home():
    return redirect(url_for('amino.welcome'))

# Register our game blueprints
app.register_blueprint(amino_controller.bp)
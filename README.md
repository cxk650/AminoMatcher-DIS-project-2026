# AminoMatcher

AminoMatcher is a browser-based educational game build with Python and Flask. 

It's purpose is to help students memories Amino acids and their properties.

## Group members

- Rikke Lissau
- Lea Rasmussen
- Julie Madsen
- Ellen Bendtsen

## How to run the project

1. Clone the repository:

```bash
git clone <repository-url>
cd AminoMatcher-DIS-project-2026
```

2. Create virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment:

Windows:
```bash
.venv\Scripts\activate
```

Mac/Linux:
```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run schema.sql

Only necessary first time
Make sure you're in /AminoMatcher-DIS-project-2026

```bash
sqlite3 /aminomatcher.db < schema.sql
```
6. Run import_csv.py 

Only necessary first time
```bash
python import_csv.py
```

7. Run app.py

```bash
python app.py
```

8. Run the Flask app:

```bash
flask run --debug
```

9. Open the game in your webbrowser 
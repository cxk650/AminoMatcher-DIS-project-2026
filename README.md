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
cd AminoMatcher
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
source . venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Adjust and run schema.sql

Under sql run schema.sql, take note on where your tables are created in your database.
The first line in schema.sql controls which schema the tables are created in.
Adjust it depending on where you want your tables to be placed in your PostgreSQL database.

```sql
SET search_path TO public;
```
Then run sql file in your preferred SQL tool

6. Change database login in app.py
```python
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",   # change this to your database name
        user="postgres",    # change to where your tables are after loading schema.sql
        password=""    # write password when necessary 
    )
    return conn
```
Password is only necessary when you have a password in your postgres setup, when using Postgres.app on macOS there usually is no need for a password.

7. Run the Flask app:

```bash
flask run --debug
```

8. Open the game in your webbrowser 
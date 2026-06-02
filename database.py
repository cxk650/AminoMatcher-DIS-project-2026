import psycopg2
import os

# Try to get from system enviroment variable
# Set your Postgres user and password as second arguments of these two next function calls
user = os.environ.get('PGUSER', 'postgres')
password = os.environ.get('PGPASSWORD', '123')
host = os.environ.get('HOST', '127.0.0.1')

def db_connection():
    db = "dbname='todo' user=" + user + " host=" + host + " password =" + password
    conn = psycopg2.connect(db)

    return conn


def init_db():
    conn = db_connection()
    cur = conn.cursor()
    
    # 1. Opret tabel for GameMode
    cur.execute('''
        CREATE TABLE IF NOT EXISTS GameMode (
            mode_id SERIAL PRIMARY KEY,
            mode_name TEXT NOT NULL
        )
    ''')
    
    # 2. Opret tabel for AminoAcids (one_letter_abbr og three_letter_abbr i stedet for tal)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS AminoAcids (
            aminoacid_id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            three_letter_abbr TEXT NOT NULL,
            one_letter_abbr TEXT NOT NULL,
            structure TEXT,
            property TEXT
        )
    ''')
    
    # 3. Opret tabel for GameSession
    cur.execute('''
        CREATE TABLE IF NOT EXISTS GameSession (
            session_id SERIAL PRIMARY KEY,
            amount_questions INTEGER NOT NULL,
            score INTEGER DEFAULT 0,
            mode_id INTEGER,
            FOREIGN KEY (mode_id) REFERENCES GameMode(mode_id)
        )
    ''')
    
    # 4. Opret tabel for Question
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Question (
            question_id SERIAL PRIMARY KEY,
            aminoacid_id INTEGER,
            session_id INTEGER,
            FOREIGN KEY (aminoacid_id) REFERENCES AminoAcids(aminoacid_id),
            FOREIGN KEY (session_id) REFERENCES GameSession(session_id)
        )
    ''')
    
    conn.commit()

    # INDSÆT TEST-DATA (ON CONFLICT DO NOTHING sørger for, det ikke crasher hvis det findes)
    # Først spiltyper:
    cur.execute('INSERT INTO GameMode (mode_id, mode_name) VALUES (%s, %s) ON CONFLICT DO NOTHING', (1, 'Gæt ud fra struktur'))
    cur.execute('INSERT INTO GameMode (mode_id, mode_name) VALUES (%s, %s) ON CONFLICT DO NOTHING', (2, 'Gæt ud fra egenskaber'))
    
    # Dernæst et par aminosyrer:
    cur.execute('''
        INSERT INTO AminoAcids (aminoacid_id, name, three_letter_abbr, one_letter_abbr, structure, property) 
        VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
    ''', (1, 'Alanine', 'Ala', 'A', 'CH3', 'Aliphatic'))
    
    cur.execute('''
        INSERT INTO AminoAcids (aminoacid_id, name, three_letter_abbr, one_letter_abbr, structure, property) 
        VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
    ''', (2, 'Glycine', 'Gly', 'G', 'H', 'Aliphatic'))

    conn.commit()
    conn.close()
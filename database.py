import psycopg2
import os
import csv

user = os.environ.get('PGUSER', 'learasmussen')
password = os.environ.get('PGPASSWORD', '')
host = os.environ.get('HOST', '127.0.0.1')

def db_connection():
    db = "dbname='todo' user=" + user + " host=" + host + " password=" + password
    conn = psycopg2.connect(db)
    return conn

def init_db():
    conn = db_connection()
    cur = conn.cursor()
    
    # 1. LÆS DEN SEPARATE SQL-FIL (Krav opfyldt!)
    with open('sql/schema.sql', 'r') as f:
        cur.execute(f.read())
    conn.commit()

    # Indsæt standard spiltyper via SQL
    cur.execute('INSERT INTO GameMode (mode_id, mode_name) VALUES (%s, %s) ON CONFLICT DO NOTHING', (1, 'Gæt ud fra struktur'))
    cur.execute('INSERT INTO GameMode (mode_id, mode_name) VALUES (%s, %s) ON CONFLICT DO NOTHING', (2, 'Gæt ud fra egenskaber'))
    
    # 2. LÆS AUTOMATISK FRA JERES CSV-FIL
    csv_path = 'aminoacids.csv'
    if os.path.exists(csv_path):
        with open(csv_path, mode='r', encoding='utf-8') as file:
            # Vi bruger DictReader, så vi kan ramme kolonnerne præcist via deres navne
            reader = csv.DictReader(file)
            
            for row in reader:
                # Vi udtrækker kun de 5 kolonner, jeres gruppe skal bruge
                name = row.get('Name')
                abbr = row.get('Abbr')
                letter = row.get('Letter')
                structure = row.get('Molecular Formula')
                prop = row.get('property') # Default hvis tom
                
                # Hvis rækken har de nødvendige basisdata, indsætter vi den i PostgreSQL
                if name and abbr and letter:
                    cur.execute('''
                        INSERT INTO AminoAcids (name, three_letter_abbr, one_letter_abbr, structure, property) 
                        VALUES (%s, %s, %s, %s, %s) ON CONFLICT (name) DO NOTHING
                    ''', (name, abbr, letter, structure, prop))
                    
    conn.commit()
    cur.close()
    conn.close()
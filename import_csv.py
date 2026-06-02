import csv
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="qbq52yex"
)
cur = conn.cursor()

with open('aminoacids.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cur.execute("""
            INSERT INTO aminoacid (name, one_letter_abbr, three_letter_abbr, molecular_formula, property)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            row['Name'],
            row['Letter'],
            row['Abbr'],
            row['Molecular Formula'],
            row['property']  # eller 'property' afhængigt af din CSV
        ))

conn.commit()
cur.close()
conn.close()

print("CSV-data er nu indlæst i aminoacid-tabellen.")
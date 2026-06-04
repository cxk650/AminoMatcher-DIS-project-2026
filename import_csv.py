import csv
import sqlite3

conn = sqlite3.connect("aminomatcher.db")
cur = conn.cursor()

with open('aminoacids.csv', newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cur.execute("""
            INSERT INTO aminoacid 
            (name, one_letter_abbr, three_letter_abbr, molecular_formula, property, image_filename)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row['Name'],
            row['Letter'],
            row['Abbr'],
            row['Molecular Formula'],
            row['property'],
            row['image_filename']
        ))

conn.commit()
cur.close()
conn.close()

print("CSV-data er nu indlæst i aminoacid-tabellen.")

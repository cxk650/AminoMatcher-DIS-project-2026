-- Ny sql fil til at indsætte data fra vores csv fil til vores tables
-- Vi har vores csv fil som vi importerer vores ting fra

\copy Amino_acids(Name, Abbr, Letter, Molecular_Formula, property) FROM '/Users/rikkelissau/KU/KU2/DIS/Project/AminoMatcher-DIS-Project-2026/aminoacids.csv' 
DELIMITER ',' CSV HEADER;

--Nu indsætter vi vores forskellige gamemodes med titler som man skal kune vælge fra på hjemmesiden;
INSERT INTO Game_modes (Mode_name) VALUES
('Match one-letter code'),
('Match three-letter abbreviation'),
('Match property (hydrophobe/hydrophile)'),
('Match molecular formula');

--Spørgsmål tid, her starter jeg lige med første gamemode; Match one-letter code:
INSERT INTO Questions (Amino_acid_id, Question_text)
SELECT Aminoacid_id, 'What is the one-letter code for ' || Name || '?'
FROM Amino_acids;
INSERT INTO Questions (Amino_acid_id, Question_text)
SELECT Aminoacid_id, 'What is the name for this one-letter code aminoacid ' || Letter || '?'
FROM Amino_acids;

--Moving on til match the three-letter abbreviation;
INSERT INTO Questions (Amino_acid_id, Question_text)
SELECT Aminoacid_id, 'What is the three-letter abbreviation for ' || Name || '?'
FROM Amino_acids;
INSERT INTO Questions (Amino_acid_id, Question_text)
SELECT Aminoacid_id, 'What is the name for this three-letter abbreviation aminoacid ' || Abbr || '?'
FROM Amino_acids;

--Vi hopper til property;
INSERT INTO Questions (Amino_acid_id, Question_text)
SELECT Aminoacid_id, 'Is ' || Name || ' hydrophobic, hydrophilic, negative or positive?'
FROM Amino_acids;
--kan man vende spårgsmålet om på samme måde som de andre?

--Molekylær formula;
INSERT INTO Questions (Amino_acid_id, Question_text)
SELECT Aminoacid_id, 'What is the name of the amoniacid with the molecular formula of ' || Molecular_Formula || '?'
FROM Amino_acids;
--er det for svært at vende den om?


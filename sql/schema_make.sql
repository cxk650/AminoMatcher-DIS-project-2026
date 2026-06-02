-- Dette er første dokument i vores sql kodning. 
-- Ud fra Bank eksemplet lavede de en sql fil for hver handling, så planen er, at 
-- vi har denne fil som er nr. 1 i "serien" af sql filer.
-- Denne fil bruges udelukkende til at lave vores tables outline.
-- Dette betyder IKKE at vi indsætter diverse værdier i vores tables, det gør vi i et andet sted
-- Vi tilføjer værdier i vores tables i filen "schema_insert.sql", hvor vi angiver data til alle keys/foreign keys/primary keys.
-- Vi indsætter dog ikke på de attributes hvor vi havde streg under, da det angiveligt bliver gjort dynamisk.
-- Det betyder, at vi kan ændre vores tables uden at ændre vores sql filer, hvilket er ret slay.

-- Nu laver vi vores aller første tabel:
-- 1. AminoAcids
CREATE TABLE Amino_acids (
    Aminoacid_id SERIAL PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    One_letter CHAR(1) NOT NULL,
    Three_letter VARCHAR(3) NOT NULL,
    Property VARCHAR(50)
);
-- Her bruger vi kommando "CREATE TABLE" og giver det navnet "Amonio_acids" og indsætter diverse attributes fra vores E/R diagram.
-- Vi bruger kommandoen "SERIAL" og "PRIMARY KEY" for at angive, at vores primær nøgle XXXX
-- Vi bruger kommandoen "VARCHAR(x)" for at angive at vores attributes skal være indenfor en bestemt mængde af indeces (bogstaver)
-- Vi bruger kommandoen "NOT NULL" for at angive, at vores attributes ikke kan være tomme 

-- 2. GameMode
CREATE TABLE Game_modes (
    Mode_id SERIAL PRIMARY KEY,
    Mode_name VARCHAR(50) NOT NULL
);
-- Her har vi game modes hvor vi skal have et mode_id som også har "SERIAL PRIMARY KEY", da det er hvad den er..? 
-- Og mode_name kan man kalde whatever så længe at man har under 50 bogstaver, og at feltet ikke er tomt

-- 3. GameSession (har fremmednøgle til GameMode)
CREATE TABLE Game_sessions (
    Session_id SERIAL PRIMARY KEY,
    Mode_id INTEGER REFERENCES Game_modes(Mode_id),
    Score INTEGER DEFAULT 0 --Man skal vel starte med en score på 0 hvis vu stadig har den med 
);
-- Her laver vi vores game session, hvor vi har session_id som primary key
-- Vi har mode_id som er en integer og den hentes jo fra et andet table, derfor bruger vi "REFERENCES", navnet på den table vi henter fra
-- og til sidst specifikt hvilken kolonne/attribute vi gerne vil have hentet fra vores andet table

-- Forbindelsestabel mellem GameSession og Question
CREATE TABLE Questions (
    Session_id INTEGER REFERENCES Game_sessions(Session_id),
    Question_id INTEGER REFERENCES Questions(Question_id),
    User_answer VARCHAR(50),   -- hvad brugeren svarede
    Is_correct BOOLEAN,        -- om svaret var korrekt så er der point på spil? medmindre vi dropper det?
    PRIMARY KEY (Session_id, Question_id) -- For at vi ikke får det samme spørgsmål flere gange igen og igen i én session
);
-- Grunden til vi bruger forbindelsestabel er fordi vi har brugt de pile vi har, her tænkte jeg at vi havde en many-to-many da:
-- en session har mange spørgsmål, et spørgsmål kan indgå i mange sessioner..? eller måske har jeg misforstået noget
-- Her henter vi session_id som er fra vores game_sessions tabel, det samme gør vi med Question id fra vores questions tabel

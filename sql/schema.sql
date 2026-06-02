-- Opret tabeller ud fra jeres E/R-diagram
CREATE TABLE IF NOT EXISTS GameMode (
    mode_id SERIAL PRIMARY KEY,
    mode_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS AminoAcids (
    aminoacid_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    three_letter_abbr TEXT NOT NULL,
    one_letter_abbr TEXT NOT NULL,
    structure TEXT,
    property TEXT
);

CREATE TABLE IF NOT EXISTS GameSession (
    session_id SERIAL PRIMARY KEY,
    amount_questions INTEGER NOT NULL,
    score INTEGER DEFAULT 0,
    mode_id INTEGER,
    FOREIGN KEY (mode_id) REFERENCES GameMode(mode_id)
);

CREATE TABLE IF NOT EXISTS Question (
    question_id SERIAL PRIMARY KEY,
    aminoacid_id INTEGER,
    session_id INTEGER,
    FOREIGN KEY (aminoacid_id) REFERENCES AminoAcids(aminoacid_id),
    FOREIGN KEY (session_id) REFERENCES GameSession(session_id)
);
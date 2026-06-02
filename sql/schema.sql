DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS game_session;
DROP TABLE IF EXISTS game_modes;
DROP TABLE IF EXISTS amino_acids;

CREATE TABLE amino_acids (
    aminoacid_id SERIAL PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Abbr VARCHAR(3) NOT NULL,
    Letter VARCHAR(1) NOT NULL,
    Molecular_Formula TEXT,
    property TEXT
);

CREATE TABLE game_modes (
    mode_id SERIAL PRIMARY KEY,
    mode_name TEXT NOT NULL UNIQUE
);

CREATE TABLE game_session (
    session_id SERIAL PRIMARY KEY,
    amount_questions INTEGER NOT NULL,
    score INTEGER DEFAULT 0,
    mode_id INTEGER NOT NULL,
    FOREIGN KEY (mode_id) REFERENCES game_modes(mode_id)
);

CREATE TABLE questions (
    question_id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL,
    aminoacid_id INTEGER NOT NULL,
    FOREIGN KEY (session_id) REFERENCES game_session(session_id),
    FOREIGN KEY (aminoacid_id) REFERENCES amino_acids(aminoacid_id)
);
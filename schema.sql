PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS gamesession;
DROP TABLE IF EXISTS answerchoice;
DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS aminoacid;
DROP TABLE IF EXISTS gamemode;

-- 1) GameMode
CREATE TABLE gamemode (
    mode_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mode_name TEXT NOT NULL,
    amount_questions INTEGER NOT NULL
);

-- 2) AminoAcid
CREATE TABLE aminoacid (
    aminoacid_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    one_letter_abbr TEXT NOT NULL,
    three_letter_abbr TEXT NOT NULL,
    molecular_formula TEXT NOT NULL,
    property TEXT,
    image_filename TEXT
);

-- 3) Question
CREATE TABLE question (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    aminoacid_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    FOREIGN KEY (aminoacid_id)
        REFERENCES aminoacid(aminoacid_id)
        ON DELETE CASCADE
);

-- 4) AnswerChoice
CREATE TABLE answerchoice (
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    answer_text TEXT NOT NULL,
    is_correct INTEGER NOT NULL,  -- 0/1 i stedet for BOOLEAN
    FOREIGN KEY (question_id)
        REFERENCES question(question_id)
        ON DELETE CASCADE
);

-- 5) GameSession
CREATE TABLE gamesession (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mode_id INTEGER NOT NULL,
    score INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (mode_id)
        REFERENCES gamemode(mode_id)
);

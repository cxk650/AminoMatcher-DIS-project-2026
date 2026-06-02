SET search_path TO aminomatcher, public;
-- Drop tables if they already exist (godt til udvikling)
DROP TABLE IF EXISTS gamesession;
DROP TABLE IF EXISTS answerchoice;
DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS aminoacid;
DROP TABLE IF EXISTS gamemode;

-- 1) GameMode
CREATE TABLE gamemode (
    mode_id SERIAL PRIMARY KEY,
    mode_name VARCHAR(100) NOT NULL,
    amount_questions INT NOT NULL
);

-- 2) AminoAcid
CREATE TABLE aminoacid (
    aminoacid_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    one_letter_abbr VARCHAR(1) NOT NULL,
    three_letter_abbr VARCHAR(3) NOT NULL,
    molecular_formula VARCHAR(100) NOT NULL,
    property VARCHAR(100)
);

-- 3) Question
CREATE TABLE question (
    question_id SERIAL PRIMARY KEY,
    aminoacid_id INT NOT NULL,
    question_text VARCHAR(255) NOT NULL,
    CONSTRAINT fk_question_aminoacid
        FOREIGN KEY (aminoacid_id)
        REFERENCES aminoacid(aminoacid_id)
        ON DELETE CASCADE
);

-- 4) AnswerChoice
CREATE TABLE answerchoice (
    answer_id SERIAL PRIMARY KEY,
    question_id INT NOT NULL,
    answer_text VARCHAR(255) NOT NULL,
    is_correct BOOLEAN NOT NULL,
    CONSTRAINT fk_answerchoice_question
        FOREIGN KEY (question_id)
        REFERENCES question(question_id)
        ON DELETE CASCADE
);

-- 5) GameSession
CREATE TABLE gamesession (
    session_id SERIAL PRIMARY KEY,
    mode_id INT NOT NULL,
    score INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_gamesession_gamemode
        FOREIGN KEY (mode_id)
        REFERENCES gamemode(mode_id)
        ON DELETE RESTRICT
);

SELECT * FROM aminoacid LIMIT 5;

CREATE SCHEMA quizmania;
USE quizmania;

CREATE TABLE difficulty (
    id INT PRIMARY KEY  AUTO_INCREMENT,
    name VARCHAR(45) UNIQUE,
    multiplier FLOAT
);

CREATE TABLE question (
    id INT PRIMARY KEY AUTO_INCREMENT,
    text VARCHAR(220) UNIQUE,
    difficulty_id INT,
    FOREIGN KEY (difficulty_id) REFERENCES difficulty(id)
);

CREATE TABLE topic (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(220) UNIQUE,
    description VARCHAR(220)
);

CREATE TABLE belongs (
    topic_id INT,
    question_id INT,
    PRIMARY KEY (topic_id, question_id),
    FOREIGN KEY (topic_id) REFERENCES topic(id),
    FOREIGN KEY (question_id) REFERENCES question(id)
);

CREATE TABLE answer (
    number INT,
    question_id INT,
    text VARCHAR(220),
    isRight TINYINT(1),
    PRIMARY KEY (number, question_id),
    FOREIGN KEY (question_id) REFERENCES question(id)
);

CREATE TABLE type (
    text VARCHAR(45) PRIMARY KEY
);

CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(45),
    surname VARCHAR(45),
    email VARCHAR(45) UNIQUE,
    newsletter TINYINT(1),
    type_text VARCHAR(45),
    player_session_id INT,
    FOREIGN KEY (player_session_id) REFERENCES player(session_id),
    FOREIGN KEY (type_text) REFERENCES type(text)
);

CREATE TABLE host (
    session_id INT PRIMARY KEY
);

CREATE TABLE room (
    id INT PRIMARY KEY,
    host_session_id INT,
    topic_id INT,
    FOREIGN KEY (host_session_id) REFERENCES host(session_id),
    FOREIGN KEY (topic_id) REFERENCES topic(id)
);

CREATE TABLE player (
    session_id INT PRIMARY KEY,
    timestamp TIMESTAMP,
    room_id INT,
    FOREIGN KEY (room_id) REFERENCES room(id)
);

CREATE TABLE answers (
    answer_number INT,
    answer_question_id INT,
    game_session_id INT,
    timestamp TIMESTAMP,
    points INT,
    PRIMARY KEY (answer_number, answer_question_id, game_session_id),
    FOREIGN KEY (answer_number) REFERENCES answer(number),
    FOREIGN KEY (answer_question_id) REFERENCES answer(question_id),
    FOREIGN KEY (game_session_id) REFERENCES player(session_id)
);

INSERT INTO type VALUE ('studente medie');
INSERT INTO type VALUE ('studente superiori');
INSERT INTO type VALUE ('studente universitario');
INSERT INTO type VALUE ('lavoratore');
INSERT INTO type VALUE ('altro');

drop table if exists quizzes;
drop table if exists questions;
drop table if exists answers;
drop table if exists users;

CREATE TABLE quizzes(
    quiz_id integer primary key autoincrement not null,
    title TEXT not null
);

CREATE TABLE questions(
    question_id integer primary key autoincrement not null,
    quiz_id integer not null,
    question TEXT not null,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(quiz_id)
);

CREATE TABLE answers(
    question_id integer not null,
    answer TEXT not null,
    FOREIGN KEY (question_id) REFERENCES questions(question_id)
);

CREATE TABLE users(
    user_id integer primary key autoincrement not null,
    username TEXT not null,
    password TEXT not null,
    permission TEXT not null
);

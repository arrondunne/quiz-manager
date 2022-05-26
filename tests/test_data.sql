INSERT INTO users (username, password, permission)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f', 'edit'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79', 'edit');


--Maths Quiz
INSERT INTO quizzes (title, description) VALUES ('Maths Quiz', 'The first quiz in the system!');

INSERT INTO questions (quiz_id, question) VALUES ((SELECT quiz_id FROM quizzes WHERE title='Maths Quiz'), 'What is 1 + 1?');
INSERT INTO questions (quiz_id, question) VALUES ((SELECT quiz_id FROM quizzes WHERE title='Maths Quiz'), 'What is 6 x 5?');
INSERT INTO questions (quiz_id, question) VALUES ((SELECT quiz_id FROM quizzes WHERE title='Maths Quiz'), 'What is 1 ^ 3?');

INSERT INTO answers (question_id, answer) VALUES ((SELECT question_id FROM questions WHERE question='What is 1 + 1?'), '1');
INSERT INTO answers (question_id, answer) VALUES ((SELECT question_id FROM questions WHERE question='What is 1 + 1?'), '2');
INSERT INTO answers (question_id, answer) VALUES ((SELECT question_id FROM questions WHERE question='What is 1 + 1?'), '3');
INSERT INTO answers (question_id, answer) VALUES ((SELECT question_id FROM questions WHERE question='What is 6 x 5?'), '10');
INSERT INTO answers (question_id, answer) VALUES ((SELECT question_id FROM questions WHERE question='What is 6 x 5?'), '20');
INSERT INTO answers (question_id, answer) VALUES ((SELECT question_id FROM questions WHERE question='What is 6 x 5?'), '30');
INSERT INTO answers (question_id, answer) VALUES ((SELECT question_id FROM questions WHERE question='What is 6 x 5?'), '69');
INSERT INTO answers (question_id, answer) VALUES ((SELECT question_id FROM questions WHERE question='What is 1 ^ 3?'), '1');
INSERT INTO answers (question_id, answer) VALUES ((SELECT question_id FROM questions WHERE question='What is 1 ^ 3?'), '2');
INSERT INTO answers (question_id, answer) VALUES ((SELECT question_id FROM questions WHERE question='What is 1 ^ 3?'), '3');


-- Geography Quiz
INSERT INTO quizzes (title, description) VALUES ('Geography Quiz', 'Testing if you know the countries - by Arron');

INSERT INTO questions (quiz_id, question) VALUES ((SELECT quiz_id FROM quizzes WHERE title='Geography Quiz'), 'What is London?');
INSERT INTO questions (quiz_id, question) VALUES ((SELECT quiz_id FROM quizzes WHERE title='Geography Quiz'), 'What is the World?');

INSERT INTO answers (question_id, answer) VALUES ((SELECT question_id FROM questions WHERE question='What is London?'), '1');
INSERT INTO answers (question_id, answer) VALUES ((SELECT question_id FROM questions WHERE question='What is London?'), '22222');
INSERT INTO answers (question_id, answer) VALUES ((SELECT question_id FROM questions WHERE question='What is London?'), 'adlkfgjh');
INSERT INTO answers (question_id, answer) VALUES ((SELECT question_id FROM questions WHERE question='What is the World?'), '1');
INSERT INTO answers (question_id, answer) VALUES ((SELECT question_id FROM questions WHERE question='What is the World?'), '2');
INSERT INTO answers (question_id, answer) VALUES ((SELECT question_id FROM questions WHERE question='What is the World?'), '3');
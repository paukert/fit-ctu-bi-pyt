INSERT INTO `poll` (id, name, owner_id, state_id) VALUES (1, 'Sports', 1, 2);
INSERT INTO `poll` (id, name, owner_id, state_id) VALUES (2, 'Forms', 1, 1);
-----------------------------------------------------------
INSERT INTO `question` (id, text, `order`, poll_id, question_type_id) VALUES (1, 'Sex', 1, 1, 1);
INSERT INTO `question` (id, text, `order`, poll_id, question_type_id) VALUES (2, 'What sports do you like?', 2, 1, 2);
INSERT INTO `question` (id, text, `order`, poll_id, question_type_id) VALUES (3, 'Name sportsman/sportswoman who:', 3, 1, 3);

INSERT INTO `question` (id, text, `order`, poll_id, question_type_id) VALUES (4, 'What service do you usually use?', null, 2, 1);
INSERT INTO `question` (id, text, `order`, poll_id, question_type_id) VALUES (5, 'What are you not satisfied with?', null, 2, 3);
INSERT INTO `question` (id, text, `order`, poll_id, question_type_id) VALUES (6, 'Other messages', null, 2, 3);
-----------------------------------------------------------
INSERT INTO `option` (id, text, question_id) VALUES (1, 'Male', 1);
INSERT INTO `option` (id, text, question_id) VALUES (2, 'Female', 1);
INSERT INTO `option` (id, text, question_id) VALUES (3, 'Tennis', 2);
INSERT INTO `option` (id, text, question_id) VALUES (4, 'Running', 2);
INSERT INTO `option` (id, text, question_id) VALUES (5, 'Cycling', 2);
INSERT INTO `option` (id, text, question_id) VALUES (6, 'Swimming', 2);
INSERT INTO `option` (id, text, question_id) VALUES (7, 'plays tennis', 3);
INSERT INTO `option` (id, text, question_id) VALUES (8, 'is football player', 3);

INSERT INTO `option` (id, text, question_id) VALUES (9, 'Google forms', 4);
INSERT INTO `option` (id, text, question_id) VALUES (10, 'Microsoft forms', 4);
INSERT INTO `option` (id, text, question_id) VALUES (11, 'JotForms', 4);
INSERT INTO `option` (id, text, question_id) VALUES (12, 'Feedback is important for us', 5);
INSERT INTO `option` (id, text, question_id) VALUES (13, 'Limit 300 words', 6);
-----------------------------------------------------------
INSERT INTO `answer` (id, name, date, gdpr_agreement, poll_id) VALUES (1, 'Lukas', '2021-05-07 13:03:25.624863', 1, 1);
INSERT INTO `answer` (id, name, date, gdpr_agreement, poll_id) VALUES (2, 'Markéta', '2021-05-07 13:04:15.135177', 1, 1);
INSERT INTO `answer` (id, name, date, gdpr_agreement, poll_id) VALUES (3, 'Anonymous user', '2021-05-07 13:04:38.929912', 0, 1);
-----------------------------------------------------------
INSERT INTO `answer_part` (id, text, answer_id, option_id) VALUES (1, '', 1, 1);
INSERT INTO `answer_part` (id, text, answer_id, option_id) VALUES (2, '', 1, 4);
INSERT INTO `answer_part` (id, text, answer_id, option_id) VALUES (3, '', 1, 5);
INSERT INTO `answer_part` (id, text, answer_id, option_id) VALUES (4, '', 1, 6);
INSERT INTO `answer_part` (id, text, answer_id, option_id) VALUES (5, 'Tomáš Berdych', 1, 7);
INSERT INTO `answer_part` (id, text, answer_id, option_id) VALUES (6, 'Tomáš Řepka', 1, 8);
INSERT INTO `answer_part` (id, text, answer_id, option_id) VALUES (7, '', 2, 2);
INSERT INTO `answer_part` (id, text, answer_id, option_id) VALUES (8, '', 2, 4);
INSERT INTO `answer_part` (id, text, answer_id, option_id) VALUES (9, '', 2, 5);
INSERT INTO `answer_part` (id, text, answer_id, option_id) VALUES (10, 'Nevím', 2, 7);
INSERT INTO `answer_part` (id, text, answer_id, option_id) VALUES (11, 'Milan Baroš', 2, 8);
INSERT INTO `answer_part` (id, text, answer_id, option_id) VALUES (12, '', 3, 1);
INSERT INTO `answer_part` (id, text, answer_id, option_id) VALUES (13, '', 3, 3);
INSERT INTO `answer_part` (id, text, answer_id, option_id) VALUES (14, '', 3, 4);
INSERT INTO `answer_part` (id, text, answer_id, option_id) VALUES (15, 'Radek Štěpánek', 3, 7);

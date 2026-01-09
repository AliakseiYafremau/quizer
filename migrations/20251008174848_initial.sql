-- +goose Up
-- +goose StatementBegin
CREATE TABLE users (
    id CHAR PRIMARY KEY,
    name VARCHAR NOT NULL
);
CREATE TABLE survey (
    id CHAR PRIMARY KEY,
    name CHAR NOT NULL,
    author CHAR REFERENCES users(id),
    is_available BOOLEAN
);
CREATE TABLE questions (
    id CHAR PRIMARY KEY,
    name CHAR NOT NULL,
    survey_id CHAR REFERENCES survey(id)
);
CREATE TABLE answers (
    id CHAR PRIMARY KEY,
    user_id CHAR NOT NULL REFERENCES users(id),
    survey_id CHAR NOT NULL REFERENCES survey(id)
);
CREATE TABLE questions_options (
    id SERIAL PRIMARY KEY,
    question_id CHAR NOT NULL REFERENCES questions(id),
    value VARCHAR,
    position INT NOT NULL
);
CREATE TABLE questions_answers (
    id SERIAL PRIMARY KEY,
    answer_id CHAR NOT NULL REFERENCES answers(id),
    question_id CHAR NOT NULL REFERENCES questions(id),
    option_index INT NOT NULL
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE questions_answers;
DROP TABLE questions_options;
DROP TABLE answers;
DROP TABLE questions;
DROP TABLE survey;
DROP TABLE users;
-- +goose StatementEnd

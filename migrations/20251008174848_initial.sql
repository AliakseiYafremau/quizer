-- +goose Up
-- +goose StatementBegin
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL
);
CREATE TABLE survey (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    author VARCHAR REFERENCES users(id),
    is_available BOOLEAN
);
CREATE TABLE questions (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    survey_id VARCHAR REFERENCES survey(id)
);
CREATE TABLE answers (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL REFERENCES users(id),
    survey_id VARCHAR NOT NULL REFERENCES survey(id)
);
CREATE TABLE questions_options (
    id SERIAL PRIMARY KEY,
    question_id VARCHAR NOT NULL REFERENCES questions(id),
    value VARCHAR,
    position INT NOT NULL
);
CREATE TABLE questions_answers (
    id SERIAL PRIMARY KEY,
    answer_id VARCHAR NOT NULL REFERENCES answers(id),
    question_id VARCHAR NOT NULL REFERENCES questions(id),
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

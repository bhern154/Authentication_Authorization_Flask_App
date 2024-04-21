DROP DATABASE IF EXISTS auth_db;

CREATE DATABASE auth_db;

\c auth_db

-- - ***username*** - a unique primary key that is no longer than 20 characters.
-- - ***password*** - a not-nullable column that is text
-- - ***email*** - a not-nullable column that is unique and no longer than 50 characters.
-- - ***first_name*** - a not-nullable column that is no longer than 30 characters.
-- - ***last_name*** - a not-nullable column that is no longer than 30 characters.

CREATE TABLE "user"
(
  username VARCHAR(20) NOT NULL PRIMARY KEY,
  password TEXT NOT NULL,
  email VARCHAR(50) NOT NULL UNIQUE,
  first_name VARCHAR(30) NOT NULL,
  last_name VARCHAR(30) NOT NULL
);

-- ADD SOME DATA

INSERT INTO "user"
  (username, password, email, first_name, last_name)
VALUES
  ('potato14', 'frenchdog', 'ilovefries2@gmail.com', 'Potato', 'Head');

INSERT INTO "user"
  (username, password, email, first_name, last_name)
VALUES
  ('jewels4u', 'jasperispurpl3', 'blingbling92@gmail.com', 'Howard', 'Fern');

  -- - ***id*** - a unique primary key that is an auto incrementing integer
  -- - ***title*** - a not-nullable column that is at most 100 characters
  -- - ***content*** - a not-nullable column that is text
  -- - ***username*** - a foreign key that references the username column in the users table

CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    username VARCHAR(20) NOT NULL,
    FOREIGN KEY (username) REFERENCES "user"(username)
);

INSERT INTO feedback
  (title, content, username)
VALUES
  ('Needs Work', 'Add more details and be specific', 'potato14')

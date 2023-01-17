CREATE TABLE users (
    email VARCHAR(100) NOT NULL,  PRIMARY KEY(email),
    hash VARCHAR(122) NOT NULL,
    created_at TIMESTAMP NOT NULL
);
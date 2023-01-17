CREATE TABLE invitations (
     id VARCHAR(40) NOT NULL PRIMARY KEY,
     email VARCHAR(60) NOT NULL,
     expires_at TIMESTAMP NOT NULL
);
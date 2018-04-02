DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(60),
    first_name VARCHAR(60),
    last_name VARCHAR(60),
    email VARCHAR(255),
    date_of_birth VARCHAR(60),
    gender VARCHAR(6),
    street VARCHAR(255),
    city VARCHAR(60),
    state VARCHAR(60),
    zip VARCHAR(6),
    about VARCHAR(2047),
    theme VARCHAR(6)
);


COPY users (
        id,
        username,
        first_name,
        last_name,
        email,
        date_of_birth,
        gender,
        street,
        city,
        state,
        zip,
        about,
        theme
    )
    FROM '/vagrant/dummy-users.csv'
    WITH DELIMITER ',' CSV HEADER;

ALTER TABLE users ALTER COLUMN date_of_birth type DATE using to_date(date_of_birth, 'YYYY-MM-DD');

CLUSTER users USING users_pkey;

    
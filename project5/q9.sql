DROP TABLE IF EXISTS users2;
DROP TABLE IF EXISTS users3;

CREATE TABLE users2 (
    id INT,
    username VARCHAR(60),
    first_name VARCHAR(60),
    last_name VARCHAR(60),
    date_of_birth date,
    primary key(first_name, username)
);

CREATE TABLE users3 (
    id INT,
    username VARCHAR(60),
    first_name VARCHAR(60),
    last_name VARCHAR(60),
    date_of_brith date,
    primary key(first_name, username)
);

CLUSTER users2 using users2_pkey;
CLUSTER users3 using users3_pkey;

CREATE INDEX id_index_on_users2 ON users2 (id) with (fillfactor=50);
CREATE INDEX id_index_on_users3 ON users3 (id) with (fillfactor=50);   


DROP INDEX IF EXISTS uniq_username;
DROP INDEX IF EXISTS users_last_name;
DROP INDEX IF EXISTS users_state;
DROP INDEX IF EXISTS users_about;
DROP INDEX IF EXISTS users_date_of_birth;
DROP INDEX IF EXISTS id_index_on_users2;
DROP INDEX IF EXISTS id_index_on_users3;
DROP INDEX IF EXISTS id_index_on_q8_users2;
CLUSTER users USING users_pkey;


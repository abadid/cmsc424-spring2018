DROP TABLE IF EXISTS q8_users1;
DROP TABLE IF EXISTS q8_users2;

create table q8_users1 as select id, date_of_birth from users;
create table q8_users2 as select id, date_of_birth from users;
create index id_index_on_q8_users2 on q8_users2 (id);

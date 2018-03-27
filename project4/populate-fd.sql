drop table if exists dataset;
create table dataset(id1 float, id2 int, id3 float, id4 int, id5
float, id6 float, id7 float, id8 float, id9 float, id10 float, id11
varchar(10));
copy dataset from '/vagrant/functionaldependency/data.csv' DELIMITER ',' CSV;
create user test1 with password 'asdf';
grant all on dataset to test1;

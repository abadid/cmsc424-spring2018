#!/bin/bash

TIMEFORMAT='%3R'

sudo -u vagrant psql --quiet -d app -f drop-indexes.sql

echo -e "\n"
echo "Creating users2 and users3 tables, and their respective id indexes"
sudo -u vagrant -H -- psql --quiet -d app -f q9.sql    

echo "inserting 10000 records into the users2 table in order of the id attribute"
ct=1;
for i in `seq 1 1000`;
        do
          sudo -u vagrant -H -- psql --quiet -d app -c \
           "INSERT INTO users2 select id,username,first_name,last_name,date_of_birth from users where id >= $i*10 and id < ($i+1)*10"
          ct=$ct+1
        done

echo "inserting the same 10000 records into the users3 table in mostly random order of id" 
ct=1;
for i in `seq 1 1000 | sort -R`;
        do
          sudo -u vagrant -H -- psql --quiet -d app -c \
           "INSERT INTO users3 select id,username,first_name,last_name,date_of_birth from users where id >= $i*10 and id < ($i+1)*10"
          ct=$ct+1
        done



echo "Sizes of two first name index for each copy of the users table:"
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
sudo -u vagrant -H -- psql --quiet -d app -c \
    "ANALYZE users2; ANALYZE users3; SELECT relname as index_name, relpages as number_of_pages
     FROM pg_class
     WHERE relname like 'id%'" 


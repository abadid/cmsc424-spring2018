#!/bin/bash

TIMEFORMAT='%3R'

sudo -u vagrant psql --quiet -d app -f drop-indexes.sql
sudo -u vagrant psql --quiet -d app -f q8.sql

echo -e "\n"
echo "Question 8"
echo "-------------------------------------"
echo "Executing Q8.1..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u vagrant -H -- psql --quiet -d app -c \
    "update q8_users1 set id = (extract(year from date_of_birth)::char(4)||id::varchar(10))::int;" 


echo -e "\n\n-------------------------------------"
echo "Executing Q8.2..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u vagrant -H -- psql --quiet  -d app -c \
    "update q8_users2 set id = (extract(year from date_of_birth)::char(4)||id::varchar(10))::int;" 


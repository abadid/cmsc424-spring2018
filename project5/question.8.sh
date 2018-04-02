#!/bin/bash

TIMEFORMAT='%3R'

sudo -u vagrant psql --quiet -d app -f drop-indexes.sql

echo -e "\n"
echo "Creating UNIQUE index on username..."
sudo -u vagrant -H -- psql --quiet -d app -c \
    "CREATE UNIQUE INDEX uniq_username ON users (username);"

echo "Creating index on date_of_birth..."
sudo -u vagrant -H -- psql --quiet -d app -c \
    "CREATE INDEX users_date_of_birth ON users (date_of_birth);"

echo "Two indexes created."

echo -e "\n"
echo "Question 8"
echo "-------------------------------------"
echo "Executing Q8.1..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u vagrant -H -- psql --quiet -d app -c \
    "UPDATE users
     SET username = 'kilobyte1'
     WHERE id = '228521';" 


echo -e "\n\n-------------------------------------"
echo "Executing Q8.2..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u vagrant -H -- psql --quiet  -d app -c \
    "UPDATE users
     SET date_of_birth = date_of_birth + interval '1 year'
     WHERE id = '89976';" 

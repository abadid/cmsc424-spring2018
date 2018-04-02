#!/bin/bash

TIMEFORMAT='%3R'
echo "Question 8"
echo "-------------------------------------"

sudo -u postgres psql --quiet -f drop-indexes.sql
sudo -u postgres -H -- psql --quiet -d postgres -c \
    "CREATE UNIQUE INDEX uniq_username ON users (username);"
sudo -u postgres -H -- psql --quiet -d postgres -c \
    "CREATE INDEX users_date_of_birth ON users (date_of_birth);"

echo "Executing Q8.1..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u postgres -H -- psql --quiet -d postgres -c \
    "UPDATE users
     SET username = 'kilobyte1'
     WHERE id = '73456';" 


echo -e "\n\n-------------------------------------"
echo "Executing Q8.2..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u postgres -H -- psql --quiet  -d postgres -c \
    "UPDATE users
     SET date_of_birth = date_of_birth + interval '1 year'
     WHERE id = '89976';" 

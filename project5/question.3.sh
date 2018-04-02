#!/bin/bash

TIMEFORMAT='%3R'
echo "Question 3"
echo "-------------------------------------"

sudo -u postgres psql --quiet -f drop-indexes.sql
sudo -u postgres -H -- psql --quiet -d postgres -c \
    "CREATE INDEX users_last_name ON users (last_name);"

echo "Executing Q3.1..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u postgres -H -- psql --quiet -d postgres -c \
    "SELECT username, first_name, last_name
     FROM users
     WHERE first_name = 'Bethzy' AND last_name = 'Smith'" 


echo -e "\n\n-------------------------------------"
echo "Executing Q3.2..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u postgres -H -- psql --quiet  -d postgres -c \
    "SELECT username, first_name, last_name
     FROM users
     WHERE first_name = 'James' AND last_name = 'Giant'" 

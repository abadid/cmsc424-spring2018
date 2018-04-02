#!/bin/bash

TIMEFORMAT='%3R'
echo "Question 5"
echo "-------------------------------------"

sudo -u postgres psql --quiet -f drop-indexes.sql
sudo -u postgres -H -- psql --quiet -d postgres -c \
    "CREATE UNIQUE INDEX uniq_username ON users (username);"
sudo -u postgres -H -- psql --quiet -d postgres -c \
    "CREATE INDEX users_state ON users (state);"

echo "Executing Q5.1..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u postgres -H -- psql --quiet -d postgres -c \
    "SELECT username, first_name, last_name
     FROM users
     WHERE username = 'alchemist';" 


echo -e "\n\n-------------------------------------"
echo "Executing Q5.2..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u postgres -H -- psql --quiet  -d postgres -c \
    "SELECT *
     FROM users
     WHERE state = 'CA' AND first_name = 'Jaxson' AND last_name = 'PENNYPACKER'" 

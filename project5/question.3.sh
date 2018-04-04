#!/bin/bash

TIMEFORMAT='%3R'

sudo -u vagrant psql --quiet -d app -f drop-indexes.sql

echo -e "\n"
echo "Creating index on last_name..."
sudo -u vagrant -H -- psql --quiet -d app -c \
    "CREATE INDEX users_last_name ON users (last_name);"

echo -e "\n"
echo "Question 3"
echo "-------------------------------------"

echo "Executing Q3.1..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u vagrant -H -- psql --quiet -d app -c \
    "SELECT username, first_name, last_name
     FROM users
     WHERE first_name = 'Bethzy' AND last_name = 'Richardson'" 


echo -e "\n\n-------------------------------------"
echo "Executing Q3.2..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u vagrant -H -- psql --quiet  -d app -c \
    "SELECT username, first_name, last_name
     FROM users
     WHERE first_name = 'Patrick' AND last_name = 'Giant'" 

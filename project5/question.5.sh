#!/bin/bash

TIMEFORMAT='%3R'

sudo -u vagrant psql --quiet -d app -f drop-indexes.sql

echo -e "\n"
echo "Creating UNIQUE index on username..."
sudo -u vagrant -H -- psql --quiet -d app -c \
    "CREATE UNIQUE INDEX uniq_username ON users (username);"

echo "Creating index on state..."
sudo -u vagrant -H -- psql --quiet -d app -c \
    "CREATE INDEX users_state ON users (state);"
echo "Two indexes created."

echo -e "\n"
echo "Question 5"
echo "-------------------------------------"

echo "Executing Q5.1..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u vagrant -H -- psql --quiet -d app -c \
    "SELECT username, first_name, last_name
     FROM users
     WHERE username = 'alchemist';" 


echo -e "\n\n-------------------------------------"
echo "Executing Q5.2..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u vagrant -H -- psql --quiet  -d app -c \
    "SELECT username, first_name, last_name
     FROM users
     WHERE state = 'CA' AND first_name = 'Alan' AND last_name = 'Soto'" 

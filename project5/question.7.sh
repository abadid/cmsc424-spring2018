#!/bin/bash

TIMEFORMAT='%3R'
echo "Question 7"
echo "-------------------------------------"

sudo -u postgres psql --quiet -f drop-indexes.sql
sudo -u postgres -H -- psql --quiet -d postgres -c \
    "CREATE UNIQUE INDEX uniq_username ON users (username);"
sudo -u postgres -H -- psql --quiet -d postgres -c \
    "CREATE INDEX users_about ON users (about);"

sudo -u postgres -H -- psql --quiet -d postgres -c \
    "SELECT relname, relpages
     FROM pg_class
     WHERE relname IN ('uniq_username', 'users_about');"

echo "Executing Q7.1..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u postgres -H -- psql --quiet -d postgres -c \
    "SELECT username, first_name, last_name
     FROM users
     WHERE username = 'od' AND state = 'MD'" 


echo -e "\n\n-------------------------------------"
echo "Executing Q7.2..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u postgres -H -- psql --quiet  -d postgres -c \
    "SELECT username, first_name, last_name 
     FROM users
     WHERE about = 'I am simply a test user for Question 7.' AND state = 'MD'" 

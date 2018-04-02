#!/bin/bash

TIMEFORMAT='%3R'
echo "Question 2"
echo "-------------------------------------"

sudo -u postgres psql --quiet -f drop-indexes.sql
sudo -u postgres -H -- psql --quiet -d postgres -c \
    "CREATE UNIQUE INDEX uniq_username ON users (username);"

echo "Executing Q2.1..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u postgres -H -- psql --quiet -d postgres -c \
    "SELECT username, first_name, last_name
     FROM users
     WHERE id >= 5000 AND id < 5100;" 


echo -e "\n\n-------------------------------------"
echo "Executing Q2.2..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u postgres -H -- psql --quiet  -d postgres -c \
    "SELECT *
     FROM users 
     WHERE username LIKE 'zeus%'" 

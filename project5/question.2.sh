#!/bin/bash

TIMEFORMAT='%3R'
echo "Question 2"
echo "-------------------------------------"

sudo -u vagrant psql --quiet -d app -f drop-indexes.sql
sudo -u vagrant -H -- psql --quiet -d app -c \
    "CREATE UNIQUE INDEX uniq_username ON users (username);"

echo "Executing Q2.1..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u vagrant -H -- psql --quiet -d app -c \
    "SELECT username, first_name, last_name
     FROM users
     WHERE id >= 5000 AND id < 5100;" 


echo -e "\n\n-------------------------------------"
echo "Executing Q2.2..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u vagrant -H -- psql --quiet  -d app -c \
    "SELECT username, first_name, last_name
     FROM users 
     WHERE username LIKE 'zeus%'" 

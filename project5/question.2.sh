#!/bin/bash

TIMEFORMAT='%3R'
sudo -u vagrant psql --quiet -d app -f drop-indexes.sql

echo -e "\n"
echo "Creating UNIQUE index on username..."
sudo -u vagrant -H -- psql --quiet -d app -c \
    "CREATE UNIQUE INDEX uniq_username ON users (username);"
echo "Index created successfully."

echo -e "\n"
echo "Question 2"
echo "-------------------------------------"

echo "Executing Q2.1..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u vagrant -H -- psql --quiet -d app -c \
    "SELECT min(date_of_birth), max(date_of_birth)
     FROM users
     WHERE id >= 5000 AND id < 5100;" 


echo -e "\n\n-------------------------------------"
echo "Executing Q2.2..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u vagrant -H -- psql --quiet  -d app -c \
    "SELECT  min(date_of_birth), max(date_of_birth)
     FROM users 
     WHERE username > 'zeus' and username < 'zeut';" 

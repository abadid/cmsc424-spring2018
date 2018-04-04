#!/bin/bash

TIMEFORMAT='%3R'

sudo -u vagrant psql --quiet -d app -f drop-indexes.sql

echo "Question 1"
echo "-------------------------------------"

echo "Executing Q1.1..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u vagrant -H -- psql --quiet -d app -c \
    "SELECT username, first_name, last_name 
     FROM users 
     WHERE id = 267577;" 


echo -e "\n\n-------------------------------------"
echo "Executing Q1.2..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u vagrant -H -- psql --quiet  -d app -c \
    "SELECT username, first_name, last_name 
     FROM users 
     WHERE username = 'bristleback';" 
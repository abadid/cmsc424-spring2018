#!/bin/bash

TIMEFORMAT='%3R'
echo "Question 1"
echo "-------------------------------------"

echo "Executing Q1.1..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u postgres -H -- psql --quiet -d postgres -c \
    "SELECT username, first_name, last_name 
     FROM users 
     WHERE id = 50001;" 


echo -e "\n\n-------------------------------------"
echo "Executing Q1.2..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
time sudo -u postgres -H -- psql --quiet  -d postgres -c \
    "SELECT username, first_name, last_name 
     FROM users 
     WHERE username = 'bristleback';" 
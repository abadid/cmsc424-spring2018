#!/bin/bash

TIMEFORMAT='%3R'
echo "Question 1"
echo "-------------------------------------"

echo "Executing Q1.1..."
time sudo -u postgres -H -- psql --quiet -d postgres -c \
    "SELECT username, first_name, last_name 
     FROM users 
     LIMIT 1;" 

echo "-------------------------------------"
echo "Executing Q1.2..."
time sudo -u postgres -H -- psql --quiet  -d postgres -c \
    "SELECT username, first_name, last_name 
     FROM users 
     WHERE username = 'bristleback';" 
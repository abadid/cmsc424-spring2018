#!/bin/bash

TIMEFORMAT='%3R'

sudo -u vagrant psql --quiet -d app -f drop-indexes.sql

echo -e "\n"
echo "Creating UNIQUE index on username..."
sudo -u vagrant -H -- psql --quiet -d app -c \
    "CREATE UNIQUE INDEX uniq_username ON users (username);"

echo "Creating index on about..."
sudo -u vagrant -H -- psql --quiet -d app -c \
    "CREATE INDEX users_about ON users (about);"

echo "Two indexes created."

echo -e "\n"
echo "Question 7"
echo "-------------------------------------"
echo "Determining page sizes of each index..."
sudo -u vagrant -H -- psql --quiet -d app -c \
    "SELECT relname, relpages
     FROM pg_class
     WHERE relname IN ('uniq_username', 'users_about');"

echo -e "\n\n-------------------------------------"
echo "Executing Q7.1..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
sudo -u vagrant -H -- psql --quiet -d app -c \
    "create table tmp1 as select username from users where first_name='Aaron';" 
time sudo -u vagrant -H -- psql --quiet -d app -c \
    "select max(last_name) from users where username in (select * from tmp1);" 


echo -e "\n\n-------------------------------------"
echo "Executing Q7.2..."
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' 
sudo -u vagrant -H -- psql --quiet  -d app -c \
    "create table tmp2 as select about from users where first_name='Aaron';"
time sudo -u vagrant -H -- psql --quiet  -d app -c \
    "select max(last_name) from users where about in (select * from tmp2);" 

sudo -u vagrant -H -- psql --quiet  -d app -c \
    "drop table tmp1; drop table tmp2;"

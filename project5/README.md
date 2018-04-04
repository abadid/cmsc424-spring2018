# Project 5: Index

This project can be done in groups. There are no limits in group size, but the more you can do yourself, the more you will learn. 

The goal of this project is to give you some hands on experience converting the theory of B trees that we've been learning about in the textbook and in lecture into practice on a real database. We have provided you with a sample dataset that you will use to try out some of the queries mentioned below. Based on your understanding and experience, you will answer a few questions on ELMS, that count as the deliverable for this project. 

Most of the questions below ask you to run a shell script. These are the `question.x.sh` files in the directory, where `x` is the respective question number. Each script may set up some indexes and execute a couple of `SELECT` statements. You are to note the output of each script, as the questions are based on it. Apart from the queries that are provided by us, we encourage you to explore the dataset using `SELECT` statements of your own. This may help you to chose between the different options we give you in the multiple choice questions. You can log in to the psql instance for this project by running 'psql app' and running your queries on the command line. **Most importantly, pay careful attention to what indexes are present on the table when you work on a particular question -- the set of indexes changes from one question to another.**

## About the database
For this project, we will use a table with approximately 500K records, representing users of a web application. The table is created for you using the following SQL.

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(60),
    first_name VARCHAR(60),
    last_name VARCHAR(60),
    email VARCHAR(255),
    date_of_birth VARCHAR(60),
    gender VARCHAR(6),
    street_address VARCHAR(255),
    city VARCHAR(60),
    state VARCHAR(60),
    zip VARCHAR(6),
    about VARCHAR(2047),
    theme VARCHAR(6)
);
```


Most of the attributes should be self-explanatory. However, note the following:
- `id` and `username` are unique for every user. 
- `about` is meant to capture the bio of a user in a few sentences. However, the current values in this field are only a placeholder and will not make sense.
- Similarly, the values for `city` and `zip` are arbitrary. 
- You can think of the `theme` column as denoting some form of personalization for the user, e.g., some users might prefer a blue background when they visit your site, other might prefer gray, etc. Currently, there are 74 distinct theme values, encoded using a single character ('b', 'Y', etc.).
- **Do not assume anything about the data unless you verify it** by inspecting the given table. You are free to run any SELECT query you like to learn about the data. For example, there are about 43K zip codes in the US, however, this table has about 99K. 


We have populated the table with data in the file `dummy-users.csv` using the following command:
```sql
COPY users (
        id,
        username,
        first_name,
        last_name,
        email,
        date_of_birth,
        gender,
        street_address,
        city,
        state,
        zip,
        about,
        theme
    )
    FROM '/vagrant/dummy-users.csv'
    WITH DELIMITER ',' CSV HEADER;
```


## Exercises

If you are using a Windows machine, please run `dos2unix` as below to account for differences in line-endings. (You should only have to do this once, and then you should be fine for the rest of the project.)
```bash
dos2unix question.*.sh
```

To run a script for a question, type the following (replace `x` by the question number):
```bash
sudo bash question.x.sh
```



### Question 1
Run the file `question.1.sh` and note its output. **No new indexes are created when you run this script.**

This file runs two queries on the `users` table. The first query is (Q1.1):
```sql
SELECT username, first_name, last_name
FROM users
WHERE id = 267577;
```

And the second query is (Q1.2):
```sql
SELECT username, first_name, last_name
FROM users
WHERE username = 'bristleback';
```

If you notice the output, both queries return the same user. However, the first one finishes in much less time than the second. Why? If more than one answer is correct, choose the best of the correct answers:
- [ ] This is arbitrary. If we change the constant value in the where clause, the results could be substantially different.
- [ ] There is an index on `id` because it is declared as a `PRIMARY KEY`. 
- [ ] Comparing strings is slower than comparing integers.
- [ ] The first query ran earlier, so the table is still in the cache at the time that it ran. 
- [ ] The id attribute appears before the username attribute in the table declaration, so it is faster to extract the id of a tuple than the username.


### Question 2
Run the file `question.2.sh` and note its output. This script creates a UNIQUE index on the `username` attribute using the following command:
```sql
CREATE UNIQUE INDEX uniq_username ON users (username);
```

For more detail, see [https://www.postgresql.org/docs/9.6/static/indexes-unique.html](https://www.postgresql.org/docs/9.6/static/indexes-unique.html)

After creating the index, we run two queries on the table. 

The first query is (Q2.1):
```sql
SELECT min(date_of_birth), max(date_of_birth)
FROM users
WHERE id >= 5000 AND id < 5100;
```

And the second query is (Q2.2):
```sql
SELECT min(date_of_birth), max(date_of_birth)
FROM users 
WHERE username > 'zeus' and username < 'zeut';
```

Although the WHERE clause of both queries select the same number of tuples (100 tuples), and there is an index on both `id` and `username`, why does the first query finish in less time than the second one?
- [ ] The WHERE clauses actually returns a different set of 100 tuples. It is the particular set of 100 tuples returned by Q2.2 that makes second query slow. 
- [ ] Records are clustered according to `id`. Therefore the index on id is primary and the index on username is secondary. Range predicates are usually faster on primary indexes.
- [ ] The `username` index is on a string. Indexes on strings are much less useful than indexes on integers. 
- [ ] Indexes on strings cannot be used for range predicates.
- [ ] The table is sorted on id, therefore the index on id is unnecessary.



### Question 3
This is a two part question. Run the file `question.3.sh` and note its output. **After executing this script, apart from the table definition, only following index is present.**

We want to find users efficiently by their name. As a first step, we add an index on `last_name` using the command:
```sql
CREATE INDEX users_last_name ON users (last_name);
```

 
**Part I:**
This shell script runs the following two queries on the `users` table.

Query 3.1:
```sql
SELECT username, first_name, last_name
FROM users
WHERE first_name = 'Bethzy' AND last_name = 'Richardson'
```

Query 3.2:
```sql
SELECT username, first_name, last_name
FROM users
WHERE first_name = 'Patrick' AND last_name = 'Giant'
```

Both queries find one user in the table. However, the first one takes longer. Why? (Choose the best answer).
- [ ] In the index, the record for 'Patrick Giant' appears much earlier than the record for 'Bethzy Richardson', and hence PostgreSQL found it earlier.
- [ ] The `id` of 'Patrick Giant' is much smaller than the `id` of 'Bethzy Richardson'. Hence PostgreSQL found it earlier.
- [ ] There are many more users having last name 'Richardson' compared to 'Giant', so the index is less helpful.
- [ ] The Postgres developers were misogynists, and biased the system to find males faster than females.
- [ ] 'Giant' is a shorter string than 'Richardson'. Therefore, the string comparison operations that happen when traversing the index are faster.


**Part 2:** Suppose instead of creating an index on `last_name`, we created it on `first_name`. Based on your understanding so far, what can you say about the run time of the two queries above, and why?
- [ ] Both queries will take the same time since the B-tree on last name will be balanced.
- [ ] There will be no change, we will observe similar behavior as before
- [ ] The behaviour will be flipped, Q3.2 will take more time than Q3.1


### Question 4

Before you do this part, read section 11.5.2 from your textbook (it should be a tiny bit more than a single page). The main thing you need to know is that the concatenation of multiple attributes can be indexed the same way as an index on a single attribute. This is called a "multi-column index". Suppose instead of creating separate indexes on one of `first_name` or `last_name`, we create a _multicolumn_ index containing both attributes (i.e. a concatenation of both attributes). Specifically, we could create the following index (although we do not imclude a script that does this):
```sql
CREATE INDEX users_first_last_name ON users (first_name, last_name);
```

Which of the following queries would be good candidates for using our new index?
- [ ] Query 4.1:
```sql
SELECT username, first_name, last_name
FROM users
WHERE first_name = 'Bethzy' AND last_name = 'Smith'
```

- [ ] Query 4.2:
```sql
SELECT username, first_name, last_name
FROM users
WHERE last_name = 'Giant'
```

- [ ] Query 4.3:
```sql
SELECT username, first_name, last_name
FROM users
WHERE first_name = 'Jaxson'
```

- [ ] Query 4.4:
```sql
SELECT username, first_name, last_name
FROM users
WHERE first_name LIKE 'Jord%'
```

- [ ] Query 4.5:
```sql
SELECT username, first_name, last_name
FROM users
WHERE last_name LIKE 'Jord%'
```


### Question 5
Run the file `question.5.sh` and note its output. For this part, we create an index on `state` using the following command.
```sql
CREATE INDEX users_state ON users (state);
```
Apart from the above index, we also create a `UNIQUE` index on `username` as before (in Question 2).

We then run the following two queries:

Query 5.1
```sql
SELECT username, first_name, last_name
FROM users
WHERE username = 'alchemist';
```

Query 5.2
```sql
SELECT username, first_name, last_name
FROM users
WHERE state = 'CA' AND first_name = 'Alan' AND last_name = 'Soto'
```

Both queries return the same user record and can make use of at least one index. However, the second query takes longer to run than the first, why? (Choose the best answer):

- [ ] Q5.2 compares three column values for every user, whereas Q5.1 compares only one.
- [ ] Usernames are larger (in terms of number of bytes) than states. Therefore the index on username is more helpful.
- [ ] There are many user records that have `state = 'CA'`, so the index on `state` is not particularly helpful.
- [ ] The table is sorted by username; therefore selection predicates on username are faster.



### Question 6
Suppose we want to run many queries of the following type:
```sql
SELECT username, first_name, last_name
FROM users
WHERE date_of_birth >= '1990-01-01' AND date_of_birth <= '1990-02-01'
    AND theme = 'B'
```
However, each query will have different constant values for the date_of_birth predicate (but with a similar date range of about a month) and different constant values for theme as well. 

Which one of the following indexes would be most helpful?
- [ ] 1.
```sql
CREATE INDEX users_dob ON users (date_of_birth);
```
- [ ] 2.
```sql
CREATE INDEX users_theme ON users (theme);
```
- [ ] 3.
```sql
CREATE INDEX users_theme_dob ON users (theme, date_of_birth);
```
- [ ] 4.
```sql
CREATE INDEX users_dob_theme ON users (date_of_birth, theme);
```


### Question 7
Run the file `question.7.sh` and note its output. In this part, we want to find users by their `about` description, and we decide to create an index on it.
```sql
CREATE INDEX users_about ON users (about);
```

In addition, we also create a `UNIQUE` index on `username` as before. 

Then we run the following query to determine the size of each index, in terms of the number of disk pages:
```sql
SELECT relname, relpages
FROM pg_class
WHERE relname IN ('uniq_username', 'users_about');
```

Then we create two temporary tables via running a select statement and putting the results in the newly created tables:
```sql
create table tmp1 as select username from users where first_name='Aaron';
create table tmp2 as select about from users where first_name='Aaron';
```


Finally the script runs the following two queries, that both return the same value:

Query 7.1
```sql
select max(last_name) from users where username in (select * from tmp1);
```

Query 7.2
```sql
select max(last_name) from users where about in (select * from tmp2);
```

Why is Q7.2 slower than Q7.1?
- [ ] The cost to use the index on the about attribute is larger than the cost to use the index on the username attribute, since the index is larger and the search keys are larger.
- [ ] Although the value returned is the same, that is because this is an aggregate. The set of of records that are read from the users table are different. In particular, Q7.2 has to read more records.
- [ ] PostgreSQL knows to stop when it finds one record in Q7.1, because there is a `UNIQUE` index on `username`. However, because the index on `about` is not unique, it reads more records than necessary.
- [ ] The 'username' attribute appears first in the record, before the 'about' attribute. Therefore, the cost of extracting the 'about' attribute is larger than the cost of extracting the 'username' attribute from each record in users.


### Question 8
Run the file `question.8.sh` and note its output. For this part, we will measure the performance of `UPDATE` statements when indexes are present.

We start by running 3 SQL commands:

```sql
create table q8_users1 as select id, date_of_birth from users;
create table q8_users2 as select id, date_of_birth from users;
create index id_index_on_q8_users2 on q8_users2 (id);
```

Note that q8\_users1 has no indexes, and q8\_users2 has a single index on id.

Then we run the following queries:

Query 8.1
```sql
update q8_users1 set id = (extract(year from date_of_birth)::char(4)||id::varchar(10))::int;
```

Query 8.2
```sql
update q8_users2 set id = (extract(year from date_of_birth)::char(4)||id::varchar(10))::int;
```

Both queries update the id value of every single tuple in the table by concatening the year of birth with the old id. Don't worry about all of the type casting in the query --- you can trust that it works correctly. The main thing to note is that every single id value changes. 

Why does Q8.2 run slower than Q8.1?
- [ ] Q8.2 runs after Q8.1 and the CPU on my computer slows down over time. 
- [ ] q8_users1 is smaller than q8_users2 since it doesn't have an index. Therefore q8_users1 blocks are more likely to be in cache or memory than q8_users2 blocks (which are more likely to be on disk).
- [ ] Because we didn't create an index on q8_users1, it automatically created an index on its primary key. This index helps to accelerate the update statements.
- [ ] The update in Q8.2 is more expensive because the index has to be updated as well.

### Question 9
Run the file `question.9.sh` and note its output. For this part, we will measure how index size is based on `INSERT` patterns.

We start by running the following SQL commands:

```sql
CREATE TABLE users2 (
    id INT,
    username VARCHAR(60),
    first_name VARCHAR(60),
    last_name VARCHAR(60),
    date_of_birth date,
    primary key(first_name, username)
);

CREATE TABLE users3 (
    id INT,
    username VARCHAR(60),
    first_name VARCHAR(60),
    last_name VARCHAR(60),
    date_of_brith date,
    primary key(first_name, username)
);

CLUSTER users2 using users2_pkey;
CLUSTER users3 using users3_pkey;

CREATE INDEX id_index_on_users2 ON users2 (id) with (fillfactor=50);
CREATE INDEX id_index_on_users3 ON users3 (id) with (fillfactor=50);
```

Note that users2 and users3 have an identical schema. Note that the primary key is composed of both the first_name and username, and that the tables are clustered (sorted) by the primary key. After we create the tables and declare the sort order, we then create an index on the id attribute for each table (the index is the same for each of them). (The fillfactor part of the statement makes the index insertion algorithm more similar to the description in your textbook and in lecture --- index nodes must be between half full and totally full).  

After we do this, we extract all tuples with id in between 10 and 10009 from the users table, and insert the id, username, first and last name, and date of birth from these tuples into the users2 and users3 tables. The only difference with the way that this insert is done is that for the users2 table, the tuples are inserted in sorted order by the id attribute (each tuple that is inserted has a higher id than the previous one). However, for the users3 table, the tuples are inserted in a more random order. You can look at the bash script for how this is done if you want to, but looking at the script is unlikely to help you more than just focusing on the main point: tuples are inserted in sorted order by id for users2 and (mostly) random order for users3. 

After doing all of the tuple insertions, the script then prints the size of each index. Surprisingly, the index for which insertions happened in sorted order is *larger* than the the index for which insertions happened in *random* order. Please use your understanding of how insertions into indexes work from the textbook and the lectures this semester to explain why there is a size difference between the two indexes. (Write your response in the last question on the quiz on Elms). 


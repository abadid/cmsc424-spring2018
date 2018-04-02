# Project 5: Index

The goal of this project is to introduce you to one of the most common index type in databases -- the B-tree. We have provided you with a toy database that you will use to try out some of the queries mentioned below. Based on your understanding and experience, you will answer a few questions on ELMS, that count as the deliverable for this project. 

Each question below asks you to run a shell script. These are the `question.x.sh` files in the directory, where `x` is the respective question number. Each script may set up some indexes and execute a couple of `SELECT` statements. You are to note the output of each script, as the questions are based on it. Apart from the queries that are provided by us, we encourage you to explore the dataset using `SELECT` statements of your own. It will help you verify your understanding. **Most importantly, pay careful attention to what indexes are present on the table when you work on a particular question -- the set of indexes changes from one question to another.**

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

To run a file, type the following (replace `x` by the question number):
```bash
sudo bash question.x.sh
```


### Question 1
Run the file `question.1.sh` and note its output. **No new indexes are created when you run this script.**

This file runs two queries on the `users` table. The first query is (Q1.1):
```sql
SELECT username, first_name, last_name
FROM users
WHERE id = 1005;
```

And the second query is (Q1.2):
```sql
SELECT username, first_name, last_name
FROM users
WHERE username = 'bristleback';
```

If you notice the output, both queries return the same user. However, the first one finishes in much less time than the second. Why? Select one that is most appropriate in this context.
- [ ] This is arbitrary; in general, both will take similar time to execute.
- [ ] There is an index on `id` because it is declared as a `PRIMARY KEY`. 
- [ ] Comparing strings is slower than comparing integers.
- [ ] 




### Question 2
Run the file `question.2.sh` and note its output. This script creates a UNIQUE index on the `username` attribute using the following command:
```sql
CREATE UNIQUE INDEX uniq_username ON users (username);
```

For more detail, see [https://www.postgresql.org/docs/9.6/static/indexes-unique.html](https://www.postgresql.org/docs/9.6/static/indexes-unique.html)

After creating the index, we run two queries on the table and both return 100 user records. The first query is (Q2.1):
```sql
SELECT min(date_of_birth), max(date_of_birth)
FROM users
WHERE id >= 5000 AND id < 5100;
```

And the second query is (Q2.2):
```sql
SELECT min(date_of_birth), max(date_of_birth)
FROM users 
WHERE username LIKE "zeus%"
```

Although the result sizes are the same, and there is an index on `username`, why does the first query finish in less time than the second one?
- [ ] We got lucky; in general, both will run in the same amount of time.
- [ ] Records are clustered according to `id`
- [ ] PostgreSQL cannot use the index on `username` for a pattern matching operation as in Q2.2


Answer the following questions based on your understanding so far.

For which of the follwing queries, the index on `username` helps?
- [ ] `select * from users where username like '%hero%'`
- [ ] `select * from users where username like '%hero'`
- [ ] `select * from users where username like 'hero%`
- [ ] `select * from users where username = 'hero'`

Suppose we run the following command:
```sql
CLUSTER users USING uniq_username;
```
See [https://www.postgresql.org/docs/9.6/static/sql-cluster.html](https://www.postgresql.org/docs/9.6/static/sql-cluster.html) for details.

If we were to execute (Q2.1) and (Q2.2) again, how will the results change?
- [ ] There will be no change, we will observe similar behavior as before
- [ ] The 
- [ ] Both will take the same time


### Question 3
This is a two part question. Run the file `question.3.sh` and note its output. **After executing this script, apart from the table definition, only following index is present.**

We want to find users efficiently by their name. As a first step, we add an index on `last_name` using the command:
```sql
CREATE INDEX users_last_name ON users (last_name);
```

 
**Part I:**
This file runs the following two queries on the `users` table.

Query 3.1:
```sql
SELECT username, first_name, last_name
FROM users
WHERE first_name = "Bethzy" AND last_name = "Richardson"
```

Query 3.2:
```sql
SELECT username, first_name, last_name
FROM users
WHERE first_name = "Patrick" AND last_name = "Giant"
```

Both queries find one user in the table. However, the first one takes longer. Why?
- [ ] On disk, the record for 'Bethzy Smith' appears much before the record for 'James Giant', and PostgreSQL found it earlier in the scan.
- [ ] Postgres used the index `users_last_name` for Q3.2 but not for Q3.1
- [ ] There are many users having last name "Smith" compared to "Giant"


**Part 2:** Suppose instead of creating an index on `last_name`, we created it on `first_name`. Based on your understanding so far, what can you say about the run time of the two queries above, and why?
- [ ] No change
- [ ] Same time for both
- [ ] Flipped


### Question 4

Suppose instead of creating separate indexes on one of `first_name` or `last_name`, we create a _multicolumn_ index containing both attributes. Specifically, we create the following index:
```sql
CREATE INDEX users_first_last_name ON users (first_name, last_name);
```

For which of the following three queries, would the index help?
- [ ] Query 4.1:
```sql
SELECT username, first_name, last_name
FROM users
WHERE first_name = "Bethzy" AND last_name = "Smith"
```

- [ ] Query 3.2:
```sql
SELECT username, first_name, last_name
FROM users
WHERE last_name = "Giant"
```

- [ ] Query 3.3:
```sql
SELECT username, first_name, last_name
FROM users
WHERE first_name = "Jaxson"
```

- [ ] Query 3.4:
```sql
SELECT username, first_name, last_name
FROM users
WHERE first_name LIKE "Jord%"
```

- [ ] Query 3.5:
```sql
SELECT username, first_name, last_name
FROM users
WHERE last_name LIKE "Jord%"
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
WHERE username = "alchemist";
```

Query 5.2
```sql
SELECT username, first_name, last_name
FROM users
WHERE state = "CA" AND first_name = "Alan" AND last_name = "Soto"
```

Both queries return the same user record. We also have an index on `username` and on `state`. However, the second query takes longer to run than the first, why?

- [ ] Q5.2 compares three column values for every user, whereas Q5.1 compares only one.
- [ ] PostgreSQL knows that there is a UNIQUE index on `username`, hence it returns as soon as it finds one record in Q5.1. However, in Q5.2, it cannot do so, as the index on `state` is not unique.
- [ ] There are many user records that have `state = 'CA'`, so the index on `state` is not helpful.



### Question 6
Suppose we want to run many queries of the following type:
```sql
SELECT username, first_name, last_name
FROM users
WHERE date_of_birth >= '1990-01-01' AND date_of_birth <= '1990-02-01'
    AND theme = 'B'
```
Assume that the range for `date_of_birth` is around a month (25-35 days). 

Which one of the following index would be most helpful?
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

Finally the script runs the following two queries, that both return the same user, but Q7.2 is slower than Q7.1. Why?
Query 7.1
```sql
SELECT username, first_name, last_name 
FROM users
WHERE username = 'od' AND state = 'MD'
```

Query 7.2
```sql
SELECT username, first_name, last_name 
FROM users
WHERE about = 'I am simply a test user for Question 7.' AND state = 'MD'
```

- [ ] This is arbitrary; in general, we cannot say for certain that one will be faster than another.
- [ ] There are more disk seeks when using the index in Q7.2 compared to Q7.1
- [ ] PostgreSQL knows to stop when it finds one record in Q7.1, because there is a `UNIQUE` index on `username`. However, because the index on `about` is not unique, it reads more records than necessary.


### Question 8
Run the file `question.8.sh` and note its output. For this part, we will measure the performance of `UPDATE` statements when indexes are present.

We start with creating two indexes, a `UNIQUE` index on `username`, and an index on `date_of_birth`. Then we run the following queries:

Query 8.1
```sql
UPDATE users
SET username = 'kilobyte1'
WHERE id = '73456';
```

Query 8.2
```sql
UPDATE users
SET date_of_birth = date_of_birth + interval '1 year'
WHERE id = '89976';
```

Both queries find a user by id, and update one column in the found record. However, Q8.2 runs slower than Q8.1. Why?
- [ ] In Q8.1, the new value (for `username`) is readily available, however, we need to calculate the new value (for `date_of_birth`) in Q8.2
- [ ] Updating strings is faster than updating dates
- [ ] Q8.1 does not have to update the index on `username`, whereas Q8.2 has to update the index on `date_of_birth`.
- [ ] We got lucky in this instance, index update in Q8.1 finished earlier than Q8.2. 




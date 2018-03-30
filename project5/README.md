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
sudo sh ./question.x.sh
```


### Question 1
Run the file `question.1.sh` and note its output. **No new indexes are created when you run this script.**

This file runs two queries on the `users` table. The first query is (Q1.1):
```sql
SELECT *
FROM users
WHERE id = 1005;
```

And the second query is (Q1.2):
```sql
SELECT *
FROM users
WHERE username = 'bristleback';
```

If you notice the output, both queries return the same user. However, the first one finishes in much less time than the second. Why? Select one that is most appropriate in this context.
- [ ] We got lucky; in general, both will run in the same amount of time
- [ ] There is an index on `id`
- [ ] Comparing strings is slower than comparing integers.



### Question 2
Run the file `question.2.sh` and note its output. This script creates a UNIQUE index on the `username` attribute using the following command:
```sql
CREATE UNIQUE INDEX uniq_username ON users (username);
```

For more detail, see [https://www.postgresql.org/docs/9.6/static/indexes-unique.html](https://www.postgresql.org/docs/9.6/static/indexes-unique.html)

After creating the index, we run two queries on the table and both return 100 user records. The first query is (Q2.1):
```sql
SELECT *
FROM users
WHERE id >= 5000 AND id < 5100;
```

And the second query is (Q2.2):
```sql
SELECT *
FROM users 
WHERE username LIKE "zeus%"
```

Although the result sizes are the same, and there is an index on `username`, why does the first query finish in less time than the second one?
- [ ] We got lucky; in general, both will run in the same amount of time.
- [ ] Records are clustered according to `id`
- [ ] Q2.2 is not using the index on `username` at all


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
- [ ] No change
- [ ] Execution times flipped
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
SELECT *
FROM users
WHERE first_name = "Bethzy" AND last_name = "Smith"
```

Query 3.2:
```sql
SELECT *
FROM users
WHERE first_name = "James" AND last_name = "Giant"
```

Both queries find one user in the table. However, the first one takes longer. Why?
- [ ] On disk, the record for 'Bethzy Smith' appears much before the record for 'James Giant'.
- [ ] Postgres used the index `users_last_name` for Q3.2 but not for Q3.1
- [ ] There are many users having last name "Smith" compared to "Giant"


**Part 2:** Suppose instead of creating an index on `last_name`, we created it on `first_name`. Based on your understanding so far, what can you say about the run time of the two queries above, and why?
- [ ] No change
- [ ] Same time for both
- [ ] Flipped

_runtimes should flip -- James is a common first name, Bethzy is very uncommon for a first name_



### Question 4

Suppose instead of creating separate indexes on one of `first_name` or `last_name`, we create a _multicolumn_ index containing both attributes. Specifically, we create the following index:
```sql
CREATE INDEX users_first_last_name ON users (first_name, last_name);
```

For which of the following three queries, would the index help?
- [ ] Query 4.1:
```sql
SELECT *
FROM users
WHERE first_name = "Bethzy" AND last_name = "Smith"
```

- [ ] Query 3.2:
```sql
SELECT *
FROM users
WHERE last_name = "Giant"
```

- [ ] Query 3.3:
```sql
SELECT *
FROM users
WHERE first_name = "Jaxson"
```


### Question 5
Run the file `question.5.sh` and note its output. For this part, we create an index on `state` using the following command.
```sql
CREATE INDEX users_state ON users (state);
```

Apart from the above, we also create a `UNIQUE` index on `username` as before.

We then run the following two queries:

Query 5.1
```sql
SELECT *
FROM users
WHERE username = "alchemist";
```

Query 5.2
```sql
SELECT *
FROM users
WHERE state = "CA" AND first_name = "Jaxson" AND last_name = "PENNYPACKER"
```

Both queries return the same user record. We also have an index on `username` and on `state`. However, the second query takes longer to run than the first, why?

**TODO: MCQ**



### Question 6
Suppose we want to run many queries of the following type:
```sql
SELECT *
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


### Question 6
Run the file `question.5.sh` and note its output. In this part, we want to find users by their `about` description, and we decide to create an index on it.
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

**TODO: Explain the output?**

Finally the script runs the following two queries, that both return the same user, but Q6.2 is slower than Q6.1. Why?
Query 6.1
```sql
SELECT * 
FROM users
WHERE username = 'od'
```

```sql
SELECT * 
FROM users
WHERE username = 'Their sanity I will shatter, their dreams of conquest I will destroy.'
```

**TODO : MCQ**



### Question 7

Update performance.


### Misc
Clear page cache on linux before running every query:
```bash
echo 3 | sudo tee /proc/sys/vm/drop_caches
```

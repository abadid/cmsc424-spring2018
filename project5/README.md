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
- `about` is meant to capture the bio of a user in a few sentences. However, the current values for this field will not make sense, as it is meant to be a placeholder.
- Similarly `city` and `zip` values will not make sense. 
- You can think of the `theme` column as denoting some form of personalization for the user, e.g., some users might prefer a blue background when they visit your site, other might prefer gray, etc. Currently, there are 74 distinct theme values, encoded using a single character.
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
- [] We got lucky, in general, both will run in the same amount of time
- [] There is an index on `id`
- [] Comparing strings is slower than comparing integers.



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
- [] We got lucky, in general, both will run in the same amount of time.
- [] Records are clustered according to `id`
- [] Q2.2 is not using the index on `username` at all


Answer the following questions based on your understanding so far.

For which of the follwing queries, the index on `username` helps?
- `select * from users where username like '%hero%'`
- `select * from users where username like '%hero'`
- `select * from users where username like 'hero%`
- `select * from users where username = 'hero'`

Suppose we run the following command:
```sql
CLUSTER users USING uniq_username;
```
See [https://www.postgresql.org/docs/9.6/static/sql-cluster.html](https://www.postgresql.org/docs/9.6/static/sql-cluster.html) for details.

If we were to execute (Q2.1) and (Q2.2) again, how will the results change?
- [] No change
- [] Execution times flipped
- [] Both will take the same time


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
**TODO: MCQ**

**Part 2:** Suppose instead of creating an index on `last_name`, we created it on `first_name`. Based on your understanding so far, what can you say about the run time of the two queries above, and why?

_runtimes should flip -- James is a common first name, Bethzy is very uncommon for a first name_



### Question 4
Next, we will drop the index on `last_name`, and instead create one on `first_name, last_name` together. Specifically, we create the following index:
```sql
CREATE INDEX users_first_last_name ON users (first_name, last_name);
```

For which of the following three queries, the index would help?

Query 4.1:
```sql
SELECT *
FROM users
WHERE first_name = "Bethzy" AND last_name = "Smith"
```

Query 3.2:
```sql
SELECT *
FROM users
WHERE last_name = "Giant"
```

Query 3.3:
```sql
SELECT *
FROM users
WHERE first_name = "Jaxson"
```


### Question 5
For this part, we will create an index on `state` using the following command.
```sql
CREATE INDEX users_state ON users (state);
```

Note that apart from the above index, at this point there is only one more B-tree index on `username`.

Run the file `question.5.sh` and note its output.

This file runs two queries:

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
Bigger sized keys in index, possibly a text column? See dataset available at (https://www.kaggle.com/zynicide/wine-reviews/data)[https://www.kaggle.com/zynicide/wine-reviews/data].



### Misc
Clear page cache on linux before running every query:
```bash
echo 3 | sudo tee /proc/sys/vm/drop_caches
```

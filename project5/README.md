# Project 5: Index

The goal of this project is to introduce you to one of the most common index type in databases -- B-tree. We have provided you with a toy database that you will use to try out some of the queries mentioned below. Based on your understanding and experience, you will answer a few questions on ELMS, that count as the deliverable for this project. 

Note that apart from the queries that you are required to run in order to answer the questions, we also encourage you to explore the dataset using SELECT queries of your own. It will help you verfiy your understanding.

## About the database
For this project, we will use a table with XXX records, representing users of a web application. The table is created for you using the following SQL.

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(60),
    first_name VARCHAR(60),
    last_name VARCHAR(60),
    email VARCHAR(120),
    gender VARCHAR(6),
    street_address VARCHAR(360),
    state VARCHAR(60),
    zip VARCHAR(6),
    last_login TIMESTAMP,
    created_at TIMESTAMP
);
```

We have populated the table with XXX user records using the command:
```sql
COPY users (
        id,
        username,
        first_name,
        last_name,
        email,
        gender,
        street_address,
        state,
        zip,
        last_login,
        created_at
    )
    FROM '/vagrant/dummy-users.csv'
    DELIMITER ',';
```


## Exercises


### Question 1
Run the file `question.1.sh` and note its output.

This file runs two queries on the `users` table. The first query is:
```sql
SELECT *
FROM users
WHERE id = 1005;
```

The second query is:
```sql
SELECT *
FROM users
WHERE username = "bristleback";
```

If you notice the output, both queries return the same user. However, the first one finishes in much less time than the second. Why?

**TODO: Multiple choice Q?** 



We will now create an index on `username` using the following command:
```sql
CREATE UNIQUE INDEX uniq_username ON users (username);
```

*Maybe: We encourage you to try out running `question.1.sh` and see if creating the index made any difference*

### Question 2
Run the file `question.2.sh` and note its output.

This file also runs two queries on the `users` table, and both queries return 100 user records. The first query is:
```sql
SELECT *
FROM users
WHERE id >= 5000 AND id < 5100;
```

The second query is:
```sql
SELECT *
FROM users 
WHERE username LIKE "zeus%"
LIMIT 100;
```

Although the result sizes are the same, why does the first query finish in less time than the second one?

**TODO: MCQ**


### Question 3
This is a two part question.

**Part I:** Now that we know that adding indexes improves retrieval time, lets add another index on `last_name`, so that we can efficiently find users by name.
```sql
CREATE INDEX users_last_name ON users (last_name);
```

Run the file `question.3.sh` and note its output.

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
## Project 2: Advanced SQL Assignment, CMSC424, Spring 2018

*The assignment is to be done by yourself.*

Please do a `git pull` to download the directory `project2`. The files are:

1. README.md: This file
1. small.sql: SQL script for populating `flights` database.
1. queries.py: The file where to enter your answer for Q1; this file has to be submitted
1. answers.py: The answers to query Q1 and Q3.
1. answers.txt: The answers to queries Q2 and Q3.
1. SQLTesting.py: File to be used for testing your SQL submission -- see below 
1. table4storedproc.sql: SQL script for populating `stpc` database.
1. trigger-database.sql: SQL script for setting up the `flightsales` database.
1. trigger-test.py: Python script for testing the trigger.
1. Vagrantfile: Vagrantfile that creates the required databases and populates some of them.

### Getting started
Start the VM with `vagrant up` in the `project2/` directory. The databases `flights` and `stpc` should already be set up. The `flightsales` database is already created for you, but you need to populate it explicitly. 

### Testing and submitting using SQLTesting.py
- Your answers (i.e., SQL queries) should be added to the `queries.py` file similar to Project 1. You are also provided with a Python file `SQLTesting.py` for testing your answers.

- We recommend that you use `psql` to design your queries, and then paste the queries to the `queries.py` file, and confirm it works.

- SQLTesting takes quite a few options: use `python SQLTesting.py -h` to see the options.

- If you want to test your answer to Question 1, use: `python SQLTesting.py -dbname flights -q 1`. The program compares the result of running your query against the provided answer (in the `answers.py` file).

- The -v flag will print out more information, including the correct and submitted answers etc.

### Submission Instructions
- Submit your answers to Q1 in `queries.py`
- Submit your answers to Q2, Q3 in `answers.txt`
- Submit your answer to Q4 in `trigger.sql`

<br />


**Q1 (5pt)**. [Outer Join] Write a query that uses an outer join to list all the flights that flew empty on August 5, 2016. [Output Column: `flightid`]

**Q2 (8pt)**. [Outer Join] We will write a query using outer joins to find all the customers who satisfy all the following conditions <br />
  1. are born in or after 1996, and <br />
  1. have taken a flight at least once, and <br />
  1. have never taken a flight in or out of ‘ORD’.

Note that your query should **only use** the following views which are defined as:

```
create view customer_flight as
select distinct c.customerid as cid, flightid
from customers c, flewon f
where c.customerid = f.customerid and extract(year from birthdate) >= 1996
order by cid, flightid;
	
create view flight_ORD as
select flightid from flights
where source = 'ORD' or dest = 'ORD'
order by flightid;
```

The `customer_flight` view lists all the customers who are born in or after 1996 and the flightid of the flights that the customer has taken. The `flight_ORD` view lists all the flights that fly in or out of ORD.

```
with temp as (
select distinct cid, v2.flightid as afid
from customer_flight v1 left outer join flight_ORD v2
on v1.flightid = v2.flightid
order by cid
)
select cid
from temp
group by cid
having count(*)=1
order by cid;
```

Does the query always produce the correct output? Explain. If not, modify the above query to produce the correct output. If you modify the query, you can only change the having clause. Right now it says: `having count(*)= 1`. You can change it to say: `having count(*) = 1 AND exists (<write your expression here>)`. You cannot change any other part of the query.

**Q3 (13pt)**.[PL/pgSQL Functions] PL/pgSQL is a procedural language for the PostgreSQL database system that can be used to create functions and trigger procedures. In this assignment we will use PL/pgSQL to perform complex computations that are otherwise not straigtforward using SQL queries.

To begin with this, you must switch to `stpc` and load the data using `\i table4storedproc.sql`. You are provided with an initial table `inittab` and you are required to generate new table `finaltab`, where the count attribute in ```finaltab``` is transformed according to the following transformation rule:

```
finaltab.tcount(i) = inittab.tcount(i) + inittab.tcount(i-1), where i is the ith row in the table
```

The rule above implies that the value of tcount of the ith row in ```finaltab``` is the sum of the ith row and the one before it in ```inittab```. For the first row, we just make a copy of it. An example is provided below:

| transid | tcount |  
|:---:|:---:| 
| 12 | 10 | 
| 23 | 20 | 
| 15 | 30 |
| 2  | 10 | 

`inittab`

| transid | tcount |  
|:---:|:---:| 
| 12 | 10 | 
| 23 | 30 | 
| 15 | 50 |
| 2  | 40 | 

`finaltab`

**Part I**: (i) Write a PL/pgSQL function `function1()` using the procedural language in Postgres to generate `finaltab`. You may want to start with the PL/pgSQL example from class on Feb 21 in order to get started. As far as the definition of the "ith row" in the table for the calculation mentioned above, you can assume that this is the same as the ith row that is encountered in a ```FOR LOOP``` in PL/pgSQL that iterates through (```SELECT * FROM inittab```). For this part, you are required to create the `finaltab` table within the function and insert the required tuples into it. Your function should not return anything. We will test it by invoking `SELECT function1();`



Here is a more involved transformation rule:

```
finaltab2.tcount(i) = sum of the values of tcount attribute in inittab from row i to row (i-inittab.transid(i)), 
if (i-inittab.transid(i)) < 1, then we sum the values up to row 1
```
For example, this transformation rule, when applied to the ```inittab``` from above, would produce the result:

| transid | tcount |  
|:---:|:---:| 
| 12 | 10 | 
| 23 | 30 | 
| 15 | 60 |
| 2  | 60 | 

`finaltab2`

**Part II**: Write a PL/pgSQL function `function2()` to generate `finaltab2`. Just like part I, you are required to create the `finaltab2` table within the function and insert the required tuples into it. Your function should not return anything. We will test it by invoking `SELECT function2();` Again, you can assume that the definition of the "ith row" in the table for the calculation mentioned above is the same as the ith row that is encountered in a ```FOR LOOP``` in PL/pgSQL that iterates through (```SELECT * FROM inittab```)

The following links contain some useful documentation on PL/pgSQL: <br />
1. https://www.postgresql.org/docs/9.2/static/plpgsql.html
1. https://www.postgresql.org/docs/9.2/static/plpgsql-control-structures.html 
1. https://stackoverflow.com/questions/30786295/postgres-unassigned-record-is-there-a-way-to-test-for-null


**Q4 (14pt)**.[Trigger] For this problem, we’ll be using a new hypothetical database `flightsales`, that has all the tables in the `flights` database except that the `flewon` table is replaced with the `ticketsales` table. The table `ticketsales (ticketid, flightid, customerid, salesdate)` in the `flightsales` database records the ticket sales transactions. To keep things simple, we will assume that every customer always makes a single ticket purchase for a given flight at a time. We want the ability to keep track of the total number of ticket sales per airline company in the table `airlinesales (airlineid, total_ticket_sales)`.  We use the following command to create this table:

```
create table airlinesales as
select substring(flightid from 1 for 2) as airlineid, count(*) as total_ticket_sales
from ticketsales
group by airlineid;
```
This table won’t be kept up-to-date by the database as this is a derived table and not a view. Write a trigger to keep this new table updated when a new ticket (row) is purchased (inserted) into or cancelled (deleted) from the `ticketsales` table. Remember that `airlineid` corresponding to the new `ticketsales` update may not exist in the `airlinesales` table at that time and it should be added to the table with a count of 1, in that case. When a row is deleted from `ticketsales`, we will decrement the count of `total_ticket_sales` corresponding to the deleted `airlineid` by 1. Note that this means that there may be a row in `airlinesales` with a `total_ticket_sales` of 0 if all the records for an airline in `ticketsales` are subsequently deleted. (Note that if we just created a view using the above SQL (instead of creating a seperate table), there would never be records in `airlinesales` with a `total_ticket_sales` of 0.)

In addition to this, for every insertion or deletion of a tuple into/from `ticketsales` (henceforth referred to as a `ticketsales` transaction), we want to check if, as a result of this transaction, a new airline (or set of airlines) is (are) now included in the set of airlines in `airlinesales` with the minimum `total_ticket_sales`. If so, we will report those new airlines with minimum `total_ticket_sales` by inserting each of those airlines into the `reportmin (airlineid, salesdate)` table along with the salesdate of the `ticketsales` transaction (the record that was inserted or deleted) that caused them to become the new minimum. The example below shows how the `reportmin` table is updated:

Consider the transactions in the `ticketsales` table. When the first tuple `(T1, AA101, cust0, 2016-08-09)` was inserted into the `ticketsales` table, we have the state of the `airlinesales` and `reportmin` tables as:

| airlineid | total_ticket_sales |
| :---: | :---: |
| AA | 1 |

`airlinesales`

| airlineid | salesdate |
|:---:|:---:| 
| AA | 2016-08-09 |

`reportmin`

Next, after the insertion of `(T2, AA101, cust0, 2016-08-10)` into `ticketsales`, the corresponding state of the `airlinesales` and `reportmin` tables will be:

| airlineid | total_ticket_sales |
| :---: | :---: |
| AA | 2 |

`airlinesales`

| airlineid | salesdate |
|:---:|:---:| 
| AA | 2016-08-09 |

`reportmin`

Note that `(AA, 2016-08-10)` did not get inserted into `reportmin` because `AA` was already the minimum `airlineid` in `airlinesales`.

Next, after `(T3, UA101, cust2, 2016-08-08)` is inserted into `ticketsales`, we have:

| airlineid | total_ticket_sales |
| :---: | :---: |
| AA | 2 |
| UA | 1 |

`airlinesales`

| airlineid | salesdate |
|:---:|:---:| 
| AA | 2016-08-09 |
| UA | 2016-08-08 |

`reportmin`

Next, after `(T4, SW102, cust1, 2016-08-08)` is inserted into `ticketsales`, we have:

| airlineid | total_ticket_sales |
| :---: | :---: |
| AA | 2 |
| UA | 1 |
| SW | 1 |

`airlinesales`

| airlineid | salesdate |
|:---:|:---:| 
| AA | 2016-08-09 |
| UA | 2016-08-08 |
| SW | 2016-08-08 |

`reportmin`

Note here that although both `UA` and `SW` are the `airlineid`'s with minimal sales in the `airlinesales` table, only the record corresponding to `SW` was inserted into the `reportmin` table, because `UA` was already the minimum `airlineid` prior to this transaction.

Finally, after inserting `(T5, UA101, cust1, 2016-08-09)` into `ticketsales`, we have:

| airlineid | total_ticket_sales |
| :---: | :---: |
| AA | 2 |
| UA | 2 |
| SW | 1 |

`airlinesales`

| airlineid | salesdate |
|:---:|:---:| 
| AA | 2016-08-09 |
| UA | 2016-08-08 |
| SW | 2016-08-08 |

`reportmin`

Here again, `SW` is listed as the `airlineid` with minimal sales in `airlinesales`, but an additional record for `SW` did not get inserted into the `reportmin` table because `SW` was already the minimum `airlineid` prior to this transaction.

Now, if we delete the following tuple from `ticketsales`: `(T2, AA101, cust0, 2016-08-10)` we would have:

| airlineid | total_ticket_sales |
| :---: | :---: |
| AA | 1 |
| UA | 2 |
| SW | 1 |

`airlinesales`

| airlineid | salesdate |
|:---:|:---:| 
| AA | 2016-08-09 |
| UA | 2016-08-08 |
| SW | 2016-08-08 |
| AA | 2016-08-10 |

`reportmin`

Here, both `AA` and `SW` are the airlines with minimum sales after this transaction, but only `AA` gets inserted into `reportmin` since `SW` was already the minimum `airlineid` prior to this transaction. Note that the `salesdate` used for this insert into `reportmin` corresponds to the sales date of the deleted record from `ticketsales`.

Switch to the `flightsales` database, and load the data using `\i trigger-database.sql`. We have already created the `airlinesales` and the `reportmin` tables and initialized them for you. The trigger code should be submitted in `trigger.sql` file. Running `psql -f trigger.sql flightsales` should generate the trigger without errors.

You may also use `trigger-test.py`, in which case you do not need to execute `\i trigger-database.sql` and `psql -f trigger.sql flightsales` (they are included in the script). You can run the test script as `python trigger-test.py trigger.sql`. A few transactions to the `ticketsales` table are also provided. You are free to add more transactions for purposes of testing your trigger code. Remember to create the `flightsales` database before running the test script. If you are going to run it multiple times, you need to `dropdb flightsales` before every run (no easy way to clear all the functions and triggers otherwise).

In the following link, you’ll find some useful trigger examples. You can also use the example from class on Feb 21 to get started:
https://www.postgresql.org/docs/9.2/static/plpgsql-trigger.html

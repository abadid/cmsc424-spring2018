## Project 2: Advanced SQL Assignment, CMSC424, Spring 2018

**1. [Outer Join]** Write a query that uses an outer join to list all the flights that flew empty on August 5, 2016. 

**2. [Outer Join]** We will write a query using outer joins to find all the customers who satisfy all the following conditions <br />
  a. are born in or after 1996, and <br />
  b. have taken a flight at least once, and <br />
  c. have never taken a flight in or out of ‘ORD’.

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

Does the query always produce the correct output? Explain. If not, modify the above query to produce the correct output. 

**3.[SQL Functions]** To begin with this, you must create a new database ```stpc``` and load the data using ```\i table4storedproc.sql```. You are provided with an initial table `inittab` and you are required to generate new table `finaltab`, where the count attribute in ```finaltab``` is transformed according to the following transformation rule:

```
finaltab_count(i) = inittab_count(i) + inittab_count(i-1), where i indicates the row-id
```
The rule above implies that the value of the attribute count of the current row is the sum of the current row and the previous row. For the first row, we just make a copy of it. An example is provided below:

| id | count |  
|:---:|:---:| 
| 12 | 10 | 
| 23 | 20 | 
| 15 | 30 |
| 2  | 10 | 

`inittab`

| id | count |  
|:---:|:---:| 
| 12 | 10 | 
| 23 | 30 | 
| 15 | 50 |
| 2  | 40 | 

`finaltab`

**Part I**: (i) Write a SQL query to generate ```finaltab```, (ii) Write a SQL function using the procedural language in Postgres to generate ```finaltab```. 

As the complexity of the transformation rule increases, writing them out as SQL queries turns out to be less obvious. Here is a more involved transformation rule:

```
finaltab2_amount(i) = inittab_count(i) + F(i), where,
F(i) = sum of the values of count attribute in inittab from row (i-1) to row (i-inittab_id(i)),
if i - inittab_id(i) < 1, then we sum the values upto row 1
```
We provide an example to demonstrate the transformation rule below:

| id | count |  
|:---:|:---:| 
| 12 | 10 | 
| 23 | 30 | 
| 15 | 60 |
| 2  | 60 | 

`finaltab2`

Fortunately, the existence of SQL functions makes it easier to write these transformations.

**Part II**: Write a SQL function to generate ```finaltab2```.

In the following links, you’ll find some useful SQL function examples to get started: <br />
1. https://www.postgresql.org/docs/8.0/static/plpgsql.html <br />
2. https://www.postgresql.org/docs/9.1/static/xfunc-sql.html#XFUNC-SQL-FUNCTIONS-RETURNING-TABLE

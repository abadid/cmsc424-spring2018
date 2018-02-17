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

**3.[PL/pgSQL Functions]** PL/pgSQL is a procedural language for the PostgreSQL database system that can be used to create functions and trigger procedures. In this assignment we will use PL/pgSQL to perform complex computations that are otherwise not straigtforward using SQL queries.

To begin with this, you must create a new database `stpc` and load the data using `\i table4storedproc.sql`. You are provided with an initial table `inittab` and you are required to generate new table `finaltab`, where the count attribute in ```finaltab``` is transformed according to the following transformation rule:

```
finaltab.count(i) = inittab.count(i) + inittab.count(i-1), where i indicates the row-id
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

**Part I**: (i) Write a SQL query to generate `finaltab`, (ii) Write a PL/pgSQL function using the procedural language in Postgres to generate `finaltab`. 

As the complexity of the transformation rule increases, writing them out as SQL queries turns out to be less obvious. Here is a more involved transformation rule:

```
finaltab2.count(i) = inittab.count(i) + F(i), where,
F(i) = sum of the values of count attribute in inittab from row (i-1) to row (i-inittab.id(i)),
if i - inittab.id(i) < 1, then we sum the values upto row 1
```
We provide an example to demonstrate the transformation rule below:

| id | count |  
|:---:|:---:| 
| 12 | 10 | 
| 23 | 30 | 
| 15 | 60 |
| 2  | 60 | 

`finaltab2`

Fortunately, the existence of PL/pgSQL procedural language makes it easier to write these transformations.

**Part II**: Write a PL/pgSQL function to generate `finaltab2`.

In the following links, you’ll find some useful SQL function examples to get started: <br />
1. https://www.postgresql.org/docs/8.0/static/plpgsql.html <br />
2. https://www.postgresql.org/docs/9.1/static/xfunc-sql.html#XFUNC-SQL-FUNCTIONS-RETURNING-TABLE
3. https://stackoverflow.com/questions/30786295/postgres-unassigned-record-is-there-a-way-to-test-for-null


**4.[Trigger]** For this problem, we’ll be using a new hypothetical database `flightsales`, that has all the tables in the `flights` database except that `flewon` table is replaced with `ticketsales` table. The table `ticketsales (ticketid, flightid, customerid, salesdate)` in the `flightsales` database records the ticket sales transaction. To keep things simple, every customer always makes a single ticket purchase in a given flight at a time. We want the ability to keep track of the total number of ticket sales per airline company in the table `airlinesales (airlineid, total_ticket_sales)`.  We use the following command to create this table:

```
create table airlinesales as
select substring(flightid from 1 for 2) as airlineid, count(*) as total_ticket_sales
from ticketsales
group by airlineid;
```
This table won’t be kept up-to-date by the database as this is a derived table and not a view. Write a trigger to keep this new table updated when a new ticket (row) is purchased (inserted) into or cancelled (deleted) from the `ticketsales` table. Remember that `airlineid` corresponding to the new `ticketsales` update may not exist in the `airlinesales` table at that time and it should be added to the table with a count of 1, in that case. Similarly, if a deletion of a row in `ticketsales` results in an airline having `total_ticket_sales` to 0, then the corresponding tuple for that airline in `airlinesales` should be deleted.

In addition to this, we also want to report those airlines that had minimum ticket sales (for every ticket purchased or cancelled) and the `salesdate` of the transaction. We will use the following command to create and populate `reportmin (airlineid, salesdate)` table corresponding to the current state of `airlinesales` table:

```
create table reportmin as
select airlineid, 
(select temp.salesdate 
from (select salesdate, row_number() over() as rid from ticketsales order by rid desc) as temp 
where temp.rid = 1) as salesdate
from airlinesales
where total_ticket_sales = (select min(total_ticket_sales) from airlinesales);
```

Note that we do not report the `airlineid` even if it has the minimum `total_ticket_sales` provided it had minimum `total_ticket_sales` for the previous transaction as well. It is not immediately obvious if this `reportmin` table can be kept updated using a view. Therefore we want you to implement this logic within the trigger function.

You should be able to load the `flightsales` database by `\i trigger-database.sql`. We have already created the `airlinesales` and the `reportmin` tables for you. The trigger code should be submitted in `trigger.sql` file. Running `psql -f trigger.sql flightsales` should generate the trigger without errors.

In the following link, you’ll find some useful trigger examples to get started:
https://www.postgresql.org/docs/9.2/static/plpgsql-trigger.html


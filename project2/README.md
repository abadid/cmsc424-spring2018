## Project 2: Advanced SQL Assignment, CMSC424, Spring 2018

**1. [Outer Join]** Write a query that uses an outer join to list all the flights that flew empty on August 5, 2016. 

**2. [Outer Join]** We will write a query using outer joins to find all the customers who satisfy the following conditions <br />
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

Does the query give the desired output always? Explain. If not, modify the above query to produce the desired output. 

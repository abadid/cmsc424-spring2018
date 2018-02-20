queries = ["" for i in range(0, 11)]

### 0. List all airport codes and their cities. Order by the city name in increasing order. 
### Output column order: airportid, city

queries[0] = """
select airportid, city 
from airports
order by city;
"""

### 1. Write a query to find the names of the customers who were born after 1990-01-01, and the family name starts with 'G'
### Hint: See postgresql date operators and string functions
### Order: by name
### Output columns: name 
queries[1] = """
with temp1 as
(
select distinct flightid as fid
from flewon
where flightdate = '2016-08-05'
),
temp2 as (
select flightid as fid
from flights
),temp as
(
select t1.fid as afid , t2.fid as bfid
from temp1 t1 right outer join temp2 t2
on t1.fid=t2.fid
where t1.fid is NULL
order by t2.fid,t1.fid
)
select bfid
from temp
order by bfid;
"""


### 2. Write a query to find unique customers who flew on the dates within one week before their birthday.
### Hint: See postgresql date functions and distinct operator
### Order: by name 
### Output columns: all columns from customers
queries[2] = """
select 0;
"""

### 3. Write a query to find number of inbound flights by each airline to any airport 
### Output: (airport_city, airline_id, inbound_flights) 
### Order: first by airport_city increasingly, then inbound_flights decreasingly, then airline_id increasingly.
### Note: You must generate the airport city names instead of airport codes.
queries[3] = """
select 0;
"""

### 4. Find the name of the customer who flew the most times with his/her frequent flier airline. For example, if customer X flew Delta (which is listed as X's frequent flier airline in the customers table) 100 times, and no other customer flew their frequent flyer airline more than 99 times, the only thing returned for this query is X's name.
### Hint: use `with clause` and nested queries 
### Output: only the name of the customer. If multiple answers, return them all.
### Order: order by name.
queries[4] = """
select 0;
"""

### 5. Find all 1-stop flights from JFK to LAX having layover duration greater than or equal to 1 hour. 
### Output: (1st flight id, 2nd flight id, connection airport id, layover duration).
### Order: by the duration hours.
queries[5] = """
select 0;
"""

### 6. Assuming each flight has 120 seats, from flewon, find all flights with passenger load factor (PLF) less than or equal to 1% on Aug 1st 2016. Note, PLF is defined as number of customers on-board divided by total number of available seats.  
### Output: (flightid, PLF). 
### Order: first by PLF descreasing order, then flightid 
### Note: a) Each flight flew daily between Aug1 and Aug9, 2016. 
###          There may be empty flights which are not in the flewon table (i.e. PLF=0). 
###          Please include those.
###       b) PLF should be rounded to 2 decimal places, e.g., 10% should be 0.10.
### Hint: SQL set operators union/except/intersect may be useful.
queries[6] = """
select 0;
"""

### 7. Write a query to find the customers who used their frequent flier airline the least when compared to all the airlines that this customer as flown on. For example, if customer X has Delta as X's frequent flyer airline in the customer table, but flew on Delta only 1 time, and every other airline at least 1 time, then X's id and name would be returned as part of this query.
### Output: (customerid, customer_name) 
### Order: by customerid
### Note: a customer may have never flown on their frequent flier airlines.
queries[7] = """
select 0;
"""

### 8. Write a query to find the flights which are empty on three consecutive days, but not empty on the other days. Return the flight, and the start and end dates of those three days.  
### Hint: postgres window functions may be useful
### Output: flightid, start_date, end_date 
### Order: by start_date, then flightid 
queries[8] = """
select 0;
"""

### 9. Write a query to find the city name(s) which have the strongest connection with OAK. We define "strongest connection" as the city with the total number of customers who took a flight that departs from that city to fly to OAK, or arrives at the city from OAK.  
### Output columns: city name
### Order by: city name
### Note: a) You can assume there is only one airport in a city.
###       b) If there are ties, return all tied cities 
queries[9] = """
with from_oak as (
    select dest as airportid, count(*) as strength, 0 as direction 
    from flights natural join flewon 
    where source = 'OAK' 
    group by dest
), to_oak as (
    select source as airportid, count(*) as strength, 1 as direction 
    from flights natural join flewon 
    where dest = 'OAK' 
    group by source
), oak_connections as (
    select airportid, sum(strength) as strength 
    from (select * from from_oak union select * from to_oak) oak_edges 
    group by airportid
) 
select city from oak_connections natural join airports
where strength = (select max(strength) from oak_connections)
order by city;
"""

### 10. Write a query that outputs the ranking of the top 20 busiest flights. We rank the flights by their average number of on-board customers, so the flight with the highest average number of customers gets rank 1, and so on. 
### Output: (flightid, flight_rank)
### Order: by the rank, then by flightid 
### Note: a) If two flights tie, then they should both get the same rank, and the next rank should be skipped. For example, if the top two flights have the same average number of customers, then there should be no rank 2, e.g., 1, 1, 3 ...   
###       b) There may be empty flights.
###       c) There may be tied flights at rank 20, if so, all flights ranked 20 need to be returned
queries[10] = """
select 0;"""

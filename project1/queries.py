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
<<<<<<< HEAD
select name from customers where birthdate > '19900101' and name like '% G%' order by name;
=======
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
>>>>>>> 6dfd2e3cd50f3eaf08b38a838c6a63e26df42a6c
"""


### 2. Write a query to find unique customers who flew on the dates within one week before their birthday.
### Hint: See postgresql date functions and distinct operator
### Order: by name 
### Output columns: all columns from customers
queries[2] = """
with adjusted as (select customers.name, customers.birthdate + interval '1 year' * (2016 - date_part('year', customers.birthdate)) as birthday, flewon.flightdate from customers join flewon on customers.customerid = flewon.customerid) select distinct customers.customerid, customers.name,  customers.birthdate, customers.frequentflieron from adjusted join customers on adjusted.name = customers.name where (date_part('day', adjusted.birthday - adjusted.flightdate) <= 7 and adjusted.birthday > adjusted.flightdate);
"""

### 3. Write a query to find number of inbound flights by each airline to any airport 
### Output: (airport_city, airline_id, inbound_flights) 
### Order: first by airport_city increasingly, then inbound_flights decreasingly, then airline_id increasingly.
### Note: You must generate the airport city names instead of airport codes.
queries[3] = """
select airports.city, flights.airlineid, COUNT(*) as inbound_flights from flights join airports on airports.airportid = flights.dest group by flights.airlineid, airports.city order by airports.city, inbound_flights desc, flights.airlineid;
"""

### 4. Find the name of the customer who flew the most times with his/her frequent flier airline. For example, if customer X flew Delta (which is listed as X's frequent flier airline in the customers table) 100 times, and no other customer flew their frequent flyer airline more than 99 times, the only thing returned for this query is X's name.
### Hint: use `with clause` and nested queries 
### Output: only the name of the customer. If multiple answers, return them all.
### Order: order by name.
queries[4] = """
with counts as (with tmp as (select customers.name, customers.frequentflieron, flewon.flightid, flewon.flightdate from customers join flewon on customers.customerid = flewon.customerid where customers.frequentflieron = substring(flewon.flightid, 1, 2) order by name) select name, COUNT(*) from tmp group by name order by count desc) select name from counts where count = (select max(count) from counts) order by name;
"""

### 5. Find all 1-stop flights from JFK to LAX having layover duration greater than or equal to 1 hour. 
### Output: (1st flight id, 2nd flight id, connection airport id, layover duration).
### Order: by the duration hours.
queries[5] = """
with jfk as (select source, dest, flightid, local_arrival_time from flights where source = 'JFK'), final as (select jfk.flightid, flights.flightid, jfk.dest, flights.local_departing_time -jfk.local_arrival_time as layover from jfk join flights on jfk.dest = flights.source where flights.dest = 'LAX') select * from final where layover >= '1:00:00';
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
with tmp as (select flightid, flightdate, round(cast(COUNT(*)/cast(120 as float) as numeric) ,2) as PLF from flewon where flightdate = '20160801' group by flightid, flightdate), extras as (select flightid from flights except select flightid from tmp), final as (select flightid, 0.00 as plf from extras union select flightid, plf from tmp where plf <= .01) select * from final order by plf desc, flightid;
"""

### 7. Write a query to find the customers who used their frequent flier airline the least when compared to all the airlines that this customer as flown on. For example, if customer X has Delta as X's frequent flyer airline in the customer table, but flew on Delta only 1 time, and every other airline at least 1 time, then X's id and name would be returned as part of this query.
### Output: (customerid, customer_name) 
### Order: by customerid
### Note: a customer may have never flown on their frequent flier airlines.
queries[7] = """
with extras as (select customerid, customers.name, frequentflieron, airlineid, 0 as count from airlines cross join customers), counts as (select customers.customerid, name, frequentflieron, substring(flightid, 1, 2) as airlineid, count(*) from customers join flewon on customers.customerid = flewon.customerid group by name, airlineid, frequentflieron, customers.customerid), combined as (select * from counts union select * from extras where not exists (select * from counts where counts.customerid = extras.customerid and counts.airlineid = extras.airlineid)), mins as (select customerid, name, airlineid, frequentflieron, count, min(count) over (partition by name) as min_count from combined) select customerid, name from mins where count = min_count and airlineid = frequentflieron order by customerid;
"""

### 8. Write a query to find the flights which are empty on three consecutive days, but not empty on the other days. Return the flight, and the start and end dates of those three days.  
### Hint: postgres window functions may be useful
### Output: flightid, start_date, end_date 
### Order: by start_date, then flightid 
queries[8] = """
with flight_dates as (select distinct flights.flightid, flightdate from flights join flewon on flewon.flightid = flights.flightid),
three_gaps as (select a.flightid, a.flightdate + 1 as start_date from flight_dates a where not exists (select * from flight_dates b where b.flightdate = a.flightdate + interval '1 day' and b.flightid = a.flightid) and
not exists (select * from flight_dates b where b.flightdate = a.flightdate + interval '1 day' * 2 and b.flightid = a.flightid) and
not exists (select * from flight_dates b where b.flightdate = a.flightdate + interval '1 day' * 3 and b.flightid = a.flightid)), gaps as (select a.flightid, a.flightdate + interval '1 day' as gap from flight_dates a where not exists (select * from flight_dates b where b.flightdate = a.flightdate + interval '1 day' and b.flightid = a.flightid)), counts as (select flightid, count(*) as c from flight_dates group by flightid order by flightid) select *, start_date + 2 as end_date from three_gaps where exists (select * from counts where counts.flightid = three_gaps.flightid and c = 6) and start_date <= '20160806' order by start_date, flightid;
"""

### 9. Write a query to find the city name(s) which have the strongest connection with OAK. We define "strongest connection" as the city with the total number of customers who took a flight that departs from that city to fly to OAK, or arrives at the city from OAK.  
### Output columns: city name
### Order by: city name
### Note: a) You can assume there is only one airport in a city.
###       b) If there are ties, return all tied cities 
queries[9] = """
<<<<<<< HEAD
 with sources as (select source as airport from flights join flewon on flights.flightid = flewon.flightid where dest = 'OAK'), dests as (select dest as airport from flights join flewon on flights.flightid = flewon.flightid where source = 'OAK'), counts as (select airport, count(*) from (select * from dests union all select * from sources) t group by airport) select city from counts join airports on counts.airport = airports.airportid where counts.count = (select max(count) from counts);
=======
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
>>>>>>> 6dfd2e3cd50f3eaf08b38a838c6a63e26df42a6c
"""

### 10. Write a query that outputs the ranking of the top 20 busiest flights. We rank the flights by their average number of on-board customers, so the flight with the highest average number of customers gets rank 1, and so on. 
### Output: (flightid, flight_rank)
### Order: by the rank, then by flightid 
### Note: a) If two flights tie, then they should both get the same rank, and the next rank should be skipped. For example, if the top two flights have the same average number of customers, then there should be no rank 2, e.g., 1, 1, 3 ...   
###       b) There may be empty flights.
###       c) There may be tied flights at rank 20, if so, all flights ranked 20 need to be returned
queries[10] = """
<<<<<<< HEAD
with tmp as (select flightid, flightdate, count(*) from flewon group by flightid, flightdate) , tmp2 as (select SUM(count) as passengers, flightid from tmp group by flightid) select flightid, rank from (select flightid, rank() over (order by passengers desc) as rank from tmp2) t where rank <= 20 order by rank, flightid;
"""
=======
select 0;"""
>>>>>>> 6dfd2e3cd50f3eaf08b38a838c6a63e26df42a6c

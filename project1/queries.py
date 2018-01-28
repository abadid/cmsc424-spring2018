queries = ["" for i in range(0, 11)]

### 0. List all airport codes and their cities. Order by the city name in the increasing order. 
### Output column order: airportid, city

queries[0] = """
select airportid, city 
from airports
order by city;
"""

### 1. Write a query to find the names of the customers who were born after 1990-01-01, and the the family name starts with 'G'
### Hint: See postgresql date operators and string functions
### Order: by name
### Output columns: name 
queries[1] = """
select name from customers where birthdate > '19900101' and name like '% G%' order by name;
"""


### 2. Write a query to find any customers who flew on the dates within one week before their birthday.
### Hint: See postgresql date functions
### Order: by name 
### Output columns: all columns from customers
queries[2] = """
NOT DONE
select customers.name, customers.birthdate, flewon.flightdate from customers join flewon on customers.customerid = flewon.customerid;
"""

### 3. Write a query to find number of inbound flights by each airlines to any airport 
### Output: (airport_city, airline_id, inbound_flights) 
### Order: first by airport_city increasingly, then inbound_flights decreasingly, then airline_id increasingly.
### Note: You must generate the airport city names instead of airport codes.
queries[3] = """
select airports.city, flights.airlineid, COUNT(*) as inbound_flights from flights join airports on airports.airportid = flights.dest group by flights.airlineid, airports.city order by airports.city, inbound_flights desc, flights.airlineid;
"""

### 4. Find the name of the customer who flew the most with his/her frequent flier airlines
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

### 6. Assuming each flight have 120 seats, from flewon, find all flights with passenger load factor (PLF) less than or equal to 1% on Aug 1st 2016. Note, PLF is defined as number of customers on-board divided by total number of available seats.  
### Output: (flightid, PLF). 
### Order: first by PLF descreasing order, then flightid 
### Note: a) Each flight flew daily during Aug1 and Aug9, 2016. 
###          There may be empty flights which are not in the flewon table (i.e. PLF=0). 
###          Please include those.
###       b) PLF should be rounded to 2 decimal places, e.g., 10% should be 0.10.
### Hint: SQL set operators union/except/intersect may be useful.
queries[6] = """
with tmp as (select flightid, flightdate, round(cast(COUNT(*)/cast(120 as float) as numeric) ,2) as PLF from flewon where flightdate = '20160801' group by flightid, flightdate), extras as (select flightid from flights except select flightid from tmp), final as (select flightid, 0.00 as plf from extras union select flightid, plf from tmp where plf <= .01) select * from final order by plf desc, flightid;
"""

### 7. Write a query to find the customer who flew the least on their frequent flier airline.
### Output: (customerid, customer_name) 
### Order: by customerid
### Note: a customer may have never flown on their frequent flier airlines.
queries[7] = """
with counts as (with tmp as (select customers.customerid, customers.name, customers.frequentflieron, flewon.flightid, flewon.flightdate from customers join flewon on customers.customerid = flewon.customerid where customers.frequentflieron = substring(flewon.flightid, 1, 2) order by name) select customerid, name, COUNT(*) from tmp group by customerid,name order by count desc), extras as (select customerid, name from customers except select customerid, name from counts), final as (select * from counts UNION select customerid, name, 0 as count from extras) select customerid, name from final where count = (select min(count) from final) order by customerid;
"""

### 8. Write a query to find the flights which are empty on three consecutive days, but not empty on the other days, return the flight, and the start and end dates of those three days.  
### Hint: postgres window functions may be useful
### Output: flightid, start_date, end_date 
### Order: by start_date, then flightid 
queries[8] = """
select 0;
"""

### 9. Write a query to find the city name(s) which have the strongest connection with OAK. We define it as the total number of customers who took a flight that departures the city to OAK, or arrives the city from OAK.  
### Output columns: city name
### Order by: city name
### Note: a) You can assume there is only one airport in a city.
###       b) If there are ties, return all tied cities 
queries[9] = """
with customer_flights as (select flewon.customerid, flights.dest, flights.source, flewon.flightdate from flights join flewon on flewon.flightid = flights.flightid), dests as (select dest, COUNT(*) from customer_flights where source = 'OAK' group by dest), sources as (select source, COUNT(*) as c2 from customer_flights where dest = 'OAK' group by source), combined as (select * from dests join sources on sources.source = dests.dest), final as (select dest, count + c2 as count from combined) select airports.city from final join airports on airports.airportid = final.dest where count = (select max(count) from final) order by airports.city;
"""

### 10. Write a query that outputs the top 20 ranking of the most busy flights. We rank the flights by their average on-board customers, so the flight with the most average number of customers gets rank 1, and so on. 
### Output: (flightid, flight_rank)
### Order: by the rank 
### Note: If two flights tie, then they should both get the same rank, and the next rank should be skipped. For example, if the top two flights have the same average number of customers, then there should be no rank 2, e.g., 1, 1, 3 ...   
queries[10] = """
with tmp as (select flightid, flightdate, count(*) from flewon group by flightid, flightdate) , tmp2 as (select SUM(count) as passengers, flightid from tmp group by flightid) select flightid, rank() over (order by passengers desc) as rank from tmp2 limit 20;
"""

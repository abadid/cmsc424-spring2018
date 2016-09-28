queries = ["" for i in range(0, 11)]

### 0. List all airport codes and their cities. Order by the city name in the increasing order. 
### Output column order: airportid, city

queries[0] = """
select airportid, city 
from airports
order by city;
"""

### 1. Write a query to find the names of the customers whose names are at least 15 characters long, and the second letter in the  name is "l".
### Order by name.
queries[1] = """
select name
from customers
where length(name) >= 15 and name like '_l%'
order by name;
"""


### 2. Write a query to find any customers who flew on their birthday.  Hint: Use "extract" function that operates on the dates. 
### Order output by Customer Name.
### Output columns: all columns from customers
queries[2] = """
select c.*
from customers c natural join flewon f
where extract(day from c.birthdate) = extract(day from f.flightdate) and
    extract(month from c.birthdate) = extract(month from f.flightdate)
order by name;
"""

### 3. Write a query to generate a list: (source_city, source_airport_code, dest_city, dest_airport_code, number_of_flights) for all source-dest pairs with at least 2 flights. 
### Order first by number_of_flights in decreasing order, then source_city in the increasing order, and then dest_city in the increasing order.
### Note: You must generate the source and destination cities along with the airport codes.
queries[3] = """
select a.city, source, b.city, dest, count(*) number_of_flights
from flights, airports a, airports b
where flights.source = a.airportid and flights.dest = b.airportid
group by a.city, source, b.city, dest
having count(*) > 1
order by number_of_flights desc, a.city asc, b.city asc;
"""

### 4. Find the name of the airline with the maximum number of customers registered as frequent fliers.
### Output only the name of the airline. If multiple answers, order by name.
queries[4] = """
with temp as (
    select frequentflieron as airlineid, count(*) as numcustomers
    from customers
    group by frequentflieron
)
select name
from temp natural join airlines
where numcustomers = (select max(numcustomers) from temp)
order by name;
"""

### 5. For all flights from OAK to ATL, list the flight id, airline name, and the 
### duration in hours and minutes. So the output will have 4 fields: flightid, airline name,
### hours, minutes. Order by flightid.
queries[5] = """
with temp as (
        select flightid, name, (local_arrival_time - local_departing_time) as duration
        from flights natural join airlines
        where source = 'OAK' and dest = 'ATL'
) 
select flightid, name, extract(hours from duration) hours, extract(minutes from duration) minutes
from temp
order by flightid;
"""

### 6. Write a query to find all the empty flights (if any); recall that all the flights listed
### in the flights table are daily, and that flewon contains information for a period of 10
### days from Jan 1 to Jan 10, 2010. For each such flight, list the flightid and the date.
### Order by flight id in the increasing order, and then by date in the increasing order.
queries[6] = """
with temp as (
        select distinct flightdate
        from flewon
) 
select flightid, flightdate
from flights, temp
except
select flightid, flightdate
from flewon
order by flightid, flightdate;
"""

### 7. Write a query to generate a list of customers who don't list Southwest as their frequent flier airline, but
### actually flew the most (by number of flights) on that airline.
### Output columns: customerid, customer_name
### Order by: customerid
queries[7] = """
with temp1 as (
        select customerid, airlineid, count(*) as num_flights
        from flewon natural join flights
        group by customerid, airlineid
),
temp2 as (
        select customerid
        from temp1 t1
        where num_flights = (select max(num_flights) from temp1 t2 where t1.customerid = t2.customerid)
            and airlineid = 'SW'
)
select customers.customerid, name
from customers, temp2
where customers.customerid = temp2.customerid and customers.frequentflieron != 'SW'
order by customerid;
"""

### 8. Write a query to generate a list of customers who flew twice on two consecutive days, but did
### not fly otherwise in the 10 day period. The output should be simply a list of customer ids and
### names. Make sure the same customer does not appear multiple times in the answer. 
### Order by the customer name. 
queries[8] = """
(select distinct c.customerid, c.name
from customers c, flewon f1, flewon f2
where c.customerid = f1.customerid and f1.customerid = f2.customerid and f1.flightdate != f2.flightdate and f1.flightid != f2.flightid
and abs(extract(day from f1.flightdate) - extract(day from f2.flightdate)) < 2
)
intersect
(select distinct customerid, name
from customers natural join flewon
group by customerid, name
having count(*) = 2
)
order by name;
"""

### 9. Write a query to find the names of the customer(s) who visited the most cities in the 10 day
### duration. A customer is considered to have visited a city if he/she took a flight that either
### departed from the city or landed in the city. 
### Output columns: name
### Order by: name
queries[9] = """
with temp as (
        select distinct customerid, airports.city
        from flewon, flights, airports
        where flewon.flightid = flights.flightid and 
            (flights.source = airports.airportid or flights.dest = airports.airportid)
),
temp2 as (
        select customerid, count(*) as num_cities_visited
        from temp
        group by customerid
)
select name
from temp2 natural join customers
where num_cities_visited = (select max(num_cities_visited) from temp2)
order by name;
"""


### 10. Write a query that outputs a list: (AirportID, Airport-rank), where we rank the airports 
### by the total number of flights that depart that airport. So the airport with the maximum number
### of flights departing gets rank 1, and so on. If two airports tie, then they should 
### both get the same rank, and the next rank should be skipped.
### Order the output in the increasing order by rank.

queries[10] = """
with temp as (
        select source as airportid, count(*) as num_flights
        from flights
        group by source
)
select airportid, num_flights, (select count(*) 
                   from temp t2 
                   where t2.num_flights > t1.num_flights) + 1 as airport_rank
from temp t1
order by airport_rank;
"""

queries = ["" for i in range(0, 11)]

### 0. List all airport codes and their cities. Order by the city name in the increasing order. 
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
select name   
from customers
where birthdate >= DATE '1990-01-01' and split_part(name, ' ', 2) like 'G%'
order by name;
"""


### 2. Write a query to find unqiue customers who flew on the dates within one week before their birthday.
### Hint: See postgresql date functions and distinct operator
### Order: by name 
### Output columns: all columns from customers
queries[2] = """
select distinct(customerid), name, birthdate, frequentflieron
from 
  flewon f natural join 
  (select *, to_date(concat(2016, ' ', extract(month from birthdate), ' ', 
                     extract(day from birthdate)), 'YYYY MM DD') as birthday_2016 
   from customers) customers_with_2016birthday
where birthday_2016 <= f.flightdate + interval '1 week' and
      birthday_2016 > f.flightdate
order by name;
"""

### 3. Write a query to find number of inbound flights by each airlines to any airport 
### Output: (airport_city, airline_id, inbound_flights) 
### Order: first by airport_city in the increasing order, then inbound_flights in decreasing order, and then airline_id in the increasing order.
### Note: You must generate the airport city names instead of airport codes.
queries[3] = """
select city as airport_city, airlineid, count(*) as inbound_flights 
from flights, airports 
where flights.dest = airports.airportid
group by city, airlineid 
order by city asc, inbound_flights desc, airlineid asc;
"""

### 4. Find the name of the customer who flew the most times with his/her frequent flier airline. For example, if customer X flew Delta (which is listed as X's frequent flier airline in the customers table) 100 times, and no other customer flew their frequent flyer airline more than 99 times, the only thing returned for this query is X's name.
### Hint: use `with clause` and nested queries 
### Output: only the name of the customer. If multiple answers, return them all.
### Order: order by name.
queries[4] = """
with customer_flewontimes_by_airline as (
    select customerid, 
           substring(flightid from 1 for 2) as airline_id, 
           count(*) as flewon_times
    from flewon 
    group by customerid, airline_id
),
customer_flewontimes_ffairlines as (
    select b.name, a.flewon_times
    from customer_flewontimes_by_airline a, customers b 
    where a.customerid = b.customerid and a.airline_id = b.frequentflieron
)
select name from customer_flewontimes_ffairlines
where flewon_times = (select max(flewon_times) from customer_flewontimes_ffairlines)
order by name;
"""


### 5. Find all 1-stop flights from JFK to LAX having layover duration greater than or equal to 1 hour. 
### Output: (1st flight id, 2nd flight id, connection airport id, layover duration).
### Order: by the duration hours.
queries[5] = """
select a.flightid as flight1, 
       b.flightid as flight2, 
       b.source as connection_airport, 
       (b.local_departing_time - a.local_arrival_time) as duration 
from flights a, flights b 
where a.dest = b.source and 
      extract(hour from b.local_departing_time - a.local_arrival_time) >= 1 and 
      a.source='JFK' and b.dest='LAX'
order by duration;
"""

### 6. Assuming each flight have 120 seats, from flewon, find all flights with passenger load factor (PLF) less than or equal to 1% on Aug 1st 2016. Note, PLF is defined as number of customers on board divided by total number of available seats.  
### Output: (flightid, PLF). 
### Order: first by PLF descreasing order, then flightid 
### Note: a) Each flight flew daily during Aug1 and Aug9, 2016. There may be empty flights which are not in the flewon table (i.e. PLF=0). Please include those.
###       b) PLF should be rounded to 2 decimal places, e.g., 10% should be 0.10.
### Hint: SQL set operators union/except/intersect may be useful.
queries[6] = """
with flewon_plf_0801 as (
    select flightid, flightdate, round(count(*)/120.0, 2) as plf 
    from flewon 
    where flightdate = DATE '2016-08-01'
    group by flightid, flightdate
), 
empty_flights0801 as (
    select flightid, DATE '2016-08-01' as flightdate, round(0.0, 2) as plf
    from flights 
    where flightid not in 
        (select distinct(flightid) from flewon where flightdate = DATE '2016-08-01')
)
select flightid, plf from (
    select * from empty_flights0801
    union 
    select * from flewon_plf_0801 where plf <= 0.01
) combined_plf_0801 
order by plf desc, flightid;
"""

### 7. Write a query to find the customers who used their frequent flier airline the least when compared to all the airlines that this customer as flown on. For example, if customer X has Delta as X's frequent flyer airline in the customer table, but flew on Delta only 1 time, but every other airline at least 1 time, then X's id and name would be returned as part of this query.
### Output: (customerid, customer_name) 
### Order: by customerid
### Note: a customer may have never flown on their frequent flier airlines.
queries[7] = """
with customer_onboard_times_init as (
   select customerid, airlineid, 0 as num_flights 
   from customers, airlines
), customer_actual_onboard_times_by_airline as (
    select customerid, airlineid, count(*) as num_flights
    from flewon natural join flights
    group by customerid, airlineid
), customer_onboard_times_combined as (
    select customerid, airlineid, sum(num_flights) as total_flights 
    from (select * from customer_onboard_times_init 
          union select * from  customer_actual_onboard_times_by_airline
    ) onboard_combined
    group by customerid, airlineid
) 
select customerid, name  
from customer_onboard_times_combined t1 natural join customers 
where airlineid = frequentflieron and 
      total_flights = (select min(total_flights) 
                       from customer_onboard_times_combined t2 
                       where t1.customerid = t2.customerid) 
order by customerid;
"""

### 8. Write a query to find the flights which are empty on three consecutive days, but not empty on the other days, return the flight, and the start and end dates of those three days.  
### Hint: postgres window functions may be useful
### Output: flightid, start_date, end_date 
### Order: by start_date, then flightid 
queries[8] = """
with empty_flights as (
    select flightid, flightdate
    from flights, 
         (select distinct flightdate from flewon) all_dates
    except
    select flightid, flightdate
    from flewon
    order by flightid, flightdate
), flights_three_times_empty as (
    select * from empty_flights 
    where flightid in (
        select flightid 
        from empty_flights 
        group by flightid 
        having count(*) = 3
    ) 
) 
select flightid, min(flightdate) as start_date, max(flightdate) as end_date 
from flights_three_times_empty 
group by flightid 
having max(flightdate) - min(flightdate) = 2 
order by flightid; 
"""

### 9. Write a query to find the city name(s) which have the strongest connection with OAK. We define it as the total number of customers who took a flight that departures the city to OAK, or arrives the city from OAK.  
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

### 10. Write a query that outputs the top 20 ranking of the most busy flights. We rank the flights by their average onboard customers, so the flight with the most average number of customers gets rank 1, and so on. 
### Output: (flightid, flight_rank)
### Order: by the rank, then flightid 
### Note: a) If two flights tie, then they should both get the same rank, and the next rank should be skipped. For example, if the top two flights have the same average number of customers, then there should be no rank 2, e.g., 1, 1, 3 ...   
###       b) There may be empty flights. 
queries[10] = """
with flight_customers_per_day as (
    select flightid, flightdate, count(customerid) as onboard_cnt
    from flewon
    group by flightid, flightdate
), flight_avg_customers as (
    select flightid, 
           sum(onboard_cnt)/(select max(flightdate) - min(flightdate) + 1 
                             from flewon)*1.0 
             as avg_customer_cnt
    from flight_customers_per_day
    group by flightid
), ranked_flights as (
    select
       flightid,
       avg_customer_cnt,
       (select count(*) from flight_avg_customers t2
        where t2.avg_customer_cnt > t1.avg_customer_cnt) + 1
        as flight_rank
    from flight_avg_customers t1
)
select flightid, flight_rank from ranked_flights
where flight_rank <= 20
order by flight_rank, flightid;
"""

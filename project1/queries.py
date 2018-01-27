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
select 0;
"""


### 2. Write a query to find unique customers who flew on the dates within one week before their birthday.
### Hint: See postgresql date functions and distinct operator
### Order: by name 
### Output columns: all columns from customers
queries[2] = """
select 0;
"""

### 3. Write a query to find number of inbound flights by each airlines to any airport 
### Output: (airport_city, airline_id, inbound_flights) 
### Order: first by airport_city increasingly, then inbound_flights decreasingly, then airline_id increasingly.
### Note: You must generate the airport city names instead of airport codes.
queries[3] = """
select 0;
"""

### 4. Find the name of the customer who flew the most with his/her frequent flier airlines
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

### 6. Assuming each flight have 120 seats, from flewon, find all flights with passenger load factor (PLF) less than or equal to 1% on Aug 1st 2016. Note, PLF is defined as number of customers on-board divided by total number of available seats.  
### Output: (flightid, PLF). 
### Order: first by PLF descreasing order, then flightid 
### Note: a) Each flight flew daily during Aug1 and Aug9, 2016. 
###          There may be empty flights which are not in the flewon table (i.e. PLF=0). 
###          Please include those.
###       b) PLF should be rounded to 2 decimal places, e.g., 10% should be 0.10.
### Hint: SQL set operators union/except/intersect may be useful.
queries[6] = """
select 0;
"""

### 7. Write a query to find the customer who flew the least on their frequent flier airline.
### Output: (customerid, customer_name) 
### Order: by customerid
### Note: a customer may have never flown on their frequent flier airlines.
queries[7] = """
select 0;
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
select 0;
"""

### 10. Write a query that outputs the top 20 ranking of the most busy flights. We rank the flights by their average on-board customers, so the flight with the most average number of customers gets rank 1, and so on. 
### Output: (flightid, flight_rank)
### Order: by the rank 
### Note: If two flights tie, then they should both get the same rank, and the next rank should be skipped. For example, if the top two flights have the same average number of customers, then there should be no rank 2, e.g., 1, 1, 3 ...   
queries[10] = """
select 0;
"""

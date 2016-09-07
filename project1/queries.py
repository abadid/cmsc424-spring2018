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
select 0;
"""


### 2. Write a query to find any customers who flew on their birthday.  Hint: Use "extract" function that operates on the dates. 
### Order output by Customer Name.
### Output columns: all columns from customers
queries[2] = """
select 0;
"""

### 3. Write a query to generate a list: (source_city, source_airport_code, dest_city, dest_airport_code, number_of_flights) for all source-dest pairs with at least 2 flights. 
### Order first by number_of_flights in decreasing order, then source_city in the increasing order, and then dest_city in the increasing order.
### Note: You must generate the source and destination cities along with the airport codes.
queries[3] = """
select 0;
"""

### 4. Find the name of the airline with the maximum number of customers registered as frequent fliers.
### Output only the name of the airline. If multiple answers, order by name.
queries[4] = """
select 0;
"""

### 5. For all flights from OAK to ATL, list the flight id, airline name, and the 
### duration in hours and minutes. So the output will have 4 fields: flightid, airline name,
### hours, minutes. Order by flightid.
### Don't worry about timezones -- assume all times are reported using the same timezone.
queries[5] = """
select 0;
"""

### 6. Write a query to find all the empty flights (if any); recall that all the flights listed
### in the flights table are daily, and that flewon contains information for a period of 9
### days from August 1 to August 9, 2016. For each such flight, list the flightid and the date.
### Order by flight id in the increasing order, and then by date in the increasing order.
queries[6] = """
select 0;
"""

### 7. Write a query to generate a list of customers who don't list Southwest as their frequent flier airline, but
### actually flew the most (by number of flights) on that airline.
### Output columns: customerid, customer_name
### Order by: customerid
queries[7] = """
select 0;
"""

### 8. Write a query to generate a list of customers who flew twice on two consecutive days, but did
### not fly otherwise in the 10 day period. The output should be simply a list of customer ids and
### names. Make sure the same customer does not appear multiple times in the answer. 
### Order by the customer name. 
queries[8] = """
select 0;
"""

### 9. Write a query to find the names of the customer(s) who visited the most cities in the 10 day
### duration. A customer is considered to have visited a city if he/she took a flight that either
### departed from the city or landed in the city. 
### Output columns: name
### Order by: name
queries[9] = """
select 0;
"""


### 10. Write a query that outputs a list: (AirportID, Airport-rank), where we rank the airports 
### by the total number of flights that depart that airport. So the airport with the maximum number
### of flights departing gets rank 1, and so on. If two airports tie, then they should 
### both get the same rank, and the next rank should be skipped.
### Order the output in the increasing order by rank.
queries[10] = """
select 0;
"""

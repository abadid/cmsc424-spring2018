import psycopg2
import os
import sys
import subprocess

def executePrint(s):
	cur.execute(s)
	print cur.fetchall()

if len(sys.argv) != 2:
	print "Usage: testing-trigger-grading.py <your trigger SQL file>"
	sys.exit(1)

subprocess.call(["psql", "-f", "trigger-database.sql", "flightstrigger"])
subprocess.call(["psql", "-f", sys.argv[1], "flightstrigger"])

conn = psycopg2.connect("dbname=flightstrigger user=vagrant")
cur = conn.cursor()

## Add a customer who doesn't exist
print "==== Testing: adding a customer without a flewon entry"
executePrint("select * from NumberOfFlightsTaken where customerid = 'cust2'")

print "Inserting a flewon entry for cust731"
cur.execute("insert into flewon values ('AA101', 'cust2', to_date('2016-08-09', 'YYYY-MM-DD'))");
conn.commit()

print "Rerunning the query"
executePrint("select * from NumberOfFlightsTaken where customerid = 'cust2'")

## Remove a customer with a few entries 
print "==== Testing: removing a customer's all flewon entries"
executePrint("select * from NumberOfFlightsTaken where customerid = 'cust1'")

cur.execute("delete from flewon where customerid = 'cust1' and flightid = 'SW102'")
conn.commit()

print "Rerunning the query after deleting one entry"
executePrint("select * from NumberOfFlightsTaken where customerid = 'cust1'")

cur.execute("delete from flewon where customerid = 'cust1' and flightid = 'AA101'")
conn.commit()

print "Rerunning the query after deleting both entries"
executePrint("select * from NumberOfFlightsTaken where customerid = 'cust1'")

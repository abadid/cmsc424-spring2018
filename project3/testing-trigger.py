import psycopg2
import os
import sys
import subprocess

def executePrint(s):
	cur.execute(s)
	print cur.fetchall()

subprocess.call(["psql", "-f", "/vagrant/trigger.sql", "flightsskewed"])

conn = psycopg2.connect("dbname=flightsskewed user=vagrant")
cur = conn.cursor()

## Add a customer who doesn't exist
print "==== Testing: adding a customer without a flewon entry"
executePrint("select * from NumberOfFlightsTaken where customerid = 'cust731'")

print "Inserting a flewon entry for cust731"
cur.execute("insert into flewon values ('AA101', 'cust731', to_date('2016-08-09', 'YYYY-MM-DD'))");
conn.commit()

print "Rerunning the query"
executePrint("select * from NumberOfFlightsTaken where customerid = 'cust731'")

## Remove a customer with a few entries 
print "==== Testing: removing a customer's all flewon entries"
executePrint("select * from NumberOfFlightsTaken where customerid = 'cust597'")

cur.execute("delete from flewon where customerid = 'cust597' and flightid = 'F9103'")
conn.commit()

print "Rerunning the query after deleting one entry"
executePrint("select * from NumberOfFlightsTaken where customerid = 'cust597'")

cur.execute("delete from flewon where customerid = 'cust597' and flightid = 'AA134'")
conn.commit()

print "Rerunning the query after deleting both entries"
executePrint("select * from NumberOfFlightsTaken where customerid = 'cust597'")

## Cleanup
cur.execute("insert into flewon values ('F9103', 'cust597', to_date('2016-08-04', 'YYYY-MM-DD'))")
cur.execute("insert into flewon values ('AA134', 'cust597', to_date('2016-08-05', 'YYYY-MM-DD'))")
cur.execute("delete from flewon where customerid = 'cust731'")
conn.commit()

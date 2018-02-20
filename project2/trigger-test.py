import psycopg2
import os
import sys
import subprocess

def executePrint(s):
	cur.execute(s)
	print cur.fetchall()

if len(sys.argv) != 2:
	print "Usage: trigger-test.py <your trigger SQL file>"
	sys.exit(1)

subprocess.call(["psql", "-f", "trigger-database.sql", "flightsales"])
subprocess.call(["psql", "-f", sys.argv[1], "flightsales"])

conn = psycopg2.connect("dbname=flightsales user=vagrant")
cur = conn.cursor()

print "Initial State"
executePrint("select * from airlinesales")
executePrint("select * from reportmin")

print "Deleting a ticketsales entry for UA"
cur.execute("delete from ticketsales where customerid = 'cust2' and flightid = 'UA101'")
conn.commit()

print "After deletion"
executePrint("select * from airlinesales")
executePrint("select * from reportmin")

print "Inserting a ticketsales entry for SW"
cur.execute("insert into ticketsales values ('T6', 'SW102', 'cust2', to_date('2016-08-09', 'YYYY-MM-DD'))");
conn.commit()

print "After insertion"
executePrint("select * from airlinesales")
executePrint("select * from reportmin")


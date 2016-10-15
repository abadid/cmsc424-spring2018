import psycopg2
import os
import sys
import subprocess

def executePrint(s):
	cur.execute(s)
	print cur.fetchall()

print "Compiling..."
subprocess.call(["javac", "-classpath", ".:./json-simple-1.1.1.jar:./postgresql-9.0-801.jdbc3.jar", "JSONProcessing.java"])
print "Executing against example.json..."
subprocess.call(["java", "-classpath", ".:./json-simple-1.1.1.jar:./postgresql-9.0-801.jdbc3.jar", "JSONProcessing"], stdin=open("example.json"))

conn = psycopg2.connect("dbname=flightsskewed user=vagrant")
cur = conn.cursor()

## Add a customer who doesn't exist
print "==== Testing first json update"
executePrint("select * from customers where customerid = 'cust1000'")

print "==== Testing second json update"
executePrint("select * from flewon where flightid = 'DL108'")
executePrint("select * from customers where customerid = 'cust1001'")

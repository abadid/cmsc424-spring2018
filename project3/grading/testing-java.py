import psycopg2
import os
import sys
import subprocess

def executePrint(s):
	cur.execute(s)
	ans = cur.fetchall()
	print ans
	return ans

print "Compiling..."
subprocess.call(["javac", "-classpath", ".:../json-simple-1.1.1.jar:../postgresql-9.0-801.jdbc3.jar", "JSONProcessing.java"])
score = 0

conn = psycopg2.connect("dbname=flightsskewed user=vagrant")
cur = conn.cursor()

cur.execute("delete from flewon where  flightid = 'SW109' and flightdate = '2015-10-25'")
cur.execute("delete from customers where customerid = 'cust1002'")
cur.execute("delete from customers where customerid = 'cust1003'")
conn.commit()

### SANITY CHECK
ans = executePrint("select * from customers where customerid = 'cust1002'")
if len(ans) == 1:
	print "Something is wrong..."
	sys.exit(1)

## Add a customer who doesn't exist
try:
	print "==== Testing first json update"
	ans = executePrint("select * from customers where customerid = 'cust1002'")
	subprocess.call(["java", "-classpath", ".:../json-simple-1.1.1.jar:../postgresql-9.0-801.jdbc3.jar", "JSONProcessing"], stdin=open("testing-1.json"))
	ans = executePrint("select * from customers where customerid = 'cust1002'")
	if len(ans) == 1 and ans[0][3] == 'AA' and 'cust1002' in ans[0][0]:
		print "--- adding 0.5"
		score += 0.5
except:
	pass

try:
	print "==== Testing second json update"
	ans = executePrint("select * from flewon where flightid = 'SW109' and flightdate = '2015-10-25'")
	subprocess.call(["java", "-classpath", ".:../json-simple-1.1.1.jar:../postgresql-9.0-801.jdbc3.jar", "JSONProcessing"], stdin=open("testing-2.json"))
	ans = executePrint("select * from flewon where flightid = 'SW109' and flightdate = '2015-10-25'")
	if len(ans) == 3:
		print "--- adding 1"
		score += 1
	if len(ans) == 2:
		print "--- adding 0.5"
		score += 0.5
except:
	pass

## Add a customer who exists
try:
	print "==== Testing third json update"
	subprocess.call(["java", "-classpath", ".:../json-simple-1.1.1.jar:../postgresql-9.0-801.jdbc3.jar", "JSONProcessing"], stdin=open("testing-3.json"))
	print "--- adding 0.5"
	score += 0.5
except:
	print "--- adding 0.5 in except"
	score += 0.5
	pass

changescore = raw_input("Type score to proceed [default = {}]? ".format(score))
print "Score = {}".format(score)

import time
import threading
import re
import sqlite3
import datetime

### Connect to the database
conn = sqlite3.connect("tasks.sqlite3")
c = conn.cursor()

### Some variables to keep track of current state
BREAK = 0
RECORDING = 1
currentstate = BREAK
recordingtask = -1

### Regular Expressions
add_pattern = re.compile('^add (.*) (\d+) hours$')
modify_pattern = re.compile('^modify (.*) (\d+) hours$')
start_pattern = re.compile('^start (.*)$')
stop_pattern = re.compile('^stop (.*)$')

### Setting a thread to repeatadly get input from user
inputreceived = False
command = ""

def GetInput():
	global inputreceived
	global command
	command = raw_input()
	inputreceived = True

def StartThread():
	global inputreceived
	inputreceived = False
	t = threading.Thread(target=GetInput)
	t.daemon = True
	t.start()

# Loop
StartThread()
while True:
	if inputreceived:
		# print "Received command = {}".format(command)

		### Act on the command
		if command == "list":
			c.execute("select * from tasks")
			print "=================== Listing all the available projects"
			for row in c:
				print "Project {} -- {} hours".format(row[0], row[1])
		elif command == "summary":
			c.execute("select t.name, t.duration, round(cast(sum(strftime('%s', end) - strftime('%s', start)) as double)/60/60, 3) from log, tasks t where log.task_name = t.name group by t.name, t.duration")
			print "=================== Printing summary of the projects"
			for row in c:
				print "Project {} -- {} hours completed out of {} hours".format(row[0], row[2], row[1])
		else:
			if add_pattern.match(command):
				m = add_pattern.match(command)
				print "Adding a new project {} with {} hours".format(m.group(1), m.group(2))
				c.execute("insert into tasks values (?, ?)", (m.group(1), m.group(2)))
				conn.commit()
			elif modify_pattern.match(command):
				m = modify_pattern.match(command)
				c.execute("update tasks set duration = {} where name = \"{}\"".format(m.group(2), m.group(1)))
				conn.commit()
			elif start_pattern.match(command):
				m = start_pattern.match(command)
				currentstate = RECORDING
				recordingtask = m.group(1)
				c.execute('insert into log(task_name, start, end) values(?, ?, ?)', (recordingtask, datetime.datetime.now(), datetime.datetime.now()))
				conn.commit()
			elif command == "stop": 
				currentstate = BREAK
			else:
				print "Command not understood"

		### Restart listening
		# print "Restarting input thread"
		StartThread()
	else:
		#Depending on the state, do different things
		if currentstate != BREAK:
			#print "Adding one minute to the {}".format(recordingtask)
			c.execute("select * from log where start = (select max(start) from log)")
			row = c.fetchone()
			# Confirm that the row matches
			if row[1] == recordingtask:
				#print "Matches {}".format(row[0])
				c.execute('update log set end = ? where id = ?', (datetime.datetime.now(), row[0]))
				conn.commit()
			else:
				print "Problem"
	time.sleep(2)

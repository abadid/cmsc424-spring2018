import subprocess
from disk_relations import *
from transactions import *
import time
from exampletransactions import *
import sys
import subprocess
import random
import traceback

def runTransactions(tname, tlist):
	for l in tlist:
		threading.Thread(target=tname, args=l).start()
		time.sleep(2)

def runTransactionsNoDelay(tname, tlist):
	for l in tlist:
		threading.Thread(target=tname, args=l).start()


def killAfterSomeTime():
	print "----- STARTING TIMER"
	for i in range(0, 50):
		time.sleep(4)
		print "----- CONTINUING TIMER" + str(i)
	print "----- FAILED with TIME OUT"
	os._exit(0)

if sys.argv[1] in ['test-ixlock']:
	if len(sys.argv) != 4:
		print "Need to specify the relation name, logfile to use and which test to run"
		os._exit(1)

	bpool = BufferPool()
	r = Relation(sys.argv[2])
	LogManager.setAndAnalyzeLogFile(sys.argv[3])

	runTransactions(Transaction1, [(r, "0", 20), (r, "10", 20)])
	time.sleep(3)
	runTransactions(TransactionReadRelation, [(r, 20)])
	time.sleep(10)
	for (k, v) in LockTable.lockhashtable.items():
		print "Object " + str(k) + "; current: " + str(v.current_transactions_and_locks) + "; waiting: " + str(v.waiting_transactions_and_locks)
	correct = dict()
	correct["0"] = "Object 0; current: [(1, 1)]; waiting: []"
	correct["relation1"] = "Object relation1; current: [(1, 3), (2, 3)]; waiting: [(3, 0)]"
	correct["10"] = "Object 10; current: [(2, 1)]; waiting: []"
	for (k, v) in LockTable.lockhashtable.items():
		s = "Object " + str(k) + "; current: " + str(v.current_transactions_and_locks) + "; waiting: " + str(v.waiting_transactions_and_locks)
		if s != correct[k]:
			print "-- FAILED --"
			os._exit(1)
	print "-- PASSED --"
	print "-- PASSED --"
	os._exit(0)
elif sys.argv[1] in ['test1-deadlocks', 'test2-deadlocks', 'test3-deadlocks', 'test4-deadlocks', 'test5-deadlocks', 'test6-deadlocks', 'test7-deadlocks', 'test8-deadlocks']:
	if len(sys.argv) != 4:
		print "Need to specify the relation name, logfile to use and which test to run"
		os._exit(1)
	bpool = BufferPool()
	r = Relation(sys.argv[2])
	LogManager.setAndAnalyzeLogFile(sys.argv[3])

	if sys.argv[1] == 'test1-deadlocks':
		possible = [set([1]), set([2]), set([3])]
		runTransactions(Transaction3, [(r, "0", "10"), (r, "10", "20"), (r, "20", "0")])
	elif sys.argv[1] == 'test2-deadlocks':
		# kill two
		possible = [set([1, 3]), set([1, 4]), set([2, 3]), set([2, 4])]
		runTransactions(Transaction3, [(r, "0", "10"), (r, "10", "0"), (r, "20", "30"), (r, "30", "20")])
	elif sys.argv[1] == 'test3-deadlocks':
		# kill 1 or 3 or 4
		possible = [set([1]), set([3]), set([4])]
		runTransactions(ReadWriteTransaction, [
				(r, [["0", "X"], ["10", "X"]]), 
				(r, [["11", "X"], ["0", "X"]]), 
				(r, [["12", "X"], ["0", "X"]]), 
				(r, [["10", "X"], ["12", "X"]]), 
				]
				)
	elif sys.argv[1] == 'test4-deadlocks':
		possible = [set([])]
		runTransactions(ReadWriteTransaction, [
				(r, [["0", "S"], ["4", "S"]], 1000), 
				(r, [["1", "S"], ["5", "S"]], 1000), 
				(r, [["2", "S"], ["6", "S"]], 1000), 
				(r, [["3", "S"], ["7", "S"]], 1000), 
				(r, [["10", "X"], ["0", "X"]], 10),
				(r, [["20", "X"], ["10", "X"]], 10),
				(r, [["30", "X"], ["1", "X"]], 10),
				(r, [["40", "X"], ["3", "X"]], 10),
				]
				)
	elif sys.argv[1] == 'test5-deadlocks':
		possible = [set([1, 2, 3, 4]), set([5])]
		runTransactions(ReadWriteTransaction, [
				(r, [["0", "S"], ["4", "S"], ["10", "X"]], 10), 
				(r, [["0", "S"], ["4", "S"], ["10", "X"]], 10), 
				(r, [["0", "S"], ["4", "S"], ["10", "X"]], 10), 
				(r, [["0", "S"], ["4", "S"], ["10", "X"]], 10), 
				(r, [["10", "X"], ["0", "X"]], 10),
				]
				)
	elif sys.argv[1] == 'test6-deadlocks':
		possible = [set([1, 2, 3, 4]), set([5]), set([6])]
		runTransactions(ReadWriteTransaction, [
				(r, [["0", "S"], ["4", "S"], ["10", "S"]], 10), 
				(r, [["0", "S"], ["4", "S"], ["10", "S"]], 10), 
				(r, [["0", "S"], ["4", "S"], ["10", "S"]], 10), 
				(r, [["0", "S"], ["4", "S"], ["10", "S"]], 10), 
				(r, [["10", "X"], ["20", "X"]], 10),
				(r, [["20", "X"], ["0", "X"]], 10),
				]
				)
	elif sys.argv[1] == 'test7-deadlocks':
		possible = [set([])]
		runTransactions(ReadWriteTransaction, [
				(r, [["0", "S"], ["4", "S"], ["10", "S"]], 10), 
				(r, [["0", "S"], ["4", "S"], ["10", "S"]], 10), 
				(r, [["0", "S"], ["4", "S"], ["10", "S"]], 10), 
				(r, [["0", "S"], ["4", "S"], ["10", "S"]], 10), 
				(r, [["10", "X"], ["20", "X"]], 10),
				(r, [["20", "X"], ["30", "X"]], 10),
				(r, [["30", "X"], ["5", "X"]], 1000),
				]
				)
	elif sys.argv[1] == 'test8-deadlocks':
		possible = [set([1]), set([2]), set([3]), set([4]), set([5]), set([6]), set([7])]
		runTransactions(ReadWriteTransaction, [
				(r, [["0", "S"], ["1", "S"], ["3", "X"]], 20), 
				(r, [["1", "S"], ["2", "S"], ["4", "X"]], 20), 
				(r, [["2", "S"], ["3", "S"], ["5", "X"]], 20), 
				(r, [["3", "S"], ["4", "S"], ["6", "X"]], 20), 
				(r, [["4", "S"], ["5", "S"], ["7", "X"]], 20), 
				(r, [["5", "S"], ["6", "S"], ["2", "X"]], 20), 
				(r, [["6", "S"], ["7", "S"], ["1", "X"]], 20), 
				]
				)
	threading.Thread(target=killAfterSomeTime).start()
	time.sleep(100)
	try:
		print "Calling deadlock detection code..."
		for (k, v) in LockTable.lockhashtable.items():
			print "Object " + str(k) + "; current: " + str(v.current_transactions_and_locks) + "; waiting: " + str(v.waiting_transactions_and_locks)
		ret = LockTable.detectDeadlocksAndChooseTransactionsToAbort()
		print "Need to abort transactions: " + str(ret)
		print "Answer should be one of: " + str(possible)

		if any(ret == list(x) for x in possible):
			print "----- PASSED"
			os._exit(0)
		else:
			print "----- FAILED"
			os._exit(1)
	except:
		e = sys.exc_info()
		print "-----------------> Failed with exception" + str(e[0])
		print traceback.format_exc()
		print "----- FAILED"
		os._exit(1)
elif sys.argv[1] == 'test-recovery':
	if len(sys.argv) != 3:
		print "Need to specify the test number"
		os._exit(1)
	testno = sys.argv[2]
	bpool = BufferPool()
	relationname = "recoverytest{}_relation".format(testno)
	logfile = "recoverytest{}_logfile".format(testno)
	r = Relation(relationname)
	print "Starting to analyze the logfile " + logfile
	LogManager.setAndAnalyzeLogFile(logfile)

	correctrelationname = "recoverytests-answers/recoverytest{}_relation".format(testno)
	correctlogfile = "recoverytests-answers/recoverytest{}_logfile".format(testno)
	print "Comparing the relations" 
	rel1 = open(relationname, 'r').read()
	rel2 = open(correctrelationname, 'r').read()
	if len(rel1) != len(rel2):
		print "The two files are not the same length"
	diff1 = ""
	diff2 = ""
	for i in range(Globals.blockSize, min(len(rel1), len(rel2))): 
		if rel1[i] != rel2[i]:
			print "difference at character {}: rel1 = {} and rel2 = {}".format(i, rel1[i], rel2[i])
			diff1 += rel1[i]
			diff2 += rel2[i]
		#else:
			#print "same character {}: rel1 = {} and rel2 = {}".format(i, rel1[i], rel2[i])
	print "Comparing the logfiles" 
	subprocess.call(["diff", logfile, correctlogfile])
	if diff1 == "":
		print "-- PASSED --"
		os._exit(0)
	else:
		print "-- FAILED --"
		print "-- diff1: " + diff1
		print "-- diff2: " + diff2
		os._exit(1)

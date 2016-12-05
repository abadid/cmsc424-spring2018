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

if sys.argv[1] in ['test1-deadlocks', 'test2-deadlocks', 'test3-deadlocks']:
	if len(sys.argv) != 4:
		print "Need to specify the relation name, logfile to use and which test to run"
		os._exit(1)
	bpool = BufferPool()
	r = Relation(sys.argv[2])
	LogManager.setAndAnalyzeLogFile(sys.argv[3])

	if sys.argv[1] == 'test1-deadlocks':
		possible = [set([1]), set([2]), set([3])]
		runTransactions(Transaction3, [(r, "0", "10"), (r, "10", "20"), (r, "20", "10")])
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
		else:
			print "----- FAILED"
			print "*** NOTE: These tests assume that you have implemented IX locks properly ***"
		os._exit(0)
	except:
		e = sys.exc_info()
		print "-----------------> Failed with exception" + str(e[0])
		print traceback.format_exc()
		print "----- FAILED"
		os._exit(0)
elif sys.argv[1] == 'test-recovery':
	if len(sys.argv) != 4:
		print "Need to specify the relation name, logfile to use and which test to run"
		os._exit(1)
	if not os.path.isfile(sys.argv[2]) or not os.path.isfile(sys.argv[3]):
		print "Provided logfile or relationfile does not exist.. can't test recovery code"
	else:
		bpool = BufferPool()
		r = Relation(sys.argv[2])
		print "Starting to analyze the logfile " + sys.argv[3]
		LogManager.setAndAnalyzeLogFile(sys.argv[3])
		print "Finished calling restart recovery code... the logfile {} should now end with a CHECKPOINT record and the relation file {} should be in a consistent state (compare with provided answer)".format(sys.argv[3], sys.argv[2])

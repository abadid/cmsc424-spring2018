import math
from disk_relations import *
from queryprocessing import *
import sys
from collections import Counter
import re
import pickle
import imp
import sqlite3
import traceback

import random

# A simple class to keep track of the set of relations and indexes created together
class Database:
	def __init__(self, name):
		self.name = name
		self.relations = dict()
		self.indexes = dict()
	def newRelation(self, relname, rel_schema):
		self.relations[relname] = Relation(relname, rel_schema)
		return self.relations[relname]
	def getRelation(self, relname):
		return self.relations[relname]

########################################
from functools import wraps
import errno
import os
import signal

class TimeoutError(Exception):
    pass

def timeout(seconds=100, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator
########################################

@timeout(100)
def collectAll(plan):
	ret = list()
	plan.init()
	#print "collectall -->"
	for t in plan.get_next():
		#print t
		s = re.sub('[\(\[\)\]\']', '', str(t))
		ret.append(re.sub('None', 'NULL', s))
	return Counter(ret)


def aggregateRelations(db):
	S_Schema = ["B", "C", "D"]
	random.seed(0)

	Brange = range(0, 100)
	Crange = range(-100, 100, 2)
	Drange = range(-100, 0)
	random.shuffle(Brange)
	random.shuffle(Crange)
	random.shuffle(Drange)

	Bvalues = [Brange[i] for i in range(0, 100) for j in range(0, i)]
	Cvalues = [Crange[i] for i in range(0, 100) for j in range(0, i)]
	Dvalues = [Drange[i] for i in range(0, 100) for j in range(0, i)]

	random.shuffle(Bvalues)
	random.shuffle(Cvalues)
	random.shuffle(Dvalues)

	S_Schema = ["B", "C", "D"]
	agg_relation = db.newRelation("agg_relation", S_Schema)

	for i in range(0, len(Bvalues)):
		agg_relation.insertTuple(Tuple(S_Schema, (str(Bvalues[i]), str(Cvalues[i]), str(Dvalues[i]))))

	return agg_relation

def joinRelations(db):
	R_Schema = ["A", "B"]
	S_Schema = ["B", "C"]
	R = db.newRelation("R", R_Schema)
	S = db.newRelation("S", S_Schema)

	random.seed(0)

	for i in range(0, 5):
		R.insertTuple(Tuple(R_Schema, ("0", str(i))))
		S.insertTuple(Tuple(S_Schema, (str(i), "0")))

	for i in range(0, 5):
		R.insertTuple(Tuple(R_Schema, ("1", str(i))))

	for i in range(0, 5):
		S.insertTuple(Tuple(S_Schema, (str(i), "2")))

	for i in range(0, 100):
		if random.random() > 0.3:
			R.insertTuple(Tuple(R_Schema, ("3", str(i))))
		if random.random() > 0.3:
			S.insertTuple(Tuple(S_Schema, (str(i), "3")))

	for i in range(0, 100):
		if random.random() > 0.3:
			R.insertTuple(Tuple(R_Schema, ("4", str(i%20))))
		if random.random() > 0.3:
			S.insertTuple(Tuple(S_Schema, (str(i%20), "4")))

	for i in range(0, 2000):
		R.insertTuple(Tuple(R_Schema, ("5", str(i))))
		S.insertTuple(Tuple(S_Schema, (str(i), "5")))

	return (R, S)

def setMinusRelations(db):
	R_Schema = ["A", "B"]
	R1 = db.newRelation("R1", R_Schema)
	R2 = db.newRelation("R2", R_Schema)

	random.seed(0)

	for i in range(0, 10):
		R1.insertTuple(Tuple(R_Schema, ("0", str(i))))
		R2.insertTuple(Tuple(R_Schema, ("0", str(i))))

	for i in range(0, 100):
		if random.random() > 0.3:
			R1.insertTuple(Tuple(R_Schema, ("1", str(i))))
		if random.random() > 0.3:
			R2.insertTuple(Tuple(R_Schema, ("1", str(i))))

	for i in range(0, 10):
		R1.insertTuple(Tuple(R_Schema, ("2", "2")))
		R2.insertTuple(Tuple(R_Schema, ("2", "2")))

	for i in range(0, 100):
		if random.random() > 0.3:
			R1.insertTuple(Tuple(R_Schema, ("3", str(i%20))))
		if random.random() > 0.3:
			R2.insertTuple(Tuple(R_Schema, ("3", str(i%20))))

	for i in range(0, 10):
		R1.insertTuple(Tuple(R_Schema, ("4", str(i))))

	for i in range(0, 10):
		R2.insertTuple(Tuple(R_Schema, ("5", str(i))))

	for i in range(0, 2000):
		if random.random() > 0.5:
			R1.insertTuple(Tuple(R_Schema, ("6", str(i%200))))
		if random.random() > 0.5:
			R2.insertTuple(Tuple(R_Schema, ("6", str(i%200))))

	return (R1, R2)


if sys.argv[1] == 'pickle':
	raise ValueError("Don't run with this option -- it will overwrite the data.pkl file which contains the correct answers")
	output = open('data.pkl', 'wb')
	db = Database("test")
	aggregateRelations(db)
	joinRelations(db)
	setMinusRelations(db)
	pickle.dump(db, output)
else:
	pkl_file = open('data.pkl', 'rb')
	db = pickle.load(pkl_file)
	correctanswers = pickle.load(pkl_file)
	pkl_file.close()

queryno = int(sys.argv[2])

agg_relation = db.getRelation("agg_relation")
joinrel_1 = db.getRelation("R")
joinrel_2 = db.getRelation("S")
smrel_1 = db.getRelation("R1")
smrel_2 = db.getRelation("R2")


queries = [
	('aggr 1', GroupByAggregate(SequentialScan(agg_relation), "B", GroupByAggregate.AVERAGE), 1), 
	('aggr 2', GroupByAggregate(SequentialScan(agg_relation), "C", GroupByAggregate.AVERAGE), 1), 
	('aggr 3', GroupByAggregate(SequentialScan(agg_relation), "D", GroupByAggregate.AVERAGE), 1), 
	('aggr 4', GroupByAggregate(SequentialScan(agg_relation, Predicate("B", "nomatch")), "B", GroupByAggregate.AVERAGE), 1), 
	('aggr 5', GroupByAggregate(SequentialScan(agg_relation), "B", GroupByAggregate.MEDIAN), 1), 
	('aggr 6', GroupByAggregate(SequentialScan(agg_relation), "C", GroupByAggregate.MEDIAN), 1), 
	('aggr 7', GroupByAggregate(SequentialScan(agg_relation), "D", GroupByAggregate.MEDIAN), 1), 
	('aggr 8', GroupByAggregate(SequentialScan(agg_relation, Predicate("B", "nomatch")), "B", GroupByAggregate.MEDIAN), 1), 
	('aggr 9', GroupByAggregate(SequentialScan(agg_relation), "B", GroupByAggregate.MODE), 1), 
	('aggr 10', GroupByAggregate(SequentialScan(agg_relation), "C", GroupByAggregate.MODE), 1), 
	('aggr 11', GroupByAggregate(SequentialScan(agg_relation), "D", GroupByAggregate.MODE), 1), 
	('aggr 12', GroupByAggregate(SequentialScan(agg_relation, Predicate("B", "nomatch")), "B", GroupByAggregate.MODE), 1), 

	('smj 1', SortMergeJoin(SequentialScan(joinrel_1, Predicate("A", "0")), SequentialScan(joinrel_2, Predicate("C", "0")), "B", "B", SortMergeJoin.FULL_OUTER_JOIN), 1),
	('smj 2', SortMergeJoin(SequentialScan(joinrel_1, Predicate("A", "1")), SequentialScan(joinrel_2, Predicate("C", "1")), "B", "B", SortMergeJoin.FULL_OUTER_JOIN), 1),
	('smj 3', SortMergeJoin(SequentialScan(joinrel_1, Predicate("A", "2")), SequentialScan(joinrel_2, Predicate("C", "2")), "B", "B", SortMergeJoin.FULL_OUTER_JOIN), 1),
	('smj 4', SortMergeJoin(SequentialScan(joinrel_1, Predicate("A", "3")), SequentialScan(joinrel_2, Predicate("C", "3")), "B", "B", SortMergeJoin.FULL_OUTER_JOIN), 1),
	('smj 5', SortMergeJoin(SequentialScan(joinrel_1, Predicate("A", "4")), SequentialScan(joinrel_2, Predicate("C", "4")), "B", "B", SortMergeJoin.FULL_OUTER_JOIN), 2),
	('smj 6', SortMergeJoin(SequentialScan(joinrel_1, Predicate("A", "5")), SequentialScan(joinrel_2, Predicate("C", "5")), "B", "B", SortMergeJoin.FULL_OUTER_JOIN), 2),

	('setminus 1', SetMinus(SequentialScan(smrel_1, Predicate("A", "0")), SequentialScan(smrel_2, Predicate("A", "0")), keep_duplicates = False), 1),
	('setminus 2', SetMinus(SequentialScan(smrel_1, Predicate("A", "1")), SequentialScan(smrel_2, Predicate("A", "1")), keep_duplicates = False), 1),
	('setminus 3', SetMinus(SequentialScan(smrel_1, Predicate("A", "2")), SequentialScan(smrel_2, Predicate("A", "2")), keep_duplicates = True), 1),
	('setminus 4', SetMinus(SequentialScan(smrel_1, Predicate("A", "3")), SequentialScan(smrel_2, Predicate("A", "3")), keep_duplicates = True), 1),
	('setminus 5', SetMinus(SequentialScan(smrel_1, Predicate("A", "4")), SequentialScan(smrel_2, Predicate("A", "4")), keep_duplicates = True), 1),
	('setminus 6', SetMinus(SequentialScan(smrel_1, Predicate("A", "5")), SequentialScan(smrel_2, Predicate("A", "5")), keep_duplicates = True), 1),
	('setminus 7', SetMinus(SequentialScan(smrel_1, Predicate("A", "6")), SequentialScan(smrel_2, Predicate("A", "6")), keep_duplicates = True), 1),
	('setminus 8', SetMinus(SequentialScan(smrel_1, Predicate("A", "6")), SequentialScan(smrel_2, Predicate("A", "6")), keep_duplicates = False), 1)
	]


def check_answer(queryno, diff, c_ans):
	total = 0
	print "----- checking answer"
	for x in diff:
		if diff[x] != 0:
			print "{}: count = {}".format(x, diff[x])
		total = total + abs(diff[x])
	if total == 0:
		return True
	else:
		if queryno < 12:
			items = diff.items()
			if len(items) == 2:
				if items[1][0] == 'NULL':
					return items[0][0] == '0'
				if items[0][0] == 'NULL':
					return items[1][0] == '0'
				if abs(float(items[0][0]) - float(items[1][0])) < 1:
					return True
				else:
					print "----- difference too high for aggregate"
					print diff
					return False
			else:
				print "Not sure how the length is not 2"
				return False
		else:
			return False

try:
	answers = [None for i in range(0, len(queries))]
	for i in range(0, len(queries)):
		if queryno == -1 or i == queryno:
			q = queries[i][1]
			q.init()
			print "--------------------------------------------------------------------- Executing Query {}".format(queries[i][0])
			answers[i] = collectAll(q)


	if sys.argv[1] == 'pickle':
		pickle.dump(answers, output)
		output.close()
	else:
		# compare
		for i in range(0, len(queries)):
			if queryno == -1 or i == queryno:
				print "--------------------------------------------------------------------- Checking Query {}".format(queries[i][0])
				ans = answers[i]
				c_ans = correctanswers[i]

				print "************ submission "
				print ans
				print "************ correct "
				print c_ans

				ans.subtract(c_ans)
				if check_answer(queryno, ans, c_ans):
					print "Correct"
				else:
					print "Not the same -- however, partial credit may have been awarded"
					for x in ans:
						print "{} : {}".format(x, c_ans[x])
except:
	e = sys.exc_info()
	print "-----------------> Failed the case with exception" + str(e[0]) 
	print traceback.format_exc()

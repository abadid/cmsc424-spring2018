import math
from disk_relations import *
from btree import *
from queryprocessing import *
from create_sample_databases import *
import sys

import random

def testQueriesExampleDB():
	db1 = createDatabase1("whateve")
	scan1 = SequentialScan(db1.getRelation("instructor"))
	aggr = MyGroupByAggregate(scan1, "salary", GroupByAggregate.SUM, "dept_name")
	print "==================== Executing A Groupby Aggregate Query ================"
	aggr.init()
	for t in aggr.get_next():
		print "---> " + str(t)

def testQueries():
	## Let's first create a relation with a bunch of tuples 
	db = Database("test")

	R_Schema = ["A", "B"]
	S_Schema = ["B", "C", "D"]

	Cvalues = [1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 0]
	Dvalues = [5, 5, 5, 5, 3, 2, 2, 1, 1, 1, 0]
	random.shuffle(Cvalues)
	random.shuffle(Dvalues)

	R = db.newRelation("R", R_Schema)
	R2 = db.newRelation("R2", R_Schema)
	S = db.newRelation("S", S_Schema)

	random.seed(0)
	for i in range(0, 10):
		R.insertTuple(Tuple(R_Schema, (str(i), str(i+3))))
		if random.random() < 0.5:
			R2.insertTuple(Tuple(R_Schema, (str(i), str(i+3))))
			R2.insertTuple(Tuple(R_Schema, (str(i), str(i+3))))
			R2.insertTuple(Tuple(R_Schema, (str(i), str(i+3))))
		S.insertTuple(Tuple(S_Schema, (str(i+1), str(Cvalues[i]), str(Dvalues[i]))))
	i = 10
	S.insertTuple(Tuple(S_Schema, (str(i+1), str(Cvalues[i]), str(Dvalues[i]))))

	R.printTuples()
	R2.printTuples()
	S.printTuples()

	queries = [GroupByAggregate(SequentialScan(S), "C", GroupByAggregate.AVERAGE), 
		GroupByAggregate(SequentialScan(S), "C", GroupByAggregate.MEDIAN), 
		GroupByAggregate(SequentialScan(S), "C", GroupByAggregate.MODE), 
		SetMinus(SequentialScan(R2), SequentialScan(R), keep_duplicates = True),
		SetMinus(SequentialScan(R2), SequentialScan(R), keep_duplicates = False),
		SortMergeJoin(SequentialScan(R), SequentialScan(S), "B", "B", SortMergeJoin.FULL_OUTER_JOIN)]


	for i in range(0, len(queries)):
		queries[i].init()
		print "--- Executing Query {}".format(i)
		for t in queries[i].get_next():
			print  str(t)

testQueries()

from pyspark import SparkContext
from functions import *
import re
import sys

sc = SparkContext("local", "Simple App")
setDefaultAnswer(sc.parallelize([0]))

taskno = int(sys.argv[1])

if taskno == 1 or taskno == -1:
	playRDD = sc.textFile("bigdatafiles/play.txt")
	### Task 1
	print "=========================== Task 1"
	task1_result = task1(playRDD)
	for x in task1_result.takeOrdered(100):
		print x

if taskno == 2 or taskno == -1:
	### Task 2
	print "=========================== Task 2"
	nobelRDD = sc.textFile("bigdatafiles/prize.json")
	task2_result = nobelRDD.map(json.loads).flatMap(task2_flatmap).distinct()
	for x in task2_result.takeOrdered(100):
		print x.encode('utf-8')

if taskno == 3 or taskno == -1:
	#### Task 3
	print "=========================== Task 3"
	nobelRDD = sc.textFile("bigdatafiles/prize.json")
	task3_result = task3(nobelRDD)
	for x in task3_result.takeOrdered(100):
		print x

if taskno == 4 or taskno == -1:
	#### Task 4
	logsRDD = sc.textFile("bigdatafiles/NASA_logs_sample.txt")
	print "=========================== Task 4"
	task4_result = task4(logsRDD, ['02/Jul/1995', '03/Jul/1995', '04/Jul/1995', '05/Jul/1995', '06/Jul/1995'])
	for x in task4_result.takeOrdered(100):
		print x.encode('utf-8')

if taskno == 5 or taskno == -1:
	#### Task 5
	print "=========================== Task 5"
	amazonInputRDD = sc.textFile("bigdatafiles/amazon-ratings.txt")
	amazonBipartiteRDD = amazonInputRDD.map(lambda x: x.split(" ")).map(lambda x: (x[0], x[1])).distinct()
	task5_result = task5(amazonBipartiteRDD)
	for x in task5_result.takeOrdered(100):
		print x

if taskno == 6 or taskno == -1:
	#### Task 6
	print "=========================== Task 6"
	logsRDD = sc.textFile("bigdatafiles/NASA_logs_sample.txt")
	task6_result = task6(logsRDD, '03/Jul/1995', '05/Jul/1995')
	for x in task6_result.takeOrdered(100):
		print x

if taskno == 7 or taskno == -1:
	#### Task 7
	print "=========================== Task 7"
	nobelRDD = sc.textFile("bigdatafiles/prize.json")
	task7_result = task7(nobelRDD)
	for x in task7_result.takeOrdered(100):
		print x

if taskno == 8 or taskno == -1:
	#### Task 8 -- we will start with a non-empty currentMatching and do a few iterations
	amazonInputRDD = sc.textFile("bigdatafiles/amazon-ratings.txt")
	amazonBipartiteRDD = amazonInputRDD.map(lambda x: x.split(" ")).map(lambda x: (x[0], x[1])).distinct()
	print "=========================== Task 8"
	currentMatching = sc.parallelize([('user1', 'product8')])
	res1 = task8(amazonBipartiteRDD, currentMatching)
	print "Found {} edges to add to the matching".format(res1.count())
	for x in res1.takeOrdered(100):
		print x
	currentMatching = currentMatching.union(res1)
	res2 = task8(amazonBipartiteRDD, currentMatching)
	print "Found {} edges to add to the matching".format(res2.count())
	for x in res2.takeOrdered(100):
		print x
	currentMatching = currentMatching.union(res2)

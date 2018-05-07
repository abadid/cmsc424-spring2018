from pyspark import SparkContext
from tasks import *
import re

sc = SparkContext("local", "Simple App")
sc.setLogLevel("OFF")

project_path = "/vagrant"
python_path = project_path + "/python"

sc.addPyFile(python_path + '/tasks.py')
sc.addPyFile(python_path + '/fragAndReplicate.py')

datafiles_path = project_path + "/datafiles"

## Load data into RDDs
playRDD = sc.textFile(datafiles_path + "/play.txt")
logsRDD = sc.textFile(datafiles_path + "/NASA_logs_sample.txt")
amazonInputRDD = sc.textFile(datafiles_path + "/amazon-ratings.txt")
nobelRDD = sc.textFile(datafiles_path + "/prize.json")
flewonRDD = sc.textFile(datafiles_path + "/flewon.csv")

## The following converts the flewonRDD into 3-tuples
flewonRDD = flewonRDD.map(lambda x: tuple(x.split(",")))

## The following converts the amazonInputRDD into 2-tuples with integers
amazonBipartiteRDD = amazonInputRDD.map(lambda x: x.split(" ")).map(lambda x: (x[0], x[1])).distinct()


### Task 1
print "=========================== Task 1"
task1_result = task1(playRDD)
for x in task1_result.collect():
	print x

### Task 2
print "=========================== Task 2"
task2_result = nobelRDD.map(json.loads).flatMap(task2_flatmap)
for x in task2_result.collect():
	print x

#### Task 3
print "=========================== Task 3"
task3_result = task3(nobelRDD)
for x in task3_result.collect():
	print x

#### Task 4
print "=========================== Task 4"
task4_result = task4(logsRDD, ['/facilities/vab.html', '/images/vab-small.gif'])
for x in task4_result.collect():
	print x

#### Task 5
print "=========================== Task 5"
task5_result = task5(amazonBipartiteRDD)
print task5_result.collect()

#### Task 6
print "=========================== Task 6"
task6_result = task6(logsRDD, 'ppp199.aix.or.jp', 'drjo002a099.embratel.net.br')
for x in task6_result.collect():
	print x

#### Task 7
print "=========================== Task 7"
task7_result = task7(nobelRDD)
for x in task7_result.collect():
	print x

#### Task 8
print "=========================== Task 8"
task8_result = task8(flewonRDD, 4, 5)
for x in task8_result.collect():
    print x

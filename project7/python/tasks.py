import json
import re
from fragAndReplicate import fragment_and_replicate
from pyspark import SparkContext

def task1(playRDD):
    return playRDD

def task2_flatmap(x):
    return []

def task3(nobelRDD):
    return nobelRDD

def task4(logsRDD, l):
    return logsRDD

def task5(bipartiteGraphRDD):
    return bipartiteGraphRDD

def task6(logsRDD, day1, day2):
    return logsRDD

def task7(nobelRDD):
    return nobelRDD

def task8(flewon, n, m):
    fragment_and_replicate()
    return flewon

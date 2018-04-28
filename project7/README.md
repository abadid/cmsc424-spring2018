# Project 7

Project 7 focuses on using Apache Spark for doing large-scale data analysis tasks. For this assignment, we will use relatively small datasets and  we won't run anything in distributed mode; however Spark can be easily used to run the same programs on much larger datasets.

## Getting Started with Spark

This guide is basically a summary of the excellent tutorials that can be found at the [Spark website](http://spark.apache.org).

[Apache Spark](https://spark.apache.org) is a relatively new cluster computing framework, developed originally at UC Berkeley. It significantly generalizes
the 2-stage Map-Reduce paradigm (originally proposed by Google and popularized by open-source Hadoop system); Spark is instead based on the abstraction of **resilient distributed datasets (RDDs)**. An RDD is basically a distributed collection 
of items, that can be created in a variety of ways. Spark provides a set of operations to transform one or more RDDs into an output RDD, and analysis tasks are written as
chains of these operations.

Spark can be used with the Hadoop ecosystem, including the HDFS file system and the YARN resource manager. 

### Installing Spark

As before, we have provided a VagrantFile in the `project5` directory. Since the Spark distribution is large, we ask you to download that directly from the Spark website.

1. Download the Spark package at http://spark.apache.org/downloads.html. We will use **Version 2.0.1, Pre-built for Hadoop 2.7 or later**.
2. Move the downloaded file to the `project5/` directory (so it is available in '/vagrant' on the virtual machine), and uncompress it using: 
`tar zxvf spark-2.0.1-bin-hadoop2.7.tgz`
3. This will create a new directory: `spark-2.0.1-bin-hadoop2.7`. 
4. Set the SPARKHOME variable: `export SPARKHOME=/vagrant/spark-2.0.1-bin-hadoop2.7`

We are ready to use Spark. 

### Spark and Python

Spark primarily supports three languages: Scala (Spark is written in Scala), Java, and Python. We will use Python here -- you can follow the instructions at the tutorial
and quick start (http://spark.apache.org/docs/latest/quick-start.html) for other languages. The Java equivalent code can be very verbose and hard to follow. The below
shows a way to use the Python interface through the standard Python shell.

### PySpark Shell

You can also use the PySpark Shell directly.

1. `$SPARKHOME/bin/pyspark`: This will start a Python shell (it will also output a bunch of stuff about what Spark is doing). The relevant variables are initialized in this python
shell, but otherwise it is just a standard Python shell.

2. `>>> textFile = sc.textFile("README.md")`: This creates a new RDD, called `textFile`, by reading data from a local file. The `sc.textFile` commands create an RDD
containing one entry per line in the file.

3. You can see some information about the RDD by doing `textFile.count()` or `textFile.first()`, or `textFile.take(5)` (which prints an array containing 5 items from the RDD).

4. We recommend you follow the rest of the commands in the quick start guide (http://spark.apache.org/docs/latest/quick-start.html). Here we will simply do the Word Count
application.

#### Word Count Application

The following command (in the pyspark shell) does a word count, i.e., it counts the number of times each word appears in the file `README.md`. Use `counts.take(5)` to see the output.

`>>> counts = textfile.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)`

Here is the same code without the use of `lambda` functions.

```
def split(line): 
    return line.split(" ")
def generateone(word): 
    return (word, 1)
def sum(a, b):
    return a + b

textfile.flatMap(split).map(generateone).reduceByKey(sum)
```

The `flatmap` splits each line into words, and the following `map` and `reduce` do the counting (we will discuss this in the class, but here is an excellent and detailed
description: [Hadoop Map-Reduce Tutorial](http://hadoop.apache.org/docs/r1.2.1/mapred_tutorial.html#Source+Code) (look for Walk-Through).

The `lambda` representation is more compact and preferable, especially for small functions, but for large functions, it is better to separate out the definitions.

### Running it as an Application

Instead of using a shell, you can also write your code as a python file, and *submit* that to the spark cluster. The `project7` directory contains a python file `wordcount.py`,
which runs the program in a local mode. To run the program, do:
`$SPARKHOME/bin/spark-submit wordcount.py`

### More...

We encourage you to look at the [Spark Programming Guide](https://spark.apache.org/docs/latest/programming-guide.html) and play with the other RDD manipulation commands. 
You should also try out the Scala and Java interfaces.

## Assignment Details

We have provided a Python file: `assignment.py`, that initializes the folllowing RDDs:
* An RDD consisting of lines from a Shakespeare play (`play.txt`)
* An RDD consisting of lines from a log file (`NASA_logs_sample.txt`)
* An RDD consisting of 2-tuples indicating user-product ratings from Amazon Dataset (`amazon-ratings.txt`)
* An RDD consisting of 3-tuples representing the flewon table from `project1` (`flewon.csv`)
* An RDD consisting of JSON documents pertaining to all the Noble Laureates over last few years (`prize.json`)

The file also contains some examples of operations on these RDDs. 

Your tasks are to fill out the 8 functions that are defined in the `task.py` file (starting with `task`). The amount of code that you 
write would typically be small (several would be one-liners). 

To run the code written in tasks.py you can run `$SPARKHOME/bin/spark-submit python/assignment.py`

- **Task 1 (4pt)**: This takes as input the playRDD and for each line, finds the first word in the line, and also counts the number of words. It should then filter the RDD by only selecting the lines where the count of words in the line is > 10. The output will be an RDD where the key is the first word in the line, and the value is a 2-tuple, the first being the line and the second being the number of words (which must be >10). Simplest way to do it is probably a `map` followed by a `filter`.

- **Task 2 (4pt)**: Write just the flatmap function (`task2_flatmap`) that takes in a parsed JSON document (from `prize.json`) and returns the surnames of the Nobel Laureates. In other words, the following command should create an RDD with all the surnames. We will use `json.loads` to parse the JSONs (this is already done). Make sure to look at what it returns so you know how to access the information inside the parsed JSONs (these are basically nested dictionaries). (https://docs.python.org/2/library/json.html)
```
     	task2_result = nobelRDD.map(json.loads).flatMap(task2_flatmap)
```

- **Task 3 (4pt)**: Write a sequence of transformations starting from prizeRDD that returns an PairRDD where the key is the `category` (`physics` etc), and the value is a list of all Nobel Laureates for that category (just their surnames). Make sure the final values are `list`s, and not some other class objects (if you do a `take(5)`, it should print out the lists).

- **Task 4 (4pt)**: This function operates on the `logsRDD`. It takes as input a list of *dates* and returns an RDD with "hosts" that were present in the log on all of 
those dates. The dates would be provided as strings, in the same format that they appear in the logs (e.g., '01/Jul/1995' and '02/Jul/1995').
The format of the log entries should be self-explanatory, but here are more details if you need: [NASA Logs](http://ita.ee.lbl.gov/html/contrib/NASA-HTTP.html)
Try to minimize the number of RDDs you end up creating.

- **Task 5 (4pt)**: Complete a function to calculate the degree distribution of user nodes in the Amazon graph (i.e., `amazonBipartiteRDD`). In other words, calculate 
the degree of 
each user node (i.e., number of products each user has rated), and then use a reduceByKey (or aggregateByKey) to find the number of nodes with a given degree. The output 
should be a PairRDD where the key is the degree, and the value is the number of nodes in the graph with that degree.

- **Task 6 (4pt)**: On the `logsRDD`, for two given days (provided as input analogous to Task 4 above), use a 'cogroup' to create the following RDD: the key of 
the RDD will be a host, and the value will be a 2-tuple, where the first element is a list of all URLs fetched from that host on the first day, and the second element
is the list of all URLs fetched from that host on the second day. Use `filter` to first create two RDDs from the input `logsRDD`.

- **Task 7 (8pt)**: [Bigrams](http://en.wikipedia.org/wiki/Bigram) are sequences of two consecutive words. For example, the previous sentence contains the following bigrams: "Bigrams are", "are simply", "simply sequences", "sequences of", etc. Your task is to write a bigram counting application for counting the bigrams in the `motivation`s of the Nobel Prizes (i.e., the reason they were given the Nobel Prize). The return value should be a PairRDD where the key is a bigram, and the value is its count, i.e., in how many different `motivations` did it appear. Don't assume 'motivation' is always present.

- **Task 8 (8pt)**: Your goal for task 8 is to implement the fragment and replicate join from Section 18.5.2.2 of the textbook using SparkPrimitives. Recall from lecture that fragment and replicate join is a way of joining two relations in a parallel database system by partitioning the tuples of each relation across multiple processors, joining the tuples at each processor, then aggregating the results from all the processors. Since you are running Spark on a single machine, your fragment and replicate join implementation will replace processors with explicit groups. Your implementation of fragment-and-replicate join should work roughly as follows:
    * Partition the left and right relations into n and m partitions, respectively.
    * For each of the n partitions of the left relation, assign the tuples in the partition to m groups. Do the same for the right relation, reversing the role of n and m.
    * For each of the n * m groups, join the tuples in that group using a join algorithm of your choosing (nested loop join would be the easiest).
    * Aggregate the joined tuples in each group together into a single relation.

Some Spark primitives that may be helpful for your implementation are listed below. You are not required to use any of these primitives, and you are allowed to use any Spark primitives (the ones listed in the documentation in the assigned reading for April 30) that are not listed here except join. (That join probably won’t help you anyway, since it is only an equi-join).
    * zipWithIndex(): Assigns each tuple in the relation a unique index starting at zero.
    * flatMap(f): Returns a new relation that is the result of applying f to each tuple then flattening the resulting lists.
    * groupByKey(): Groups the values for each key in the RDD into a single sequence.
    * cogroup(): Combines two relations by key.

After you’ve implemented fragment-and-replicate join, you will put it to use by implementing a SQL query using Spark primitives. Since the fragment-and-replicate join algorithm is particularly useful for inequality-based joins, we will revisit Query 10 from Project 1, which you wrote earlier this semester using the flights database. The reference solution for this query can be found in repo under project1.  Write your fragment and replicate join in either fragAndReplicate.py or FragmentAndReplicateJoin.java.




### Correct Answers
You can use spark-submit to run the `assignment.py` file and see the output of all tasks, but it would be easier to develop with pyspark (by copying the commands over). We will also shortly post iPython instructions.

**correctanswers/correctX** has the results of taskX`

### Submission

Submit the `tasks.py` file.


# Project 7: Apache Spark

Project 7 focuses on using Apache Spark for doing large-scale data analysis tasks. For this assignment, we will use relatively small datasets and  we won't run anything in distributed mode; however Spark can be easily used to run the same programs on much larger datasets.

## Getting Started with Spark

This section is basically a summary of the excellent tutorials that can be found at the [Spark website](http://spark.apache.org).

<<<<<<< HEAD
[Apache Spark](https://spark.apache.org) is a relatively new cluster computing framework, developed originally at UC Berkeley. It significantly generalizes the two-stage Map-Reduce paradigm originally proposed by Google and popularized by the open-source Hadoop system. Spark is fundamentally based on the abstraction of **resilient distributed datasets (RDDs)**. An RDD is basically a distributed collection of items that can be created in a variety of ways. Spark provides a set of operations to transform one or more RDDs into an output RDD, and analysis tasks are written as chains of these operations.
=======
[Apache Spark](https://spark.apache.org) is a relatively new cluster computing framework, developed originally at UC Berkeley. It significantly generalizes the two-stage Map-Reduce paradigm originally proposed by Google and popularized by open-source Hadoop system. Spark is fundamentally based on the abstraction of **resilient distributed datasets (RDDs)**. An RDD is basically a distributed collection of items that can be created in a variety of ways. Spark provides a set of operations to transform one or more RDDs into an output RDD, and analysis tasks are written as chains of these operations.
>>>>>>> e744d4304a422776e3ef60a7090f10851dd0e0a0

Spark can be used with the Hadoop ecosystem, including the HDFS file system and the YARN resource manager. 

### Installing Spark

<<<<<<< HEAD
We have provided a Vagrantfile in the `project7` directory. Navigate to the `project7` directory and run `vagrant up` to start the virtual machine, which should have everything you need (except for Spark) to work on this project. Since the Spark distribution is large, we ask you to download it directly from the Spark website.

1. Download the Spark package at http://spark.apache.org/downloads.html. We will use **Version 2.0.1, Pre-built for Hadoop 2.7 or later**.
2. Move the downloaded file to the `project7` directory (so it is available in `/vagrant` on the virtual machine), and uncompress it using: `tar zxvf spark-2.0.1-bin-hadoop2.7.tgz`
=======
We have provided a Vagrantfile in the `project7` directory. Navigate to the `project 5` directory and run `vagrant up` to start the virtual machine, which should have everything you need except for Spark to work on this project. Since the Spark distribution is large, we ask you to download it directly from the Spark website.

1. Download the Spark package at http://spark.apache.org/downloads.html. We will use **Version 2.0.1, Pre-built for Hadoop 2.7 or later**.
2. Move the downloaded file to the `project7/` directory (so it is available in `/vagrant` on the virtual machine), and uncompress it using: `tar zxvf spark-2.0.1-bin-hadoop2.7.tgz`
>>>>>>> e744d4304a422776e3ef60a7090f10851dd0e0a0
3. This will create a new directory: `spark-2.0.1-bin-hadoop2.7` 
4. Set the SPARKHOME environment variable: `export SPARKHOME=/vagrant/spark-2.0.1-bin-hadoop2.7`
5. Test that Spark has been successfully installed by running: `$SPARKHOME/bin/pyspark`. This should run the Spark Python shell, which is a REPL which you can use for prototyping your Python code (there is not a corresponding Spark shell for Java).

### Writing Spark Code

Spark primarily supports three languages: Scala (Spark is written in Scala), Java, and Python. For this project, you have the option of writing your code in either Python or Java. Feel free to work with whichever language you are most comfortable with. You are highly encouraged to read the [Spark Quick Start Guide](http://spark.apache.org/docs/latest/quick-start.html), which has well-written tutorials for working with both languages.

#### Spark and Python

All files for implementing this project in Python are located in the `python` directory. You will write your code for completing each task in `tasks.py`, which contains a function for each task. Your implementation of fragment-and-replicate join for Task 8 should go in `fragAndReplicate.py`. We have also provided a file called `assignment.py` that will call your implementation of each task and print out the results.

You can prototype your Python code using the Spark Python shell, which you can start by running `$SPARKHOME/bin/pyspark`. After you've written your code in `tasks.py`, you can see the results of running `assignment.py` by submitting it to the Spark cluster, which is done by running `$SPARKHOME/bin/spark-submit assignment.py`.

#### Spark and Java

All files for implementing this project in Java are located in the `java` directory. You will write your code for completing each task in `Tasks.java`, which contains a function for each task. Your implementation of fragment-and-replicate join for Task 8 should go in `FragmentAndReplicate.java`. We have also provided a file called `Assignment.java` that will call your implementation of each task and print out the results.

To make it easier to compile your Java code with all of the Spark dependencies, we use a build system called [Maven](https://maven.apache.org/what-is-maven.html). The Maven directory structure has already been set up for you, so all you need to do to compile you code is run `mvn package` from the `java` directory. After you've written your code in `Tasks.java`, you can see the results of running `Assignment.java` by submitting it to the Spark cluster, which is done by running `$SPARKHOME/bin/spark-submit --class "Assignment" target/project7-1.0.jar`.

<<<<<<< HEAD
## Example Spark Application

Below, we provide an example Spark application written in both Python and Java that counts the number of times each word appears in the file `README.md`. Use this example as a guide for how to write your code for this project.

### Wordcount in Python

The wordcount application is implemented by the following command, when input in the Pyspark shell. Use `counts.take(5)` to see the top five results from the output.
=======
#### Word Count Application

The following command (in the pyspark shell) does a word count, i.e., it counts the number of times each word appears in the file `README.md`. Use `counts.take(5)` to see the output.
>>>>>>> e744d4304a422776e3ef60a7090f10851dd0e0a0

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

<<<<<<< HEAD
The `flatMap` function splits each line into words, and the following `map` and `reduceByKey` do the counting. The `lambda` representation is more compact and preferable, especially for small functions, but for large functions, it is better to separate out the definitions.

Instead of using a shell, you can also write your code as a Python file, and submit that to the Spark cluster. The `examples` directory contains a Python file `wordcount.py`, which runs the program in a local mode. To run the program, do: `$SPARKHOME/bin/spark-submit wordcount.py`.

### Wordcount in Java
=======
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
>>>>>>> e744d4304a422776e3ef60a7090f10851dd0e0a0

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

- **Task 1 (4pt)**: This takes as input the playRDD and for each line counts the number of words. It should then filter the RDD by only selecting the lines That are speaking lines. A speaking line is any line in which a character is speaking and it specifically excludes three types of lines: lines with the word `ACT` or `SCENE` in it, lines with `*` in it and lines with `/` in it.  The output will be an RDD where the key is the line, and the value is the number of words in the line. Simplest way to do it is probably a `map` followed by a `filter`.

- **Task 2 (4pt)**: Write just the flatmap function (`task2_flatmap`) that takes in a parsed JSON document (from `prize.json`) and returns the surnames of the Nobel Laureates. In other words, the following command should create an RDD with all the surnames. We will use `json.loads` to parse the JSONs (this is already done). Make sure to look at what it returns so you know how to access the information inside the parsed JSONs (these are basically nested dictionaries). (https://docs.python.org/2/library/json.html)
```
     	task2_result = nobelRDD.map(json.loads).flatMap(task2_flatmap)
```

- **Task 3 (4pt)**: Write a sequence of transformations starting from prizeRDD that returns an PairRDD where the key is the `category` (`physics` etc), and the value is a list of all Nobel Laureates for that category (just their surnames). Make sure the final values are `list`s, and not some other class objects (if you do a `take(5)`, it should print out the lists).

<<<<<<< HEAD
- **Task 4 (4pt)**: This function operates on the `logsRDD`. It takes as input a list of *web resources* and returns an RDD with "hosts" that requested all of those web resources
The web resources will be provided as strings, in the same format that they appear in the logs (e.g., '/facilites/vab.html' and '/images/vab-small.gif').
=======
- **Task 4 (4pt)**: This function operates on the `logsRDD`. It takes as input a list of *web requests* and returns an RDD with "hosts" that fulfilled all of those web requests
The web requests will be provided as strings, in the same format that they appear in the logs (e.g., '/facilites/vab.html' and '/images/vab-small.gif').
The format of the log entries should be self-explanatory, but here are more details if you need: [NASA Logs](http://ita.ee.lbl.gov/html/contrib/NASA-HTTP.html)
Try to minimize the number of RDDs you end up creating.
>>>>>>> e744d4304a422776e3ef60a7090f10851dd0e0a0

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

<<<<<<< HEAD
### Correct Answers
You can use spark-submit to run the `assignment.py` file and see the output of all tasks, but it would be easier to develop with pyspark (by copying the commands over). We will also shortly post iPython instructions.

**correctanswers/correctX** has the results of `taskX`
=======



### Correct Answers
You can use spark-submit to run the `assignment.py` file and see the output of all tasks, but it would be easier to develop with pyspark (by copying the commands over). We will also shortly post iPython instructions.

**correctanswers/correctX** has the results of taskX`
>>>>>>> e744d4304a422776e3ef60a7090f10851dd0e0a0

### Submission

Submit the `tasks.py/Tasks.java` and `fragAndReplicate.py/FragmentAndReplicateJoin.java` files.

<<<<<<< HEAD
## Helpful Resources

The following references may be helpful as you are implementing this project.
* [Hadoop Map-Reduce Tutorial](http://hadoop.apache.org/docs/r1.2.1/mapred_tutorial.html#Source+Code)
* [Spark Programming Guide](https://spark.apache.org/docs/latest/programming-guide.html)
=======
>>>>>>> e744d4304a422776e3ef60a7090f10851dd0e0a0

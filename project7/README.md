# Project 7: Apache Spark

*The assignment is to be done by yourself.*

*Due to the fact that this is the final assignment and your final grades must be submitted within 2 days of the final exam, this assignment has different late policies than the rest of the assignments this semester: It is due May 10, 11:59PM. However, if you miss this deadline, as long as you submit it before the final exam for our class (May 15, 1:30PM), you will only lose 1 point (out of 40) for lateness. If you submit it by 1:30PM on May 16, you will lose 7 points for lateness. After that point, we cannot accept late submissions since we need to grade all submissions and submit your final grade.*

Project 7 focuses on using Apache Spark for doing large-scale data analysis tasks. For this assignment, we will use relatively small datasets and we won't run anything in distributed mode; however Spark can be easily used to run the same programs on much larger datasets over very large clusters of machines.

## Getting Started with Spark

This section is basically a summary of the excellent tutorials that can be found at the [Spark website](http://spark.apache.org).

[Apache Spark](https://spark.apache.org) is a popular cluster computing framework, developed originally at UC Berkeley. It significantly generalizes the two-stage Map-Reduce paradigm originally proposed by Google and popularized by the open-source Hadoop system. Spark is fundamentally based on the abstraction of **resilient distributed datasets (RDDs)**. An RDD is basically a distributed collection of items that can be created in a variety of ways. Spark provides a set of operations to transform one or more RDDs into an output RDD, and analysis tasks are written as chains of these operations.

Spark can be used with the Hadoop ecosystem, including the HDFS file system and the YARN resource manager. 

### Installing Spark

We have provided a Vagrantfile in the `project7` directory. Navigate to the `project7` directory and run `vagrant up` to start the virtual machine, which should have everything you need (except for Spark) to work on this project. Since the Spark distribution is large, we ask you to download it directly from the Spark website.

1. Download the Spark package at http://spark.apache.org/downloads.html. We will use **Version 2.3.0, Pre-built for Hadoop 2.7 or later**.
2. Move the downloaded file to the `project7` directory (so it is available in `/vagrant` on the virtual machine), and uncompress it using: `tar zxvf spark-2.3.0-bin-hadoop2.7.tgz`. This will create a new directory: `spark-2.3.0-bin-hadoop2.7`.
3. Set the `SPARKHOME` environment variable: `echo "export SPARKHOME=/vagrant/spark-2.3.0-bin-hadoop2.7" >> ~/.bashrc`
4. Set the `JAVA_HOME` environment variable: `echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> ~/.bashrc && source ~/.bashrc`
5. Test that Spark has been successfully installed by running: `$SPARKHOME/bin/pyspark`. This should run the Spark Python shell, which is a REPL which you can use for prototyping your Python code (there is not a corresponding Spark shell for Java).

### Writing Spark Code

Spark primarily supports three languages: Scala (Spark is written in Scala), Java, and Python. For this project, you have the option of writing your code in either Python or Java. Feel free to work with whichever language you are most comfortable with, but we have found that Spark Python is somewhat easier to use and faster to get started. You are highly encouraged to read the [Spark Quick Start Guide](http://spark.apache.org/docs/latest/quick-start.html), which has well-written tutorials for working with both languages.

#### Spark and Python

All files for implementing this project in Python are located in the `python` directory. You will write your code for completing each task in `tasks.py`, which contains a function for each task. Your implementation of fragment-and-replicate join for Task 8 should go in `fragAndReplicate.py`. We have also provided a file called `assignment.py` that will call your implementation of each task and print out the results.

You can prototype your Python code using the Spark Python shell, which you can start by running `$SPARKHOME/bin/pyspark`. After you've written your code in `tasks.py`, you can see the results of running `assignment.py` by submitting it to the Spark "cluster" (which is this case is just your machine), which is done by running `$SPARKHOME/bin/spark-submit assignment.py`.

#### Spark and Java

All files for implementing this project in Java are located in the `java` directory. You will write your code for completing each task in `Tasks.java`, which contains a function for each task. Your implementation of fragment-and-replicate join for Task 8 should go in `FragmentAndReplicate.java`. We have also provided a file called `Assignment.java` that will call your implementation of each task and print out the results.

To make it easier to compile your Java code with all of the Spark dependencies, we use a build system called [Maven](https://maven.apache.org/what-is-maven.html). The Maven directory structure has already been set up for you, so all you need to do to compile you code is run `mvn package` from the `java` directory. After you've written your code in `Tasks.java`, you can see the results of running `Assignment.java` by submitting it to the Spark cluster, which is done by running `$SPARKHOME/bin/spark-submit --class "Assignment" --jars ~/.m2/repository/org/json/json/20180130/json-20180130.jar target/project7-1.0.jar`.

## Example Spark Application

Below, we provide an example Spark application written in both Python and Java that counts the number of times each word appears in the file `README.md`. You can use this example as a guide for how to write your code for this project.

### Wordcount in Python

The wordcount application is implemented by the following command, when input in the Pyspark shell. Use `counts.take(5)` to see the top five results from the output.

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

The `flatMap` function splits each line into words, and the following `map` and `reduceByKey` do the counting. The `lambda` representation is more compact and preferable, especially for small functions, but for large functions, it is better to separate out the definitions.

Instead of using a shell, you can also write your code as a Python file, and submit that to the Spark cluster. The `examples` directory contains a Python file `wordcount.py`, which runs the program in a local mode. To run the program, do: `$SPARKHOME/bin/spark-submit wordcount.py`.

### Wordcount in Java

The corresponding Java code can be found in the file `examples/src/main/java/Wordcount.java`. The semantics of the Java version are the exact same as the Python version, but the syntax is much different. To compile this example, navigate to the `examples` directory and run `mvn package`, which generates a `.jar` file called `wordcount-1.0.jar`. You can then run the program by submitting this jar file to the Spark cluster: `$SPARKHOME/bin/spark-submit --class "Wordcount" target/wordcount-1.0.jar`.

## Assignment Details

We have provided a Python file `assignment.py` and a Java file `Assignment.java` that initializes the folllowing RDDs:
* An RDD consisting of lines from a Shakespeare play (`play.txt`)
* An RDD consisting of lines from a log file (`NASA_logs_sample.txt`)
* An RDD consisting of 2-tuples indicating user-product ratings from Amazon Dataset (`amazon-ratings.txt`)
* An RDD consisting of 3-tuples representing the flewon table from `project1` (`flewon.csv`)
* An RDD consisting of JSON documents pertaining to all the Noble Laureates over last few years (`prize.json`)

Your tasks are to fill out the eight functions that are defined in the `tasks.py` or `Tasks.java` file. The main point of this assignment is Task 8, where you'll be implementing parallel database query operators using Spark -- Task 8 should take the majority of your time for this assignment. The amount of code that you write for the other tasks should typically be small (several can be implemented in one line). The goal of the other tasks is to introduce you to using different Spark primitives, a subset of which will be helpful for Task 8.

See the instructions in the section "Writing Spark Code" for compiling and running the code you write for these tasks.

Note some of the tasks ask you to return a "Pair RDD". A Pair RDD is an RDD with the form (K, V) where K is a key and V is a value. Pair RDD's have additional functions available to them such as `reduceByKey`. For more information on Pair RDD's see [here](https://www.safaribooksonline.com/library/view/learning-spark/9781449359034/ch04.html).

- **Task 1 (2pt)**: Write a function to count the number of words in each speaking line in the Shakespeare play RDD `play.txt`. A "speaking line" is a line in which a character is speaking -- it is any line that does not begin with "ACT", "SCENE", "*" or "/". The output will be an RDD where the key is the speaking line and the value is the number of words in the line. You may assume that splitting the line by the space character will correctly separate the line into words.

- **Task 2 (4pt)**: Write just the flatmap function (Python: `task2_flatmap`, Java: `task2`) that takes in a parsed JSON document from `prize.json` and returns the number of words in each of the motivations. In other words, the code shown below should create an RDD with all the word counts of the motivations. We will use Python `json.loads` function and Java `org.json` library to parse the JSON objects (this is already done). Make sure to consult the documentation ([Python](https://docs.python.org/2/library/json.html), [Java](https://stleary.github.io/JSON-java/)) so you know how to access the information inside the parsed JSON objects. The resultant RDD should be a list of word counts for every motivation, ie if there are 10 motivations with 12 words in them there should be 10 12's in this list.
    * Python: `task2_result = nobelRDD.map(json.loads).flatMap(task2_flatmap)`
    * Java: `JavaRDD<Integer> resultTask2 = nobelRDD.map(line -> new JSONObject(line)).flatMap(json -> Tasks.task2(json));`

- **Task 3 (4pt)**: Write a sequence of transformations starting from nobelRDD that returns an Pair RDD where the key is the `category` (e.g. physics) and the value is a list of the number of words in each motivation. For example the RDD will look like the following [(<category_name>, [number of words in motivation1, number of words in motivation2...])...].  The values in each individual list should be distinct; i.e., for each category, the corresponding list should hold no duplicates. For Python, make sure the final values are `list`s, and not some other class objects (if you do a `take(5)`, it should print out the first five lists; use `collect()` to see the full results). For Java, see the method signature for the return type we are expecting. 

- **Task 4 (2pt)**: This function operates on the `logsRDD`. It takes as input a list of *web requests* and returns an RDD with "hosts" that fulfilled all of those web requests. The web requests will be provided as strings, in the same format that they appear in the logs (e.g., '/facilites/vab.html' and '/images/vab-small.gif'). The format of the log entries should be self-explanatory, but here are more details: [NASA Logs](http://ita.ee.lbl.gov/html/contrib/NASA-HTTP.html). Try to minimize the number of RDDs you end up creating.

- **Task 5 (2pt)**: Complete a function to calculate the degree distribution of user nodes in the Amazon graph (i.e., `amazonBipartiteRDD`). In other words, calculate 
the degree of 
each user node (i.e., number of products each user has rated), and then use a reduceByKey (or aggregateByKey) to find the number of nodes with a given degree. The output 
should be a PairRDD where the key is the degree, and the value is the number of nodes in the graph with that degree.

- **Task 6 (2pt)**: On the `logsRDD`, for two given hosts, use a 'cogroup' to create the following pair RDD: the key of 
the RDD will be a date, and the value will be a 2-tuple, where the first element is a list of all URLs fetched from the first host on that day, and the second element
is the list of all URLs fetched from the second host on that day. Use `filter` to first create two RDDs from the input `logsRDD`.

- **Task 7 (4pt)**: [Bigrams](http://en.wikipedia.org/wiki/Bigram) are simply sequences of two consecutive words. For example, the previous sentence contains the following bigrams: "Bigrams are", "are simply", "simply sequences", "sequences of", etc. Your task is to write a bigram counting application for counting the bigrams in the `motivation`s of the Nobel Prizes (i.e., the reason they were given the Nobel Prize). The return value should be a PairRDD where the key is a bigram, and the value is its count, i.e., in how many times it appeared across all the `motivations`. Don't assume 'motivation' is always present. Punctuation and case should be ignored. Thus "for writing", "For writing" and "for writing." are all the same bigram.

### Task 8 (24pt)

Your goal for task 8 is to implement the fragment-and-replicate join algorithm from Section 18.5.2.2 of the textbook using Spark primitives (**12 points**) and then use it to implement a full SQL query (**12 points**).

#### Part A: Implementing Fragment-and-Replicate Join (12pt)

Recall from lecture that fragment-and-replicate join is a way of joining two relations in a parallel database system by partitioning the tuples of each relation across multiple processors, joining the tuples at each processor, then aggregating the results from all the processors. Since you are running Spark on a single machine, all of the processors will be located on the same machine (your machine). But as long as you create the partitions correctly (see below), Spark could easily parallelize your code across multiple machines if you had them -- each partition can be processed by a separate machine.

In the file `fragAndReplicate.py` (Python) or `FragmentAndReplicateJoin.java` (Java), implement the fragment-and-replicate join algorithm in the function `fragment_and_replicate` (Python) or `fragmentAndReplicateJoin` (Java) using Spark primitives. Your function must return an RDD consisting of four-tuples that is the result of joining the two RDDs provided as arguments. Your function will have the following five parameters:
* `leftRelation`: An RDD containing tuples of the first relation being joined. Each tuple of `leftRelation` is a two-tuple containing a String and a Double value.
* `n`: An integer representing the number of partitions your function should create of `leftRelation`.
* `rightRelation`: An RDD containing tuples of the second relation being joined. Each tuple of `rightRelation` is a two-tuple containing a String and a Double value.
* `m`: An integer representing the number of partitions your function should create of `rightRelation`.
* `joinCondition`: A lambda function containing the join predicate. You must use this function to test if two tuples should be joined together and included in the output of your function.

Your implementation of fragment-and-replicate join should work roughly as follows:
* Partition the left and right relations into *n* and *m* partitions, respectively, using round-robin partitioning.
* For each of the *n* partitions of the left relation, replicate the tuples in the partition *m* times, corresponding to one row in Figure 18.3 of your textbook. Name each replica (e.g., via giving each tuple in that replica the same key name, perhaps (x,y) corressponding to P<sub>x,y</sub> in the book) according to the cell from Figure 18.3 that it belongs. Do the same for the right relation, reversing the role of *n* and *m*. 
* For each cell you created above, you will have a partition of tuples from each relation. Join those partitions using a join algorithm of your choosing (nested loop join would be the easiest). You can assume that all the tuples within each partition will easily fit in memory.
* Aggregate the joined tuples from each cell together into a single relation.
   
You can use any of the Spark primitives listed in the documentation in the [assigned reading for April 30](https://spark.apache.org/docs/latest/rdd-programming-guide.html) except `join` to complete this task (that join primitive won’t help you anyway, since it is only an equi-join). In addition, you can use the following primitive which may be helpful in the initial partitioning step:
* zipWithIndex(): Assigns each tuple in the relation a unique index starting at zero.

**Grading:** We will grade you implementation by calling your `fragmentAndReplicateJoin` function with multiple different values for `n`, `m`, and `joinCondition`. In addition, we will be grading the intermediate results of your implementation. Therefore, please print to standard output the following intermediate results that your implementation creates (using the standard string representation is fine, see `assignment.py` or `Assignment.java` for examples):
* The tuples in each of the `n` partitions of `leftRelation` that were created.
* The tuples in each of the `m` partitions of `rightRelation` that were created.
* The result of assigning tuples from each patition of each relation to cells.
* The result of joining the tuples in each cell.

#### Part B: Implementing a SQL Query with Spark (12pt)

After you’ve implemented fragment-and-replicate join, you will put it to use by implementing a SQL query using Spark primitives. Since the fragment-and-replicate join algorithm is particularly useful for inequality-based joins, we will revisit Query 10 from Project 1, which you wrote earlier this semester using the flights database. Please use the following solution to Query 10:

```sql
WITH flight_customers_per_day AS (
    SELECT flightid, flightdate, count(customerid) AS onboard_cnt
    FROM flewon
    GROUP BY flightid, flightdate
), flight_avg_customers(flightid, avg_customer) AS (
    SELECT flightid, sum(onboard_cnt) / (SELECT max(flightdate) - min(flightdate) + 1.0 FROM flewon)
    FROM flight_customers_per_day
    GROUP BY flightid
)
    (SELECT t1.flightid, count(*)+1 as rank
    FROM flight_avg_customers t1, flight_avg_customers t2
    WHERE t2.avg_customer > t1.avg_customer
    GROUP BY t1.flightid, t1.avg_customer
    HAVING count(*) < 20)
    UNION
    (SELECT flightid, 1
    FROM flight_avg_customers
    WHERE avg_customer = (SELECT max(avg_customer) FROM flight_avg_customers))
    ORDER BY rank, flightid;
```

Your goal is to implement the above query using the Spark primitives and the fragment-and-replicate-join you wrote and placed in either `fragAndReplicate.py` or `FragmentAndReplicateJoin.java`. If you want to make modifications to the above query, that's fine. The only restriction is that: (1) Your query must return the same results and (2) the 
```sql
FROM flight_avg_customers t1, flight_avg_customers t2 
WHERE t2.avg_customer > t1.avg_customer
```
part of the above query must remain and be implemented using your fragment-and-replicate join.

## Submission

Submit the following two files under the Project 7 assignment on ELMS:
* **Python:** `tasks.py` and `fragAndReplicate.py`
* **Java:** `Tasks.java` and `FragmentAndReplicateJoin.java`

## Helpful Resources

The following references may be helpful as you are implementing this project.
* [Hadoop Map-Reduce Tutorial](http://hadoop.apache.org/docs/r1.2.1/mapred_tutorial.html#Source+Code)
* [Spark Programming Guide](https://spark.apache.org/docs/latest/programming-guide.html)
* [Learning Spark](https://www.safaribooksonline.com/library/view/learning-spark/9781449359034/)
* [Spark Quick-Start Guide](http://spark.apache.org/docs/latest/quick-start.html)
* [Spark Examples](https://github.com/holdenk/learning-spark-examples)
* [Spark Java Documentation](https://spark.apache.org/docs/latest/api/java/index.html)

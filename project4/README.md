## Project 4: Query Processing, CMSC424, Spring 2018

*The assignment is to be done by yourself.*

Please do a `git pull` to download the directory `project4`. The files are:

1. README.md: This file
1. small.sql: SQL script for populating `flights` database.
1. queries.py: The file where to enter your answer for Q1; this file has to be submitted
1. answers.py: The answers to query Q1 and Q3.
1. answers.txt: The answers to queries Q2 and Q3.
1. SQLTesting.py: File to be used for testing your SQL submission -- see below 
1. table4storedproc.sql: SQL script for populating `stpc` database.
1. trigger-database.sql: SQL script for setting up the `flightsales` database.
1. trigger-test.py: Python script for testing the trigger.
1. Vagrantfile: Vagrantfile that creates the required databases and populates some of them.

### Getting started
Start the VM with `vagrant up` in the `project4/` directory. The database `q2db` should already be set up.

### Submission Instructions
- Submit your answers to Q1 in `queries.py`
- Submit your answers to Q2, Q3 in `answers.txt`
- Submit your answer to Q4 in `trigger.sql`

<br />


**Q4 (10pt)**. [Sort Merge Join] In this problem, you will implement the sort merge join algorithm, more specifically the merge algorithm. You will be joining the following two tables, 
``` 
CompanyLocation (cId, cLoc)
CompanyName (id, cId, cName)
```
and the resulting table will be
```
ResultTable (cId, cLoc, id, cLoc, cName)
```
The two tables will be joined on `cId` which is the primary key in `CompanyLocation` and foreign key in `CompanyName`. Note that for sort merge join, we need the two tables to be sorted on the join keys. We have already sorted the tables on the join keys for you. Now let us see an example below:

| cId | cLoc |  
|:---:|:---:| 
| 1 | NY | 
| 2 | CA | 
| 3 | OR |
| 4 | WA | 

`CompanyLocation`

| id | cId | cName |  
|:---:|:---:|:---:|
| 1 | 1 | IBM |
| 2 | 2 | Google |
| 4 | 2 | Facebook |
| 3 | 4 | Microsoft |

`CompanyName`

| cId | cLoc | id | cId | cName |  
|:---:|:---:|:---:|:---:|:---:|
| 1 | NY | 1 | 1 | IBM |
| 2 | CA | 2 | 2 | Google |
| 2 | CA | 4 | 2 | Facebook |
| 4 | WA | 3 | 4 | Microsoft |

`ResultTable`

### Coding Details:
We have provided a package `queryproc` with the following java classes:
1. **JoinOperators.java**: Your join algorithm must be written within the SortMergeJoin method.
1. **QueryProcessing.java**: Contains the main method with some helper methods for displaying the tables and testing the result.
1. **Relation.java**: The relation class with some helper methods.
1. **TupleType1.java**: Class defining the attributes for table `CompanyLoc` with helper methods.
1. **TupleType2.java**: Class defining the attributes for table `CompanyName` with helper methods.
1. **TupleType3.java**: Class defining the attributes for table `ResultTable` with helper methods.

### Coding Restrictions:
1. You are only allowed to **add/modify** your **own** code to the following: (i) **JoinOperators.java**: Put all your code within the SortMergeJoin method, (ii) **Relation.java**: If you think you require additional helper methods in Relation.java, you may include them. 
1. Please do not modify any existing code in any of the java files.
1. Please remember to maintain the same order of attributes as shown in the example above when inserting a tuple in the table `ResultTable`. More instructions provided in JoinOperators.java.
1. You may write your code with/without the help of an IDE of your choice (We encourage you to write/debug your code in an IDE). However your final code should compile and run with the following commands within the VM.
```
javac queryproc/*.java
java queryproc/QueryProcessing
```
### What to turn in:
Please submit JoinOperators.java and Relation.java.

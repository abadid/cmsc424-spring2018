## Project 4: Query Processing, CMSC424, Spring 2018

*The assignment is to be done by yourself.*

Please do a `git pull` to download the directory `project4`. The files are:

### Getting started
Start the VM with `vagrant up` in the `project4/` directory. The database `q2db` should already be set up.

**Q2 (10pt)**. [Query Debugging] For this problem you are required to switch to `q2db` database (`psql q2db`) where we have already populated the `customers` table with a large dataset. The `customers` table has the same schema as the one that we had used in Project 1. The following query counts the number of customer pairs whose year of birth differ by a year.

```
select count(\*)
from customers a, customers b
where extract(year from b.birthdate) - extract(year from a.birthdate) = 1 
and extract(year from a.birthdate) < extract(year from b.birthdate);
```
This query takes around 10 seconds to execute in the VM. Could you rewrite the query to make it execute more efficiently.

[**Note**: In general, query optimizers does not require the users to rewrite the most efficient query. For a given query, the query optimizer enumerates all possible query plans and chooses the most efficient plan based on some heuristic. Surprisingly in this case, the query optimizer of Postgres does not do a good job!] 

### What to turn in:
Submit your efficient version of the query above in the `queries4.py` file. 

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
1. You are only allowed to **add/modify** your **own** code to the following: (i) **JoinOperators.java**: Put all your code within the SortMergeJoin method, (ii) **Relation.java**: If you think you need additional variables or helper methods in Relation.java, you may include them. You may also add additional code in the constructor if required, but you are not allowed to modify the constructor input parameters. 
1. Please do not modify any existing code in any of the java files.
1. Please remember to maintain the same order of attributes as shown in the example above when inserting a tuple in the table `ResultTable`. More instructions provided in JoinOperators.java.
1. You may write your code with/without the help of an IDE of your choice (We encourage you to write/debug your code in an IDE). However your final code should compile and run with the following commands within the VM.
```
javac queryproc/*.java
java queryproc/QueryProcessing
```
### What to turn in:
Please submit JoinOperators.java and Relation.java.

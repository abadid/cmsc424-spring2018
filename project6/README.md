## Project 6: Query Processing, CMSC424, Spring 2018

*The assignment is to be done by yourself.*

Please do a `git pull` to download the directory `project6`.

### Getting started
Start the VM with `vagrant up` in the `project6/` directory.

**Q1 (5pt)**. [Query Plan] If you add the keyword EXPLAIN at the beginning of a query, PostgreSQL will display the execution plan for that query. This plan includes how many tuples are estimated by the query optimizer to be generated after each operation in the query plan. Furthermore, if you add the keyword ANALYZE after EXPLAIN at the beginning of a query, then in addition to getting the execution plan, the query also gets executed and also shows the actual number of tuples that were generated when the query plan was executed.

Below is a query that was sent to PostgreSQL that prints the customers who have taken a flight more than once from a source or destination which is the hub of his frequentflyer airline. 

```
explain analyze select c.customerid, count(*) as hub_flight_freq
from customers c, flewon fl, flights f, airlines a 
where c.customerid = fl.customerid 
and fl.flightid = f.flightid 
and c.frequentflieron = a.airlineid
and (a.hub = f.source or a.hub = f.dest)
group by c.customerid having count(*) > 1
order by count(*) desc, c.customerid;
```

In order to view the query plan and its execution on the query, we ran `explain analyze` on the query as shown above. The following was the query plan generated for the above query.


```
QUERY PLAN                                                                    
--------------------------------------------------------------------------------------------------------------------------------------------------
 Sort  (cost=72.55..72.56 rows=8 width=11) (actual time=0.926..0.928 rows=60 loops=1)
   Sort Key: (count(*)), c.customerid
   Sort Method: quicksort  Memory: 29kB
   ->  HashAggregate  (cost=72.33..72.42 rows=8 width=11) (actual time=0.801..0.815 rows=60 loops=1)
         Filter: (count(*) > 1)
         Rows Removed by Filter: 31
         ->  Hash Join  (cost=32.27..72.27 rows=8 width=11) (actual time=0.167..0.722 rows=198 loops=1)
               Hash Cond: (fl.flightid = f.flightid)
               Join Filter: ((a.hub = f.source) OR (a.hub = f.dest))
               Rows Removed by Join Filter: 602
               ->  Hash Join  (cost=29.46..54.47 rows=800 width=34) (actual time=0.116..0.409 rows=800 loops=1)
                     Hash Cond: (fl.customerid = c.customerid)
                     ->  Seq Scan on flewon fl  (cost=0.00..14.00 rows=800 width=18) (actual time=0.004..0.066 rows=800 loops=1)
                     ->  Hash  (cost=27.86..27.86 rows=128 width=27) (actual time=0.101..0.101 rows=128 loops=1)
                           Buckets: 1024  Batches: 1  Memory Usage: 6kB
                           ->  Hash Join  (cost=22.82..27.86 rows=128 width=27) (actual time=0.021..0.070 rows=128 loops=1)
                                 Hash Cond: (c.frequentflieron = a.airlineid)
                                 ->  Seq Scan on customers c  (cost=0.00..3.28 rows=128 width=14) (actual time=0.002..0.012 rows=128 loops=1)
                                 ->  Hash  (cost=15.70..15.70 rows=570 width=28) (actual time=0.004..0.004 rows=4 loops=1)
                                       Buckets: 1024  Batches: 1  Memory Usage: 1kB
                                       ->  Seq Scan on airlines a  (cost=0.00..15.70 rows=570 width=28) (actual time=0.003..0.003 rows=4 loops=1)
               ->  Hash  (cost=1.80..1.80 rows=80 width=15) (actual time=0.035..0.035 rows=80 loops=1)
                     Buckets: 1024  Batches: 1  Memory Usage: 4kB
                     ->  Seq Scan on flights f  (cost=0.00..1.80 rows=80 width=15) (actual time=0.005..0.016 rows=80 loops=1)
 Total runtime: 1.030 ms
```

You do not need to run the query (you can rely on the output we got above when we ran the query). The output is at first a little overwhelming to understand. However, Postgres' documentation is actually pretty good at explaining how to read this output: https://www.postgresql.org/docs/9.5/static/using-explain.html. In addition, https://robots.thoughtbot.com/reading-an-explain-analyze-query-plan also overviews how to understand the output of Postgres EXPLAIN ANALYZE. Try to read these overviews and then afterwards, make an attempt to understand the query plan shown above. You don't have to understand every detail, but you should get a general sense of of the main flow of operators and cost estimates --- at least enough to understand the questions below.

#### Answer the following questions on ELMS

1. True or False: The first operator in this query plan is a sort. The output of the sort is then sent to an operator called "HashAggregate". 
2. How many rows were estimated to be returned by the query?
3. How many rows were actually returned by the query?
4. Multiple choice (only one correct): The join operations are performed in the following order (earliest to last): 
   1. fl.flightid=f.flightid, fl.customerid = c.customerid, c.frequentflieron = a.airlineid. 
   2. c.frequentflieron = a.airlineid, fl.customerid = c.customerid, fl.flightid=f.flightid.
   3. fl.customerid = c.customerid, fl.flightid=f.flightid, c.frequentflieron = a.airlineid.
   4. c.frequentflieron = a.airlineid, fl.flightid=f.flightid, fl.customerid = c.customerid.
5. True or false: At least one table is first accessed with some method other than a sequential scan
6. True or false: Each join has exactly two (not more and not less) operators that feed data into it. 
7. Multiple choice (only one correct): On which of the following join conditions does the query optimizer perform poorly in terms of overestimating or underestimating the size of the output?
   1. fl.flightid=f.flightid
   2. fl.customerid = c.customerid
   3. c.frequentflieron = a.airlineid 

**Q2 (4pt)**. [Query Debugging] For this problem, you are required to switch to `q2db` database (`psql q2db`) where we have already populated the `customers` table with a relatively large dataset. The `customers` table has the same schema as the one that we had used in Project 1. The following query counts the number of customer pairs whose year of birth differ by a year.

```
with custbyear as (
select customerid, name, extract(year from birthdate) as birthyear, frequentflieron
from customers)
select count(*)
from custbyear a, custbyear b
where b.birthyear - a.birthyear = 1;
```
This query takes around 3.5 seconds to execute in the VM. Could you rewrite the query to make it execute approximately 10X faster.

[**Hint**: You might want to use EXPLAIN to view the query plan of the query.]

The most significant reason why the query above is inefficient is because of which of the following? [choose the best answer]:

1. The query involves a self join.
2. The choice of the join algorithm by Postgres.
3. The lack of index usage in this query plan.
4. The query involves performing arithmetic operations which are expensive.


[**Note**: In general, query optimizers does not require users to write the most efficient query. For a given query, the query optimizer enumerates all possible query plans and chooses the most efficient plan based on some heuristic. Surprisingly in this case, the query optimizer of Postgres does not do a good job!] 

#### What to turn in:
1. Submit your efficient version of the query above in the `p6q2.py` file.
1. Answer the multiple choice question in ELMS.


**Q3 (4pt)**. [Sort Merge Join] In this problem, you will implement a merge join algorithm for two tables that have already been sorted. The schema of the two tables to be joined and the resulting table are as follows:
``` 
Locations (id, state, region)
Companies (id, locid, name)
ResultRelation (id, state, region, id, locid, name)
```
The two tables (`Locations` and `Companies`) will be joined using the `id` attribute from the `Locations` table (`id` is the primary key for that table) and  the `locid` attribute from the `Companies` table (which is a foreign key into the Locations table). You can assume that both input tables will be sorted on these join key attributes. Now let us see an example below:


`Locations`

| id | state | region |
|:---:|:---:|:---:|
| 1 | NY | NE |
| 2 | CA | W |
| 3 | OR | W |
| 4 | WA | W |


`Companies`

| id | locid | name |
|:---:|:---:|:---:|
| 1 | 1 | IBM |
| 2 | 2 | Google |
| 4 | 2 | Facebook |
| 3 | 4 | Microsoft |


`ResultRelation`

| id | state | region | id | locid | name |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | NY | NE | 1 | 1 | IBM |
| 2 | CA | W | 2 | 2 | Google |
| 2 | CA | W | 4 | 2 | Facebook |
| 4 | WA | W | 3 | 4 | Microsoft |

#### Coding Details:
We have provided a package `queryproc` with the following java classes:
1. **JoinOperators.java**: Your join algorithm must be written within the `MergeJoinOnIntegerAttributes` method. This method takes in two relations (or tables) as input (`leftRelation` and `rightRelation`) and the indexes of the attributes (from `leftRelation` and `rightRelation`, respectively) on which the relations are to be joined and returns the `resultRelation`.
1. **QueryProcessing.java**: Contains the main method with some helper methods for displaying the tables and testing the result.
1. **Relation.java**: The relation class with some helper methods.
1. **TupleType1.java**: Class defining the attributes for table `Locations` with helper methods.
1. **TupleType2.java**: Class defining the attributes for table `Companies` with helper methods.
1. **TupleType3.java**: Class defining the attributes for table `ResultRelation` with helper methods.

You may write your code in whatever environment you are most comfortable with. However your final code should compile and run with the following commands within the VM in the project6 directory.

```
javac queryproc/*.java
java queryproc/QueryProcessing
```

**Assumptions**: Please note the following assumptions in regards to testing your code:
1. The join key in the `leftRelation` will always be the primary key of the `leftRelation`.
1. The join key in the `rightRelation` will always refer to the primary key of the `leftRelation`, i.e. it is a foreign key.
1. There are not any `NULL` values in the tables provided.
1. The input tables can be assumed to have at least one tuple.
1. The input tables will be sorted on the join keys.

#### Coding Restrictions:
1. You are only allowed to **add/modify** your **own** code within the `MergeJoinOnIntegerAttributes` method in **JoinOperators.java**. For the remaining java files, please do not modify any existing code in any of those files.
1. Please remember to maintain the same order of attributes as shown in the example above when inserting a tuple in the table `ResultRelation`. More instructions provided in `JoinOperators.java`.

#### What to turn in:
Please submit `JoinOperators.java`.

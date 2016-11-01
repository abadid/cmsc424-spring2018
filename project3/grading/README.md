### Grading Data

`testing-[123].json` contain the JSON used for testing.

You should copy your JSONProcessing.java file into this directory, and run `python testing-java.py`. If the results were as expected, full points were awarded (unless an exception was raised for the last part).

You should run: `python testing-trigger-grading.py <your-trigger-sql-file>` for testing the trigger. The code is pretty self-explanatory. Note that: this assumes the existence of a database: `flightstrigger`, and you should create one first using: `createdb flightstrigger`. If you are going to run it multiple times, you need to `dropdb flightstrigger` before every run (no easy way to clear all the functions and triggers otherwise).

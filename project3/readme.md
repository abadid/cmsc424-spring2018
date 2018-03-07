# **Project 3: Matchapp (JDBC Manipulation)**

## **Introduction**

This project should help you gain the skills involved in creating a fully functional web application that interfaces with a database system using JDBC. We will be creating an application that matches users with other users with similar interests and backgrounds. We will be using Java and Tomcat to make this happen in conjunction with a variation of HTML (JSP) to create webpages. You will be a "Full-stack developer" in this project since you will be dealing with all three tiers of a 3-tier architecture: the front-end (presentation tier), the back-end (logic tier), and the database system components of the application!

## **Relevant Project Files**

To begin this project you will have to pull the project 3 folder from our git repo. Below, we give an overview of the important files that you should know about; all of the other files that are included in the code that you pull are just there to make sure that the application works properly:

* **build.sh**: you should run "sudo ./build.sh" in order for your project files to build. This will compile all the necessary files for the application. Make sure you run build as the root user **(sudo)** to have it copy the war file to the tomcat directory properly.

* **src/**

    * ***.jsp**: These are the Java Server Pages. JSP allows Java code to be interleaved with static web markup content (HTML in our case), with the resulting page being compiled and executed on the server to deliver a complete HTML page. Basically Java is being used to dynamically create HTML pages. A good overview/tutorial on JSP can be found at: [https://www.tutorialspoint.com/jsp/jsp_overview.htm](https://www.tutorialspoint.com/jsp/jsp_overview.htm) (however, you can skip the parts of the tutorial on how to set up the enviornment, since we’ve already done that for you). It is a good idea to check out the other jsp files we are providing you, so that you can get a sense of how each page of the app is generated. **(Front-end Component)**

    * **com/match/**

        * **model/**

            * **Match.java:** You must complete this file to interface with the match table in the matchapp database. **(Back-end + DB Component)**

            * **Person.java:** This Java file interfaces with the person table in the matchapp database. We provide basic constructors for a person object but there are several functions missing that you must complete. **(Back-end + DB Component)**

        * **web/**

            * **.java:** These are servlet files that deal with porting over information computed by the **model** files. They help bridge the gap between the back-end and the frontend. **(Back-end + Front-end Components)**

## **Getting Started**

Start the VM with **"vagrant up"**. You will use the database “matchapp” which we create for you. For this database you must create 2 tables as well as a user role. You will see the technical details in the sections below. We will be using tomcat to run our server locally and eventually through Amazon Web Services (aka "the cloud"). Here are some useful commands to run (run as super user, i.e. “sudo” or “sudo su”):

* systemctl start tomcat: Starts your server

* systemctl status tomcat: Checks status of your server

* systemctl stop tomcat: Stops your server

* ./build.sh:  Builds all necessary files and copies your **ROOT.war** file to the right directory

* tail /opt/tomcat/logs/catalina.out: Checks log file of tomcat server

* tail /opt/tomcat/logs/localhost.(current-date): Checks log file of localhost

You won't be able to debug this web application with print statements like you would for other programs. With Tomcat, you can print values and errors to the log and view the output they produce in the log file. We have set up the log and have included some uses of the logger in the getConnection method but you may want to add your own statements that log information in the methods you write to debug what your program is doing. [Here](https://logging.apache.org/log4j/2.x/manual/messages.html) is a useful link to using the log with examples. Basically, you can add logger.info and logger.trace statements to print values when your code runs that you can then view the output of in the catalina.out file. If your application isn't behaving as expected or is crashing, add logging statements to your code and view the log to figure out the issue.

Navigate to the page localhost:8080 in your browser (you can use whatever browser you usually use on your computer) to see the website. Take some time to view the different pages and examine the format of the website. Here is which files correspond to which links on the website:

404.jsp - going to any url that is not set up to be a page on the website  
add.jsp - The Register link  
default.jsp - The home page  
feedback.jsp - Blank page that you will have to create in Part 6  
generate.jsp - The Find Matches page  
invalid_input.jsp - Page shown if the user enters invalid input in the Register page  
matches.jsp - The View Matches link  
people.jsp - The People link  

## **Schema + User**

 You will have to create 2 tables (person and match) as you have seen in project 0 and 1. You can create your tables however you wish (directly in psql or with a .sql file). We will be testing your code on tables that we have already created that match the schema described below. The schema is as follows (you must use intuition as well as the **person.sql** file we use to insert into your tables to infer the types): Note you can use either varchars or chars to represent what we refer to as a string in the schema. 

* **person**

    * **id:** This is the primary key of the table, to represent a unique person. This should should be of type "serial" which we have not seen yet this semester; this data type auto generates a next unique id to assign to a new person in the table.

    * **first_name:** A string less than or equal to 12 characters long.

    * **last_name:** A string less than or equal to 18 characters long.

    * **age:** A number greater than or equal to 18.

    * **major:** A string less than or equal to 20 characters long.

    * **gender:** This must be an integer type that is not null. Below, we will ask you to decide how to map real-world genders that the user sees in the app interface to integer values that are stored in the database. But as far the database is concerned, each gender option is stored as an integer.

    * **seeking_relationship_type:** Must be an integer between 1 and 3.

    * **seeking_gender:** You can decide how to represent this field, which corresponds to the gender that a person is seeking for the type of relationship set in the seeking_relationship_type field. But you must include a constraint that this column is not null.

    * **language:** A string 3 characters or less (e.g. English could be represented as ENG).

    * **county:** A string less than or equal to 20 characters long.

    * **approval_rating:** A floating point number with a precision of 2 digits after the decimal. All users start with a rating of 1.0, where the minimum is 0 and max is 9.99. But this value can go up or down depending on whether they treat the other users on the app with politeness, kindness, and respect. 

* **match**

    * **id1:** **(Primary Key)**  An integer that must reference the person table's id attribute. This means that id must appear in the person table in order to appear in this table as id1. id1 is the field for the person who goes to the Find Matches page and generates matches for his or herself. 

    * **id2:** **(Primary Key)** An integer that must also reference the person table's id attribute. This means that id2 must appear in the person table in order to appear in this table as id2. id2 is the field for the person who gets assigned as a match to the person in id1.

    * **date_of_match:** Must be a date datatype

    * **Rating:** A decimal value.


You will also have to add one more attribute to the person table with any type of your choice. Once you create your tables, you can run /i person.sql in matchapp in psql to populate the person database with people. You will also have to create a user with name **"matchmaker"** and password **“kingofthenorth”** and you must grant all permissions to that user to access your database and tables as it will be the one doing the database manipulation. Below is the command to do this (which you can run in psql or add to a .sql file):

create user matchmaker with password 'kingofthenorth';
grant all on (insert table name) to matchmaker;

## **Part 1: ER diagram (5 points)** 
Please draw an ER diagram that could have been used to generate this schema specified above such that it contains at least one recursive relationship set. Please answer the following questions about your ER diagram:

How many entity sets were included in your ER diagram for this appliciation? (You can count weak entity sets as entity sets for the purpose of this question.) Answer must be an integer.

Does the match table correspond to an entity set, a weak entity set, or a relationship set? Answer must be one of "entity set", "weak entity set", or "relationship set"

How many attributes were included in the match [entity set or relationship set depending on your answer above] in the ER diagram? Answer must be an integer.

True or False: There are no one-to-one, many-to-one, or one-to-many mapping cardinalities in the ER diagram. In other words you didn't draw any directed edges in your diagram. Answer either "true" or "false"

Did you draw any double-lines in your ER model corresponding to a total participation constraint? Answer either "yes" or "no"

Please answer the questions in a text file called part1.txt with one line per answer. For example, the part1.txt file would contain:

5  
relationship set  
5  
false  
yes

if you thought the answers to the five questions are 5, relationship set, 5, false, and yes respectively. Please note that the grader will not be case sensitive, but it will be spelling sensitive --- so please be careful to spell your answers to the second, fourth, and fifth questions correctly. Use the exact format shown after each question. Note the possible answers for 2 are as follows: "entity set", "weak entity set", and "relationship set". If you have an answer that is not spelled exactly like one of those three it will be marked wrong. 

Please submit your ER diagram as a .png, .jpg, or .pdf file. Feel free to draw it by hand, take a picture of what you drew, and submit it that way. It will not be graded seperately, but might be looked at to give you partial credit if you got several of the questions above incorrect. 

## **Part 2: Person.java: Back-end + DB (14 points)**

You will need to complete the following methods in the Person.java model file that interfaces with the person table in the matchapp database. We have already completed a few of these methods, including the constructors as well as functions that interface with your database remotely and locally. You have to complete:

* **getPeople():** Get a list of all the people in the database.

* **getPerson(id):** Get a specific person given a value for the id attribute.

* **getPersonSearch(query):** Return people in the Person table that have an attribute that have a substring match with the query

* **addPerson(*all person attributes*):** Add a person with the specified values for all attributes of that person.

* **getMatchedPeople(id):** Get the top 5 matches for a specific person via id.

The Person.java file has comments above each method with more details about what each method should do. We will be testing each of these methods individually to ensure that they produce the output as specified by the comments above each method on a database with different people and matches that we make. The data we test it on will be exactly the same as the form we have given to you in person.sql --- only the actual values will be different.  

## **Part 3: Match.java: Back-end + DB (10 points)**

A match in this application represents a match between 2 entities(people) in the Person table. Matches are only generated when a user
goes to the Find Matches page and generates new matches for his or herself. This means that if person A goes to the Find Matches page and gets
matched with person B, a match should be written to the table with id1 as A and id2 as B only. Person B should still have 0 matches until that person
goes to the Find Matches page and generates matches, at which point they could potentially match with A and be written to the matches database as a seperate tuple. 
You will have to complete most of this file. Here are some general things you will probably need to write:

* Constructors for the Match object to be written to the database.

* Functions to make data retrieval easy.

You will be **required** to write these functions:

* **getMatchesFor(id):** Get the matches from the match table that include the person with the specified value for the id attribute. Note that all matches this should return should be where id matches the id1 field in the match table only. 

* **At least these fields and getter methods:**

    * **getMatchedID():** Get the id of the person that was matched to the user who called getMatchesFor. In other words, the id of the person 
    who did not generate the match, and who was assigned as a match to the person who did call getMatchesFor. (which should be the id2 field in the schema)

    * **getDate():** Get the date of match in a string form. This should follow string form of an java.sql.date object, which looks like yyyy-mm-dd. You can view more at the documentation here https://docs.oracle.com/javase/7/docs/api/java/sql/Date.html

    * **getRating():** Get the rating (or score) of a match.

Again, see the comments in the file for more details about what these methods should do. They will be tested in the same kind of fashion as described for part 3. In addition, once you have completed this project and the web application is fully functional, the "view matches" page should properly display the matches. For example, if person with id 1 is matched with id 2, 3, and 4, then if the id of 1 is submitted to the "view matches" page, the entries for id 2, 3, and 4 should be displayed.

## **Part 4: Add.jsp: Front-end (3 points)**

As of now, there are not that many attributes of a person that are useful in matching people with each other. The next step is to add an additional attribute to a person that will be useful in your match algrotihm. You will need to add this field in all relevant parts of the system --- the database table, the back-end, and also here --- in the front-end. 

Please create some way for a user to specify the value of this field on the "add a person" page. You can model it just like any of the other input fields already there on the page. See the add.jsp file and its comments for exactly where to modify and insert the form field. Whatever field you decide to add, make sure you do not set a not null constraint on the person table for the field. You can see more about html form elements online here: [https://www.w3schools.com/html/html_form_elements.asp](https://www.w3schools.com/html/html_form_elements.asp)

Furthermore, you can modify the fields where the user can enter a gender and seeking\_gender so that the current menu of options correspond to real-world genders. The mapping of these options to integers for storage in the database is (and should remain) hidden from the end user. We certainly don't want to give end users any kind of impression that one gender has a higher value than another one! You will not be tested in any way on what genders you specify in the dropdown or what values they are mapped to. Feel free to make them as realistic or unrealistic as you wish.

## **Part 5: AddPerson.java: Back-end + Front-end (3 points)**

Now that you have successfully finished the majority of the back-end (logic tier) components, you will now have to hook up the back-end with the front-end components. This process will be done via the Java files in the **web** directory. We will only be editing the AddPerson.java file and this process is trivial (most of what you need is already there). All you have to do is make sure you alter the file to accept a new field that you added to the person table, and then add it to the addPerson method call at the end of the file. See the comments in the file for the specific things to do.

## **Part 6: Adding a Page (10 points)**

Finally, we want you to put all of these steps together and add a new page to MatchMaker. The purpose of this page is to let users give feedback on their matches which will increase or decrease the approval rating of the person that they were matched with. Follow these steps to create and add the page to your website:

Note: We are giving you some free range here so we will not be grading you strictly on exactly how your html page looks. We will only be testing to see that your page is added and visible on the website and that it meets the functional requirements discussed below. The purpose of this part is to give you experience adding a new feature to the website from start to finish.

1. First, go to the given file feedback.jsp. This file will contain the html that we want to display for the page. It is mostly blank right now. You will need to add a form element to display input boxes corresponding to the person’s id who is giving feedback and their match id they are giving feedback for, in addition to a radio button to designate whether they were treated respectfully and politely by their match (independent on whether or not it was a good match). View the comments in the file for more guidance.

2. Now we need to set up an HttpServlet file to display and handle the form data for the jsp file. You want to create a new java file that will extend HttpServlet and contain the void doPost(HttpServletRequest request, HttpServletResponse response) method. This java file should be placed in the com.match.web directory. Look at the AddPerson.java file for a template on how to create this. Within this file, you need to get the parameters you pass from the request (which will be each field in the form submitted by the user in feedback.jsp), make a call to a method in Match.java that you create to check and submit the new data to the database (described in step 3), and send the response back to the feedback.jsp page where the user can enter another piece of feedback information. If you are really confused on how to do this, view the comments in AddPerson.java that explain what each part of it does and model your file just like it, only adapted to the different fields and methods you use.

3. Now we need to add the method in Match to update the approval_rating field in the database appropriately. How much you increment or decrement this field is entirely up to you, but it must be a constant amount (for example, +1 for good and -1 for bad). However, it is required that a user cannot give feedback for someone that they are not matched with. This means the ID of the user giving feedback and the person matched ID must be an entry in the matches table (where userID is id1 and matchedID is id2 only). If this condition is not met or either of the ids is not in the person table at all, do nothing or give an error message (you can decide); otherwise update the approval_rating of the matched person. Note that for this project it is fine if a user gives feedback on one of their matches as many times as they like and each time it affects the other users approval_rating. 

4. The last steps we have to do is connect all of the files we just made and expose them on the website. We need to register our feedback.jsp file as a web page and our HttpServlet file from step 2 as a servlet. To do this, open the web.xml file. Here is a template for what you need to insert: 

```
  <servlet>
    <servlet-name>INSERT NAME</servlet-name> --choose a name for your servlet
    <jsp-file>/feedback.jsp</jsp-file> --the jsp file we made
  </servlet>
  <servlet-mapping>
    <servlet-name>SAME NAME AS ABOVE</servlet-name>
    <url-pattern>/URL</url-pattern> --whatever you want the url to be to direct you to this page (for example, if it is /feedback, going to localhost:8080/feedback takes you to the page
  </servlet-mapping>


  <servlet>
    <servlet-name>INSERT NAME</servlet-name> -- C
    <servlet-class>com.match.web.(NAME OF YOUR JAVA HTTPSERVLET FILE)</servlet-class>
  </servlet>
  <servlet-mapping>
    <servlet-name>SAME NAME AS ABOVE</servlet-name>
    <url-pattern>/(NAME OF THE ACTION IN YOUR FORM)</url-pattern>
  </servlet-mapping>
  ```

For the second servlet, make sure the url pattern is the same as the action field in the form you created in feedback.jsp. This tells the feedback.jsp form to direct to the java file you made in step 2 which then adds the info to the database. The first servlet exposes the feedback.jsp file and creates a url to access the page. 

5. Last, we need to add our new files to the build and build the web application. In the build.sh file, add this line to build your Java HttpServlet file from step 2. 

javac -classpath WEB-INF/lib/*:WEB-INF/classes -d WEB-INF/classes com/match/web/AddFeedback.java

You may encounter an issue with running sudo ./build.sh you are using Windows to edit build.sh. This might cause issues with carriage return characters and when you try to run it no command runs properly (the first line will be along the lines of "1: cd: can't cd to ./src"). If this happens, you can resolve this by doing the following:

 - Download the program dos2unix on your vagrant machine with: sudo apt-get install dos2unix
 - Run dos2unix build.sh in your vagrant command line

In addition to editing ./build.sh, we want to add a link to the new page in the header bar of the site. In header.tag under WEB-INF/tags, add 
```<li><a href="your url for the jsp page">Whatever you want the link to say</a></li> ``` so that you can navigate to the page from the header.

## **Part 7 (Optional): Deploying to AWS (2 extra credit points)**

More likely than not, you will have to work with a database in the cloud at some point in the future. Here we give you the opportunity to deploy your MatchMaker application to the cloud, turn it into a publicly accessible Website, and get to work with cloud databases a little bit. Note that you can sign up for a free tier trial to use AWS with a new account; however Amazon may charge money to deploy this app. However, you can apply for free Amazon credit as a student (https://www.awseducate.com/Registration) that should cover the costs of the initial deployment. Please note that this application process may take several days for them to get back to you.

 Follow these steps to do this:

1. Open the [Elastic Beanstalk Management Console](https://console.aws.amazon.com/elasticbeanstalk/home)

2. Choose *Create New Application*

3. For *Application Name*, type tomcat-snakes. Choose *Next*.

4. Choose *Web Server Environment*

5. Set the platform to *Tomcat* and choose *Next*.

    * Use the tomcat8/java8 platform (which it should set to by default)

6. Choose *Upload your own* and *Choose File*.

7. Upload *ROOT.war* from your project directory and choose *Next*.

8. Type a unique *Environment URL* and choose *Next*.

9. Check *Create an RDS DB Instance with this environment* and choose *Next*.

10. Set *Instance type* to *t2.nano* and choose *Next*. Choose *Next* again to skip tag configuration.

11. Apply the following RDS settings and choose *Next* (leave the other settings default):

    * DB engine: *postgres*

    * Engine version: *9.6.2 (or whatever the most recent version is)*

    * Instance class: *db.t2.micro*

    * Master username: any username (make sure you know it)

    * Master password: any password (make sure you know it)

12. Choose Next to create and use the default role and instance profile.

13. Choose Launch.

This may take awhile (10 to 15 minutes). After it finishes, your application is in the cloud, but your database it created to go with it is actually empty :(. You need to create the person and match table in the database instance just like you did in your local postgres environment. You can do this by connecting to the database from your a postgresql client. Here are directions for using the psql linux client (which you already have on your virtual machine)

1. Navigate to the configuration tab on your Elastic Beanstalk management console in your environment that you deployed the match application

2. Scroll down to the Data Tier section and click on the link in the RDS card called "endpoint"

3. It should take you to the Amazon RDS portion of the console. From here click on the link for your database. If you have used AWS and have other instances already there you should click on the link for the instance you just made, if not you should only have one link to click on anyways

4. Scroll down to the Connect tab on the page 

5. Here you should see information we’re going to need to connect to the database: Take note of the endpoint name and port number. Make sure under publicly accessible it says "yes" (AWS should do this for you when you deployed with Beanstalk)

6. We need to add a security rule to allow you to connect to your database from your own psql client. Go ahead and click on the link to the security group which is just below the endpoint information. This will take you to a new page in the console.

7. At the bottom of the page, click on the inbound tab and click the edit button

8. Click Add Rule and add a new rule with the following fields:

    1. Type: All Traffic

    2. Protocol: All

    3. Port Range: 0 - 65535

    4. Source: Custom

        1. In the box enter "0.0.0.0/0"

9. Leave the description blank and hit the save button

10.  Now that our rule is set, we should be able to use psql to connect to the database

11. From the command line on your machine type the following to connect:

Psql --host=yourendpointname --port=yourport(should be 5432) --username=username you set previously in deploying --password --dbname=ebdb

Notes:

Your endpoint name should look something like: randomcharacters.morerandomcharacters.us-east-2.rds.amazonaws.com

The dbname should be ebdb by default, if it is not, find the database name on the page for your db instance information

You should get the prompt from ebdb, once there, create your tables.

We won’t go through filling our tables with prepopulated values like we did locally. Test adding people on the register page and generating matches for them to make sure it is working. You will receive credit as long as we can add a person to your cloud deployed application, view added people in the people tab, and generate a match that writes to the match table. Add a line to the end of your part1.txt file with the url to your deployed application to receive extra credit for completing Part 6. 

Don't forget to delete your account (or at least undeploy the Website) after you receive the extra credit --- otherwise Amazon will continue to charge you after your free credits are used up. Alternateively, you can get a real domain name, get users to pay for the app (which means you will probably have to add more features), and cover your costs that way ;)

## **Submission**

To submit the project, zip the matchapp folder into a zip file named matchapp.zip. Please submit your zip file, part1.txt file and ER diagram as separate files on ELMS.

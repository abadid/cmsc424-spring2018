# **Project 3: Matchapp (JDBC Manipulation)**

## **Introduction**

This project should give you all the skills needed to create your own fully functional web page that interfaces with a your own database using JDBC. We will be creating an application that matches uses with other users with similar interests and backgrounds. We will be using Java and Tomcat to make this happen in conjunction with a variation of HTML (JSP) to create webpages. You will be a "Full-stack developer" in this project since you will be dealing with the front-end, the back-end, and the database system components of the application!

## **Relevant Project Files**

To begin this project you will have to pull code from our git repo, ?. Below, we give an overview of the important files that you should know about; all of the other files that are included in the code that you pull are just there to make sure that the application works properly:

* **build.sh**: you should run "./build.sh" in order for your project files to build. This will compile all the necessary files for the application. Make sure you run build as the root user **(sudo)** to have it copy the war file to the tomcat directory properly.

* **src/**

    * ***.jsp**: These are the Java Server Pages. JSP allows Java code to be interleaved with static web markup content (HTML in our case), with the resulting page being compiled and executed on the server to deliver a complete HTML page. Basically Java is being used to dynamically create HTML pages. A good overview/tutorial on JSP can be found at: [https://www.tutorialspoint.com/jsp/jsp_overview.htm](https://www.tutorialspoint.com/jsp/jsp_overview.htm) (however, you can skip the parts of the tutorial on how to set up the enviornment, since we’ve already done that for you). For this project, the only jsp page that you will have to modify in this is **add.jsp**, however, it is a good idea to check out the other jsp files that we are providing you if you want to get a sense of how each page of the app is generated. **(Front-end Component)**

    * **com/match/**

        * **model/**

            * **Match.java:** You must complete this file to interface with the match table in the matchapp database. **(Back-end + DB Component)**

            * **Person.java:** This Java file interfaces with the person table in the matchapp database. We provide basic constructors for a person object but here are several functions missing that you must complete. **(Back-end + DB Component)**

        * **web/**

            * **.java:** These are servlet files that deal with porting over information computed by the **model** files. They help bridge the gap between the back-end and the frontend. **(Back-end + Front-end Components)**

## **Getting Started**

Start the VM with **"vagrant up"**. You will use the database “matchapp” which we create for you. For this database you must create 2 tables as well as a user role. You will see the technical details in the sections below. We will be using tomcat to run our server locally and eventually through AWS. Here are some useful commands to run (run as super user, i.e. “sudo” or “sudo su”):

* systemctl start tomcat: Starts your server

* systemctl status tomcat: Checks status of your server

* systemctl stop tomcat: Stops your server

* ./build.sh:  Builds all necessary files and copies your **ROOT.war** file to the right directory

* tail /opt/tomcat/logs/catalina.out: Checks log file of tomcat server

* tail /opt/tomcat/logs/localhost.(current-date): Checks log file of localhost

## **Schema + User**

 You will have to create 2 tables (person and match) as you have seen in project 0 and 1. The schema is as follows (you must use intuition as well as the **person.sql** file we use to insert into your tables to infer the types):

* **person**

    * **id:** This is the primary key of the table, to represent a unique person. This should be a serial type which auto generates a next unique id to assign to a new person in the table.

    * **first_name:** Must be less than or equal to 12 characters long.

    * **last_name:** Must be less than or equal to 18 characters long.

    * **age:** Must be greater than or equal to 18.

    * **major:** Must be less than or equal to 20 characters long.

    * **gender:** This must be an integer type where you can decide how to map genders to integer values, but you must include a constraint that this column is not null.

    * **seeking_relationship_type:** Must be an integer between 1 and 3.

    * **seeking_gender:** You can decide how to represent this field, but you must include a constraint that this column is not null.

    * **language:** Must be 3 characters or less (e.g. English could be represented as ENG).

    * **county:** Must be less than or equal to 20 characters long.

    * **approval_rating:** Must be a floating point number with a precision of 2 digits after the decimal. All users start with a rating of 1.0, and the max is 9.99. But this value can go up or down depending on whether they treat the other users on the app with politeness, kindness, and respect. 

* **match**

    * **id1:** This must reference the person tables id attribute. **(Primary Key)** 

    * **id2:** This must also reference the person tables id attribute. **(Primary Key)**

    * **date_of_match:** Must use a date datatype

    * **Rating:** Must be a decimal value.

You will also have to include one more attribute into the person table with any type of your choice. Once you create your tables, you can run /i person.sql in matchapp in psql to populate the person database with people. You will also have to create a user with name **"matchmaker"** and password **“kingofthenorth”** and you must grant all permissions to that user to access your database and tables as it will be the one doing the database manipulation. You should find the commands to do this (check the textbook and past projects in this class and online resources).

## **Part 1: Person.java (Back-end + DB)**

You will need to complete the following functions in Person.java model file that interface with the person table in the matchapp database. We have completed a few of these methods including the Constructors as well as functions that interface with your database remotely and locally:

* **getPeople():** Get a list of all the people in the database.

* **getPerson(id):** Get a specific person via id.

* **addPerson(*all person parameters*):** Add a person using all the parameters.

* **getMatchedPeople(id):** Get the top 5 matches for a specific person via id.

## **Part 2: Match.java (Back-end + DB)**

You will have to complete most of this file. Here are some general things you will probably need to write:

* Constructors for the Match object to be written to the database.

* Functions to make data retrieval easy.

* Functions to connect with the database remotely and locally (this should be similar to the ones in Person).

You will be **required** to write these functions:

* **getMatchesFor(id):** Get the matches from the match table via the id

* **At least these fields and getter methods:**

    * **getMatchedID():** Get the id of the person that the user is matched with.

    * **getDate():** Get date of match.

    * **getRating():** Get the rating of a match.

## **Part 3: Web Servlets (AddPerson.java) (Back-end + Front-end)**

Now that you have successfully finished the majority of the Back-end Components you will now have to hook up the the Back-end with the Front-end Components. This process will be done via the Java files in the **web** directory. We will only be editing the AddPerson.java file and this process is trivial. All you have to do is make sure you alter the file to accept a new field that you added to the person table and then add it to the addPerson method call at the end of the file. See the comments in the file for the specific things to do.

## **Part 4: JSP Files (add.jsp) (Front-end)**

The next step is to add the input field for the attribute you decided to create in the person table on the add a person page. You can model it just like the other input fields already there on the page. See the add.jsp file and its comments for exactly where to modify and insert the form field. Whatever field you decide to add, make sure you do not set a not null constraint on the person table for the field. You can see more about html form elements online here: [https://www.w3schools.com/html/html_form_elements.asp](https://www.w3schools.com/html/html_form_elements.asp)

## **Part 5: Adding a Page**

Finally, we want you to put all of these steps together and add a new page to MatchMaker. The purpose of this page is to let users give feedback on their matches which will increase or decrease their matches approval rating. Follow these steps to create and add the page to your website.

Note: We are giving you some free range here so we will not be grading you strictly on exactly how your html page looks. We will only be testing to see that your page is added and visible on the website and that it meets the functional requirements discussed below. The purpose of this part is to give you experience adding a new feature to the website from start to finish.

1. First, go to the given file feedback.jsp. This file will contain the html we want to display for the page. It is mostly blank right now. You will need to add a form element to display input boxes for the person’s id who is giving feedback and their match id they are giving feedback for, in addition to a radio button to designate whether they approve or disapprove of the match. View the comments in the file for more guidance.

2. Now we need to set up an HttpServlet file to display and handle the form data for the jsp file. You want to create a new java file that will extend HttpServlet and contain the void doPost(HttpServletRequest request, HttpServletResponse response) method. This java file should be placed in the com.match.web directory. Look at the AddPerson.java file for a template on how to create this. Within this file, you need to get the parameters you pass from the request (which will be each field in the form submitted by the user in feedback.jsp), make a call to a method in Match.java that you create to check and submit the new data to the database (described in step 3), and send the response back to the feedback.jsp page where the user can enter another piece of feedback information. If you are really confused on how to do this, view the comments in AddPerson.java that explain what each part of it does and model your file just like it only adapted to the different fields and methods you use.

3. Now we need to add the method in Match to update the approval_rating field in the database appropriately. How much you increment or decrement this field is entirely up to you, but it must be a constant amount (for example, +5 for good and -3 for bad). However, it is required that a user cannot give feedback for someone that they are not matched with. This means the userID and the person matched ID must be an entry in the matches database to be able to give a good or bad rating for their match. If this condition is not met or either of the ids is not in the person table at all, do nothing, otherwise update the approval_rating of the matched person.

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

Also, we want to add a link to the new page in the header bar of the site. In header.tag under WEB-INF/tags, add 
```<li><a href="your url for the jsp page">Whatever you want the link to say</a></li> ``` so that you can navigate to the page from the header.

## **Part 6 (Optional): Deploying to AWS**

More likely than not, you will have to work with a database in the cloud at some point in the future. Here we give you the opportunity to deploy your MatchMaker application to the cloud and get to work with cloud databases a little bit. Follow these steps to do this:

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

We won’t go through filling our tables with prepopulated values like we did locally. Test adding people on the register page and generating matches for them to make sure it is working. You will receive credit as long as we can add a person to your cloud deployed application, view added people in the people tab, and generate a match that writes to the match table. Add a comment in your Person.java file with the url to your deployed application to receive extra credit for completing Part 6. 


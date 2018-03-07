package com.match.model;
import java.sql.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.lang.NullPointerException;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import com.fasterxml.jackson.core.*;
import com.fasterxml.jackson.databind.*;
import java.io.File;
import java.io.IOException;

public class Person {

	static Connection con = null;
  /*Fields for a person entry in the person table
  remember to add one of your own choice of fields 
  */
	private String firstName, lastName, major, language, county;
	private int age, gender, seeking_relationship, seeking_gender;

  private double approval_rating;

  //used for logging output, see catalina.out for log files
  private static final Logger logger = LogManager.getLogger("match");
	static JsonFactory factory = new JsonFactory();

	public Person() {

	}

  //constructor for person if only need to display the name
	public Person(String firstName, String lastName) {
		this.firstName = firstName;
		this.lastName = lastName;
	}

  //constructor for person with all fields
	public Person(String firstName, String lastName, int age, String major, int gender, int seeking_relationship, int seeking_gender, 
					String language, String county, double approval_rating) { 
		this.firstName = firstName;
		this.lastName = lastName;
		this.age = age;
		this.major = major;
		this.gender = gender;
		this.seeking_relationship = seeking_relationship;
		this.seeking_gender = seeking_gender;
		this.language = language;
		this.county = county;
		this.approval_rating= approval_rating;
	}

	public String getFirstName() {
		return firstName;
	}

	public String getLastName() {
		return lastName;
	}

  //Return an array of all the people in the person table
  //You will need to make a SQL call via JDBC to the database to get all of the people
  //Since the webpage only needs to display the person's first and last name, only those fields 
  //of the Person object need to be instantiated (i.e., you can use the second of the three Person constructors above) 
	public static Person[] getPeople() {
	    
	     con = getConnection();
	     
	     if (con == null) {
	     logger.warn("Connection Failed!");
	       Person failed = new Person("Connection", "Failed");
	       return new Person[] { failed };
       }
	      

	    return new Person[]{} ; //remove this line and replace with your code
  }

  /* For every person record in the database, search each of its character fields to see if input query is a substring of any of them
  Return everything that matches with every char/varchar column. This should be case senstive in finding substring matches

  For example if we have 2 people with:
  First: Alex, Last: Westmore, Major: Biology, County: Howard, Language: ENG
  First: Dave, Last: Howland, Major: Geology, County: Frederick, Language: ENG

  If we query with the string: "How", the Person array that is returned contains both people 
  If we query with the string: "more", the Person array that is returned contains just Alex
  If we query with the string: COUNT, the Person array is empty

  The order of the people returned does not matter

  If no rows in the database are found with a substring match, you should return an empty array of Person.

  */

  public static Person[] getPersonSearch(String query) {
  		 
      con = getConnection();
      
      if (con == null) {
      logger.warn("Connection Failed!");
        Person failed = new Person("Connection", "Failed");
        return new Person[] { failed };
      }
      

      return new Person[]{}; //remove this line and replace with your code
  }	

  /*This should return a Person object with all of its fields instatiated 
  for the person with the given id in the person table. Note that since id is unique, there
  will only be one person ever returned by this method 

  Return a person with the first name "No" and the last name "Matches" if
  the person with the id does not exist.
  */
  public static Person getPerson(String id) {
    
      con = getConnection();
        
      if (con == null) {
      logger.warn("Connection Failed!");
        Person failed = new Person("Connection", "Failed");
        return failed;
      }
     

      return new Person("Blank", "Person");  //remove this line and replace with your code
  }

  /*Add a person to the database with all of the fields specified
  
  If the connection fails or the person was not inserted, return -1, otherwise return the id of the person that you inserted

  You must use a prepared statement to insert the person
  */
  public static int addPerson(String first, String last, int age, String major, int gender, int seeking_relationship, int seeking_gender, 
  								String language, String county, double approval_rating) {

    return -1;  //remove this line and replace with your code
  }

  /*Return a list of the best 5 matches in the database for the person with the given id based on the score method that
    you write later in this file (see below).
    
    A person is not allowed to be matched with herself or himself.

  You must write these matches to the matches table including the date and their score

  Note: Once someone has already matched with someone, do not return them again. This means your method will return the
  top 5 matches for that person in the entire database on the first call. On the second call it should return the next
  5 best matches, and so on.
  
  
  If the person with id does not exist, return a Person array with one person with the first name "No" and last name "Matches"
  If the person has no matches, return an empty Person array
  */

  public static Person[] getMatchedPeople(String id) {
    
      con = getConnection();
      // If that fails, send dummy entries
      if (con == null) {
      logger.warn("Connection Failed!");
        Person failed = new Person("Connection", "Failed");
        return new Person[] { failed };
      }
      

      return new Person[]{new Person("No", "Matches")};  //remove this line and replace with your code
     
  }


  /* Fill in this method to compute the match score between 2 people. 
  How you score is up to you, but you must use all fields in person 
  except for the name and id fields in some way.

  This has to be deterministic (not random) which means the same 2 people must generate
  the same score every time the method is called
  */
  public static int computeMatchScore (Person p, Person alt){
    return 0;  //remove this line and replace with your code
  }

  private static Connection getConnection() {
    // Return existing connection after first call
    if (con != null) {
      return con;
    }
    logger.trace("Getting database connection...");
    // Get RDS connection from environment properties provided by Elastic Beanstalk
    con = getRemoteConnection();
    // If that fails, attempt to connect to a local postgres server
    if (con == null) {
      con = getLocalConnection();
    }
    // If that fails, give up
    if (con == null) {
      return null;
    }
    // Attempt to initialize the database on first connection
    //initDatabase();
    return con;
  }

  //Used for AWS connection to DB, not used locally!
  private static Connection getRemoteConnection() {
    /* Read database info from /tmp/database.json (advanced, more secure option)
    * - Requires database.config to be moved into .ebextensions folder and updated to 
    * point to a JSON file in an S3 bucket that the instance profile has permission to read.
    */
    try {
      /* Load the file and create a parser. If the project is not configured to store
      * database credentials in S3, fail out and try the next method.
      */
      File databaseConfig = new File("/tmp/database.json");
      JsonParser parser = factory.createParser(databaseConfig);
      // Load the Postgresql driver class
      Class.forName("org.postgresql.Driver");
      /* Read the first value in the JSON document with Jackson. This must be a full JDBC
      *  connection string a la jdbc:postgresql://hostname:port/dbName?user=userName&password=password
      */
      JsonToken jsonToken = null;
      while ( jsonToken != JsonToken.VALUE_STRING ) 
        jsonToken = parser.nextToken();
      String jdbcUrl = parser.getValueAsString();
      // Connect to the database
      logger.trace("Getting remote connection with url from database config file.");
      Connection con = DriverManager.getConnection(jdbcUrl);
      logger.info("Remote connection successful.");
      return con;
    }
    catch (IOException e) { logger.warn("Database configuration file not found. Checking environment variables.");}
    catch (ClassNotFoundException e) { logger.warn(e.toString());}
    catch (SQLException e) { logger.warn(e.toString());}

    // Read database info from environment variables (standard configration)
    if (System.getProperty("RDS_HOSTNAME") != null) {
      try {
      Class.forName("org.postgresql.Driver");
      String dbName = System.getProperty("RDS_DB_NAME");
      String userName = System.getProperty("RDS_USERNAME");
      String password = System.getProperty("RDS_PASSWORD");
      String hostname = System.getProperty("RDS_HOSTNAME");
      String port = System.getProperty("RDS_PORT");
      String jdbcUrl = "jdbc:postgresql://" + hostname + ":" + port + "/" + dbName + "?user=" + userName + "&password=" + password;
      logger.trace("Getting remote connection with connection string from environment variables.");
      Connection con = DriverManager.getConnection(jdbcUrl);
      logger.info("Remote connection successful.");
      return con;
    }
    catch (ClassNotFoundException e) { logger.warn(e.toString());}
    catch (SQLException e) { logger.warn(e.toString());}
    }
    return null;
  }

  /* Connect to the local database for development purposes
    Your database must be named "matchapp" and you must make a user "matchmaker" with the password "kingofthenorth"
  */
  private static Connection getLocalConnection() {
    try {
      Class.forName("org.postgresql.Driver");
      logger.info("Getting local connection");
      Connection con = DriverManager.getConnection(
            "jdbc:postgresql://localhost/matchapp",
            "matchmaker",
            "kingofthenorth");
      logger.info("Local connection successful.");
      return con;
    }
    catch (ClassNotFoundException e) { logger.warn(e.toString());}
    catch (SQLException e) { logger.warn(e.toString());}
    return null;
  }


}

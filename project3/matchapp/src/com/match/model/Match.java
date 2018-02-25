package com.match.model;
import java.sql.*;
import java.lang.NullPointerException;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import com.fasterxml.jackson.core.*;
import com.fasterxml.jackson.databind.*;
import java.io.File;
import java.io.IOException;

public class Match {
	static Connection con = null;

  /*
  TODO: 
  Write getMatchesFor(String id) function
  Add fields and write getter methods:
    getMatchedID(): Get the current match id.
    getDate(): Get date of match.
    getRating(): Get the rating of a match.

  Write method for feedback page in part 5
  Write any other method you think would be useful or needed
  */

  public int getMatchedID() {
    return 0;
  }

  public String getDate() {
    return "";
  }
  public int getRating() {
    return 0;
  }

	private static final Logger logger = LogManager.getLogger("match");
	static JsonFactory factory = new JsonFactory();


	public static Match[] getMatchesFor(String id) {
		return new Match[]{};
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
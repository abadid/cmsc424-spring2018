package com.match.web; 
import com.match.model.Person;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import javax.servlet.jsp.tagext.SimpleTagSupport;
import java.io.*;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class AddPerson extends HttpServlet {
  private static final Logger logger = LogManager.getLogger("match");
  public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException, NumberFormatException {
    
    //Gets the string data of all of the fields in the form to register

    //TODO: Make sure you get your field here that you create as well
    String first = request.getParameter("first");
    String last = request.getParameter("last");
    String age = request.getParameter("age");
    String major = request.getParameter("major");
    String gender = request.getParameter("gender");
    String relationship = request.getParameter("relationship");
    String seeking = request.getParameter("seeking");
    String language = request.getParameter("lang");
    String county = request.getParameter("county");
    //get your parameter from the request here 

    //get integer values of string fields 
    int age_int = Integer.parseInt(age);
    int gender_int = Integer.parseInt(gender);
    int relationship_int = Integer.parseInt(relationship);
    int seeking_int = Integer.parseInt(seeking);
  

    //check to see if the values entered are valid input, if not, redirects the response to the invalid input page
    if (first.length() > 12 || last.length() > 18 || age_int < 18 || major.length() > 20 || relationship_int > 3 || 
        relationship_int < 1 || language.length() > 3 || county.length() > 20) {
      response.sendRedirect("invalidinput");
    }
    else {
        //Here we make the call to the method in Person that connects to the database and inserts the person with the given values
        //Your addPerson method should accept one more argument at the end which contains the field you created

        int id = Person.addPerson(first, last, age_int, major, gender_int, relationship_int, seeking_int, language, county, 1.0);
        
        //Sends the response to the add page so that another person can be added. ID is passed as a parameter to display the id 
        //for the new user to refer to get and view matches
        response.sendRedirect("add?id=" + id);
    }
    
    
  }
}
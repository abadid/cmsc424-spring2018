package com.match.web; 
import com.match.model.Person;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import javax.servlet.jsp.tagext.SimpleTagSupport;
import java.io.*;

public class ListPeople extends SimpleTagSupport {
  Person[] people = null;
  String query = "";

  public void setQuery(String query) {
    this.query = query;
  }

  public void doTag() throws JspException, IOException {
    //if the query is changed, search based on the query
    if (!query.equals(""))
      //You write this method
      people = Person.getPersonSearch(query);
    else //just get all of the people from the person table
      //You write this method
      people = Person.getPeople();
    
    //We will only display first 10 for webpage
    int length = people.length;
    if(length > 10) {
      length = 10;
    }

    for (int i = 0; i < length; i++) {
      getJspContext().setAttribute("first", people[i].getFirstName());
      getJspContext().setAttribute("last", people[i].getLastName());
      getJspBody().invoke(null);
    }
  }
}

package com.match.web;
import com.match.model.Person;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import javax.servlet.jsp.tagext.SimpleTagSupport;
import java.io.*;

public class GenerateMatch extends SimpleTagSupport {
  Person[] people = null;
  private String id;
  private static final Logger logger = LogManager.getLogger("match");

  public void setId(String id) {
    this.id = id;
  }


  public void doTag() throws JspException, IOException {
    //You write Person.getMatchedPeople in Person class
    people = Person.getMatchedPeople(id);

    for (int i = 0; i < people.length; i++) {
      getJspContext().setAttribute("first", people[i].getFirstName());
      getJspContext().setAttribute("last", people[i].getLastName());
      getJspBody().invoke(null);
    }
  }
}

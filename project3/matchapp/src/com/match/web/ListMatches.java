package com.match.web; 
import com.match.model.Match;
import com.match.model.Person;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;
import javax.servlet.jsp.tagext.SimpleTagSupport;
import java.io.*;

public class ListMatches extends SimpleTagSupport {
  Match[] matches = null;
  String id = "";

  public void setId(String id) {
    this.id = id;
  }

  public void doTag() throws JspException, IOException {
    //You write getMatchesFor in Match class
    matches = Match.getMatchesFor(id);

    int length = matches.length;

    for (int i = 0; i < length; i++) {
      Person matchedPerson = Person.getPerson(matches[i].getMatchedID() + "");
      getJspContext().setAttribute("first", matchedPerson.getFirstName());
      getJspContext().setAttribute("last",  matchedPerson.getLastName());
      getJspContext().setAttribute("date",  matches[i].getDate());
      getJspContext().setAttribute("rating", matches[i].getRating());
      getJspBody().invoke(null);
    }
  }
}
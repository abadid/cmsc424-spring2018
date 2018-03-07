<%@ taglib prefix="tagfiles" tagdir="/WEB-INF/tags" %>

<html>

  <head>
    <meta charset="utf-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    
    <link href="css/bootstrap.css" rel="stylesheet" />
    <link href="css/match.css" rel="stylesheet" />

    <title>Register to find your match!</title>
  </head>

  <body>
    <tagfiles:header />

    <div class="container heading">
      <h2>Enter Your Information</h2>
      <form action="add.do" method="post">
        <div class = "row">
          <div class="column">
            <h3>Personal Information</h3>
            First Name: <br />
            <input type="text" size="18" name="first" required  />
            <br />
            Last Name: <br />
            <input type="text" size="18" name="last" required/>
            <br />
            Age: <br />
            <input type="text" size="18" name="age" />
            <br/>
            
            Major: <br />
            <input type="text" size="18" name="major" />
            <br/>
          </div>

          <div class= "column">
            <h3> Relation Information </h3>
            
            Gender: <br />
            <select name = "gender">
              <option value="1">Add your gender here</option>
              <option value="2">Add your gender here</option>
            </select>
            </br>
 
            Relationship Type: <br />
            <input type="radio" name ="relationship" value="1" required>Date</input>
            <br />
            <input type="radio" name="relationship" value="2">Friend</input>
            <br />
            <input type="radio" name="relationship" value="3" style="margin-bottom: 30px;">Study budy</input>
            <br />

            Gender Seeking: <br />
            <select name = "seeking">
              <option value="1">Add your gender here</option>
              <option value="2">Add your gender here</option>
            </select>
            <br/>
          </div>

          <div class = "column">
            <h3> Other Information </h3>
            Language: (3 characters) <br />
            <input type="text" size="18" name="lang" required/>
            <br/>
            County: <br />
            <input type="text" size="18" name="county" />
            <br/>
            <!-- ADD YOUR INPUT FIELD FOR THE FIELD YOU ADDED TO THE PERSON DATABASE RIGHT HERE-->
          </div>
        </div>

        <div>
          <input type="submit" value="Submit" />
        </div>

      </form>
    </div>
    <div>
      <% 
        String id =  request.getParameter("id");
        if(id == null) {
          id = "";
        }
        else {
          id = "Your ID is " + id + " - Remember it!";
        }
      %>
      <p><%= id %></p>


    </div>

    <div class="sample">
      <p>MatchMaker</p>
    </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
  </body>
</html>


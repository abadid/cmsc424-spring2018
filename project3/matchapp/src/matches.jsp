<%@ taglib prefix="tagfiles" tagdir="/WEB-INF/tags" %>
<%@ taglib prefix="match" uri="match-functions" %>
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    
    <link href="css/bootstrap.css" rel="stylesheet" />
    <link href="css/match.css" rel="stylesheet" />

    <title>Match List</title>
  </head>
  <body>
    <tagfiles:header />
    
    <div class="container heading">
      <form action="viewmatch" method="get">
        Enter your id to see your matches: 
        <br />
        <input type="number" name="id" />
        <input type="submit" value="Submit" />
      </form>

      <h2>Match List</h2>
      <table align="center">
        <tr><td><u>First</u></td><td><u>Last</u></td><td><u>Date</u></td><td><u>Rating</u></td></tr>
        <match:listmatches id = "${id}">
          <tr><td>${first}</td><td>${last}</td><td>${date}</td><td>${rating}</td></tr>
        </match:listmatches>
      </table>
    </div>


    <div class="sample">
      <p>MatchMaker</p>
    </div>
  </body>
</html>
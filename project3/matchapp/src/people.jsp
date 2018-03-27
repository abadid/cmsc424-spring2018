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

    <title>People List</title>
  </head>
  <body>
    <tagfiles:header />
    
    <div class="container heading">
      <form action="search" method="get">
        Search for Person: 
        <input type="text" name="query" />
        <input type="submit" value="Submit" />
      </form>

      <h2>People List</h2>
      <table align="center">
        <match:listpeople query="${query}">
          <tr><td>${first}</td><td>${last}</td></tr>
        </match:listpeople>
      </table>
    </div>


    <div class="sample">
      <p>MatchMaker</p>
    </div>
  </body>
</html>
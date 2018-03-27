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

    <div class="container GenerateMatch">
      <div class="container heading">
        <h2>Enter Your ID to see your matches</h2>
        <form action="searchmatch" method="get">
         Enter your id to see your matches: 
          <br />
          <input type="number" name="id" />
          <input type = "submit" value = "Generate Match!" />

        </form>
        <table align="center">
          <match:generatematch id = "${id}">
            <tr><td>${first}</td><td>${last}</td></tr>
          </match:generatematch>
        </table>
    </div>

    <div class="sample">
      <p>MatchMaker</p>
    </div>
  </body>
</html>

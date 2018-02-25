<%@ taglib prefix="tagfiles" tagdir="/WEB-INF/tags" %>

<html>

  <head>
    <meta charset="utf-8"/>
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    
    <link href="css/bootstrap.css" rel="stylesheet" />
    <link href="css/match.css" rel="stylesheet" />

    <title>Feedback</title>
  </head>

  <body>
    <tagfiles:header />

    <div class="container heading">
      <h2>Match == good or match == bad?</h2>
      <!-- Add a form element with the following input fields:
            your ID - The id of the user who wants to give feeback to their match
            match ID - The id of the match the user wants to review
            Good or Bad - A radio button with the options of saying the match is good or the match is bad

            You will need to set the action attribute of the form to the url of the service that you create 
            in later steps. 
      -->
    </div>

    <div class="sample">
      <p>MatchMaker</p>
    </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
  </body>
</html>

